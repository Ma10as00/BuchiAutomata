# BuchiAutomata
Tool for conceptualizing and visualizing Büchi automata.

As part of my master thesis project, I developed a Python implementation of Büchi Automata (BA) to support quicker evaluation of new hypotheses.
The code consists of 5 scripts: 
- ba.py
- ba_generator.py
- ba_saver.py
- redrawing_py
- equality_check.py

## ba.py
This file defines the class BuchiAutomaton which holds all the data of a BA, as well as class-specific methods. 

The class BuchiAutomaton holds field variables for an automaton’s states, alphabet, transition function, initial state, and the set of accepting states. Class-specific methods include simple operations, such as adding a transition, as well as more complex algorithms, like the reduction algorithm described in [2] and the upper part construction from the complementation algorithm in [1]. There is also a method to check for isomorphism with another automaton, using a DiGraphMatcher from the library NetworkX ([7]). The visualize()-method imports functionality from another library, Graphviz ([8]), and was used to render all figures of Büchi automata in my master thesis.

## ba_generator.py
The BA-generator can generate random Büchi Automata, with parameters controlling their size and non-determinism degree. 

## ba_saver.py
Finally, ba_saver.py provides a file management system, taking care of saving and loading BA-files.

## redrawing.py
To customize the generated plots of different BAs, I sometimes tweaked some attributes in the ba.visualize() method.
Then, this script was ran to re-render all the plots of my saved BAs, according to the updated visualizing method.

## equality_check.py
This script  was developed to test the hypothesis U(A)=U(R), i.e. to visualize the results of both paths to the upper part construction, given a Büchi automata A; the direct path without reduction and the indirect path via non-determinism reduction. To identify counter examples, the script was built to generate random automata and compare the output automata U(A) and U(R).

For more details, please refer to the full thesis.
