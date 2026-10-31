# Caqui Invest — Design System

Version: 0.2 (working draft)
Status: Proposal; not approved for production

## Brand strategy
- Audience: beginner investors.
- Positioning: accessible investment brokerage with a sophisticated, non-elitist identity.
- Value proposition: security and transparency; digital self-service with human support.
- Voice: approachable, sophisticated, precise, never promising returns.
- Visual direction: abstract editorial photography, custom typographic wordmark without literal fruit or leaves, Manrope + Inter.

## Principles
1. Clarity over decoration.
2. Show risks, fees, liquidity, taxation and terms at the decision point.
3. Progressive disclosure, never conceal essential financial information.
4. One primary action per decision region.
5. Shared tokens, responsive patterns designed for each context.

## Brand primitives
| Token | Hex |
|---|---|
| brand.moss | #0B2B18 |
| brand.ivory | #DDD2B7 |
| brand.leafy | #82A591 |
| brand.orange | #D95E00 |

## Neutral primitives (draft)
| Token | Hex |
|---|---|
| neutral.50 | #FAFAF7 |
| neutral.100 | #F4F5F0 |
| neutral.200 | #E5E7E1 |
| neutral.300 | #CDD3CA |
| neutral.400 | #9BA69C |
| neutral.500 | #66736B |
| neutral.700 | #35473B |
| neutral.900 | #17251D |

## Semantic tokens — light
| Token | Reference |
|---|---|
| background.default | neutral.50 |
| background.surface | #FFFFFF |
| background.subtle | neutral.100 |
| foreground.default | neutral.900 |
| foreground.muted | neutral.500 |
| border.default | neutral.200 |
| action.primary | brand.moss |
| action.on-primary | #FFFFFF |
| action.accent | brand.orange |
| focus.ring | brand.orange (provisional; test against surrounding surfaces) |
| feedback.success | #247A4B |
| feedback.danger | #B63C35 |

Color meaning: orange is a brand accent, not a success indicator; financial gain/loss should never rely on color alone. All foreground/background combinations require WCAG contrast verification. Target >= 4.5:1 normal text, >= 3:1 large text and essential UI graphics.

## Typography
- Display: Manrope Semibold 48/56
- H1: Manrope Semibold 36/44
- H2: Manrope Semibold 28/36
- H3: Manrope Semibold 22/30
- Body large: Inter Regular 16/24
- Body: Inter Regular 14/22
- Caption: Inter Regular 12/18 (noncritical)
- Financial value: Inter Semibold 28/36; tabular numerals
- Use Brazilian locale currency formatting, e.g. R$ 24.850,00.

## Spacing, radii and sizing
- Spacing primitives: 4, 8, 12, 16, 24, 32, 48 px; extend to 64 and 80 for page composition.
- Radius: 4 (sm), 8 (md), 12 (lg), 16 (xl) px.
- Control heights: 32 (compact), 40 (default), 48 (comfortable/mobile) px.
- Interactive touch targets: aim for at least 44x44 CSS px on mobile.
- Responsive layout proposal: mobile < 768 px, tablet 768–1199 px, desktop >= 1200 px. These are starting breakpoints, not device classifications.
- Desktop content max-width: 1200 px; mobile horizontal padding 16 px, desktop 24–32 px.

## Component specifications (v0.2)

### Button
- Variants: primary, secondary, tertiary, destructive, link.
- Sizes: sm 32, md 40, lg 48 px.
- States: default, hover, pressed, focus-visible, disabled, loading.
- Primary: moss background, white text, radius 8, 16 px horizontal padding minimum.
- Disabled: do not convey state by opacity alone; remove action and provide explanation when useful.
- Loading: preserve width; prevent duplicate submission; announce status accessibly.
- Icon-only buttons require accessible labels.

### Text field
- Variants: default, with prefix/suffix, search, currency, password.
- States: empty, filled, focus, invalid, disabled, read-only, loading.
- Persistent visible label, optional hint and error text; do not rely on placeholder as label.
- Error: icon + text, not color alone.
- Currency: accept locale-aware entry and format on blur; retain precision during editing.

### Card
- Variants: summary, product, educational, action, advisory.
- States: static, interactive default/hover/focus, loading skeleton, empty, error.
- Surface white, subtle border, radius 12, padding 16–24 px.
- Interactive cards require a clear action and keyboard accessibility.

### Badge / status
- Variants: neutral, positive, warning, negative, informational.
- Status labels must remain explicit; never use only color.
- Distinguish product risk level from performance change.

### Table
- Right-align numeric values; tabular numerals.
- Sort states: none, ascending, descending; indicate active sort textually.
- Mobile: prefer meaningful row-to-detail transformation over horizontal truncation.
- Provide empty, loading, error, and no-results states.

### Financial chart
- State period and unit; explain whether data are gross/net and historical/projected.
- Provide text or tabular alternative.
- Avoid implying guaranteed returns or using decorative upward trends.
- Gains/losses require signs and text in addition to colors.

### Navigation
- Desktop: sidebar for authenticated area; top navigation for public website.
- Mobile: bottom navigation for 3–5 top-level destinations; secondary actions inside contextual screens.
- Clearly distinguish active, hover and keyboard focus states.

## Product patterns
- Portfolio overview: total invested/patrimony, time period, performance methodology, allocation, next actions.
- Product details: risk, liquidity, minimum, fees, tax, issuer and protections where applicable, shown before confirmation.
- Investment confirmation: amount, destination, settlement, cost, risk disclosure and explicit confirmation.
- Human support: visible entry point; clear expected response channel/time, never invent SLA.
- Education: contextual explanations without blocking experienced users.

## Figma structure
Pages:
00 Cover & Guidelines
01 Brand Foundations
02 Product Foundations
03 Components
04 Patterns & Templates

Variable collections:
- Primitives: color, spacing, radius, dimensions.
- Semantic: background, foreground, border, action, feedback, focus (mode: Light; Dark reserved).
- Layout: breakpoints, grid, container and spacing roles.

Component naming examples:
- Button / Primary / Medium
- Input / Text / Default
- Card / Portfolio / Summary
- Navigation / Sidebar / Item
- Feedback / Alert / Warning

Prefer component properties for variant, size, state, icon visibility, and content. Use Auto Layout, constraints and accessible annotations.

## Open decisions
- Final proprietary wordmark design and trademark check.
- Final abstract image/graphic library.
- Semantic contrast audit and interactive state color values.
- First reference flow and prioritized components.
- Regulatory and legal review for actual brokerage deployment.

## Implementation notes
Suitable for React + Tailwind + shadcn/ui; map semantic Figma variables to CSS custom properties, not direct primitive hex values in components. This document is a design specification, not an importable Figma library.

---

## v0.3 — Dashboard & Portfolio experience (2026-10-31)
Status: design proposal; pending user review and accessibility validation. All financial values and products in mockups are illustrative, not factual product offers.

### Decisions
- Primary reference flow: dashboard and investment portfolio.
- Desktop navigation: hybrid. Global topbar for search, notifications, help and account; persistent left sidebar for primary destinations; local tabs within content. Avoid a permanent third navigation rail.
- Responsive system: same semantic foundations and component APIs, different layout and navigation compositions for desktop and mobile.
- Information density: balanced, with progressive disclosure. Never conceal risk, fees, liquidity, taxation or material terms at investment confirmation.
- Primary actions use Deep Moss; orange is an accent, not a competing primary action or semantic success indicator.

### Information architecture
Primary destinations: Início, Carteira, Investir, Aprender, Atendimento. Account and settings via topbar profile. Desktop sidebar may collapse. Mobile bottom bar: Início, Carteira, Investir, Aprender, Mais (Atendimento prominently available from Mais and contextual help); 5 items maximum. Search and notifications in mobile header. The labels are provisional and should be tested with beginners.

### Screen specifications
**Desktop Dashboard — 1440px reference**
- Global topbar 64px tall. Sidebar 224px expanded, 72px collapsed. Content maximum 1200px with 24px gutters, responsive.
- Greeting with as-of timestamp, privacy toggle for financial values, and period control.
- Primary summary: patrimônio total, performance with explicit period and calculation basis, chart with accessible table alternative and loading/error/empty states.
- Allocation summary: category shares with both percentages and currency values; never rely solely on color.
- Actions: Investir, Transferir, Resgatar, Falar com especialista; show only contextually valid actions.
- Holdings: product name, type, current value, performance period, liquidity; sort/filter and link to details. Do not conflate cash flows and investment return.
- Educational next steps and human support after financial overview, not replacing critical data.

**Desktop Carteira**
- Portfolio totals and as-of timestamp; allocation by class; tabs: Posições, Movimentações, Rentabilidade.
- Posições table: Produto, Categoria, Saldo, Rentabilidade (with reference period), Liquidez, Ações. Support keyboard sorting and explicit sort order; avoid horizontal scroll at desktop widths.
- Details drawer or dedicated page: issuer, guarantees (when applicable), fees, taxation, maturity, liquidity, risks and relevant documents.

**Mobile Dashboard — 390px reference**
- Compact header with brand, notifications and account. Bottom navigation persistent where appropriate; avoid covering content or keyboard.
- Summary card first; chart with selectable periods and textual summary; quick actions in 2×2 grid; allocation list with text labels and values; recent holdings preview; help entry point.
- 16px side gutters, minimum 44×44px touch targets, safe-area insets; use no horizontal scroll for core data.

**Mobile Carteira**
- Summary and period selector; segmented local tabs (Posições / Movimentações / Rentabilidade).
- Holdings as stacked rows/cards with product, current value, category and liquidity; details open a dedicated view. Long labels wrap, monetary values remain legible at 200% text zoom.

### Responsive layout tokens
| Token | Value |
|---|---|
| breakpoint.sm | 640px |
| breakpoint.md | 768px |
| breakpoint.lg | 1024px |
| breakpoint.xl | 1280px |
| layout.mobile.gutter | 16px |
| layout.tablet.gutter | 24px |
| layout.desktop.gutter | 32px |
| layout.desktop.sidebar | 224px |
| layout.desktop.sidebar.collapsed | 72px |
| layout.desktop.topbar | 64px |
| layout.mobile.bottomNav | 64px + safe area |
| layout.content.max | 1200px |

Breakpoints are implementation starting points, not device categories; test intermediate widths and content-driven behavior.

### Component additions
- AppShell: desktop(topbar + sidebar + main), mobile(header + bottom nav + main).
- NavItem: default, hover, active, focus-visible, disabled; icon + label and aria-current.
- PortfolioSummary: loading, populated, empty, error, hidden-values; amount, as-of timestamp, period and trend.
- PerformanceChart: 1M, 3M, 6M, 1A, all; tooltip keyboard equivalent; tabular alternative; empty/error/loading; label baseline and returns methodology.
- AllocationBreakdown: chart + legend/list; percentages and currency values; no color-only encoding.
- HoldingRow: product, category, balance, return period, liquidity, details; loading/empty/error.
- QuickAction: default, focus, disabled, pending; optional contextual explanation.
- FilterTabs: selected, unselected, focus, disabled; semantic tab behavior only when controlling tabpanels.
- PrivacyToggle: visible/hidden balances; must also hide chart tooltip and accessible descriptions containing sensitive amounts.
- SupportEntry: contextual assistance and handoff to a human; clear availability status without fabricated response-time guarantees.

### Figma component conventions
- `Navigation/AppShell`, `Navigation/SidebarItem`, `Navigation/BottomNavItem`
- `DataDisplay/PortfolioSummary`, `DataDisplay/AllocationBreakdown`, `DataDisplay/HoldingRow`, `DataViz/PerformanceChart`
- `Actions/QuickAction`, `Controls/PeriodSelector`, `Controls/PrivacyToggle`, `Support/EntryPoint`
- Component properties: `variant`, `size`, `state`, `icon`, `label`, `showDescription` as appropriate. Prefer boolean/text properties and instance swaps over detached duplicates.
- Use Auto Layout, constraints, variables and accessible text styles. Create desktop and mobile composition variants rather than scaling components proportionally.

### Interaction and accessibility requirements
- WCAG 2.2 AA target; verify actual contrast, keyboard order, focus indicator, semantic labels and zoom/reflow.
- Financial trends require positive/negative labels, comparison period and a non-color indicator. Orange is not a warning or positive-return semantic by default.
- Loading: skeleton or progress label; empty: explanation and next action; error: recovery and timestamp of last valid data where known.
- Show updated-at timestamp, data source or calculation method where material; distinguish market movement from deposits and withdrawals.
- Never imply guaranteed performance; illustrative data must be labeled.
- Confirm irreversible or financially consequential actions with a summary of material terms.

### Implementation guidance
- React + Tailwind + shadcn/ui is the reference stack, not a mandatory dependency.
- Keep semantic CSS variables separate from raw brand values; use `font-variant-numeric: tabular-nums` for balances and tables.
- Build accessible table and chart alternatives; avoid hardcoding return signs or colors into domain logic.
- Test 320px, 390px, 768px, 1024px and 1440px widths, keyboard-only, reduced motion and 200% text zoom.

### Open decisions for v0.4
1. Is the main dashboard goal portfolio monitoring or guidance toward a next investment?
2. Should financial amounts be visible by default or hidden until explicitly revealed?
3. Which portfolio performance metric should lead: nominal return, percentage return or benchmark-relative return?
4. Confirm the five-item mobile navigation taxonomy with usability testing.

---

## v0.4 — Dashboard & Carteira UX refinement (2026-10-31)
**Approved:** dashboard priority B (balanced monitoring + next-step guidance); privacy A (balances shown by default, user can hide). Status: specification draft, not implemented or published to Figma.

### Trust and financial precision
- Never use evaluative copy such as "Seu patrimônio está rendendo bem" without objective criteria and user context. Prefer "Veja como seu patrimônio mudou no período".
- Separate **patrimônio atual**, **valor investido**, **resultado acumulado**, **aportes/resgates** and **saldo disponível**; never present cashflow as returns.
- Every performance figure must label period, calculation basis (gross/net), source, and last update; show explicit `—` if unknown, not 0%.
- Display both amount and percentage when supported, with matching dates and methodology. Do not compare to CDI without a valid benchmark-series calculation.
- Avoid predictive rising-line decoration; graph axes and period markers must be meaningful. Use text equivalents and keyboard-accessible data table.
- Product risks, liquidity, costs and settlement conditions remain discoverable from holding detail. No guaranteed-return framing.

### Desktop Dashboard proposed hierarchy
1. Topbar: brand, global search, notifications, help, account. Left sidebar: Início, Carteira, Investir, Aprender, Atendimento; active state unique.
2. Page heading "Visão geral" with `Dados atualizados em ...` and contextual support.
3. Financial overview: patrimônio amount + privacy toggle + period selector; supporting "Investido", "Saldo disponível", "Resultado no período" with labelled metrics.
4. Performance chart with deposit/withdrawal indicators, dates and text/table alternative.
5. Allocation (with category labels, percentage and value) plus quick actions Investir, Transferir, Resgatar; actions must specify eligibility and limits.
6. Next-step guidance: educational message, not unsolicited financial recommendation; support entry.
7. Recent positions with link "Ver carteira completa".

### Desktop Carteira proposed hierarchy
- Heading "Minha carteira" with updated-at timestamp and explicit total.
- Tabs Posições, Movimentações, Rentabilidade with semantic descriptions.
- Filters: categoria, liquidez, ordenação and search; responsive to longer labels.
- Holdings table columns: Produto, Categoria, Saldo atual, Valor investido, Resultado no período, Liquidez, Detalhes; right align currency and numeric data.
- Details must distinguish issuer from distributor; omit unknown fields rather than invent values.
- Totals must equal holdings and show any excluded pending operations separately.

### Mobile-specific changes
- Home: overview card first; values toggle always reachable, then timeframe, 1 concise performance summary, actions, allocation list, contextual next step and holdings preview.
- Carteira: show compact holding rows with name, current amount, category and liquidity; drill-down for return and transaction history; never shrink numerical labels to fit.
- Bottom navigation five or fewer items, with context-specific support access; avoid duplicate permanent navigation.
- Privacy toggle defaults to visible, persists user choice only where permitted, and obscures balances in charts, tooltips, summaries, accessibility labels, notifications and background app previews. Consider optional "ocultar ao sair" in settings.

### Component & state contracts
- `DataDisplay/FinancialOverview`: populated, loading, empty, error, values-hidden; fields `asOf`, `total`, `invested`, `available`, `resultAbsolute`, `resultPercent`, `basis`, `period`.
- `Controls/PrivacyToggle`: shown/hidden, focus, disabled; explicit accessible text "Ocultar valores" / "Mostrar valores"; control all dependent surfaces via one state.
- `DataViz/PerformanceChart`: loading, no-data, partial-data, error, populated; trend accessibility, flows annotations, time selection, calculation explanation.
- `DataDisplay/HoldingRow`: default, focus, active, loading, error; product name, class, balance, liquidity and disclosed period.
- `DataDisplay/AllocationBreakdown`: categorical numeric legend + data visualization + total; category colors cannot be the only distinguisher.
- `Guidance/NextStep`: educational, personalized-if-authorized, unavailable; must be identified as information vs regulated recommendation.

### Example UI copy
- Dashboard heading: "Seu patrimônio, com clareza."
- Secondary: "Acompanhe seus investimentos e entenda as mudanças no período."
- Update: "Atualizado em 31 out 2026, 11h30" **only when backed by a real timestamp**.
- Empty returns: "Ainda não há dados suficientes para calcular o resultado deste período."
- Privacy toggle: "Ocultar valores" / "Mostrar valores".
- Next step: "Conheça como funciona a liquidez antes de investir."

### Deliverable limitations
- The editable SVG board is a handoff artifact; importing SVG into Figma creates editable vector/text nodes where supported, not native Figma components, variables or Auto Layout. Those must be configured within Figma.
- No modifications have been made to the user's linked Figma file in this version.

---

## Decisões do Figma sobre a v0.4 (31/10/2026)

Arquivo: https://www.figma.com/design/tl9FFynv0PPlTdnLkGVPPb (páginas 00 a 04). Onde o Figma diverge deste documento, vale o Figma, pelos motivos abaixo.

| Tema | v0.4 | Figma | Por quê |
| --- | --- | --- | --- |
| Borda de campo | `neutral.200` (1,25:1) | `border/input` = `neutral.500` (5,0:1) | WCAG 1.4.11 pede 3:1 no limite de controle |
| Anel de foco | `brand.orange` (provisório) | anel duplo: 2px branco + 2px `neutral.900` | laranja dá 2,5:1 sobre ivory |
| Texto secundário | `neutral.500` | igual; `neutral.400` nunca em texto | `neutral.400` dá 2,5:1 |
| Leafy | cor de apoio | só grafismo e dado, nunca texto | 2,7:1 no branco |
| Fundos de feedback | não definidos | `green-50` `#E7F2EB`, `red-50` `#F8E7E6`, `orange-50` `#FBEBDD` | status precisam de fundo sutil legível |
| Estados de ação | não definidos | hover `neutral.700`, pressed `neutral.900` (provisório) | auditoria pendente |
| Navegação mobile | Início, Carteira, Investir, Aprender, Mais | Início, Carteira, Investir, Aprender, **Atendimento** | o humano nunca fica escondido em "Mais" |

## Regras do case que viram regra de interface

1. **Fonte em toda informação factual:** `KB-xxx`, `OP-xxxxx` ou `P-xxxx`, em texto visível.
2. **Saída para pessoa em toda tela de atendimento.** Das 8h às 20h, com espera estimada; fora disso, protocolo e "volta às 8h". Segurança 24h.
3. **Golpe interrompe:** sinal de golpe troca a tela inteira pelo fluxo de segurança (`feedback/danger`), sem responder a pergunta original.
4. **Sem recomendação:** conteúdo educativo leva o rótulo "não é recomendação"; pedido de onde investir vai para o especialista com agendamento.
5. **Datas, IR e rendimento vêm do motor** (`motor/caqui_motor.py`), nunca do LLM. A tela mostra o motivo de cada data ("02/11 é feriado").
6. **Protocolo visível** em toda conversa e transferência: o cliente nunca repete a demanda.
7. **"Fazer uma reclamação" e "Encerrar minha conta"** acessíveis em qualquer passo do atendimento.

## Tokens prontos para o código

```css
:root {
  /* primitivas */
  --moss: #0B2B18; --ivory: #DDD2B7; --leafy: #82A591; --orange: #D95E00;
  --n50: #FAFAF7; --n100: #F4F5F0; --n200: #E5E7E1; --n300: #CDD3CA;
  --n400: #9BA69C; --n500: #66736B; --n700: #35473B; --n900: #17251D;
  --green-700: #247A4B; --green-50: #E7F2EB; --red-700: #B63C35; --red-50: #F8E7E6; --orange-50: #FBEBDD;

  /* semânticos (nomes do shadcn/ui) */
  --background: var(--n50);
  --foreground: var(--n900);
  --card: #FFFFFF;
  --card-foreground: var(--n900);
  --muted: var(--n100);
  --muted-foreground: var(--n500);
  --border: var(--n200);
  --input: var(--n500);
  --primary: var(--moss);
  --primary-foreground: #FFFFFF;
  --secondary: var(--ivory);
  --secondary-foreground: var(--n900);
  --accent: var(--orange);
  --destructive: var(--red-700);
  --success: var(--green-700);
  --ring: var(--n900);
  --radius: 8px;

  --font-heading: "Manrope", system-ui, sans-serif;
  --font-sans: "Inter", system-ui, sans-serif;
}

:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; box-shadow: 0 0 0 2px #FFFFFF; }
.valor { font-variant-numeric: tabular-nums; }
```

Escala tipográfica no código: Display 48/56, H1 36/44, H2 28/36, H3 22/30 (Manrope 600); Body large 16/24, Body 14/22, Label 14/20 (500), Caption 12/18 só para informação não crítica, Valor 28/36 (Inter 600, `tabular-nums`). Controles: 32 / 40 / 48 px; alvo de toque mínimo de 44×44 no mobile.
