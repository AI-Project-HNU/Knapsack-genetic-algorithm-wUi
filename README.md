# ⬡ Knapsack GA Solver

A professional, high-performance **Genetic Algorithm (GA)** solver for the Knapsack Problem. This application features a modern dark-themed GUI built with Python's `tkinter` and provides real-time visualization and data management capabilities.

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

* **Language**: Python 3.8 or higher
* **GUI Framework**: `Tkinter` (with custom threading for non-blocking UI)
* **Data Visualization**: `Matplotlib`
* **Algorithm**: Genetic Algorithm (Selection, Crossover, Mutation, and Fitness Evaluation)

## 📥 Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites

* **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
* **pip** - Python package manager (comes with Python 3.4+)
* **Git** - [Download Git](https://git-scm.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/AI-Project-HNU/Knapsack-genetic-algorithm-wUi.git
cd Knapsack-genetic-algorithm-wUi
```

### 2. Create a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Required packages:**
* `matplotlib>=3.5.0` - For real-time fitness visualization
* `numpy>=1.21.0` - For numerical computations

### 4. Verify Installation

```bash
python -c "import tkinter; import matplotlib; import numpy; print('All dependencies installed successfully!')"
```

### 5. Run the Application

```bash
python main.py
```

The application will launch with a splash screen followed by the main GA Solver interface.

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python Version | 3.8 | 3.10+ |
| RAM | 512 MB | 2 GB+ |
| Disk Space | 100 MB | 500 MB |
| OS | Windows 10+ / macOS 10.14+ / Ubuntu 18.04+ | Latest LTS |

## 🔧 Configuration

### Project Structure

```
Knapsack-genetic-algorithm-wUi/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── gui/               # UI components
│   ├── algorithm/         # Genetic algorithm implementation
│   └── utils/             # Utility functions
└── data/
    └── datasets/          # Sample JSON datasets
```

### Configuration File

Edit `config.json` (if available) to customize:
* Default population size
* Default mutation rate
* Default crossover rate
* Default generations

## 🎯 Quick Start

1. **Launch the app**: `python main.py`
2. **Load a dataset**: Click "Load Dataset" and select a JSON file from the `data/datasets/` folder
3. **Configure GA parameters**: Adjust population size, generations, mutation rate, and crossover rate
4. **Run the algorithm**: Click "Solve" and watch the real-time fitness chart
5. **Export results**: Click "Export" to save your solution

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution**: 
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Tkinter is included with Python.app from python.org

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution**: Run `pip install -r requirements.txt` again to ensure all dependencies are installed.

### Issue: Application runs slowly or crashes
**Solution**: 
- Reduce population size or generation count
- Close other applications to free up memory
- Ensure you have at least 512 MB of available RAM

## 📝 Requirements File

Create a `requirements.txt` file with:

```
matplotlib>=3.5.0
numpy>=1.21.0
```

## 📞 Support & Contribution

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/AI-Project-HNU/Knapsack-genetic-algorithm-wUi).

## 📄 License

This project is part of the CS212 Artificial Intelligence course. Please check the repository for specific license details.

---

**Last Updated**: May 2026
