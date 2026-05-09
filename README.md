# Plot-Sandbox

<img src="readme.gif" width="640" alt="Plot-Sandbox Physics Simulation" style="display: block; margin-left: auto; margin-right: auto;">

## Overview

Plot-Sandbox is a Python visualization tool that simulates how nodes interact under physical forces. Each node experiences gravity toward a central focus point, repulsion from nearby nodes, and attraction between connected pairs. The system evolves over time until reaching equilibrium, providing insight into how data structures compress and organize themselves within vector space.

## How It Works

The project separates concerns into independent layers. The DOM stores node positions, weights, and connectivity. The physics engine applies forces using pure NumPy calculations without any knowledge of the UI. Mutations to the graph are queued between physics steps to avoid race conditions. The 3D renderer displays the live state and updates in place as nodes move, creating a smooth visualization of the system relaxing toward stability.

## Running the Application

To launch the interactive physics simulator with a Tkinter window, run `python main.py`. For reproducible layouts, you can seed the initial state with `python main.py --seed 42`. To run in headless mode without the UI, use `python main.py --cli`. The application will display nodes as spheres in 3D space, with colors and sizes determined by node properties, and edges drawn between nodes that fall within the attraction radius.

Dependencies are listed in `requirements.txt` and include matplotlib and NumPy.
