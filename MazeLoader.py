import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "uwu"

class MazeLoader():
    """
    Class to load and use the map.\n
    """
    def __init__(self):
        """
        Constructor of the class MazeLoader.\n
        """
        self.__matrix = None

    def load_maze(self, filepath):
        """Method to load the maze and set the attribute matrix.\n

        Args:\n
            filepath (str): the path to the file that contains the matrix.\n

        Returns:\n
            list: the matrix in the file in a 2D array (list).\n
        """
        #create a matrix for the game
        game_matrix = []
        #load the file
        map_file = open(filepath).read()
        #create a 1D matrix from the map
        matrix = map_file.split("\n")
        #remove the last line if its empty
        if(matrix[len(matrix)-1] == ""):
            matrix.pop(len(matrix)-1)
        #convert it into a 2D array
        for string in range(len(matrix)):
            line_matrix = []
            for letter in range(len(matrix[string])):
                #remove the whitespaces
                if(matrix[string][letter] != " "):
                    #add each letter in the line
                    line_matrix.append(matrix[string][letter])
            #add the line to the game_matrix
            game_matrix.append(line_matrix)
        
        self.matrix=game_matrix 

        return self.matrix
    
    @property
    def matrix(self):
        """Getter of self.__matrix\n

        Returns:\n
            list: list: the matrix in the file in a 2D array (list).\n
        """
        return self.__matrix

    @matrix.setter
    def matrix(self, matrix):
        """Setter of self.__matrix\n

        Args:\n
            matrix (list): 2D array representing the map\n
        """
        self.__matrix = matrix
