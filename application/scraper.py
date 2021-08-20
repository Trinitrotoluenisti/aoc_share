from requests import get
from json import load, dump

from .configs import *
from .models import *


def get_data():
    data = {}

    # Tries to load the offline data if the OFFLINE config is set to true
    if OFFLINE:
        try:
            with open('data.json') as f:
                data = load(f)
        except:
            raise FileNotFoundError('Offline data not found')

    # If OFFLINE is set to false or the file data.json doesn't
    # exist it will make a request to the AOC's apis
    if not OFFLINE or not data:
        url = f'https://adventofcode.com/{AOC_YEAR}/leaderboard/private/view/{AOC_LEADERBOARD}.json'
        r = get(url, cookies={'session': AOC_SESSION})

        # Ensures the request has been successfull
        if not r.ok:
            raise ValueError("Error trying to retrieve data from the aoc's server")

        data = r.json()

        # And it saves them for the next time
        if OFFLINE:
            with open('data.json', 'w') as f:
                dump(data, f)

    return data

def populate_db():
    data = get_data()

    # Creates an update saying that the server has just been started
    lu = Update(data='Server started')
    db.session.add(lu)
    db.session.commit()

    for user_data in data['members'].values():
        # Adds new users
        user = User(id=user_data['id'], username=user_data['name'], points=user_data['local_score'], last_update_id=lu.id)
        db.session.add(user)

        # Registers all the levels done
        for day, parts in user_data['completion_day_level'].items():
            for part in parts:
                db.session.add(Solution(author=user, day=day, part=part))

    # Saves changes
    db.session.commit()
