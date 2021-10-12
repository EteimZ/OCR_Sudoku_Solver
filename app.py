from flask import Flask, render_template, request, redirect, url_for, session
from google.protobuf import message
from solve_sudoku_puzzle import sudokuSolver
import os


UPLOAD_FOLDER = './upload'

# saved model 
model_path = "saved_model/digit_classifier.h5"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = b'(>\xefI\x9b\xe2r\xddD\x87\x04\xbc5\x14\xeb\xb7'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        solved_image = sudokuSolver(model_path, path)
        if solved_image == "Success":
            return redirect(url_for('success'))
        else:
            return redirect(url_for('fail'))
    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/fail')
def fail():
    return render_template('fail.html')


@app.route('/steps')
def steps():
    data = [
            {'image': 'static/output.png', 'text': 'Original Sudoku Image'},
            {'image': 'static/Threshold.png', 'text': 'Thresholded version of Image'},
            {'image': 'static/outline.png', 'text': 'Detect contour of Image'},
            {'image': 'static/transform.png', 'text': 'Applying Perpective Transform'}
    ]

    digits = os.listdir('static/digits')
    digits.sort()

    return render_template('step.html', data=data, digits=digits)