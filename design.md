# design.md · Caqui Invest

Guia de design para quem constrói a interface da Caqui Invest, seja pessoa ou agente de IA. Leia antes de escrever qualquer tela. Fonte visual: [Figma · Caqui Invest Kit de UX de confiança](https://www.figma.com/design/tl9FFynv0PPlTdnLkGVPPb), página **Componentes**.

> Base visual: [shadcn/ui](https://ui.shadcn.com/) com tamanhos e contrastes ajustados para acessibilidade (ver 3.1.1). A Caqui é fictícia. Dados, taxas e pessoas são sintéticos. Nada aqui pode imitar marca real.

## 1. Para quem e por quê

- **Pessoa-guia:** Dona Marta, 63 anos, primeiro CDB, quer ver o dinheiro a cada passo. Se a interface funciona para ela, funciona para o Rafael (27 anos, quer resposta em 30 segundos).
- **Dado:** 14 dos 50 clientes sintéticos têm 60 anos ou mais.
- **Promessa da interface:** o cliente sempre vê **o que está acontecendo** (status, data, fonte) e sempre tem **uma saída** (pessoa, bloqueio, voltar).

## 2. Regras que não se quebram

1. **Nenhum texto abaixo de 16px.** Texto sempre em cinza (zinc); cor fica para ação, status e segurança.
2. **Todo controle tocável tem no mínimo 48px de altura.**
3. **Contraste AA:** 4,5:1 para texto, 3:1 para bordas de controles e ícones que carregam informação.
4. **Cor nunca é a única informação.** Status tem ícone e texto, seleção tem check ou ponto, erro tem ícone e frase.
5. **Rótulo sempre visível.** Placeholder não é rótulo.
6. **Foco visível no teclado:** anel duplo, com 2px de `--cor-superficie` colado ao elemento e 2px de `--cor-tinta` por fora (ver 3.1).
7. **Toda frase factual mostra a fonte** (artigo `KB-xxx`, operação `OP-xxxxx` ou posição `P-xxxx`) com o componente **Chip de fonte**.
8. **"Falar com uma pessoa" fica fixo no rodapé** de toda tela de atendimento. Fora das 8h–20h, ele vira protocolo com horário de retorno.
9. **Sinal de golpe troca a tela inteira** para o fluxo de segurança. Não vira mais uma mensagem.
10. **Datas, IR e rendimento vêm do motor de cálculo.** O LLM só redige. Nenhum prazo é inventado.
11. **Nenhuma recomendação de investimento.** Pedido de recomendação leva para o especialista.

## 3. Tokens

### 3.1 Cor

Base neutra na escala zinc (a mesma do shadcn/ui) e três cores de apoio com papel fixo: **verde** para ação e concluído, **laranja** para em andamento, **vermelho** só para segurança.

| Token | Hex | Uso | Contraste no branco |
| --- | --- | --- | ---: |
| `--cor-tinta` | `#09090B` | Texto principal (zinc-950) | 19,9:1 |
| `--cor-suave` | `#6B6B73` | Texto secundário e borda de campo | 5,3:1 (4,8:1 no zinc-100) |
| `--cor-linha` | `#E4E4E7` | Divisores (zinc-200), nunca texto nem limite único de controle | 1,3:1 |
| `--cor-fundo` | `#F4F4F5` | Fundo de tela e superfícies secundárias (zinc-100) | |
| `--cor-superficie` | `#FFFFFF` | Cards e campos | |
| `--cor-primaria` | `#1E4D33` | Verde Caqui: ação primária, seleção, concluído | 9,7:1 |
| `--cor-primaria-suave` | `#E8F0EA` | Fundo de concluído e de item ativo | verde sobre ele 8,4:1 |
| `--cor-destaque` | `#D95E00` | Laranja: só "em andamento" (ponto atual, progresso, ícone) | 3,8:1 |
| `--cor-destaque-suave` | `#FFF1E6` | Fundo de atenção e de "em andamento" | |
| `--cor-perigo` | `#B3261E` | Vermelho: só segurança e erro | 6,5:1 |
| `--cor-perigo-suave` | `#FDECEA` | Fundo de alerta de segurança | vermelho sobre ele 5,7:1 |
| `--cor-desabilitado` | `#A1A1AA` | Desabilitado (zinc-400), sempre com motivo escrito | 2,6:1 |

**Como usar:**
- Texto é sempre cinza: `--cor-tinta` ou `--cor-suave`. Cor em texto só em rótulo de status (verde em "Liquidada", vermelho em segurança).
- O laranja nunca é texto: 3,8:1 serve para ícone e barra, não para corpo.
- Nunca use `zinc-400` ou mais claro em texto.
- Separação por espaço e por fundo (`--cor-fundo` x `--cor-superficie`), não por borda. Borda só em campo de formulário e botão secundário.

**Foco:** anel duplo, 2px branco colado ao elemento e 2px `--cor-tinta` por fora. Passa sobre qualquer fundo.

### 3.1.1 Relação com o shadcn/ui

| shadcn | Caqui | Por quê |
| --- | --- | --- |
| `--background` branco | `--cor-fundo` zinc-100, cards brancos | Separar sem borda |
| `--primary` zinc-900 | `--cor-primaria` verde | Identidade da Caqui |
| `--muted-foreground` zinc-500 (4,8:1) | `#6B6B73` (5,3:1) | Ainda passa AA sobre zinc-100 |
| `--border` / `--input` zinc-200 | divisor zinc-200; campo `#6B6B73` | zinc-200 tem 1,3:1 e falha no WCAG 1.4.11 em campo |
| `text-sm` (14px) | 16px mínimo | 14 de 50 clientes têm 60+ |
| `h-9` (36px) | 48px mínimo | Alvo de toque |
| `--radius` 0,625rem | 10px controles, 14px cards | Igual em espírito |

### 3.2 Tipografia

Família única: **Inter** (400, 500, 600). Números de dinheiro com `font-variant-numeric: tabular-nums`.

| Estilo | Tamanho / altura | Peso | Uso |
| --- | --- | --- | --- |
| Display | 32 / 40 | 600 | Título de impacto (tela de golpe) |
| Título | 24 / 32 | 600 | Título de tela |
| Subtítulo | 20 / 28 | 600 | Título de card ou seção |
| Valor | 28 / 36 | 600 | Valores em R$ |
| Corpo | 16 / 24 | 400 | Texto corrido |
| Corpo destaque | 16 / 24 | 600 | Ênfase, rótulo de botão |
| Rótulo | 16 / 24 | 500 | Rótulo de campo, chip, badge |

### 3.3 Espaçamento, raio e tamanho

| Token | Valor |
| --- | ---: |
| `--espaco-1` | 4px |
| `--espaco-2` | 8px |
| `--espaco-3` | 12px |
| `--espaco-4` | 16px |
| `--espaco-6` | 24px |
| `--espaco-8` | 32px |
| `--espaco-12` | 48px |
| `--raio-sm` | 8px (chip de fonte) |
| `--raio-md` | 10px (botão, campo, alerta) |
| `--raio-lg` | 14px (card) |
| `--raio-pill` | 999px (chip de filtro, badge) |
| `--alvo-toque` | 48px |

Margem lateral de tela: 16px. Espaço entre cards: 12–16px. Padding de card: 16px.

**Elevação:** sem sombra e quase sem borda. Card branco sobre fundo zinc-100. A única sombra é a do item selecionado no controle segmentado (0 1px 3px, 8%).

### 3.4 CSS pronto para colar

```css
:root {
  --cor-tinta: #09090B;
  --cor-suave: #6B6B73;
  --cor-linha: #E4E4E7;
  --cor-fundo: #F4F4F5;
  --cor-superficie: #FFFFFF;
  --cor-primaria: #1E4D33;
  --cor-primaria-suave: #E8F0EA;
  --cor-destaque: #D95E00;
  --cor-destaque-suave: #FFF1E6;
  --cor-perigo: #B3261E;
  --cor-perigo-suave: #FDECEA;
  --cor-desabilitado: #A1A1AA;

  /* nomes do shadcn/ui apontando para os tokens da Caqui */
  --background: var(--cor-fundo);
  --foreground: var(--cor-tinta);
  --card: var(--cor-superficie);
  --primary: var(--cor-primaria);
  --primary-foreground: #FFFFFF;
  --muted: var(--cor-fundo);
  --muted-foreground: var(--cor-suave);
  --border: var(--cor-linha);
  --input: var(--cor-suave);
  --destructive: var(--cor-perigo);
  --ring: var(--cor-tinta);
  --radius: 10px;

  --fonte: "Inter", system-ui, sans-serif;
  --texto-display: 600 2rem/2.5rem var(--fonte);
  --texto-titulo: 600 1.5rem/2rem var(--fonte);
  --texto-subtitulo: 600 1.25rem/1.75rem var(--fonte);
  --texto-valor: 600 1.75rem/2.25rem var(--fonte);
  --texto-corpo: 400 1rem/1.5rem var(--fonte);
  --texto-corpo-destaque: 600 1rem/1.5rem var(--fonte);
  --texto-rotulo: 500 1rem/1.5rem var(--fonte);

  --espaco-1: 4px; --espaco-2: 8px; --espaco-3: 12px; --espaco-4: 16px;
  --espaco-6: 24px; --espaco-8: 32px; --espaco-12: 48px;
  --raio-sm: 8px; --raio-md: 10px; --raio-lg: 14px; --raio-pill: 999px;
  --alvo-toque: 48px;
}

html { font-size: 100%; } /* respeita o zoom do sistema; nunca fixe em px */
body { font: var(--texto-corpo); color: var(--cor-tinta); background: var(--cor-fundo); }
/* anel duplo: visível sobre qualquer fundo */
:focus-visible { outline: 2px solid var(--cor-tinta); outline-offset: 2px; box-shadow: 0 0 0 2px #FFFFFF; }
.valor { font: var(--texto-valor); font-variant-numeric: tabular-nums; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
```

### 3.5 Tailwind (opcional)

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        tinta: "#09090B", suave: "#6B6B73", linha: "#E4E4E7",
        fundo: "#F4F4F5", superficie: "#FFFFFF",
        primaria: { DEFAULT: "#1E4D33", suave: "#E8F0EA" },
        destaque: { DEFAULT: "#D95E00", suave: "#FFF1E6" },
        perigo: { DEFAULT: "#B3261E", suave: "#FDECEA" },
        desabilitado: "#A1A1AA",
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"] },
      fontSize: {
        display: ["2rem", { lineHeight: "2.5rem", fontWeight: "600" }],
        titulo: ["1.5rem", { lineHeight: "2rem", fontWeight: "600" }],
        subtitulo: ["1.25rem", { lineHeight: "1.75rem", fontWeight: "600" }],
        valor: ["1.75rem", { lineHeight: "2.25rem", fontWeight: "600" }],
        corpo: ["1rem", { lineHeight: "1.5rem" }],
      },
      borderRadius: { sm: "8px", md: "10px", lg: "14px" },
      minHeight: { toque: "48px" },
    },
  },
};
```

Não use `text-xs` nem `text-sm` no produto.

## 4. Componentes

Todos estão no Figma com os mesmos nomes. Os nomes de variante são `Propriedade=Valor`.

| Componente | Variantes | Regras de uso | Acessibilidade no código |
| --- | --- | --- | --- |
| **Botão** | Tipo: Primário (verde), Secundário (contorno), Terciário (link), Segurança · Estado: Padrão, Foco, Desabilitado | Um primário por tela. O rótulo diz a ação ("Confirmar resgate", nunca "OK"). Segurança só no fluxo de golpe. Desabilitado sempre com o motivo escrito ao lado. | `<button>`; desabilitado com `aria-disabled` e texto explicativo ligado por `aria-describedby` |
| **Botão de ícone** | Tipo: Primário, Secundário · Ícone (troca) | 48×48. Usado em voltar e avançar. | `aria-label` obrigatório ("Voltar") |
| **Campo de texto** | Estado: Padrão, Foco, Erro, Desabilitado | Rótulo acima, ajuda abaixo com ícone. O erro diz como corrigir ("Digite até R$ 40.791,24"). Borda `--cor-suave`. | `<label for>`, `aria-describedby` na ajuda, `aria-invalid` no erro, `inputmode="decimal"` para valor |
| **Radio** | Selecionado: Sim, Não | Escolha única entre 2 e 5 opções, cada uma com texto completo (produto + saldo). | `fieldset` + `legend` |
| **Checkbox** | Selecionado: Sim, Não | Confirmação de entendimento antes de ação com dinheiro. | Área clicável inclui o texto |
| **Switch** | Selecionado: Sim, Não | Liga na hora, sem salvar. O texto descreve o que liga. | `role="switch"`, `aria-checked` |
| **Chip de filtro** | Selecionado: Sim, Não | Selecionado tem check e fundo musgo. | `aria-pressed` |
| **Chip de fonte** | texto | Sempre que houver fato: KB, OP ou P. | Pode ser link para o artigo |
| **Status da operação** | Liquidada, Em processamento, Pendente, Recusada | Espelha `status` de `operacoes.csv`. Ícone + texto. | Texto lido pelo leitor de tela; ícone `aria-hidden` |
| **Card de investimento** | texto | Diz se o valor é bruto ou líquido. Mostra a posição de origem. O card inteiro é o alvo. | Um único link ou botão envolvendo o card |
| **Linha de extrato** | Tipo: Saída, Entrada | Sinal + ou −, ícone de direção, número da operação e status. | Lista `<ul>` |
| **Barra de progresso** | texto | O número escrito é a informação; a barra só reforça. Laranja só aqui. | `role="progressbar"`, `aria-valuenow`, `aria-valuemax` |
| **Passo de linha do tempo** | Estado: feito, atual, futuro | Cada data traz o motivo ("02/11 é feriado"). Datas vêm do motor. | Lista ordenada `<ol>`, passo atual com `aria-current="step"` |
| **Alerta** | Tipo: Info, Atenção, Segurança · Mostrar ação | Ícone + título + texto + ação opcional. A borda esquerda de 4px reforça o tipo. | Info e Atenção: `role="status"`; Segurança: `role="alert"` |
| **Mensagem** | Autor: Cliente, Caqui | Cliente à direita em musgo. Caqui à esquerda, com fontes. | Região com `aria-live="polite"` |
| **Barra "Falar com uma pessoa"** | Status (texto) | Fixa no rodapé. Mostra a espera estimada, ou protocolo e horário fora do expediente. | Botão com texto completo, nunca só ícone |
| **Cabeçalho** | Mostrar voltar | O título é o `h1` da tela. | Voltar com `aria-label` |
| **Tab bar** | 4 itens | Início, Investir, Atendimento, Perfil. Rótulos sempre visíveis. Item ativo com indicador e peso. | `nav` + `aria-current="page"` |
| **Modal · Confirmar resgate** | conteúdo | Repete valor, origem, destino e data calculada. Checkbox de entendimento libera o botão. | `role="dialog"`, `aria-modal`, foco preso, Esc fecha |
| **Toast** | texto | Confirma o que aconteceu, com protocolo. Fica no mínimo 6s e nunca leva ação crítica. | `role="status"` |
| **Estado vazio** | texto | Explica o que vai aparecer e dá o próximo passo. | |
| **Estado de erro** | texto | Primeiro tranquiliza sobre o dinheiro. Oferece tentar de novo e pessoa. Nunca culpa o cliente. | Foco vai para o título do erro |
| **Ícones** | 21 ícones (Lucide, ISC) | 24px, traço de 2px, cor da variável. | Decorativo: `aria-hidden`; sozinho: `aria-label` |

## 5. Padrões de tela

| Padrão | Quando | Composição |
| --- | --- | --- |
| **Home** | Abertura do app | Ordem fixa: o que está em andamento, patrimônio (bruto e líquido rotulados), avisos de calendário, investimentos com liquidez escrita, pessoa a um toque, aprender sem recomendar, lembrete de segurança. Ver página "Home · Conceito" no Figma. |
| **Rastreio de resgate** | Qualquer resgate em andamento | Cabeçalho, card de resumo (valor + data de pagamento + "não sumiu"), linha do tempo, barra de pessoa |
| **Resposta com fonte** | Pergunta factual no atendimento | Mensagem da Caqui com a conta aberta (bruto, IR, líquido) + chips de fonte + respostas rápidas |
| **Golpe interrompe** | A triagem detecta sinal de golpe | Tela inteira `--cor-perigo`: o que fazer em 3 passos, "Bloquear acesso", "Falar com a segurança" (24h). A pergunta original fica salva no protocolo. |
| **Fora do horário** | Pedido de pessoa fora das 8h–20h | Protocolo, horário de retorno, alerta de segurança 24h. Nunca promete humano. |
| **Pedido de recomendação** | Cliente pede onde investir | Recusa em uma frase, agenda com especialista, conceitos que podem ser explicados |
| **Confirmação de dinheiro** | Antes de qualquer resgate ou aplicação | Modal de confirmação. Cliente 60+ com resgate total ou atípico: alerta e oferta de pessoa **antes** do modal. |

## 6. Voz e texto

- Frases curtas, com menos de 20 palavras. Uma ideia por frase.
- Responda ao medo antes da pergunta: "Seu dinheiro não sumiu" vem antes do prazo.
- Data sempre com dia da semana: "05/11/2026, quinta".
- Valores sempre com R$ e dizendo se são bruto ou líquido.
- Nada de jargão sem explicação: "cotização" vem com "1 dia útil após o pedido".
- Não sabe? Diga que não sabe e ofereça uma pessoa. Nunca invente prazo ou taxa.
- Nunca: "Recomendo", "melhor opção para você", "coloque em".

## 7. Checklist antes de publicar

- [ ] Nenhum texto abaixo de 16px (procure `text-xs`, `text-sm`, `font-size: 1[0-5]px`)
- [ ] Todo controle com 48px ou mais
- [ ] Zoom de 200% sem cortar conteúdo
- [ ] Navegação só por teclado, com foco visível em tudo
- [ ] Leitor de tela anuncia status, erros e mensagens novas
- [ ] Nenhum estado transmitido só por cor
- [ ] Toda frase factual com chip de fonte
- [ ] Barra "Falar com uma pessoa" presente em toda tela de atendimento
- [ ] Teste às 14h e às 23h: humano com espera, depois protocolo
- [ ] Teste de golpe no meio da frase: a tela troca na hora
- [ ] CPF sempre mascarado na tela e no log

## 8. Hipóteses de design ainda não validadas

Isto é intenção, não fato. Validar com pessoas antes de defender como resultado.

- Base neutra com verde Caqui transmite calma e confiança para quem vem da poupança, sem parecer genérica.
- A tela de golpe vermelha e cheia não paralisa a pessoa idosa.
- A linha do tempo proativa reduz os contatos de "onde está meu dinheiro".
- Corpo de 16px em todo o app não deixa o Rafael achando a interface "infantil".
