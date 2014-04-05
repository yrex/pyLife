Game Of Life (pyLife)
=====================

This is my implementation of [Conway's Game of Life](http://en.wikipedia.org/wiki/Conway's_Game_of_Life) in Python. There are variations of this available on the Internet, and I wanted to create my version.

Two files are included:
- LaunchLife.py: This is the main file where you can set various parameters and launch Life.
- life.py: This files defines the class Life.

#### General Overview
My implementation uses Numpy, Scipy and Matplotlib. The Life grid is updated on a 2D plot using Matplotlib.


#### Parameters
You can pass various parameters to control the Life grid. These can be expanded further to create a flexible simulation environment.

The parameters available so far are:
- rows: number of rows in the grid
- cols: number of columns in the grid
- steps: number of steps in the simulation
- seedType: select from various grid initial states
- refreshInterval: animation refresh rate (in miliseconds)
- colourmap: choice of matplotlib colourmaps