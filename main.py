from visualisation import ChessBoardGUI
from logic import ChessBoardLogic

    
if __name__ == "__main__":    
    gui = ChessBoardGUI()
    
    logic = ChessBoardLogic()
    logic.print_chessboard()
    
    gui.mainloop()