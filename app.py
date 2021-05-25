from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
from sklearn.linear_model import LogisticRegression
from pywebio import start_server
import argparse
import numpy as np
import pickle

model = pickle.load(open('final.pkl','rb'))
app = Flask(__name__)

def predict():
    data = input_group("Diabetes Prediction",[
    input('Number of pregnency', placeholder="e.g. 0", name='pregnancy',type=NUMBER),
    input('Glucose(mg/dL)', name='glucose', placeholder="e.g. 120",type=FLOAT),
    input('Blood Pressure(mm Hg)', name='bp', placeholder="e.g. 80",type=NUMBER),
    input('Insulin(IU/mL)', name='insulin', placeholder="e.g. 79",type=FLOAT),
    input('Skin Thickness(mm)', name='skin', placeholder="e.g. 20",type=FLOAT),
    input('Body Mass Index(kg/m2)', name='bmi', placeholder="e.g. 19.5",type=FLOAT),
    input('Diabetes Prediction Function', name='dpf', placeholder="e.g. 0.6", type=FLOAT),
    input('Age', name='age', placeholder="e.g. 0", type=NUMBER),
    ])

    preg = data['pregnancy']
    glucose = data['glucose']
    bp = data['bp']
    st = data['skin']
    insulin = data['insulin']
    bmi = data['bmi']
    dpf = data['dpf']
    age = data['age']

    fetch_data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
    my_prediction = model.predict(fetch_data)
    if my_prediction == 0:
        result = "Great! You DON'T have diabetes."
        put_success(result)
        put_html('<img src="https://media0.giphy.com/media/TGQyLdzYv90FjplXkr/giphy.gif">')
    if my_prediction == 1:
        result = "Oops! You Have Diabetes"
        put_warning(result)
        put_html('<img src="https://media4.giphy.com/media/1k1ytTA4AHJnp7OvUJ/giphy.gif">')


app.add_url_rule('/','webio_view',webio_view(predict), methods=['GET','POST','OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)

#app.run(host='localhost',port=80)

