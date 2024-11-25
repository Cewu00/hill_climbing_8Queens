from random import randint, choice
from time import time
import matplotlib.pyplot as plt
import numpy as np


class ChessBoardLogic():
    def __init__(self, board_size=8): 
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.collisions = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.queen_positions = {} # (x : y)
        self.current_heuristics = 0
        self.possible_minimums = []
        self.chosen_minimum = 0
        # vecina ovih pamcenja jedne vrijednosti se radi radi lakse vizuelizacije
        
        self.random_board()
        
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
                if self.board[y0][x0] == 1:
                    num += 1
        return num
    
    def board_colisions_calculator(self): # znam da racunanje kolizije ne mora da se poziva za cijelu tablu i da je dovoljno samo da uradimo -1 na stare putanje
        for i in range(self.board_size):  # i +1 na nove putanje pomjerene kraljice... ali necu da unosim mogucu dodatnu nebulozu... ovako je jednostavno
            for j in range(self.board_size):
                self.collisions[i][j] = self.square_collisions_calculator(j, i) # x, y
        
        return self.collisions
    
    def board_heuristics_calculator(self):
        original_colisions = [] # pocetno stanje kraljica
        for x in range(self.board_size):
            y = self.queen_positions[x]
            # print(x, y)
            original_colisions.append(self.collisions[y][x])
        heur = sum(original_colisions) # heuristika za pocetno stanje
        # print(original_colisions, heur)
        
        self.current_heuristics = heur//2
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.queen_positions[i] == j:
                    self.heuristics[j][i] = heur//2 - original_colisions[i] + self.collisions[j][i]
                    if self.current_heuristics != self.heuristics[j][i]: # za svaki slucaj... koliko ovdje ima setanja po ovim matricama ne bi me cudilo da sam nesto zabrljao
                        raise Exception("Something's wrong I can feel it!")
                else:
                    self.heuristics[j][i] = heur//2 - original_colisions[i] + self.collisions[j][i]

        return self.heuristics
    
    def get_min_heuristics(self):
        matrix = np.array(self.heuristics)

        min_coords = []
        min_value = float('inf')
        for x in range(self.board_size):
            for y in range(self.board_size):
                if x in self.queen_positions and self.queen_positions[x] == y:
                    continue
                
                if matrix[x, y] < min_value:
                    min_value = matrix[x, y]
                    min_coords = [(x, y)]  # reset sa ovom kordinatom
                elif matrix[x, y] == min_value:
                    min_coords.append((x, y))
        
        self.possible_minimums = min_coords # pamtimo vrijednost svih minimuma radi lakse vizuelizacije
        # ako imamo vise kordinata istih minimalnih vrijednosti biramo nasumicnu
        selected_coord = choice(min_coords)
        self.chosen_minimum = selected_coord # pamtimo vrijednost odabranog minimuma radi lakse vizuelizacije
        
        return selected_coord[1], selected_coord[0], min_value
    
    def move_queen(self, queen_x, new_y):
        queen_y = self.queen_positions.pop(queen_x)
        self.board[queen_y][queen_x] = 0
        self.board[new_y][queen_x] = 1
        self.queen_positions[queen_x] = new_y

    def hill_climbing(self):
        # bojim se da nesto ovdje nisam shvatio kako treba... jer nikako ne mogu da spustim broj poteza na 21 kako stoji u knjizi... 
        # ispravio sam par stvari (koje su bile pogresne) i sad vise ni success_rate nije kako treba...
        step_counter = 0
        random_move_counter = 0
        while True:
            queen_x, new_y, value = self.get_min_heuristics()
            #print(queen_x, new_y, value)
            if value == 0:
                self.move_queen(queen_x, new_y)
                step_counter += 1
                #print(value, self.current_heuristics)
                return step_counter, random_move_counter, True
            
            elif value == self.current_heuristics: 
                # gledao sam vizuelizaciju koja implementira algoritam na isti nacin... algoritam, voli da se zaglavi i da, nakon sto iskoci sa nasumicnim brojem,
                # se vrati u prethodno polje... ali nisam siguran koji bi bio najbolji nacin da to rijesim... 
                # razmisljao sam mozda samo da radim nasumicne poteze dok se minimum ne pomjeri... ali ne znam
                x = randint(0, self.board_size-1)
                y = randint(0, self.board_size-1)
                while y == self.queen_positions[x]: # ima smisla da nasumicni pomjeraj mora biti pomjeraj... a ne isto stanje
                    x = randint(0, self.board_size-1)
                    y = randint(0, self.board_size-1)
                self.move_queen(x, y)
                random_move_counter += 1
                #step_counter += 1 # bas nisam siguran da li ovo treba da se broji ali neka ga...
                if random_move_counter == 100:
                    break
                self.board_colisions_calculator()
                self.board_heuristics_calculator()
            elif value > self.current_heuristics: 
                break
            elif value < self.current_heuristics:
                self.move_queen(queen_x, new_y)
                step_counter += 1
                self.board_colisions_calculator()
                self.board_heuristics_calculator()

     
        return step_counter, random_move_counter, False
        
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
    
    # Tabla iz knjige
    # pred5_board = {0:4, 1:5, 2:6, 3:3, 4:4, 5:5, 6:6, 7:5}
    # chess_board.set_custom_board_state(pred5_board.copy())
    # chess_board.print_chessboard()
    
    # chess_board.board_colisions_calculator()
    # chess_board.print_collisions()
    
    # chess_board.board_heuristics_calculator()
    # chess_board.print_heruistics()

    iter_number = 200
    
    steps_taken_list = []
    steps_taken_failed_list = []
    steps_taken_success_list = []
    
    random_count_list = []
    random_count_failed_list = []
    random_count_success_list = []

    success_rate = 0
    fail_rate = 0
    
    t1 = time()
    for i in range(1, iter_number+1):
        chess_board.random_board()
        chess_board.board_colisions_calculator()
        chess_board.board_heuristics_calculator()
        steps_taken, random_count, state = chess_board.hill_climbing()
        if state:
            success_rate += 1
            steps_taken_success_list.append(steps_taken)
            random_count_success_list.append(random_count)
        else:
            fail_rate += 1
            steps_taken_failed_list.append(steps_taken)
            random_count_failed_list.append(random_count)
            
        steps_taken_list.append(steps_taken)
        random_count_list.append(random_count) 
        
        print(f"{i} > {steps_taken}, {success_rate}, {fail_rate}, {random_count}")  
    t2 = time()

    print(f"\nSuccess Rate: {(success_rate/(success_rate+fail_rate)) * 100:.2f}%")
    print(f"Fail Rate: {(fail_rate/(success_rate+fail_rate)) * 100:.2f}%")
    
    print(f"\nAVG number of steps: {sum(steps_taken_list)/len(steps_taken_list):.2f}")
    print(f"AVG number of steps (success): {sum(steps_taken_success_list) / len(steps_taken_success_list):.2f}")
    print(f"AVG number of steps (failure): {sum(steps_taken_failed_list) / len(steps_taken_failed_list):.2f}")
    
    print(f"\nAVG number of sidesteps: {sum(random_count_list) / len(random_count_list):.2f}")
    print(f"AVG number of sidesteps (success): {sum(random_count_success_list) / len(random_count_success_list):.2f}")
    print(f"AVG number of sidesteps (failure): {sum(random_count_failed_list) / len(random_count_failed_list):.2f}")
    
    print(f"\nTime Taken: {t2 - t1:.2f}s")
    print(f"Avg Time Taken for One Loop: {(t2 - t1)/iter_number * 10**3:.2f}ms")
    
    fig, axes = plt.subplots(3, 2, figsize=(16, 8))  # 8x8 inches for good window size

    all_lists = [[steps_taken_list, steps_taken_success_list, steps_taken_failed_list], [random_count_list, random_count_success_list, random_count_failed_list]]
    all_titles = [['Steps Taken (Total)', 'Steps Taken (Success)', 'Steps Taken (Fail)'], ['Side-steps Taken (Total)', 'Side-steps Taken (Success)', 'Side-steps Taken (Fail)']]
    for i in range(len(all_lists)):
        for j in range(len(all_lists[i])):
            axes[j, i].hist(all_lists[i][j], bins=range(min(all_lists[i][j]), max(all_lists[i][j]) + 2), edgecolor='black')
            axes[j, i].set_title(all_titles[i][j])
            axes[j, i].set_xlabel('Number')
            axes[j, i].set_ylabel('Frequency')
            
    y_lims = [ax.get_ylim() for ax_row in axes for ax in ax_row]
    global_y_min = min(y[0] for y in y_lims)
    global_y_max = max(y[1] for y in y_lims)

    for ax_row in axes:
        for ax in ax_row:
            ax.set_ylim(global_y_min, global_y_max)
        
    plt.tight_layout()
    plt.show()
    
    
    
