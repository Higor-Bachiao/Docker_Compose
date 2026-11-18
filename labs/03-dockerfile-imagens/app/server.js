const http = require("http");
const os = require("os");

const PORTA = process.env.PORTA || 3000;
const INICIO = new Date();

const servidor = http.createServer((req, res) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
  res.end(
    JSON.stringify(
      {
        mensagem: "Ola, Unifeg! Mensagem alterada para testar o cache de camadas.",
        hostname: os.hostname(),
        plataforma: `${os.platform()}/${os.arch()}`,
        versaoNode: process.version,
        noArDesde: INICIO.toISOString(),
      },
      null,
      2
    )
  );
});

servidor.listen(PORTA, () => {
  console.log(`Servidor ouvindo na porta ${PORTA}`);
});
