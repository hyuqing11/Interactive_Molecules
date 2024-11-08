import streamlit as st
import numpy as np
from ase import build
from transformations import transform_positions
from calculations import calculation_functions, apply_transformation
from visualizations import display_3d_molecule, show_array
from stmol import showmol
from custom_function_handler import handle_custom_function
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
selected_func_name = st.sidebar.selectbox("Select Calculation Function", list(funcs.keys()))

# Show input fields for custom function only if "CustomFunc" is selected
'''if selected_func_name == "CustomFunc":
    st.sidebar.header("Add Your Own Calculation Function")
    custom_function_name = st.sidebar.text_input("Function Name", "CustomFunc")
    custom_function_code = st.sidebar.text_area(
        "Function Code (use 'pos' as the input variable, e.g., 'lambda pos: np.mean(pos, axis=0).reshape(-1,1)')",
        "lambda x: np.mean(x, axis=0).reshape(-1,1)"
    )

    # Try to add the custom function
    try:
        custom_function = eval(custom_function_code)
        funcs[custom_function_name] = custom_function
        st.sidebar.success(f"Function '{custom_function_name}' added successfully!")
    except Exception as e:
        st.sidebar.error(f"Error in your function code: {e}")'''
if selected_func_name == "CustomFunc":
    custom_function = handle_custom_function()
    if custom_function:
        funcs[selected_func_name] = custom_function

selected_func = funcs[selected_func_name]

transformed_positions = transform_positions(positions, xrot, xtrans, swap)
results = apply_transformation(transformed_positions, selected_func)


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