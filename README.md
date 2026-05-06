# ⬡ Knapsack GA Solver

> 🎒 A modern desktop GUI for solving **0-1** and **Unbounded Knapsack Problems** using a **Genetic Algorithm**  
> 🎓 Built for *CS212 Artificial Intelligence · Q19*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-5B8DEF?style=flat)](https://docs.python.org/3/library/tkinter.html)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-5B8DEF?style=flat)](https://matplotlib.org)

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🖼️ Screenshots](#️-screenshots)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🎮 Usage Guide](#-usage-guide)
- [⚙️ GA Parameters](#️-ga-parameters)
- [📁 Project Structure](#-project-structure)
- [🔧 Configuration](#-configuration)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔀 **Dual Problem Support** | Solve both **0-1 Knapsack** (items once) and **Unbounded Knapsack** (items repeated) |
| 🧬 **Genetic Algorithm Engine** | Configurable evolution: population, generations, mutation & crossover rates |
| 🎨 **Modern Dark UI** | Clean, customizable interface built with tkinter and custom themed widgets |
| 📊 **Live Fitness Visualization** | Real-time matplotlib chart showing convergence over generations |
| ✏️ **Interactive Item Editor** | Add, edit (double-click), delete, or randomize items directly in the table |
| 📤 **Dataset Management** | Load predefined problem instances or export results to `.txt` |
| ⏱️ **Responsive Execution** | GA runs in background thread with progress bar and stop capability |
| ✅ **Input Validation** | Robust checks for items, capacity, and GA parameters before execution |

---

## 🖼️ Screenshots

> *Placeholders — replace with actual screenshots from your application*

<div align="center">

![Main Interface](docs/screenshots/main_ui.png)  
*Main dashboard with items table, parameters, and results*

![Fitness Chart](docs/screenshots/fitness_chart.png)  
*Live convergence plot during GA execution*

![Results Export](docs/screenshots/export_results.png)  
*Formatted solution output with export option*

</div>

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/knapsack-ga-solver.git
cd knapsack-ga-solver

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
python main.py
