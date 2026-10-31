# Onde a IA errou

Anotar na hora, não no fim do dia. Um caso por bloco.

## 1. A triagem passava em todos os testes e perdia golpes reais

- **O que a IA fez:** escreveu a triagem de risco por padrões de texto. Passou 40/40 no `checar_respostas.py`.
- **Como percebemos:** rodamos a mesma triagem contra os rótulos das 300 conversas (`motor/avaliar_triagem.py`). Ela pegava só 12 de 20 golpes e 1 de 12 clientes vulneráveis. Os testes estavam verdes e a regra estava quebrada.
- **O que mudou:** novos padrões (app de acesso remoto, link com senha, "esqueça a política") e vulnerabilidade usando a idade do cadastro (60+, KB-028). Recall foi a 100%, mas é otimista: os padrões foram ajustados olhando os mesmos dados. A verificação contra as conversas entrou no hook.

## 2. (próximo)

- **O que a IA fez:**
- **Como percebemos:**
- **O que mudou:**
