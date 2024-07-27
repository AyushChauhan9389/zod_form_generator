import streamlit as st
from utils import generate_zod_schema

def zod_schema_page():
    st.header("Zod Schema Generator")

    schema_type = st.selectbox("Select schema type", ["object", "array", "string", "number", "boolean"])
    
    if schema_type == "object":
        num_fields = st.number_input("Number of fields", min_value=1, max_value=10, value=3)
        fields = []
        for i in range(num_fields):
            field_name = st.text_input(f"Field {i+1} name")
            field_type = st.selectbox(f"Field {i+1} type", ["string", "number", "boolean", "array", "object"])
            fields.append((field_name, field_type))
        
        if st.button("Generate Schema"):
            schema = generate_zod_schema(schema_type, fields)
            st.code(schema, language="typescript")
    
    elif schema_type in ["string", "number", "boolean"]:
        if st.button("Generate Schema"):
            schema = generate_zod_schema(schema_type)
            st.code(schema, language="typescript")
    
    elif schema_type == "array":
        item_type = st.selectbox("Array item type", ["string", "number", "boolean", "object"])
        if st.button("Generate Schema"):
            schema = generate_zod_schema(schema_type, item_type=item_type)
            st.code(schema, language="typescript")

if __name__ == "__main__":
    zod_schema_page()