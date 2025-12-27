# ============================================================================
# ⚛️ NPE-PSQ-2D/3D v3.4: TUNED EDITION (NMPC Fix + Citation)
# ============================================================================
# Status: PUBLICATION READY
# Author: Guilherme Brasil de Souza (Akira) | ORCID: 0009-0000-4750-6365
# DOI: 10.5281/zenodo.18064672
# ============================================================================

import numpy as np
import logging
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, List
from enum import Enum
from datetime import datetime
from scipy.optimize import minimize
from scipy.linalg import solve_continuous_are
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

class DimensionType(Enum): DIM1D = "1D"; DIM2D = "2D"
class ControllerType(Enum): NMPC = "NMPC"; LQR = "LQR"; PID = "PID"
class SimulationStatus(Enum): SUCCESS = "SUCCESS"; VDE = "VDE"; CQ = "CQ"; NUMERICAL = "NUMERICAL"

@dataclass
class PhysicalConfig:
    dimension: DimensionType = DimensionType.DIM2D
    gamma_z: float = 25.0; gamma_r: float = 15.0; k_coupling: float = 0.5
    Ip_nominal: float = 1.0e6
    M_plasma_z: float = 1.0; M_plasma_r: float = 0.8
    k_eddy_z: float = 3.0e6; k_eddy_r: float = 2.5e6; lambda_eddy: float = 0.4
    B_control_z: float = 60.0; B_control_r: float = 40.0
    dt: float = 0.0005; noise_level: float = 0.01
    vde_threshold_z: float = 1.0; vde_threshold_r: float = 0.8
    z_cq_trigger: float = 0.25; Ip_cq_rate: float = 2.0e7
    def validate(self):
        if self.dt <= 0: raise ValueError("dt must be > 0")

class TokamakPresets:
    @staticmethod
    def ITER_Scale() -> PhysicalConfig:
        return PhysicalConfig(
            dimension=DimensionType.DIM2D, gamma_z=10.0, Ip_nominal=15.0e6,
            M_plasma_z=100.0, k_eddy_z=5.0e7, B_control_z=1000.0, vde_threshold_z=2.0
        )
    @staticmethod
    def SPARC_Scale() -> PhysicalConfig:
        return PhysicalConfig(
            dimension=DimensionType.DIM2D, gamma_z=50.0, Ip_nominal=8.7e6,
            M_plasma_z=20.0, B_control_z=500.0, dt=0.0001
        )

@dataclass
class StateVector:
    z: float; v_z: float; Ip: float; r: float = 0.0; v_r: float = 0.0
    def to_array(self) -> np.ndarray: return np.array([self.z, self.v_z, self.Ip, self.r, self.v_r])
    @staticmethod
    def from_array(arr: np.ndarray) -> 'StateVector': return StateVector(z=arr[0], v_z=arr[1], Ip=arr[2], r=arr[3], v_r=arr[4])

@dataclass
class SimulationMetrics:
    timestamp: str; trace_id: str; controller: str; status: str
    duration: float; steps: int; computational_time_ms: float
    max_z: float; mean_u: float; constraint_violations: int
    final_state: Dict[str, float]

@dataclass
class SimulationResult: metrics: SimulationMetrics; history: Dict[str, List[float]]

class TokamakPlant:
    def __init__(self, config: PhysicalConfig):
        self.config = config; self.config.validate()
        self.rng = np.random.RandomState(); self.reset()
    def set_seed(self, seed: int): self.rng = np.random.RandomState(seed)
    def reset(self) -> StateVector:
        self.time = 0.0; self.steps = 0
        self.state = StateVector(z=0.02, v_z=0.0, Ip=self.config.Ip_nominal, r=0.01, v_r=0.0)
        return self.state
    def _derivatives(self, s: StateVector, u_z: float, u_r: float) -> np.ndarray:
        F_mag_z = self.config.gamma_z**2 * s.z * (s.Ip / self.config.Ip_nominal)
        F_eddy_z = -self.config.k_eddy_z * s.z * np.exp(-abs(s.z)/self.config.lambda_eddy)
        F_cpl_z = -self.config.k_coupling * self.config.gamma_r**2 * s.r * s.z if self.config.dimension == DimensionType.DIM2D else 0.0
        acc_z = (F_mag_z + F_eddy_z + F_cpl_z + self.config.B_control_z * u_z) / self.config.M_plasma_z
        acc_r = 0.0
        if self.config.dimension == DimensionType.DIM2D:
            F_mag_r = self.config.gamma_r**2 * s.r
            F_eddy_r = -self.config.k_eddy_r * s.r * np.exp(-abs(s.r)/self.config.lambda_eddy)
            acc_r = (F_mag_r + F_eddy_r + self.config.B_control_r * u_r) / self.config.M_plasma_r
        dIp = -self.config.Ip_cq_rate if abs(s.z) > self.config.z_cq_trigger else 0.0
        return np.array([s.v_z, acc_z, dIp, s.v_r, acc_r])
    def step(self, u_z: float, u_r: float = 0.0) -> Tuple[StateVector, bool, str]:
        dt = self.config.dt; y0 = self.state.to_array(); s0 = self.state
        k1 = self._derivatives(s0, u_z, u_r)
        y_k2 = y0 + 0.5 * dt * k1; k2 = self._derivatives(StateVector.from_array(y_k2), u_z, u_r)
        y_k3 = y0 + 0.5 * dt * k2; k3 = self._derivatives(StateVector.from_array(y_k3), u_z, u_r)
        y_k4 = y0 + dt * k3; k4 = self._derivatives(StateVector.from_array(y_k4), u_z, u_r)
        y_next = y0 + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        noise_std = self.config.noise_level / np.sqrt(dt)
        noise_z = self.rng.normal(0, noise_std) / self.config.M_plasma_z
        y_next[1] += noise_z * dt
        self.state = StateVector.from_array(y_next); self.time += dt; self.steps += 1
        status = "RUNNING"; done = False
        if abs(self.state.z) > self.config.vde_threshold_z: status = "VDE"; done = True
        elif self.state.Ip < self.config.Ip_nominal * 0.1: status = "CQ"; done = True
        return self.state, done, status

class RealLQRController:
    def __init__(self, config: PhysicalConfig):
        A = np.array([[0, 1], [config.gamma_z**2, 0]])
        B = np.array([[0], [config.B_control_z / config.M_plasma_z]])
        Q = np.diag([1000, 1]); R = np.array([[0.1]])
        try: P = solve_continuous_are(A, B, Q, R); self.K = np.linalg.inv(R) @ B.T @ P
        except: self.K = np.zeros((1, 2))
    def compute(self, s: StateVector) -> float: return float((-self.K @ np.array([s.z, s.v_z]))[0])

class NMPCController:
    def __init__(self, plant: TokamakPlant, horizon: int = 15):
        self.plant = plant; self.H = horizon; self.last_u = np.zeros(horizon); self.cfg = plant.config 
    def _predict_cost(self, u_seq, s0: StateVector):
        cost = 0.0; z, v_z = s0.z, s0.v_z; dt = self.cfg.dt
        # --- TUNING FIX: Reduced control penalty (W_u) to encourage action ---
        W_z = 5000.0; W_u = 0.001 
        for u in u_seq:
            F_mag = self.cfg.gamma_z**2 * z * (s0.Ip / self.cfg.Ip_nominal)
            F_eddy = -self.cfg.k_eddy_z * z * np.exp(-abs(z)/self.cfg.lambda_eddy)
            acc_z = (F_mag + F_eddy + self.cfg.B_control_z * u) / self.cfg.M_plasma_z
            v_z += acc_z * dt; z += v_z * dt
            cost += W_z * z**2 + W_u * u**2
            if abs(z) > self.cfg.vde_threshold_z: cost += 1e5 * (abs(z) - self.cfg.vde_threshold_z)**2
        return cost
    def compute(self, s: StateVector) -> float:
        bnds = [(-1.0, 1.0) for _ in range(self.H)]
        # --- TUNING FIX: Increased maxiter for convergence ---
        res = minimize(self._predict_cost, self.last_u, args=(s,), method='SLSQP', bounds=bnds, tol=1e-3, options={'maxiter': 50, 'disp': False})
        if res.success: self.last_u = np.roll(res.x, -1); self.last_u[-1] = 0.0; return res.x[0]
        return 0.0

class VisualizationUtils:
    @staticmethod
    def plot_results(result: SimulationResult, filename: str):
        hist = result.history; t = hist['time']
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
        ax1.plot(t, np.array(hist['z'])*1000, 'b-', label='Plasma Z')
        ax1.axhline(result.metrics.max_z*1000, color='r', linestyle='--', alpha=0.3)
        ax1.set_ylabel('Z (mm)'); ax1.grid(True, alpha=0.3); ax1.legend(); ax1.set_title(f"Controller: {result.metrics.controller} | Status: {result.metrics.status}")
        ax2.plot(t, hist['u_z'], 'k-', alpha=0.6, label='Control (Norm)'); ax2.set_ylabel('U'); ax2.set_xlabel('Time (s)'); ax2.grid(True)
        plt.tight_layout(); plt.savefig(filename, dpi=150); plt.close(); logger.info(f"📈 Plot saved: {filename}")

class Simulator:
    def __init__(self, config: PhysicalConfig): self.config = config
    def run(self, controller_type: ControllerType, duration: float = 0.5, seed: int = 42) -> SimulationResult:
        start_t = time.perf_counter(); plant = TokamakPlant(self.config); plant.set_seed(seed); state = plant.reset()
        if controller_type == ControllerType.LQR: ctrl = RealLQRController(self.config)
        elif controller_type == ControllerType.NMPC: ctrl = NMPCController(plant)
        else: raise NotImplementedError
        hist = {'time': [], 'z': [], 'u_z': []}; violations = 0
        for _ in range(int(duration / self.config.dt)):
            u_val = ctrl.compute(state)
            u_norm = np.clip(u_val if controller_type == ControllerType.NMPC else u_val/self.config.B_control_z, -1.0, 1.0)
            state, done, status = plant.step(u_norm)
            hist['time'].append(plant.time); hist['z'].append(state.z); hist['u_z'].append(u_norm)
            if abs(state.z) > self.config.vde_threshold_z: violations += 1
            if done: break
        cpu_time = (time.perf_counter() - start_t) * 1000
        metrics = SimulationMetrics(datetime.now().isoformat(), str(uuid.uuid4())[:8], controller_type.value, status, plant.time, plant.steps, cpu_time, max(np.abs(hist['z'])), np.mean(np.abs(hist['u_z'])), violations, asdict(state))
        return SimulationResult(metrics, hist)