"""Script for saving and loading BAs.

This file allows for saving of BA-objects by writing "pickled" representations
of them to a file with the chosen filename. Likewise, a BA-object can be loaded by 
"unpickling" the data from such a file. (See the module pickle for more details)

Running this file saves the BA defined in its main-method.
Edit the code in the main-method to customize your own BA, 
and run it to start a user interface for saving in the terminal.
"""

from ba import BuchiAutomaton
import pickle
import os

BA_FOLDER_NAME = "saved_BAs"

def save_ba(automaton: BuchiAutomaton, filename: str):
    """
    Description of save_ba

    Args:
        automaton (BuchiAutomaton):
        filename (str):

    """
    """
    Saves a BA-object to a file.

    Args:
        automaton (BuchiAutomaton): The BA to save
        filename (str): Name of the file, to which the BA is saved
    """
    path = os.path.join(BA_FOLDER_NAME, filename)
    with open(path, "wb") as f:
        pickle.dump(automaton, f)

def load_ba(filename: str) -> BuchiAutomaton:
    """
    Loads a BA-object from a file.

    Args:
        filename (str): Name of the file, from which the BA should be loaded

    Returns:
        BuchiAutomaton - The loaded BA
    """
    path = os.path.join(BA_FOLDER_NAME, filename)
    with open(path, "rb") as f:
        return pickle.load(f)
    
def ask_n_save(ba: BuchiAutomaton):
    """
    Terminal user interface for optional saving of a BA.

    Prints the details of the given BA to the terminal, and asks the user if they want to save it to a file.
    If the user inputs 'y', the BA is saved to a filename, also given by the user through the terminal.
    On the other hand, if the user inputs 'n', the BA is not saved.

    Args:
        ba (BuchiAutomaton): The BA that might be saved 
    """
    print(ba)
    while True:
        answer = input("Do you want to save this BA? (y/n) ")
        if answer == "y":
            filename = input("Choose a filename: ")
            save_ba(ba, filename)
            ba.visualize(filename=os.path.join(BA_FOLDER_NAME, filename))
            break
        elif answer == "n":
            break
        else:
            print("Invalid input. Please, reply with 'y' or 'n'.")
    return


if __name__ == "__main__":
    # Edit to define your automaton
    ba = BuchiAutomaton(
        states={"0", "1", "2", "3", "4", "5", "6"},
        alphabet={"a", "b"},
        transitions={},
        initial_state="0",
        accepting_states={"3", "6"}
    )

    # Add transitions: state --symbol--> state,
    ba.add_transition("0", "a", "1")
    ba.add_transition("0", "a", "2")
    ba.add_transition("0", "a", "3")

    ba.add_transition("1", "b", "4")
    ba.add_transition("1", "b", "5")
    ba.add_transition("1", "b", "6")
    
    ba.add_transition("3", "a", "3")
    
    ba.add_transition("6", "b", "6")

    # Dont remove this
    ask_n_save(ba)

