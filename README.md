<p align="center">
  <img src="images/yPlus-calculator-logo-blue.png" alt="SaMPH-yPlus Logo" width="180"/>
</p>

<h1 align="center">SaMPH-yPlus</h1>

<p align="center">
  <strong>Advanced CFD y+ and First-Grid Spacing Calculator</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#methodology">Methodology</a> •
  <a href="#screenshots">Screenshots</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/GUI-PySide6%20(Qt6)-41CD52?logo=qt&logoColor=white" alt="PySide6"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License MIT"/>
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey" alt="Platform"/>
</p>

---

## Overview

**SaMPH-yPlus** is a professional desktop application designed for CFD (Computational Fluid Dynamics) engineers and researchers. It provides a modern, user-friendly interface to calculate critical near-wall grid parameters, including **y+**, **first-grid spacing**, **Reynolds number**, and **boundary layer thickness**.

By accurately estimating the first layer height, users can ensure their mesh adheres to the requirements of various turbulence models, leading to more reliable and convergent simulations.

---

## Features

### 🚀 Scientific Core
- **First-Grid Spacing ($\Delta S$)**: Automatic calculation based on target $y^+$ and flow conditions.
- **Multiple Skin Friction ($C_f$) Formulas**:
  - Prandtl-Schlichting (1979)
  - ITTC-1957 (Ship correlation line)
  - Prandtl-Kármán (1932)
- **Boundary Layer Thickness ($\delta$) Estimation**:
  - Schlichting (1979)
  - White (1991)
- **Mesh Layering**: Estimate the number of prism layers ($N$) required to cover the boundary layer based on a specific grid stretch ratio.
- **Spatial Discretization Support**: Handles both **Cell-centered** and **Vertex-centered** schemes.

### 🖥️ Modern Windows 11 GUI
- **Clean Interface**: Built with **PySide6 / Qt6** following modern design principles.
- **Interactive Tools**: 
  - Integrated **Virtual Keyboard** for touch or mouse-driven input.
  - Built-in **Search Bar** (Google/Baidu) for quick access to CFD theory.
- **Real-time Logging**: Comprehensive log panel to track calculation steps and warnings.
- **Input Validation**: Ensures physical realism for velocities, densities, and lengths.

### 🌐 Global Readiness
- **Multilingual**: Supports English and 中文 (Simplified Chinese).
- **Auto-detection**: Smart language and theme loading based on user settings.
- **Persistent Settings**: Remembers your preferred formulas, units, and appearance.

---

## Installation

### Prerequisites

- **Python 3.8+**
- **pip** package manager

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/SaMPH-yPlus.git
cd SaMPH-yPlus

# Install dependencies
pip install -r requirements.txt

# Launch the application
python src/Main.py
```

### Build Executable (Windows)

```bash
# Generate a single standalone EXE
Generate_single_exe.bat
```

The compiled output will be in the `dist/` directory.

---

## Quick Start

1. **Launch** `SaMPH-yPlus`.
2. **Select** your **Material** (e.g., Sea water, Air) or manually enter density and viscosity.
3. **Choose** the **Discretization Scheme** (Cell-centered is common for OpenFOAM/Fluent).
4. **Enter flow parameters**:
   - Freestream Velocity ($U_\infty$)
   - Reference Length ($L$)
   - Target $y^+$ (e.g., 1.0 for wall-resolved, 30-100 for wall-functions)
5. **Click** *"Compute"* (or press Enter).
6. **Review** the output results: **First-grid spacing**, **Reynolds number**, and **Number of prism layers**.

---


## Project Structure

```
SaMPH-yPlus/
├── src/
│   ├── Main.py                 # Entry point
│   ├── Algorithm/
│   │   └── Calculate_yPlus.py  # Core physics & math logic
│   └── GUI/
│       ├── GUI_Application.py  # Main window assembly
│       ├── Operation_*.py      # Business logic controllers
│       ├── Page_*.py           # UI components (Settings, Log, Menu)
│       ├── Utils.py            # Path handling & unit conversions
│       └── Language_Manager.py # i18n support
├── images/                     # Icons and logos
├── usr/                        # User settings & logs (Git ignored)
├── requirements.txt            # Dependencies
├── Generate_single_exe.bat     # Build script
└── README.md
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

**Author**: Shanqin Jin  
**Contact**: sjin@mun.ca
