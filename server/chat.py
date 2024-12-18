from openai import OpenAI
import base64
import PyPDF2
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize an empty list to store conversation history
conversation_history = []

def get_response_image(base64_image):
    # Append the user's image message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "Name the dish and how is it prepared and what are the possible allergens in this dish? Give the response in pure text format dont use heading or subsection just pure paragraphed text only."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]
    })
    
    # Generate the response using the accumulated conversation history
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )
    
    # Append the assistant's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    
    return response

def get_response_text(message):
    # Append the user's text message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": message
    })
    
    # Generate the response using the accumulated conversation history
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history
    )
    
    # Append the assistant's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    
    return response

def pdf_to_text(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
    
        # Create a new text file to save the extracted content
        with open(output_text_file, 'w', encoding='utf-8') as txt_file:
            # Process each page
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                # Write the extracted text to the output file
                if text:
                    txt_file.write(f"Page {page_num + 1}\n{text}\n\n")
    
    with open(output_text_file, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
    return text_content
