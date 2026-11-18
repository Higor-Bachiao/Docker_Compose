import http from "http";
import os from "os";

const PORTA = Number(process.env.PORTA) || 5000;

interface Resposta {
  servico: string;
  compilado: boolean;
  imagemBase: string;
  hostname: string;
  memoriaUsadaMB: number;
}

const servidor = http.createServer((_req, res) => {
  const corpo: Resposta = {
    servico: "app-multistage",
    compilado: true,
    imagemBase: process.env.IMAGEM_BASE ?? "desconhecida",
    hostname: os.hostname(),
    memoriaUsadaMB: Math.round(process.memoryUsage().rss / 1024 / 1024),
  };
  res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(corpo));
});

servidor.listen(PORTA, () => console.log(`API (TypeScript compilado) na porta ${PORTA}`));
