# 📖 Changelog

All notable changes to this project will be documented here.  
This project follows [Semantic Versioning](https://semver.org/).

---

## [2.1.0](https://github.com/kallegrens/dfrobot_environmental_sensor/compare/v2.0.0...v2.1.0) (2025-08-23)


### Features

* add support for pip installation ([c2c6235](https://github.com/kallegrens/dfrobot_environmental_sensor/commit/c2c623589278f9df28bccebe54bfe61c14969708))


### Bug Fixes

* debug UV sensor ([f0bc8da](https://github.com/kallegrens/dfrobot_environmental_sensor/commit/f0bc8da651f41e2da8976e977b23c3c859e0c98f))
* more readable constant names ([5116078](https://github.com/kallegrens/dfrobot_environmental_sensor/commit/511607828dc470a7a62ff9ca71b17ec54b218e1c))
* move release-please config to parent dir .github/ ([efb1564](https://github.com/kallegrens/dfrobot_environmental_sensor/commit/efb1564d5c56c9e297ee6625bd5f9ae3501afc85))
* update .gitignore to exclude venv ([644dab4](https://github.com/kallegrens/dfrobot_environmental_sensor/commit/644dab4b779ea7ae5440e3c42f84580e17c3c14e))

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
