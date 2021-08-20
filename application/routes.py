from flask import request, render_template, redirect, make_response

from . import app
from .models import *


@app.route('/')
def index_route():
    # Redirects to the login page if the user is not logged in
    if not request.cookies.get('username'):
        return redirect('/login')

    # Otherwise returns the homepage
    leaderboard = enumerate(User.get_points_leaderboard())
    return render_template('home.html', leaderboard=leaderboard)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    # Returns a login page to the get requests
    if request.method == 'GET':
        return render_template('login.html')

    # Collects the request's data
    username = request.form.get('username')
    keep_logged = request.form.get('keep_logged')

    # Ensures the user exists
    if not User.query.filter_by(username=username).first():
        return render_template('login.html', error='Invalid username'), 401

    # Redirects to the index page setting the username
    r = make_response(redirect('/'), 200)
    r.set_cookie('username', username, samesite='Lax', max_age=(2600000 if keep_logged else None))
    return r

@app.route('/logout', methods=['POST'])
def logout_route():
    # Removes the cookies
    r = make_response(redirect('/login'), 200)
    r.set_cookie('username', '')
    return r
