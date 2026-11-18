const http = require("http");
const os = require("os");

const PORTA = process.env.PORTA || 4000;
let atendidas = 0;

const servidor = http.createServer((req, res) => {
  atendidas += 1;
  console.log(`[backend] #${atendidas} ${req.method} ${req.url} (X-Real-IP=${req.headers["x-real-ip"] || "-"})`);
  res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
  res.end(
    JSON.stringify({
      servico: "backend-lab07",
      status: "ok",
      hostname: os.hostname(),
      caminhoRecebido: req.url,
      requisicoesAtendidas: atendidas,
      ipOriginalDoCliente: req.headers["x-real-ip"] || null,
    })
  );
});

servidor.listen(PORTA, () => console.log(`Backend ouvindo na porta ${PORTA}`));
