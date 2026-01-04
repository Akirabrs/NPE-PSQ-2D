
# ⚛️ NPE-PSQ-2D: AION-CORE Ecosystem v4.5

<div align="center">
  <img src="assets/nmpc_stabilization.gif" width="600">
  <p><i>Visualização do controle preditivo estabilizando a posição vertical do plasma (VDE).</i></p>
</div>

---

## 🏗️ Arquitetura: Interface Bridge (PI-POD)
Este repositório integra a física do **NPE-PSQ** (44 variáveis) com o controle de tempo real do **AION-CORE** via uma camada de redução inteligente.

### 🧠 Lógica de Derivação Física (A Sua Ideia)
O sistema não apenas reduz dados estatisticamente, mas utiliza **Leis Constitutivas**:
- **Estados Fundamentais**: Processamento direto de $z, r, Ip, ne, Te$.
- **Estados Derivados**: Variáveis como $\beta_n$ e $B_{tor}$ são derivadas via lógica física (Ex: $B_{tor} = f(Ip)$ via Lei de Ampère).
- **Vantagem**: Garante consistência física e resposta em hardware em menos de **1µs**.

---

## 📂 Organização do Repositório
- `/AION_CORE/core`: Implementação do PI-POD Reducer.
- `/AION_CORE/docs`: Dicionário de estados (44 variáveis).
- `/assets`: Recursos visuais e animações de simulação.

## 🛡️ Transparência
Projeto desenvolvido por **Guilherme Brasil de Souza**. Assistência técnica de LLMs utilizada para otimização de código sob supervisão científica original.
