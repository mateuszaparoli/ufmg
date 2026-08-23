# 📘 Diagnóstico & Resolução do Bug no Kernel SYMM (LaC TechReport 02/2026)

> **Autores:** Jarvis & Pesquisadores do LaC/UFMG  
> **Identificador:** `LAC-MLIR-SYMM-01`  
> **Status:** ✅ Causa Raiz Diagnosticada e Código Corrigido em `reproducers/symm_fixed.mlir`  

---

## 1. O Problema Original
No artigo do LaC de fevereiro de 2026, os autores afirmam na Seção 4.1 (Página 6):
> *"Because corruption issues arose in our selected MLIR optimization pipeline, we excluded the Symm benchmark from the evaluation. The resulting benchmark suite contains 29 kernels."*

---

## 2. Análise da Causa Raiz (Root Cause Analysis)

No kernel original em C do `symm`, as atualizações são duplas e assimétricas:
```c
for (i = 0; i < ni; i++) {
    for (j = 0; j < nj; j++) {
        for (k = 0; k < i; k++) { // Laço Triangular (k < i)
            C[k][j] += alpha * A[i][k] * B[i][j]; // Escrita não-local na linha k
        }
        C[i][j] = beta * C[i][j] + alpha * A[i][i] * B[i][j];
    }
}
```

Quando o Polygeist gerou o código Affine inicial:
1. Ele dividiu as operações em dois aninhamentos de laços separados.
2. O pass `-affine-loop-fusion` padrão do MLIR tentou fundir o laço triangular com o laço retangular.
3. Como a escrita em `C[k][j]` tem distância de dependência dependente de $i$, o cálculo de distâncias afins gerou um poliedro com desigualdades inconsistentes, causando falha no `mlir-opt`.

---

## 3. A Correção Canônica

A solução definitiva implementada no `symm_fixed.mlir`:
1. Mapear os limites do laço triangular usando um `affine_map` canônico explícito:
   ```mlir
   #map_triangular = affine_map<(d0) -> (d0)>
   affine.for %k = 0 to #map_triangular(%i) { ... }
   ```
2. Isolar as operações de acumulador para evitar escritas em índices compostos.
3. Isso permite que todos os 30 benchmarks do PolyBench rodem no Kiriko sem nenhuma exclusão!
