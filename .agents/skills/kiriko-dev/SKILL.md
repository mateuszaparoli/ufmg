---
name: kiriko-dev
description: >-
  Especialista em Desenvolvimento e Extensão do Framework Kiriko,
  Pipelines MLIR, Compilação de PolyBench, Otimização de Compiladores e Linux Perf.
---

# ⚙️ Kiriko Dev — Engenharia de Compiladores & Benchmarking

Esta skill guia o desenvolvimento, customização e execução do framework **Kiriko** e da suíte **PolyBench-MLIR**.

---

## 🛠️ Arquitetura do Kiriko

O Kiriko é composto por:
- `Scripts/tools.py`: Descoberta de ferramentas (`clang`, `mlir-opt`, `mlir-translate`, `llc`, `polycc`).
- `Scripts/compile_mlir.py`: Pipeline de otimização MLIR Affine e lowering para LLVM IR e binário.
- `Scripts/compile_clang.py`: Pipeline Clang (`-O0`, `-O1`, `-O2`, `-O3`, Polly).
- `Scripts/compile_pluto.py`: Pipeline Pluto (geração de C transformado -> Clang).
- `Scripts/collect_metrics.py`: Execução e coleta de tempos de execução e métricas de hardware via Linux Perf.
- `Scripts/process_results.py`: Agregação estatística de múltiplos experimentos (média, mediana, desvio padrão).
- `polybench-c-mlir-3.2/`: Coleção dos 30 benchmarks em C pré-processado e MLIR Affine.

---

## 🚀 Padrões de Extensão

1. **Adição de Novos Passes MLIR:**
   - Edite `compile_mlir.py` modificando `opt_pipeline` ou crie pipelines dinâmicos (ex: parametrização de `--affine-loop-tile=tile-size=...`, `--affine-vectorize`, `--convert-linalg-to-affine`, etc.).
2. **Suporte a Novas Ferramentas / Backends:**
   - Crie `compile_<backend>.py` seguindo o contrato: compila o kernel para arquivo objeto `.o` e linka com o driver pré-processado (`<kernel>_prep_c.c` ou `<kernel>_prep_mlir.c`).
3. **Novas Métricas de Hardware:**
   - Adicione eventos ao `collect_metrics.py` (ex: `power/energy-pkg/`, `instructions`, `cycles`, etc.).
4. **Autotuning & Busca em Espaço de Otimizações:**
   - Crie scripts para variar hiperparâmetros de compilação e registrar resultados no diretório `Results/`.
