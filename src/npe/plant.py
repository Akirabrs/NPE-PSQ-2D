
import numpy as np

class TokamakPlant:
    """
    NPE-PSQ-2D: Linearized Vertical Instability Model (VDE)
    Simulates the vertical motion of a plasma filament in an unstable magnetic field.
    
    Dynamics:
    dz/dt = v
    dv/dt = gamma^2 * z + (F_act / m)
    """
    def __init__(self, gamma=10.0, dt=0.001):
        self.gamma = gamma  # Growth rate (instability factor)
        self.dt = dt
        self.state = np.array([0.05, 0.0]) # z (m), v (m/s)
        self.max_z = 1.0 # Wall limit
        
    def reset(self):
        self.state = np.array([0.05, 0.0]) # Start with 5cm offset
        return self.state

    def step(self, u_volts):
        z, v = self.state
        
        # Physics Constants
        mass_factor = 50.0 # Inertia proxy
        
        # Equations of Motion (Unstable)
        # acceleration = (instability force) + (control force)
        acc = (self.gamma**2 * z) + (u_volts * mass_factor)
        
        # Euler Integration
        v_new = v + acc * self.dt
        z_new = z + v * self.dt
        
        # Add Process Noise (Plasma Turbulence)
        z_new += np.random.normal(0, 0.0001)
        
        self.state = np.array([z_new, v_new])
        
        # Check collision
        done = bool(abs(z_new) > self.max_z)
        return self.state, done
