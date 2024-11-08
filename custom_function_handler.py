import streamlit as st
import importlib.util
import os

def handle_custom_function():
    st.sidebar.header("Add Your Custom Function")
    custom_input_method = st.sidebar.radio("Choose how to add your custom function:", ("Write Code", "Upload File"))
    if custom_input_method == "Write Code":
        # Allow users to write their custom function code directly
        custom_function_code = st.sidebar.text_area(
            "Function Code (use 'pos' as the input variable, e.g., 'lambda pos: np.mean(pos, axis=0).reshape(-1,1)')",
            "lambda pos: np.mean(pos, axis=0).reshape(-1,1)"
        )
        try:
            custom_function = eval(custom_function_code)
            st.sidebar.success("Custom function added successfully!")
            return custom_function
        except Exception as e:
            st.sidebar.error(f"Error in your function code: {e}")
            return None


    elif custom_input_method == "Upload File":
        uploaded_file = st.sidebar.file_uploader("Upload a Python file (.py) with your custom function", type="py")
        if uploaded_file is not None:
            try:
                # Save the uploaded file temporarily
                file_path = "temp_uploaded_function.py"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # Dynamically import the module
                spec = importlib.util.spec_from_file_location("custom_module", file_path)
                custom_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(custom_module)
                # Assume the user has defined a function named `custom_function`
                if hasattr(custom_module, "custom_function"):
                    st.sidebar.success("Custom function loaded successfully from file!")
                    return getattr(custom_module, "custom_function")
                else:
                    st.sidebar.error("The uploaded file does not contain a function named 'custom_function'.")
                    return None
            except Exception as e:
                st.sidebar.error(f"Error loading custom function from file: {e}")
                return None
            finally:
                # Clean up the temporary file
                if os.path.exists(file_path):
                    os.remove(file_path)
            return None
