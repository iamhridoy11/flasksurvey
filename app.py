from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "response"


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickeneater12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# response = []


@app.route('/')
def home_page():

    return render_template('home.html', survey=satisfaction_survey)


@app.route('/start', methods=["POST"])
def show_begain():
    """Adding an empty session of response"""
    session[RESPONSES_KEY] = []

    # RESPONSE = []

    return redirect('/questions/0')


@app.route('/questions/<int:id>')
def show_question(id):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[id]

    return render_template("questions.html", question_num=id, question=question)
    # question = satisfaction_survey.questions[id]

    # return render_template('questions.html', question=question)


@app.route('/answer', methods=["POST"])
def work_with_answer():

    choice = request.form['answer']

    # Adding response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    # response.append(choice)

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

    # if (len(response) == len(satisfaction_survey.questions)):
    #     return redirect('/complete')
    # else:
    #     return redirect(f"/questions/{len(response)}")


@app.route('/complete')
def complete_survey():
    return render_template('complete.html')
