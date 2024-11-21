from visualisation import ChessBoardGUI
from logic import ChessBoardLogic

def set_board(gui:ChessBoardGUI, queen_positions:dict): # for logic only
    if len(queen_positions) != gui.board_size:
        raise Exception(f"Queen position lenght not matching board size {len(queen_positions)} != {gui.board_size}")
    if all(x in queen_positions for x in range(gui.board_size)):
        raise Exception(f"X values must be between 0 and {gui.board_size - 1}")
    
    for i in range(gui.board_size):
        y = queen_positions[i]

def move_queen(self, x_position, new_y):
    pass

if __name__ == "__main__":    
    gui = ChessBoardGUI()
    logic = ChessBoardLogic()
    
    queen_positions = {}
    
    set_board(gui, queen_positions)
    
    
    gui.mainloop()