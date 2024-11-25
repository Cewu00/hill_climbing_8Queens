from visualisation import ChessBoardGUI
from logic import ChessBoardLogic
from random import randint
from queue import Queue
from copy import deepcopy

class TaskScheduler:
    def __init__(self, gui:ChessBoardGUI):
        self.gui = gui
        self.task_queue = Queue()
        self.is_task_running = False

    def add_task(self, func, delay, *args, **kwargs):
        self.task_queue.put((func, delay, args, kwargs))

    def execute_next_task(self):
        if not self.task_queue.empty() and not self.is_task_running:
            self.is_task_running = True  # Block the scheduler until the task finishes
            func, delay, args, kwargs = self.task_queue.get()

            # Call the function after the delay, passing the `callback`
            self.gui.after(delay, lambda: func(self.callback, *args, **kwargs))

    def callback(self):
        self.is_task_running = False
        self.execute_next_task()
        

def set_board(callback, gui:ChessBoardGUI, queen_positions:dict):
    if len(queen_positions) != gui.board_size:
        raise Exception(f"Queen position length not matching board size {len(queen_positions)} != {gui.board_size}")
    if not all(x in queen_positions for x in range(gui.board_size)):
        raise Exception(f"X values must be between 0 and {gui.board_size - 1}")
    
    for i in range(gui.board_size):
        y = queen_positions[i]
        gui.draw_queen(i, y)

    # Signal the scheduler that this task is complete
    callback()

def change_queens_colour(callback, gui:ChessBoardGUI, colour:str):
    gui.main_canvas.itemconfig('queen', image=gui.queen_images[colour])

def show_random(callback, gui:ChessBoardGUI, x:int, y:int):
    after_time = 0
    
    for i in range(0, gui.board_size):
        for j in range(0, gui.board_size):
            after_time += 25
            gui.draw_circle(j, i)
            
    random_moves = []
    for i in range(0, gui.board_size**2//3):
        xr = randint(0, gui.board_size-1)
        yr = randint(0, gui.board_size-1)
        while xr == x and yr == y:
            xr = randint(0, gui.board_size-1)
            yr = randint(0, gui.board_size-1)
            
        random_moves.append((xr, yr))
        
    for coord in random_moves:
        gui.
        for j in range(3):
            gui.after(after_time, lambda tag='circle', colour='green' : gui.main_canvas.itemconfig(tagOrId=tag, outline=colour, fill=colour))
            after_time += 200 
            gui.after(after_time, lambda tag='circle', colour='blue', fill='' : gui.main_canvas.itemconfig(tagOrId=tag, outline=colour, fill=fill))
            after_time += 200
        break    
    
    callback()
            

def move_queen(callback, gui:ChessBoardGUI, x:int, new_y:int, y):
    gui.main_canvas.delete('large')
    gui.move_queen(x, y, x, new_y)
    callback()
    
def show_all_collisions(callback, gui:ChessBoardGUI, collisions:list, queen_positions:dict):
    after_time = 0  # Local delay tracker

    def cleanup_and_finish():
        gui.main_canvas.delete('path')
        callback()

    for x in range(len(collisions)):
        x_queen = x
        y_queen = queen_positions[x]
        
        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.remove_queen(x, y))
        after_time += 250
        for y in range(len(collisions)):
            gui.after(after_time, lambda x=x, y=y, colour='Green': gui.draw_queen(x, y, colour))
            gui.after(after_time, lambda x=x, y=y: gui.draw_queen_path(x, y))
            gui.after(after_time, lambda x=x, y=y, number=collisions[y][x]: gui.write_number_large(x, y, number))
            after_time += 100 # brzina, sto manje to je brze
            gui.after(after_time, lambda x=x, y=y: gui.remove_queen(x, y))
            gui.after(after_time, lambda x=x, y=y: gui.large_to_small(x, y))

        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.draw_queen(x, y))

    gui.after(after_time, cleanup_and_finish)
    

def show_all_herusitics(callback, gui:ChessBoardGUI, heuristics:list, queen_positions:dict):
    after_time = 0
    
    def cleanup_and_finish():
        gui.main_canvas.delete('path')
        callback()

    for x in range(len(heuristics)):
        x_queen = x
        y_queen = queen_positions[x]

        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.remove_queen(x, y))
        after_time += 300

        for y in range(len(heuristics)):
            gui.after(after_time, lambda x=x, y=y, colour='Green': gui.draw_queen(x, y, colour))
            gui.after(after_time, lambda x=x, y=y, number=heuristics[y][x]: gui.write_number_large(x, y, number))
            after_time += 100 # brzina, sto manje to je brze
            gui.after(after_time, lambda x=x, y=y: gui.remove_queen(x, y))

        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.draw_queen(x, y))

    gui.after(after_time, cleanup_and_finish)   

def show_minimums(callback, gui:ChessBoardGUI, x_min, y_min, coord_minimums):
    after_time = 0
    
    def cleanup_and_finish():
        gui.main_canvas.delete('circle')
        callback()
    
    for x, y in coord_minimums:
        gui.after(after_time, lambda id=gui.large_numbers_positions[(y, x)] : gui.main_canvas.itemconfig(tagOrId=id, fill='purple'))
    
    after_time += 250
    repeats = 3
    for i in range(repeats):
        for yc, xc in coord_minimums:
            gui.after(after_time, lambda x=xc, y=yc : gui.draw_circle(x, y))
            after_time += 300 # brzina, sto manje to je brze
            if i == repeats-1 and xc == x_min and yc == y_min:
                for j in range(3):
                    gui.after(after_time, lambda tag='circle', colour='green' : gui.main_canvas.itemconfig(tagOrId=tag, outline=colour, fill=colour))
                    after_time += 200 
                    gui.after(after_time, lambda tag='circle', colour='purple', fill='' : gui.main_canvas.itemconfig(tagOrId=tag, outline=colour, fill=fill))
                    after_time += 200
                break     
            gui.after(after_time, lambda : gui.main_canvas.delete('circle'))
                    
    gui.after(after_time, cleanup_and_finish)
    
def hill_climbing_steps(gui:ChessBoardGUI, logic:ChessBoardLogic):
    random_num = 0
    
    collisions = deepcopy(logic.board_colisions_calculator())
    heuristics = deepcopy(logic.board_heuristics_calculator())
    queen_positions = deepcopy(logic.queen_positions)
    previous_heuristics = logic.current_heuristics
    
    scheduler.add_task(show_all_collisions, 0, gui, collisions, queen_positions)
    scheduler.add_task(show_all_herusitics, 0, gui, heuristics, queen_positions)
    
    while True:
        x_min, y_min, minimum = deepcopy(logic.get_min_heuristics())
        coord_minimums = deepcopy(logic.possible_minimums)
        
        if minimum != previous_heuristics:
            scheduler.add_task(show_minimums, 1000, gui, x_min, y_min, coord_minimums)

        #print(previous_heuristics, minimum)
        if minimum == 0:
            y_old = logic.queen_positions[x_min]
            logic.move_queen(x_min, y_min)
            scheduler.add_task(move_queen, 1000, gui, x_min, y_min, y_old)
            #print(logic.queen_positions)
            return True
        elif minimum == previous_heuristics:
            random_num += 1
            xr = randint(0, logic.board_size-1)
            yr = randint(0, logic.board_size-1)
            while yr == logic.queen_positions[xr]:
                xr = randint(0, logic.board_size-1)
                yr = randint(0, logic.board_size-1)
            y_old = logic.queen_positions[xr]
            print(xr, yr, y_old)
            logic.move_queen(xr, yr)
            #scheduler.add_task(show_random, 1000, gui, xr, yr) # TODO: FINISH VISUALISATION FOR RANDOM MOVE
            scheduler.add_task(move_queen, 1000, gui, xr, yr, y_old)
            
            collisions = deepcopy(logic.board_colisions_calculator())
            heuristics = deepcopy(logic.board_heuristics_calculator())
            queen_positions = deepcopy(logic.queen_positions)
            previous_heuristics = logic.current_heuristics
            
            scheduler.add_task(show_all_collisions, 1000, gui, collisions, queen_positions)
            scheduler.add_task(show_all_herusitics, 1000, gui, heuristics, queen_positions)
            
            if random_num >= 100:
                return False
        elif minimum < previous_heuristics:
            y_old = logic.queen_positions[x_min]
            logic.move_queen(x_min, y_min)
            print(x_min, y_min, y_old)
            scheduler.add_task(move_queen, 1000, gui, x_min, y_min, y_old)
            collisions = deepcopy(logic.board_colisions_calculator())
            heuristics = deepcopy(logic.board_heuristics_calculator())
            queen_positions = deepcopy(logic.queen_positions)
            previous_heuristics = logic.current_heuristics
            
            scheduler.add_task(show_all_collisions, 1000, gui, collisions, queen_positions)
            scheduler.add_task(show_all_herusitics, 1000, gui, heuristics, queen_positions)
        elif minimum > previous_heuristics:
            return False
        

        
        

if __name__ == "__main__":
    gui = ChessBoardGUI()
    logic = ChessBoardLogic()
    scheduler = TaskScheduler(gui)

    queen_positions = logic.queen_positions.copy()
    scheduler.add_task(set_board, 0, gui, queen_positions)
    
    # prikazije jedan prolaz algoritma, nebitno da li se algoritam izvrsio uspjesno ili ne
    result = hill_climbing_steps(gui, logic)
    print(result)
    if result:
        scheduler.add_task(change_queens_colour, 500, gui, 'Green')
    else:
        scheduler.add_task(change_queens_colour, 500, gui, 'Red')

    scheduler.execute_next_task() # empty the schedule :D

    gui.mainloop()