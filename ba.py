from dataclasses import dataclass, field
from typing import Set, Dict, Tuple
from graphviz import Digraph
import re
import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher

PLOTTED_BAs_FOLDER_NAME = "plots"

@dataclass
class BuchiAutomaton:
    states: Set[str] = field(default_factory=set)
    alphabet: Set[str] = field(default_factory=set)
    transitions: Dict[Tuple[str, str], Set[str]] = field(default_factory=dict) # (state, symbol) -> set of target states
    initial_state: str = field(default_factory=str)
    accepting_states: Set[str] = field(default_factory=set)

    def add_transition(self, from_state: str, symbol: str, to_state: str, accept_new_elements: bool = True) -> None:
        if accept_new_elements:
            if from_state not in self.states:
                self.states.add(from_state)
            if symbol not in self.alphabet:
                self.alphabet.add(symbol)
            if to_state not in self.states:
                self.states.add(to_state)
        else:
            assert from_state in self.states, "Cannot add transition from non-existing state"
            assert symbol in self.alphabet, "Cannot add transition with non-existing symbol"
            assert to_state in self.states, "Cannot add transition to non-existing state"
            
        key = (from_state, symbol)
        if key not in self.transitions:
            self.transitions[key] = set()
        self.transitions[key].add(to_state)

    def visualize(self, filename: str="buchi_automaton") -> None:
        """
        Writes an image of this BuchiAutomaton to a file with the specified filename.
        """
        graph = Digraph(engine="circo")   # Options: "circo", "twopi", "fdp", "sfdp", "neato"
        # graph.attr(nodesep="0.5")
        # graph.attr(ranksep="0.5")
        graph.attr(splines="polyline")

        # Special case: Empty BA
        if self.is_empty():
            graph.node(f"init", label="", shape="point")
            graph.node("nothing", label="nothing", shape="none")
            graph.edge(f"init", "nothing")
            graph.render(PLOTTED_BAs_FOLDER_NAME + "/" + filename, format="png", cleanup=True)
            return

        # Mark initial states with an arrow
        graph.node(f"init_{self.initial_state}", label="", shape="point")
        graph.edge(f"init_{self.initial_state}", self.initial_state)

        # Define states
        for state in self.states:
            shape = "doublecircle" if state in self.accepting_states else "circle"
            graph.node(state, shape=shape)

        # Add transitions
        done = set()
        for (from_state, symbol), to_states in self.transitions.items():
            for to_state in to_states:
                if (from_state, to_state) not in done:
                    # Check if there are multiple symbols leading to the same state
                    label_symbols = symbol
                    for other_symbol in self.alphabet:
                        if (other_symbol is not symbol) and \
                                ((from_state, other_symbol) in self.transitions) and \
                                (to_state in self.transitions[(from_state, other_symbol)]):
                            label_symbols += other_symbol
                    label = ''.join(sorted(label_symbols))
                    # Draw the edge labeled with all apropriate symbols
                    graph.edge(from_state, to_state, taillabel=label, labelfontsize='12', labelangle='15', labeldistance='2')
                    done.add((from_state, to_state))

        graph.render(PLOTTED_BAs_FOLDER_NAME + "/" + filename, format="png", cleanup=True)

    def reduce_nondeterm(self) -> "BuchiAutomaton":
        """
        Executes an algorithm to reduce the non-determinism degree of the Büchi automaton. 
        The resulting BA will have non-determinism degree <= 2. Furthermore, if the non-determinism degree is exactly 2,
        a state with two possible transitions for a given symbol will always lead to one accepting state
        and one non-accepting state for this symbol (i.e., it will satisfy property P).

        This function assumes that the original automaton's state ids does not contain any commas (',').
        This condition can be fullfilled by calling rename_states().

        :return: A Büchi automaton that accepts the same language as this, with a non-determinism degree of at most 2
        """
        # Initialize the reduced automaton with the initial state
        reduced_states = set()
        reduced_states.add(self.initial_state)
        reduced_ba = BuchiAutomaton(states=reduced_states, 
                                    alphabet=self.alphabet, 
                                    initial_state=self.initial_state)
        # Initialize sets to keep track of which states have been checked for new transitions
        to_do = reduced_states.copy()
        done = set()
        while (to_do):
            # Pick a state from the to_do list
            current_state = to_do.pop()
            # If it represents several states from the original automaton, we should consider them all individually
            repr_states = current_state.split(sep=",")

            # Go through all possible input symbols
            for symbol in self.alphabet:
                target_states = set()
                for state in repr_states:
                    if ((state, symbol) in self.transitions.keys()):
                        target_states = target_states.union(self.transitions[(state, symbol)])
                
                # Split target states into accepting and non-accepting
                accepting_target_states = []
                nonacc_target_states = []
                for target in target_states:
                    if target in self.accepting_states:
                        accepting_target_states.append(target)
                    else:
                        nonacc_target_states.append(target)

                # Add new transitions in the reduced automaton
                if accepting_target_states:
                    # Build string of target state (Sort to avoid duplicates)
                    new_state = ",".join(sorted(accepting_target_states))
                    # Add target state to to_do list if not already added
                    if (new_state not in done):
                        if (new_state not in to_do):
                            if (not new_state == current_state):
                               to_do.add(new_state)
                    # Add transition and mark target state as accepting
                    reduced_ba.add_transition(current_state, symbol, new_state)
                    reduced_ba.accepting_states.add(new_state)
                    
                if nonacc_target_states:
                    # Build string of target state (Sort to avoid duplicates)
                    new_state = ",".join(sorted(nonacc_target_states))
                    # Add target state to to_do list if not already added
                    if (new_state not in done):
                        if (new_state not in to_do):
                            if (not new_state == current_state):
                               to_do.add(new_state)
                    # Add transition
                    reduced_ba.add_transition(current_state, symbol, new_state)

            # Mark the current state as checked for transitions
            done.add(current_state)
        
        return reduced_ba

    def upper_part(self) -> "BuchiAutomaton":
        """
        Constructs the upper part A' of the complement automaton, given Büchi Automaton A.

        This function assumes that the original automaton's state ids does not contain any commas or curly brackets (, { }).
        This condition can be fullfilled by calling rename_states().
        """
        # Initialize the reduced automaton with the initial state
        states = set()
        states.add("{"+self.initial_state+"}")
        upper_part = BuchiAutomaton(states=states, 
                                    alphabet=self.alphabet, 
                                    initial_state="{"+self.initial_state+"}")
        # Initialize sets to keep track of which states have been checked for new transitions
        to_do = states.copy()
        done = set()
        while (to_do):
            # Pick a state from the to_do list
            current_state = to_do.pop()

            # If it contains several sets of states, we need to split them up
            state_sets = re.findall(r'\{([^}]*)\}', current_state) # identifies groups within curly brackets in a string
            state_sets.reverse() # to consider the right-most set first

            # Go through all possible input symbols
            for symbol in self.alphabet:

                # Initialize new state
                new_state_sets = []

                for state_set in state_sets:
                    # If the set represents several states from the original automaton, we should consider them all individually
                    repr_states = state_set.split(sep=",")
                    target_states = set()
                    for state in repr_states:
                        if ((state, symbol) in self.transitions.keys()):
                            target_states = target_states.union(self.transitions[(state, symbol)])
                    
                    # Split target states into accepting and non-accepting
                    accepting_target_states = []
                    nonacc_target_states = []
                    for target in target_states:
                        if target in self.accepting_states:
                            accepting_target_states.append(target)
                        else:
                            nonacc_target_states.append(target)

                    # Add new sets to the new state
                    if accepting_target_states:
                        # Build string for the accepting target set
                        accepting_set_string = "{" + ",".join(sorted(accepting_target_states)) + "}"
                        # Add it to the new state if not already present
                        if accepting_set_string not in new_state_sets:
                            new_state_sets.append(accepting_set_string)

                    if nonacc_target_states:
                        # Build string for the non-accepting target set
                        nonacc_set_string = "{" + ",".join(sorted(nonacc_target_states)) + "}"
                        if nonacc_set_string not in new_state_sets:
                            new_state_sets.append(nonacc_set_string)

                if new_state_sets:
                    # Build string for new state
                    new_state = ",".join(sorted(new_state_sets))
                    # Add new state to to_do list if not already added
                    if (new_state not in done):
                        if (new_state not in to_do):
                            if (not new_state == current_state):
                                to_do.add(new_state)
                    # Add transition to new state
                    upper_part.add_transition(current_state, symbol, new_state)

            # Mark the current state as checked for transitions
            done.add(current_state)
        
        return upper_part

    def rename_states(self) -> None:
        """
        Renames the states of this BuchiAutomaton to simply "0", "1", "2", ...
        """
        old_states = list(self.states)
        new_states = [str(i) for i in range(len(old_states))]
        # Mapping from old names to new names
        map = dict(zip(old_states, new_states))

        states = set(new_states)
        alphabet = self.alphabet
        transitions = {(map[from_state], symbol): set([map[s] for s in to_states]) for (from_state, symbol), to_states in self.transitions.items()}
        initial_state = map[self.initial_state]
        accepting_states = set([map[s] for s in self.accepting_states])

        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def is_valid(self) -> bool:
        """
        Checks if this BA is valid, i.e. that the states, tranistions, initial state and accepting states all match.
        """
        if self.initial_state not in self.states and not self.initial_state == "":
            return False
        if not self.accepting_states.issubset(self.states):
            return False
        for (from_state, symbol), to_states in self.transitions.items():
            if (from_state not in self.states) or \
               (symbol not in self.alphabet) or \
               (not to_states.issubset(self.states)):
                return False
        return True
    
    def is_empty(self) -> bool:
        """
        Checks if this BA is valid and empty, i.e. without any states.
        """
        return self.is_valid() and len(self.states) < 1
    
    def is_complete(self) -> bool:
        """
        Checks if this BA is valid and complete, i.e. every state has a transition for every symbol in the alphabet.
        """
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) in self.transitions.keys() and self.transitions[(state, symbol)]:
                    continue
                else:
                    return False
        return True
    
    def copy(self) -> "BuchiAutomaton":
        copy = BuchiAutomaton(
            states=self.states,
            alphabet=self.alphabet,
            transitions=self.transitions,
            initial_state=self.initial_state,
            accepting_states=self.accepting_states
        )
        return copy

    def __str__(self):
        def transitions_str():
            return "\n".join([f"{from_state} --{symbol}--> {to_states}" for (from_state, symbol), to_states in self.transitions.items()])
        return (
            f"States: {self.states}\n"
            f"Alphabet: {self.alphabet}\n"
            f"Initial State: {self.initial_state}\n"
            f"Accepting States: {self.accepting_states}\n"
            f"Transitions: \n{transitions_str()}"
        ) 

    def to_nx_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        for state in self.states:
            G.add_node(state, 
                    is_initial=state == self.initial_state,
                    is_accepting=state in self.accepting_states)
        for (from_state, symbol), targets in self.transitions.items():
            for tgt in targets:
                G.add_edge(from_state, tgt, symbol=symbol)
        return G

    def equals(self, other: "BuchiAutomaton") -> bool:
        G1 = self.to_nx_graph()
        G2 = other.to_nx_graph()

        node_match = lambda n1, n2: n1 == n2
        edge_match = lambda e1, e2: e1['symbol'] == e2['symbol']

        matcher = DiGraphMatcher(G1, G2, node_match=node_match, edge_match=edge_match)
        if matcher.is_isomorphic():
            print("Isomorphism:")
            print("\n".join(sorted([f"{key}\t--->\t{value}" for key, value in matcher.mapping.items()])))
            return True
        else:
            print("No isomorphism found.")
            return False
    
if __name__ == "__main__":
    from ba_generator import generate_ba

    ba = generate_ba(max_n_states=5, max_n_acc_states=1)
    
    # Test: ba == ba.rename_states()
    renamed = ba.copy()
    renamed.rename_states()
    print("Equal after renaming...")
    assert ba.equals(renamed)
    print("Test passed!")
    ba.visualize("original_ba")
    renamed.visualize("renamed_ba")

    # Test: Empty BA == Empty BA
    ba = BuchiAutomaton()
    assert ba.is_empty()
    other = ba.copy()
    print("Empty BAs are equal...")
    assert ba.equals(other)
    print("Test passed!")
    ba.visualize("empty_ba")

    # Test: Validation
    print("Validation works correctly...")
    ## Ex: valid
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('2','b'): {'2'}},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert ba.is_valid()
    ## Ex: invalid accepting state
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('2','b'): {'2'}},
        initial_state='1',
        accepting_states={'3'}   
    )
    assert not ba.is_valid()
    ## Ex: invalid transition symbol
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('2','b'): {'2'}},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert not ba.is_valid()
    ## Ex: invalid initial state
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('2','b'): {'2'}},
        initial_state='3',
        accepting_states={'2'}   
    )
    assert not ba.is_valid()
    ## Ex: invalid from_state
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('3','b'): {'2'}},
        initial_state='2',
        accepting_states={'2'}   
    )
    assert not ba.is_valid()
    ## Ex: invalid to_state
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('2','b'): {'3'}},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert not ba.is_valid()
    print("Test passed!")

    # Test: is_complete()
    ## Ex: complete
    print("Completeness check works properly...")
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'2'},
                     ('2','b'): {'2'}},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert ba.is_complete()
    ## Ex: Missing symbol in keys
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'1'},
                     ('2','a'): {'2'}},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert not ba.is_complete()
    ## Ex: Missing state in keys
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'}},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert not ba.is_complete()
    ## Ex: Empty transition (leading nowhere)
    ba = BuchiAutomaton(
        states={'1','2'},
        alphabet={'a','b'},
        transitions={('1','a'): {'1'},
                     ('1','b'): {'2'},
                     ('2','a'): {'1'},
                     ('2','b'): set()},
        initial_state='1',
        accepting_states={'2'}   
    )
    assert not ba.is_complete()
    print("Test passed!")