# NPE-PSQ-2D: AION-CORE Ecosystem v4.5

![Stabilization](https://raw.githubusercontent.com/Akirabrs/NPE-PSQ-2D/main/assets/nmpc_stabilization.gif)

## Arquitetura Hibrida
O sistema conecta a Simulacao Fisica (NPE-PSQ) ao Hardware de Controle (AION-CORE).

ESTRUTURA:
1. NPE-PSQ (Fisica) -> Gera 44 Variaveis
2. Ponte PI-POD -> Reduz para 12 Variaveis
3. Kernel AION -> Calcula Estabilidade
4. Hardware -> Aplica Correcao

## Transparencia
Projeto de Guilherme Brasil de Souza.
