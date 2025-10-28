## GroupID-20 (22114029_22113078) - Dhruv, Komal
## Date: Oct 28, 2025
## visualizer.py - Bentley–Ottmann Sweep Line Visualizer

import tkinter as tk
from tkinter import ttk
import random
from geometry import segment_intersection
from segment import Segment, Event
from sweep_line import SweepLine

class BentleyVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Bentley–Ottmann Sweep Line Visualizer")

        self.W, self.H = 900, 600
        self.canvas = tk.Canvas(master, width=self.W, height=self.H, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.right = ttk.Frame(master)
        self.right.pack(side=tk.LEFT, fill=tk.Y, padx=8)

        ttk.Label(self.right, text="n (segments):").pack()
        self.n_var = tk.IntVar(value=20)
        ttk.Entry(self.right, textvariable=self.n_var, width=6).pack(pady=4)
        ttk.Button(self.right, text="Generate", command=self.generate_segments).pack()
        ttk.Button(self.right, text="Step", command=self.step).pack(pady=4)

        self.log_box = tk.Text(self.right, height=25, width=40)
        self.log_box.pack(pady=4)

        self.segments, self.events = [], []
        self.event_index = 0
        self.sweep = None
        self.colors = ["#ef4444","#f59e0b","#10b981","#3b82f6","#7c3aed","#ec4899","#0ea5a4"]

        self.generate_segments()

    def log(self, msg: str):
        self.log_box.insert("1.0", msg + "\n")

    def generate_segments(self):
        n = self.n_var.get()
        self.canvas.delete("all")
        self.segments = []
        for i in range(n):
            x1, y1 = random.uniform(20, self.W-20), random.uniform(20, self.H-20)
            x2, y2 = random.uniform(20, self.W-20), random.uniform(20, self.H-20)
            color = self.colors[i % len(self.colors)]
            seg = Segment(i, (x1, y1), (x2, y2), color)
            self.segments.append(seg)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        self.create_events()
        self.event_index = 0
        self.sweep = SweepLine(self.segments, log_fn=self.log)
        self.log(f"Generated {n} random segments")

    def create_events(self):
        self.events = []
        for s in self.segments:
            left = s.a if s.a[0] < s.b[0] else s.b
            right = s.b if left is s.a else s.a
            self.events.append(Event(left[0], left[1], 'L', (s.id, None)))
            self.events.append(Event(right[0], right[1], 'R', (s.id, None)))
        self.events.sort(key=lambda e: (e.x, e.y))
        self.log(f"Created {len(self.events)} events")

    def step(self):
        if not self.sweep or self.event_index >= len(self.events):
            self.log("No more events.")
            return
        ev = self.events[self.event_index]
        self.sweep.process_event(ev)
        self.event_index += 1
        self.redraw(ev)

    def redraw(self, ev):
        self.canvas.delete("all")
        # draw all segments
        for s in self.segments:
            self.canvas.create_line(s.a[0], s.a[1], s.b[0], s.b[1], fill=s.color, width=2)
        # draw intersections
        for (x, y) in self.sweep.intersections:
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black")
        # draw sweep line
        self.canvas.create_line(ev.x, 0, ev.x, self.H, fill="red", dash=(5,3))
