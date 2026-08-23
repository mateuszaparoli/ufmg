---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #0f172a
color: #f8fafc
style: |
  section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 22px;
    padding: 40px 60px;
  }
  h1 {
    color: #38bdf8;
    font-size: 40px;
    margin-bottom: 12px;
  }
  h2 {
    color: #22d3ee;
    font-size: 30px;
    margin-bottom: 16px;
  }
  h3 {
    color: #94a3b8;
    font-size: 24px;
  }
  strong {
    color: #38bdf8;
  }
  code {
    background-color: #1e293b;
    color: #f472b6;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  pre {
    background-color: #020617;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 14px;
    font-size: 16px;
    line-height: 1.4;
  }
  table {
    font-size: 18px;
    border-collapse: collapse;
    width: 100%;
    margin-top: 10px;
  }
  th {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 8px 12px;
    border: 1px solid #334155;
  }
  td {
    padding: 8px 12px;
    border: 1px solid #334155;
    background-color: #0f172a;
  }
  footer {
    font-size: 13px;
    color: #64748b;
  }
  .highlight-box {
    background: #1e293b;
    border-left: 4px solid #38bdf8;
    padding: 12px 18px;
    border-radius: 4px;
    margin-top: 12px;
  }
---

# 🚀 Enhancing Jest Testing with `jest-bdd-generator`
### Como o TikTok unificou Testes Unitários e BDD via Transformação de Sintaxe

**Artigo Original:** *Make your tests readable with jest-bdd-generator*  
**Autor:** Shiguang Ai (Software Engineer, TikTok)  
**Tópicos:** Jest, BDD (Behavior-Driven Development), Gherkin, AST Transformation  

---

## 📌 Contexto & Motivação: O Dilema dos Testes Frontend

* **O Domínio do Jest:**
  * Padrão quase unânime no ecossistema JavaScript / TypeScript / React.
  * Forte integração com pipelines de CI, cobertura de código e ferramentas de build.

* **O Problema da Legibilidade:**
  * Embora o Jest use `describe()` e `expect()`, testes ainda são **programas imperativos**.
  * No ritmo ágil de entrega, testes acumulam código confuso: setup extenso, mocks complexos e lógica de depuração.
  * **Consequência:** Dificuldade para gerentes, analistas de negócio (PO), QA ou novos desenvolvedores entenderem o que está sendo testado.

---

## 💡 Por que BDD (Behavior-Driven Development)?

* **Foco no Comportamento:**
  * Descreve os requisitos do sistema em **linguagem natural e estruturada**.
  * Padrão clássico com **Cucumber** e a sintaxe **Gherkin**:
    * `Given` (Dado um contexto inicial)
    * `When` (Quando uma ação acontece)
    * `Then` (Então espera-se um resultado específico)

* **Especificação Executável (*Executable Specification*):**
  * Diferente de documentações em Wiki que ficam desatualizadas, a especificação Gherkin é o próprio teste rodando.
  * Serve simultaneamente como **documentação viva**, **critério de aceite** e **validação automatizada**.

---

## ⚠️ O Desafio de Adoção do BDD na Prática

Por que muitas equipes desistem de adotar BDD com Cucumber?

1. **Ruptura de Stack:**
   * Abandonar o Jest em prol do Cucumber.js puro descarta anos de investimento em tooling, mocks e ecossistema React.
2. **Complexidade de Ferramental Híbrido:**
   * Adaptadores que rodam Gherkin sobre Jest exigem manter **dois formatos separados** simultaneamente.
   * O desenvolvedor precisa configurar e sincronizar arquivos `.feature` e arquivos de *step definitions*.
3. **Resistência dos Times:**
   * A sobrecarga cognitiva e o retrabalho desestimulam a adesão contínua da engenharia.

---

## 🎯 A Ideia do TikTok: *Roundtrip Syntax Transformations*

> *"E se pudéssemos sobrepor os benefícios do Gherkin diretamente dentro dos testes comuns do Jest, sem mudar de framework?"*

* **A Abordagem Inovadora:**
  * Os testes continuam sendo arquivos Jest normais (`.test.ts`).
  * As especificações Gherkin são adicionadas como **comentários semânticos** (`//@Given`, `//@When`, `//@Then`).
  * Através da **análise de AST do TypeScript**, o `jest-bdd-generator` converte código em especificação e vice-versa de forma bidirecional.

---

## 🔄 O Ciclo Bidirecional (*The Roundtrip Workflow*)

```text
               ┌──────────────────────────────┐
               │    Código de Teste Jest      │
               │      (math.test.ts)          │
               └──────────────┬───────────────┘
                              │
               [ gen-comments / gen-doc ]
                              │
                              ▼
               ┌──────────────────────────────┐
               │   Especificação Gherkin      │
               │      (math.feature)          │
               └──────────────┬───────────────┘
                              │
                        [ gen-test ]
                              │
                              ▼
               ┌──────────────────────────────┐
               │ Teste Jest Atualizado/Sync   │
               └──────────────────────────────┘
```

---

## 🧩 1. Injetando Anotações: `gen-comments`

O comando `gen-comments` analisa o teste existente (ex: `test.each`) e gera stubs de comentários:

```typescript
describe('Rounding methods of Math', () => {
  test.each([
    { num: 1234.1, method: 'ceil', result: 1235 },
    { num: 1234.9, method: 'ceil', result: 1235 },
    { num: 1234.5, method: 'round', result: 1235 }
  ])('Integer pattern', async ({ num, method, result }) => {
    //@Given input number is <num>
    expect(typeof num).toBe('number');

    //@When rounding method is <method>
    expect(Math).toHaveProperty(method);

    //@Then rounded number is <result>
    expect(Math[method](num)).toEqual(result);
  });
});
```

---

## 📄 2. De Jest para Gherkin: `gen-doc`

Executando o comando de extração:
```bash
gen-doc pathTestsInput=./src/tests/math.test.ts \
  pathOutput=./docs/features/math.feature
```

Gera automaticamente o arquivo `.feature` padronizado:

```gherkin
@format-feature
Feature: Rounding methods of Math

Scenario Outline: Integer pattern
  Given input number is <num>
  When rounding with <method>
  Then rounded number is <result>

Examples:
| num    | method  | result |
| 1234.1 | "ceil"  | 1235   |
| 1234.5 | "round" | 1235   |
```

---

## ✍️ 3. De Gherkin para Jest: `gen-test`

Quando novos cenários de negócio são adicionados no arquivo `.feature` por analistas/QA:

```bash
# Faz backup do teste original
mv src/tests/math.test.ts src/tests/math-orig.test.ts

# Regenera e sincroniza o código TypeScript do Jest
gen-test pathTestsInput=src/tests/math-orig.test.ts \
  pathGherkinInput=docs/features/math.feature \
  pathOutput=src/tests/math.test.ts
```

* **Vantagem:** O código do Jest é atualizado automaticamente para refletir a nova tabela de exemplos ou novos passos, sem escrita manual repetitiva.

---

## 📊 4. Relatórios Executáveis: `gen-report`

A ferramenta permite gerar relatórios visuais com o layout do Cucumber a partir das execuções do Jest:

```bash
gen-report pathTestsInput=src/tests/math-orig.test.ts \
  pathFeatureInput=docs/features/math.feature
```

* **Benefícios:**
  * Relatório em HTML claro e intuitivo para stakeholders.
  * Exibe call stacks e diagnósticos detalhados para testes que falharam.
  * Rastreabilidade total entre requisitos de negócio e falhas técnicas.

---

## 🔬 Diferenciais e Recursos Avançados

* **Não interfere na execução padrão:**
  * O Jest continua rodando `npm test` normalmente em CI/CD sem dependências extras em runtime.
* **Test Oracle Experimental:**
  * O projeto inclui um servidor experimental de *Test Oracle* para auxiliar na inferência de asserções e comportamento esperado.
* **Open Source:**
  * Repositório oficial aberto pela ByteDance/TikTok no GitHub:
  * [`github.com/tiktok/jest-bdd-generator`](https://github.com/tiktok/jest-bdd-generator)

---

## 🎓 Conclusão & Principais Aprendizados

1. **Preservação de Ferramental:** Não foi necessário substituir o Jest ou reescrever a suíte de testes.
2. **Ponte entre Negócio e Engenharia:** Comentários semânticos + Gherkin aproximam a equipe de produto da implementação real.
3. **AST como Alavanca de DX:** A transformação de código TypeScript possibilita documentação viva e sincronização bidirecional sem esforço manual redundante.

---

<!-- _class: lead -->
# Obrigado! 👏
### Dúvidas ou Perguntas?

**Referência:** [TikTok Developers Blog — Make your tests readable with jest-bdd-generator](https://developers.tiktok.com/blog/jest-bdd-generator)
