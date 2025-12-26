
import numpy as np
from simulator.plant import TokamakPlant

env = TokamakPlant()
print("🚀 Simulation Started...")
for i in range(100):
    u = -50.0 * env.x[0] # Controle P simples
    state = env.step(u)
print(f"✅ Final State: {state}")
