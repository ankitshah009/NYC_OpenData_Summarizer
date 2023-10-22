import requests
from flask import Flask, request
from flask_cors import CORS
import numpy as np
from rag_generation import answer_nyc_question
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return 'Server is running'


@app.route('/about')
def about():
    return "This api is used to answer any questions one has about the essential services in NYC".


@app.route('/get_answer', methods=['POST']) 
def get_answer():
    translation_url = "http://burro.mlsp.cs.cmu.edu:5000/translate"
    question = request.get_json()['question']
    language = request.get_json()['language']
    # english langauge key: en
    translated_response = requests.post(translation_url, data={"q": question, "source": "auto", "target": "en", "format": "text"})
    translated_question = translated_response.json()['translatedText']
    answer, sources = answer_nyc_question(question)
    payload = {
        "q": answer,
        "source": "en",
        "target": language,
        "format": "text"
    }
    translated_response = requests.post(translation_url, data=payload)
    translated_answer = translated_response.json()['translatedText']

    return {"answer": answer, "translatedAnswer": translated_answer + '\n\n' + sources}


if __name__ == '__main__':
    app.run(debug=True)
