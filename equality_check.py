"""Scripts to test the hypothesis U(A)=U(R)

Let A be a Büchi automaton.
Let R be the result of reducing the non-determinism of A.
Finally, let U be a function that constructs the upper part, as described in Allred & Ultes-Nitsche's algorithm.

Then, this script checks if the relation U(A)=U(R) holds for all Büchi automata A.

Using the terminal as the user interface, the user can initiate the "equality check", either for a specific saved BA, 
or iteratively on multiple randomly generated BAs.
"""

from ba import BuchiAutomaton
from ba_generator import generate_ba
from ba_saver import load_ba, ask_n_save
from tqdm import tqdm
    
def run_equal_check(ba: BuchiAutomaton, verbose: bool = False) -> bool:
    """
    Runs the equality check, i.e. tests if U(A)=U(R) for a given Büchi automaton A.

    Args:
        ba (BuchiAutomaton): The Büchi automaton A
        verbose (bool=False): Set to True to print and plot images of all the constructed BAs, \
            i.e. the original automaton A, the reduced one R, and both constructions U(A) and U(R)

    Returns:
        bool: The result of the equality check
    """
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
        reduced_ba.visualize(filename="renamed_ba")
        red_up.visualize(filename="upper_part_from_reduced_ba")

    if verbose:
        print("---CHECKING FOR EQUALITY----")
        print("upper_part and upper_part_from_reduced_ba are...")
    if uppper_part.equals(red_up):
        if verbose:
            print("EQUAL")
            uppper_part.print_mapping(red_up)
        return True
    else:
        if verbose:
            print("NOT EQUAL")
        return False

def iterate_equal_check(it: int, plotting: bool=False) -> BuchiAutomaton | bool:
    """
    Generates a new BA per iteration, and runs the equality check on it.
    
    Args:
        it (int): Number of iterations, i.e. number of BAs to run the equality check for
        plotting (bool=False): Set to True to plot an image file of each generated BA. Warning: This significantly increases runtime.

    Returns:
        (BuchiAutomaton | bool): True (if all generated BAs passsed the equality check) or the first BA that did not pass the equality check.
    """
    for i in tqdm(range(it)):
        ba = generate_ba()
        if plotting:
            ba.visualize(filename=f"iteration_{str(i+1)}")
        if (run_equal_check(ba)):
            continue
        else:
            return ba
    return True

def run_equal_check_on_ba_file(filename: str) -> bool:
    """
    Runs the equality check, i.e. tests if U(A)=U(R) for a given Büchi automaton A.

    Args:
        filename (str): The filename under which the Büchi Automaton A is saved

    Returns:
        bool: The result of the equality check
    """
    ba = load_ba(filename)
    return run_equal_check(ba, verbose=True)

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
            plot_or_not = input("Do you want the BAs to be plotted (this will slow down the process)? (y/n)\t")
            plotting = True if plot_or_not == "y" else False
            result = iterate_equal_check(iterations, plotting=plotting)
            if result.__class__.__name__=="BuchiAutomaton":
                ask_n_save(result)
            else:
                print(f"Result: {result}")
            done = True
        else:
            print("Invalid input. Please type 's' or 'g'.")
