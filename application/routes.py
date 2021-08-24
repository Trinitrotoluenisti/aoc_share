from flask import request, render_template, redirect, make_response, send_file
from functools import wraps
from os import remove

from . import app
from .models import *
from .configs import SOLUTIONS_DIR


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
    # Calculates the leaderboard based on aoc's local_score
    leaderboard = User.query.all()
    leaderboard.sort(key=lambda p: p.points, reverse=True)
    return render_template('home.html', leaderboard=leaderboard, username=username)

@app.route('/login/', methods=['GET', 'POST'])
def login_route():
    # Returns a login page to the get requests
    if request.method == 'GET':
        return render_template('login.html', login_page=True)

    # Collects the request's data
    username = request.form.get('username')
    keep_logged = request.form.get('keep_logged')

    # Ensures the user exists
    if not User.query.filter_by(username=username).first():
        return render_template('login.html', login_page=True, error='Invalid username'), 401

    # Redirects to the index page setting the username
    r = make_response(redirect('/'), 200)
    r.set_cookie('username', username, samesite='Lax', max_age=(2600000 if keep_logged else None))
    return r

@app.route('/logout/', methods=['POST'])
@needs_auth
def logout_route(username):
    # Removes the cookies
    r = make_response(redirect('/login'), 200)
    r.set_cookie('username', '', max_age=0)
    return r

@app.route('/days/<int:day>/')
@needs_auth
def day_route(username, day):
    # Ensures the day is valid
    if day not in range(1, 26):
        return redirect('/'), 404

    # Looks for solutions in the database
    solutions = {'part_1': [], 'part_2': []}
    for part in (1, 2):
        data = Solution.query.filter_by(day=day, part=part).all()
        solutions[f'part_{part}'] = sorted(data, key=lambda s: s.author.username)

    # Calculates the user's index in the solutions
    user_indexes = {}
    for part in (1, 2):
        index = [i for i, u in enumerate(solutions[f'part_{part}']) if u.author.username == username]
        user_indexes[f'part_{part}'] = index[0] if index else -1

    # Returns the day.html page
    return render_template('day.html', day=day, solutions=solutions, user_indexes=user_indexes)

@app.route('/days/<int:day>/solutions/<int:part>/', methods=['GET', 'POST'])
@needs_auth
def day_solution_route(username, day, part):
    # Ensures the day and the part are valid
    if day not in range(1, 26) or part not in (1, 2):
        return (redirect('/') if request.method == 'GET' else 'Day or part not found'), 404

    # Ensures the user has completed that level
    user = User.query.filter_by(username=username).first()
    solution = Solution.query.filter_by(day=day, part=part, author=user).first()
    if not solution:
        return (redirect('/days/') if request.method == 'GET' else 'Level not unlocked'), 403

    # Returns the page if it's a get request
    if request.method == 'GET':
        return render_template('solution.html', day=day, part=part, new=(solution.type == 0), public=(solution.type == 2))

    # Checks if the solution has to be deleted or created/edited
    if 'delete' in request.form:
        # Deletes the file if exists
        if solution.type > 0:
            remove(f'{SOLUTIONS_DIR}/{solution.id}')

        # Sets the solution's type as 'Not Uploaded'
        solution.type = 0
    else:
        # Ensures that a file has been uploaded if the solution is new
        file = request.files.get('file')
        if solution.type == 0 and (not file or not file.filename):
            return render_template('solution.html', day=day, part=part, new=(solution.type == 0), public=(solution.type == 2), error='Missing file'), 400

        # Saves the file
        if file and file.filename:
            solution.name = file.filename
            file.save(f'{SOLUTIONS_DIR}/{solution.id}')

        # Saves all in the database
        solution.type = 2 if 'public' in request.form else 1

    db.session.commit()
    return redirect(f'/days/{day}/'), 201

@app.route('/solutions/<int:solution>/')
@needs_auth
def solutions_route(username, solution):
    solution = Solution.query.get(solution)
    user = User.query.filter_by(username=username).first()

    # Ensures the solution exists and can be downloaded
    if not solution:
        return 'Solution not found', 404
    elif solution.type == 0 or solution.type == 1 and solution.author != user:
        return 'Private or not uploaded solution', 403

    # Ensures the user has unlocked that level
    if not Solution.query.filter_by(author=user, day=solution.day, part=solution.part).first():
        return 'Level not unlocked', 403

    # Returns the file to download
    return send_file(f'{SOLUTIONS_DIR}/{solution.id}', download_name=solution.name, as_attachment=True)
