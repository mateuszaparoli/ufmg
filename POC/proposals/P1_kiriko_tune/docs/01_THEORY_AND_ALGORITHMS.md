# 📘 Kiriko-Tune: Fundamentação Teórica & Algoritmos de Autotuning

> **Autores:** Jarvis & Pesquisadores do LaC/UFMG  
> **Tema:** Autotuning de Parâmetros e Ordem de Passes no Dialeto MLIR Affine  

---

## 1. A Natureza do Espaço de Otimização de Compiladores

Otimizar um compilador para uma arquitetura específica não é um problema linear ou convexo. O espaço de busca $\mathcal{S}$ de configurações de compilação apresenta:
1. **Não-linearidade extrema:** Pequenas variações no tamanho de bloco (*tile size*) podem causar saltos abruptos de desempenho devido a efeitos de *cache associativity conflicts* e *aliasing*.
2. **Interações Não-Ortonormais entre Passes (Phase Ordering Problem):** Aplicar vetorização antes ou depois do desenrolamento de laço altera drasticamente a estrutura de instruções gerada pelo LLVM backend.
3. **Alto Custo de Amostragem:** Cada avaliação requer compilar com `mlir-opt`, traduzir para LLVM IR, compilar com `llc`/`clang` e executar repetidas vezes para mitigar ruído temporal.

---

## 2. Otimização Bayesiana com Processos Gaussianos & TPE

A **Otimização Bayesiana (BO)** trata a função objetivo de desempenho $f(\vec{x})$ (tempo de execução ou speedup) como uma função caixa-preta desconhecida e modela sua distribuição a posteriori usando um modelo substituto (*surrogate model*):

$$P(f \mid \mathcal{D}_{1:t}) \sim \mathcal{GP}(\mu(\vec{x}), k(\vec{x}, \vec{x}'))$$

### 2.1. Função de Aquisição: Expected Improvement (EI)
A próxima configuração $\vec{x}_{t+1}$ a ser avaliada no compilador é escolhida maximizando o ganho esperado em relação ao melhor valor encontrado até o momento $y^*$:

$$\text{EI}(\vec{x}) = \mathbb{E}\left[ \max(0, f(\vec{x}) - y^*) \right]$$

O algoritmo balanceia naturalmente:
- **Explotação (*Exploitation*):** Amostrar em regiões onde a média predita $\mu(\vec{x})$ é alta.
- **Exploração (*Exploration*):** Amostrar em regiões com alta incerteza $\sigma(\vec{x})$ (pouco visitadas).

### 2.2. Tree-structured Parzen Estimator (TPE)
Para espaços discretos/categóricos (como escolhas de passes e flags booleanas), o TPE modela $P(\vec{x} \mid y)$ diretamente dividindo as observações em dois grupos:
$$P(\vec{x} \mid y) = \begin{cases} \ell(\vec{x}) & \text{se } y > y^* \\ g(\vec{x}) & \text{se } y \le y^* \end{cases}$$
Maximizando a razão $\frac{\ell(\vec{x})}{g(\vec{x})}$.

---

## 3. Algoritmo Genético para Permutação de Passes (Phase Ordering)

Para o problema da ordem de passes afins, os cromossomos são representados como permutações de passes:
$$\mathcal{C} = \langle p_{\pi_1}, p_{\pi_2}, \dots, p_{\pi_k} \rangle, \quad p_i \in \{ \text{tile}, \text{fusion}, \text{scalrep}, \text{unroll}, \text{vectorize} \}$$

- **Operador de Cruzamento (PMX / Uniform Crossover):** Combina blocos de passes preservando a unicidade.
- **Operador de Mutação:** Troca a posição de dois passes adjacentes (*swap*) ou altera valores numéricos de genes de parâmetros (*tile sizes*, *unroll factor*).
- **Elitismo:** Preserva as 2 melhores configurações entre gerações consecutivas.
