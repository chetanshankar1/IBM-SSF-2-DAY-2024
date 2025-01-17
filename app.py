from flask import Flask, render_template, request
import pickle
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)

def predict(values, dic):
    model = None
    
    if len(values) == 8:
        model = pickle.load(open('models/diabetes.pkl', 'rb'))
    elif len(values) == 26:
        model = pickle.load(open('models/breast_cancer.pkl', 'rb'))
    elif len(values) == 13:
        model = pickle.load(open('models/heart.pkl', 'rb'))
    elif len(values) == 18:
        model = pickle.load(open('models/kidney.pkl', 'rb'))
    elif len(values) == 10:
        model = pickle.load(open('models/liver.pkl', 'rb'))

    if model:
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    return None

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/diabetes", methods=['GET', 'POST'])
def diabetesPage():
    return render_template('diabetes.html')

@app.route("/cancer", methods=['GET', 'POST'])
def cancerPage():
    return render_template('breast_cancer.html')

@app.route("/heart", methods=['GET', 'POST'])
def heartPage():
    return render_template('heart.html')

@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')

@app.route("/liver", methods=['GET', 'POST'])
def liverPage():
    return render_template('liver.html')

@app.route("/malaria", methods=['GET', 'POST'])
def malariaPage():
    return render_template('malaria.html')

@app.route("/pneumonia", methods=['GET', 'POST'])
def pneumoniaPage():
    return render_template('pneumonia.html')

@app.route("/predict", methods=['POST'])
def predictPage():
    try:
        to_predict_dict = request.form.to_dict()
        to_predict_list = list(map(float, list(to_predict_dict.values())))
        pred = predict(to_predict_list, to_predict_dict)
        
        if pred is None:
            raise ValueError("Invalid number of inputs")

    except Exception as e:
        message = f"Please enter valid data: {e}"
        return render_template("home.html", message=message)

    return render_template('predict.html', pred=pred)

@app.route("/malariapredict", methods=['POST'])
def malariapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image'])
                img = img.resize((36, 36))
                img = np.asarray(img)
                img = img.reshape((1, 36, 36, 3))
                img = img.astype(np.float64)
                model = load_model("models/malaria.h5")
                pred = np.argmax(model.predict(img)[0])
            else:
                raise ValueError("No image uploaded")

        except Exception as e:
            message = f"Please upload a valid image: {e}"
            return render_template('malaria.html', message=message)
    
    return render_template('malaria_predict.html', pred=pred)

@app.route("/pneumoniapredict", methods=['POST'])
def pneumoniapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image']).convert('L')
                img = img.resize((36, 36))
                img = np.asarray(img)
                img = img.reshape((1, 36, 36, 1))
                img = img / 255.0
                model = load_model("models/pneumonia.h5")
                pred = np.argmax(model.predict(img)[0])
            else:
                raise ValueError("No image uploaded")

        except Exception as e:
            message = f"Please upload a valid image: {e}"
            return render_template('pneumonia.html', message=message)
    
    return render_template('pneumonia_predict.html', pred=pred)

if __name__ == '__main__':
    app.run(debug=True)
