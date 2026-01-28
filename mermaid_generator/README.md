# Mermaid Flow Generator Agent 🧜‍♂️📊

Este projeto implementa um sistema de agentes inteligentes capazes de transformar descrições informais de processos em diagramas **Mermaid.js** profissionais e sintaticamente corretos. Utilizando a biblioteca `google.adk` e o modelo `gemini-2.5-flash`, o sistema utiliza uma abordagem multi-agente para garantir precisão lógica e visual.

## 🚀 Arquitetura de Agentes

O projeto utiliza um `SequentialAgent` que orquestra a comunicação entre sub-agentes especializados:

1.  **Interpreter Agent**: O "Cérebro" analista. Ele recebe o texto desestruturado e gera um **JSON Semântico**.
    * Identifica atores, decisões (IF/ELSE) e pontos de erro.
    * Garante que a lógica do fluxo esteja coerente antes da geração do código.
2.  **Mermaid Agent**: O "Compilador" visual. Ele traduz o JSON para a sintaxe Mermaid.
    * Aplica estilos específicos: `([ ])` para início/fim, `{ }` para decisões e `[ ]` para processos.
3.  **Reviewer Agent**: O "Auditor" de sintaxe.
    * Corrige quebras de linha, aspas obrigatórias e garante que o código seja renderizável em qualquer editor Mermaid.

---

## 🛠️ Tecnologias e Configurações

* **Modelo Core**: `gemini-2.5-flash`
* **Framework**: `google.adk`
* **Linguagem**: Python

### Estrutura de Arquivos
* `agent.py`: Definição e encadeamento dos agentes (`LlmAgent` e `SequentialAgent`).
* `prompts.py`: Engenharia de prompt detalhada com instruções de sistema e exemplos *few-shot*.

---

## 📝 Exemplo de Processamento

### 1. Entrada do Usuário (Texto Informal)
> "Se o usuário estiver logado, ele vai para o dashboard. Se não, vai para o login. No login, se ele errar a senha 3 vezes, bloqueia a conta."

### 2. Saída do Interpreter (JSON Interno)
```json
{
  "contexto": "Fluxo de Autenticação",
  "tipo_diagrama": "flowchart",
  "elementos": [
    {"id": "inicio", "label": "Verificar Login", "tipo": "decisao"},
    {"id": "dash", "label": "Dashboard", "tipo": "fim"},
    {"id": "err", "label": "Erro de Senha", "tipo": "decisao"}
  ],
  "conexoes": [...]
}