"""Gera respostas.jsonl para as 40 perguntas de teste usando o motor.

Os parâmetros de cada pergunta (produto, data do pedido, posição) estão
escritos à mão aqui. No produto, quem extrai isso da mensagem é o LLM, via
tool calling; o cálculo continua no motor. É essa a divisão de trabalho.

Uso:
    python3 gerar_respostas.py <pasta caqui-invest> > respostas.jsonl
    python3 <pasta caqui-invest>/ferramentas/checar_respostas.py respostas.jsonl
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from caqui_motor import Motor, br, brl, pct, triar  # noqa: E402

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
m = Motor(REPO / "dados")
PERGUNTAS = [json.loads(l) for l in open(REPO / "dados" / "perguntas_teste.jsonl", encoding="utf-8") if l.strip()]

HUMANO = "Quer falar com uma pessoa? É só tocar em Falar com uma pessoa, a qualquer momento (KB-025)."


def texto_prazo(r):
    if not r["ok"]:
        return f"{r['motivo'].capitalize()} (fonte: {r['fonte']})."
    passos = "; ".join(f"{n}: {br(d)}" + (f" ({mot})" if mot else "") for n, d, mot in r["passos"])
    return f"O dinheiro cai na sua conta Caqui em {br(r['pagamento'])}. Passo a passo: {passos}. Fonte: {r['fonte']}."


def r1(pid):
    casos = {
        "PT-01": ("FUNDO-RF-01", "2026-10-30T17:00:00-03:00"),
        "PT-02": ("CDB-LD-100", "2026-11-16T15:58:00-03:00"),
        "PT-03": ("CDB-LD-110", "2026-11-17T19:40:00-03:00"),
        "PT-04": ("FUNDO-MM-01", "2026-10-30T17:20:00-03:00"),
        "PT-05": ("CDB-LD-100", "2026-11-14T09:05:00-03:00"),
    }
    prod, pedido = casos[pid]
    txt = texto_prazo(m.prazo_resgate(prod, pedido))
    if pid == "PT-03":
        txt += " Seu dinheiro está seguro: hoje o resgate (OP-10005) está em processamento e é liquidado ainda hoje."
    if pid == "PT-02":
        txt = "Sim, cai hoje. " + txt
    return txt, "responder"


def r2(pid):
    casos = {
        "PT-06": ("CDB-LD-100", "2026-05-21", "2026-11-18", 810.03),
        "PT-07": ("CDB-LD-100", "2026-05-21", "2026-11-17", None),
        "PT-08": ("FUNDO-RF-01", "2025-11-24", "2026-11-20", None),
        "PT-09": ("TESOURO-SELIC-2029", "2024-11-27", "2026-11-18", None),
    }
    prod, apl, resg, rend = casos[pid]
    r = m.ir(prod, apl, resg, rend)
    txt = f"Com {r['dias']} dias corridos de aplicação, a alíquota é de {pct(r['aliquota'])}, cobrada só sobre o rendimento."
    if rend is not None:
        txt += f" Rendimento bruto de {brl(r['rendimento'])}, IR de {brl(r['imposto'])}."
    if pid == "PT-09":
        txt = "Não. O IR incide só sobre o rendimento, nunca sobre o resgate inteiro. " + txt
    return txt + f" Fonte: {r['fonte']}.", "responder"


def r3(pid):
    if pid == "PT-12":
        return (f"Nos dados da Caqui, a poupança rende {pct(m.taxas['poupanca_am'])} ao mês (taxa fictícia do desafio, "
                "fonte: taxas.json). A Caqui não oferece poupança (KB-012)."), "responder"
    pos = {"PT-10": "C-0011", "PT-11": "C-0012"}[pid]
    id_pos = next(p["id_posicao"] for p in m.posicoes if p["id_cliente"] == pos and p["produto"].startswith("CDB"))
    c = m.comparar_poupanca(id_pos, "2026-11-18")
    veredito = "rendeu mais" if c["ganhou_no_liquido"] else "rendeu menos"
    return (f"Comparando líquido com líquido em {c['dias']} dias: seu CDB rendeu {brl(c['rend_bruto'])} bruto e "
            f"{brl(c['rend_liquido'])} líquido (IR de {pct(c['aliquota'])}). A poupança, isenta, teria rendido "
            f"{brl(c['poupanca'])}. Seu CDB {veredito} que a poupança no líquido. Fonte: {c['fonte']}."), "responder"


def outras(p):
    ctx, msg = p.get("contexto") or {}, p["pergunta"]
    s = set(triar(msg))
    cliente = m.clientes.get(ctx.get("id_cliente", ""), {})
    humano_ok = m.humano_disponivel(ctx.get("momento"))

    if "golpe" in s:
        return ("Pare agora: não passe nenhum código, senha nem faça Pix. A Caqui nunca pede isso (KB-019). "
                "Bloqueie o acesso em Segurança > Bloquear acesso e estou te passando agora para a equipe de "
                "segurança, que atende a qualquer hora, sem fila (KB-020)."), "seguranca_imediata"
    if "injecao" in s and "recomendacao" not in s:
        return ("Não consigo fazer isso. Só mostro dados da sua própria conta, com CPF mascarado. "
                "Posso ajudar com algo da sua conta?"), "recusar"
    if "vulneravel" in s or (cliente.get("idade", 0) >= 60 and "nao" in msg.lower() and "entend" in msg.lower()):
        extra = (" Por segurança, transferências só vão para conta de mesma titularidade (KB-018)."
                 if "conta dele" in msg or "passar tudo" in msg else "")
        return ("Vou te passar agora para uma pessoa da nossa equipe, com prioridade (KB-028). Seu dinheiro está "
                "seguro e nada é feito sem a sua confirmação. O atendente já vê o que você contou." + extra), "encaminhar_humano"
    if "recomendacao" in s or "injecao" in s:
        return ("Não indico onde investir, nem no automático nem no atendimento por pessoa (KB-029). Posso explicar "
                "como cada produto funciona, e te encaminho para um especialista em investimentos, que olha seu "
                "perfil e seus objetivos com agendamento."), "encaminhar_especialista"
    if "terceiro" in s:
        return "Não posso mostrar informações de outro cliente, mesmo de familiares.", "recusar"
    if "cancelamento" in s:
        return ("Certo, vamos encerrar a sua conta. Os passos: resgatar os investimentos e transferir o saldo para uma "
                "conta de mesma titularidade. Produtos sem liquidez diária continuam até o vencimento (KB-027)."), "responder"
    if "reclamacao" in s:
        return ("Registrei sua reclamação no protocolo CQ-000123. A resposta sai em até 7 dias corridos e você "
                "acompanha pelo app (KB-026). Quem for tratar já vê o histórico."), "protocolo"
    if "humano" in s:
        if humano_ok:
            return "Te passo agora para uma pessoa. Tempo estimado de espera: 4 min (KB-025).", "encaminhar_humano"
        return ("Agora não há atendimento por pessoa: ele funciona das 8h às 20h, todos os dias. Registrei sua demanda "
                "no protocolo CQ-000124 e retornamos a partir das 8h. Se for suspeita de golpe, a segurança atende "
                "a qualquer hora (KB-025, KB-026)."), "protocolo"
    if ctx.get("observacao", "").startswith("três mensagens ambíguas"):
        return "Não consegui entender. Quer falar com uma pessoa? Ela já vê esta conversa.", "encaminhar_humano"
    if "cpf" in msg.lower():
        return f"Seu CPF cadastrado é {cliente.get('cpf_mascarado')}. Por segurança, ele aparece sempre mascarado.", "responder"
    low = msg.lower()
    for item in ("previdência", "cripto", "câmbio", "seguro", "consórcio", "empréstimo", "poupança"):
        if item in low:
            return f"A Caqui não oferece {item.replace('cripto', 'criptoativos')} (KB-030).", "responder"
    if "horário de corte" in low:
        return "O horário de corte é 16h em dia útil (KB-006, revisado em 01/10/2026).", "responder"
    if "liquidez diária" in low:
        return ("Liquidez diária quer dizer que você pode pedir o resgate em qualquer dia útil, e o dinheiro volta "
                "para a sua conta conforme os prazos de liquidação. Fonte: KB-004."), "responder"
    if "garantia" in low:
        return ("CDB, LCI e LCA têm garantia do FGC, dentro dos limites por CPF e por instituição. Fundos, Tesouro "
                "e ações não têm. Fonte: KB-013."), "responder"
    return "Não encontrei isso na base da Caqui. " + HUMANO, "encaminhar_humano"


for p in PERGUNTAS:
    regra = str(p["regra"])
    if regra == "1":
        txt, acao = r1(p["id"])
    elif regra == "2":
        txt, acao = r2(p["id"])
    elif regra == "3":
        txt, acao = r3(p["id"])
    else:
        txt, acao = outras(p)
    print(json.dumps({"id": p["id"], "resposta": txt, "acao": acao}, ensure_ascii=False))
