import torch
import torch.nn as nn
import torch.nn.functional as F
import streamlit as st
class LocalEmbeddingNetwork(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=32, output_dim=16):
        super(LocalEmbeddingNetwork, self).__init__()

        # Define the neural network layers
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Forward pass through the network
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)  # No activation on the output layer (linear transformation)
        return x

    # Function to construct R_i matrix with atom-type encoding
class GNetwork(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=32, output_dim=8):
        super(GNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Define the switching function s(r) with piecewise definition
def switching_function(r, r_s=1.0, r_c=5.0):
    x = (r - r_s) / (r_c - r_s)
    s_r = torch.where(
        r < r_s,
        1.0 / r,  # Case 1: r < r_s
        torch.where(
            (r >= r_s) & (r < r_c),
            (1.0 / r) * (x**3 * (-6 * x**2 + 15 * x - 10) + 1),  # Case 2: r_s <= r < r_c
            torch.zeros_like(r)  # Case 3: r >= r_c
        )
    )
    return s_r



# Function to construct R_i matrix using distances and dot products
def construct_R_i_matrix(positions, r_s=9.0, r_c=10.0):
    central_atom = positions[0:1, :]  # Central atom (i)
    neighbor_atoms = positions[1:, :]  # Neighboring atoms

    # Compute relative positions and distances
    relative_positions = neighbor_atoms - central_atom
    distances = torch.norm(relative_positions, dim=1, keepdim=True)

    # Apply switching function s(r)
    s_r = switching_function(distances, r_s, r_c)

    # Construct R^i by normalizing relative positions and multiplying by s(r)
    normalized_positions = relative_positions / (distances + 1e-8)  # Avoid division by zero
    weighted_positions = s_r * normalized_positions
    R_i = torch.cat([s_r, weighted_positions], dim=1)
    #st.write(R_i.squeeze(0).detach().numpy())# (N_neighbors, 4)
    return R_i


# Function to compute D^i matrix using the embedding networks G^i1 and G^i2
def compute_D_i(positions, G_i1, G_i2, N_c=9):
    # Step 1: Construct R^i matrix
    R_i = construct_R_i_matrix(positions).unsqueeze(0)  # Shape (1, N_neighbors, 4)

    # Step 2: Apply G networks to each s(r_ij) component to get embeddings
    s_r = R_i[:, :, :1]  # Extract the s(r_ij) part from R^i
    G_i1_output = G_i1(s_r)  # Shape (1, N_neighbors, M)
    G_i2_output = G_i2(s_r)  # Shape (1, N_neighbors, M)

    # Step 3: Compute D^i using product without symmetrization
    G_i1_T = G_i1_output.transpose(1, 2)  # Transpose for batch matrix multiplication
    R_i_product = torch.bmm(R_i, R_i.transpose(1, 2))  # R_i * R_i^T
    D_i = (1 / N_c ** 2) * torch.bmm(G_i1_T, torch.bmm(R_i_product, G_i2_output))

    return D_i

