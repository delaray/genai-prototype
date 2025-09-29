# Code for course Fast Gen AI Profstotyping.

# Python Imports
from dotenv import load_dotenv
import openai
import streamlit as st
import os
import pandas as pd
import string
import re

# Load environment variables
load_dotenv()

# Initilize OpenAI client
client = openai.OpenAI()


def get_dataset_path():
    csv_path = os.path.join('data', 'customer_reviews.csv')
    return csv_path


def replace_punctuation(text):
    """
    Replace all punctuation in a string with ", ".
    """
    # Create a regex pattern that matches any punctuation character
    pattern = f"[{re.escape(string.punctuation)}]"
    return re.sub(pattern, ", ", text)


def clean_text(text):
    text = replace_punctuation(text)
    text = text.lower()
    text = text.strip()
    return text


@st.cache_data
def get_response(user_prompt, temperature):
    response = client.responses.create(
        model='gpt-4o',
        input=[
            {'role': 'user', 'content': user_prompt},
        ],
        temperature=temperature,
        max_output_tokens=100)
    return response


st.title('Hello, GenAI')
st.write('This is your first Streamlit App.')

col1, col2 = st.columns(2)

with col1:
    if st.button('Ingest Dataset'):
        try:
            csv_path = get_dataset_path()
            st.session_state['df'] = pd.read_csv(csv_path)
            st.success('Dataset loaded successfully')
        except FileNotFoundError:
            st.error('Dataset not found.')

with col2:
    if st.button('Parse Reviews'):
        if 'df' in st.session_state:
            st.session_state['df']['CLEANED_SUMMARY'] = \
                st.session_state['df']['SUMMARY'].apply(clean_text)
            st.success('Reviews parsed and cleaned')
        else:
            st.warning('Please ingest a dataset first.')


if 'df' in st.session_state:
    st.subheader(f"Filter by product")
    product = st.selectbox("Choose a product",
                           ['All Products'] +
                           list(st.session_state['df']['PRODUCT'].unique()))

    if product != 'All Products':
        filtered_df = st.session_state['df'][st.session_state['df']
                                             ['PRODUCT'] == product]
    else:
        filtered_df = st.session_state['df']

    st.subheader(f"Dataset Preview")
    st.dataframe(filtered_df.head())

# user_prompt = st.text_input('Enter your prompt:',
#                             'Explain Generative AI in one sentence.')

# temperature = st.slider(
#     'Model temperature:',
#     min_value=0.0,
#     max_value=1.0,
#     value=0.7,
#     step=0.01,
#     help='Control randomness: 0 = deterministic and 1 = creative.')


# with st.spinner('AOI is wiorking hard...'):
#     response = get_response(user_prompt, temperature)


# st.write(response.output[0].content[0].text)
