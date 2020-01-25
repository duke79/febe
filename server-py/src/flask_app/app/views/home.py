from flask import render_template
from ...app import app


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template('home.html')


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0
