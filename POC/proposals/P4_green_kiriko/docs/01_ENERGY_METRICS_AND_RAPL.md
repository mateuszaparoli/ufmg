# 📘 Green-Kiriko: Métricas Energéticas, RAPL & Otimização Sustentável

> **Autores:** Jarvis & Pesquisadores do LaC/UFMG  
> **Tema:** Profiling Energético em Joules, EDP e Green HPC no Ecossistema MLIR  

---

## 1. A Interface Intel/AMD RAPL (*Running Average Power Limit*)

O hardware moderno de CPU expõe contadores de energia acumulada através de MSRs (*Model Specific Registers*) e da interface sysfs em `/sys/class/powercap/intel-rapl/`:
- **Package Domain (`intel-rapl:0`):** Toda a energia consumida pelo chip (núcleos + cache L3 + interconexão).
- **DRAM Domain (`intel-rapl:0:0`):** Energia consumida pelos canais de memória RAM DDR.

### A Equação da Energia:
$$E_{\text{total}} = \int_{0}^{T} P(t) \, dt \approx P_{\text{médio}} \times T$$

Mesmo que uma otimização aumente a potência instantânea $P$ (por exemplo, ativando unidades SIMD AVX-512 que consomem mais Watts), a redução drástica no tempo de execução $T$ gera uma **redução líquida substancial na energia total consumida em Joules** (*Race to Sleep effect*).

---

## 2. Métricas de Eficiência: EDP e $ED^2P$

- **Energy-Delay Product ($EDP = E \times T$):** Pondera igualmente o consumo de energia e o tempo de execução.
- **Energy-Delay-Squared ($ED^2P = E \times T^2$):** Dá peso quadrático ao tempo de execução, útil para HPC de alto throughput onde latência é prioritária.
