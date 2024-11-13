import tkinter as tk
from PIL import Image, ImageTk

class ChessBoardGUI(tk.Tk):
    SUPPORTED_COLOURS = ['Black', 'Green', 'Red']
    
    def __init__(self, square = 120, board_size = 8):
        super().__init__()
        if square in [100, 120]:
            self.square = square #px
        else:
            raise Exception("Squares can only be 100px or 120px long and wide")
        
        self.board_size = board_size
        self.board_px_width = self.square * self.board_size
        self.board_px_height = self.square * self.board_size
        
        self.geometry(f"{self.board_px_width}x{self.board_px_height}+{int(self.winfo_screenwidth()/2 - self.board_px_width/2)}+{0}")
        self.maxsize(self.board_px_width, self.board_px_height)
        self.minsize(self.board_px_width, self.board_px_height)
        self.title("Chess Board")
        
        self.main_canvas = tk.Canvas(self, width=self.board_px_width, height=self.board_px_height)
        self.main_canvas.pack()
        
        self.draw_board()

        self.queen_images = {}
        for colour in self.SUPPORTED_COLOURS:    
            PIL_img = Image.open(f".\\Sprites\\Img{self.square}px\\Queen_{colour}_{self.square}.png")
            self.queen_images[colour] = ImageTk.PhotoImage(PIL_img)

    def draw_board(self):
        self.main_canvas.delete('all')
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                if (row+col)%2==0:
                    square_colour = '#f3dec5'
                else:
                    square_colour = '#572f00'
                x0 = row * self.square
                y0 = col * self.square
                x1 = x0 + self.square
                y1 = y0 + self.square
                self.main_canvas.create_rectangle(x0, y0, x1, y1, fill=square_colour)
        
    def draw_queen(self, x:int, y:int, colour:str = 'Black'):
        # all(isinstance(i, int) for i in lista) - provjerava jel sve sto je u listu int
        if isinstance(x, int) and isinstance(y, int):
            if (0 < x or x < self.board_size) or (0 < y or y < self.board_size):
                if colour in self.SUPPORTED_COLOURS:
                    self.main_canvas.create_image(x*self.square, y*self.square, image = self.queen_images[colour], anchor='nw')
                else:
                    raise Exception(f"Colour is not supported: {colour}")
            else:
                raise Exception(f"x:{x} and y:{y} have to be between 0 and {self.board_size - 1}")
        else:
            raise Exception(f"x and y have to be intigers, currently they are: {isinstance(x)}, {isinstance(y)}")
        
if __name__ == "__main__":

    gui = ChessBoardGUI()
    gui.draw_queen(0, 0, 'Black')
    gui.draw_queen(3, 4, 'Black')
    gui.draw_queen(3, 7, 'Red')
    gui.mainloop()




