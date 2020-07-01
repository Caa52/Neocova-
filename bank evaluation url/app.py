import numpy as np
from flask import Flask, request, jsonify, render_template
import json
import pickle
import requests 

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = [int_features]

    scoring_uri = 'http://43aa851b-4045-482b-9016-9f97cc6b3e70.westus2.azurecontainer.io/score'
 
    data = {"data": final_features}

    input_data = json.dumps(data)
    headers= {'Content-Type': 'application/json'}
    resp = requests.post(scoring_uri, input_data, headers=headers)
    prediction = "the value should be" + resp.text


    return render_template('index.html', prediction_text=prediction)



if __name__ == "__main__":
    app.run(debug=True)