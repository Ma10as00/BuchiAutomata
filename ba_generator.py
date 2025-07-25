from ba import BuchiAutomaton
import random
from ba_saver import ask_n_save
from ba import PLOTTED_BAs_FOLDER_NAME

# Number of states
MIN_N_STATES = 1
MAX_N_STATES = 6
# Nondeterminism degree
MIN_NONDET_DEGREE = 0   # >1 ensures completeness
MAX_NONDET_DEGREE = 4
# Number of accepting states
MIN_N_ACC_STATES = 1    # >1 ensures acceptance
MAX_N_ACC_STATES = 3
# Size of alphabet
MIN_ALPHABET_SIZE = 2
MAX_ALPHABET_SIZE = 3

def generate_ba(min_n_states: int=MIN_N_STATES,
                max_n_states: int=MAX_N_STATES, 
                min_nondet_degree: int=MIN_NONDET_DEGREE, 
                max_nondet_degree: int=MAX_NONDET_DEGREE,
                min_n_acc_states: int=MIN_N_ACC_STATES, 
                max_n_acc_states: int=MAX_N_ACC_STATES, 
                min_alph_size: int=MIN_ALPHABET_SIZE, 
                max_alph_size: int=MAX_ALPHABET_SIZE) -> BuchiAutomaton:
    
    n_states = random.randint(min_n_states, max_n_states)
    generated_states = set([str(i) for i in range(n_states)])
    n_acc_states = random.randint(min(min_n_acc_states, n_states), min(max_n_acc_states, n_states))
    generated_acc_states = set(random.sample(list(generated_states), n_acc_states))
    generated_alphabet = set([chr(ord('a') + i) for i in range(random.randint(min_alph_size, max_alph_size))])

    # Initialize BA without transitions
    ba = BuchiAutomaton(
        states=generated_states,
        alphabet=generated_alphabet,
        transitions={},
        initial_state="0",
        accepting_states=generated_acc_states,
    )

    # Add transitions
    for state in ba.states:
        for symbol in ba.alphabet:
            done = set() # To avoid choosing same target twice
            for i in range(random.randint(min(min_nondet_degree, n_states), min(max_nondet_degree, n_states))):
                target = random.choice(list(ba.states.difference(done)))
                ba.add_transition(state, symbol, target)
                done.add(target)
    
    return ba

if __name__ == "__main__":
    ba = generate_ba()
    ba.visualize("generated_ba")
    print("The generated BA can be viewed in the file 'generated_ba.png' in the folder '" + PLOTTED_BAs_FOLDER_NAME + "'")
    ask_n_save(ba)
