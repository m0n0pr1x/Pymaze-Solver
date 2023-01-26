class Maze:
    """
    What does this class do? please give it a description !!!\n
    """
    def __init__(self):
        self._maze = [[]] 
        self._ghosts = 0
        self._doors = 0
        self._ghost_coords = []
        self._length = 0
        self._co_start = (0,0)
        self._co_end = (0,0)
        self._keys = 0
        self._doors = 0
        self._empty_maze = []

    @property
    def maze(self):
        return self._maze
    
    @maze.setter
    def maze(self, new_maze):
        raise Exception("You are not allowed to redefine the maze")

    @property
    def doors(self):
        return self._doors
    
    @doors.setter
    def doors(self, doors):
        self._doors = doors;

    @property
    def ghosts(self):
        return self._ghosts
    
    @ghosts.setter
    def ghosts(self, ghosts):
        self._ghosts = ghosts;

    @property
    def ghost_coords(self):
        return self._ghost_coords
    
    @ghost_coords.setter
    def ghost_coords(self, ghost_coords):
        self._ghost_coords = ghost_coords;

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, length):
        self._length = length;

    @property
    def co_start(self):
        return self._co_start
    
    @co_start.setter
    def co_start(self, co_start):
        self._co_start = co_start;

    @property
    def co_end(self):
        return self._co_end
    
    @co_end.setter
    def co_end(self, co_end):
        self._co_end = co_end;

    @property
    def keys(self):
        return self._keys
    
    @keys.setter
    def keys(self, keys):
        self._keys = keys;

    @property
    def empty_maze(self):
        return self._empty_maze
    
    @empty_maze.setter
    def empty_maze(self, empty_maze):
        self._empty_maze = empty_maze;


    def __getitem__(self,x):
        if x > self.length[0] or x > self.length[1]:
            raise Exception(f"The element at index {x} you try to get is out of bound")
        
        return self.maze[x]

    def __str__(self):
        self.affichage(self.maze)
        return ""


    def initializer(self, matrice):
        """
        Initialize the Maze class with a matrix, get all the ghost, find the start the end, put the range of the ghost,etc.\n
        """
        self._maze = matrice
        self.ghosts = 0
        self.doors = 0
        self.ghost_coords = []
        self.length = (len(self.maze),len(self.maze[0]))
        if self.length == 0:
            raise Exception("Empty Maze")

        self.co_start = self.find_end_start(self.maze)[0]
        self.co_end = self.find_end_start(self.maze)[1]

        if self.co_start == self.co_end:
            raise Exception("Start position and end position at the same place")


        self.keys = self.get_keys(self.maze)
        self.doors = self.get_doors(self.maze)
        if len(self.doors) != len(self.keys):
            raise Exception("Not the same amount of keys and doors")

        self.empty_maze = self.generateur_maze_vide(self.maze)
        self.ghost_coords = self.solve_ghost_coords(self.maze)
        self.ghost_block()


    def find_end_start(self, maze:list)->list:
        """
        Take a maze and returns the coordonates of the start and the end\n

        Examples:\n
            OUTPUT:\n
            [(0,0),(9,9)]\n
        """
        coordonate = []
        found_end = 0
        found_start = 0
        
        for ligne in range(len(maze)):
            for column in range(len(maze[ligne])):
                if found_start == 0:
                    if maze[ligne][column] == 's':
                        coordonate.append((ligne, column))
                        found_start = 1
                        continue
                
                if found_end == 0:
                    if maze[ligne][column] == 'e':
                        coordonate.append((ligne, column))
                        found_end = 1
                        continue
                
                if(found_start and found_end):
                    return coordonate
        
        if(not found_start or found_end):
            raise Exception("No end or start found")
            return []

    def get_keys(self, maze)->list:
        """
        Return a list of the keys available in the maze\n
        """
        keys_available = []
        for line in maze:
            for character in line:
                if character in ['f','d','a','h']:
                    keys_available.append(character)
        return keys_available

    def get_doors(self, maze)->list:
        """
        Return a list of the doors available in the maze\n
        """
        doors_available = []
        for line in maze:
            for character in line:
                if character in ['g','c','b','i']:
                    doors_available.append(character)
        return doors_available

    def generateur_maze_vide(self,maze):
        """
        Generate an empty maze, with the size of the maze\n
        """
        return [['0' for i in range(len(maze[0]))]for j in range(len(maze))]

    def affichage(self, maze):
        """
        Temporary function to print a maze to the console\n
        """
        print("----------------------------")
        for ligne in maze:
            for case in ligne:
                if case == '0':
                    print("_",end=" ")
                elif case == '1':
                    print("X",end=" ")
                elif case == '-1':
                    print("-",end=" ")
                else:
                    print(case,end=" ")
            print()
        print("-----------------------------")

    def solve_ghost_coords(self, matrice):
        """
        Return the list of coords of the ghosts\n
        """
        list_of_coords = []

        #for each line/sublist of the self.maze
        for line in range(len(matrice)):
            #for each element in the line/sublist
            for character in range(len(matrice[0])):
                #if the element is numeric
                if(matrice[line][character].isnumeric()):
                    #check if it is >= 2
                    if(int(matrice[line][character]) >= 2):
                        #add them to the tuple
                        current_tuple = (int(matrice[line][character]),character, line)
                        #and append it to the list of coordinates (list_of_coords)
                        list_of_coords.append(current_tuple)


        return list_of_coords


    def ghost_block(self):
        """This function is made to take the position of the of ghosts and place -1 on it range.\n

        Args:\n
            maze (maze): take any maze of maze\n

        Returns:\n
            maze: Return the maze update with the range of ghosts\n
        """
        ghost = self.ghost_coords
        if ghost == []:
            return

        for ghost_num in range(len(ghost)):
            name_ghost = ghost[ghost_num][0]
            coord_ghost_col = ghost[ghost_num][2]
            coord_ghost_line = ghost[ghost_num][1]

            through_wall_up = 0
            through_wall_down = 0
            through_wall_rigth =0
            through_wall_left = 0

            through_wall_diag_up_rigth = 0
            through_wall_diag_up_left = 0
            through_wall_diag_down_rigth = 0
            through_wall_diag_down_left = 0

            through_2wall_diag_up_left = 0
            through_2wall_diag_up_right = 0
            through_2wall_diag_down_left = 0
            through_2wall_diag_down_right = 0

            for ghost_ray in range(1,name_ghost):
                if(coord_ghost_line + ghost_ray <  len(self.maze[0]) and coord_ghost_col + ghost_ray < len(self.maze) and coord_ghost_col - ghost_ray > 0):
                    

                    #replace the path with a wall if it's a path in bottom right diagonal
                    if((self.maze[coord_ghost_col + ghost_ray][coord_ghost_line + ghost_ray]) == "1"):
                        through_wall_diag_down_rigth = 1

                    if(self.maze[coord_ghost_col + ghost_ray][coord_ghost_line] == "1" and self.maze[coord_ghost_col][coord_ghost_line + ghost_ray] == "1"):
                        through_2wall_diag_down_right = 1
                    
                    if((self.maze[coord_ghost_col + ghost_ray][coord_ghost_line + ghost_ray]) == "0" and through_wall_diag_down_rigth == 0 and through_2wall_diag_down_right == 0):
                        self.maze[coord_ghost_col + ghost_ray][coord_ghost_line + ghost_ray] = "-1"
                if((coord_ghost_line + ghost_ray <  len(self.maze[0]) and coord_ghost_col - ghost_ray > 0)):
                    #replace the path with a wall if it's a path in top right diagonal
                    if((self.maze[coord_ghost_col - ghost_ray][coord_ghost_line + ghost_ray]) == "1"):
                        through_wall_diag_up_rigth = 1

                    if(self.maze[coord_ghost_col - ghost_ray][coord_ghost_line] == "1" and self.maze[coord_ghost_col][coord_ghost_line + ghost_ray] == "1"):
                        through_2wall_diag_up_right = 1
                     
                    
                    if((self.maze[coord_ghost_col - ghost_ray][coord_ghost_line + ghost_ray]) == "0" and through_wall_diag_up_rigth == 0 and through_2wall_diag_up_right == 0):
                        self.maze[coord_ghost_col - ghost_ray][coord_ghost_line + ghost_ray] = "-1"


                if(coord_ghost_line - ghost_ray > 0 and coord_ghost_col - ghost_ray  > 0 and coord_ghost_col + ghost_ray < len(self.maze)):
                    
                    #replace the path with a wall if it's a path in bottom left diagonal
                    if((self.maze[coord_ghost_col + ghost_ray][coord_ghost_line - ghost_ray]) == "1"):
                        through_wall_diag_down_left = 1

                    if(self.maze[coord_ghost_col + ghost_ray][coord_ghost_line] == "1" and self.maze[coord_ghost_col][coord_ghost_line - ghost_ray] == "1"):
                        through_2wall_diag_down_left = 1
                    
                    if((self.maze[coord_ghost_col + ghost_ray][coord_ghost_line - ghost_ray]) == "0" and through_wall_diag_down_left == 0 and through_2wall_diag_down_left == 0):
                        self.maze[coord_ghost_col + ghost_ray][coord_ghost_line - ghost_ray] = "-1"
                if(coord_ghost_line - ghost_ray > 0 and coord_ghost_col - ghost_ray  > 0):
                    #replace the path with a wall if it's a path in top left diagonal
                    if((self.maze[coord_ghost_col - ghost_ray][coord_ghost_line - ghost_ray]) == "1"):
                        
                        through_wall_diag_up_left = 1

                    if(self.maze[coord_ghost_col - ghost_ray][coord_ghost_line] == "1" and self.maze[coord_ghost_col][coord_ghost_line - ghost_ray] == "1"):
                        through_2wall_diag_up_left = 1
                        
                    
                    if((self.maze[coord_ghost_col - ghost_ray][coord_ghost_line - ghost_ray]) == "0" and through_wall_diag_up_left == 0 and through_2wall_diag_up_left == 0):
                        self.maze[coord_ghost_col - ghost_ray][coord_ghost_line - ghost_ray] = "-1"

                if(coord_ghost_col + ghost_ray < len(self.maze)):

                    if((self.maze[coord_ghost_col + ghost_ray][coord_ghost_line]) == "1"):
                        through_wall_down = 1

                    #replace the path with a wall if it's a path underneath
                    if((self.maze[coord_ghost_col + ghost_ray][coord_ghost_line]) == "0" and through_wall_down == 0):
                        self.maze[coord_ghost_col + ghost_ray][coord_ghost_line] = "-1"


                if(coord_ghost_col - ghost_ray> 0):
                    if((self.maze[coord_ghost_col - ghost_ray][coord_ghost_line]) == "1"):
                        through_wall_up = 1

                    #replace the path with a wall if it's a path upneath
                    if((self.maze[coord_ghost_col - ghost_ray][coord_ghost_line]) == "0" and through_wall_up == 0):
                        self.maze[coord_ghost_col - ghost_ray][coord_ghost_line] = "-1"


                if(coord_ghost_line + ghost_ray < len(self.maze[0])):
                    if((self.maze[coord_ghost_col][coord_ghost_line + ghost_ray]) == "1"):
                        through_wall_rigth = 1

                    #replace the path with a wall if it's a path rigth
                    if((self.maze[coord_ghost_col][coord_ghost_line + ghost_ray]) == "0" and through_wall_rigth == 0):
                        self.maze[coord_ghost_col][coord_ghost_line + ghost_ray] = "-1"


                if(coord_ghost_line - ghost_ray > 0):
                    if((self.maze[coord_ghost_col][coord_ghost_line - ghost_ray]) == "1"):
                        through_wall_left = 1
                    #replace the path with a wall if it's a path left
                    if((self.maze[coord_ghost_col][coord_ghost_line - ghost_ray]) == "0" and through_wall_left == 0):
                        self.maze[coord_ghost_col][coord_ghost_line - ghost_ray] = "-1"
