# AOC Share

AOC Share is a website that provides a simple interface to share the solutions to the Advent of Code's problems.

Before starting it (by running `run.py`), you have to create a config file inside `application`; it must contain the following variables:

```python
from pathlib import Path

AOC_YEAR = 2020
AOC_LEADERBOARD = 123456
AOC_SESSION = '123abc' # It can be found in the advent's cookies saved in your browser

# NB: the following two variables must be absolute paths and instances of pathlib.Path
DATABASE_PATH = Path('database/').resolve() # The folder where aoc_share.db is created
SOLUTIONS_DIR = Path('database/solutions/').resolve() # The folder where all the submitted solutions are saved

OFFLINE = False # If set to true the server will load the data from a local copy instead of fetching it from the aoc's server
```
