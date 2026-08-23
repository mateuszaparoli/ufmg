# 🧭 Jarvis State & Roadmap — TCC em Compiladores (UFMG / DCC)

> **Última Atualização:** 2026-08-21T21:30:00-03:00  
> **Status Geral:** 🟢 Estruturação Inicial & Propostas de TCC Concluídas com Sucesso  
> **Área:** Compiladores, Modelo Poliédrico, MLIR (Affine/GPU/Linalg) e HPC  
> **Laboratório / Contexto:** Laboratório de Compiladores (LaC - DCC/UFMG) & Cadence Design Systems  

---

## 🎯 Visão Geral da Sessão Autônoma

Durante o período de trabalho contínuo (`/goal`), o **Jarvis** foi formalmente inicializado como o agente orquestrador mestre e orientador acadêmico do TCC. Foram desenvolvidos os subagentes especializados, analisado exaustivamente o relatório técnico `LaC_TechReport022026.pdf`, auditada a base de código do **Kiriko** e formuladas 6 propostas completas de TCC com masterclass pedagógica integrada.

---

## 📚 Mapa de Navegação da Documentação Criada

Todos os artefatos de pesquisa, engenharia e didática estão organizados no diretório [`POC/`](file:///home/mateuszaparoli/ufmg/POC):

| Arquivo / Documento | Descrição e Finalidade |
| :--- | :--- |
| [`GEMINI.md`](file:///home/mateuszaparoli/ufmg/POC/GEMINI.md) | Identidade, personas multi-agente e diretrizes operacionais do Jarvis local. |
| [`PREFERENCES.md`](file:///home/mateuszaparoli/ufmg/POC/PREFERENCES.md) | Perfil do estudante, objetivos de publicação, estilo de aprendizado e restrições. |
| [`docs/01_PAPER_ANALYSIS_LAC_REPORT.md`](file:///home/mateuszaparoli/ufmg/POC/docs/01_PAPER_ANALYSIS_LAC_REPORT.md) | Análise técnica aprofundada do artigo do LaC/Cadence (02/2026), metodologias e lacunas. |
| [`docs/02_KIRIKO_CODEBASE_AUDIT.md`](file:///home/mateuszaparoli/ufmg/POC/docs/02_KIRIKO_CODEBASE_AUDIT.md) | Auditoria linha a linha do repositório Kiriko, scripts, pipelines MLIR e diagnóstico do bug `symm`. |
| [`docs/03_THESIS_PROPOSALS.md`](file:///home/mateuszaparoli/ufmg/POC/docs/03_THESIS_PROPOSALS.md) | **6 Propostas completas de TCC** com motivação, hipóteses, cronogramas e publicações alvo. |
| [`docs/04_PEDAGOGICAL_MASTERCLASS_COMPILERS.md`](file:///home/mateuszaparoli/ufmg/POC/docs/04_PEDAGOGICAL_MASTERCLASS_COMPILERS.md) | Livro-texto didático cobrindo Modelo Poliédrico, Dialetos MLIR, Tiling, Vectorização e Roofline. |
| [`docs/05_JARVIS_AGENT_ECOSYSTEM.md`](file:///home/mateuszaparoli/ufmg/POC/docs/05_JARVIS_AGENT_ECOSYSTEM.md) | Arquitetura multi-agente do Jarvis (Mentor, Pesquisador, Engenheiro, Revisor). |
| [`docs/06_NEXT_STEPS_ACTION_PLAN.md`](file:///home/mateuszaparoli/ufmg/POC/docs/06_NEXT_STEPS_ACTION_PLAN.md) | Matriz de decisão rápida e roteiro passo a passo para a volta do estudante. |

---

## 📋 Roadmap & Checklist de Tarefas

### 🔹 Fase 1: Fundação & Planejamento (Concluída ✅)
- [x] Criação do ecossistema de skills do Jarvis em `.agents/skills/` (`jarvis-tcc`, `polyhedral-mentor`, `thesis-researcher`, `kiriko-dev`).
- [x] Configuração da identidade local em `POC/GEMINI.md` e `POC/PREFERENCES.md`.
- [x] Leitura completa e análise crítica de `LaC_TechReport022026.pdf`.
- [x] Auditoria estrutural e de código do repositório `Kiriko`.
- [x] Formulação de 6 propostas de TCC de alto impacto acadêmico.
- [x] Elaboração da Masterclass Pedagógica em Compiladores e MLIR.
- [x] Elaboração do Plano de Ação e Matriz de Decisão para retorno.

### 🔹 Fase 2: Seleção de Tema & Refinamento (Próxima Etapa ⏳)
- [ ] Escolha da proposta de TCC pelo estudante (Recomendações: **Kiriko-Tune** ou **PolyBench-GPU**).
- [ ] Reunião e alinhamento do tema com o orientador no DCC/UFMG.
- [ ] Escrita da Proposta Formal de TCC 1 (Introdução, Objetivos, Metodologia).

### 🔹 Fase 3: Engenharia & Implementação (A Executar 🔜)
- [ ] Configuração e validação do ambiente LLVM/MLIR 20.1 no Linux.
- [ ] Desenvolvimento dos novos passes / módulos do Kiriko (conforme proposta escolhida).
- [ ] Execução da primeira bateria de benchmarks com $N \ge 30$ amostras.

### 🔹 Fase 4: Redação Científica & Defesa (Futuro 🎓)
- [ ] Redação dos capítulos da monografia no template LaTeX da UFMG.
- [ ] Revisão rigorosa de ameaças à validade e testes estatísticos.
- [ ] Submissão do artigo para conferência (CGO / CC / PACT / SBLP / WSCAD).

---

## 🧠 Histórico de Decisões Arquiteturais
- **2026-08-21:**
  - *Decisão:* Adotar uma arquitetura multi-agente modular baseada em 4 personas especializadas (Mentor Pedagógico, Pesquisador de Literatura, Engenheiro de Compiladores e Revisor Crítico) para garantir suporte tanto prático quanto teórico.
  - *Decisão:* Priorizar as propostas de **Autotuning Bayesiano (Kiriko-Tune)** e **Aceleração em GPU (PolyBench-GPU)** devido à alta complementaridade com os pontos fracos e oportunidades em aberto deixadas pelo relatório técnico do LaC de fevereiro de 2026.
  - *Decisão:* Documentar toda a fundamentação teórica em formato de Masterclass no repositório local para permitir que o estudante estude e domine todos os conceitos de forma autodidata.

---

## 🛠️ Como Executar os Scripts do Kiriko

```bash
# Definir caminhos das ferramentas se não estiverem no PATH global
export CLANG_PATH=/usr/bin/clang-20
export MLIR_OPT_PATH=/usr/bin/mlir-opt-20
export MLIR_TRANSLATE_PATH=/usr/bin/mlir-translate-20
export LLC_PATH=/usr/bin/llc-20
export POLYCC_PATH=/usr/local/bin/polycc

# Definir número de repetições por benchmark (padrão do artigo: 30)
export SAMPLE_SIZE=30

# Executar a bateria de compilação e coleta de métricas
cd /home/mateuszaparoli/ufmg/POC/Kiriko
python3 Scripts/runBenchmarks.py

# Processar e agregar resultados estatísticos (média, mediana, desvio)
python3 Scripts/process_results.py ../Results/mlir/ --output ../Results/mlir_aggregated.csv
```
