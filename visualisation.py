import tkinter as tk
from time import sleep
from PIL import Image, ImageTk

class ChessBoardGUI(tk.Tk):
    SUPPORTED_QUEEN_COLOURS = ['Black', 'Green', 'Red']
    SQUARE_COLOURS = ['#F3DEC5', '#3B2824'] #WHITE, #BLACK
    #GREEN_SQUARE_COLOURS = ['#B6E694', '#2B631A'] #WHITE, #BLACK
    GREEN_SQUARE_COLOURS = ['#AEE78C', '#334820'] #WHITE, #BLACK
    
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
        for col in range(0, self.board_size):
            for row in range(0, self.board_size):
                if (col+row)%2==0:
                    square_colour = self.SQUARE_COLOURS[0]
                    text_colour = self.SQUARE_COLOURS[1]
                else:
                    square_colour = self.SQUARE_COLOURS[1]
                    text_colour = self.SQUARE_COLOURS[0]
                    
                x0 = col * self.square
                y0 = row * self.square
                x1 = x0 + self.square
                y1 = y0 + self.square
                self.main_canvas.create_rectangle(x0, y0, x1, y1, fill=square_colour, tags='board')
                self.main_canvas.create_text(x0+5, y0+5, text=f"{row}{col}", font=("Arial", 10), fill=text_colour, anchor="nw", tags="board num")
    
    def draw_queen(self, x:int, y:int, colour:str = 'Black') -> bool:
        if not (isinstance(x, int) and isinstance(y, int)):
            raise Exception(f"x and y have to be intigers, currently they are: {isinstance(x)}, {isinstance(y)}")
        if not ((0 <= x and x < self.board_size) and (0 <= y and y < self.board_size)):
            raise Exception(f"x:{x} and y:{y} have to be between 0 and {self.board_size - 1}")
        if colour not in self.SUPPORTED_QUEEN_COLOURS:
            raise Exception(f"Colour is not supported: {colour}")
        
        if self.queen_positions.get((x, y)) == None:
            img_id = self.main_canvas.create_image(x*self.square, y*self.square, image = self.queen_images[colour], anchor='nw', tags=f"queen")
            self.queen_positions[(x, y)] = img_id # {column, row : Queen ID} - ovako je najbolje      
            return True
        else:
            return False

    def remove_all_queens(self):
        self.queen_positions.clear()
        self.main_canvas.delete('queen')
        self.main_canvas.delete('path')
    
    def remove_queen(self, x, y):
        queen_img = self.queen_positions[x, y]
        self.queen_positions.pop((x, y))
        self.main_canvas.delete(queen_img)
        
    def draw_queen_path(self, x, y):
        self.main_canvas.delete('path')
         
        sq_y = y*self.square 
        for i in range(self.board_size): # horizontala
            if (y + i) % 2 == 0:
                colour = self.GREEN_SQUARE_COLOURS[0] # white
            else:
                colour = self.GREEN_SQUARE_COLOURS[1] # black
            if i != x:
                if self.queen_positions.get((i, y)) != None:
                    self.main_canvas.create_rectangle(i*self.square, sq_y, (i+1)*self.square, sq_y+self.square, fill='red', tags='path horisontal')
                else:
                    self.main_canvas.create_rectangle(i*self.square, sq_y, (i+1)*self.square, sq_y+self.square, fill=colour, tags='path horisontal')
                    
        sq_x = x*self.square
        for i in range(self.board_size): # vertikala
            if (x + i) % 2 == 0:
                colour = self.GREEN_SQUARE_COLOURS[0] # white
            else:
                colour = self.GREEN_SQUARE_COLOURS[1] # black
            if i != y:
                if self.queen_positions.get((x, i)) != None:
                    self.main_canvas.create_rectangle(sq_x, i*self.square, sq_x+self.square, (i+1)*self.square, fill='red', tags='path vertical')
                else:
                    self.main_canvas.create_rectangle(sq_x, i*self.square, sq_x+self.square, (i+1)*self.square, fill=colour, tags='path vertical')
                
        if (x + y) % 2 == 0:
            colour = self.GREEN_SQUARE_COLOURS[0] # white
        else:
            colour = self.GREEN_SQUARE_COLOURS[1] # black
        
        # broj kvadrata koji ce biti od kraljice do kraja table 
        nw_diag = min(y, x)
        ne_diag = min(y, self.board_size - x - 1)
        sw_diag = min(self.board_size - y - 1, x)
        se_diag = self.board_size - 1 - max(y, x)
        
        diagonals = [nw_diag, ne_diag, sw_diag, se_diag]
        movments = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        
        for diagonal, movment in zip(diagonals, movments):
            for i in range(1, diagonal + 1):
                x0 = (x + i*movment[0])
                y0 = (y + i*movment[1])
                sq_x = x0 * self.square
                sq_y = y0 * self.square
                if self.queen_positions.get((x0, y0)) != None:
                    self.main_canvas.create_rectangle(sq_x, sq_y, sq_x+self.square, sq_y+self.square, fill='red', tags='path diagonal')
                else:
                    self.main_canvas.create_rectangle(sq_x, sq_y, sq_x+self.square, sq_y+self.square, fill=colour, tags='path diagonal')
                    
        self.main_canvas.tag_raise('queen')
        self.main_canvas.tag_raise('num')

        
    def test_path_logic(self, x , y, q_list = []):
        if x == self.board_size:
            if y == self.board_size-1:
                return
            for i, j in q_list:
                self.remove_queen(i, j)
            self.after(0, lambda x=0, y=y+1, q_list=[]: self.test_path_logic(x, y, q_list))
        else:
            state = self.draw_queen(x, y)
            if state:
                q_list.append((x, y))
            self.draw_queen_path(x, y)
            self.after(500, lambda x=x+1, y=y: self.test_path_logic(x, y, q_list))


    
if __name__ == "__main__":

    gui = ChessBoardGUI()
    
    gui.after(100, lambda: gui.draw_queen(0, 6))
    gui.after(100, lambda: gui.draw_queen(3, 6))

    gui.test_path_logic(0, 0)
    
    gui.mainloop()




