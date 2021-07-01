import copy
import time
import abc
import random


class Game(object):
    """A connect four game."""

    def __init__(self, grid):
        """Instances differ by their board."""
        self.grid = copy.deepcopy(grid)  # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            for mark in row:
                print(mark, end='')
            print()
        print()

    def possible_moves(self):
        """Return a list of possible moves given the current board."""
        # YOU FILL THIS IN
        moves = []
        for i in range(8):
            if(self.grid[0][i]=='-'):
                moves.append(i)
        return moves

    def neighbor(self, col, color):
        """Return a Game instance like this one but with a move made into the specified column."""
        # YOU FILL THIS IN
        Grid2 = copy.deepcopy(self.grid)
        if Grid2[7][col] == '-':
            Grid2[7][col] = color
            return Game(Grid2)
        for i in range(8):
            if Grid2[i][col]=="R" or Grid2[i][col]=="B":
                Grid2[i-1][col] = color
                break

        return Game(Grid2)

    def chipCountToUtility(self, color, count):
        if count == 3:
            return 690000
        elif count == 2:
            return 69000
        else:
            return 6900


    def utility(self):
        """Return the minimax utility value of this game"""
        # YOU FILL THIS IN
        utility = 0
        for col in range(8):
            redCount = 0
            blackCount = 0
            for row in range(8):
                if self.grid[row][col] == 'R':
                    blackCount = 0
                    redCount += 1
                elif self.grid[row][col] == 'B':
                    redCount = 0
                    blackCount += 1
                else:
                    if redCount == 4:
                        return float('inf')
                    utility += self.chipCountToUtility('R', redCount)
                    utility -= self.chipCountToUtility('B', blackCount)

        # Horizontal
        for row in range(8):
            if redCount == 4:
                return float('inf')
            utility += self.chipCountToUtility('R', redCount)
            utility -= self.chipCountToUtility('B', blackCount)
            redCount = 0
            blackCount = 0
            for col in range(8):
                if self.grid[row][col] == 'R':
                    blackCount = 0
                    redCount += 1
                elif self.grid[row][col] == 'B':
                    redCount = 0
                    blackCount += 1
                else:
                    if redCount == 4:
                        return float('inf')
                    utility += self.chipCountToUtility('R', redCount)
                    utility -= self.chipCountToUtility('B', blackCount)
        return utility




    def winning_state(self):
        """Returns float("inf") if Red wins; float("-inf") if Black wins;
           0 if board full; None if not full and no winner"""
        # YOU FILL THIS IN
        # Vertical
        for col in range(8):
            redCount = 0
            blackCount = 0
            for row in range(8):
                if self.grid[row][col] == 'R':
                    if blackCount:
                        blackCount = 0
                    redCount += 1
                    if redCount == 4:
                        return float('inf')
                elif self.grid[row][col] == 'B':
                    if redCount:
                        redCount = 0
                    blackCount += 1
                    if blackCount == 4:
                        return float('-inf')
        # Horizontal
        for row in range(8):
            redCount = 0
            blackCount = 0
            for col in range(8):
                if self.grid[row][col] == 'R':
                    if blackCount:
                        blackCount = 0
                    redCount += 1
                    if redCount == 4:
                        return float('inf')
                elif self.grid[row][col] == 'B':
                    if redCount:
                        redCount = 0
                    blackCount += 1
                    if blackCount == 4:
                        return float('-inf')
                else:
                    redCount = 0
                    blackCount = 0

        # NEGATIVE SLOPE DIAGONALS
        # top half
        for colStartingPosition in range(8):
            row = 0
            redCount = 0
            blackCount = 0
            for col in range(colStartingPosition, 8):
                if self.grid[row][col] == 'R':
                    if blackCount:
                        blackCount=0
                    redCount += 1
                    if redCount == 4:
                        return float('inf')
                elif self.grid[row][col] == 'B':
                    if redCount:
                        redCount = 0
                    blackCount += 1
                    if blackCount == 4:
                        return float('-inf')
                else:
                    redCount = 0
                    blackCount = 0
                row+=1

        # bottom half
        for colStartingPosition in range(6,-1,-1):
            row = 7
            redCount = 0
            blackCount = 0
            for col in range(colStartingPosition, -1,-1):
                if self.grid[row][col] == 'R':
                    if blackCount:
                        blackCount = 0
                    redCount += 1
                    if redCount == 4:
                        return float('inf')
                elif self.grid[row][col] == 'B':
                    if redCount:
                        redCount = 0
                    blackCount += 1
                    if blackCount == 4:
                        return float('-inf')
                else:
                    redCount = 0
                    blackCount = 0
                row -= 1

        # POSITIVE SLOPE DIAGONALS
        # top half
        for colStartingPosition in range(6,-1,-1):
            row = 0
            redCount = 0
            blackCount = 0
            for col in range(colStartingPosition, -1,-1):
                if self.grid[row][col] == 'R':
                    if blackCount:
                        blackCount=0
                    redCount += 1
                    if redCount == 4:
                        return float('inf')
                elif self.grid[row][col] == 'B':
                    if redCount:
                        redCount = 0
                    blackCount += 1
                    if blackCount == 4:
                        return float('-inf')
                else:
                    redCount = 0
                    blackCount = 0
                row+=1
        # bottom half
        for colStartingPosition in range(8):
            row = 7
            redCount = 0
            blackCount = 0
            for col in range(colStartingPosition,8):
                if self.grid[row][col] == 'R':
                    if blackCount:
                        blackCount = 0
                    redCount += 1
                    if redCount == 4:
                        return float('inf')
                elif self.grid[row][col] == 'B':
                    if redCount:
                        redCount = 0
                    blackCount += 1
                    if blackCount == 4:
                        return float('-inf')
                else:
                    redCount = 0
                    blackCount = 0
                row -= 1
        if '-' not in self.grid[0]:
            return 0
        return None


class Agent(object):
    """Abstract class, extended by classes RandomAgent, FirstMoveAgent, MinimaxAgent.
    Do not make an instance of this class."""

    def __init__(self, color):
        """Agents use either RED or BLACK chips."""
        self.color = color

    @abc.abstractmethod
    def move(self, game):
        """Abstract. Must be implemented by a class that extends Agent."""
        pass


class RandomAgent(Agent):
    """Naive agent -- always performs a random move"""

    def move(self, game):
        """Returns a random move"""
        # YOU FILL THIS IN
        moves = game.possible_moves()
        return random.choice(moves)

class FirstMoveAgent(Agent):
    """Naive agent -- always performs the first move"""
    def move(self, game):
        """Returns the first possible move"""
        # YOU FILL THIS IN
        moves = game.possible_moves()
        return moves[0]

class MinimaxAgent(Agent):
    """Smart agent -- uses minimax to determine the best move"""
    def minimax(self, game, depth,maxplayer):
        if game.winning_state() or depth == 0:
            return [game.utility(), None]
        bestMove = [None, None]
        if maxplayer:
            bestMove[0] = float("-inf")
            for move in game.possible_moves():
                eval = self.minimax(game.neighbor(move, 'R'), depth-1,False)[0]
                if bestMove[0] < eval:
                    bestMove[0] = eval
                    bestMove[1] = move
            return bestMove
        else:
            bestMove[0] = float("inf")
            for move in game.possible_moves():
                eval = self.minimax(game.neighbor(move, 'B'), depth - 1,True)[0]
                if bestMove[0] > eval:
                    bestMove[0] = eval
                    bestMove[1] = move
            return bestMove

    def move(self, game):
        """Returns the best move using minimax"""
        # YOU FILL THIS IN
        bestMove = self.minimax(game, 3, True)
        return bestMove[1]

def tournament(simulations=50):
    """Simulate connect four games, of a minimax agent playing
    against a random agent"""

    redwin, blackwin, tie = 0,0,0
    for i in range(simulations):

        game = single_game(io=False)

        print(i, end=" ")
        if game.winning_state() == float("inf"):
            redwin += 1
        elif game.winning_state() == float("-inf"):
            blackwin += 1
        elif game.winning_state() == 0:
            tie += 1

    print("Red %d (%.0f%%) Black %d (%.0f%%) Tie %d" % (redwin,redwin/simulations*100,blackwin,blackwin/simulations*100,tie))

    return redwin/simulations


def single_game(io=True):
    """Create a game and have two agents play it."""

    game = Game([['-' for i in range(8)] for j in range(8)])   # 8x8 empty board
    if io:
        game.display()

    maxplayer = MinimaxAgent('R')
    minplayer = RandomAgent('B')

    while True:

        m = maxplayer.move(game)
        game = game.neighbor(m, maxplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

        m = minplayer.move(game)
        game = game.neighbor(m, minplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

    if game.winning_state() == float("inf"):
        print("RED WINS!")
    elif game.winning_state() == float("-inf"):
        print("BLACK WINS!")
    elif game.winning_state() == 0:
        print("TIE!")

    return game


if __name__ == '__main__':
    # single_game(io=True)
    tournament(simulations=50)