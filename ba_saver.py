from ba import BuchiAutomaton
import pickle

BA_FOLDER_NAME = "saved_BAs"
def save_ba(automaton: BuchiAutomaton, filename: str):
    path = BA_FOLDER_NAME + "/" + filename
    with open(path, "wb") as f:
        pickle.dump(automaton, f)

def load_ba(filename: str) -> BuchiAutomaton:
    path = BA_FOLDER_NAME + "/" + filename
    with open(path, "rb") as f:
        return pickle.load(f)
    
def ask_n_save(ba: BuchiAutomaton):
    print(ba)
    while True:
        answer = input("Do you want to save this BA? (y/n) ")
        if answer == "y":
            filename = input("Choose a filename: ")
            save_ba(ba, filename)
            break
        elif answer == "n":
            break
        else:
            print("Invalid input. Please, reply with 'y' or 'n'.")


if __name__ == "__main__":
    # Edit to define your automaton
    ba = BuchiAutomaton(
        states={"0", "1", "2", "3", "4"},
        alphabet={"a", "b"},
        transitions={},
        initial_state="0",
        accepting_states={"1", "3"}
    )

    # Add transitions: state --symbol--> state,
    ba.add_transition("0", "a", "0")
    ba.add_transition("0", "a", "1")
    ba.add_transition("0", "b", "0")
    ba.add_transition("0", "b", "2")

    ba.add_transition("1", "a", "1")
    ba.add_transition("1", "b", "1")
    ba.add_transition("1", "b", "4")
    
    ba.add_transition("2", "a", "4")
    ba.add_transition("2", "b", "3")
    
    ba.add_transition("3", "a", "4")
    ba.add_transition("3", "b", "3")

    ba.add_transition("4", "a", "4")
    ba.add_transition("4", "b", "4")

    # Dont remove this
    ask_n_save(ba)

