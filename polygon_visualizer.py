## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 29, 2025
## polygon_visualizer.py - GUI for polygon self-intersection

import tkinter as tk
from tkinter import ttk
from typing import List
from geometry import Point
import polygon_checker

class PolygonVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Polygon Self-Intersection Detector")

        self.W, self.H = 900, 600
        self.canvas = tk.Canvas(master, width=self.W, height=self.H, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.right = ttk.Frame(master)
        self.right.pack(side=tk.LEFT, fill=tk.Y, padx=8)

        ttk.Label(self.right, text="Instructions:").pack()
        ttk.Label(self.right, text="1. Click on the canvas to add points.", wraplength=250).pack(anchor='w')
        ttk.Label(self.right, text="2. Click 'Check Polygon' to finish.", wraplength=250).pack(anchor='w')
        
        self.btn_check = ttk.Button(self.right, text="Check Polygon", command=self.check_polygon)
        self.btn_check.pack(pady=10)
        
        self.btn_clear = ttk.Button(self.right, text="Clear", command=self.clear_canvas)
        self.btn_clear.pack()

        self.log_box = tk.Text(self.right, height=25, width=40)
        self.log_box.pack(pady=10)

        self.vertices: List[Point] = []
        self.canvas_items = []
        
        self.canvas.bind("<Button-1>", self.add_point)
        self.log("Ready. Click to draw polygon vertices.")

    def log(self, msg: str):
        self.log_box.insert("1.0", msg + "\n")

    def add_point(self, event):
        x, y = float(event.x), float(event.y)
        self.vertices.append((x, y))
        
        v_id = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="blue")
        self.canvas_items.append(v_id)
        
        if len(self.vertices) > 1:
            p1 = self.vertices[-2]
            p2 = self.vertices[-1]
            e_id = self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2)
            self.canvas_items.append(e_id)
        
        self.log(f"Added vertex {len(self.vertices)} at ({x:.0f}, {y:.0f})")

    def clear_canvas(self):
        for item_id in self.canvas_items:
            self.canvas.delete(item_id)
        self.canvas.delete("intersection")
            
        self.vertices = []
        self.canvas_items = []
        self.log_box.delete("1.0", tk.END)
        self.log("Cleared canvas. Ready to draw new polygon.")

    def check_polygon(self):
        if len(self.vertices) < 3:
            self.log("Error: A polygon needs at least 3 vertices.")
            return

        p_last = self.vertices[-1]
        p_first = self.vertices[0]
        e_id = self.canvas.create_line(p_last[0], p_last[1], p_first[0], p_first[1], fill="blue", width=2)
        self.canvas_items.append(e_id)
        
        self.log(f"Checking {len(self.vertices)}-sided polygon...")
        self.canvas.unbind("<Button-1>")

        intersection_points = polygon_checker.check_polygon(self.vertices, log_fn=self.log)
        
        if intersection_points:
            self.log(f"--- POLYGON IS SELF-INTERSECTING ---")
            self.log(f"Found {len(intersection_points)} non-adjacent intersection(s):")
            
            for i, (x, y) in enumerate(intersection_points):
                self.log(f"  {i+1}. at ({x:.2f}, {y:.2f})")
                
                self.canvas.create_oval(x-6, y-6, x+6, y+6, 
                                        outline="red", fill="red", tags="intersection")
                self.canvas.create_text(x, y-10, text=f"{i+1}", 
                                        fill="red", tags="intersection", font=("Arial", 10, "bold"))
        else:
            self.log(f"--- Polygon is SIMPLE (not self-intersecting) ---")
            
        self.canvas.bind("<Button-1>", self.add_point)
