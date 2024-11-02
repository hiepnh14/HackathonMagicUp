import openai
import requests
from PIL import Image
from io import BytesIO
import os
import json
import re
openai.api_key = os.getenv("OPENAI_API_KEY")  
# Set your OpenAI API key
# openai.api_key = "YOUR_API_KEY"

def get_multimodal_response(image_path, text_prompt):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Multimodal model for image + text input
            messages=[
                {"role": "user", "content": text_prompt}
            ]
            # ,
            # files=[
            #     {"name": "image", "file": image_file}
            # ]
        )
    return response

def download_and_save_image(image_url, save_path="output_image.jpg"):
    """
    Downloads an image from a given URL and saves it to a specified path.
    Args:
        image_url (str): The URL of the image to download.
        save_path (str, optional): The path where the image will be saved. Defaults to "output_image.jpg".
    Returns:
        None
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
        IOError: If there is an issue saving the image.
    """
    # Download the image from the URL
    image_response = requests.get(image_url)
    
    # Check if the request was successful
    if image_response.status_code == 200:
        # Open the image and save it
        image = Image.open(BytesIO(image_response.content))
        image.save(save_path)
        print(f"Image saved at {save_path}")
        
        # Display the image
        image.show()
    else:
        print("Failed to download image")

def draftPrompt(userRequest):
    """
    Appends a specific instruction to the user's request for generating a JSON file 
   
    Args:
        userRequest (str): The initial request from the user.

    Returns:
        str: The modified request with the appended instruction to generate a JSON 
    """
    return userRequest + " Generate a json file of hair, upper lip, lower lip, left eye, and right eye color for the requested makeup in this format: [[r, g, b], [r, g, b],[r, g, b], [r, g, b], [r, g, b]]. Just generate the array only without any text."

def getResponseColors(text, image_path=None):
    response = get_multimodal_response(image_path, text)
    return processResponse(response)

def processResponse(response):
    dataString = response['choices'][0]['message']['content']
    cleaned_string = re.sub(r"```json\n|\n```", "", dataString)

# Step 2: Parse the cleaned JSON string
    try:
        data_array = json.loads(cleaned_string)
        print("Extracted 3D array:", data_array)
    except json.JSONDecodeError:
        print("Failed to parse JSON")

    return data_array
def getColors(image_path, userRequest):
    text = draftPrompt(userRequest)
    return getResponseColors(text, image_path)
# script_dir = os.path.dirname(__file__)
# image_path = os.path.join(script_dir, "image.jpeg")
# text_prompt = "I want to have a feminine makeup look for halloween. Generate a json file of hair, upper lip, lower lip, and iris color in this format: [[b, g, r], [b, g, r], [b, g, r], [b, g, r]]. Just generate the array only without any text."

# response = get_multimodal_response(image_path, text_prompt)
# print(response)
# Check if the response contains an image URL
# if "image_url" in response:  # Replace "image_url" with the correct field from the API response
#     image_url = response["image_url"]
#     download_and_save_image(image_url)
# else:
#     print("No image URL found in the response")
#     print(response)  # Print the full response for debugging
