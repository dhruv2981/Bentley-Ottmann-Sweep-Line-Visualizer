# Bentley–Ottmann Sweep Line Visualizer

## GroupID-20 (22114029_22113078) - Dhruv, Komal  
**Date:** Oct 28, 2025  

This project implements the Bentley–Ottmann Sweep Line Algorithm for two main purposes:

- Detecting intersections among a set of line segments.
- Checking a user-drawn polygon for self-intersections.

It includes graphical user interfaces (GUIs) to visualize both applications.

---

## Features
- **Application Launcher:** A main menu to select either the segment intersection or polygon checking tool.
### Module 1: Segment Intersection (Bentley-Ottmann)
- **Segment Generation:** Randomly generates a set of line segments with unique colors.
- **Event Handling:** Processes left, right, and intersection events using the sweep line algorithm.
- **Visualization:** Displays the segments, sweep line, and detected intersections in real-time.
- **Step Execution:** Allows users to step through the algorithm to observe its behavior.

### Module 2: Polygon Self-Intersection
- **Interactive Drawing:** Allows users to draw a polygon by clicking vertices on the canvas.
- **Self-Intersection Detection:** Runs a modified sweep line algorithm on the polygon's edges.
- **Smart Highlighting:** Correctly finds and displays all self-intersection points, while properly ignoring valid intersections between adjacent edges (at vertices).

---

## Project Structure

### Files
1. **[`main.py`](main.py)**  
   Entry point for the application. Initializes the GUI and starts the visualizer.

2. **[`visualizer.py`](visualizer.py)**  
   Implements the GUI for the Bentley–Ottmann Sweep Line Visualizer using `tkinter`. Handles segment generation, event creation, and visualization updates.

3. **[`polygon_visualizer.py`](polygon_visualizer.py)** 
   Implements the GUI for the Polygon Self-Intersection Detector (Module 2). Handles drawing and results display.

4. **[`sweep_line.py`](sweep_line.py)**  
   Contains the implementation of the sweep line algorithm. Manages the event queue, status structure, and intersection detection.

5. **[`polygon_checker.py`](polygon_checker.py)**
   Contains the derived class (PolygonSweep) that extends SweepLine to add the specific logic for finding non-adjacent intersections in a polygon.

6. **[`segment.py`](segment.py)**  
   Defines the data structures for line segments and events.

7. **[`geometry.py`](geometry.py)**  
   Provides utility functions for geometric calculations, such as orientation tests, segment intersection detection, and y-coordinate computation.

---

## How to Run

1. **Install Dependencies:**  
   Ensure Python 3.x is installed. The project uses the `tkinter` library, which is included in most Python installations.

2. **Run the Application:**  
   Execute the following command in the terminal:
   ```bash
   python main.py