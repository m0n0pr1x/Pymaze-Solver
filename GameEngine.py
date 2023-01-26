import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "uwu"
import pygame
from Maze import Maze
from MazeLoader import MazeLoader
from MazeSolver import MazeSolver
from MazeGUI import MazeGUI
from copy import deepcopy
from time import sleep

class GameEngine():
    """
    Class that represents the GameEngine. It will 'connect' everything together.\n
    """
    def __init__(self):
        self.__Maze = None
        self.__playermaze = None
        self.__MazeLoader = None
        self.__MazeSolver = None
        self.__MazeGUI = None
        self.__player_coords = []
        self.__player_key = None
        self.__sounds = None

    def init_game(self, maze_instance, mazeloader_instance, mazesolver_instance):
        """
        Method that will initialize the game by initializing all the needed classes.\n
        with the parser in main.py init_game will be called with the argument matrix_path as the path of the file\n
        """
        #Initialize all the classes
        self.Maze = maze_instance
        self.MazeLoader = mazeloader_instance
        self.MazeSolver = mazesolver_instance
        self.MazeSolver.solving()
        self.playermaze = deepcopy(mazeloader_instance.matrix)

        self.MazeGUI = MazeGUI()
        self.MazeGUI.matrix = self.playermaze
        self.MazeGUI.load_ressources()
        self.MazeGUI.new_GUI()
        self.player_coords = self.Maze.co_start
        pygame.mixer.init()
        self.sounds ={
                "ghost_sound":pygame.mixer.Sound("sounds/ghost_sound.mp3"),
                "door_sound":pygame.mixer.Sound("sounds/door_sound.mp3"),
                "finish_sound":pygame.mixer.Sound("sounds/finish_sound.mp3"),
                "restart_sound":pygame.mixer.Sound("sounds/restart_sound.mp3"),
                "door-locked_sound":pygame.mixer.Sound("sounds/door-locked_sound.mp3"),
                "key_sound":pygame.mixer.Sound("sounds/key_sound.mp3")
        }
        #MazeGUI is initialized. Probably do a while(True) loop or something like in "Maze_GUI_test.py"
        #END OF THE GAME

    #Could add more methods to get more features and more flexibility.

    def check_win(self):
        if self.playermaze[self.Maze.co_end[0]][self.Maze.co_end[1]] == 's':
            self.sound_player(self.sounds["finish_sound"])
            return 1
        return 0


    def play(self):
        ticker = 0
        while True:
            if self.check_win():
                break
            self.MazeGUI.screen_update(self.playermaze)
            keys = pygame.key.get_pressed()
            if ticker > 0:
                ticker-=1
            if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and ticker == 0:
                print(f"You moved left {self.player_coords}")
                ticker = 10
                self.move_left()
            if ( keys[pygame.K_RIGHT] or keys[pygame.K_d] ) and ticker == 0:
                print(f"You moved right {self.player_coords}")
                ticker = 10
                self.move_right()
            if ( keys[pygame.K_UP] or keys[pygame.K_z] ) and ticker == 0:
                print(f"You moved up {self.player_coords}")
                ticker = 10
                self.move_up()
            if ( keys[pygame.K_DOWN] or keys[pygame.K_s] ) and ticker == 0:
                print(f"You moved down {self.player_coords}")
                ticker = 10
                self.move_down()
        self.sound_player(self.sounds["finish_sound"])
        sleep(2)

    @property
    def Maze(self):
        """Getter method of Maze attribute.\n

        Returns:\n
            Maze: Instance of Maze\n
        """
        return self.__Maze

    @property
    def playermaze(self):
        """Getter method of playermaze attribute.\n

        Returns:\n
            Maze: Instance of Maze\n
        """
        return self.__playermaze

    @property
    def MazeLoader(self):
        """Getter method of MazeLoader attribute.\n

        Returns:\n
            MazeLoader: Instance of MazeLoader\n
        """
        return self.__MazeLoader

    @property
    def MazeSolver(self):
        """Getter method of MazeSolver attribute.\n

        Returns:\n
            MazeSolver: Instance of MazeSolver\n
        """
        return self.__MazeSolver

    @property
    def MazeGUI(self):
        """Getter method of MazeGUI attribute.\n

        Returns:\n
            MazeGUI: Instance of MazeGUI\n
        """
        return self.__MazeGUI

    @property
    def player_coords(self):
        """Getter method of player_coords attribute.\n

        Returns:\n
            list: Instance of player_coords\n
        """
        return self.__player_coords

    @property
    def player_key(self):
        """Getter of player_key\n

        Returns:\n
            str: key possesed by the player\n
        """
        return self.__player_key

    @Maze.setter
    def Maze(self, Maze):
        """Setter procedure of Maze attribute.\n
        """
        self.__Maze = Maze

    @MazeLoader.setter
    def MazeLoader(self, MazeLoader):
        """Setter procedure of MazeLoader attribute.\n
        """
        self.__MazeLoader = MazeLoader

    @playermaze.setter
    def playermaze(self, playermaze):
        """Setter procedure of MazeLoader attribute.\n
        """
        self.__playermaze = playermaze

    @MazeSolver.setter
    def MazeSolver(self, MazeSolver):
        """Setter procedure of MazeSolver attribute.\n
        """
        self.__MazeSolver = MazeSolver

    @MazeGUI.setter
    def MazeGUI(self, MazeGUI):
        """Setter procedure of MazeGUI attribute.\n
        """
        self.__MazeGUI = MazeGUI

    @player_coords.setter
    def player_coords(self, coords):
        """Setter method of player_coords attribute.\n
        """
        self.__player_coords = coords

    @player_key.setter
    def player_key(self, key):
        """Setter to set the key taken by player\n

        Args:\n
            key (str): key that the player took\n
        """
        self.__player_key = key

    def is_wall(self, x, y):
        """
        Method that returns true if the position enterred is a wall\n
        """

        if(self.playermaze[x][y] == "1"):
            return 1

        return 0

    #Method to verify if ghost
    def is_ghost(self, x, y):
        """
        Method that returns true if the position enterred is a ghost block\n
        """
        coords = self.player_coords
        if(self.playermaze[x][y] in ["-1", "ghost"]):
            print(f"start coords {self.Maze.co_start}")
            self.playermaze[coords[0]][coords[1]] = "0"
            coords = [self.Maze.co_start[0], self.Maze.co_start[1]]
            self.playermaze[coords[0]][coords[1]] = "s"
            self.player_coords = coords
            self.playermaze = deepcopy(self.Maze.maze)
            self.player_key = None
            self.sound_player(self.sounds["ghost_sound"])
            return 1

        return 0

    def sound_player(self,sound):
        """
        Sound player
        """
        pygame.mixer.Sound.play(sound)
        pygame.mixer.music.stop()

    #Method to verify if the player can open the door
    def is_door(self, x, y):
        """
        Method that returns true if the position enterred is a door\n
        """

        if(self.playermaze[x][y] in ["i", "c", "g", "b"]):
            return 1

        return 0

    def is_key(self, x, y):
        """Method that will return if the current position is at a key.\n

        Args:\n
            x (int): position in x\n
            y (int): position in y\n

        Returns:\n
            int: 1 if is key 0 if is not key\n
        """
        if(self.playermaze[x][y] in ["h", "d", "f", "a"]):
            return 1
        return 0

    def take_key(self, x, y):
        if(self.player_key == None):
            self.player_key = self.playermaze[x][y]
            print(f"key owned by player: {self.player_key}")
            self.sound_player(self.sounds["key_sound"])
            return 1
        else:
            print("You already have a key!")
            return 0

    def door_open(self, x, y):
        """
        Method that returns true if the position enterred is a door\n
        """
        if(self.playermaze[x][y] == "i" and  "h" == self.player_key):
            self.sound_player(self.sounds["door_sound"])
            self.player_key = None
            return 1
        if(self.playermaze[x][y] == "c" and  "d" == self.player_key):
            self.sound_player(self.sounds["door_sound"])
            self.player_key = None
            return 1
        if(self.playermaze[x][y] == "g" and  "f" == self.player_key):
            self.sound_player(self.sounds["door_sound"])
            self.player_key = None
            return 1
        if(self.playermaze[x][y] == "b" and  "a" == self.player_key):
            self.sound_player(self.sounds["door_sound"])
            self.player_key = None
            return 1

        return 0

    #Methods to move the player.

    def move_up(self):
        """
        Method to move the player up\n

        Returns:\n
            int: If the player moved\n
        """
        coords = self.player_coords
        print(coords)

        if(self.is_key(coords[0]-1, coords[1])):
            if(self.take_key(coords[0]-1, coords[1]) == 0):
                return 0

        if(self.is_door(coords[0]-1, coords[1])):
            if(self.door_open(coords[0]-1, coords[1])):
                self.playermaze[coords[0]][coords[1]] = "0"
                coords = [coords[0]-1, coords[1]]
                self.playermaze[coords[0]][coords[1]] = "s"
                self.player_coords = coords
                return 1
            else:
                self.sound_player(self.sounds["door-locked_sound"])


        if(not self.is_wall(coords[0]-1, coords[1]) and not self.is_ghost(coords[0]-1, coords[1]) and not self.is_door(coords[0]-1, coords[1])):
            self.playermaze[coords[0]][coords[1]] = "0"
            coords = [coords[0]-1, coords[1]]
            self.playermaze[coords[0]][coords[1]] = "s"
            self.player_coords = coords
            print("new coords",coords)
            return 1
        print("Not allowed here")

        return 0

    def move_down(self):
        """
        Method to move the player down\n

        Returns:\n
            int: If the player moved\n
        """
        coords = self.player_coords
        print(coords)

        if(self.is_key(coords[0]+1, coords[1])):
            if(self.take_key(coords[0]+1, coords[1]) == 0):
                return 0

        if(self.is_door(coords[0]+1, coords[1])):
            if(self.door_open(coords[0]+1, coords[1])):
                self.playermaze[coords[0]][coords[1]] = "0"
                coords = [coords[0]+1, coords[1]]
                self.playermaze[coords[0]][coords[1]] = "s"
                self.player_coords = coords
                return 1
            else:
                self.sound_player(self.sounds["door-locked_sound"])

        if(not self.is_wall(coords[0]+1, coords[1]) and not self.is_ghost(coords[0]+1, coords[1]) and not self.is_door(coords[0]+1, coords[1])):
            self.playermaze[coords[0]][coords[1]] = "0"
            coords = [coords[0]+1, coords[1]]
            self.playermaze[coords[0]][coords[1]] = "s"
            self.player_coords = coords
            return 1
        print("Not allowed here")

        return 0

    def move_right(self):
        """
        Method to move the player right\n

        Returns:\n
            int: If the player moved\n
        """
        coords = self.player_coords
        print(coords)

        if(self.is_key(coords[0], coords[1]+1)):
            if(self.take_key(coords[0], coords[1]+1) == 0):
                return 0

        if(self.is_door(coords[0], coords[1]+1)):
            if(self.door_open(coords[0], coords[1]+1)):
                self.playermaze[coords[0]][coords[1]] = "0"
                coords = [coords[0], coords[1]+1]
                self.playermaze[coords[0]][coords[1]] = "s"
                self.player_coords = coords
                return 1
            else:
                self.sound_player(self.sounds["door-locked_sound"])

        if(not self.is_wall(coords[0], coords[1]+1) and not self.is_ghost(coords[0], coords[1]+1) and not self.is_door(coords[0], coords[1]+1)):
            self.playermaze[coords[0]][coords[1]] = "0"
            coords = [coords[0], coords[1]+1]
            self.playermaze[coords[0]][coords[1]] = "s"
            self.player_coords = coords
            return 1

        print("Not allowed here")

        return 0

    def move_left(self):
        """
        Method to move the player left\n

        Returns:\n
            int: If the player moved\n
        """
        coords = self.player_coords
        print(coords)

        if(self.is_key(coords[0], coords[1]-1)):
            if(self.take_key(coords[0], coords[1]-1) == 0):
                return 0

        if(self.is_door(coords[0], coords[1]-1)):
            if(self.door_open(coords[0], coords[1]-1)):
                self.playermaze[coords[0]][coords[1]] = "0"
                coords = [coords[0], coords[1]-1]
                self.playermaze[coords[0]][coords[1]] = "s"
                self.player_coords = coords
                return 1
            else:
                self.sound_player(self.sounds["door-locked_sound"])

        if(not self.is_wall(coords[0], coords[1]-1) and not self.is_ghost(coords[0], coords[1]-1) and not self.is_door(coords[0], coords[1]-1)):
            self.playermaze[coords[0]][coords[1]] = "0"
            coords = [coords[0], coords[1]-1]
            self.playermaze[coords[0]][coords[1]] = "s"
            self.player_coords = coords
            return 1
        print("Not allowed here")

        return 0
