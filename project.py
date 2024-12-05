import tkinter as tk
from tkinter import messagebox
from queue import Queue, PriorityQueue
import time

# Helper Functions
def is_valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid."""
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        if board[box_row + i // 3][box_col + i % 3] == num:
            return False
    return True

def find_empty_cell(board):
    """Find the next empty cell on the Sudoku board."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def update_gui(board, elapsed_time, delay=0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001):
    """Update the GUI with the current board state."""
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)
            if board[row][col] != 0:
                entries[row][col].insert(0, str(board[row][col]))
    time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
    root.update()
    time.sleep(delay)

# BFS Solver
def bfs_solver(board):
    queue = Queue()
    queue.put(board)
    start_time = time.time()
    while not queue.empty():
        current_board = queue.get()
        elapsed_time = time.time() - start_time
        update_gui(current_board, elapsed_time)  # Show each step
        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                queue.put(new_board)
    return None

# DFS Solver
def dfs_solver(board):
    stack = [board]
    start_time = time.time()
    while stack:
        current_board = stack.pop()
        elapsed_time = time.time() - start_time
        update_gui(current_board, elapsed_time)  # Show each step
        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                stack.append(new_board)
    return None

# UCS Solver
def ucs_solver(board):
    pq = PriorityQueue()
    pq.put((0, board))
    start_time = time.time()
    while not pq.empty():
        cost, current_board = pq.get()
        elapsed_time = time.time() - start_time
        update_gui(current_board, elapsed_time)  # Show each step
        empty_cell = find_empty_cell(current_board)
        if not empty_cell:
            return current_board
        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(current_board, row, col, num):
                new_board = [row[:] for row in current_board]
                new_board[row][col] = num
                pq.put((cost + 1, new_board))
    return None

# GUI Functions
def load_board():
    """Load the board from the GUI entries."""
    board = []
    for row in range(9):
        current_row = []
        for col in range(9):
            value = entries[row][col].get()
            current_row.append(int(value) if value.isdigit() else 0)
        board.append(current_row)
    return board

def reset():
    """Clear all entries."""
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)
            if default_board[row][col] != 0:
                entries[row][col].insert(0, str(default_board[row][col]))
    time_label.config(text="Elapsed Time: 0.00 seconds")

def solve_with_algorithm(algorithm):
    """Solve the Sudoku puzzle with the selected algorithm."""
    board = load_board()
    solved_board = algorithm(board)
    if solved_board:
        update_gui(solved_board, time.time() - start_time, delay=0)  # type: ignore # Final update without delay
        messagebox.showinfo("Success", f"Sudoku solved using {algorithm._name_}!")
    else:
        messagebox.showerror("Error", "No solution exists!")

# Default Sudoku Puzzle
default_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# GUI Setup
root = tk.Tk()
root.title("Sudoku Solver with Timing")
root.geometry("500x640")

entries = [[None for _ in range(9)] for _ in range(9)]

# Create a grid of Entry widgets
for row in range(9):
    for col in range(9):
        entry = tk.Entry(root, width=2, font=('Arial', 18), justify='center')
        entry.grid(row=row, column=col, padx=5, pady=5, ipady=5)
        entries[row][col] = entry
        if default_board[row][col] != 0:
            entry.insert(0, str(default_board[row][col]))

# Elapsed Time Label
time_label = tk.Label(root, text="Elapsed Time: 0.00 seconds", font=('Arial', 14))
time_label.grid(row=9, column=0, columnspan=9, pady=10)

# Buttons for Algorithms
button_frame = tk.Frame(root)
button_frame.grid(row=10, column=0, columnspan=9, pady=10)

bfs_button = tk.Button(button_frame, text="Solve with BFS", font=('Arial', 12), bg='blue', fg='white',
                       command=lambda: solve_with_algorithm(bfs_solver))
bfs_button.grid(row=0, column=0, padx=5)

dfs_button = tk.Button(button_frame, text="Solve with DFS", font=('Arial', 12), bg='green', fg='white',
                       command=lambda: solve_with_algorithm(dfs_solver))
dfs_button.grid(row=0, column=1, padx=5)

ucs_button = tk.Button(button_frame, text="Solve with UCS", font=('Arial', 12), bg='orange', fg='white',
                       command=lambda: solve_with_algorithm(ucs_solver))
ucs_button.grid(row=0, column=2, padx=5)

reset_button = tk.Button(root, text="Reset", font=('Arial', 14), bg='red', fg='white', command=reset)
reset_button.grid(row=11, column=0, columnspan=9, pady=10, sticky="ew")

# Run the GUI
root.mainloop()