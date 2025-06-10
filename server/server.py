from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import chat
import requests

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()['image']
    if data.startswith("data:image"):
        base64_image_data = data.split(',')[1]
    else:
        base64_image_data = data

    response = chat.get_response_image(base64_image_data)
    return jsonify({"result": response.text})

@app.route('/talk', methods=['POST'])
def talk():
    data = request.get_json()['question']
    response = chat.get_response_text(data)
    print(response.text)
    return jsonify({"result": response.text})

@app.route('/profile', methods=['POST'])
def profile():
    data = request.get_json()['data']
    print(data)
    response = chat.get_response_text("These are the preferences and allergens that i am aware of: " + str(data) + ". Keeping this in mind answer my questions")
    print(response.text)
    return jsonify("")

if __name__ == '__main__':
    app.run(debug=True)