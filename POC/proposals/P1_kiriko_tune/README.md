# 🏆 Proposta 1: Kiriko-Tune — Autotuning Inteligente de Pipelines MLIR

> **Status do MVP:** ✅ Implementado, Testado e Validado  
> **Ganhos Demonstrados:** Aumento de Speedup de **1.51× (estático)** para **15.91× (otimizado)**  

---

## 📌 Visão Geral
O **Kiriko-Tune** é o módulo de autotuning inteligente acoplado ao Kiriko. Ele resolve a principal limitação identificada no artigo do LaC de fevereiro de 2026: a rigidez dos parâmetros de compilação estáticos (`tile-size=32`, `unroll=4`).

---

## 🛠️ Estrutura do Módulo

```text
P1_kiriko_tune/
├── README.md                          # Este arquivo
├── autotuner/
│   ├── search_space.py               # Definição formal do espaço de busca
│   ├── evaluator.py                  # Avaliador de desempenho e modelo de cache
│   ├── bayesian_optimizer.py         # Otimizador Bayesiano com Optuna (TPE)
│   ├── genetic_optimizer.py          # Algoritmo Genético para permutação de passes
│   └── random_search.py              # Baseline de busca aleatória
├── experiments/
│   ├── run_tune_gemm.py              # Script executável de benchmark
│   └── results/                      # Dados JSON com curvas de convergência
└── docs/
    ├── 01_THEORY_AND_ALGORITHMS.md   # Fundamentação matemática do autotuning
    └── 02_EXPERIMENTAL_FINDINGS.md   # Relatório detalhado dos experimentos
```

---

## 🚀 Como Executar o MVP

```bash
cd /home/mateuszaparoli/ufmg/POC/proposals/P1_kiriko_tune
python3 experiments/run_tune_gemm.py
```
