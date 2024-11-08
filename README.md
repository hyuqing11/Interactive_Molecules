# Interactive Molecular Transformation App

This is a Streamlit web application for visualizing and transforming molecular structures interactively. Users can select different molecules, apply transformations, and visualize the results in 3D.

## Features
- **Molecule Selection**: Choose from a variety of molecules such as O3, CH4, O2, H2O, CO2, NH3, and CH3CH2OCH3.
- **Transformations**: Rotate, translate, or swap atom positions in the molecule.
- **Calculation Functions**: Apply built-in calculations such as DeepPot_SE and DimnetPlus, or add your own custom functions.
- **Custom Functions**: Users can add custom functions by either writing code directly or uploading a Python file.
- **3D Visualization**: View the transformed molecular structure in an interactive 3D plot using `py3Dmol`.

## Usage

1. **Access the application:**
   - You can open the app directly using this [website link](https://interactivemolecules-9jdne3eohsikroemn7mtlx.streamlit.app/).
   - Or, start the application locally by running the command:
     ```bash
     streamlit run app.py
     ```
2. **Use the sidebar to:**
   - **Select a molecule** from a list of options (e.g., CH₄, O₂, H₂O).
   - **Adjust transformation parameters**:
     - Adjust rotation (degrees), translation, and atom swapping using sliders.
   - **Choose a descriptor**:
     - Select from built-in options like **DeepPot_SE** and **DimnetPlus**.
   - Or, **add your own custom function**:
       - **Write Code**: Enter your function directly in the provided text area.
       - **Upload File**: Upload a `.py` file containing your custom function (e.g., a function named `custom_function`).

3. **View the results**:
   - **Transformed Positions**: See the updated atomic positions displayed in a data table.
   - **Calculation Results**: View the results as 2D heatmaps, generated based on the selected calculation function.
   - **3D Molecular Visualization**: Interact with the 3D molecular model to explore different views and gain insights into the structure.
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this project, create issues, and submit pull requests. Contributions are always welcome!

## Acknowledgements

- Streamlit
- ASE (Atomic Simulation Environment)
- py3Dmol
## Contact
For questions or suggestions, contact yuiqinghuang2018@gmail.com or create an issue on this repository.


