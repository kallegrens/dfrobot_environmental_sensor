# 📖 Changelog

All notable changes to this project will be documented here.  
This project follows [Semantic Versioning](https://semver.org/).

---

## [2.0.0] - 2025-08-20

### ✨ Added

- Python 3.8+ support using `smbus3`
- Refactored example scripts for Raspberry Pi
- Modernized README with usage examples and installation instructions
- PyPi compatible project structure, enabling installation by `pip`

### 💥 Breaking Changes

- Removed all Arduino-related code and support — the fork is **Python-only**.
- Dropped support for Python 2.x and Python < 3.8.

### ⚠️ Changed

- Restructured repository for Python usage (cleaner module layout, updated docs).
- Library renamed for PyPI: `dfrobot-environmental-sensor` (import path is `dfrobot_environmental_sensor`).

### 🐛 Fixed

- Broken documentation links

---

## [1.1.0] - 2024-12-18

### ⚡ Changed

- Code updates from DFRobot

## [1.0.2] - 2022-07-01

### 🐛 Fixed

- Minor fixes and demo adjustments

## [1.0.1] - 2022-05-18

### 🐛 Fixed

- Initial bugfixes and demo changes

## [1.0.0] - 2021-12-20

### ✨ Added

- Initial release by DFRobot (Arduino-compatible)
