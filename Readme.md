# Daggerfall Spell Calculator
This is a side project intended to calculate out data related to spells in the game Daggerfall.

It started as a simple optimization on a fatigue spell, but I figured I might as well make a whole system to optimize spell output
for given parameters.

## state of the program

The program isn't close to complete yet.

Right now it can derive a dictionary of all the possible base spells in the game from the table on the wiki and accurately caluclate the 
base cost of the spell in terms of cost. Character specific mana costs & well as more breadth of data as well as custom optimizations on
that data are still to come. 

The base spell organization also needs to be adjusted to account for multiple effects on one spell.

There also isn't an interface for anything yet so everything has to be tested through change in source code at the main level.

Overall organization is also completely subject to change, although what is here will probably stay in some form or another.