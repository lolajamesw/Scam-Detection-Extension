from fastapi import FastAPI
from openai import OpenAI
import requests
import os

client = OpenAI(api_key="sk-proj-RVLC61PxNdqS5r1CzleKlWHBhYYVm_facvYAU7qEfXLy2RL9XRbt4OPrihWwDpbKjuVqotnhyT3BlbkFJEbvQIaJCFdupjTpI4ScGlQVdjYTv3iBC4rPSWd99oUdyAjknUPSoYlpaV4qeVhKNv0aXeMQbsA")

API_URL = "https://l7sol6qs4x9pu9j7.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def check_for_vague_descriptions(listing, tokens=25):
    # avgCost = get_avg_rent()
    assessment = query({
        "inputs": """Analyze the following rental listing for potential scam indicators based on specific details. 

==============
""" + listing + """
===============

Key areas to assess:
- Is the price more than 50% lower than average for similar properties in the area?
- Does the listing lack an exact address
- Are property details and amenities realistic for the price? 
- Has the lease requested specific payment methods other than through a bank or online banking platform
- Does the listing request any form of payment to be done before the renter signs the lease

The risk level should only increase if one of the key areas returns true


Based on the above, provide an overall risk level of Low, Medium, or High, explaining the reasoning and provide an expected price for what is advertised."

Risk level: """,
        "parameters": {
            "top_p": 0.7,
            "temperature": 0.01,  # Adjust this value as needed for more creative or conservative responses
            "max_new_tokens": tokens,
            "return_text": True,
            "return_full_text": False,
            "return_tensors": True,
            "clean_up_tokenization_spaces": True,
            "prefix": "",
            "handle_long_generation": "whole"
        }   
    })
    return assessment



# API endpoint for the LLaMA model hosted on Hugging Face

def query(payload):
    """
    Sends a POST request to the LLaMA model API with the given payload.

    Args:
        payload (dict): The payload containing inputs and parameters for the model.

    Returns:
        dict: The JSON response from the API.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Sample payload to make a query
# output1 = query({
#     "inputs": """
# Analyze the following rental listing for potential scam indicators based on specific details. 

# ==============
# Charming 1-Bedroom Apartment in the Heart of the City

# Based on the above, provide an overall risk level of Low, Medium, or High, explaining any concerns raised."
# Welcome to your new home! This delightful 1-bedroom apartment boasts a fantastic location that is perfect for anyone looking to experience city living.

# Features:

# Spacious living area with a cozy feel
# A kitchen that can accommodate all your cooking needs
# Bright and airy bedroom perfect for relaxation
# Modern bathroom with all the essentials
# Convenient access to public transportation and nearby attractions
# Additional Details:

# Reasonable monthly rent
# Utilities not included
# Pet-friendly environment
# Don't miss the chance to live in this beautiful apartment that offers everything you could possibly want!

# Contact us for more details and to schedule a viewing!
# ===============

# Key areas to assess:
# - Is the listing title overly vague or attention-grabbing without details?
# - Is the price significantly lower than average for similar properties?
# - Does the source indicate a high risk of scams (e.g., Craigslist)?
# - Is the location description specific enough to be verifiable?
# - Are property details and amenities realistic for the price?
# - Are the lease terms standard, and do they require unusual payment methods?
# - Are there security features or viewing options included?
# - Are there additional fees that seem unusual or excessive?

# Based on the above, provide an overall risk level of Low, Medium, or High, explaining any concerns raised."

# Risk level: """,
#     "parameters": {
#         "top_p": 0.7,
#         "temperature": 0.1,  # Adjust this value as needed for more creative or conservative responses
#         "max_new_tokens": 25,
#         "return_text": True,
#         "return_full_text": False,
#         "return_tensors": True,
#         "clean_up_tokenization_spaces": True,
#         "prefix": "",
#         "handle_long_generation": "whole"
#     }
# })

# output2 = query({
#     "inputs": """Address: 123 Main Street, Unit 4B, Cityville

# Welcome to your new home! This well-maintained 1-bedroom apartment features modern amenities and a prime downtown location.

# Apartment Features:

# Living Area: 350 sq ft with large windows offering plenty of natural light and a beautiful view of the city skyline.
# Kitchen: Fully equipped with stainless steel appliances, including a refrigerator, stove, oven, and dishwasher. Ample cabinet space and granite countertops.
# Bedroom: 200 sq ft with a queen-size bed frame included, a spacious closet, and a large window for natural light.
# Bathroom: Recently renovated with a walk-in shower, contemporary fixtures, and tile flooring.
# Building Amenities:

# On-site laundry facilities
# Secure building access with intercom system
# Rooftop terrace with city views and BBQ grill area
# Fitness center and bike storage available
# Location:

# 5-minute walk to the Cityville Metro Station
# Close to grocery stores, restaurants, parks, and entertainment venues
# Quiet street with minimal traffic noise
# Rent: $1,800 per month (includes water and trash removal; electricity and internet are not included)

# Pet Policy: Cats allowed with a $300 non-refundable pet deposit. No dogs permitted.

# Contact Information: For more details or to schedule a viewing, please call Jane at (555) 123-4567 or email jane@example.com.

# Prompt: All listings should include a full address, the property type, available utilities/amenities, lease details, contact information, and pet policies. If a listing is missing or unclear about at least half of these requirements then it's likely to be fraud.
# Based on this, is the above listing likely to be fraud (Yes or no)?
# Answer: """,
#     "parameters": {
#         "top_p": 0.7,
#         "temperature": 0.1,  # Adjust this value as needed for more creative or conservative responses
#         "max_new_tokens": 25,
#         "return_text": True,
#         "return_full_text": False,
#         "return_tensors": True,
#         "clean_up_tokenization_spaces": True,
#         "prefix": "",
#         "handle_long_generation": "whole"
#     }
# })

output1 = check_for_vague_descriptions("""Modern 2-Bedroom Apartment Near University of Waterloo - Available January 2025

Welcome to your new home! This bright, spacious 2-bedroom, 1-bathroom apartment is located just a 10-minute walk from the University of Waterloo campus. Perfect for students or young professionals, this unit offers convenient access to local amenities, public transit, and university facilities.

Key Features:

Location: Situated on Lester Street, Waterloo, ON, close to UW, Laurier, and the vibrant Waterloo town square.
Monthly Rent: $2,400 + utilities.
Availability: Starting January 2025, 12-month lease preferred.
Appliances Included: Stainless steel fridge, stove, microwave, and dishwasher.
Furniture: Fully furnished with a sofa, coffee table, dining set, and double beds in each room.
Internet: High-speed Wi-Fi included.
Building Amenities: Fitness center, laundry room on each floor, secured entry, and bike storage.
Parking: Underground parking available for an additional $50/month.
Transportation: Steps away from multiple bus routes and a 5-minute drive to Conestoga Mall.
Additional Details:

Pet Policy: Pets are welcome with an additional deposit.
Lease Terms: First month’s rent due at signing; tenant insurance required.
Application Requirements: Proof of income, references, and a credit check.
Contact us today to schedule a viewing and make this your new home in Waterloo!
""", 250)
print(output1[0]['generated_text'])
# print('\n', output2)











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