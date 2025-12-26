import numpy as np
import matplotlib.pyplot as plt
from simulator.plant import TokamakPlant

def run():
    env = TokamakPlant()
    history = []
    print("🚀 Starting NPE-PSQ Simulation...")
    for t in range(100):
        # Controlador Proporcional simples para teste
        u = -10.0 * env.x[0] 
        state = env.step(u)
        history.append(state[0])
    
    print("✅ Simulation finished. Z-position final:", history[-1])

if __name__ == "__main__":
    run()