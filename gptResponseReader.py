from fastapi import FastAPI
from openai import OpenAI
import requests
import os

client = OpenAI(api_key="sk-proj-RVLC61PxNdqS5r1CzleKlWHBhYYVm_facvYAU7qEfXLy2RL9XRbt4OPrihWwDpbKjuVqotnhyT3BlbkFJEbvQIaJCFdupjTpI4ScGlQVdjYTv3iBC4rPSWd99oUdyAjknUPSoYlpaV4qeVhKNv0aXeMQbsA")





# API endpoint for the LLaMA model hosted on Hugging Face
API_URL = "https://l7sol6qs4x9pu9j7.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def query(payload):
    """
    Sends a POST request to the LLaMA model API with the given payload.

    Args:
        payload (dict): The payload containing inputs and parameters for the model.

    Returns:
        dict: The JSON response from the API.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]

# Sample payload to make a query
output = query({
    "inputs": "Answer in one word: What color is the sky?",
    "parameters": {
        "top_p": 0.8,
        "temperature": 0.35,  # Adjust this value as needed for more creative or conservative responses
        "max_new_tokens": 15,
        "return_text": True,
        "return_full_text": False,
        "return_tensors": True,
        "clean_up_tokenization_spaces": True,
        "prefix": "#",
        "handle_long_generation": "truncate"
    }
})

print(output)











"""




MODEL="gpt-4o"

def call_open_ai(input_data):
    completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )
    return("Assistant: " + completion.choices[0].message.content)


@app.post("/process")
async def process_data():
    result = call_open_ai(input_data)
    return {"result": result}

    """