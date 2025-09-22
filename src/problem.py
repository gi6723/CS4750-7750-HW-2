from typing import Tuple, FrozenSet, Iterable

"""
problem.py
-----------

Defines the Vacuum world problem enviorment:
- State representaiton (agents location, dirty cells)
- Action costs and grid boundaries (4x5 grid, specified action cost)
- Successor function for generating new states
- Goal test (all cells clean)
- Two problem instances
"""

# Define the grid size (rows x cols)
ROWS = 4
COLS = 5

#Defining the cost of actions
ACTIONS = {
    "Left": 1.0,
    "Right": 0.9,
    "Up": 0.8,
    "Down": 0.7,
    "Suck": 0.6,
}

# Added limits as specified by your canvas message
MAX_EXPANSIONS = 1000000
MAX_SECONDS = 3600

# Defining state (row, col, frozenset of dirt positions)
State = Tuple[int, int, FrozenSet[Tuple[int, int]]]

def within_bounds(r: int, c:int) -> bool:
    # Returns true if (row,col) is inside of the grid
    return (1 <= r <= ROWS) and (1 <= c <= COLS)

def goal_test(s: State) -> bool:
    #Checks if the state is a goal state (no dirty cells)
    return len(s[2]) == 0

def successor(s: State) -> Iterable[Tuple[str, State, float]]:
    # We Yield (action, next_state, cost) for each valid action from state s.
    r, c, dirt = s

    #Movement actions
    if within_bounds(r, c - 1):
        yield ("Left", (r, c - 1, dirt), ACTIONS["Left"])
    if within_bounds(r, c + 1):
        yield ("Right", (r, c + 1, dirt), ACTIONS["Right"])
    if within_bounds(r - 1, c):
        yield ("Up", (r - 1, c, dirt), ACTIONS["Up"])
    if within_bounds(r + 1, c):
        yield ("Down", (r + 1, c, dirt), ACTIONS["Down"])

    #Suck action if dirt is present
    if (r,c) in dirt:
        new_dirt = set(dirt)
        new_dirt.remove((r,c))

        #We use frozenset to make a new updated dirt set for the child state
        yield ("Suck", (r, c, frozenset(new_dirt)), ACTIONS["Suck"])


def make_state(start_rc, dirt_coords) -> State:
    # Create a State with a frozenset dirt component.
    r, c = start_rc
    return (r, c, frozenset(dirt_coords))

INSTANCE_1 = make_state((2, 2), {(1, 2), (2, 4), (3, 5)})
INSTANCE_2 = make_state((3, 2), {(1, 2), (2, 1), (2, 4), (3, 3)})