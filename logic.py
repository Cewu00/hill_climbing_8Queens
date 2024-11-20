from random import randint
from time import time

class ChessBoardLogic():
    def __init__(self, board_size=8): 
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.collisions = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.queen_positions = {} # (x : y)
        self.current_heuristics = 0
        
        # self.random_board()
        # self.board_colisions_calculator()
        # self.board_heuristics_calculator()
        
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
        
        self.current_heuristics = heur//2
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.queen_positions[i] == j:
                    self.heuristics[j][i] = (heur - 2 * original_colisions[i] + 2 * self.collisions[j][i])//2
                    if self.current_heuristics != self.heuristics[j][i]: # za svaki slucaj... koliko ovdje ima setanja po ovim matricama ne bi me cudilo da sam nesto zabrljao
                        raise Exception("Something's wrong I can feel it!")
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
        random_choice = randint(1, minimum_count) # TODO: pitaj profa: da li ovo sto se vraca vazda treba da bude prvi???

        num = 1
        for i in range(len(minimums)):
            if minimums[i] != 0:
                for tp in minimums[i]:
                    if num == random_choice:
                        return (i, tp[0], tp[1]) # x, y, heuristic_value (returning a random heuristic value of all the lowest ones)
                    num += 1
        
    def move_queen(self, queen_x, new_y):
        queen_y = self.queen_positions.pop(queen_x)
        self.board[queen_y][queen_x] = 0
        self.board[new_y][queen_x] = 1
        self.queen_positions[queen_x] = new_y

    def hill_climbing(self):
        num = 0
        random_move_counter = 0
        queen_x, new_y, value = self.get_min_heuristics()
        while True:
            queen_x, new_y, value = self.get_min_heuristics()
            if value == 0:
                self.move_queen(queen_x, new_y)
                num += 1
                #print(value, self.current_heuristics)
                return num, True
            else:
                self.move_queen(queen_x, new_y)
                num += 1
                #print(value, self.current_heuristics)
                self.board_colisions_calculator()
                self.board_heuristics_calculator()
            
            if value >= self.current_heuristics:
                self.move_queen(randint(0, self.board_size-1), randint(0, self.board_size-1))
                random_move_counter += 1
                if random_move_counter == 100:
                    break
                
        return num, False
    
    def hill_climbing_premmited_equalities(self, number_of_equalities:int = 100):
        #ovo samo doupsta da se krecemo po nasumicnim jednakim vrijednostima do 100 puta... 
        #nije rijesenje za 100 sporednih poteza
        num = 0
        equality_num = 0
        queen_x, new_y, value = self.get_min_heuristics()
        while value <= self.current_heuristics:
            queen_x, new_y, value = self.get_min_heuristics()
            if value == 0:
                self.move_queen(queen_x, new_y)
                num += 1
                #print(value, self.current_heuristics)
                return num, True
            else:
                self.move_queen(queen_x, new_y)
                num += 1
                #print(value, self.current_heuristics)
                self.board_colisions_calculator()
                self.board_heuristics_calculator()
            
            if value == self.current_heuristics: # ovo bi trabalo da samo ako 
                equality_num += 1
                if equality_num == number_of_equalities:
                    break
            else:
                equality_num = 0
                  
        return num, False
        
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
    
                    
if __name__ == "__main__": # ovdje pisi stvari dok testiras 
    
    chess_board = ChessBoardLogic()
    
    # pred5_board = {0:4, 1:5, 2:6, 3:3, 4:4, 5:5, 6:6, 7:5}
    # chess_board.set_custom_board_state(pred5_board.copy())
    # chess_board.print_chessboard()
    
    # chess_board.board_colisions_calculator()
    # chess_board.print_collisions()
    
    # chess_board.board_heuristics_calculator()
    # chess_board.print_heruistics()

    steps_taken_list = []
    steps_taken_failed_list = []
    success_rate = 0
    fail_rate = 0
    t1 = time()
    for i in range(1000):
        chess_board.random_board()
        chess_board.board_colisions_calculator()
        chess_board.board_heuristics_calculator()
        steps_taken, state = chess_board.hill_climbing()
        if state:
            success_rate += 1
        else:
            fail_rate += 1
            steps_taken_failed_list.append(steps_taken)
        steps_taken_list.append(steps_taken)
        
        print(f"{i} > {steps_taken}, {success_rate}, {fail_rate}")
        
    t2 = time()


    #print(steps_taken_list, success_rate, fail_rate)
    print(f"Fail Rate: {(fail_rate/(success_rate+fail_rate)) * 100:.2f}%")
    print(f"Success Rate: {(success_rate/(success_rate+fail_rate)) * 100:.2f}%")
    
    print(f"AVG number of steps: {sum(steps_taken_list)/len(steps_taken_list)}")
    print(f"AVG number of steps (excluding faliures): {(sum(steps_taken_list) - sum(steps_taken_failed_list))/(len(steps_taken_list) - fail_rate)}")


    print(f"Time Taken: {t2 - t1:.2f}s")
    print(f"Time Taken for One Loop: {(t2 - t1)/1000 * 10**3:.2f}ms")

        

    
