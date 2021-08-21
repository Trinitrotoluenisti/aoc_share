from sqlalchemy import ForeignKey

from . import db


class Update(db.Model):
    """
    The Update model contains:

    id   [PK]: an auto-generated id
    data     : the actual update
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String, nullable=False)

class User(db.Model):
    """
    The User model contains:

    id             [PK]: the user's id from Advent of Code
    username        [U]: the user's username
    points             : the user's points (local_score)
    last_update_id  [F]: the id of the last update received
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    solutions = db.relationship('Solution', backref='author')
    last_update_id = db.Column(db.Integer, ForeignKey('update.id'), nullable=False)

    def get_points_leaderboard():
        """
        Returns a leaderboard of the users' scores.

        eg:
            [(user_username, user_points), ...]
        """

        leaderboard = [(u.username, u.points) for u in User.query.all()]
        leaderboard.sort(key=lambda p: p[1], reverse=True)
        return leaderboard


class Solution(db.Model):
    """
    The Solution model contains:

    id       [PK]: an auto-generated id
    type         : 0 if not uploaded, 1 if private, 2 if public
    author    [B]: the User who submitted the solution
    author_id [F]: the id of the User who submitted the solution
    day          : the day for which the solution has been submitted
    part         : the part of the day (1 or 2)
    name      [N]: the name of the file
    public    [N]: if true the solution can be downloaded by other users
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    part = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=True)

    def get_by_day(day):
        """
        Returns the list of solutions given for a day.

        eg:
            {
                "part_1": [('author_username', 'solution_type', 'solution_id'), ...],
                "part_2": [('author_username', 'solution_type', 'solution.id'), ...]
            }
        """

        # Ensures the day is valid
        if day not in range(1, 26):
            raise ValueError(f'Invalid day: {day}')

        data = {}
        for part in (1, 2):
            # Search for solutions in the db, then sorts them
            solutions = Solution.query.filter_by(day=day, part=part).all()
            data[f'part_{part}'] = []

            for s in sorted(solutions, key=lambda s: s.author.username):
                # Adds the solution's id only to the solutions of type 1 or 2
                data[f'part_{part}'].append((s.author.username, s.type, s.id if s.type > 0 else 0))

        return data
