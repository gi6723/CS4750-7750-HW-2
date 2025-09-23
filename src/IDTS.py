from typing import Any, Dict, Optional, Tuple
from itertools import count
from problem import State, goal_test, successor
from utils import now, within_limits, reconstruct

def idts(start_state: State, max_depth: int = 10_000) -> Dict[str, Any]:
    """
    Run Iterative Deepening Tree Search from depth = 0 up to max_depth.
    Returns the same result dict shape used by your other algorithms.
    """
    start_time = now()

    # Totals across all depth iterations
    expanded_total = 0      # nodes popped/processed
    generated_total = 0     # successors produced
    first5 = []             # first five expansions overall (state, g)

    # A simple monotonic counter to attach as tie_id when we create nodes
    tie = count()

    # Depth loop: try depth limits 0, 1, 2, ...
    for limit in range(0, max_depth + 1):
        # Per-iteration counters that roll into totals after each DLS
        expanded = expanded_total
        generated = 0

        goal_node, cutoff_due_to_limits = _dls_tree(
            start_state=start_state,
            depth_limit=limit,
            start_time=start_time,
            counters={"expanded": expanded, "generated": generated},
            first5=first5,
            tie=tie
        )

        # Pull back the updated counters
        expanded_total = goal_node["expanded_after"] if goal_node else _extract_expanded(goal_node, expanded)
        generated_total += goal_node["generated_this_iter"] if goal_node else generated

        # If we exceeded global limits during this iteration, stop and report
        if cutoff_due_to_limits or not within_limits(start_time, expanded_total):
            return _pack(
                solution=None, cost=None, expanded=expanded_total,
                generated=generated_total, start_time=start_time,
                first5=first5, cutoff=True
            )

        # Found a solution at this depth?
        if goal_node and goal_node["node"] is not None:
            # Reconstruct using shared utility
            actions, states, final_cost = reconstruct(goal_node["node"])
            return _pack(
                solution=actions, cost=final_cost, expanded=expanded_total,
                generated=generated_total, start_time=start_time,
                first5=first5, cutoff=False
            )

    # Reached max_depth without finding a solution
    return _pack(
        solution=None, cost=None, expanded=expanded_total,
        generated=generated_total, start_time=start_time,
        first5=first5, cutoff=False
    )

# Helper for depth-limited search (DLS) within IDTS
def _dls_tree(start_state: State,
              depth_limit: int,
              start_time: float,
              counters: Dict[str, int],
              first5,
              tie) -> Tuple[Optional[Dict[str, Any]], bool]:

    # Stack entries: (state, parent_node, action_from_parent, depth, g_cost, tie_id)
    # We include tie_id to keep a consistent node shape if we hit the goal.
    stack = [(start_state, None, None, 0, 0.0, next(tie))]

    # Track how many generated in THIS depth iteration
    generated_this_iter = 0

    while stack:
        # Global cutoff check (based on counters["expanded"])
        if not within_limits(start_time, counters["expanded"]):
            # No goal; signal cutoff due to limits
            return None, True

        state, parent_node, action_from_parent, depth, g_cost, my_tie = stack.pop()

        # We've popped it → count an expansion
        counters["expanded"] += 1

        # Record first five expansions overall
        if len(first5) < 5:
            first5.append((state, g_cost))

        # Goal check
        if goal_test(state):
            # Build a UCS-style node tuple so utils.reconstruct works
            goal_tuple = (g_cost, my_tie, state, parent_node, action_from_parent)
            return ({
                "node": goal_tuple,
                "expanded_after": counters["expanded"],
                "generated_this_iter": generated_this_iter
            }, False)

        # If under depth limit, expand successors
        if depth < depth_limit:
            # Generate successors (count all of them as "generated")
            succs = list(successor(state))
            generated_this_iter += len(succs)

            # Push children to the stack (LIFO). Reverse to keep the first successor expanded next.
            for act, next_state, step_cost in reversed(succs):
                child_g = g_cost + step_cost
                child_tie = next(tie)
                child_parent = (g_cost, my_tie, state, parent_node, action_from_parent)
                stack.append((next_state, child_parent, act, depth + 1, child_g, child_tie))

        # Else: at depth limit → do not expand further; continue loop

    # Searched entire fringe up to depth_limit with no solution, no cutoff
    return ({
        "node": None,
        "expanded_after": counters["expanded"],
        "generated_this_iter": generated_this_iter
    }, False)

def _extract_expanded(goal_node, fallback_expanded):
    # Helper to get expanded count whether we found a goal or not
    if goal_node and "expanded_after" in goal_node:
        return goal_node["expanded_after"]
    return fallback_expanded

def _pack(solution, cost, expanded, generated, start_time, first5, cutoff):
    return {
        "solution": solution,
        "cost": cost,
        "expanded": expanded,
        "generated": generated,
        "time": now() - start_time,
        "first5": first5,
        "cutoff": cutoff,
    }