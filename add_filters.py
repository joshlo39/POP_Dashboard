
import streamlit as st
from Filters import Filters
import json

def add_to_dropdown(dropdown_name, json_file, dropdown_values=None):
    """
    Generic function to add a value to a dropdown list and save it.
    :param dropdown_name: Display name for Streamlit input
    :param json_file: File where dropdown values are stored
    :param dropdown_values: Existing list of values, if None, will load from json_file
    """
    if dropdown_values is None:
        try:
            with open(json_file, 'r') as f:
                dropdown_values = json.load(f)
        except FileNotFoundError:
            dropdown_values = []

    if dropdown_name not in st.session_state:
        st.session_state[dropdown_name] = dropdown_values.copy()

    new_value = st.text_input(f"Add a new {dropdown_name.replace('_', ' ').title()}:")
    if st.button(f"Add {dropdown_name.replace('_', ' ').title()}"):
        if new_value:
            if new_value not in st.session_state[dropdown_name]:
                st.session_state[dropdown_name].append(new_value)
                with open(json_file, 'w') as f:
                    json.dump(st.session_state[dropdown_name], f, indent=4)
                st.success(f"Added {new_value} to {dropdown_name.replace('_', ' ').title()}!")
            else:
                st.warning(f"{new_value} already exists in {dropdown_name.replace('_', ' ').title()}.")
        else:
            st.error(f"No value entered for {dropdown_name.replace('_', ' ').title()}.")

    return st.session_state[dropdown_name]
