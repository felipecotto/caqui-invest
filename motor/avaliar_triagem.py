"""Mede a triagem contra os rótulos de conversas.csv (precisão e recall por sinal).

Uso: python3 avaliar_triagem.py <pasta caqui-invest>
"""
import csv, json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from caqui_motor import triar  # noqa: E402

dados = Path(sys.argv[1] if len(sys.argv) > 1 else ".") / "dados"
clientes = {c["id"]: c for c in json.loads((dados / "clientes.json").read_text(encoding="utf-8"))}
ALVO = {"golpe", "recomendacao", "vulneravel", "injecao"}
tp, fp, fn = Counter(), Counter(), Counter()
with open(dados / "conversas.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        falas = " ".join(t.split(":", 1)[1] for t in r["transcricao"].split(" | ") if t.lower().startswith("cliente"))
        got = set(triar(falas, clientes.get(r["id_cliente"]))) & ALVO
        lab = {s for s in r["sinais"].split(";") if s}
        for s in got & lab: tp[s] += 1
        for s in got - lab: fp[s] += 1
        for s in lab - got: fn[s] += 1
print(f"{'sinal':<14}{'recall':>8}{'precisão':>10}   (acertos / rotulados / falsos alarmes)")
for s in sorted(ALVO):
    rec = tp[s] / (tp[s] + fn[s]) if tp[s] + fn[s] else 0
    pre = tp[s] / (tp[s] + fp[s]) if tp[s] + fp[s] else 0
    print(f"{s:<14}{rec:>8.0%}{pre:>10.0%}   ({tp[s]} / {tp[s]+fn[s]} / {fp[s]})")

# golpe, injeção e recomendação são regras críticas (4, 5, 11): qualquer perda bloqueia
criticos = [s for s in ("golpe", "injecao", "recomendacao") if fn[s] > 0]
if criticos:
    print("Triagem perdeu casos críticos:", ", ".join(criticos))
    sys.exit(1)
