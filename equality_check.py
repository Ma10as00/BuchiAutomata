from ba import BuchiAutomaton
from ba_generator import generate_ba
from ba_saver import load_ba
from tqdm import tqdm
    
def run_equal_check(ba: BuchiAutomaton, verbose: bool = False) -> bool:
    
    if verbose:
        # Print the automaton's structure
        print(ba)

    # Print automaton reduced to nondeterminism degree 2
    reduced_ba = ba.reduce_nondeterm()
    if verbose:
        print("-" * 5 + "REDUCED" + "-" * 5)
        print(reduced_ba)

    # Print upper part derived from ba
    uppper_part = ba.upper_part()
    if verbose:
        print("-" * 5 + "UPPER PART" + "-" * 5)
        print(uppper_part)

        # Visualize it
        ba.visualize(filename="original_ba")
        reduced_ba.visualize(filename="reduced_ba")
        uppper_part.visualize(filename="upper_part")
    
    reduced_ba.rename_states()
    red_up = reduced_ba.upper_part()
    if verbose:
        red_up.rename_states()
        red_up.visualize(filename="upper_part_from_reduced_ba")

    if verbose:
        print("---CHECKING FOR EQUALITY----")
        print("upper_part and upper_part_from_reduced_ba are...")
    if uppper_part.equals(red_up):
        if verbose:
            print("EQUAL")
        return True
    else:
        if verbose:
            print("NOT EQUAL")
        return False

def iterate_equal_check(it: int) -> BuchiAutomaton | bool:
    """
    Generates a new BA per iteration, and runs the equality check on it.
    
    :return: True (if all generated BAs passsed the equality check) or the first BA that did not pass the equality check.
    """
    for i in tqdm(range(it)):
        ba = generate_ba()
        ba.visualize(filename=f"iteration_{str(i+1)}")
        if (run_equal_check(ba, False)):
            continue
        else:
            return ba
    return True

def run_equal_check_on_ba_file(filename: str) -> bool:
    ba = load_ba(filename)
    return run_equal_check(ba, True)

if __name__ == "__main__":
    done = False
    while not done:
        version = input("Do you want to test a (s)pecific BA for equality, " \
        "or do you want to run equality tests on a number of (g)enerated BAs?\t")
        if version == "s":
            filename = input("Please input the filename of your specific saved BA:\t")
            print(f"Result: {run_equal_check_on_ba_file(filename)}")
            done = True
        elif version == "g":
            iterations = int(input("How many BAs should we generate and check for equality?\t"))
            print(f"Result: {iterate_equal_check(iterations)}")
            done = True
        else:
            print("Invalid input. Please type 's' or 'g'.")
