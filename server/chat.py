from google.generativeai import GenerativeModel
import google.generativeai as genai
import base64
import PyPDF2
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize models
client_text = GenerativeModel("gemini-pro")
# CHANGE THIS LINE: Update from "gemini-pro-vision" to "gemini-1.5-flash"
client_image = GenerativeModel("gemini-1.5-flash") 

# Initialize an empty list to store conversation history
# Gemini expects history in a specific format: [{"role": "user", "parts": ["text"]}, {"role": "model", "parts": ["text"]}]
conversation_history = []

def get_response_image(base64_image):
    # Gemini's `generate_content` can directly handle image URLs/data in content parts
    # Ensure the image data is correctly formatted as a part
    image_part = {
        "mime_type": "image/jpeg",  # Assuming JPEG, adjust if necessary
        "data": base64.b64decode(base64_image)
    }

    user_message_parts = [
        {"text": "Name the dish and how is it prepared and what are the possible allergens in this dish? Give the response in pure text format dont use heading or subsection just pure paragraphed text only."},
        image_part
    ]
    
    # Append the user's image message to the conversation history
    conversation_history.append({
        "role": "user",
        "parts": user_message_parts
    })
    
    # Generate the response using the accumulated conversation history
    # For multimodal input, use generate_content directly with the parts
    response = client_image.generate_content(
        contents=conversation_history[-1]["parts"] # Only send the latest user message for image
    )
    
    # Append the assistant's response to the conversation history
    assistant_response_content = response.text
    conversation_history.append({
        "role": "model",
        "parts": [assistant_response_content]
    })
    
    return response

def get_response_text(message):
    # Append the user's text message to the conversation history
    conversation_history.append({
        "role": "user",
        "parts": [message]
    })
    
    # Generate the response using the accumulated conversation history
    # For text-only, use start_chat and send_message
    chat_session = client_text.start_chat(history=conversation_history[:-1]) # Provide history excluding the current message
    response = chat_session.send_message(message)
    
    # Append the assistant's response to the conversation history
    assistant_response_content = response.text
    conversation_history.append({
        "role": "model",
        "parts": [assistant_response_content]
    })
    
    return response

def pdf_to_text(pdf_path):
    # Open the PDF file
    output_text_file = "extracted_text.txt" # Define the output file name
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
    
        # Create a new text file to save the extracted content
        with open(output_text_file, 'w', encoding='utf-8') as txt_file:
            # Process each page
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                # Write the extracted text to the extracted text
                if text:
                    txt_file.write(f"Page {page_num + 1}\n{text}\n\n")
    
    with open(output_text_file, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
    return text_content