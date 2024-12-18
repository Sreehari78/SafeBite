from flask import Flask, request, jsonify
import chat
import requests

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()['image']
    # print(data[23:])
    response = chat.get_response_image(data[23:])
    return jsonify({"result": response.choices[0].message.content})

@app.route('/talk', methods=['POST'])
def talk():
    data = request.get_json()['question']
    response = chat.get_response_text(data)
    print(response.choices[0].message.content)
    return jsonify({"result": response.choices[0].message.content})

@app.route('/profile', methods=['POST'])
def profile():
    data = request.get_json()['data']
    # if data['medicalRecords'] != None:
    #     data['medicalRecords'] = chat.pdf_to_text(data['medicalRecords'])
    print(data)
    response = chat.get_response_text("These are the preferences and allergens that i am aware of: " + str(data) + ". Keeping this in mind answer my questions")
    print(response.choices[0].message.content)
    return jsonify("")

if __name__ == '__main__':
    app.run(debug=True)
