import copy
import time
from collections import deque


class Puzzle:
    """A sliding-block puzzle."""
  
    def __init__(self, grid):
        """Instances differ by their number configurations."""
        self.grid = copy.deepcopy(grid) # No aliasing!
    
    def display(self):
        """Print the puzzle."""
        for row in self.grid:
            for number in row:
                print(number, end="")
            print()
        print()

    def moves(self):
        """Return a list of possible moves given the current configuration."""
        # YOU FILL THIS IN
        length = len(self.grid)
        move = []
        for row in range(length):
            for number in range(len(self.grid[row])):
                if self.grid[row][number] == " ":
                    r,c = row, number
                    break
        if(r-1 < length and r-1 >= 0):
            move.append("N")
        if (r+1 < length):
            move.append("S")
        if (c+1 < len(self.grid[r])):
            move.append("E")
        if (c-1 < len(self.grid[r]) and c-1 >= 0):
            move.append("W")
        return move
    
    def neighbor(self, move):
        """Return a Puzzle instance like this one but with one move made."""
        # YOU FILL THIS IN
        for row in range(len(self.grid)):
            for number in range(len(self.grid[row])):
                if self.grid[row][number] == " ":
                    r, c = row, number
                    break
        copied = copy.deepcopy(self.grid)
        if (move == "N"):
            temp = copied[r-1][c]
            copied[r-1][c] = " "
            copied[r][c] = temp

        if (move == "S"):
            temp = copied[r + 1][c]
            copied[r + 1][c] = " "
            copied[r][c] = temp

        if (move == "W"):
            temp = copied[r][c-1]
            copied[r][c-1] = " "
            copied[r][c] = temp

        if (move == "E"):
            temp = copied[r][c+1]
            copied[r][c+1] = " "
            copied[r][c] = temp

        return Puzzle(copied)

    def h(self, goal):
        """Compute the distance heuristic from this instance to the goal."""
        # YOU FILL THIS IN
        misplaced = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (self.grid[row][col] != goal.grid[row][col]):
                    misplaced += 1
        return misplaced


class Agent:
    """Knows how to solve a sliding-block puzzle with A* search."""
    
    def astar(self, puzzle, goal):
        """Return a list of moves to get the puzzle to match the goal."""
        # YOU FILL THIS IN
        frontier = []
        finished = []
        frontier.append((puzzle.h(goal), puzzle, []))
        while(frontier):
            frontier.sort(key=lambda i: i[0])
            parent = frontier.pop(0)
            ph, ppuzzle, ppath = parent
            if (ppuzzle.grid == goal.grid):
                return ppath
            finished.append(ppuzzle.grid)
            move = ppuzzle.moves()

            for x in move:
                neighbor = ppuzzle.neighbor(x)
                if neighbor.grid in finished:
                    continue
                    
                ch = neighbor.h(goal)
                child = (ch + len(ppath), neighbor, ppath + [x])

                for n in range(len(frontier)):
                    if child[1].grid in frontier[n]:
                        if(child[0] < frontier[n][0]):
                            frontier[n] = child
                            break
                else:
                    frontier.append(child)

        return ppath

def main():
    """Create a puzzle, solve it with A*, and console-animate."""
    
    puzzle = Puzzle([[1, 2, 5],
                     [4, 8, 7],
                     [3, 6,' ']])
    puzzle.display()
    
    agent = Agent()
    goal = Puzzle([[' ',1,2],
                   [3, 4, 5],
                   [6, 7, 8]])
    path = agent.astar(puzzle, goal)
    
    while path:
        move = path.pop(0)
        puzzle = puzzle.neighbor(move)
        time.sleep(1)
        puzzle.display()


if __name__ == '__main__':
    main()
