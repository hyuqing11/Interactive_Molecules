import torch
from nn_test import compute_D_i, GNetwork
from GNN import GNN
import numpy as np


def DeepPot_SE(positions,input_dim=1,hidden_dim=32,output_dim=4):
    torch.manual_seed(42)
    positions = torch.Tensor(positions)
    # Instantiate G networks for embeddings
    G_i1 = GNetwork(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim)
    G_i2 = GNetwork(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim)

    D_i = compute_D_i(positions, G_i1, G_i2)


    return D_i.squeeze(0).detach().numpy()


def DimnetPlus(positions):
    positions = torch.Tensor(positions)
    gnn = GNN()
    rbf,sbf =gnn.DimnetPlusLocalEnvironment(len(positions),positions)
    return rbf.detach().numpy(), sbf.detach().numpy()

def center(pos):
    # Subtract centre of mass
    return pos - pos.sum(axis=0) / len(pos)

def sum_coords(pos):
    # Sum the coordinates along x, y and z
    return pos.sum(axis=0).reshape(3, 1)

def norms(pos):
    # Get norms of pos vectors
    return (pos**2).sum(axis=1).reshape(-1, 1)

def invariance(pos):
    trans = center(pos)
    rots = norms(trans)
    return rots.sum().reshape(-1, 1)



def calculation_functions():
    return {
        "None": lambda x: x,
        "Center": center,
        "Sum Coordinates": sum_coords,
        "Norms": norms,
        "Invariance": invariance,
        "DeepPot_SE": DeepPot_SE,
        "DimnetPlus": DimnetPlus,
        "CustomFunc": lambda x: x  # Placeholder for custom function
    }


def apply_transformation(pos, function):
    return function(pos)
