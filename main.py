## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## main.py - Entry point for the Bentley–Ottmann Sweep Line Visualizer

import tkinter as tk
from tkinter import ttk
from visualizer import BentleyVisualizer
from polygon_visualizer import PolygonVisualizer

def launch_bentley(launcher_window):
    """Closes launcher and opens the Bentley-Ottmann visualizer."""
    launcher_window.destroy()
    root = tk.Tk()
    app = BentleyVisualizer(root)
    root.mainloop()

def launch_polygon(launcher_window):
    """Closes launcher and opens the Polygon Self-Intersection visualizer."""
    launcher_window.destroy()
    root = tk.Tk()
    app = PolygonVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    launcher = tk.Tk()
    launcher.title("Project Version Selector")
    
    frame = ttk.Frame(launcher, padding="20 20 20 20")
    frame.pack()

    ttk.Label(frame, text="Please choose an application to run:",
              font=("Arial", 14)).pack(pady=10)

    ttk.Button(frame, text="1. Bentley–Ottmann Visualizer", 
               command=lambda: launch_bentley(launcher)).pack(fill='x', pady=5)
               
    ttk.Button(frame, text="2. Polygon Self-Intersection Detector", 
               command=lambda: launch_polygon(launcher)).pack(fill='x', pady=5)

    launcher.eval('tk::PlaceWindow . center')
    launcher.mainloop()