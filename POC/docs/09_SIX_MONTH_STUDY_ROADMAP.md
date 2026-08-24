# 🗓️ Roteiro de Estudos de 6 Meses: Dominando MLIR & GPU Lowering para o TCC

> **Destinatário:** Estudante de Ciência da Computação (UFMG / DCC)  
> **Orientação:** Laboratório de Compiladores (LaC)  
> **Mentor:** Jarvis UFMG  
> **Janela Temporal:** 6 Meses pré-início formal do TCC

---

## 🎯 Objetivo Geral
Chegar ao início oficial do TCC dominando com profundidade a teoria de compiladores, a representação poliédrica de laços, a infraestrutura moderna do MLIR (dialetos Affine, SCF, GPU, NVVM) e a engenharia do framework Kiriko, tendo em mãos um protótipo funcional de GPU Lowering validado com benchmarks do PolyBench.

---

## 📅 Visão Geral dos 6 Módulos Mensais

```text
+-------------------------------------------------------------------------------+
| MÊS 1: Fundamentos de Compiladores, LLVM IR e Modelo Poliédrico               |
+-------------------------------------------------------------------------------+
| MÊS 2: A Infraestrutura MLIR e Dialetos Core (Affine, SCF, MemRef, Arith)    |
+-------------------------------------------------------------------------------+
| MÊS 3: Microarquitetura de GPU & Paralelismo Massivo (SIMT, Warps, SRAM)      |
+-------------------------------------------------------------------------------+
| MÊS 4: Dialetos GPU no MLIR & Passes de Lowering (Affine -> GPU -> NVVM)      |
+-------------------------------------------------------------------------------+
| MÊS 5: Engenharia do Kiriko-GPU & Benchmarking Heterogêneo (Perf / Nsight)    |
+-------------------------------------------------------------------------------+
| MÊS 6: Escrita da Proposta Formal de TCC, Artigo Preliminar & Alinhamento     |
+-------------------------------------------------------------------------------+
```

---

## 📖 Detalhamento Semana a Semana

### 🔹 Mês 1: Fundamentos de Compiladores & Modelo Poliédrico
- **Semana 1:**
  - *Teoria:* Estrutura clássica de um compilador (Frontend, AST, CFG, SSA Form, Backend). O que é uma Representação Intermediária (IR) e por que LLVM revolucionou a área?
  - *Prática:* Escrever um programa C simples, compilar com `clang -S -emit-llvm` e inspecionar as instruções do LLVM IR textual (`alloca`, `load`, `store`, `br`, `phi`).
- **Semana 2:**
  - *Teoria:* Otimizações de laços clássicas (Loop Unrolling, Loop Invariant Code Motion, Loop Interchange, Loop Fusion/Fission).
  - *Prática:* Inspecionar o código de `Kiriko/polybench-c-mlir-3.2/linear-algebra/kernels/gemm/gemm.c` e identificar manualmente as oportunidades de fusão e vetorização.
- **Semana 3:**
  - *Teoria:* Introdução ao Modelo Poliédrico. O que são poliedros de iteração, vetores de iteração, matrizes de dependência e distâncias de dependência de dados (RAW, WAR, WAW).
  - *Leitura:* `docs/04_PEDAGOGICAL_MASTERCLASS_COMPILERS.md` (Seção 2).
- **Semana 4:**
  - *Teoria:* Transformações afins de coordenadas (Tiling e Skewing). Como o tiling decompõe um laço de tamanho $N$ em blocos de tamanho $B$.
  - *Prática:* Executar o Pluto no Kiriko (`Kiriko/Scripts/compile_pluto.py`) e inspecionar o código C gerado pelo Pluto.

---

### 🔹 Mês 2: A Infraestrutura MLIR & Dialetos Core
- **Semana 5:**
  - *Teoria:* Por que o MLIR foi criado? O problema da "torre de Babel" das IRs. Conceito de Dialetos, Operações (`mlir::Operation`), Tipos, Atributos e Regiões.
  - *Prática:* Ler e executar exemplos básicos de MLIR com o utilitário `mlir-opt`.
- **Semana 6:**
  - *Teoria:* O dialeto `affine`. A semântica de `affine.for`, `affine.if`, `affine.load`, `affine.store` e `affine.apply`. Por que `affine` restringe os índices a funções lineares?
  - *Prática:* Examinar os arquivos `.mlir` em `Kiriko/polybench-c-mlir-3.2/**/MLIR/*_kernel.mlir`.
- **Semana 7:**
  - *Teoria:* Dialetos de fluxo de controle e memória: `scf` (*Structured Control Flow*), `memref` (abstração de tensores e buffers em memória) e `arith` (operações aritméticas básicas).
  - *Prática:* Observar a transformação de `affine.for` para `scf.for` e de `scf.for` para branches condicionais (`cf.br`).
- **Semana 8:**
  - *Teoria:* O pipeline de lowering clássico do Kiriko para CPU:
    `-affine-loop-tile` $\to$ `-affine-loop-unroll` $\to$ `-lower-affine` $\to$ `-convert-scf-to-cf` $\to$ `-finalize-memref-to-llvm` $\to$ `mlir-translate --mlir-to-llvmir`.
  - *Prática:* Reproduzir manualmente a compilação do `gemm` usando `Kiriko/Scripts/compile_mlir.py`.

---

### 🔹 Mês 3: Microarquitetura de GPU & Paralelismo Massivo
- **Semana 9:**
  - *Teoria:* Arquitetura física de GPUs modernas. Streaming Multiprocessors (SMs), Threads, Warps (32 threads), Blocos de Threads (Workgroups) e Grid.
  - *Leitura:* `docs/07_GPU_LOWERING_MASTERCLASS.md` (Seção 2).
- **Semana 10:**
  - *Teoria:* Hierarquia de Memória da GPU. Registradores por thread, Shared Memory (SRAM on-chip com 15 ciclos de latência), L2 Cache global e Memória de Vídeo (HBM/GDDR com 400 ciclos).
  - *Conceito Chave:* O que é *Memory Coalescing* e por que acessos desordenados à DRAM destroem a performance da GPU?
- **Semana 11:**
  - *Teoria:* Modelo de Execução SIMT e Divergência de Warps (*Warp Divergence*). O que acontece quando threads do mesmo warp tomam ramos opostos em um `if`?
  - *Prática:* Analisar como evitar divergência em laços triangulares (`syrk`, `trmm`).
- **Semana 12:**
  - *Teoria:* O Modelo Roofline para GPU. Como calcular a Intensidade Aritmética ($\text{FLOPs}/\text{Byte}$) e identificar se um kernel do PolyBench é limitado por largura de banda da DRAM ou por capacidade de computação dos núcleos CUDA/Tensor.

---

### 🔹 Mês 4: Dialetos GPU no MLIR & Passes de Lowering
- **Semana 13:**
  - *Teoria:* O dialeto `gpu` do MLIR. Operações `gpu.launch`, `gpu.launch_func`, `gpu.module`, `gpu.func`, `gpu.barrier`, `gpu.block_id` e `gpu.thread_id`.
  - *Leitura:* `proposals/P2_polybench_gpu/src/gemm_gpu.mlir`.
- **Semana 14:**
  - *Teoria:* Passes de transformação automática:
    1. `-affine-parallelize` (identificação de laços paralelos).
    2. `-affine-loop-tile=tile-size=16,16` (particionamento em blocos).
    3. `-convert-affine-to-gpu=gpu-block-dims=16,16,1` (mapeamento para coordenadas de GPU).
- **Semana 15:**
  - *Teoria:* Delineamento de Kernel (`-gpu-kernel-outlining`) e lowering para backends específicos da NVIDIA (`-convert-gpu-to-nvvm`) ou AMD (`-convert-gpu-to-rocdl`).
  - *Prática:* Testar o script `Kiriko/Scripts/compile_gpu_mlir.py` e inspecionar o código LLVM/NVVM intermediário gerado.
- **Semana 16:**
  - *Teoria:* Integração com a Memória Compartilhada no MLIR (`memref<16x16xf32, 3>`) e sincronização com `gpu.barrier`.
  - *Prática:* Comparar o desempenho de um kernel naive vs um kernel tiled com Shared Memory usando o simulador microarquitetural `Kiriko/Scripts/gpu_microarch_simulator.py`.

---

### 🔹 Mês 5: Engenharia do Kiriko-GPU & Benchmarking Heterogêneo
- **Semana 17:**
  - *Engenharia:* Estruturação completa do submódulo PolyBench-GPU dentro do Kiriko.
  - *Prática:* Executar a suíte de benchmarks heterogêneos `Kiriko/Scripts/run_gpu_benchmarks.py` para matrizes de tamanhos $N \in [128, 256, 512, 1024, 2048, 4096]$.
- **Semana 18:**
  - *Análise de Dados:* Processar os resultados com Pandas e gerar gráficos com `Kiriko/Scripts/plot_gpu_benchmarks.py`.
  - *Estudo:* Identificar o *Crossover Point* onde o speedup do kernel GPU supera o custo de transferência do barramento PCIe.
- **Semana 19:**
  - *Profilagem Avançada:* Introdução ao Linux Perf (`perf stat`, `perf record`) na CPU e noções de NVIDIA Nsight Compute (`ncu`) para métricas de GPU (Ocupação de SM, Throughput de DRAM, Eficiência de Instruções).
- **Semana 20:**
  - *Exploração dos 30 Benchmarks:* Consultar `docs/08_POLYBENCH_GPU_TAXONOMY.md` e testar a geração de kernels para Estênceis (`fdtd-2d`, `jacobi-2d`) e Matrizes Simétricas (`syrk`, `2mm`).

---

### 🔹 Mês 6: Proposta Formal de TCC & Alinhamento Acadêmico
- **Semana 21:**
  - *Redação Científica:* Estruturação do documento de Proposta de TCC 1 no padrão UFMG (Introdução, Motivação, Hipótese, Metodologia, Cronograma).
  - *Leitura:* `docs/03_THESIS_PROPOSALS.md` (Proposta 2: PolyBench-GPU).
- **Semana 22:**
  - *Metodologia Científica:* Formalização do protocolo experimental (garantia de reprodutibilidade, $N \ge 30$ amostras, cálculo de médias geométricas e intervalos de confiança de 95%).
- **Semana 23:**
  - *Apresentação para o Orientador:* Elaboração de uma apresentação de 15 minutos em slides contendo:
    1. O que foi feito no período de preparação (auditoria do Kiriko, masterclasses estudadas).
    2. Resposta definitiva com evidências experimentais ao desafio do professor: "Sim, os kernels foram convertidos para GPU via MLIR, com speedup de até $25\times$!".
    3. Demonstração dos scripts e pipeline automatizado.
- **Semana 24:**
  - *Kickoff Oficial do TCC:* Início do semestre letivo com o tema 100% definido, ferramentas instaladas e protótipo funcional em mãos.
