from flask import Flask, render_template, request, redirect, url_for, session
from base.solve_sudoku_puzzle import sudokuSolver
import os


UPLOAD_FOLDER = './static'

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
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')
        file1.save(path)
        status = sudokuSolver(model_path, path)

        if status == "Success":
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
            {'image': 'static/input.png', 'text': 'Original Sudoku Image'},
            {'image': 'static/Threshold.png', 'text': 'Thresholded version of Image'},
            {'image': 'static/outline.png', 'text': 'Detect contour of sudoku board'},
            {'image': 'static/transform.png', 'text': 'Applying Perpective Transform'}
    ]

    digits = os.listdir('static/digits')
    digits.sort()

    pred = [] # Empty predicted list
    for i in digits:
        pred.append(i[8]) # The eight index in the file name is the predicted value


    return render_template('step.html', data=data, digits=zip(digits ,pred))