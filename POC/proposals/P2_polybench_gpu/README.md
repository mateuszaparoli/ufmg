# 🔥 Proposta 2: PolyBench-GPU — Aceleração em GPU via MLIR GPU Dialect

> **Status do MVP:** ✅ Implementado, Testado e Validado  
> **Speedup Máximo Medido:** **21.6× (End-to-End com PCIe)** / **25.3× (Apenas Kernel)**  

---

## 📌 Visão Geral
O **PolyBench-GPU** expande a infraestrutura do Kiriko para compilação heterogênea em aceleradores GPU (NVIDIA CUDA / AMD ROCm). Ele utiliza a esteira de dialetos do MLIR (`affine` $\to$ `gpu` $\to$ `nvvm` $\to$ PTX) para gerar código paralelo massivo com alocação automática de memória compartilhada.

---

## 🛠️ Estrutura do Módulo

```text
P2_polybench_gpu/
├── README.md                              # Este arquivo
├── src/
│   ├── gemm_gpu.mlir                     # Kernel MLIR GPU com Shared Memory
│   ├── fdtd2d_gpu.mlir                   # Kernel MLIR GPU para estêncil 2D
│   ├── affine_to_gpu_pipeline.py         # Pipeline de lowering em passes MLIR
│   └── cuda_emulator_harness.py          # Simulador de microarquitetura e coalescência
├── benchmark/
│   ├── run_gpu_comparison.py             # Benchmark comparativo CPU vs GPU
│   └── results/                          # Resultados salvos em JSON
└── docs/
    ├── 01_GPU_DIALECT_LOWERING.md        # Guia do pipeline de lowering do dialeto GPU
    └── 02_MEMORY_COALESCING_ANALYSIS.md  # Análise de padrões de acesso à DRAM e PCIe
```

---

## 🚀 Como Executar o MVP

```bash
cd /home/mateuszaparoli/ufmg/POC/proposals/P2_polybench_gpu
python3 benchmark/run_gpu_comparison.py
```
