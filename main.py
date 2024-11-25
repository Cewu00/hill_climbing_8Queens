from visualisation import ChessBoardGUI
from logic import ChessBoardLogic
from random import randint
from queue import Queue

class TaskScheduler:
    def __init__(self, gui:ChessBoardGUI):
        self.gui = gui
        self.task_queue = Queue()
        self.is_task_running = False

    def add_task(self, func, delay, *args, **kwargs):
        """Add a task to the queue."""
        self.task_queue.put((func, delay, args, kwargs))

    def execute_next_task(self):
        """Execute the next task in the queue."""
        if not self.task_queue.empty() and not self.is_task_running:
            self.is_task_running = True  # Block the scheduler until the task finishes
            func, delay, args, kwargs = self.task_queue.get()

            # Call the function after the delay, passing the `done_callback`
            self.gui.after(delay, lambda: func(self.done_callback, *args, **kwargs))

    def done_callback(self):
        """Signal that the current task is done and trigger the next task."""
        self.is_task_running = False
        self.execute_next_task()


def set_board(done_callback, gui:ChessBoardGUI, queen_positions:dict):
    if len(queen_positions) != gui.board_size:
        raise Exception(f"Queen position length not matching board size {len(queen_positions)} != {gui.board_size}")
    if not all(x in queen_positions for x in range(gui.board_size)):
        raise Exception(f"X values must be between 0 and {gui.board_size - 1}")
    
    for i in range(gui.board_size):
        y = queen_positions[i]
        gui.draw_queen(i, y)

    # Signal the scheduler that this task is complete
    done_callback()
        

def move_queen(gui:ChessBoardGUI, logic:ChessBoardLogic, x:int, new_y:int):
    y = queen_positions[x]
    logic.move_queen(x, new_y)
    gui.move_queen(x, y, x, new_y)

def move_to_minimum(done_callback, gui:ChessBoardGUI, logic:ChessBoardLogic):
    minimum = logic.chosen_minimum
    move_queen(gui, logic, minimum[1], minimum[0])
    
    done_callback()
    
def show_all_collisions(done_callback, gui:ChessBoardGUI, logic:ChessBoardLogic):
    collisions = logic.board_colisions_calculator()
    queen_positions = logic.queen_positions
    after_time = 0  # Local delay tracker

    def cleanup_and_finish():
        """Remove path visuals and signal the task is complete."""
        gui.main_canvas.delete('path')
        done_callback()

    for x in range(len(collisions)):
        x_queen = x
        y_queen = queen_positions[x]
        
        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.remove_queen(x, y))
        after_time += 250
        for y in range(len(collisions)):
            gui.after(after_time, lambda x=x, y=y, colour='Green': gui.draw_queen(x, y, colour))
            gui.after(after_time, lambda x=x, y=y: gui.draw_queen_path(x, y))
            gui.after(after_time, lambda x=x, y=y, number=collisions[y][x]: gui.write_number_large(x, y, number))
            after_time += 250
            gui.after(after_time, lambda x=x, y=y: gui.remove_queen(x, y))
            gui.after(after_time, lambda x=x, y=y: gui.large_to_small(x, y))

        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.draw_queen(x, y))

    # Clean up and signal completion after all animations are done
    gui.after(after_time, cleanup_and_finish)
    

def show_all_herusitics(done_callback, gui: ChessBoardGUI, logic: ChessBoardLogic):
    heuristics = logic.board_heuristics_calculator()
    queen_positions = logic.queen_positions
    after_time = 0  # Local delay tracker
    
    def cleanup_and_finish():
        """Clean up any temporary paths or visuals and signal the task is complete."""
        gui.main_canvas.delete('path')
        done_callback()

    for x in range(len(heuristics)):
        x_queen = x
        y_queen = queen_positions[x]

        # Remove the queen at the start of processing
        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.remove_queen(x, y))
        after_time += 250

        # Process heuristic values for each cell in the column
        for y in range(len(heuristics)):
            gui.after(after_time, lambda x=x, y=y, colour='Green': gui.draw_queen(x, y, colour))
            # Display heuristic value
            gui.after(after_time, lambda x=x, y=y, number=heuristics[y][x]: gui.write_number_large(x, y, number))
            after_time += 250
            # Remove temporary visualization
            gui.after(after_time, lambda x=x, y=y: gui.remove_queen(x, y))

        # Restore the original queen in the column
        gui.after(after_time, lambda x=x_queen, y=y_queen: gui.draw_queen(x, y))

    # After all animations, clean up and call the done callback
    gui.after(after_time, cleanup_and_finish)   

def show_minimums(done_callback, gui:ChessBoardGUI, logic:ChessBoardLogic):
    x_min, y_min, minimum = logic.get_min_heuristics()
    coord_minimums = logic.possible_minimums
    after_time = 0
    
    def cleanup_and_finish():
        gui.main_canvas.delete('circle')
        done_callback()
    
    for x, y in coord_minimums:
        gui.after(after_time, lambda id=gui.large_numbers_positions[(y, x)] : gui.main_canvas.itemconfig(tagOrId=id, fill='purple'))
    
    after_time += 250
    repeats = 3
    for i in range(repeats):
        for yc, xc in coord_minimums:
            gui.after(after_time, lambda x=xc, y=yc : gui.draw_circle(x, y))
            after_time += 300
            if i == repeats-1 and xc == x_min and yc == y_min:
                for j in range(3):
                    gui.after(after_time, lambda tag='circle', colour='green' : gui.main_canvas.itemconfig(tagOrId=tag, outline=colour, fill=colour))
                    after_time += 200
                    gui.after(after_time, lambda tag='circle', colour='purple', fill='' : gui.main_canvas.itemconfig(tagOrId=tag, outline=colour, fill=fill))
                    after_time += 200
                break     
            gui.after(after_time, lambda : gui.main_canvas.delete('circle'))
                    
    gui.after(after_time, cleanup_and_finish)
    
# def hill_climbing_visualised():
#     return
    

if __name__ == "__main__":
    gui = ChessBoardGUI()
    logic = ChessBoardLogic()
    scheduler = TaskScheduler(gui)

    queen_positions = logic.queen_positions

    # Add tasks to the scheduler
    scheduler.add_task(set_board, 500, gui, queen_positions)
    
    scheduler.add_task(show_all_collisions, 1000, gui, logic)
    scheduler.add_task(show_all_herusitics, 1000, gui, logic)
    scheduler.add_task(show_minimums, 1000, gui, logic)
    scheduler.add_task(move_to_minimum, 1000, gui, logic)
    scheduler.add_task(show_all_collisions, 1000, gui, logic)
    scheduler.add_task(show_all_herusitics, 1000, gui, logic)
    scheduler.add_task(show_minimums, 1000, gui, logic)
    scheduler.add_task(move_to_minimum, 1000, gui, logic)

    # Start the task execution
    scheduler.execute_next_task()

    gui.mainloop()