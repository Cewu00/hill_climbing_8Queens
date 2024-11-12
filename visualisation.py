import tkinter as tk
from PIL import Image, ImageTk

class ChessBoardGUI(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__()
        
        self.step = 120
        self.board_size = 8
        self.board_px_width = self.step * self.board_size
        self.board_px_height = self.step * self.board_size
        
        self.geometry(f"{self.board_px_width}x{self.board_px_height}+{int(self.winfo_screenwidth()/2 - self.board_px_width/2)}+{0}")
        self.maxsize(self.board_px_width, self.board_px_height)
        self.minsize(self.board_px_width, self.board_px_height)
        self.title("Chess Board")
        
        self.main_canvas = tk.Canvas(self, width=self.board_px_width, height=self.board_px_height)
        self.main_canvas.pack()
        
        self.draw_board()

        self.queen_images = {}
        for colour in ['Black', 'Green', 'Red']:    
            PIL_img = Image.open(f".\\Sprites\\Img{self.step}px\\Queen_{colour}_{self.step}.png")
            self.queen_images[colour] = ImageTk.PhotoImage(PIL_img)

    def draw_board(self):
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                if (row+col)%2==0:
                    step_colour = '#f3dec5'
                else:
                    step_colour = '#572f00'
                    
                x0 = row * self.step
                y0 = col * self.step
                x1 = x0 + self.step
                y1 = y0 + self.step
                self.main_canvas.create_rectangle(x0, y0, x1, y1, fill=step_colour)
        
    def draw_queen(self):
        self.main_canvas.create_image(0, 0, image = self.queen_images['Black'], anchor='nw')


if __name__ == "__main__":

    gui = ChessBoardGUI()  # ChessboardGUI is now a tk.Tk window
    gui.mainloop()




