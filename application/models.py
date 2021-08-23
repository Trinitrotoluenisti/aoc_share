from sqlalchemy import ForeignKey

from . import db


class User(db.Model):
    """
    The User model contains:

    id             [PK]: the user's id from Advent of Code
    username        [U]: the user's username
    points             : the user's points (local_score)
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    solutions = db.relationship('Solution', backref='author')


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
