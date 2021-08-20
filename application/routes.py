from flask import render_template

from . import app


@app.route('/login')
def login_route():
    return render_template('login.html')
