# Motor Caqui (referência de preparação)

Código de apoio para o Hands On. Python 3.9+, sem dependências.

## Ideia

O LLM conversa e extrai parâmetros (produto, data do pedido, posição). **Quem calcula prazo, IR e rendimento é este código.** O LLM nunca faz conta de data nem de imposto. Cada resultado volta com a fonte (artigo da base ou dado da conta), que é o item 3 do case ("toda informação factual mostra de onde veio").

## Arquivos

| Arquivo | O que faz |
| --- | --- |
| `caqui_motor.py` | Calendário, dia-base com corte das 16h, liquidação por produto (regra 1), IR regressivo (regra 2), comparação líquida com a poupança (regra 3), horário do humano (regra 12) e triagem de risco por padrões (regras 4, 5, 6, 11) |
| `gerar_respostas.py` | Responde as 40 perguntas de teste e grava o JSONL do checador |
| `avaliar_triagem.py` | Mede a triagem contra os rótulos das 300 conversas |

## Rodar

```bash
R=caminho/para/caqui-invest
python3 gerar_respostas.py $R > respostas.jsonl
python3 $R/ferramentas/checar_respostas.py respostas.jsonl
python3 avaliar_triagem.py $R
```

## Resultado (30/10/2026)

- Checador oficial: **40/40** nas pistas, e os números das regras 1 a 3 batem com a `resposta_esperada` (conferido linha a linha).
- Auditoria de `liquidacao_prevista`: 125 resgates, 62 com data no arquivo, **0 divergências** com o motor. Outros 48 vinham vazios e o motor calcula. Os 15 restantes não têm data porque o resgate é recusado (8 sem liquidez diária) ou está em carência de LCI (7).
- Triagem contra as 300 conversas rotuladas:

| Sinal | Recall | Precisão |
| --- | ---: | ---: |
| golpe | 100% | 100% |
| injeção | 100% | 100% |
| recomendação | 100% | 92% |
| vulnerável | 100% | 15% |

## Limites (leia antes de usar)

- **Os padrões foram ajustados olhando estes mesmos dados.** A primeira versão passava 40/40 no checador e mesmo assim só pegava 12 de 20 golpes e 1 de 12 vulneráveis nas conversas. Isso dá um bom "momento em que a IA errou" para a apresentação. Os 100% acima são otimistas: com frases novas, o recall vai cair. No produto, use um classificador LLM e deixe estes padrões como rede de segurança.
- **Vulnerável com 15% de precisão:** idade 60+ sozinha marca gente demais. A leitura de produto é: idade dá **prioridade na fila** (KB-028), e confusão ou pressão de terceiro **interrompe e encaminha**. Hoje o motor trata as duas coisas igual.
- Nas regras 4 a 12, as respostas são modelos escritos à mão. Servem de gabarito de tom e de ação, não de conversa real.
- Protocolo e tempo de espera são simulados.
- Combine com o grupo antes de usar: o espírito do evento é construir no dia.
