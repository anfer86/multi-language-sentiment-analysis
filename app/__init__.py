import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import app.helper
from app.helper import load_bert_model, predict_from_sentenca

app = Flask(__name__, template_folder='front-end')
CORS(app)

# Carregando o modelo (os scores)
print('Carregando o modelo', end='...')
model_saved_path='model/bert_model.h5'
model, tokenizer = load_bert_model(model_saved_path)
print('Concluido')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/sentiment_analysis', methods=['POST'])
def predict():

	print('Recebendo os dados via POST')	
	data = request.get_json(force=True)
	print(data)

	sentenca = data['text']	
	print('Sentenca: ', sentenca)

	print('Realizando a predicao')
	predictions = predict_from_sentenca([sentenca], model, tokenizer)
	prediction = predictions[0]

	print('Predição: ', prediction)
	print('Respondendo a requisição')
	output = jsonify( int(prediction) )
	print(output)
	return output
