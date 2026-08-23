---
name: jarvis-factory
description: >-
  Cria, inicializa e gerencia agentes 'Jarvis' especializados para qualquer
  subdiretório, submódulo ou projeto prático dentro do repositório UFMG.
  Use esta skill sempre que o usuário pedir para criar um Jarvis para uma pasta/repositório,
  resumir o progresso ou continuar a exploração de um subprojeto.
---

# 🤖 Jarvis Factory (UFMG)

Esta skill define o procedimento padrão para inicializar e manter agentes **Jarvis** especializados para cada disciplina, trabalho prático (TP) ou projeto dentro do ecossistema UFMG.

---

## 🎯 Objetivo de um Jarvis Local

Cada subdiretório/projeto com um Jarvis possui:
1. **Identidade e Contexto Dedicado (`GEMINI.md` local):** O agente entende a matéria, a stack tecnológica, as regras de entrega e o escopo do projeto.
2. **Memória Contínua e Rastreador de Progresso (`JARVIS_STATE.md` local):** Registra o estado atual das tarefas, decisões arquiteturais, problemas encontrados, notas de estudo e próximos passos.

---

## 📋 Procedimento: "Crie um Jarvis para este repositório"

Quando o usuário solicitar a criação de um Jarvis para a pasta atual (ou um subdiretório especificado):

### Passo 1: Inspecionar o Subdiretório
1. Analise a árvore de arquivos do subdiretório (`README.md`, código-fonte, `Makefile`, `package.json`, `requirements.txt`, etc.).
2. Identifique:
   - **Nome da Disciplina / Projeto** (ex: *Compiladores*, *IIA - TP2*, *Sistemas Operacionais*).
   - **Stack Tecnológica** (ex: C++, Python, Rust, Node.js, Twelf).
   - **Objetivo do Projeto / Trabalho Prático**.
   - **Estado Atual** (o que já está implementado e o que parece estar pendente).

### Passo 2: Criar o Arquivo de Regras Local (`GEMINI.md`)
Crie um arquivo `GEMINI.md` dentro da pasta do projeto com o formato:

```markdown
# 🤖 Jarvis — [Nome da Disciplina / Projeto]

Você é o **Jarvis**, assistente especializado dedicado a este projeto/disciplina na UFMG.

## 📌 Contexto Local
- **Disciplina/Projeto:** [Nome do Projeto]
- **Stack & Ferramentas:** [Linguagens, bibliotecas, ferramentas]
- **Objetivo:** [Breve descrição dos requisitos e metas de entrega]

## 🧠 Memória e Estado
- Antes de iniciar qualquer tarefa, consulte sempre [`JARVIS_STATE.md`](./JARVIS_STATE.md) para resgatar o contexto, as decisões anteriores e o checklist de progresso.
- Ao final de tarefas significativas ou ao encerrar uma exploração, atualize o [`JARVIS_STATE.md`](./JARVIS_STATE.md) com novos aprendizados, decisões tomadas e próximos passos.

## ⚙️ Diretrizes Locais
1. Mantenha os padrões de código e convenções já adotados neste diretório.
2. Não altere arquivos fora do escopo deste projeto sem confirmação.
3. Priorize soluções testáveis e documentadas para relatórios e entregas acadêmicas.
```

### Passo 3: Criar o Rastreador de Progresso (`JARVIS_STATE.md`)
Crie o arquivo `JARVIS_STATE.md` dentro da pasta do projeto estruturado da seguinte forma:

```markdown
# 🧭 Jarvis State & Roadmap — [Nome do Projeto]

> **Última Atualização:** [Data/Hora atual]  
> **Status Geral:** [Em Andamento / Planejamento / Concluído]

---

## 🎯 Visão Geral & Objetivos
[Resumo conciso do que o projeto resolve e o que precisa ser entregue]

---

## 📋 Roadmap & Checklist de Tarefas
- [x] Tarefa já concluída / identificada no código
- [ ] Próxima tarefa prioritária
- [ ] Tarefas futuras / refinamento

---

## 🧠 Histórico de Exploração & Decisões Arquiteturais
- **[Data]:** [Resumo do que foi analisado, decidido ou implementado]

---

## 🛠️ Comandos Úteis & Como Executar
```bash
# Como compilar / rodar / testar neste subdiretório
```

---

## 📌 Notas, Dúvidas & Próximos Passos
- [Anotação relevante ou ponto a investigar na próxima sessão]
```

### Passo 4: Confirmar ao Usuário
Apresente um resumo com link clicável para o `GEMINI.md` e `JARVIS_STATE.md` criados, destacando o estado inicial identificado e os próximos passos sugeridos.

---

## 🔄 Procedimento: Manter e Atualizar o Progresso

Sempre que novas implementações forem concluídas ou decisões forem tomadas no subdiretório:
1. Marque itens concluídos no checklist (`- [x]`).
2. Adicione uma entrada concisa no **Histórico de Exploração**.
3. Atualize a data de **Última Atualização** e os **Próximos Passos**.
