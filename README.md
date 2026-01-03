# ⚛️ NPE-PSQ-2D: Tokamak Physics Engine v4.0
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18065774.svg)](https://doi.org/10.5281/zenodo.18065774)

![Plasma Stabilization](nmpc_stabilization.gif)

## 🎯 Sobre o Projeto
O **NPE-PSQ** é um simulador de alta fidelidade para dinâmica vertical de plasma, focado em **VDE (Vertical Displacement Events)**.

## 🚀 Especificações
* **Controlador:** Tube-based MPC (NMPC + LQR).
* **Integrador:** Runge-Kutta 4.
* **Física:** Ruído de Wiener e dinâmica não-linear.

## 📄 Documentação
Veja os detalhes matemáticos em [`paper.md`](paper.md).

## ⚡ ATUALIZAÇÃO 2026: INTEGRAÇÃO AION-CORE
Este repositório agora inclui o ecossistema de controle **AION-CORE**, evoluindo a base NPE-PSQ para:
- Controle de Plasma 3D (44 variáveis de estado).
- Módulo de Injeção Forense para validação com dados reais (JET/DIII-D).
- Prontidão para Hardware-in-the-Loop (HIL).
