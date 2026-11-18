# Uso: source evidencias/_run.sh ; EV=arquivo ; r 'comando'
# Grava "$ comando" + saída real (stdout+stderr) no arquivo de evidência e na tela.
r() { printf '$ %s\n' "$1" | tee -a "$EV"; bash -c "$1" 2>&1 | tee -a "$EV"; printf '\n' >> "$EV"; }
