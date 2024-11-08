import py3Dmol
import plotly.express as px
import plotly.graph_objects as go
from stmol import add_sphere

def show_array(positions, width=500, height=500):
    fig = px.imshow(positions, color_continuous_scale='Viridis', width=width, height=height,aspect="auto")
    return go.Figure(fig)

def display_3d_molecule(molecule, positions):
    view = py3Dmol.view(width=400, height=400)
    atom_properties = {
        'C': {'color': '0x777777', 'radius': 0.7},
        'H': {'color': '0xFFFFFF', 'radius': 0.3},
        'O': {'color': '0xFF0D0D', 'radius': 0.6},
        'N': {'color': '0x3050F8', 'radius': 0.65},
        'default': {'color': '0xCCCCCC', 'radius': 0.5}
    }

    for symbol, pos in zip(molecule.get_chemical_symbols(), positions):
        props = atom_properties.get(symbol, atom_properties['default'])
        add_sphere(view, spcenter=list(pos), radius=props['radius'], spColor=props['color'])
    view.zoomTo()
    return view

