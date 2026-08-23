# 📘 MLIR-PolyFuzz: Guia de Teste Metamórfico & Diferencial

> **Tema:** Metodologia de Fuzzing para Passes Poliédricos em Compiladores  

---

## 1. O Problema do Oráculo em Compiladores

Como testar se um passe de compilação complexo (ex: `-affine-loop-fusion` ou `-affine-super-vectorize`) preserva a semântica de um programa arbitrário?  
Na ausência de um oráculo formal estático, o **Teste Metamórfico e Diferencial** executa o código sob duas esteiras:
1. **Pipeline de Referência (Ground Truth):** Lowering direto sem passes agressivos (`--lower-affine -> LLVM`).
2. **Pipeline em Teste:** Otimizações afins completas (`tile`, `fusion`, `scalrep`, `vectorize`).

Se a saída numérica diferir por mais de um $\epsilon = 10^{-5}$, um bug semântico de compilador é detectado e o kernel é isolado para relatório.
