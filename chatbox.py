from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(message):
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=message
    )
    return response.output_text