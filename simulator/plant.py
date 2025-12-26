import numpy as np
class TokamakPlant:
    def __init__(self, dt=0.001):
        self.dt = dt
        # Modelo Instável Verticalmente (Autovalor > 1)
        self.A = np.array([[1.01, 0.01], [0.05, 1.0]]) 
        self.B = np.array([[0.0], [0.1]])
        self.x = np.array([0.01, 0.0]) # Inicial perturbado
        
    def step(self, u):
        noise = np.random.normal(0, 0.001, 2)
        self.x = self.A @ self.x + self.B.flatten() * u + noise
        return self.x