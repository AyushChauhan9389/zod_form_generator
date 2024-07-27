import streamlit as st
from utils import generate_server_action

def server_action_page():
    st.header("Server Action Generator")

    action_name = st.text_input("Action Name", "handleFormSubmission")
    
    http_method = st.selectbox("HTTP Method", ["POST", "GET", "PUT", "DELETE"])
    
    num_params = st.number_input("Number of parameters", min_value=1, max_value=5, value=2)
    
    params = []
    for i in range(num_params):
        col1, col2 = st.columns(2)
        with col1:
            param_name = st.text_input(f"Parameter {i+1} name")
        with col2:
            param_type = st.selectbox(f"Parameter {i+1} type", ["string", "number", "boolean", "object", "any"])
        params.append((param_name, param_type))
    
    use_zod = st.checkbox("Use Zod for input validation", value=True)
    
    if st.button("Generate Server Action"):
        server_action_code = generate_server_action(action_name, http_method, params, use_zod)
        st.code(server_action_code, language="typescript")

if __name__ == "__main__":
    server_action_page()