from flask import Flask, render_template, request, redirect, url_for
from solve_sudoku_puzzle import sudokuSolver
import os

UPLOAD_FOLDER = './upload'

# saved model 
model_path = "saved_model/digit_classifier.h5"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        solved_image = sudokuSolver(model_path, path)
        return redirect(url_for('result'))
    return render_template('index.html')


@app.route('/result')
def result():
    return render_template('result.html')