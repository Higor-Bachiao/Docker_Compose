# Prática 03 — primeira imagem própria
FROM node:20-alpine

WORKDIR /app

# Copiado antes do restante do código para aproveitar o cache de camadas:
# só reinstala dependências quando package.json mudar.
COPY app/package.json ./
RUN npm install --omit=dev

COPY app/server.js ./

ENV PORTA=3000
EXPOSE 3000

# DESAFIO P03: o Docker testa a rota / a cada 10s; 3 falhas seguidas = unhealthy.
# wget ja vem no busybox do alpine (curl nao), por isso ele foi o escolhido.
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://localhost:${PORTA}/ || exit 1

CMD ["node", "server.js"]
