# Multi-stage build: o estágio "builder" tem tudo que é preciso para
# COMPILAR (TypeScript, devDependencies); o estágio final (base alpine)
# recebe só o resultado — dist/ e as dependências de produção.

# ---- estágio 1: build ----
FROM node:20 AS builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

# ---- estágio 2 (DESAFIO P11): teste ----
# Herda do builder (tem dist/ e o node completo) e faz um smoke test:
# sobe a API compilada e confere se o JSON responde com compilado=true.
# O BuildKit só executa este estágio quando pedido (--target test) ou
# quando outro estágio depende dele — por isso ele não pesa na imagem final.
FROM builder AS test
RUN node dist/index.js & \
    sleep 1 && \
    curl -sf http://localhost:5000 | tee /tmp/resposta.json && \
    grep -q '"compilado":true' /tmp/resposta.json && \
    echo "\nSMOKE TEST OK"

# ---- estágio 3: produção ----
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY --from=builder /app/dist ./dist

ENV IMAGEM_BASE=node:20-alpine
EXPOSE 5000
CMD ["node", "dist/index.js"]
