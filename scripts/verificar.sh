#!/bin/sh
# Verificação do grupo: regras do case viram teste.
# 1. Gera as respostas (troque RESPOSTAS pela saída da solução quando ela existir).
# 2. Roda o checador oficial nas regras tratadas.
# 3. Mede a triagem contra os rótulos de dados/conversas.csv.
# 4. Bloqueia segredo e CPF sem máscara nos arquivos versionados.
set -e
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

REGRAS="${REGRAS:-1,2,3,4,5,6,7,8,9,10,11,12,geral}"
RESPOSTAS="${RESPOSTAS:-/tmp/caqui-respostas.jsonl}"

if [ "$RESPOSTAS" = "/tmp/caqui-respostas.jsonl" ]; then
  python3 motor/gerar_respostas.py . > "$RESPOSTAS"
fi

echo "== Checador oficial (regras $REGRAS)"
python3 ferramentas/checar_respostas.py "$RESPOSTAS" --regras "$REGRAS"

echo "== Triagem contra as 300 conversas rotuladas"
python3 motor/avaliar_triagem.py .

echo "== Segredos e CPF"
ARQS=$(git ls-files 2>/dev/null; git diff --cached --name-only 2>/dev/null)
if [ -n "$ARQS" ]; then
  if echo "$ARQS" | sort -u | grep -v '^dados/' | xargs grep -nE '(sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})' 2>/dev/null; then
    echo "Encontrado segredo ou CPF sem máscara. Commit bloqueado."; exit 1
  fi
fi
echo "OK"
