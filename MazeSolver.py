import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "uwu"
import Maze
from time import sleep

class MazeSolver:
    def __init__(self,maze):
        self._maze = maze
        self._plus_courte_distance = 9999
        self._solutions = []
        self._solution_finale = []
        self._doors_available = maze.doors.copy()
        self._keys_available = maze.keys.copy()


    @property
    def maze(self):
        return self._maze

    @maze.setter
    def maze(self, maze):
        self._maze = maze

    @property
    def plus_courte_distance(self):
        return self._plus_courte_distance

    @plus_courte_distance.setter
    def plus_courte_distance(self, plus_courte_distance):
        self._plus_courte_distance = plus_courte_distance;

    @property
    def solutions(self):
        return self._solutions

    @solutions.setter
    def solutions(self, solutions):
        self._solutions = solutions;

    @property
    def solution_finale(self):
        return self._solution_finale

    @solution_finale.setter
    def solution_finale(self, solution_finale):
        self._solution_finale = solution_finale;

    @property
    def doors_available(self):
        return self._doors_available

    @doors_available.setter
    def doors_available(self, doors_available):
        self._doors_available = doors_available;

    @property
    def keys_available(self):
        return self._keys_available

    @keys_available.setter
    def keys_available(self, keys_available):
        self._keys_available = keys_available;


    def get_co_of_the_key(self, key):
        """
        Get the coordonates of the key given in paramater\n
        """
        for indice_ligne in range(len(self.maze.maze)):
            for indice_pos in range(len(self.maze.maze[indice_ligne])):
                if self.maze.maze[indice_ligne][indice_pos] == key:
                    return (indice_ligne,indice_pos)


    def key_finding(self, i, j, sol, path, distance=0):
        """
        AVOID TO USE THIS FUNCTION DIRECTLY\n

        Start from i and j and search for a key, then give the path to this key\n
        The keys are checked from key_available\n
        """
        if i >= self.maze.length[0] or j >= self.maze.length[1] or i < 0 or j < 0 or self.maze[i][j] in ['1','-1']+self.doors_available or sol[i][j] == '1':
            return;

        if self.maze[i][j] in self.keys_available:
            if distance < self.plus_courte_distance:

                self.plus_courte_distance = distance
                copy_sol = [ligne[:] for ligne in sol]
                copy_path = [p for p in path]
                self.solutions.append((copy_path,self.maze[i][j]))
                return path


        path.append((i,j))
        sol[i][j] = '1'

        self.key_finding(i+1, j,   sol, path, distance+1)
        self.key_finding(i-1, j,   sol, path, distance+1)
        self.key_finding(i,   j+1, sol, path, distance+1)
        self.key_finding(i,   j-1, sol, path, distance+1)

        path.pop()
        sol[i][j] = '0'
        return;


    def path_finding(self, i, j, sol, path, distance=0):
        """
        AVOID TO USE THIS FUNCTION DIRECTLY\n
        start from i and j and search for the end\n
        """
        if i >= self.maze.length[0] or j >= self.maze.length[1] or i < 0 or j < 0 or self.maze[i][j] in ['1','-1'] or sol[i][j] == '1':
            return;

        if (i,j) == self.maze.co_end:
            if distance < self.plus_courte_distance:
                self.plus_courte_distance = distance

                copy_sol = [ligne[:] for ligne in sol]
                copy_path = [p for p in path]
                self.solutions.append(copy_path)
                return sol



        path.append((i,j))
        sol[i][j] = '1'

        self.path_finding(i+1,j, sol, path, distance+1)# vas en bas
        self.path_finding(i-1,j, sol, path, distance+1)# vas en haut
        self.path_finding(i,j+1, sol, path, distance+1)# vas a droite
        self.path_finding(i,j-1, sol, path, distance+1)# vas a gauche

        sol[i][j] = '0'
        path.pop()
        return;

    def print_solution(self):
        maze_vide = self.maze.generateur_maze_vide(self.maze.maze)
        prev = (-1,-1)
        for tupel in self.solution_finale:
            if prev == tupel:
                maze_vide[tupel[0]][tupel[1]] = '0'
                self.maze.affichage(maze_vide)
                sleep(0.3)
            else:
                prev = tupel
                maze_vide[tupel[0]][tupel[1]] = '1'
                self.maze.affichage(maze_vide)
                sleep(0.3)


    def solving(self):
        """
        Use this function to solve the maze\n
        """
        try:
            if self.doors_available == []: # If there is no door
                start = self.maze.co_start
                maze_vide = self.maze.generateur_maze_vide(self.maze.maze)
                self.plus_courte_distance = 9999
                self.path_finding(start[0],start[1], maze_vide, [], 0)
                self.solution_finale.extend(self.solutions[-1]) # On met le derneir chemin performaant trouvée
                self.solution_finale.extend([self.maze.co_end])
                return self.solution_finale



            self._solution_finale = [self.maze.co_start]
            self.solutions = []
            self.plus_courte_distance = 9999
            start = self.maze.co_start
            while self.doors_available != []:
                self.solutions = [] # on clear les solutions
                self.plus_courte_distance = 9999 # on remet la distance plus longue
                maze_vide = self.maze.generateur_maze_vide(self.maze.maze)


                self.key_finding(start[0],start[1], maze_vide, [], 0) # on lance le key_finding
                last_solution = self.solutions[-1]
                last_solution_path = last_solution[0]
                last_solution_key = last_solution[1]
                last_solution_path.append(self.get_co_of_the_key(last_solution_key))

                self.doors_available.remove({"f":"g","d":"c","a":"b","h":"i"}[last_solution_key]) # on supprime la porte avec la clé quon a trouvé

                self.keys_available.remove(last_solution_key)# on supprime aussi la clé pour ne plus la chercher

                self.solution_finale.extend(last_solution_path[1:]) # on ajoute le chemin à la solution finale

                start = (last_solution_path[-1])

            self.solutions = []
            self.plus_courte_distance = 9999
            start = self.solution_finale[-1] # on place le start au dernier tuple
            maze_vide = self.maze.generateur_maze_vide(self.maze.maze)
            self.path_finding(start[0],start[1], maze_vide, [])
            self.solution_finale.extend(self.solutions[-1][1:])
            self.solution_finale.extend([self.maze.co_end])
        except IndexError:
            print("Pas de solutions")
            return []

        return self.solution_finale
