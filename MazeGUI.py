import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "uwu"

import pygame
import MazeLoader
import sys
import time
from copy import deepcopy
from PIL import Image
"""
Program that displays the game using the library pygame.\n
"""
class MazeGUI():
    """
    Class that displays the game\n
    """
    def __init__(self, win_title="PyMaze - AROF", win_height=900, win_width=900):
        """Constructor of the class\n

        Args:\n
            win_title (str, optional): title of the window. Defaults to "PyMaze - AROF".\n
            win_height (int, optional): height of the window. Defaults to 900.\n
            win_width (int, optional): width of the windows. Defaults to 900.\n
            matrix (str, optional): matrix of the game.\n
        """
        self.__win_title = win_title
        self.__win_height = win_height
        self.__win_width = win_width
        #Matrix will be change once loaded by MazeLoader
        self.__matrix = None
        self.__ressources = {}
        self.__clock = None
        self.__screen = None

    @property    
    def win_title(self):
        """Getter method of self.__win_title\n
        """
        return self.__win_title
    @property 
    def win_height(self):
        """Getter method of self.__win_height\n
        """
        return self.__win_height
    @property 
    def win_width(self):
        """Getter method of self.__win_width\n
        """
        return self.__win_width
    @property 
    def matrix(self):
        """Getter method of self.__matrix\n
        """
        return self.__matrix
    @property 
    def ressources(self):
        """Getter method of self.__ressources\n
        """
        return self.__ressources
    @property 
    def clock(self):
        """Getter of self.__clock\n
        """
        return self.__clock
    @property 
    def screen(self):
        """Getter of self.__screen\n
        """
        return self.__screen

    @win_title.setter
    def win_title(self, title="PyMaze - AROF"):
        """Setter method of self.__win_title\n

        Args:\n
            win_title (str, optional): title of the window. Defaults to "PyMaze - AROF".\n
        """
        self.__win_title = title

    @win_height.setter
    def win_height(self, height=900):
        """Setter method of self.__win_height\n

        Args:\n
            win_height (int, optional): height of the window. Defaults to 900.\n
        """
        self.__win_height = height

    @win_width.setter
    def win_width(self, width=900):
        """Setter method of self.__win_width\n

        Args:\n
            win_width (int, optional): width of the windows. Defaults to 900.\n
        """
        self.__win_width = width

    @matrix.setter
    def matrix(self, matrix=None):
        """Setter method of self.__matrix\n
        Args:\n
            matrix (str, optional): matrix of the game. Defaults to "None".\n
        """
        self.__matrix = matrix

    @ressources.setter
    def ressources(self, ressource_dict):
        """Setter method of self.__ressources\n
        Args:\n
            ressources_dict (dict): dictionnary of all the ressources of the game name:pygameressource\n
        """
        self.__ressources = ressource_dict

    @clock.setter
    def clock(self, clock):
        """Setter of self.__clock\n
        """
        self.__clock = clock

    @screen.setter
    def screen(self, screen):
        """Setter of self.__screen\n
        """
        self.__screen = screen
        
    def load_ressources(self):
        """Method to load all the ressources of the game\n
        """
        block = pygame.image.load(os.path.join("./imgs/", "block.png"))
        blue_door = pygame.image.load(os.path.join("./imgs/", "blue_door.png"))
        blue_key = pygame.image.load(os.path.join("./imgs/", "blue_key.png"))
        ghost = pygame.image.load(os.path.join("./imgs/", "ghost.png"))
        green_door = pygame.image.load(os.path.join("./imgs/", "green_door.png"))
        green_key = pygame.image.load(os.path.join("./imgs/", "green_key.png"))
        pacman = pygame.image.load(os.path.join("./imgs/", "pacman.png"))
        path = pygame.image.load(os.path.join("./imgs/", "path.png"))
        pink_cell = pygame.image.load(os.path.join("./imgs/", "pink_cell.png"))
        red_door = pygame.image.load(os.path.join("./imgs/", "red_door.png"))
        red_key = pygame.image.load(os.path.join("./imgs/", "red_key.png"))
        reward = pygame.image.load(os.path.join("./imgs/", "reward.png"))
        yellow_door = pygame.image.load(os.path.join("./imgs/", "yellow_door.png"))
        yellow_key = pygame.image.load(os.path.join("./imgs/", "yellow_key.png"))
        solution_path = pygame.image.load(os.path.join("./imgs/", "solution.png"))
        solution_path2 = pygame.image.load(os.path.join("./imgs/", "solution2.png"))
        solution_path3 = pygame.image.load(os.path.join("./imgs/", "solution3.png"))
        solution_path4 = pygame.image.load(os.path.join("./imgs/", "solution4.png"))
        solution_path5 = pygame.image.load(os.path.join("./imgs/", "solution5.png"))
        solution_path6 = pygame.image.load(os.path.join("./imgs/", "solution6.png"))
        solution_path7 = pygame.image.load(os.path.join("./imgs/", "solution7.png"))
        
        self.ressources=  {"1":block, "i":blue_door, "h":blue_key, "ghost":ghost, "c":green_door, 
                             "d":green_key, "s":pacman, "0":path, "-1":pink_cell, "g":red_door,
                             "f":red_key, "e":reward, "b":yellow_door, "a":yellow_key, "z":solution_path,
                             "y":solution_path2, "x":solution_path3, "w":solution_path4, "v":solution_path5, 
                             "u":solution_path6, "t":solution_path7}
    
    def new_GUI(self):
        """Create a new window\n
        """
        self.clock=pygame.time.Clock()
        self.screen=pygame.display.set_mode((53*len(self.__matrix[0]),53*len(self.__matrix)))
        
        self.load_ressources()
        
        pygame.mouse.set_visible(0)
        pygame.display.caption=self.win_title
        
    def show_solution(self, matrix, solution_path, refresh_rate=3):
        """Method that will update the screen and show the path\n

        Args:\n
            matrix (list): matrix of the game\n
            solution_path (list): list of tuple position of the solutions.\n
        """
        solution_matrix = deepcopy(matrix)
        refresh_delay = 1/refresh_rate
        
        for coord in solution_path:
            if solution_matrix[coord[0]][coord[1]] == 'z':
                solution_matrix[coord[0]][coord[1]] = 'y'
                
            elif solution_matrix[coord[0]][coord[1]] == 'y':
                solution_matrix[coord[0]][coord[1]] = 'x'
                
            elif solution_matrix[coord[0]][coord[1]] == 'x':
                solution_matrix[coord[0]][coord[1]] = 'w'
                
            elif solution_matrix[coord[0]][coord[1]] == 'w':
                solution_matrix[coord[0]][coord[1]] = 'v'
                
            elif solution_matrix[coord[0]][coord[1]] == 'v':
                solution_matrix[coord[0]][coord[1]] = 'u'
                
            elif solution_matrix[coord[0]][coord[1]] == 'u':
                solution_matrix[coord[0]][coord[1]] = 't'

            else:
                solution_matrix[coord[0]][coord[1]] = "z"
            

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                refresh_delay =0.05
            else:
                refresh_delay = 1/3
            self.screen_update(solution_matrix)
            time.sleep(refresh_delay)
            
    #Create function to update the screen:
    def screen_update(self, matrix):
        """Method that updates the current screen/window with the matrix in argument\n

        Args:\n
            matrix (list): 2D array of the game\n
        """
        self.clock.tick(60)
            
        x_position = -53
        y_position = -53
        
        for line in range(len(matrix)):
            y_position+=53
            for element in range(len(matrix[line])):
                x_position+=53
                if(matrix[line][element].isnumeric()):
                    #if it's a ghost
                    if(int(matrix[line][element])>=2):
                        self.screen.blit(self.ressources.get('ghost'), [x_position, y_position])
                    else:
                        #if it's a number but not a ghost
                        self.screen.blit(self.ressources.get(matrix[line][element]), [x_position, y_position])
                else:
                    #if it's a letter.
                    self.screen.blit(self.ressources.get(matrix[line][element]), [x_position, y_position])
                
            x_position = -53
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()
