from sqlalchemy import ForeignKey

from . import db


class User(db.Model):
    """
    The User model contains:
    id             [PK]: the user's id from Advent of Code
    username        [U]: the user's username
    last_update_id  [F]: the id of the last update received
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    solutions = db.relationship('Solution', backref='author')
    last_update_id = db.Column(db.Integer, ForeignKey('update.id'), nullable=False)


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


class Update(db.Model):
    """
    The Update model contains:
    id   [PK]: an auto-generated id
    data     : the actual update
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String, nullable=False)
