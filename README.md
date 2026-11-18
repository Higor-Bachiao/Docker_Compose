# Docker e Docker Compose: práticas de Sistemas Distribuídos (SD 2026B)

Resolução das 14 práticas do roteiro de laboratório da Unifeg (Ciência da Computação,
8º período), executadas num macOS com Apple Silicon e Docker Desktop 29.0.1.

## Entrega

| Arquivo | O que é |
|---|---|
| [docs/Roteiro_Docker_Aluno_PREENCHIDO.docx](docs/Roteiro_Docker_Aluno_PREENCHIDO.docx) | Roteiro com as saídas reais coladas nos quadros 📎, respostas das 45 perguntas, os 14 desafios e o checklist |
| [docs/Roteiro_Docker_Aluno_PREENCHIDO.pdf](docs/Roteiro_Docker_Aluno_PREENCHIDO.pdf) | O mesmo documento em PDF |
| [evidencias/](evidencias/) | `pXX.txt`: cada comando executado (`$ comando`) seguido da saída real. `prints/`: capturas das telas React |

O .docx é gerado a partir do roteiro original por [docs/preencher_roteiro.py](docs/preencher_roteiro.py).
O conteúdo escrito (respostas e desafios) fica em [docs/respostas.py](docs/respostas.py), e as saídas
vêm direto de `evidencias/`.

## O que mudei em relação ao material base

- **Conteúdo próprio:** mensagens das APIs, sites do Apache e do Nginx, apps React (checklist de tópicos
  na P12; cadastro e exclusão na P14) e seed do banco com uma turma fictícia.
- **Segurança:** senhas aleatórias nos `.env` (fora do Git, adicionados ao `.gitignore`) e cabeçalho
  `X-Aluno` no Apache.
- **Desafios implementados:**
  - HEALTHCHECK no Dockerfile (P03)
  - `-Indexes` no Apache (P06)
  - `/saude/` e `/bruto/` no Nginx (P07)
  - `NGINX_HOST` e healthcheck no Compose (P08)
  - índice via init SQL (P09)
  - healthcheck do pgAdmin com um serviço `monitor` (P10)
  - estágio de teste no multi-stage (P11)
  - imagem dev-em-produção para comparação (P12)
  - falhas forçadas e diagnóstico (P13)
  - `DELETE /alunos/:id` com botão na interface (P14)
- **Troubleshooting real (P12/P14):** o `rollup` 4.68.6, publicado em 18/11/2026, quebrava o
  `vite build` ("Code is nested too deeply"). Fixei a 4.68.5 via `overrides` no `package.json`
  e adicionei um `.dockerignore`.

## Como rodar uma prática

```bash
cd labs/14-projeto-integrador
cp .env.example .env        # troque as senhas
docker compose up -d --build
curl http://localhost:8084/api/alunos
docker compose down -v
```

Os comandos de cada prática estão no `README.md` da pasta correspondente em `labs/`.
