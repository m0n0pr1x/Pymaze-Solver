#Import argparse to parse the arguments enterred in the terminal
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "uwu"
import argparse
from time import sleep
from Maze import Maze
from MazeLoader import MazeLoader
from MazeSolver import MazeSolver
from MazeGUI import MazeGUI
from MazeExamples import *
from GameEngine import GameEngine



def main():
    """The function that will start the game\n
    Name : main()\n

    Import needed :\n
        -argparse : - pip install argparse -\n
    Arguments :\n
        -f --file : take a maze file and print its solution. Required.\n
        -g --gui : print the solution in a nice GUI. Optional.\n
        -p --play : launch the game. Optional.\n
    """
    global maze_test, maze_test_solving


    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="take a maze file and print its solution.", required="True")
    parser.add_argument("-g", "--gui",  help="print the solution in a nice GUI", action="store_true")
    parser.add_argument("-p", "--play", help="launch the game", action="store_true")

    args = parser.parse_args() # parse the args
    file_path = args.file # get the file provided as param

    #Instancialize the object
    maze_instance = Maze()
    loader_instance = MazeLoader()

    loader_instance.load_maze(file_path)

    matrix = loader_instance.matrix # get the maze file as a matrix
    maze_instance.initializer(matrix) # put the matrix into a maze object
    mazesolver_instance = MazeSolver(maze_instance)

    if args.play:
        # launch the game
        print("let's launch the game")
        game_instance = GameEngine()
        game_instance.init_game(maze_instance, loader_instance, mazesolver_instance)
        game_instance.play()

    elif args.gui:
        gui_instance = MazeGUI()
        gui_instance.matrix=matrix
        gui_instance.load_ressources()
        gui_instance.new_GUI()
        mazesolver_instance.solving()
        gui_instance.show_solution(matrix, mazesolver_instance.solution_finale)
        #The gui must be launched and display the solution

    else:
        mazesolver_instance.solving()
        print(mazesolver_instance.solution_finale)
        # we must print the solution tuple to the console

if __name__ == '__main__':
    main()
