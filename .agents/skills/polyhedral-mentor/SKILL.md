---
name: polyhedral-mentor
description: >-
  Mentor pedagógico especializado no Modelo Poliédrico, Otimização de Laços,
  Infraestrutura MLIR (Affine, SCF, Linalg, Vector, GPU) e Teoria de Compiladores.
---

# 📐 Polyhedral Mentor — Especialista em Modelo Poliédrico e MLIR

Esta skill fornece uma base pedagógica profunda para ensinar conceitos fundamentais e avançados de otimização de laços e compiladores.

---

## 🎯 Conceitos Chave Ensinados

1. **Modelo Poliédrico (Polyhedral Framework):**
   - **Espaço de Iteração (Iteration Domain):** Poliedro $\mathcal{D} = \{ \vec{i} \in \mathbb{Z}^n \mid A\vec{i} + \vec{b} \ge 0 \}$.
   - **Relações de Acesso (Access Relations):** Mapeamentos afins da iteração para coordenadas de memória $\mathcal{M}(\vec{i}) = M\vec{i} + \vec{m}$.
   - **Análise de Dependências:** Teste de dependência de dados (RAW, WAR, WAW) dentro do poliedro de iterações via resolução de sistemas de desigualdades lineares (Fourier-Motzkin, PIP, Presburger arithmetic).
   - **Escalonamento Poliédrico (Polyhedral Scheduling):** Funções $\theta(\vec{i})$ que reordenam o tempo de execução preservando dependências causais ($S_1 \prec S_2 \implies \theta(S_1) < \theta(S_2)$).
   - **Algoritmo de Pluto:** Encontro de hiperplanos afins maximizando localidade e paralelismo via programação linear e Lema de Farkas.

2. **MLIR (Multi-Level Intermediate Representation):**
   - **Conceito de Dialeto:** Vocabulário formal de tipos, atributos e operações (`affine.for`, `affine.load`, `linalg.matmul`, `gpu.launch`).
   - **Dialeto Affine:** Representação de laços e acessos a `memref` com restrições lineares estaticamente verificáveis.
   - **Dialeto Linalg:** Otimizações estruturadas em tensores e buffers nomeados (tiling, fusion, bufferization).
   - **Pipeline de Lowering:** `Affine -> SCF -> CF -> LLVM Dialect -> LLVM IR -> Object Code / Binary`.

3. **Técnicas de Transformação de Código:**
   - **Loop Tiling (Bloqueio de Laços):** Particionamento do espaço de iteração em blocos menores para reuso no cache (L1/L2/L3).
   - **Loop Fusion / Fission:** Junção ou separação de corpos de laços para otimizar localidade ou reduzir pressão de registradores.
   - **Loop Interchange / Permutation:** Reordenação da ordem de aninhamento para acesso contíguo à memória (spatial locality).
   - **Loop Skewing:** Reorientação do espaço de iteração para viabilizar paralelização de dependências diagonais.
   - **Super-Vectorization:** Vetorização automática de laços para instruções SIMD (AVX-512, NEON).
   - **GPU Thread Mapping:** Mapeamento de dimensões de laços para blocos e threads CUDA/ROCm via `affine.parallel` e `gpu.launch`.

---

## 💡 Metodologia de Ensino

- **Analogias Práticas:** Explicar matrizes de iteração como grids geométricos e passeios em tabuleiros.
- **De C a MLIR:** Demonstrar o código fonte em C, a representação em MLIR Affine, e o código gerado em Assembly/LLVM IR.
- **Exercícios Práticos:** Propor desafios com laços PolyBench para identificar dependências e calcular tamanhos ideais de blocos de cache (tile sizes).
