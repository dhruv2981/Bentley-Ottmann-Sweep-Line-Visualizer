## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## main.py - Entry point for the Bentley–Ottmann Sweep Line Visualizer

import tkinter as tk
from visualizer import BentleyVisualizer

if __name__ == "__main__":
    root = tk.Tk()
    app = BentleyVisualizer(root)
    root.mainloop()
