from ba import BuchiAutomaton
import pickle
import os

BA_FOLDER_NAME = "saved_BAs"

def save_ba(automaton: BuchiAutomaton, filename: str):
    path = os.path.join(BA_FOLDER_NAME, filename)
    with open(path, "wb") as f:
        pickle.dump(automaton, f)

def load_ba(filename: str) -> BuchiAutomaton:
    path = os.path.join(BA_FOLDER_NAME, filename)
    with open(path, "rb") as f:
        return pickle.load(f)
    
def ask_n_save(ba: BuchiAutomaton):
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


if __name__ == "__main__":
    # Edit to define your automaton
    ba = BuchiAutomaton(
        states={"0", "1", "2", "3"},
        alphabet={"a", "b"},
        transitions={},
        initial_state="0",
        accepting_states={"1"}
    )

    # Add transitions: state --symbol--> state,
    ba.add_transition("0", "a", "0")
    ba.add_transition("0", "b", "1")
    ba.add_transition("0", "b", "0")

    ba.add_transition("1", "a", "2")
    ba.add_transition("1", "a", "3")
    ba.add_transition("1", "b", "1")
    
    ba.add_transition("2", "a", "2")
    ba.add_transition("2", "a", "3")
    ba.add_transition("2", "b", "2")
    
    ba.add_transition("3", "a", "3")
    ba.add_transition("3", "b", "1")

    # Dont remove this
    ask_n_save(ba)

