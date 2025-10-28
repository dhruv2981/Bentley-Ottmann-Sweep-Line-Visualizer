# Bentley–Ottmann Sweep Line Visualizer

## GroupID-20 (22114029_22113078) - Dhruv, Komal  
**Date:** Oct 28, 2025  

This project implements the Bentley–Ottmann Sweep Line Algorithm for detecting intersections among a set of line segments. It includes a graphical user interface (GUI) to visualize the algorithm's step-by-step execution.

---

## Features
- **Segment Generation:** Randomly generates a set of line segments with unique colors.
- **Event Handling:** Processes left, right, and intersection events using the sweep line algorithm.
- **Visualization:** Displays the segments, sweep line, and detected intersections in real-time.
- **Step Execution:** Allows users to step through the algorithm to observe its behavior.

---

## Project Structure

### Files
1. **[`main.py`](main.py)**  
   Entry point for the application. Initializes the GUI and starts the visualizer.

2. **[`visualizer.py`](visualizer.py)**  
   Implements the GUI for the Bentley–Ottmann Sweep Line Visualizer using `tkinter`. Handles segment generation, event creation, and visualization updates.

3. **[`sweep_line.py`](sweep_line.py)**  
   Contains the implementation of the sweep line algorithm. Manages the event queue, status structure, and intersection detection.

4. **[`segment.py`](segment.py)**  
   Defines the data structures for line segments and events.

5. **[`geometry.py`](geometry.py)**  
   Provides utility functions for geometric calculations, such as orientation tests, segment intersection detection, and y-coordinate computation.

---

## How to Run

1. **Install Dependencies:**  
   Ensure Python 3.x is installed. The project uses the `tkinter` library, which is included in most Python installations.

2. **Run the Application:**  
   Execute the following command in the terminal:
   ```bash
   python main.py