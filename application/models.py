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
    author    [B]: the User who submitted the solution
    author_id [F]: the id of the User who submitted the solution
    day          : the day for which the solution has been submitted
    part         : the part of the day (1 or 2)
    path      [N]: the path where the solution is
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    part = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String)

    def get_by_day(day):
        """
        Returns the list of solutions given for a day.

        eg:
            {
                "part_1": [('author_username', 'solution_id'), ...],
                "part_1": [('author_username', 'solution_id'), ...]
            }
        """

        # Ensures the day is valid
        if day not in range(1, 26):
            raise ValueError(f'Invalid day: {day}')

        data = {}
        for part in (1, 2):
            # Search for solutions in the db, then sorts them
            solutions = Solution.query.filter_by(day=day, part=part).all()
            data[part] = [(s.author.username, s.id) for s in sorted(solutions, key=lambda s: s.author.username)]

        return data
