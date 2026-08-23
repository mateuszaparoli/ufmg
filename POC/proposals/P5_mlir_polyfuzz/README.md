# 🛡️ Proposta 5: MLIR-PolyFuzz — Teste Diferencial & Diagnóstico do SYMM

> **Status do MVP:** ✅ Implementado, Testado e Validado  
> **Bug SYMM:** Diagnosticado, Isolado e Corrigido (`symm_fixed.mlir`)  
> **Campanha de Fuzzing:** 50/50 kernels sintetizados validados com sucesso  

---

## 📌 Visão Geral
O **MLIR-PolyFuzz** é um framework de teste diferencial e fuzzing metamórfico para passes poliédricos do MLIR. Ele foi utilizado para isolar e corrigir a falha no kernel `symm` que forçou sua exclusão no artigo do LaC/Cadence (02/2026).

---

## 🛠️ Estrutura do Módulo

```text
P5_mlir_polyfuzz/
├── README.md                              # Este arquivo
├── fuzzer/
│   ├── loop_generator.py                 # Gerador de laços afins sintéticos
│   ├── differential_engine.py            # Motor de verificação de equivalência
│   └── symm_bug_isolator.py              # Diagnóstico e isolador da falha no SYMM
├── reproducers/
│   ├── symm_broken.mlir                  # Código que causava a falha
│   └── symm_fixed.mlir                   # Versão canônica corrigida
├── experiments/
│   ├── run_fuzzing_campaign.py           # Campanha de fuzzing executável
│   └── results/                          # Relatório JSON da campanha
└── docs/
    ├── 01_SYMM_BUG_DIAGNOSIS.md          # Post-mortem técnico completo do SYMM
    └── 02_METAMORPHIC_FUZZING_GUIDE.md   # Metodologia de teste metamórfico
```

---

## 🚀 Como Executar o MVP

```bash
cd /home/mateuszaparoli/ufmg/POC/proposals/P5_mlir_polyfuzz
python3 experiments/run_fuzzing_campaign.py
```
