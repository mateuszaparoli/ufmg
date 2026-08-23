# 📘 PolyBench-Linalg: Abstrações Estruturadas vs. Análise Poliédrica

> **Autores:** Jarvis & Pesquisadores do LaC/UFMG  
> **Tema:** O Confronto entre Dialeto Linalg e Dialeto Affine no Ecossistema MLIR  

---

## 1. As Duas Filosofias de Compilação no MLIR

```mermaid
graph TD
    subgraph Filosofia Poliédrica (Affine Dialect)
        A1["Laços Imperativos Aninhados (affine.for)"]
        A2["Análise Exata de Dependência (ISL / Poliedros)"]
        A3["Resolução de ILP / Fourier-Motzkin"]
        A4["Reconstrução de Laços Tiled"]
        A1 --> A2 --> A3 --> A4
    end

    subgraph Filosofia Estruturada (Linalg Dialect)
        L1["Operações Nomeadas / Genéricas (linalg.matmul, linalg.generic)"]
        L2["Preservação de Semântica Tensorial (Tensors / Parallel / Reduction)"]
        L3["Tiling por Transform Dialect (Tile and Fuse)"]
        L4["Bufferização em MemRef + Vetorização Direta"]
        L1 --> L2 --> L3 --> L4
    end
```

---

## 2. Principais Vantagens do Dialeto Linalg
1. **Tempo de Compilação Escalonável:** O Linalg não precisa resolver sistemas de desigualdades inteiras $A\vec{i} + \vec{b} \ge 0$ de alta dimensionalidade. O tiling é aplicado como uma transformação estrutural direta ($O(1)$).
2. **Fusão de Produtor-Consumidor Natural:** A fusão de operadores consecutivos (`linalg.fuse_elementwise_ops`) opera sobre grafos de tensores sem a fragilidade de testes de dependência cruzada que causaram a exclusão do pass de fusão no `reg_detect` e o bug no `symm`.
3. **Compatibilidade com Ecossistemas de IA:** Google IREE, Torch-MLIR e StableHLO geram Linalg nativamente.
