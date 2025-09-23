import heapq
from itertools import count
from typing import Any, Dict
from problem import State, goal_test, successor
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
    r0, c0, _ = start_state
    start_node = (0.0, r0, c0, next(tie), start_state, None, None)

    #define the frontier: min heap
    frontier = [start_node]

    #Main loop: execute while we still have nodes to explore
    while frontier:
        #stop if we hit cutoffs
        if not within_limits(start_time, expanded):
            return pack_result(None, None, expanded, generated, start_time, first5, cutoff = True)
        g_cost, r, c, tie_id, state, parent_node, action_from_parent = heapq.heappop(frontier)
        expanded += 1

        #record the first 5 nodes
        if len(first5) < 5:
            first5.append((state, g_cost))
        #if goal is reached reconstruct and return
        if goal_test(state):
            #rebuild action list and cost
            actions, states, final_cost = reconstruct((g_cost, tie_id, state, parent_node, action_from_parent))
            #return results
            return pack_result(actions, final_cost, expanded, generated, start_time, first5, cutoff=False)

        #else generate children from this state
        for act, next_state, step_cost in successor(state):
            #track nodes generated
            generated += 1
            #calculate total path cost
            child_g = g_cost + step_cost
            #build child node
            r2, c2, _ = next_state
            parent_5tuple = (g_cost, tie_id, state, parent_node, action_from_parent)
            child_node = (child_g, r2, c2, next(tie), next_state, parent_5tuple, act)
            #push onto the heap
            heapq.heappush(frontier, child_node)
    return pack_result(None, None, expanded, generated, start_time, first5, cutoff=False)


#helper to package results in a dict
def pack_result(solution, cost, expanded, generated, start_time, first5, cutoff):
    #return all fields
    return{
        #list of actions
        "solution": solution,
        #total path cost
        "cost": cost,
        #nodes expanded
        "expanded": expanded,
        #successors generated
        "generated": generated,
        #elapsed time
        "time": now() - start_time,
        #first five
        "first5": first5,
        #True if stopped due to limits
        "cutoff": cutoff,
    }
