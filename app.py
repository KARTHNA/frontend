import streamlit as st
import requests
import io
import pandas as pd
from PIL import Image

API_URL = "https://dbbackend001.azurewebsites.net/process_request"
     
st.title("Database Chatbot")
st.write("Ask questions related to the database content.")

# Initialize session state variables
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

if 'response' not in st.session_state:
    st.session_state.response = ""

if 'plots' not in st.session_state:
    st.session_state.plots = {}

if 'table_data' not in st.session_state:
    st.session_state.table_data = []

# Input field for the user query
user_query = st.text_input("Enter your query:", value=st.session_state.user_query, key='query_input')

def call_backend_api(query):
    try:
        headers = {"Content-Type": "application/json"}
        data = {"user_query": query, "request_id": "123"}
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while communicating with the backend: {e}")
        return None

# Enter button to trigger API call
if st.button("Enter"):
    if user_query:
        response = call_backend_api(user_query)
        if response:
            st.session_state.response = response.get('remarks', 'No remarks available')
            st.session_state.plots = response.get('plots', {})
            st.session_state.table_data = response.get('table_data', [])
        else:
            st.session_state.response = "No response received from the backend."
            st.session_state.plots = {}
            st.session_state.table_data = []
        st.session_state.user_query = user_query

# Display the response
if st.session_state.response:
    st.write(f"Response: {st.session_state.response}")

# Display all graphical data if available
if st.session_state.plots:
    st.write("Graphical Representations:")
    for plot_type, byte_img in st.session_state.plots.items():
        if byte_img:
            st.write(f"Plot Type: {plot_type.capitalize()}")
            img = Image.open(io.BytesIO(bytearray(byte_img)))
            st.image(img, caption=f"Generated {plot_type.capitalize()} Plot")

# Display table data if available
if st.session_state.table_data:
    st.write("Table Data:")
    df = pd.DataFrame(st.session_state.table_data)
    st.table(df)

# Clear button to reset input and response
if st.button("Clear"):
    st.session_state.user_query = ""
    st.session_state.response = ""
    st.session_state.plots = {}
    st.session_state.table_data = []
    st.experimental_rerun()