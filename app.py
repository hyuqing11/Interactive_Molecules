import streamlit as st
import numpy as np
from ase import build
from transformations import transform_positions
from calculations import calculation_functions, apply_transformation
from visualizations import display_3d_molecule, show_array
from stmol import showmol

# Main Streamlit App
st.title("Interactive Molecular Transformation")

# Molecule selection
molecule_choice = st.sidebar.selectbox("Select Molecule", ["O3", "CH4", "O2", "H2O", "CO2", "NH3", "CH3CH2OCH3"])
molecule = build.molecule(molecule_choice)
positions = molecule.positions

# Transformations
xrot = st.sidebar.slider("Rotation (degrees)", 0, 360, 0)
xtrans = st.sidebar.slider("Translation", -10, 10, 0)
swap = st.sidebar.slider("Swap Atom Index with First Atom", 0, len(positions) - 1, 0)

# Calculations
funcs = calculation_functions()
selected_func = st.sidebar.selectbox("Select Calculation Function", list(funcs.keys()))
transformed_positions = transform_positions(positions, xrot, xtrans, swap)
results = apply_transformation(transformed_positions, funcs[selected_func])


# Display results
col1, col_gap, col2 = st.columns([3, 0.1, 1.5])
with col1:
    st.markdown("<h4 style='color:#A9A9A9;'>Input Data:</h4>", unsafe_allow_html=True)
    if isinstance(results, tuple):
        for result in results:
            st.plotly_chart(show_array(result,width=500, height=500))
    else:
        st.plotly_chart(show_array(results,width=500, height=500))

# 3D Visualization
with col2:
    st.markdown("<h4  style = color:#A9A9A9;'>Molecular Visualization:</h4>", unsafe_allow_html=True)
    molecular_view = display_3d_molecule(molecule, transformed_positions)
    showmol(molecular_view,height=400, width=400)
    st.markdown("<h4 style=color:#A9A9A9;'>Transformed Positions:</h4>", unsafe_allow_html=True)
    st.write(transformed_positions)