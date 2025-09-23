import heapq
from itertools import count
from typing import Any, Dict
from problem import State, goal_test, successor
from utils import now, within_limits, reconstruct

# Function header/setup for ucgs
def graph_search(start_state: State) -> Dict[str, Any]:
    # record the start time
    start_time = now()
    # count how many nodes we popped/processed
    expanded = 0
    # count how many children we created
    generated = 0
    # first 5 expansions to display
    first5 = []
    # tie-breaker counter
    tie = count()

    # Build the starting node
    r0, c0, _ = start_state
    start_node = (0.0, r0, c0, next(tie), start_state, None, None)

    # define the frontier: min heap
    frontier = [start_node]

    # best_g[state] = cheapest path cost discovered to reach 'state'
    best_g = { start_state: 0.0 }

    # Main loop: while there are nodes to explore
    while frontier:
        # stop if cutoffs are exceeded
        if not within_limits(start_time, expanded):
            return _pack(None, None, expanded, generated, start_time, first5, cutoff=True)

        # pop the cheapest node from the frontier
        g_cost, r, c, tie_id, state, parent_node, action_from_parent = heapq.heappop(frontier)

        # skip this node if we already found a cheaper path to this state
        if g_cost > best_g.get(state, float("inf")):
            continue

        # track how many nodes we expanded
        expanded += 1

        # record the first 5 expanded nodes
        if len(first5) < 5:
            first5.append((state, g_cost))

        # goal check
        if goal_test(state):
            # reconstruct the solution path
            actions, states, final_cost = reconstruct((g_cost, tie_id, state, parent_node, action_from_parent))
            # return results
            return _pack(actions, final_cost, expanded, generated, start_time, first5, cutoff=False)

        # otherwise, expand this node
        for act, next_state, step_cost in successor(state):
            # track generated count
            generated += 1
            # compute path cost for child
            child_g = g_cost + step_cost

            # only queue this child if it is strictly better than any previous path
            if child_g < best_g.get(next_state, float("inf")):
                best_g[next_state] = child_g
                r2, c2, _ = next_state
                parent_5tuple = (g_cost, tie_id, state, parent_node, action_from_parent)  # reconstruct-compatible
                child_node = (child_g, r2, c2, next(tie), next_state, parent_5tuple, act)
                heapq.heappush(frontier, child_node)

    # frontier is empty → no solution
    return _pack(None, None, expanded, generated, start_time, first5, cutoff=False)


# helper to package results in a dict
def _pack(solution, cost, expanded, generated, start_time, first5, cutoff):
    return {
        # list of actions taken to goal
        "solution": solution,
        # total path cost
        "cost": cost,
        # nodes expanded
        "expanded": expanded,
        # successors generated
        "generated": generated,
        # elapsed runtime
        "time": now() - start_time,
        # first five nodes expanded
        "first5": first5,
        # True if we cut off due to limits
        "cutoff": cutoff,
    }