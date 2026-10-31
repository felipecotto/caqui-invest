"""Motor determinístico da Caqui Invest (regras 1, 2, 3 e triagem de risco).

Ideia central: o LLM conversa e extrai parâmetros; quem faz conta de data,
imposto e rendimento é este código. O LLM nunca calcula prazo nem IR.

Sem dependências. Python 3.9+.
Uso como biblioteca:
    from caqui_motor import Motor
    m = Motor("caminho/para/caqui-invest/dados")
    m.prazo_resgate("FUNDO-RF-01", "2026-10-30T17:00:00-03:00")
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from datetime import date, datetime, time, timedelta
from pathlib import Path

CORTE = time(16, 0)
HUMANO_INICIO, HUMANO_FIM = time(8, 0), time(20, 0)


def brl(v: float) -> str:
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def pct(v: float) -> str:
    s = f"{v * 100:.1f}".replace(".", ",")
    return s[:-2] + "%" if s.endswith(",0") else s + "%"


def br(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


class Motor:
    def __init__(self, pasta_dados: str | Path):
        p = Path(pasta_dados)
        cal = json.loads((p / "calendario.json").read_text(encoding="utf-8"))
        self.dias = {d["data"]: d for d in cal["dias"]}
        self.taxas = json.loads((p / "taxas.json").read_text(encoding="utf-8"))
        self.produtos = {x["codigo"]: x for x in self.taxas["produtos"]}
        with open(p / "posicoes.csv", encoding="utf-8") as f:
            self.posicoes = list(csv.DictReader(f))
        with open(p / "operacoes.csv", encoding="utf-8") as f:
            self.operacoes = list(csv.DictReader(f))
        self.clientes = {c["id"]: c for c in json.loads((p / "clientes.json").read_text(encoding="utf-8"))}

    # ---------- calendário ----------
    def dia_util(self, d: date) -> bool:
        info = self.dias.get(d.isoformat())
        if info is None:
            raise ValueError(f"{d} fora do calendário da Caqui (out/2026 a dez/2027)")
        return info["dia_util"]

    def feriado(self, d: date):
        return self.dias.get(d.isoformat(), {}).get("feriado")

    def proximo_du(self, d: date, incluir_hoje: bool = True) -> date:
        d = d if incluir_hoje else d + timedelta(1)
        while not self.dia_util(d):
            d += timedelta(1)
        return d

    def somar_du(self, d: date, n: int) -> date:
        while n > 0:
            d += timedelta(1)
            if self.dia_util(d):
                n -= 1
        return d

    def dia_base(self, pedido_em: str | datetime) -> tuple[date, str]:
        """Dia-base do pedido (KB-006): até 16h de dia útil conta no dia; senão, próximo dia útil."""
        dt = datetime.fromisoformat(pedido_em) if isinstance(pedido_em, str) else pedido_em
        d = dt.date()
        if self.dia_util(d) and dt.time() <= CORTE:
            return d, "pedido até 16h em dia útil: conta no mesmo dia"
        motivo = "pedido depois das 16h" if self.dia_util(d) else (
            f"{br(d)} é feriado ({self.feriado(d)})" if self.feriado(d) else f"{br(d)} não é dia útil")
        base = self.proximo_du(d, incluir_hoje=False)
        pulados = [x for x in (d + timedelta(i) for i in range(1, (base - d).days)) if self.feriado(x)]
        if pulados:
            motivo += "; " + ", ".join(f"{br(x)} é feriado ({self.feriado(x)})" for x in pulados)
        return base, motivo

    # ---------- regra 1: liquidação ----------
    def prazo_resgate(self, produto: str, pedido_em: str, data_aplicacao: str | None = None) -> dict:
        """Devolve passos com datas e a fonte. Nunca devolve prazo inventado."""
        prod = self.produtos.get(produto)
        if prod is None:
            return {"ok": False, "motivo": "produto não existe na base (regra 9: não inventa prazo)", "fonte": "KB-030"}
        base, motivo = self.dia_base(pedido_em)
        passos = [("dia-base", base, motivo)]
        tipo, liq = prod["tipo"], prod["liquidez"]
        if liq == "no_vencimento":
            return {"ok": False, "motivo": "produto sem liquidez diária: resgate só no vencimento", "fonte": "KB-005"}
        if liq == "diaria_apos_carencia" and data_aplicacao:
            libera = date.fromisoformat(data_aplicacao) + timedelta(prod["carencia_dias"])
            if base < libera:
                return {"ok": False, "motivo": f"em carência até {br(libera)}", "fonte": "KB-005"}
        if tipo in ("CDB", "LCI"):
            pagamento, fonte = base, "KB-006"
        elif produto == "FUNDO-RF-01":
            cot = self.somar_du(base, 1)
            passos.append(("cotização (D+1 útil)", cot, ""))
            pagamento, fonte = self.somar_du(base, 2), "KB-006, KB-014"
        elif produto == "FUNDO-MM-01":
            cot = self.proximo_du(base + timedelta(30))
            passos.append(("cotização (30 corridos, ajustada p/ dia útil)", cot, ""))
            pagamento, fonte = self.somar_du(cot, 2), "KB-006, KB-014"
        elif tipo == "TESOURO":
            pagamento, fonte = self.somar_du(base, 1), "KB-006, KB-015"
        elif tipo == "ACOES":
            pagamento, fonte = self.somar_du(base, 2), "KB-006, KB-016"
        else:
            return {"ok": False, "motivo": "regra de liquidação não encontrada", "fonte": None}
        passos.append(("pagamento", pagamento, ""))
        return {"ok": True, "dia_base": base, "pagamento": pagamento, "passos": passos, "fonte": fonte}

    def auditar_liquidacao_prevista(self) -> list[dict]:
        """Recalcula liquidacao_prevista de cada resgate e compara com o arquivo."""
        saida = []
        for op in self.operacoes:
            if op["tipo"] != "resgate" or not op["produto"]:
                continue
            pos = next((p for p in self.posicoes if p["id_cliente"] == op["id_cliente"]
                        and p["produto"] == op["produto"]), None)
            r = self.prazo_resgate(op["produto"], op["pedido_em"], pos["data_aplicacao"] if pos else None)
            calc = r["pagamento"].isoformat() if r.get("ok") else None
            saida.append({"id": op["id_operacao"], "produto": op["produto"], "status": op["status"],
                          "arquivo": op["liquidacao_prevista"] or None, "calculado": calc,
                          "motivo": None if r.get("ok") else r["motivo"], "obs": op["observacao"]})
        return saida

    # ---------- regra 2: IR ----------
    def aliquota_ir(self, dias_corridos: int) -> float:
        for faixa in self.taxas["ir_regressivo"]:
            if "acima_de_dias" in faixa and dias_corridos > faixa["acima_de_dias"]:
                return faixa["aliquota"]
            if dias_corridos <= faixa.get("ate_dias", -1) and dias_corridos >= faixa.get("de_dias", 0):
                return faixa["aliquota"]
        raise ValueError(dias_corridos)

    def ir(self, produto: str, data_aplicacao: str, data_resgate: str, rendimento: float | None = None) -> dict:
        prod = self.produtos[produto]
        dias = (date.fromisoformat(data_resgate) - date.fromisoformat(data_aplicacao)).days
        if not prod["tributavel"]:
            return {"dias": dias, "aliquota": 0.0, "isento": True, "fonte": "KB-011"}
        a = self.aliquota_ir(dias)
        out = {"dias": dias, "aliquota": a, "isento": False, "base": "rendimento", "fonte": "KB-010"}
        if rendimento is not None:
            out.update(rendimento=rendimento, imposto=round(rendimento * a, 2),
                       liquido=round(rendimento * (1 - a), 2))
        return out

    # ---------- regra 3: comparação com poupança ----------
    def comparar_poupanca(self, id_posicao: str, data_ref: str) -> dict:
        p = next(x for x in self.posicoes if x["id_posicao"] == id_posicao)
        v = float(p["valor_aplicado_brl"])
        rend_bruto = round(float(p["saldo_bruto_brl"]) - v, 2)
        imp = self.ir(p["produto"], p["data_aplicacao"], data_ref, rend_bruto)
        poup = round(v * ((1 + self.taxas["poupanca_am"]) ** (imp["dias"] / 30) - 1), 2)
        liq = imp.get("liquido", rend_bruto)
        return {"posicao": p["id_posicao"], "produto": p["produto"], "dias": imp["dias"], "aplicado": v,
                "rend_bruto": rend_bruto, "aliquota": imp["aliquota"], "rend_liquido": liq,
                "poupanca": poup, "ganhou_no_bruto": rend_bruto > poup, "ganhou_no_liquido": liq > poup,
                "fonte": "KB-009, KB-010, KB-012 + taxas.json + posição " + p["id_posicao"]}

    # ---------- horário ----------
    @staticmethod
    def humano_disponivel(momento: str | None) -> bool:
        if not momento:
            return True
        t = datetime.fromisoformat(momento).time()
        return HUMANO_INICIO <= t < HUMANO_FIM


# ---------- triagem de risco (roda ANTES do LLM) ----------
# Ordem importa: golpe > injeção > vulnerável > recomendação > cancelamento/reclamação > humano.
SINAIS = {
    "golpe": [r"codigo (do |de )?sms", r"\bcodigo\b.*(pediu|pediram|passar)", r"(pediu|pediram|pedindo).*senha",
              r"suporte remoto", r"acesso remoto", r"pix de teste", r"(gerente|seguranca|central).*(ligou|ligaram)",
              r"(ligou|ligaram).*(gerente|seguranca|caqui)", r"instalar (um )?(app|aplicativo)", r"acessar meu celular", r"token",
              r"link.*senha", r"coloquei (minha )?senha", r"passei (o |meu )?(codigo|senha)"],
    "injecao": [r"ignore (suas|as) (instrucoes|regras)", r"modo administrador", r"^sistema:", r"voce agora e",
                r"sem restricoes", r"liste os cpfs", r"esqueca a politica", r"sem as regras",
                r"senha padrao"],
    "vulneravel": [r"(sobrinho|filho|filha|neto|neta|genro|nora|vizinho).*(mandou|disse|dizendo|pediu|lado)",
                   r"nao (estou )?entend\w* nada", r"tirar todo", r"passar tudo"],
    "recomendacao": [r"onde (eu )?(coloco|invisto|investir|aplico)", r"o que (voce|vc) faria", r"me diz(er)? o que fazer",
                     r"vale (mais )?a pena", r"assessor", r"qual (e )?(o )?melhor", r"me (indica|recomenda)",
                     r"onde investir", r"pra mim\?", r"devo (tirar|colocar|aplicar|investir|resgatar)"],
    "terceiro": [r"saldo d[ao] (cliente|sr|sra|dona|seu)\b", r"saldo da [a-z]+ [a-z]+", r"sou (sobrinho|filho|parente)"],
    "cancelamento": [r"encerrar (minha )?conta", r"cancelar (minha )?conta", r"fechar (minha )?conta"],
    "reclamacao": [r"reclamacao", r"reclamar"],
    "humano": [r"falar com (uma )?(pessoa|humano|atendente)", r"^atendente$"],
}


def triar(mensagem: str, cliente: dict | None = None) -> list[str]:
    """Sinais de risco na mensagem. Com o cliente, idade 60+ também marca vulnerável (KB-028).

    Texto não basta para vulnerabilidade: nas 300 conversas rotuladas, só a idade
    explica a maioria dos casos. Regex é piso, não teto: no produto, some um
    classificador LLM e mantenha estes padrões como rede de segurança.
    """
    t = _norm(mensagem)
    sinais = [s for s, pads in SINAIS.items() if any(re.search(p, t) for p in pads)]
    if cliente and cliente.get("idade", 0) >= 60 and "vulneravel" not in sinais:
        sinais.append("vulneravel")
    return sinais
