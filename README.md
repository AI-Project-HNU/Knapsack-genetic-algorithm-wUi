# ⬡ Knapsack GA Solver

A professional, high-performance **Genetic Algorithm (GA)** solver for the Knapsack Problem. This application features a modern dark-themed GUI built with Python's `tkinter` and provides real-time visualization of the evolutionary process.

Developed as part of the **CS212 Artificial Intelligence** coursework.

## 🚀 Features

* **Dual Problem Support**: Solve both **0-1 Knapsack** (each item used once) and **Unbounded Knapsack** (items can be reused) problems.
* **Modern Dark UI**: Custom-styled widgets including a splash screen, progress bars, and "badges" for key metrics.
* **Real-time Visualization**: Dynamic fitness tracking chart using `matplotlib` to show how the solution improves over generations.
* **Flexible Data Management**:
    * Load predefined datasets from JSON.
    * Add, edit, or delete items directly within an interactive table.
    * Generate random test cases on the fly.
* **Hyperparameter Tuning**: Full control over GA parameters, including population size, generation count, mutation rate, and crossover rate.
* **Export Capabilities**: Save your best results and selected items to a `.txt` file for further analysis.

## 🛠️ Technical Stack

* **Language**: Python 3
* **GUI Framework**: `Tkinter` (with custom threading for non-blocking UI)
* **Data Visualization**: `Matplotlib`
* **Algorithm**: Genetic Algorithm (Selection, Crossover, Mutation, and Fitness Evaluation)

## 📥 Installation & Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/knapsack-ga-solver.git](https://github.com/YOUR_USERNAME/knapsack-ga-solver.git)
cd knapsack-ga-solver
