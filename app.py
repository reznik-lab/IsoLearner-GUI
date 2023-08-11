from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import visualization as vis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import IsoLearner_added_functionality as IsoLearner
import pickle

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def loading_screen():
    return render_template('loading.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    return redirect('/plotting')

@app.route('/plotting', methods=['GET'])
def plotting():
    all_files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    iso_files = []

    for file in all_files:
        if 'isotopolouges' in file:
            iso_files.append(file)

    return render_template('plotting.html', files=iso_files)

@app.route('/plot', methods=['POST'])
def plot_iso():
    iso_name = request.form['iso']
    isotope = request.form['isotope']
    file = request.form['file']

    data= pd.read_csv(f'/Users/goldfei/Documents/IsoLearner-GUI/uploads/{file}')
    vis.plot_brain(data, iso_name=f'{iso_name} m+{isotope}')
    return send_from_directory('/Users/goldfei/Documents/IsoLearner-GUI/', 'plot.png')

@app.route('/predicting', methods=['GET'])
def predicting():
    return render_template('predicting.html')


@app.route('/predict', methods=['POST'])
def predict_metabolite():
    iso_name = request.form['iso']
    isotope = request.form['isotope']
    #file = request.form['file']

    fileObj = open('Brain_Glucose_IsoLearner.pkl', 'rb')
    Brain_Glucose_IsoLearner = pickle.load(fileObj)
    
    val_ground, val_pred = Brain_Glucose_IsoLearner.cross_validation_testing()

    vis.cross_validation_results(val_ground, val_pred, coords_df = Brain_Glucose_IsoLearner.coords_df, iso_to_plot = f'{iso_name} m+{isotope}')

    return send_from_directory('/Users/goldfei/Documents/IsoLearner-GUI/', 'predict.png')

@app.route('/loading', methods=['GET'])
def loading():
    return render_template('loading.html')


if __name__ == '__main__':
    app.run(debug=True)