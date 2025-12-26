
import numpy as np

class TokamakPlant:
    def __init__(self, dt=0.001):
        self.dt = dt
        # Modelo Instável Verticalmente (Autovalor > 1)
        # x[0] = Posição Z, x[1] = Velocidade Z
        self.A = np.array([[1.001, 0.001], 
                           [0.050, 1.001]]) 
        self.B = np.array([[0.0], 
                           [0.005]])
        self.x = np.array([0.01, 0.0]) # Inicial perturbado (1cm)
        
    def step(self, u_volts):
        # Ruído de processo (Plasma noise)
        w = np.random.normal(0, 0.0001, 2)
        
        # Evolução de Estado: x_k+1 = A*x_k + B*u_k + w
        self.x = self.A @ self.x + self.B.flatten() * u_volts + w
        return self.x
