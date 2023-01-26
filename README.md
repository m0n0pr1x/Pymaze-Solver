# Maze Solver

A Python program that solves mazes with doors and ghosts, and finds the shortest solution to reach the exit.

## Usage

To run the program, call it with the -f or --file argument specifying the maze file to solve.

python maze_solver.py -f maze.txt

### Optional arguments

    -g: Show the solution step by step in a graphical user interface (GUI). In the GUI, the print of the solution can be accelerated with the space bar.
    -p: Launch a GUI with a pacman that can be controlled by the player to solve the maze.

## Example
```python
python maze_solver.py -f maze.txt -g
```
This command will solve the maze in the file "maze.txt" and display the solution in a GUI, where the user can step through the solution one move at a time using the space bar.
```python
python maze_solver.py -f maze.txt -p
```

This command will open a GUI with a pacman that can be controlled by the player to solve the maze in the file "maze.txt"
Maze files example are provided in the maze_files folder.

## Note

Please make sure to provide a valid maze file with the correct format.

