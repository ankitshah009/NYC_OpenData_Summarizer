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
# given a question, return the answer
def get_answer():
    question = request.get_json()['question']
    answer = answer_nyc_question(question)
    return {"answer": answer}
