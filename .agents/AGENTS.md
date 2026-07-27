# Diretivas de Operação do Agente (AGENTS.md)

Este arquivo define as regras fundamentais que devem ser rigorosamente seguidas pelo assistente (Antigravity/Agente) em todas as tarefas realizadas no workspace.

## 1. Fluxo de Trabalho com Git (Obrigatório)

Em **qualquer** tarefa que envolva alteração, criação ou remoção de código/arquivos, você DEVE seguir ESTE fluxo de versionamento:

1. **Commit de Segurança (Antes das Alterações):**
   - Antes de iniciar qualquer modificação no código, verifique o estado do repositório (`git status`).
   - Se houver alterações pendentes ou se for necessário registrar o estado anterior à intervenção, faça um commit garantindo um ponto de restauração seguro:
     ```bash
     git add .
     git commit -m "chore: checkpoint antes de iniciar tarefa [resumo da tarefa]"
     ```
   - *Nota: Se o working directory já estiver totalmente limpo (nada a commitar), registre isso no raciocínio antes de proceder.*

2. **Commit de Resumo (Após as Alterações):**
   - Imediatamente após finalizar e validar as alterações solicitadas pelo usuário, faça um commit resumindo detalhadamente a tarefa realizada:
     ```bash
     git add .
     git commit -m "feat/fix/docs: [resumo detalhado da tarefa concluída]"
     ```

## 2. Boas Práticas Gerais
- **Integridade do Código:** Mantenha a documentação e os comentários originais de partes do código que não estão sendo diretamente modificadas na tarefa atual.
- **Precisão nas Alterações:** Realize mudanças direcionadas e limpas, garantindo que o histórico de commits reflita precisamente o escopo de cada solicitação do usuário.
