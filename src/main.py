#Ian Cooper & Gianni Ioannou

from problem import INSTANCE_1, INSTANCE_2
from utils import print_result
from UCTS import ucts
from UCGS import graph_search
from IDTS import idts

def run_on_instance(name: str, start_state):
    print(f"\n================ {name} ================")

    # Uniform-Cost Tree Search
    res_ucts = ucts(start_state)
    print_result("UCTS", res_ucts)

    # Uniform-Cost Graph Search
    res_ucgs = graph_search(start_state)
    print_result("UCGS", res_ucgs)

    # Iterative Deepening Tree Search
    res_idts = idts(start_state)
    print_result("IDTS", res_idts)

if __name__ == "__main__":
    run_on_instance("Instance 1", INSTANCE_1)
    run_on_instance("Instance 2", INSTANCE_2)
