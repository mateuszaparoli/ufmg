# 📊 PolyBench-Linalg: Trade-offs de Tempo de Compilação & Desempenho

> **Tema:** Análise de Complexidade de Compilação e Vetorização entre Linalg e Affine  

---

## 1. Dados Experimentais Coletados

| Benchmark | Profundidade de Laços | Tempo de Compilação Affine (ms) | Tempo de Compilação Linalg (ms) | Aceleração na Compilação | Delta de Speedup de Execução |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **stencil2d** | 2D | 12.78 ms | 10.50 ms | **1.22×** | +0.40× |
| **gemm** | 3D | 23.26 ms | 11.62 ms | **2.00×** | +0.30× |
| **2mm** | 4D | 40.17 ms | 12.95 ms | **3.10×** | +0.20× |
| **doitgen** | 4D | 40.75 ms | 12.56 ms | **3.24×** | +0.20× |
| **3mm** | 6D | 131.29 ms | 15.55 ms | **8.44×** | +0.00× |

---

## 2. Análise dos Resultados (Key Takeaways)

1. **Escalabilidade Exponencial no Affine:**
   À medida que a profundidade do aninhamento de laços cresce (de 2D para 6D no `3mm`), o tempo de compilação do dialeto Affine salta de $12.78\text{ ms}$ para $131.29\text{ ms}$ ($\sim 10\times$), devido ao crescimento combinatório da eliminação de Fourier-Motzkin nos poliedros.
2. **Tempo Quase Constante no Linalg:**
   O tempo de compilação do Linalg cresce de forma quase linear ($10.5\text{ ms} \to 15.5\text{ ms}$), tornando o Linalg **8.44× mais rápido para compilar** laços profundos.
3. **Qualidade do Código Gerado:**
   O Linalg Vectorizer (`-convert-linalg-to-vector`) gera código SIMD tão eficiente quanto o `-affine-super-vectorize`, mantendo ou superando o speedup em tempo de execução.
