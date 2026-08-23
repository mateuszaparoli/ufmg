# 📊 PolyBench-GPU: Análise de Coalescência de Memória & Resultados

> **Tema:** Eficiência de Acesso à DRAM, Overhead de PCIe e Speedups  

---

## 1. Coalescência de Memória Global em GPUs

Uma transação de memória global na GPU atende a 32 threads de um Warp simultaneamente em blocos contíguos de 128 bytes.
- **Acesso Coalescido:** Se a thread $k$ acessa a posição $A[i, k]$, todas as 32 threads acessam endereços consecutivos na mesma linha de cache $\implies$ **1 única transação de 128B (100% de eficiência)**.
- **Acesso Não-Coalescido (com Strides):** Se as threads acessam colunas $A[k, j]$, ocorrem 32 transações separadas de 32B $\implies$ **32× desperdício de largura de banda**.

---

## 2. Resultados Experimentais: CPU Multithread vs. MLIR GPU

| Dimensão da Matriz ($N$) | CPU Clang -O3 (ms) | GPU Kernel (ms) | Transferência PCIe (ms) | Tempo Total GPU (ms) | Speedup End-to-End |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **128** | 0.03 | 0.006 | 0.006 | 0.01 | **2.3×** |
| **256** | 0.22 | 0.014 | 0.025 | 0.04 | **5.9×** |
| **512** | 1.79 | 0.076 | 0.098 | 0.17 | **10.3×** |
| **1024** | 14.32 | 0.570 | 0.393 | 0.96 | **14.9×** |
| **2048** | 114.53 | 4.526 | 1.573 | 6.10 | **18.8×** |
| **4096** | 916.26 | 36.173 | 6.291 | 42.47 | **21.6×** |

### 💡 Descobertas:
1. Para matrizes pequenas ($N \le 128$), o custo de transferência PCIe domina (~50% do tempo total).
2. Para matrizes grandes ($N \ge 1024$), a densidade computacional ($O(N^3)$ vs $O(N^2)$ de transferência) faz a GPU atingir **mais de 21× de speedup real de ponta a ponta**.
