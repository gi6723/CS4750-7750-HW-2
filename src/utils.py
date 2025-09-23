import time
from typing import Any, Dict, List, Tuple
from problem import MAX_EXPANSIONS, MAX_SECONDS, State

#function to keep track of runtime
def now() -> float:
    return time.perf_counter()


#function to check if we are still within the allowed limits (runtime & expansion)
def within_limits(start_t: float, expanded: int) -> bool:
    #if we've expanded 1,000,000 nodes, stop
    if expanded >= MAX_EXPANSIONS:
        return False
    #if run for more than 3600 secs, stop
    if now() - start_t >= MAX_SECONDS:
        return False
    #Else good to continue
    return True

#Rebuild the solution path
def reconstruct(goal_node: Tuple[float, int, State, Any, str]):
    actions: List[str] = []
    states: List[State] = []

    # ✅ Capture the goal total cost once (this is the correct final cost)
    final_cost = goal_node[0]

    node = goal_node
    while node is not None:
        g_cost, tie_break, state, parent, action = node
        states.append(state)
        actions.append(action)
        node = parent

    # Reverse into start→goal order; drop the initial None action
    actions = [a for a in actions[::-1] if a is not None]
    states = states[::-1]

    return actions, states, final_cost

#Print out the results
def print_result(name: str, result: Dict[str, Any]):
    print(f"\n[{name}] cutoff = {result['cutoff']}")
    print("First 5 expansions (state, g):")  # tiny grammar fix
    for state, g_cost in result.get("first5", []):
        row, col, dirt_set = state
        print(f" pos = ({row},{col}) dirt = {sorted(list(dirt_set))}, g = {g_cost:.2f}")

    print(f"Expanded: {result.get('expanded', 0):,}")
    print(f"Generated: {result.get('generated', 0):,}")
    print(f"Time: {result.get('time',0.0):.3f}")

    if result.get("solution") is not None:
        moves = result["solution"]
        print(f"Moves: {moves}")
        print(f"Number of moves: {len(moves)}")
        print(f"Total cost: {result['cost']:.2f}")
    else:
        print("No solution found (or cutoff forced stop)")


