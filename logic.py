class ChessBoardLogic():
    def __init__(self, size=8):
            self.size = size
            self.board = [[0 for _ in range(size)] for _ in range(size)]
            
            self.queen_colour = {
                1: 'Black',
                2: 'Green',
                3: 'Red'
            }

    def print_chessboard(self):
        print("Current state of the chessboard:")
        for red in self.board:
            print(red)
        print('\n')
    
    def diagonal_queens(self):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if i == j:
                    self.board[j][i] = 1
                    
    