#!/usr/bin/env bash
# Lider Avto — bitta buyruq bilan ishga tushirish (Mac/Linux):   bash start.sh
cd "$(dirname "$0")" || exit 1

PY=$(command -v python3.12 || command -v python3.13 || command -v python3.11 || command -v python3)
[ -z "$PY" ] && { echo "XATO: Python topilmadi. https://www.python.org dan Python 3.12 oʻrnating."; exit 1; }
echo "==> Python: $($PY --version)"
case "$($PY --version)" in *"3.14"*|*"3.15"*|*"3.16"*)
  echo "OGOHLANTIRISH: Python juda yangi. Muammo chiqsa:  brew install python@3.12  va qayta urining." ;; esac

if [ ! -d .venv ]; then echo "==> .venv yaratilmoqda"; "$PY" -m venv .venv || { echo "XATO: venv yaratilmadi"; exit 1; }; fi
source .venv/bin/activate
export DJANGO_DEBUG=1   # lokal ishlab chiqish rejimi (serverda ishlatilmaydi)

echo "==> Kutubxonalar oʻrnatilmoqda (birinchi marta bir necha daqiqa)"
pip install -q -r requirements.txt || { echo "XATO: pip oʻrnatmadi. Yuqoridagi xatoni menga yuboring."; exit 1; }

echo "==> Baza (migrate)"
python manage.py migrate || { echo "XATO: migrate bajarilmadi. Yuqoridagi xatoni menga yuboring."; exit 1; }
python manage.py doctor --seed-if-empty || { echo "XATO: maʼlumotlar yuklanmadi."; exit 1; }

command -v npm >/dev/null || { echo "XATO: Node.js/npm topilmadi. https://nodejs.org dan oʻrnating."; exit 1; }
if [ ! -d frontend/node_modules ]; then echo "==> Frontend kutubxonalari (npm install)"; (cd frontend && npm install) || exit 1; fi

echo "==> Backend: http://127.0.0.1:8000     Sayt: http://localhost:3005"
python manage.py runserver 8000 &
BACK=$!
trap 'kill $BACK 2>/dev/null' EXIT
cd frontend && npm run dev
