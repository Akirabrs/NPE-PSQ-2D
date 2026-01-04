<div align="center">

# ⚛️ NPE-PSQ-2D: Tokamak Physics Engine & AION-CORE Ecosystem v4.5

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18136444.svg)](https://doi.org/10.5281/zenodo.18136444)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-HIL--Ready-success.svg)](https://github.com/Akirabrs/NPE-PSQ-2D)

**Simulação de Alta Fidelidade e Controle Preditivo para Estabilização de Plasma**

[🚀 Quick Start](#-quick-start) • [🏗️ Arquitetura](#-arquitetura-do-sistema) • [📊 Resultados](#-resultados) • [📄 Licença](#-licença)

![Plasma Stabilization](https://raw.githubusercontent.com/Akirabrs/NPE-PSQ-2D/main/assets/nmpc_stabilization.gif)
*Estabilização de Vertical Displacement Events (VDE) com controle NMPC e envelope de incerteza.*

</div>

---

## 🏗️ Arquitetura do Sistema (Ecossistema Integrado)

O projeto opera como um ecossistema trifásico, conectando a física teórica ao hardware em tempo real:

1.  **NPE-PSQ-2D (Física)**: Simulador de 44 variáveis de estado que modela a dinâmica MHD do plasma.
2.  **AION-POD-REDUCER (Ponte)**: Camada de interface que utiliza **Lógica de Derivação Física** para reduzir a complexidade de 44 para 12 estados fundamentais.
3.  **AION-CORE (Controle)**: Kernel de controle projetado para hardware (Edge AI/FPGA), tomando decisões em menos de 1µs.



## 🧠 Lógica de Derivação Física (PI-POD)
Diferente de reduções puramente matemáticas, o AION utiliza relações constitutivas:
- **Estados Fundamentais**: Medição direta de $z, r, Ip, n_e, T_e$.
- **Estados Derivados**: Variáveis como $\beta_n$, $W_{mhd}$ e $B_{tor}$ são calculadas via leis físicas (Lei de Ampère, Gases Ideais), garantindo consistência e velocidade.

---

## 🚀 Quick Start

### Estrutura de Pastas
```text
/AION_CORE/
├── core/           # Redutor POD e Kernel de Controle
├── ai_models/      # Modelos treinados (GhostHunter)
├── forensics/      # Injetor de dados Reais (JET/DIII-D)
└── docs/           # Dicionário de Variáveis
