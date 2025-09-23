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
    #empty lists to collect actions taken and the visited states
    actions: List[str] = []
    states: List[State] = []

    #start from the goal node
    node = goal_node
    while node is not None:
        #node tuple
        g_cost, tie_break, state, parent, action = node

        #save the state and actions
        states.append(state)
        actions.append(action)

        #move parent node
        node = parent
    #reverse actions to get the correct route
    actions = [a for a in actions[::-1] if a is not None] #Might change confused
    #Reverse the states so they go from start to goal
    states = states[::-1]

    #return the correct path
    return actions, states, g_cost


#Print out the results
def print_result(name: str, result: Dict[str, Any]):
    print(f"\n[{name}] cutoff = {result['cutoff']}")
    print("First 5 expansion (state, g):")
    #Loop over the first five nodes that were expanded and print
    for state, g_cost in result.get("first5", []):
        #unpack the state
        row, col, dirt_set = state
        #show position, sorted cells, path cost
        print(f" pos = ({row},{col}) dirt = {sorted(list(dirt_set))}, g = {g_cost:.2f}")
    #print out required stats
    print(f"Expanded: {result.get('expanded', 0):,}")
    print(f"Generated: {result.get('generated', 0):,}")
    print(f"Time: {result.get('time',0.0):.3f}")
    #if a solution was found, print moves and cost
    if result.get("solution") is not None:
        print(f"Moves: {result['solution']}")
        print(f"Total cost: {result['cost']:.2f}")
    else:
        #else say no solution was found
        print("No solution found (or cutoff forced stop)")

