import tkinter as tk
from tkinter import ttk
import numpy as np

def hide_odd_size_message():
    odd_size_message_label.grid_forget()

def show_odd_size_message():
    odd_size_message_label.grid(row=3, column=0, padx=10, pady=(5, 10))

def is_odd(n):
    # Check if a number is odd
    return n % 2 != 0

def is_magic_square(matrix):
    n = len(matrix)

    if not is_odd(n):
        return False, "its size is not odd"

    # Calculate the expected sum (magic constant)
    magic_constant = n * (n**2 + 1) // 2

    # Create a set to store values in the matrix
    values = set()

    # Check row and column sums
    sums = []
    for i in range(n):
        row_sum = 0
        col_sum = 0
        for j in range(n):
            value = matrix[i][j]
            if value < 1 or value > n**2:
                return False, "it contains values outside the range [1, n^2]"
            if value in values:
                return False, f"it contains duplicate value: {value}"
            values.add(value)
            row_sum += value
            col_sum += matrix[j][i]
        if row_sum != magic_constant or col_sum != magic_constant:
            return False, f"the sum of row {i+1} or column {i+1} is not equal to the magic constant"
        sums.append((row_sum, col_sum))

    # Check diagonal sums
    main_diag_sum = sum(matrix[i][i] for i in range(n))
    anti_diag_sum = sum(matrix[i][n - i - 1] for i in range(n))
    if main_diag_sum != magic_constant or anti_diag_sum != magic_constant:
        return False, "the sum of diagonals is not equal to the magic constant"

    return True, sums

def display_sums(sums, main_diag_sum, anti_diag_sum):
    size = len(sums)

    for i, (row_sum, col_sum) in enumerate(sums):
        row_sum_label = ttk.Label(matrix_frame, text=f"{row_sum}", foreground="blue")
        row_sum_label.grid(row=i, column=size, padx=10)
        col_sum_label = ttk.Label(matrix_frame, text=f"{col_sum}", foreground="blue")
        col_sum_label.grid(row=size, column=i, pady=(5, 10))

    """# Display diagonal sums
    ttk.Label(matrix_frame, text=f"{main_diag_sum}", foreground="blue").grid(row=size, column=size, padx=10, pady=5)
    ttk.Label(matrix_frame, text=f"{anti_diag_sum}", foreground="blue").grid(row=size + 1, column=size, padx=9, pady=9)
"""
# Create the main window
root = tk.Tk()

# Add a title
root.title("Magic Square Checker")

# Add a section about Magic Squares
info_frame = ttk.Frame(root)
info_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
info_title = ttk.Label(info_frame, text="\u2728 Magic Square \u2728", font=("Segoe UI", 16))
info_title.pack(pady=10)
info_text = ttk.Label(info_frame, text="A magic square is a sequence of numbers, usually integers, that are arranged in a square grid. In a magic square, the sum of each row, column, and diagonal should be the same.", wraplength=450)
info_text.pack(padx=20)

# Create Entry widgets for the user to enter the number of rows and columns
root.columnconfigure(0, weight=1)  # Add this line
size_label = ttk.Label(root, text="Enter Size:")
size_label.grid(row=1, column=0, padx=10, pady=(20, 5))
size_entry = ttk.Entry(root)
size_entry.grid(row=2, column=0, padx=10)

# Create a frame to hold the matrix Entry widgets
matrix_frame = ttk.Frame(root)
matrix_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=(20, 0))

# Add a label for the "Please enter an odd size" message
odd_size_message_label = ttk.Label(root, text="Please enter an odd size", foreground="red")
odd_size_message_label.grid(row=3, column=0, padx=10, pady=(5, 10))
odd_size_message_label.grid_remove()  # Hide the message initially

def create_matrix_entries():
    # Check if the size is even and inform the user
    size = int(size_entry.get())
    if size % 2 == 0:
        show_odd_size_message()
        size_entry.delete(0, tk.END)
    else:
        hide_odd_size_message()
        # Hide the "Create Matrix" button
        create_button.grid_remove()

        # Clear the matrix frame
        for widget in matrix_frame.winfo_children():
            widget.destroy()

        # Create a grid of Entry widgets for the matrix
        for i in range(size):
            for j in range(size):
                entry = ttk.Entry(matrix_frame, width=2)
                entry.grid(row=i, column=j)

        # Increase the number of rows and columns by 1 for diagonal sums
        ttk.Label(matrix_frame, text="", width=2).grid(row=size, column=size, padx=10)
        ttk.Label(matrix_frame, text="", width=2).grid(row=size, column=size + 1, pady=(5, 10))

        def check_magic_square():
            # Get the matrix from the Entry widgets
            size = int(size_entry.get())
            matrix = np.zeros((size, size), dtype=int)
            for i in range(size):
                for j in range(size):
                    matrix[i][j] = int(matrix_frame.grid_slaves(row=i, column=j)[0].get())

            """# Check if the matrix is a magic square
            result, sums = is_magic_square(matrix)
            result_label.config(text="The matrix is a Magic Square.", foreground= "green" if result else "The matrix is not a Magic Square")"""
            # Determine whether it's a magic square
            result,sums = is_magic_square(matrix)
            is_magic, _ = is_magic_square(matrix)
            result_label.config(text="The matrix is a Magic Square." if is_magic else "The matrix is not a Magic Square", foreground="green" if is_magic else "red")
            if result:
                main_diag_sum = sum(matrix[i][i] for i in range(size))
                anti_diag_sum = sum(matrix[i][size - i - 1] for i in range(size))
                display_sums(sums, main_diag_sum, anti_diag_sum)

        # Show the "Check Magic Square" button
        check_button = ttk.Button(root, text="Check Magic Square", command=check_magic_square)
        check_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create a button for the user to click after entering the number of rows and columns
create_button = ttk.Button(root, text="Create Matrix", command=create_matrix_entries)
create_button.grid(row=4, column=0, padx=10, pady=10)

# Create a label to display the result
result_label = ttk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2, padx=10)

# Start the application
root.mainloop()