# NPE-PSQ-2D: Tokamak Vertical Stability Simulator

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

**NPE-PSQ (Nuclear Plasma Engineering - Plasma Simulator)** is a lightweight 2D physics engine designed to simulate the vertical instability event (VDE) in tokamak fusion reactors.

It serves as the *Hardware-in-the-Loop* (HIL) testing environment for the **AION-CORE** control framework.

## 🚀 Features
- **Unstable Dynamics:** Simulates the natural vertical drift of elongated plasmas ($A > 1$).
- **OpenAI Gym Style:** Simple `.step(action)` interface for RL agents.
- **Noise Injection:** Gaussian process noise to test robustness.

## 🕹️ Visual Demo
Active stabilization of the plasma column:

![Plasma Demo](prometheus_demo.gif)

## 💻 Usage
```python
from simulator.plant import TokamakPlant

env = TokamakPlant()
state = env.step(u_control)
```

---
*Last Build: 2025-12-26 17:27:52*