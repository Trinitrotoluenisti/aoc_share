from flask import request, render_template, redirect, make_response
from functools import wraps

from . import app
from .models import *


def needs_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Ensures that there is the 'username' cookie
        username = request.cookies.get('username')
        if not username:
            return redirect('/login')

        return func(username, *args, **kwargs)

    return wrapper

@app.route('/')
@needs_auth
def home_route(username):
    # Returns the homepage
    leaderboard = User.get_points_leaderboard()
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
@needs_auth
def logout_route(username):
    # Removes the cookies
    r = make_response(redirect('/login'), 200)
    r.set_cookie('username', '', max_age=0)
    return r

@app.route('/days/<int:day>')
@needs_auth
def day_route(username, day):
    # Ensures the day is valid
    if day not in range(1, 25):
        return redirect('/'), 404

    solutions = Solution.get_by_day(day)

    # Calculates the user's index in the solutions
    user_index = {}
    for part in (1, 2):
        index = [i for i, u in enumerate(solutions[f'part_{part}']) if u[0] == username]
        user_index[f'part_{part}'] = index[0] if index else -1

    # Returns the day.html page
    return render_template('day.html', day=day, solutions=solutions, user_index=user_index)
