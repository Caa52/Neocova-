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

    final_features = [int(x) for x in request.form.values()]
    
    scoring_uri = 'http://43aa851b-4045-482b-9016-9f97cc6b3e70.westus2.azurecontainer.io/score'
 
    data = {"data": final_features}

    input_data = json.dumps(data)
    headers= {'Content-Type': 'application/json'}
    resp = requests.post(scoring_uri, input_data, headers=headers)
    output  = json.loads(resp.text)
 
    return render_template('index.html', prediction_text= 'Your bank valuation is estimated as $ {}'.format(output['predict'][0]))



if __name__ == "__main__":
    app.run(debug=True)