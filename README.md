<div align="center">
  <img src="docs/banner.png" alt="NPE Banner" width="100%">
  <br><br>

  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)]()
  [![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()
  [![Physics](https://img.shields.io/badge/Physics-Unstable-red?style=for-the-badge)]()
</div>

---

# ⚡ NPE-PSQ-2D: Tokamak Physics Engine

> **Lightweight vertical instability simulator for Hardware-in-the-Loop testing**
> *The testing ground for AION-CORE*

## 🎯 Overview

**NPE-PSQ (Nuclear Plasma Engineering - Plasma Simulator)** is a specialized 2D physics engine designed to simulate the **Vertical Displacement Event (VDE)** in elongated tokamak plasmas.

Unlike general-purpose simulators, NPE-PSQ focuses strictly on the unstable vertical dynamics ($dz/dt$) to validate high-frequency control algorithms under chaotic conditions.

---

## ⚛️ Physics Model

The simulator models the plasma as a rigid current filament moving in a magnetic field with a negative decay index (unstable equilibrium).

**State Space Equation:**
$$ \dot{x} = A x + B u + w $$

Where $A$ contains the instability growth rate $\gamma > 0$ (eigenvalue > 1).

### Simulation Output
Comparison between an uncontrolled VDE (Red) and AION stabilization (Green):

![Physics Demo](docs/physics_demo.png)

---

## 🕹️ Usage (OpenAI Gym Style)

Designed to be easy for Reinforcement Learning or Classical Control testing.

```python
from simulator.plant import TokamakPlant

# Initialize Reactor
env = TokamakPlant(instability_rate=1.05)

# Control Loop
state = env.reset()
for t in range(100):
    action = -50.0 * state[0] # P-Controller
    next_state = env.step(action)
    print(f"Position Z: {next_state[0]:.4f} m")
```

---

## 🏗️ Integration with AION

```mermaid
graph LR
    AION[🧠 AION-CORE] -->|Voltage (u)| NPE[⚡ NPE-PSQ-2D]
    NPE -->|State (z, dz)| AION
    NPE -->|Disturbances| Noise((Gaussian Noise))
    style NPE fill:#f9f,stroke:#333,stroke-width:2px
```

---

## 👤 Author

**Guilherme Brasil (Akira)**
*Fusion Energy Enthusiast & Developer*

---

## 📚 References
1. **ITER Technical Basis** - Chapter 2: Plasma Control.
2. **Lazarus et al.** - *Vertical Stability in Highly Elongated Tokamaks*.