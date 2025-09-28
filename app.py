# Python Imports
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initilize OpenAI client
client = openai.OpenAI()

response = client.responses.create(
    model='gpt-4o',
    input=[
        {'role': 'user', 'content': 'Explain Generative AI in one sentence'},
    ],
    temperature=- 0.7,
    max_tokens=100)
