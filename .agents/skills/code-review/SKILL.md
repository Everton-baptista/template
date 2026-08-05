---
name: code-review
description: "Skill avançada para revisão de código, auditoria de segurança OWASP, verificação de padrões SOLID e otimização de performance."
---

# Skill: Revisão de Código & Auditoria de Arquitetura

Ao agir como Revisor de Código ou Engenheiro de Software Principal, siga rigorosamente este protocolo em 4 etapas:

## 1. Auditoria de Segurança (OWASP Top 10)
- Inspecione sanitização de dados e entradas (prevenção contra SQL Injection, XSS, Command Injection).
- Verifique segredos ou chaves API expostas em código.
- Valide gerenciamento de exceções e tratamento de erros (evitar exceções genéricas ou silenciosas).

## 2. Padrões de Projeto & SOLID
- **Single Responsibility**: Cada classe ou módulo deve ter uma única razão para mudar.
- **DRY (Don't Repeat Yourself)**: Identifique duplicações de código e proponha abstrações reusáveis.
- **KISS (Keep It Simple, Stupid)**: Evite complexidade desnecessária ou sobre-engenharia.

## 3. Qualidade & Testabilidade
- Verifique se as funções possuem tipos bem definidos (Type Annotations em Python / TypeScript).
- Garanta que a função possa ser facilmente testada com testes unitários isolados (mocks/stubs).

## 4. Formato do Feedback
Forneça o feedback no seguinte formato em Markdown:
- 🔴 **Erros Críticos / Segurança** (se houver)
- 🟡 **Otimizações & Boas Práticas**
- 🟢 **Pontos Fortes**
- 💡 **Código Sugerido Refatorado** (com diffs ou blocos completos)
