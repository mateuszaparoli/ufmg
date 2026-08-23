# ⚡ Proposta 3: PolyBench-Linalg — Transformações Estruturadas vs Poliédricas

> **Status do MVP:** ✅ Implementado, Testado e Validado  
> **Compilação:** Até **8.44× mais rápida** em laços profundos (6D)  
> **Desempenho:** Desempenho idêntico ou superior ao Affine Dialect  

---

## 📌 Visão Geral
O **PolyBench-Linalg** implementa uma versão da suíte PolyBench utilizando o dialeto **MLIR Linalg** (com operações nomeadas como `linalg.matmul` e genéricas `linalg.generic`). Ele investiga as vantagens das transformações estruturadas de tensores frente à análise poliédrica clássica do dialeto Affine.

---

## 🛠️ Estrutura do Módulo

```text
P3_polybench_linalg/
├── README.md                              # Este arquivo
├── kernels_linalg/
│   ├── gemm_linalg.mlir                  # GEMM estruturado via linalg.matmul
│   ├── 2mm_linalg.mlir                   # 2MM com fusão de operadores
│   └── generic_stencil.mlir              # Estêncil 2D via linalg.generic
├── transforms/
│   ├── linalg_tiling_pipeline.py         # Pipeline de tiling e bufferização Linalg
│   ├── compare_affine_vs_linalg.py       # Benchmark empírico de compilação e execução
│   └── results/                          # Dados JSON dos experimentos
└── docs/
    ├── 01_STRUCTURED_VS_POLYHEDRAL.md    # Fundamentação teórica Linalg vs Affine
    └── 02_COMPILATION_TIME_TRADEOFFS.md  # Análise detalhada dos resultados
```

---

## 🚀 Como Executar o MVP

```bash
cd /home/mateuszaparoli/ufmg/POC/proposals/P3_polybench_linalg
python3 transforms/compare_affine_vs_linalg.py
```
