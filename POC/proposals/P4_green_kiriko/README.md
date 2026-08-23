# 🌱 Proposta 4: Green-Kiriko — Otimização Multidimensional de Energia & EDP

> **Status do MVP:** ✅ Implementado, Testado e Validado  
> **Economia de Energia Demonstrada:** **88.2% de redução em Joules**  
> **Redução de EDP:** De **917.45 J·s** para **5.22 J·s**  

---

## 📌 Visão Geral
O **Green-Kiriko** acopla medição de energia direta em hardware (Intel/AMD RAPL) e modelagem de EDP (*Energy-Delay Product*) ao framework Kiriko. Ele analisa o trade-off entre consumo de potência (Watts), tempo de execução e eficiência energética em compiladores poliédricos.

---

## 🛠️ Estrutura do Módulo

```text
P4_green_kiriko/
├── README.md                              # Este arquivo
├── profiler/
│   ├── rapl_energy_meter.py              # Leitor RAPL e modelo de potência
│   ├── edp_calculator.py                 # Calculador de EDP / ED²P e Fronteira de Pareto
│   └── roofline_model.py                 # Modelo Roofline dinâmico (FLOPs/Byte vs GFLOPS/s)
├── experiments/
│   ├── run_energy_study.py               # Benchmark de energia entre toolchains
│   └── results/                          # Resultados JSON e pontos de Pareto
└── docs/
    ├── 01_ENERGY_METRICS_AND_RAPL.md     # Teoria do RAPL, MSRs e Race-to-Sleep
    └── 02_ENERGY_PERFORMANCE_PARETO.md   # Análise da Fronteira de Pareto
```

---

## 🚀 Como Executar o MVP

```bash
cd /home/mateuszaparoli/ufmg/POC/proposals/P4_green_kiriko
python3 experiments/run_energy_study.py
```
