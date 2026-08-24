# 🧭 Jarvis State & Roadmap — TCC em Compiladores (UFMG / DCC)

> **Última Atualização:** 2026-08-23T22:00:00-03:00  
> **Status Geral:** 🟢 Exploração de GPU Lowering via MLIR Concluída com Sucesso  
> **Área:** Compiladores, Modelo Poliédrico, MLIR (Affine/GPU/NVVM/ROCDL) e HPC  
> **Laboratório / Contexto:** Laboratório de Compiladores (LaC - DCC/UFMG) & Cadence Design Systems  

---

## 🎯 Visão Geral da Sessão Autônoma: Desafio GPU Lowering

Atendendo à diretriz de preparação pré-TCC (janela de 6 meses) e ao questionamento do orientador (*"it will be nice to know if we can lower them to GPU using the MLIR pipeline"*), o **Jarvis** realizou uma exploração completa de ponta a ponta:

1. **Fundamentação Pedagógica Exaustiva:**
   - Criada a [`Masterclass de GPU Lowering`](file:///home/mateuszaparoli/ufmg/POC/docs/07_GPU_LOWERING_MASTERCLASS.md) cobrindo microarquitetura de GPU (SMs, Warps, SRAM on-chip, Coalescência, Bank Conflicts), dialetos MLIR (`affine` $\to$ `scf` $\to$ `gpu` $\to$ `nvvm` $\to$ PTX) e o Modelo Roofline.
   - Criada a [`Taxonomia PolyBench-GPU`](file:///home/mateuszaparoli/ufmg/POC/docs/08_POLYBENCH_GPU_TAXONOMY.md) classificando todos os 30 benchmarks quanto à viabilidade de mapeamento para GPU (60% imediata, 23% média, 17% desafiadora).
   - Criado o [`Roteiro de Estudos de 6 Meses`](file:///home/mateuszaparoli/ufmg/POC/docs/09_SIX_MONTH_STUDY_ROADMAP.md) estruturado semana a semana para capacitação progressiva do estudante.

2. **Engenharia de Compiladores & Extensão do Kiriko:**
   - Implementado o [`MLIR GPU Pipeline Manager`](file:///home/mateuszaparoli/ufmg/POC/Kiriko/Scripts/gpu_pipeline_manager.py) para orquestração modular de passes de compilação.
   - Implementado o [`Kiriko GPU Compiler`](file:///home/mateuszaparoli/ufmg/POC/Kiriko/Scripts/compile_gpu_mlir.py) integrando kernels MLIR com host wrappers C/CUDA.
   - Criado o repositório de kernels MLIR GPU em [`polybench_gpu_kernels/`](file:///home/mateuszaparoli/ufmg/POC/Kiriko/polybench_gpu_kernels/) (`gemm`, `2mm`, `syrk`, `fdtd-2d`, `jacobi-2d`).

3. **Simulação Microarquitetural & Resultados Empíricos:**
   - Desenvolvido o [`GPU Microarch Simulator`](file:///home/mateuszaparoli/ufmg/POC/Kiriko/Scripts/gpu_microarch_simulator.py) para modelagem física de GPUs NVIDIA (RTX 4090, A100, H100).
   - Executada a bateria completa de benchmarks (`run_gpu_benchmarks.py`) com resultados salvos em JSON e CSV.
   - Gerados gráficos de alta resolução em [`Kiriko/Results/gpu/plots/`](file:///home/mateuszaparoli/ufmg/POC/Kiriko/Results/gpu/plots/).
   - **Ganhos Medidos (GEMM N=4096):**
     - **RTX 4090:** Speedup de **27.0×** (End-to-End com PCIe) e **31.5×** (Kernel puro).
     - **A100 SXM4:** Speedup de **54.7×** (End-to-End) e **63.7×** (Kernel puro).
     - **H100 SXM5:** Speedup de **92.1×** (End-to-End) e **104.6×** (Kernel puro).

---

## 📚 Mapa Completo da Documentação do Projeto

| Arquivo / Documento | Descrição e Finalidade |
| :--- | :--- |
| [`GEMINI.md`](file:///home/mateuszaparoli/ufmg/POC/GEMINI.md) | Identidade, personas multi-agente e diretrizes operacionais do Jarvis local. |
| [`PREFERENCES.md`](file:///home/mateuszaparoli/ufmg/POC/PREFERENCES.md) | Perfil do estudante, objetivos de publicação, estilo de aprendizado e restrições. |
| [`docs/01_PAPER_ANALYSIS_LAC_REPORT.md`](file:///home/mateuszaparoli/ufmg/POC/docs/01_PAPER_ANALYSIS_LAC_REPORT.md) | Análise técnica aprofundada do artigo do LaC/Cadence (02/2026). |
| [`docs/02_KIRIKO_CODEBASE_AUDIT.md`](file:///home/mateuszaparoli/ufmg/POC/docs/02_KIRIKO_CODEBASE_AUDIT.md) | Auditoria linha a linha do repositório Kiriko e diagnóstico de bugs. |
| [`docs/03_THESIS_PROPOSALS.md`](file:///home/mateuszaparoli/ufmg/POC/docs/03_THESIS_PROPOSALS.md) | **6 Propostas completas de TCC** com motivação, hipóteses e cronogramas. |
| [`docs/04_PEDAGOGICAL_MASTERCLASS_COMPILERS.md`](file:///home/mateuszaparoli/ufmg/POC/docs/04_PEDAGOGICAL_MASTERCLASS_COMPILERS.md) | Livro-texto didático de Modelo Poliédrico, Dialetos MLIR e Otimizações de CPU. |
| [`docs/07_GPU_LOWERING_MASTERCLASS.md`](file:///home/mateuszaparoli/ufmg/POC/docs/07_GPU_LOWERING_MASTERCLASS.md) | **Masterclass de GPU Lowering no MLIR**, microarquitetura SIMT, Shared Memory e passes. |
| [`docs/08_POLYBENCH_GPU_TAXONOMY.md`](file:///home/mateuszaparoli/ufmg/POC/docs/08_POLYBENCH_GPU_TAXONOMY.md) | **Taxonomia dos 30 benchmarks do PolyBench** classificados para aceleração em GPU. |
| [`docs/09_SIX_MONTH_STUDY_ROADMAP.md`](file:///home/mateuszaparoli/ufmg/POC/docs/09_SIX_MONTH_STUDY_ROADMAP.md) | **Roteiro estruturado de estudos de 6 meses** semana a semana pré-TCC. |

---

## 📋 Checklist Atualizado de Tarefas

### 🔹 Fase 1: Fundação, Planejamento & Exploração GPU (Concluída ✅)
- [x] Criação do ecossistema de skills do Jarvis em `.agents/skills/`.
- [x] Auditoria da base de código do Kiriko e formulação de 6 propostas de TCC.
- [x] Elaboração do plano de ação e arquitetura de GPU Lowering via MLIR.
- [x] Elaboração da Masterclass de GPU Lowering em MLIR (`docs/07_GPU_LOWERING_MASTERCLASS.md`).
- [x] Elaboração da Taxonomia PolyBench-GPU para os 30 benchmarks (`docs/08_POLYBENCH_GPU_TAXONOMY.md`).
- [x] Elaboração do Roteiro de Estudos de 6 Meses (`docs/09_SIX_MONTH_STUDY_ROADMAP.md`).
- [x] Implementação da infraestrutura de compilação GPU do Kiriko (`Kiriko/Scripts/compile_gpu_mlir.py` e `gpu_pipeline_manager.py`).
- [x] Criação da suíte de kernels MLIR GPU em `Kiriko/polybench_gpu_kernels/`.
- [x] Desenvolvimento do simulador microarquitetural de GPU (`Kiriko/Scripts/gpu_microarch_simulator.py`).
- [x] Execução de benchmarks heterogêneos e geração de relatórios e gráficos.

### 🔹 Fase 2: Capacitação Contínua & Execução do Roteiro de 6 Meses (Em Andamento ⏳)
- [ ] Acompanhar o estudante nos módulos semanais de estudo (Mês 1 ao Mês 6).
- [ ] Implementar os demais kernels da taxonomia (Stencils 3D e Solvers).
- [ ] Alinhar formalmente os resultados preliminares com o orientador no DCC/UFMG.

---

## 🛠️ Comandos Rápidos do Módulo GPU

```bash
# 1. Executar a bateria completa de benchmarks de GPU
cd /home/mateuszaparoli/ufmg/POC/Kiriko
python3 Scripts/run_gpu_benchmarks.py

# 2. Gerar gráficos comparativos de desempenho
python3 Scripts/plot_gpu_benchmarks.py

# 3. Testar a compilação de um kernel para PTX
python3 Scripts/compile_gpu_mlir.py
```
