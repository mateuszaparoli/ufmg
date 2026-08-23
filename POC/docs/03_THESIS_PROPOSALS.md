# 🎯 Propostas de TCC em Compiladores & HPC (UFMG / DCC)

Este documento detalha **6 propostas completas de Trabalho de Conclusão de Curso (TCC / Monografia)** utilizando a infraestrutura **Kiriko** e a suíte **PolyBench-MLIR** desenvolvidas no Departamento de Ciência da Computação da UFMG (DCC/UFMG) e no Laboratório de Compiladores (LaC).

---

## 🧭 Sumário Comparativo das Propostas

| ID | Título da Proposta | Área Principal | Complexidade | Potencial de Publicação | Ferramentas Chave |
| :-: | :--- | :--- | :---: | :---: | :--- |
| **P1** | **Kiriko-Tune:** Autotuning Inteligente de Pipelines MLIR via Otimização Bayesiana | Autotuning / ML + Compiladores | Média-Alta | ⭐⭐⭐⭐⭐ (CGO / CC / SBLP) | MLIR, Python, Scikit-Optimize, Optuna, Perf |
| **P2** | **PolyBench-GPU:** Otimização Poliédrica Automática para GPUs via Dialeto MLIR GPU | Computação Heterogênea / GPUs | Alta | ⭐⭐⭐⭐⭐ (PACT / WSCAD / CGO) | MLIR GPU/NVVM Dialects, CUDA, Polly-ACC |
| **P3** | **PolyBench-Linalg:** Estudo Comparativo entre Transformações Estruturadas (Linalg) e Poliédricas (Affine) | Engenharia de Compiladores | Média | ⭐⭐⭐⭐ (CC / SBLP / ERAD) | MLIR Linalg, Affine, LLVM 20 |
| **P4** | **Green-Kiriko:** Otimização Multidimensional de Consumo Energético (Joules) e EDP | Green HPC / Sustentabilidade | Média | ⭐⭐⭐⭐ (WSCAD / ERAD / ISPASS) | Intel RAPL, Linux Perf, MLIR, Python |
| **P5** | **MLIR-PolyFuzz:** Teste Diferencial e Diagnóstico de Corretude em Passes MLIR Affine | Verificação de Software / Compiladores | Alta | ⭐⭐⭐⭐⭐ (PLDI / CGO / SBES) | Fuzzing, Z3/SMT, MLIR Passes, C++ |
| **P6** | **Kiriko-Spatial:** Co-Design e Síntese de Hardware de Kernels PolyBench via CIRCT/SODA-OPT | Arquitetura de Computadores / HLS | Muito Alta | ⭐⭐⭐⭐⭐ (FCCM / FPGA / LATW) | SODA-OPT, CIRCT, Verilog, MLIR |

---

---

# 🚀 PROPOSTA 1: Kiriko-Tune — Autotuning Inteligente de Pipelines e Hiperparâmetros no MLIR

### 📌 Resumo da Proposta
No relatório técnico LaC 02/2026, os experimentos com MLIR utilizaram parâmetros estáticos fixos (`tile-size=32`, `unroll-factor=4`, ordem de passes invariável). Essa rigidez fez com que o MLIR tivesse desempenho inferior ao Polly e Clang -O3 em várias categorias (ex: no `gemm`, o MLIR atingiu 0.97× enquanto Polly obteve 26.98×).  
O **Kiriko-Tune** propõe a criação de uma camada de **Autotuning Inteligente** acoplada ao Kiriko, explorando o espaço combinatório de:
1. *Tile sizes* multidimensionais ($T_i, T_j, T_k \in \{4, 8, 16, 32, 64, 128, 256, 512\}$).
2. Fatores de *loop unrolling* e *vector register widths* (AVX2/AVX-512).
3. Habilitação seletiva e permutação da ordem de passes afins (`-affine-loop-fusion`, `-affine-scalrep`, `-affine-loop-coalescing`).
4. Algoritmos de busca: Otimização Bayesiana com Processos Gaussianos (GP), Algoritmos Genéticos (GA) e Busca por Árvore de Monte Carlo (MCTS).

### 🔬 Questões de Pesquisa (Research Questions)
- **$RQ_1$:** Qual é o ganho de desempenho real que o MLIR Affine pode atingir quando o tamanho de bloco e o fator de vetorização são ajustados para a hierarquia de memória do processador alvo?
- **$RQ_2$:** Como a ordem dos passes de otimização afim afeta a qualidade do código gerado e o tempo de compilação?
- **$RQ_3$:** A Otimização Bayesiana consegue convergir para configurações competitivas com o Polly com menos de 50 avaliações por kernel?

### 🛠️ Metodologia & Arquitetura Técnica
1. **Espaço de Busca Configurável:** Criar um gerador de pipelines dinâmicos em Python que injeta parâmetros no `mlir-opt`.
2. **Motor de Otimização:** Integrar frameworks de otimização de hiperparâmetros (ex: `Optuna` ou `scikit-optimize`).
3. **Loop de Feedback Fechado:** O Kiriko compila o kernel, executa sob isolamento térmico, mede o tempo via driver PolyBench, e alimenta a função objetivo do autotuner.
4. **Avaliação Cruzada:** Executar em processadores Intel (Xeon / Core i7) e AMD (EPYC / Ryzen) para demonstrar a adaptabilidade do compilador.

### 📅 Cronograma & Entregáveis
- **Mês 1-2:** Revisão bibliográfica sobre autotuning poliédrico (Wu et al. 2022, Sreenivasan et al. 2019) e arquitetura MLIR.
- **Mês 3-4:** Implementação do módulo `kiriko_tune.py` e parametrização do pipeline MLIR.
- **Mês 5-6:** Execução dos experimentos com todos os 30 benchmarks em 2 microarquiteturas de CPU.
- **Mês 7-8:** Análise de dados, gráficos de convergência, escrita da monografia e submissão de artigo para conferência (ex: SBLP ou CGO).

---

---

# 🚀 PROPOSTA 2: PolyBench-GPU — Otimização Poliédrica para Aceleradores Heterogêneos via Dialeto MLIR GPU

### 📌 Resumo da Proposta
A aceleração de kernels computacionais em GPUs é o padrão em inteligência artificial e simulação científica. Enquanto o Polly possui suporte a GPU via Polly-ACC e o Pluto possui o Pluto-CUDA, o MLIR possui uma infraestrutura moderna de dialetos (`gpu`, `nvvm`, `rocdl`, `spirv`).  
Esta proposta consiste em:
1. Desenvolver o pipeline de lowering automático do **PolyBench-MLIR Affine para o dialeto GPU do MLIR** (`affine.parallel` $\to$ `gpu.launch_bounds` $\to$ `gpu.launch` $\to$ PTX / NVVM / LLVM).
2. Estender o Kiriko para suportar a compilação cruzada e execução em GPUs NVIDIA (CUDA) e AMD (ROCm).
3. Conduzir um estudo comparativo pioneiro entre: **MLIR GPU Dialect vs. Polly-ACC vs. Pluto-CUDA vs. Implementações Manuais em CUDA**.

### 🔬 Questões de Pesquisa
- **$RQ_1$:** As transformações poliédricas no MLIR Affine conseguem gerar padrões de acesso coalescido à memória global e uso eficiente de memória compartilhada (*Shared Memory*) na GPU?
- **$RQ_2$:** Qual é o overhead de lançamento de kernel e cópia de memória Host-to-Device introduzido pelo pipeline do MLIR em comparação com o runtime nativo do CUDA?
- **$RQ_3$:** Quais categorias de laços (estênceis vs. álgebra linear) se beneficiam mais da compilação automática para GPU?

### 🛠️ Metodologia & Arquitetura Técnica
1. **Passes MLIR de Mapeamento:** Utilizar e aprimorar passes como `--affine-parallelize`, `--affine-loop-tile`, `--convert-affine-to-gpu` e `--gpu-kernel-outlining`.
2. **Extensão do Driver C:** Adaptar os drivers pré-processados (`<kernel>_prep_mlir.c`) para gerenciar alocação de memória na GPU (`cudaMalloc`, `cudaMemcpy`) e temporização precisa com CUDA Events.
3. **Métricas de Profiling:** Integrar medições via `nvidia-smi` e `nvprof` / `NCU` (NVIDIA Nsight Compute) para analisar *warp occupancy*, *memory throughput* e *register spill*.

---

---

# 🚀 PROPOSTA 3: PolyBench-Linalg — Transformações Estruturadas (Linalg) vs. Abstração Poliédrica (Affine)

### 📌 Resumo da Proposta
A comunidade de compiladores de Machine Learning (Google IREE, Torch-MLIR, StableHLO) tem priorizado o dialeto **Linalg** em detrimento do dialeto **Affine** para transformações estruturadas de tensores.  
Esta proposta propõe:
1. Criar a suíte **PolyBench-Linalg**, reescrevendo os kernels do PolyBench usando operações estruturadas nomeadas (`linalg.matmul`, `linalg.conv_2d`, etc.) e operações genéricas (`linalg.generic`).
2. Avaliar as estratégias de *tiling*, *fusion* e *bufferization* do Linalg contra as otimizações do dialeto Affine implementadas no Kiriko.
3. Avaliar tempo de compilação, manutenibilidade das representações intermediárias e desempenho do binário gerado.

### 🔬 Questões de Pesquisa
- **$RQ_1$:** As transformações baseadas em *pattern-matching* e *named ops* no dialeto Linalg conseguem atingir a mesma qualidade de vetorização e localidade de cache que a análise de dependência poliédrica estrita do Affine?
- **$RQ_2$:** Como o custo de compilação (tempo de execução do `mlir-opt`) escala entre o Linalg e o Affine à medida que o aninhamento de laços aumenta?

---

---

# 🚀 PROPOSTA 4: Green-Kiriko — Otimização Multidimensional de Consumo de Energia e Eficiência em HPC

### 📌 Resumo da Proposta
A eficiência energética tornou-se a restrição primária em supercomputadores e datacenters. O relatório técnico do LaC limitou-se ao tempo de execução e contadores básicos de Perf.  
O **Green-Kiriko** expande o framework para medir diretamente:
1. **Consumo Energético Total (Joules)** via interface Intel/AMD **RAPL** (*Running Average Power Limit*).
2. **Energy-Delay Product ($EDP = \text{Energy} \times \text{Delay}$)** e **Energy-Delay-Squared ($ED^2P$)**.
3. **Construção Automática do Modelo Roofline Dinâmico** (FLOPS/Byte vs. GFLOPS/s) correlacionando intensidade aritmética e otimizações poliédricas.

### 🔬 Questões de Pesquisa
- **$RQ_1$:** As configurações de compilação que atingem o menor tempo de execução (menor latência) são necessariamente as que consomem menos energia total?
- **$RQ_2$:** Como o *loop unrolling* agressivo e a super-vetorização afetam a potência instantânea (Watts) e a dissipação térmica em CPUs multinúcleo?

---

---

# 🚀 PROPOSTA 5: MLIR-PolyFuzz — Teste Diferencial e Diagnóstico de Corretude em Passes Poliédricos

### 📌 Resumo da Proposta
Durante a construção do Kiriko, o benchmark `symm` foi excluído por falhas de compilação e o kernel `reg_detect` exigiu a remoção manual do pass `-affine-loop-fusion`.  
Esta proposta propõe criar o **MLIR-PolyFuzz**:
1. Um framework de **Teste Metamórfico e Fuzzing Diferencial** para laços afins em MLIR.
2. Geração automática de variações de laços e verificação formal/diferencial de equivalência semântica entre o código pré e pós-otimização.
3. Isolamento automático da causa raiz do bug do `symm` e envio de correções/patches para o repositório oficial do LLVM/MLIR.

---

---

# 🚀 PROPOSTA 6: Kiriko-Spatial — Síntese de Aceleradores de Hardware de Alto Desempenho (CGRAs / SODA-OPT / CIRCT)

### 📌 Resumo da Proposta
O dialeto Affine do MLIR é o ponto de partida ideal para Síntese de Alto Nível (HLS) e geração de aceleradores espaciais (CGRAs, FPGAs) via projetos como SODA-OPT (Agostini et al. 2022) e CIRCT.  
Esta proposta visa:
1. Integrar o PolyBench-MLIR em fluxos de HLS para sintetizar blocos de hardware customizados a partir dos laços otimizados.
2. Comparar métricas de área (LUTs, FFs, DSPs), frequência de clock máxima e throughput entre diferentes pipelines de otimização de laços.

---

## 🏆 Recomendação do Jarvis: Qual Escolher?

Para maximizar o impacto acadêmico, a viabilidade de execução no prazo do TCC e a continuidade da parceria com o Laboratório de Compiladores (LaC/UFMG) e Cadence:

> [!IMPORTANT]
> **Recomendação Principal:** **Proposta 1 (Kiriko-Tune)** ou **Proposta 2 (PolyBench-GPU)**.
> - A **Proposta 1 (Kiriko-Tune)** tem risco controlado, implementação direta sobre o código existente do Kiriko em Python/MLIR, e resolve a principal fraqueza apontada no artigo LaC (o desempenho inferior do MLIR devido a hiperparâmetros fixos).
> - A **Proposta 2 (PolyBench-GPU)** tem o maior potencial de publicação internacional de alto impacto (CGO / PACT) por levar o PolyBench-MLIR para aceleradores GPU.
