import heapq
from itertools import count
from typing import Any, Dict
##from problem import State, is_goal, successors##Subject to change based on "problem" implementaion
from utils import *


#Function header/setup for ucts
def ucts(start_state: State) -> Dict[str, Any]:
    start_time = now()
    #How many nodes we processed
    expanded = 0
    #How many children we created
    generated = 0
    #first 5 expansions
    first5 = []
    tie = count()

    #building the staring node
    start_node = (0.0, next(tie), start_state, None, None)

    #define the frontier: min heap
    frontier = [start_node]

    #Main loop: execute while we still have nodes to explore
    while frontier:
        #stop if we hit cutoffs
        if not within_limits(start_time, expanded):
            return pack_result(None, None, expanded, generated, start_time, first5, cutoff = True)
        g_cost, tie_id, state, parent_node, action_from_parent = heapq.heappop(frontier)
        expanded += 1

        if len(first5) < 5:
            first5.append((state, g_cost))

        if is_goal(state):
