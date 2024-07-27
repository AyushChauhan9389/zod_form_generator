import streamlit as st
from utils import generate_shadcn_form

def shadcn_form_page():
    st.header("ShadCN Form Generator")

    form_name = st.text_input("Form Name", "MyForm")
    num_fields = st.number_input("Number of fields", min_value=1, max_value=10, value=3)
    
    fields = []
    for i in range(num_fields):
        col1, col2 = st.columns(2)
        with col1:
            field_name = st.text_input(f"Field {i+1} name")
        with col2:
            field_type = st.selectbox(f"Field {i+1} type", [
                "text", "email", "password", "number", "date", "checkbox", "select", "textarea"
            ])
        fields.append((field_name, field_type))
    
    use_zod = st.checkbox("Use Zod for form validation", value=True)
    
    if st.button("Generate Form"):
        form_code = generate_shadcn_form(form_name, fields, use_zod)
        st.code(form_code, language="typescript")

if __name__ == "__main__":
    shadcn_form_page()