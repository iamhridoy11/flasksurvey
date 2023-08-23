from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickeneater12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

response = []


@app.route('/')
def home_page():

    return render_template('home.html', survey=satisfaction_survey)


@app.route('/start', methods=["POST"])
def show_begain():
    RESPONSE = []
    return redirect('/questions/0')


@app.route('/questions/<int:id>')
def show_question(id):
    question = satisfaction_survey.questions[id]

    return render_template('questions.html', question=question)


@app.route('/answer', methods=["POST"])
def work_with_answer():

    choice = request.form['answer']
    response.append(choice)

    if (len(response) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(response)}")


@app.route('/complete')
def complete_survey():
    return render_template('complete.html')
