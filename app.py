# Python Imports
from dotenv import load_dotenv
import openai
import streamlit as st

# Load environment variables
load_dotenv()

# Initilize OpenAI client
client = openai.OpenAI()


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


user_prompt = st.text_input('Enter your prompt:',
                            'Explain Generative AI in one sentence.')

temperature = st.slider(
    'Model temperature:',
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.01,
    help='Control randomness: 0 = deterministic and 1 = creative.')


with st.spinner('AOI is wiorking hard...'):
    response = get_response(user_prompt, temperature)


st.write(response.output[0].content[0].text)
