from random import randint

class ChessBoardLogic():
    QUEEN_COLOUR = {
    1: 'Black',
    2: 'Green',
    3: 'Red'
    }
    
    # nekako sam uspio da ucinim ove matrice potpuno neintuitivnim... 
    # doduse takve su ja mislim... jer ne mozes o matrici da mislis kao o kordinatnom sistemu
    # uglavnom fora je da u matrici[y][x] zapravo prvo pristupas vertikali a tek onda horizontali... [[0,1,2], [0,1,2], [0,1,2]] 
    # a kad covjek o tome razimslja uvjek prvo ide x jel da XD... dok mi nesto to nije uslo u glavu sve sam odje dumao zasto su mi stvari ne konzistentne lol
    
    # sad sam provalio zasto sam se zbunio... jer kad imas for loop... 
    # ides vazda matrica[i][j] a nesto mi nije ulazilo u glavu da je to tako jer se prvo j vrti pa tek onda i... nebitno XD
    
    def __init__(self, board_size=8): 
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.collisions = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.heuristics = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.queen_positions = {} # (x : y)
        
        self.random_board()
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
    
    def board_heuristics_calculator(self): # TODO: ispravi ovo.
        # TODO: POGRESNO! heuristika mora da bude ukupni broj kolizija za trenutno stanje na cijeloj tabeli a ne samo za kvadrat
        # imam pozicije kraljica... sad mozemo da za svaku kocku samo saberemo sve pozicije osim
        
        heur = 0
        for x in range(self.board_size):
            y = self.queen_positions[x]
            heur += self.collisions[y][x]
        print(heur)
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                pass
    
    def min_heuristics_calc(self): # ovo ako radi kako treba ne bi trebalo da pravi problem nakon sto popravim racunanje heuristike
        minimums = []
        for i in range(self.board_size):
            num1 = self.heuristics[0][i]
            minimum_col = []
            for j in range(self.board_size - 1): # TODO: FIX! ne appenduje (7, num) ili (0, num) provjeri... mislim da je ovo drugo
                num2 = self.heuristics[j+1][i]
                if num1 > num2:
                    minimum_col = []
                    minimum_col.append((j+1, num2)) # y, heuristics_value (x nam ne treba jer ce to biti redom izlistano u listi 'minimums' koja se pravi)
                    num1 = num2
                elif num1 == num2:
                    minimum_col.append((j+1, num2)) # y, heuristics_value
                    
            minimums.append(minimum_col)
        for row in minimums:
            print(row)       
    
    def run_algorithm(self):
        pass
                    
if __name__ == "__main__":

    chess_board = ChessBoardLogic()
    chess_board.print_chessboard()
    chess_board.print_heruistics()
    chess_board.min_heuristics_calc()

    
