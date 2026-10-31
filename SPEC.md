# SPEC: Cadê meu dinheiro

**Grupo:** _(nomes)_
**URL pública:** _(link)_

> **Rascunho de partida.** Escrito antes da entrevista do grupo. Se o grupo escolher outro problema, reescrevam e anotem o porquê em "Decisões". Em toda conta, **dado** vem do case e **hipótese** ainda não foi validada.

## 1. Qual parte do problema?

"Onde está meu dinheiro" (aplicação, resgate, liquidação), com a Dona Marta como pessoa-guia.

- **Dado:** é o maior motivo, 12.960 de 48.000 contatos por mês (27%), com 34% de recontato em 7 dias. Na amostra de `conversas.csv`, o recontato é 44% e 36% das conversas terminam abandonadas.
- **Dado:** a resposta é determinística (calendário, corte das 16h, regras de liquidação), então dá para responder sem inventar. O bot atual errou o corte ou o fim de semana em 16 de 300 conversas.

## 2. Qual alavanca?

1. **Evitar o contato:** linha do tempo do resgate visível antes da dúvida, com data, motivo de cada etapa e fonte.
2. **Resolver sem humano:** o atendimento responde "onde está" com o motor de cálculo.
3. Camada obrigatória: **triagem de risco antes do LLM** (golpe, recomendação, injeção, vulnerável), porque as regras 4 e 5 valem para qualquer caminho.

## 3. Quanto isso move?

| Premissa | Valor | De onde veio |
| --- | --- | --- |
| Horas de atendente/mês no motivo, hoje | 1.728 h | Dado do case |
| Escala de 400 mil para 2 mi clientes | ×5 | Dado do case |
| Contatos evitados pela linha do tempo | 50% | **Hipótese** |
| Horas por atendente/mês | 154 h | Dado: 9.560 h / 62 |

**Conta:** 1.728 × 5 × 50% = 4.320 h/mês ≈ **28 atendentes**. A meta do case é tirar cerca de 32.600 h/mês (68% das 48.000 h na escala). Esta solução cobre cerca de 13% disso. Com a triagem mandando pedido de recomendação direto ao especialista (hipótese: 80% das 5.760 h na escala), chega a cerca de 27%. Nenhuma solução de um dia fecha os 68%.

**Como validar:** comparar o recontato em 7 dias entre clientes com e sem a linha do tempo.

## 4. Como a confiança aparece?

- Cada data mostra o motivo ("02/11 é feriado") e a fonte (`KB-006`, `OP-xxxxx`).
- A primeira frase responde ao medo: "Seu dinheiro não sumiu".
- "Falar com uma pessoa" fica fixo em toda tela, com espera estimada. Fora das 8h às 20h, protocolo e retorno a partir das 8h.
- Sinal de golpe troca a tela inteira pela de segurança, 24h.

## 5. O que fica de fora?

Login real, notificação real, aplicação e transferência, ações e multimercado no chat, voz e WhatsApp, e integração com sistema real de operações.

## 6. Como viabilizar?

O motor já é a regra de negócio. Próximo passo para a Caqui: ligá-lo ao sistema de operações real e rodar um piloto com clientes da parceria do varejista, medindo o recontato em 7 dias contra um grupo de controle.

## 7. Quais regras do case vocês tratam?

| # | Regra | Trata? | Como vira teste | Se não trata, por quê |
| --- | --- | --- | --- | --- |
| 1 | Liquidação | Sim | PT-01 a PT-05 + auditoria de `liquidacao_prevista` | |
| 2 | IR regressivo | Sim | PT-06 a PT-09 (borda 180/181) | |
| 3 | Comparação com a poupança | Sim | PT-10 a PT-12 | |
| 4 | Sem recomendação | Sim | PT-13 a PT-17, PT-36 + recall nas conversas | |
| 5 | Golpe | Sim | PT-18 a PT-21 + recall nas conversas (hook bloqueia queda) | |
| 6 | Cliente vulnerável | Sim | PT-22 a PT-24 | |
| 7 | Reclamação e cancelamento | Sim | PT-25, PT-26 | |
| 8 | Sem doom loop | Sim | PT-27, PT-28 | |
| 9 | Não sabe, diz que não sabe | Sim | PT-29 a PT-31 (KB-007 fora) | |
| 10 | Dados pessoais | Sim | PT-32, PT-33 + hook bloqueia CPF sem máscara | |
| 11 | Instrução escondida | Sim | PT-34 a PT-36 + recall nas conversas | |
| 12 | Horário | Sim | PT-37, PT-38 | |

Itens de "O que vale para qualquer caminho": todos se aplicam, porque a solução conversa com o cliente.

## Decisões

| Quando | Decisão | Por quê |
| --- | --- | --- |
| 30/10 | LLM não calcula data nem IR; o motor calcula | Regras 1 a 3 são onde a IA costuma errar |
| 30/10 | KB-007 fora da base consultada | Desatualizado (corte de 15h) |
| 30/10 | Triagem medida contra as conversas, não só contra o checador | Passava 40/40 e perdia 8 de 20 golpes |
