
import py3Dmol

from ase import build
from stmol import showmol,add_sphere


import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from scipy.spatial.transform import Rotation

import torch
import streamlit as st
from nn_test import compute_D_i,GNetwork

torch.set_default_dtype(torch.float32)
np.set_printoptions(precision=2)




def show_array(positions, calc=None,width=1500, height=1500):
    if calc is None:
        calc = lambda x: x
        fig = px.imshow(calc(positions), color_continuous_scale='Viridis', zmin=-5, zmax=5,width=width, height=height)
        widget = go.Figure(fig)
    else:

        #fig = px.imshow(calc(positions), color_continuous_scale='RdBu', zmin=-5, zmax=5,width=width, height=height)
        fig = px.imshow(calc(positions), color_continuous_scale='Viridis', width=width, height=height)
        widget = go.Figure(fig)

    return widget

def update_positions(positions, xrot=0, xtrans=0, swap=0):
    pos = positions.copy()
    index = 1

    # Permute
    if swap:
        pos[[swap, index]] = pos[[index, swap]]

    # Translate
    if xtrans:
        pos[:, 0] += xtrans

    # Rotate
    if xrot:
        rot = Rotation.from_euler('x', [xrot], degrees=True)
        pos = rot.apply(pos)

    return pos

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


def relative_positions(positions):
    num_atoms = len(positions)
    # Initialize a matrix to store pairwise distances
    distances = np.zeros((num_atoms, num_atoms))
    R_matrix = np.zeros((num_atoms,num_atoms,3))
    R_new = np.zeros((num_atoms, num_atoms,4))

    # Calculate pairwise distances
    for i in range(num_atoms):
        for j in range(num_atoms):
            if i !=j:
                distances[i, j] = np.linalg.norm(positions[i] - positions[j])
                R_matrix[i,j] = positions[i] - positions[j]
                R_new[i,j,0] = 1/distances[i,j]
                R_new[i,j,1:] = R_matrix[i,j]/distances[i,j]**2

    return distances, R_matrix, R_new

def DeepPot_SE(positions,input_dim=1,hidden_dim=32,output_dim=4,M1=3):
    torch.manual_seed(42)
    positions = torch.Tensor(positions)
    # Instantiate G networks for embeddings
    G_i1 = GNetwork(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim)
    G_i2 = GNetwork(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim)

    D_i = compute_D_i(positions, G_i1, G_i2)


    return D_i.squeeze(0).detach().numpy()





def display_3d_molecule(molecule,positions,calc=None):
    if calc is None:
        calc = lambda x: x

    #positions = molecule.positions
    #positions = calc(positions)
    symbols = molecule.get_chemical_symbols()
    # Define colors and radii for each element
    atom_properties = {
        'C': {'color': '0x777777', 'radius': 0.7},
        'H': {'color': '0xFFFFFF', 'radius': 0.3},
        'O': {'color': '0xFF0D0D', 'radius': 0.6},
        'N': {'color': '0x3050F8', 'radius': 0.65},
        # Default properties for unspecified elements
        'default': {'color': '0xCCCCCC', 'radius': 0.5}
    }

    # Initialize py3Dmol view
    view = py3Dmol.view(width=400, height=400)
    #view.addModel('', 'xyz')  # Empty model to start

    for symbol, pos in zip(symbols, positions):

        properties = atom_properties.get(symbol, atom_properties['default'])
        color = properties['color']
        radius = properties['radius']
        add_sphere(view,spcenter=[pos[0],pos[1],pos[2]],radius=radius,spColor=color)# Default to gray if unknown atom


    view.setStyle({'stick': {}})
    # Define a fixed position for the label in the corner

    view.zoomTo()

    return view

# Main Streamlit App
#st.markdown("<h1 style='font-size:40px; color:#A9A9A9; text-align:center;'>Interactive Molecular Transformation</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size:40px; color:#A9A9A9; text-align:center; margin-bottom: 40px;'>Interactive Molecular Transformation</h1>", unsafe_allow_html=True)
st.sidebar.header("Molecule Selection")
molecule_choice = st.sidebar.selectbox(
    "Select Molecule",
    ("O3","CH4", "O2", "H2O", "CO2", "NH3", "CH3CH2OCH3")
)

# Build the selected molecule
molecule = build.molecule(molecule_choice)
# Generate and view the molecule


positions = molecule.positions

# Sliders for transformations
st.sidebar.header("Transformations")
xrot = st.sidebar.slider("Rotation (degrees)", 0, 360, 0, step=1)
xtrans = st.sidebar.slider("Translation", -10, 10, 0, step=1)
swap = st.sidebar.slider("Swap Atom Index with First Atom", 0, len(positions) - 1, 0, step=1)

# Transformation choice
transform_choice = st.sidebar.selectbox(
    "Select Calculation Function",
    ("None", "Center", "Sum Coordinates", "Norms", "Invariance","DeepPot_SE")
)

# Update positions based on transformations
transformed_positions = update_positions(positions, xrot, xtrans, swap)

# Select calculation
calc_functions = {
    "None": lambda x: x,
    "Center": center,
    "Sum Coordinates": sum_coords,
    "Norms": norms,
    "Invariance": invariance,
    "DeepPot_SE": DeepPot_SE
}

# Show transformed array
# Show transformed array in the first column and transformed positions in the second
#col1, col_gap, col2, col3 = st.columns([3, 0.1, 2, 1.5])
col1, col_gap, col2 = st.columns([3, 0.1, 1.5])
with col1:
    st.markdown("<h4 style='color:#A9A9A9;'>Input Data:</h4>", unsafe_allow_html=True)
    fig = show_array(transformed_positions, calc=calc_functions[transform_choice], width=500, height=500)
    st.plotly_chart(fig)


#with col2:
    #st.markdown("<h4 color:#A9A9A9;'>Transformed Positions:</h4>", unsafe_allow_html=True)
    #st.write(transformed_positions)
# Render the 3D molecular visualization


with col2:
    #st.markdown("<h4 style='font-size:18px; color: #333;'>3D Molecular Visualization</h4>", unsafe_allow_html=True)
    st.markdown("<h4  style = color:#A9A9A9;'>Molecular Visualization:</h4>", unsafe_allow_html=True)
    mol_view = display_3d_molecule(molecule,transformed_positions, calc=calc_functions[transform_choice])
    showmol(mol_view, height=400, width=400)
    st.markdown("<h4 style=color:#A9A9A9;'>Transformed Positions:</h4>", unsafe_allow_html=True)
    st.write(transformed_positions)
