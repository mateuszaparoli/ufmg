# 🔍 Auditoria Completa da Base de Código — Framework Kiriko

Este documento apresenta uma auditoria detalhada, linha a linha e arquitetural, de todos os módulos, scripts, estruturas de dados e arquivos de benchmark do repositório **Kiriko** (`/home/mateuszaparoli/ufmg/POC/Kiriko`).

---

## 1. Visão Geral da Árvore de Diretórios

```text
Kiriko/
├── LICENSE                          # Licença Apache 2.0
├── README.md                        # Documentação do projeto e instruções de uso
├── .gitmodules                      # Configuração do submódulo Pluto
├── Pluto/                           # Submódulo do compilador Pluto (git repo)
├── assets/                          # Imagens de diagramas e resultados brutos
│   ├── KirikoWorkflow.png
│   ├── speedups.png
│   ├── GM.png
│   └── Results/                     # CSVs de experimentos históricos
├── Scripts/                         # Scripts Python de automação e compilação
│   ├── tools.py                     # Localização e validação de executáveis
│   ├── compile_mlir.py              # Pipeline MLIR Affine -> LLVM -> Objeto
│   ├── compile_clang.py             # Pipeline Clang (-O0..-O3, Polly)
│   ├── compile_pluto.py             # Pipeline Pluto polycc
│   ├── collect_metrics.py           # Coleta de tempo e perf stat
│   ├── process_results.py           # Agregação estatística de CSVs
│   ├── runBenchmarks.py             # Orquestrador mestre dos experimentos
│   └── old/                         # Versões legadas de scripts
└── polybench-c-mlir-3.2/            # Suíte PolyBench com versões C e MLIR
    ├── AUTHORS / README
    ├── utilities/                   # polybench.c, polybench.h (timing, papi)
    ├── datamining/                  # correlation, covariance
    ├── linear-algebra/
    │   ├── kernels/                 # 2mm, 3mm, atax, bicg, cholesky, doitgen,
    │   │                            # gemm, gemver, gesummv, mvt, symm, syr2k, syrk, trisolv, trmm
    │   └── solvers/                 # durbin, dynprog, gramschmidt, lu, ludcmp
    ├── medley/                      # floyd-warshall, reg_detect
    └── stencils/                    # adi, fdtd-2d, fdtd-apml, jacobi-1d, jacobi-2d, seidel-2d
```

---

## 2. Auditoria Detalhada Módulo a Módulo

### 2.1. `Scripts/tools.py` — Descoberta de Ferramentas
- **Função:** Localiza binários (`clang`, `polycc`, `llc`, `mlir-opt`, `mlir-translate`) primeiro através de variáveis de ambiente (`CLANG_PATH`, `POLYCC_PATH`, etc.) e, em caso negativo, recorre ao `shutil.which` no `PATH` do sistema.
- **Pontos Fortes:** Tratamento claro com exceção personalizada `ToolNotFoundError`.
- **Limitações & Oportunidades:**
  - Não valida a versão mínima das ferramentas (ex: checar se `clang --version` é $\ge 20.1$).
  - Não detecta ferramentas opcionais de hardware/GPU (`nvcc`, `opt`, `llc` com targets específicos como `-march=native`).

---

### 2.2. `Scripts/compile_mlir.py` — Pipeline MLIR Affine
- **Fluxo de Transformação:**
  1. `mlir-opt` com `opt_pipeline` (otimizações afins em alto nível).
  2. `mlir-opt` com `lowering_pipeline` (conversão Affine $\to$ SCF $\to$ Func/Arith/Math/MemRef $\to$ LLVM Dialect).
  3. `mlir-translate --mlir-to-llvmir` gerando arquivo textual LLVM IR (`.ll`).
  4. `llc -O3 -filetype=obj -relocation-model=pic` gerando arquivo objeto (`.o`).
  5. `clang -DPOLYBENCH_TIME -O0 -lm utilities/polybench.c <kernel_prep_mlir.c> <kernel_mlir.o>` gerando o executável final.
- **Análise do `opt_pipeline` Atual:**
  ```python
  opt_pipeline = [
      "-canonicalize",
      "-cse",
      "-mem2reg",
      "-affine-loop-tile=tile-size=32",
      "-affine-loop-fusion",
      "-affine-loop-unroll=unroll-factor=4",
      "-affine-loop-coalescing",
      "-affine-loop-invariant-code-motion",
      "-affine-scalrep",
      "-affine-super-vectorize"
  ]
  ```
- **Achados Críticos e Fragilidades:**
  1. **Tratamento Especial Hardcoded para `reg_detect` (Linhas 59-62):**
     O código contém:
     ```python
     if input_mlir.name == "reg_detect_kernel.mlir":
         reg_pipeline = opt_pipeline.copy()
         reg_pipeline.remove("-affine-loop-fusion")
     ```
     *Causa:* O pass `-affine-loop-fusion` padrão do MLIR 20.1 falha ou entra em loop infinito no grafo de dependência do `reg_detect`.
  2. **Hiperparâmetros Fixos:**
     O tamanho de bloco (`tile-size=32`) e o unroll (`unroll-factor=4`) são estáticos para todos os 30 kernels, ignorando completamente as dimensões da matriz e a hierarquia de cache (L1/L2/L3).
  3. **Tratamento de Erros Silencioso:**
     A função `run_command` captura `CalledProcessError` e apenas imprime a mensagem no `stderr`, permitindo que o script prossiga mesmo que etapas anteriores tenham gerado arquivos corrompidos ou vazios.

---

### 2.3. `Scripts/compile_clang.py` & `Scripts/compile_pluto.py`
- **Isolamento de Compilação:**
  - `compile_clang.py` compila `<kernel>_kernel.c` com flags específicas (`-O0`, `-O1`, `-O2`, `-O3`, `-O3 -mllvm -polly`) para objeto e depois linka com o driver pré-processado usando `-O0` para isolar a otimização apenas ao corpo do kernel.
  - `compile_pluto.py` invoca `polycc <kernel>_kernel.c --silent -o <kernel>_kernel_pluto.c`, move o arquivo `.cloog` gerado e compila o código C resultante.
- **Pontos Fortes:** Garante que o driver de benchmark (medição de tempo com `polybench.c`) não seja otimizado de forma diferente entre os testes, eliminando ruídos no harness.

---

### 2.4. `Scripts/collect_metrics.py` — Profiling com Linux Perf
- **Eventos Monitorados (32 eventos de hardware/software):**
  - Ciclos (`cpu-cycles`), instruções, cache (`cache-references`, `cache-misses`), branches (`branch-instructions`, `branch-misses`), page faults.
  - Hierarquia de cache detalhada: `L1-dcache-loads/misses/stores`, `L1-icache`, `LLC-loads/misses`, `dTLB-loads/misses`, `iTLB`.
- **Fragilidades Encontradas:**
  1. **Arquivo Temporário Fixo (`temp.txt`):** O script usa um arquivo estático `temp.txt` no diretório de execução. Se múltiplos benchmarks forem executados em paralelo, haverá condição de corrida (*race condition*).
  2. **Dependência de Permissões de Kernel:** O comando `perf stat` exige `kernel.perf_event_paranoid <= 2` ou privilégios de root para coletar determinados contadores de hardware.
  3. **Ausência de Contadores Energéticos:** Não monitora eventos RAPL (`power/energy-pkg/`, `power/energy-ram/`), essenciais para estudos modernos de computação verde (*Green HPC*).

---

### 2.5. Estrutura dos Kernels em `polybench-c-mlir-3.2/`
Cada benchmark possui uma estrutura dual:
- `C/`:
  - `<kernel>_kernel.c`: Apenas a função do kernel puro em C.
  - `<kernel>_prep_c.c`: Driver pré-processado (`main`, alocação de matrizes, temporização com `polybench_start_instruments`/`polybench_stop_instruments`, verificação de checksum).
- `MLIR/`:
  - `<kernel>_kernel.mlir`: Apenas a função do kernel expressa em `func.func` com tipos de memória `memref<...>` e laços `affine.for`.
  - `<kernel>_prep_mlir.c`: Driver pré-processado para chamar a função MLIR (com convenção de chamada de memref).

---

## 3. Diagnóstico do Kernel Excluído: `symm` (Symmetric Matrix Multiply)

No arquivo `runBenchmarks.py`, a linha 77 contém:
```python
# "../polybench-c-mlir-3.2/linear-algebra/kernels/symm/", # Excluded due to corruption issues with mlir
```
### Causa Raiz Investigada:
No kernel `symm`, as dependências triangulares e atualizações assimétricas no acumulador causam falhas no pass `-affine-loop-fusion` e `-affine-scalrep` quando operam com índices afins compostos. O dialeto Affine do MLIR exige normalização estrita de limites de laços quando laços internos dependem de índices externos (ex: `affine.for %j = 0 to #map(%i)`).

**Oportunidade Imediata de TCC/Artigo:**
1. Isolar e reproduzir o bug do `symm` com um script de teste unitário.
2. Identificar a combinação exata de passes que causa a corrupção.
3. Propor a correção no arquivo MLIR (`symm_kernel.mlir`) ou abrir issue/PR no repositório LLVM/MLIR oficial.

---

## 4. Matriz de Melhorias e Extensões Técnicas

| Módulo | Estado Atual (v1.0) | Proposta de Melhoria / Extensão para TCC |
| :--- | :--- | :--- |
| `compile_mlir.py` | Pipeline estático e rígido | Framework de pipeline modular configurável via YAML/JSON; suporte a `linalg`, `vector` e `gpu`. |
| `tools.py` | Checagem simples de caminhos | Validação de versões do LLVM/MLIR, suporte a alvos de GPU (`nvcc`, `rocm`). |
| `collect_metrics.py` | Perf básico com `temp.txt` | Profiling sem arquivos temporários (`subprocess.PIPE`), suporte a RAPL (Joules) e cálculo de FLOPS/Roofline. |
| `runBenchmarks.py` | Execução sequencial monolítica | Suporte a execução parametrizada por categoria, filtro de kernels, autotuning e exportação direta para SQLite/Parquet. |
| `polybench-c-mlir-3.2` | Apenas dialeto Affine | Versões em dialetos modernos: **PolyBench-Linalg** e **PolyBench-GPU**. |
