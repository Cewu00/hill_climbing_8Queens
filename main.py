from visualisation import ChessBoardGUI
from logic import ChessBoardLogic

after_time_tracker = 0

def set_board(gui:ChessBoardGUI, queen_positions:dict): # for logic result only, queen_positions {x:y}
    if len(queen_positions) != gui.board_size:
        raise Exception(f"Queen position lenght not matching board size {len(queen_positions)} != {gui.board_size}")
    if not all(x in queen_positions for x in range(gui.board_size)):
        raise Exception(f"X values must be between 0 and {gui.board_size - 1}")
    for i in range(gui.board_size):
        y = queen_positions[i]
        gui.draw_queen(i, y)
        

def move_queen(gui:ChessBoardGUI, x:int, queen_positions:dict, new_y:int):
    global after_time_tracker
    y = queen_positions.pop(x)
    queen_positions[x] = new_y
    after_time_tracker += 1000
    gui.move_queen(x, y, x, new_y)


def hill_climbing_visualised():
    return
    

if __name__ == "__main__":    
    gui = ChessBoardGUI()
    logic = ChessBoardLogic()
    
    
    queen_positions = logic.queen_positions
    
    set_board(gui, queen_positions)
    
    
    gui.mainloop()