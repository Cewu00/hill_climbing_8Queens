from random import randint

class ChessBoardLogic():
    def __init__(self, board_size=8): 
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.collisions = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.queen_positions = {} # (x : y)
        
        self.random_board()
        self.board_colisions_calculator()
        self.board_heuristics_calculator()
        
    def print_chessboard(self):
        print("Current state of the chessboard:")
        for red in self.board:
            print(red)
        print('\n')
    
    def print_collisions(self):
        print("Current state of the collisions:")
        for red in self.collisions:
            print(red)
        print('\n')
    
    def print_heruistics(self):
        print("Current state of the heuristics:")
        for red in self.heuristics:
            print(red)
        print('\n')
    
    def diagonal_queens(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if i == j:
                    self.board[j][i] = 1
                                   
    def random_board(self): # reset table
        random_positions = []
        for i in range(self.board_size):
            random_positions.append(randint(0, self.board_size - 1))
        
        for x, y in enumerate(random_positions):
            self.queen_positions[x] = y
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if random_positions[i] == j:
                    self.board[j][i] = 1
                else:
                    self.board[j][i] = 0    
        #print(random_positions)
        
    
    def square_collisions_calculator(self, x : int, y : int) -> int: 
        num = 0
        # u vertikali nece biti nista, ne mora da se provjerava
        
        horisontal_num = sum(self.board[y])
        if self.board[y][x] == 1:
            num += horisontal_num - 1
        else:
            num += horisontal_num
                    
        # broj kvadrata koji ce biti od kraljice do kraja table 
        nw_diag = min(y, x)
        ne_diag = min(y, self.board_size - x - 1)
        sw_diag = min(self.board_size - y - 1, x)
        se_diag = self.board_size - 1 - max(y, x)   
    
        diagonals = [nw_diag, ne_diag, sw_diag, se_diag]
        movments = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        
        for diagonal, movment in zip(diagonals, movments):
            for i in range(1, diagonal + 1): # ne provjerava sebe jer pocinje od 1
                x0 = (x + i*movment[0])
                y0 = (y + i*movment[1])
                if self.board[y0][x0] == 1: # mozda promjeni ovo u samo dodavanje broja koji je na diagonali... moguce neko marginalno ubrzanje
                    num += 1
        return num
    
    def board_colisions_calculator(self): 
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.collisions[i][j] = self.square_collisions_calculator(j, i) # x, y
                
    
    def board_heuristics_calculator(self):
        original_colisions = [] # pocetno stanje kraljica
        for x in range(self.board_size):
            y = self.queen_positions[x]
            # print(x, y)
            original_colisions.append(self.collisions[y][x])
        heur = sum(original_colisions)
        # print(original_colisions, heur)
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.queen_positions[i] == j:
                    self.heuristics[j][i] = (heur + (self.collisions[j][i] - original_colisions[i])*2)//2
                else:
                    self.heuristics[j][i] = (heur - 2 * original_colisions[i] + 2 * self.collisions[j][i])//2
    
    
    def get_min_heuristics(self): # ovo ako radi kako treba ne bi trebalo da pravi problem nakon sto popravim racunanje heuristike
        minimums = []
        overall_minimum = self.heuristics[0][0]
        for i in range(self.board_size):
            num1 = self.heuristics[0][i]
            minimum_col = [(0, num1)]
            if overall_minimum > num1:
                overall_minimum = num1  
            for j in range(self.board_size - 1): # TODO: FIX! ne appenduje (7, num) ili (0, num) provjeri... mislim da je ovo drugo
                num2 = self.heuristics[j+1][i]
                if num2 < num1:
                    minimum_col = []
                    minimum_col.append((j+1, num2)) # y, heuristics_value (x nam ne treba jer ce to biti redom izlistano u listi 'minimums' koja se pravi)
                    num1 = num2
                elif num1 == num2:
                    minimum_col.append((j+1, num2)) # y, heuristics_value
                if overall_minimum > num2:
                    overall_minimum = num2
            minimums.append(minimum_col)

        minimum_count = 0
        for i in range(len(minimums)):
            if minimums[i][0][1] > overall_minimum:
                minimums[i] = 0
            else:
                minimum_count += len(minimums[i])
        random_choice = randint(1, minimum_count)

        num = 1
        for i in range(len(minimums)):
            if minimums[i] != 0:
                for tp in minimums[i]:
                    if num == random_choice:
                        return (i, tp[0], tp[1]) # x, y, heuristic_value (returning a random heuristic value of all the lowest ones)
                    num += 1
        
    
    def hill_climbing(self):
        pass
    
    def set_custom_board_state(self, queen_positions : dict):
        if len(queen_positions) != self.board_size:
            raise Exception(f"Dictionary lenght expected to be {self.board_size} instead of {len(queen_positions)}")
        if min(queen_positions.values()) < 0 or max(queen_positions.values()) > self.board_size - 1: 
            raise Exception(f"Dictionary Y values must be between 0 and {self.board_size - 1} instead of {min(queen_positions.values())} and {max(queen_positions.values())}")
        
        self.queen_positions = queen_positions
        
        self.board = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                if self.queen_positions[j] == i:
                    row.append(1)
                else:
                    row.append(0)
            self.board.append(row)
    
                    
if __name__ == "__main__":

    chess_board = ChessBoardLogic()
    
    pred5_board = {0:4, 1:5, 2:6, 3:3, 4:4, 5:5, 6:6, 7:5}
    chess_board.set_custom_board_state(pred5_board)
    chess_board.print_chessboard()
    
    chess_board.board_colisions_calculator()
    chess_board.print_collisions()
    
    chess_board.board_heuristics_calculator()
    chess_board.print_heruistics()
    
    print(chess_board.get_min_heuristics())

    
