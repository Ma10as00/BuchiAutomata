"""Script to redraw all the plots of saved BAs. 

Whenever the implementation of BuchiAutomaton.visualize() changes, 
this python file can be ran to update the plots in "BuchiAutomata/plots/saved_BAs" 
according to the new visualize() function. 

Particularly useful if you want to change the rendering engine, 
or tweek attributes to get your desired automaton layout.
"""

from ba_saver import load_ba
from ba_saver import BA_FOLDER_NAME
import os

if __name__ == "__main__":
    saved_files = os.listdir(BA_FOLDER_NAME)
    for filename in saved_files:
        ba = load_ba(filename=filename)
        ba.visualize(filename=os.path.join(BA_FOLDER_NAME, filename))