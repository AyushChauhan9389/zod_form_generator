import streamlit as st
from zod_schema_generator import zod_schema_page
from shadcn_form_generator import shadcn_form_page
from server_action_generator import server_action_page
from safe_action_form_generator import safe_action_form_page

st.set_page_config(page_title="Zod Form Generator", layout="wide")

st.title("Zod Form Generator")

pages = {
    "Zod Schema Generator": zod_schema_page,
    "ShadCN Form Generator": shadcn_form_page,
    "Server Action Generator": server_action_page,
    "Server Next safe action": safe_action_form_page
}

selection = st.sidebar.radio("Select a page", list(pages.keys()))

pages[selection]()