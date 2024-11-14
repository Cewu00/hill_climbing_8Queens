import tkinter as tk
from time import sleep
from PIL import Image, ImageTk

class ChessBoardGUI(tk.Tk):
    SUPPORTED_QUEEN_COLOURS = ['Black', 'Green', 'Red']
    SQUARE_COLOURS = ['#f3dec5', '#3b2824']
    
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
        for colour in self.SUPPORTED_QUEEN_COLOURS:    
            PIL_img = Image.open(f".\\Sprites\\Img{self.square}px\\Queen_{colour}_{self.square}.png")
            self.queen_images[colour] = ImageTk.PhotoImage(PIL_img)
            
        self.queen_positions = {}

    def draw_board(self):
        self.main_canvas.delete('board')
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                if (row+col)%2==0:
                    square_colour = self.SQUARE_COLOURS[0]
                else:
                    square_colour = self.SQUARE_COLOURS[1]
                x0 = row * self.square
                y0 = col * self.square
                x1 = x0 + self.square
                y1 = y0 + self.square
                self.main_canvas.create_rectangle(x0, y0, x1, y1, fill=square_colour, tags='board')
    
    def draw_queen(self, x:int, y:int, colour:str = 'Black') -> int:
        # all(isinstance(i, int) for i in lista) - provjerava jel sve sto je u listu int
        if isinstance(x, int) and isinstance(y, int):
            if (0 <= x and x < self.board_size) and (0 <= y and y < self.board_size):
                if colour in self.SUPPORTED_QUEEN_COLOURS:
                    if self.queen_positions.get(x) == None:
                        queen_img = self.main_canvas.create_image(x*self.square, y*self.square, image = self.queen_images[colour], anchor='nw', tags=f"queen {x}{y}")
                        self.queen_positions[x] = (y, queen_img) # {column : row, object} - ovako je najbolje jer ce tabela imati samo jednu kraljicu po koloni
                        # univerzalinije bi bilo nesto tipa {(x, y): colour} nije dobro bas ali trt sad... muka mi je mjenjat sve XD                    
                        return queen_img
                else:
                    raise Exception(f"Colour is not supported: {colour}")
            else:
                raise Exception(f"x:{x} and y:{y} have to be between 0 and {self.board_size - 1}")
        else:
            raise Exception(f"x and y have to be intigers, currently they are: {isinstance(x)}, {isinstance(y)}")
    
    def remove_all_queens(self):
        self.queen_positions = {}
        self.main_canvas.delete('queen')
        self.main_canvas.delete('path')
    
    def remove_queen(self, x):
        queen_img = self.queen_positions[x][1]
        self.main_canvas.delete(queen_img)
        
    def draw_queen_path(self, x):
        self.main_canvas.delete('path')
        
        y = self.queen_positions[x][0] # x, y
        sq_x = x*self.square
        sq_y = y*self.square
        
        for i in range(1, self.board_size):
            i = i * self.square
            if sq_x - i >=0:
                self.main_canvas.create_rectangle(sq_x-i, sq_y, sq_x-i +self.square, sq_y+self.square, fill='green', tags='path') # - =
                if sq_y + i <= self.board_px_height:
                    self.main_canvas.create_rectangle(sq_x-i, sq_y+i, sq_x-i+self.square, sq_y+i+self.square, fill='green', tags='path') # - +
                if sq_y - i >= 0:
                    self.main_canvas.create_rectangle(sq_x-i, sq_y-i, sq_x-i +self.square, sq_y-i +self.square, fill='green', tags='path') # - -
            if sq_x + i <= self.board_px_width: # and sq_y + i <= self.board_px_height:
                self.main_canvas.create_rectangle(sq_x+i, sq_y, sq_x+i+self.square, sq_y+self.square, fill='green', tags='path') # + =
                if sq_y + i <= self.board_px_height:
                    self.main_canvas.create_rectangle(sq_x+i, sq_y+i, sq_x+i +self.square, sq_y+i +self.square, fill='green', tags='path') # + +
                if sq_y - i >= 0:
                    self.main_canvas.create_rectangle(sq_x+i, sq_y-i, sq_x+i+self.square, sq_y-i+self.square, fill='green', tags='path') # + -    
            if sq_y - i >= 0:
                self.main_canvas.create_rectangle(sq_x, sq_y-i, sq_x+self.square, sq_y-i+self.square, fill='green', tags='path') # = -
            if sq_y + i <= self.board_px_height:
                self.main_canvas.create_rectangle(sq_x, sq_y+i, sq_x+self.square, sq_y+i+self.square, fill='green', tags='path') # = +
        # osmislicu kasnije neki matematicki-ji nacin da ovo nacrtam
        
        
def test_path_logic(x , y):
    if x == gui.board_size:
        if y == gui.board_size-1:
            return
        gui.remove_all_queens()
        gui.after(0, lambda x=0, y=y+1: test_path_logic(x, y))
    else:
        gui.draw_queen(x, y)
        id = gui.draw_queen_path(x)
        gui.after(500, lambda x=x+1, y=y: test_path_logic(x, y))
    

    
if __name__ == "__main__":

    gui = ChessBoardGUI()

    
    gui.after(500, lambda: gui.draw_queen(7, 7))

    test_path_logic(0, 0)

   
    gui.mainloop()




