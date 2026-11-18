# -*- coding: utf-8 -*-
"""Conteúdo da entrega: respostas, desafios e mapeamento das evidências.

Lido por docs/preencher_roteiro.py, que injeta tudo no Roteiro_Docker_Aluno.docx.
As evidências vêm dos arquivos evidencias/pXX.txt (saída real dos comandos).
"""

AMBIENTE = [
    "Ambiente usado em todas as práticas: macOS 27 em Apple Silicon (arm64), Docker Desktop "
    "com Docker Engine 29.0.1 e Docker Compose v2.40.3. Como o macOS usa shell compatível com "
    "bash, executei sempre a coluna \U0001F427 Ubuntu do roteiro.",
    "As saídas abaixo foram copiadas dos arquivos evidencias/pXX.txt do meu repositório, que "
    "guardam cada comando executado ($ comando) seguido da saída real. Quando cortei linhas "
    "repetitivas (barras de download, por exemplo), indiquei com [...].",
]

# ---------------------------------------------------------------------------
# Quadros 📎, na ordem em que aparecem no roteiro.
# Cada item: (arquivo de evidência, [prefixos de comando], max_linhas_por_bloco)
# ---------------------------------------------------------------------------
QUADROS = [
    # P01
    ("p01", ["docker run hello-world"], 30),
    ("p01", ["docker ps -a --filter name=meu-alpine", "docker logs meu-alpine"], 10),
    # P02
    ("p02", ["docker exec lab-ubuntu sh /scripts/explorar.sh"], 40),
    # P03
    ("p03", ["docker build --progress=plain -t app-fundamentos:1.0 . 2>&1 | grep -vE"], 60),
    ("p03", ["docker run --rm -d --name app03 -p 3000:3000"], 12),
    ("p03", ["docker image history app-fundamentos:1.0", "docker image ls app-fundamentos"], 22),
    # P04
    ("p04", ["for i in 1 2 3; do docker run", "ls -l dados/"], 30),
    ("p04", ["docker volume inspect dados-contador"], 15),
    ("p04", ["docker run --rm -v \"$(pwd)/scripts:/scripts:ro\" --tmpfs"], 12),
    # P05
    ("p05", ["docker run --rm --network rede-lab05 busybox wget -qO- http://servidor"], 40),
    ("p05", ["docker port servidor-exposto", "docker network inspect rede-lab05"], 10),
    # P06
    ("p06", ["curl -i http://localhost:8080"], 40),
    ("p06", ["docker exec lab-apache httpd -t", "docker logs lab-apache"], 10),
    # P07
    ("p07", ["curl -s http://localhost:8081/api/status", "curl -s http://localhost:8081/api/qualquer/coisa"], 6),
    # P08
    ("p08", ["docker compose ps", "curl -s http://localhost:8081/api/status"], 8),
    # P09
    ("p09", ["docker logs lab-postgres 2>&1 | grep -E \"running"], 12),
    ("p09", ["docker exec lab-postgres psql -U unifeg -d lab_sistemas_distribuidos -c \"SELECT * FROM alunos;\""], 12),
    # P10
    ("p10", ["docker compose ps --format \"table {{.Service}}\\t{{.Image}}", "docker compose ps --format \"table {{.Service}}\\t{{.Status}}\"", "docker compose logs pgadmin"], 8),
    ("p10", ["docker compose exec -T -e PGPASSWORD", "docker compose exec -T pgadmin cat"], 12),
    # P11
    ("p11", ["docker image ls app-multistage", "docker image inspect -f"], 8),
    # P12
    ("p12", ["sed -i", "docker compose logs react-dev | grep"], 6),
    ("p12", ["docker compose exec react-dev sh -c \"ls /app/node_modules | wc -l\"", "docker compose exec react-dev sh -c \"du -sh", "echo \"itens em app-react/node_modules"], 8),
    # P13
    ("p13", ["docker compose ps --format", "curl -s http://localhost:6000", "docker compose exec app whoami"], 10),
    ("p13", ["docker stats --no-stream", "docker inspect $(docker compose ps -q app) --format \"NanoCpus"], 6),
    ("p13", ["docker push localhost:5000/app-lab13:1.0", "docker pull localhost:5000/app-lab13:1.0", "curl -s http://localhost:5000/v2/_catalog"], 14),
    # P14
    ("p14", ["docker compose ps --format \"table {{.Service}}\\t{{.Image}}"], 8),
    ("p14", ["curl -s http://localhost:8084/api/status; echo; curl -s http://localhost:8084/api/alunos"], 6),
    ("p14", ["curl -s -X POST http://localhost:8084/api/alunos -H \"Content-Type: application/json\" -d '{\"nome\":\"Higor"], 6),
    ("TEXTO_P14_TELA", [], 0),
]

TEXTO_P14_TELA = [
    "Abri http://localhost:8084 (Chrome). A página \"Projeto Integrador — SD 2026B\" carregou a "
    "tabela via fetch(\"/api/alunos\") com as colunas ID, RA, Nome e Período e um botão Excluir "
    "em cada linha: Marina Tavares (2023101), Otávio Rezende (2023102), Letícia Campos (2023103), "
    "Rafael Nogueira (2023104) e o registro inserido no passo 3 (2023199). Abaixo da tabela: "
    "\"5 aluno(s) no banco.\". Print em evidencias/prints/p14-frontend-tabela.png.",
    "IMG:p14-frontend-tabela.png",
    "HTML real da tabela (Chrome headless --dump-dom, botões omitidos):",
    "CODE:<tbody><tr><td>1</td><td>2023101</td><td>Marina Tavares</td><td>8º</td>...</tr>\n"
    "<tr><td>5</td><td>2023199</td><td>Higor Bachião</td><td>8º</td>...</tr></tbody>",
]

# ---------------------------------------------------------------------------
# Respostas das perguntas de verificação (na ordem do roteiro: 45 perguntas)
# ---------------------------------------------------------------------------
RESPOSTAS = [
    # ---------------- P01 ----------------
    "Não. O --rm faz o Docker apagar o container assim que o processo principal (o echo) termina. "
    "Testei com um container chamado \"efemero\": a mensagem apareceu e, logo em seguida, "
    "docker ps -a --filter name=efemero voltou só com o cabeçalho, sem nenhuma linha.",
    "docker stop encerra o processo principal (manda SIGTERM e, se não terminar em 10 s, SIGKILL), "
    "mas o container continua existindo, parado, com a camada de escrita intacta, e pode voltar "
    "com docker start. docker rm apaga o container de vez, junto com essa camada; só funciona com "
    "ele parado (ou com -f, que para e remove).",
    "Não. Sem -i o stdin não fica conectado, então o sh lê fim de arquivo e sai na hora; o "
    "container nasce e morre com status Exited (0). -i (interactive) mantém o stdin aberto para "
    "eu digitar comandos; -t (tty) aloca um pseudo-terminal, que dá o prompt \"/ #\", a edição de "
    "linha e o Ctrl+C. Para um shell utilizável os dois são necessários juntos.",
    "Não. Cada container é um processo isolado no kernel da máquina onde roda, com a sua própria "
    "camada de escrita. Os dois só partem da mesma imagem (somente-leitura) baixada do Docker Hub; "
    "o que um aluno cria ou apaga no container dele não chega ao do outro. Só compartilhariam "
    "estado através de algo externo, como um banco ou volume de rede.",
    # ---------------- P02 ----------------
    "Nos passos 1 e 2 é o MESMO container (lab-ubuntu): o curl foi gravado na camada de escrita "
    "dele, que sobrevive a stop/start. No passo 3 usei docker run, que cria um container NOVO a "
    "partir da imagem ubuntu:24.04 original, que não tem curl. Por isso deu o erro "
    "exec: \"curl\": executable file not found in $PATH.",
    "Sim, o curl estaria lá, porque o commit congela a camada de escrita como nova camada de "
    "imagem. Só que não resolve a reprodutibilidade: a imagem vira uma caixa-preta. Não fica "
    "registrado o que foi instalado, em que versão, nem em que ordem; ninguém consegue "
    "reconstruí-la a partir do código, revisar no Git ou atualizar a base de forma limpa. O "
    "Dockerfile documenta cada passo e pode ser refeito em qualquer máquina.",
    "É o kernel do host. No meu caso, o \"host\" é a VM Linux leve que o Docker Desktop roda no "
    "macOS: o explorar.sh mostrou \"Ubuntu 24.04.5 LTS\" no os-release, mas o curl foi compilado "
    "como aarch64-unknown-linux-gnu, ou seja, para a arquitetura do meu Mac. No Windows acontece o "
    "mesmo com o kernel do WSL2. Implicação: a imagem não traz kernel. Containers Linux precisam "
    "de um kernel Linux por baixo, e é por isso que Windows e macOS precisam da VM.",
    # ---------------- P03 ----------------
    "Sim. O rebuild sem alterações levou 0,56 s (real 0m0.562s), porque as quatro camadas "
    "apareceram como CACHED: o BuildKit comparou instrução e conteúdo copiado com o cache e não "
    "precisou executar nada.",
    "A primeira camada refeita foi [5/5] COPY app/server.js, que deu DONE 0.0s. Até ela, "
    "WORKDIR, COPY package.json e RUN npm install continuaram CACHED, ou seja, o npm install NÃO "
    "rodou de novo, porque o package.json não mudou.",
    "Qualquer alteração no código invalidaria a camada do COPY server.js e, com ela, TODAS as "
    "seguintes, incluindo o RUN npm install. O npm install rodaria a cada build, mesmo sem mudar "
    "nenhuma dependência. Neste app é rápido (zero dependências), mas num projeto real são "
    "minutos perdidos a cada build.",
    "O .dockerignore tira arquivos do contexto de build enviado ao daemon. Se node_modules do "
    "host não estivesse lá, ele seria enviado junto (contexto maior, build mais lento). E, num "
    "COPY . ., sobrescreveria o node_modules instalado dentro da imagem por um compilado para "
    "outro sistema operacional/arquitetura (no meu caso macOS arm64 contra Linux musl), o que "
    "quebra pacotes com binários nativos. Vi isso na prática na P12, onde precisei do "
    ".dockerignore para não levar a pasta node_modules vazia do host.",
    # ---------------- P04 ----------------
    "Não, nas duas execuções saiu \"Contador atual: 1\". O --tmpfs cria um sistema de arquivos em "
    "memória que pertence só àquele container. Com --rm, o container acaba, a memória é liberada e "
    "a segunda execução começa com /dados vazio. Repare que cada execução tem um hostname "
    "diferente (778761f13c0b e b6e6019cfac7).",
    "O bind mount aponta para uma pasta que EU escolho no host (labs/04-volumes-bind-mounts/dados); "
    "abri contador.txt e log.txt direto no Finder. O named volume fica numa área gerenciada pelo "
    "Docker: o inspect mostrou Mountpoint /var/lib/docker/volumes/dados-contador/_data, um caminho "
    "dentro da VM do Docker Desktop e não do meu Mac. Eu o acesso pelo nome, não pelo caminho.",
    "Porque o banco precisa de dados que sobrevivam ao container, mas sem depender da estrutura de "
    "pastas de cada máquina. O named volume é portável (o mesmo compose roda em qualquer host), "
    "tem dono e permissões criados corretamente para o usuário postgres e não sofre com a "
    "camada de compartilhamento de arquivos do Docker Desktop (lenta e com problemas de "
    "permissão no Windows/macOS). Também é fácil de listar, fazer backup e remover com "
    "docker volume.",
    # ---------------- P05 ----------------
    "Porque servidor e o busybox estavam na rede rede-lab05, definida por mim, e numa rede definida "
    "pelo usuário o Docker liga o DNS interno (o nslookup resolveu servidor para 172.21.0.2). No "
    "passo 5, os dois ficaram na bridge padrão, que não tem resolução por nome, e o wget deu "
    "\"bad address 'servidor-default'\". Pelo IP (172.17.0.2) a mesma requisição funcionou, o "
    "que mostra que o problema era só o nome.",
    "Não. O DNS interno só existe dentro das redes do Docker. Do host, o curl acessou "
    "localhost:8080, e a publicação de porta (-p 8080:80) encaminhou esse tráfego para a porta 80 "
    "do container. O docker port mostrou exatamente esse mapeamento: 80/tcp -> 0.0.0.0:8080.",
    "Sim. Cada container tem o seu próprio namespace de rede, então servidor e servidor-exposto "
    "ouviram na porta 80 ao mesmo tempo, sem conflito. Já duas publicações -p 8080:80 conflitam: "
    "a porta 8080 é do HOST e só um processo pode fazer bind nela. O segundo docker run falharia "
    "com \"port is already allocated\".",
    # ---------------- P06 ----------------
    "Sim, apareceu X-Servido-Por: Apache-Unifeg-Lab06 e também o X-Aluno: Higor - SD 2026B, que "
    "adicionei. Isso comprova que o Apache carregou o httpd.conf montado por bind mount, e não o "
    "padrão da imagem (que não define esses cabeçalhos). O log no formato customizado "
    "(tempo=1507-us) confirma o mesmo.",
    "Porque o bind mount não copia arquivos para dentro do container: o diretório htdocs É a pasta "
    "site/ do host. O Apache lê o index.html do disco a cada requisição, então salvar o arquivo "
    "já bastou. O curl seguinte devolveu o <h1> novo, sem restart e sem rebuild.",
    "Hoje, com :ro, qualquer escrita falharia com \"Read-only file system\" e o arquivo do host "
    "ficaria protegido. Sem :ro, a escrita funcionaria e alteraria o httpd.conf do MEU computador, "
    "porque é o mesmo arquivo. Um processo comprometido dentro do container poderia, por exemplo, "
    "mudar a configuração de forma persistente. Configuração deve ser montada como somente "
    "leitura.",
    # ---------------- P07 ----------------
    "Mostrou \"/status\". Como o proxy_pass tem uma URI (a barra final em http://backend:4000/), "
    "o Nginx troca o trecho casado pelo location (/api/) por essa URI. Fiz o mesmo com "
    "/api/qualquer/coisa, e o backend recebeu /qualquer/coisa.",
    "Testei os dois casos. (a) Backend parado depois que o Nginx subiu: o Nginx já tinha "
    "resolvido o nome para o IP e ficou tentando conectar até o timeout, e devolveu "
    "\"HTTP/1.1 504 Gateway Time-out\" (o log mostra \"upstream timed out ... while connecting to "
    "upstream\"). Se a conexão fosse recusada na hora, seria 502 Bad Gateway. (b) Nome que não "
    "existe na rede: o Nginx nem sobe, pois o nginx -t acusa \"host not found in upstream "
    "backend-errado\".",
    "O proxy reverso vira o único ponto de entrada: só ele expõe porta e a API fica invisível de "
    "fora (o backend não tem -p). Ele concentra TLS, cabeçalhos de segurança, logs, limites de "
    "requisição e cache, serve o estático sem gastar a API e permite trocar, escalar ou balancear "
    "backends sem o cliente perceber. O cliente sabe uma URL só; o resto é detalhe interno.",
    # ---------------- P08 ----------------
    "Porque os três serviços estão na mesma rede (lab08-compose-fundamentos_rede-lab08) e o Nginx "
    "fala com o backend pela porta interna 4000, resolvendo o nome do serviço pelo DNS do Docker "
    "(getent hosts backend devolveu 172.21.0.3). ports: só serve para publicar a porta no HOST; "
    "entre containers da mesma rede ela não é necessária.",
    "Substitui 4 comandos: docker network create, docker build do backend e três docker run "
    "(apache, backend e nginx), cada um com várias flags de porta, volume e rede. São 5, na "
    "verdade, contando o build. Versionado no Git, o arquivo vira documentação executável: "
    "qualquer pessoa sobe o ambiente idêntico com um comando, as mudanças passam por revisão "
    "(diff) e não dependem de alguém lembrar a ordem e as flags certas.",
    "Os dados das camadas de escrita seriam perdidos, porque o down remove os containers e o up "
    "cria novos. Nesta prática isso não faz diferença: o conteúdo do Apache e do Nginx vem de "
    "bind mounts (site/ e conf/ no host, que continuam lá) e o backend não guarda estado em "
    "disco (o contador de requisições dele, que vive em memória, voltou a 1).",
    # ---------------- P09 ----------------
    "Sim. Depois do docker rm -f e de recriar com o mesmo -v pgdata-lab09, o count(*) continuou 4, "
    "e o log mostrou \"Database directory appears to contain a database; Skipping initialization\". "
    "Se eu removesse o volume antes, o Postgres encontraria um diretório vazio, rodaria initdb e "
    "os scripts de init/ de novo, e voltaria só com o seed original. Qualquer dado inserido depois "
    "(e as alterações do backup/restore) seria perdido. Fiz isso no desafio.",
    "Porque o entrypoint da imagem só executa /docker-entrypoint-initdb.d quando PGDATA está "
    "vazio, ou seja, na criação do cluster. Com o volume já populado, ele pula a inicialização. "
    "Comprovei no desafio: depois de criar o 03-indice.sql, um docker restart NÃO criou o índice "
    "(o \\di não encontrou idx_alunos_ra); só com o volume removido o log mostrou "
    "\"running /docker-entrypoint-initdb.d/03-indice.sql\".",
    "A senha fica gravada no histórico do shell (~/.zsh_history), aparece na lista de processos "
    "para outros usuários da máquina e acaba no README ou em scripts versionados no Git. Com o "
    ".env (listado no .gitignore), a senha fica num arquivo local que não vai para o repositório. "
    "No repositório só existe o .env.example, com um valor de exemplo. A minha senha foi gerada "
    "com openssl rand -hex 12 e não aparece em nenhuma evidência.",
    # ---------------- P10 ----------------
    "depends_on simples só espera o CONTAINER do db ser criado e iniciado. O Postgres, porém, "
    "ainda leva alguns segundos rodando initdb e os scripts de init (no meu log, o servidor "
    "temporário subiu, rodou 01 e 02 e só depois reiniciou pronto). Nessa janela o pgAdmin, ou "
    "uma API, tentaria conectar e receberia \"connection refused\" ou \"the database system is "
    "starting up\". Com service_healthy, o Compose esperou o pg_isready passar (a saída mostra "
    "\"db-1 Waiting\" e depois \"Healthy\") antes de iniciar o pgadmin.",
    "Porque o servers.json é um arquivo de configuração que costuma ir para o Git: guardar a "
    "senha nele vazaria a credencial do banco. Não chega a ser um problema para a prática: o "
    "pgAdmin já traz host, porta, banco e usuário preenchidos e só pede a senha "
    "(POSTGRES_PASSWORD do .env) na primeira conexão, com opção de salvá-la no volume "
    "pgadmin_data.",
    "Não. A P10 usa outro projeto Compose e outro volume (lab10-pgadmin-compose_pgdata), "
    "independente do pgdata-lab09 da P09. O que a P10 garante é que os SEUS dados persistem: "
    "fiz down sem -v, os dois volumes continuaram listados e, depois de subir de novo, o "
    "count(*) deu 4. Só o down -v removeu os volumes (\"Volume ... Removed\").",
    # ---------------- P11 ----------------
    "Porque a imagem final do multi-stage parte do node:20-alpine e recebe só o dist/ compilado e "
    "as dependências de produção. A :single carrega o node:20 completo (Debian, com compiladores e "
    "ferramentas, cerca de 1,2 GB só de camadas da base), o TypeScript, @types/node e o src/*.ts. "
    "Resultado medido: 52.525.057 bytes contra 402.555.925 bytes (cerca de 7,7 vezes menor). "
    "Dentro da :single ainda estão tsc, tsserver e index.ts; na :multi só há dist/, node_modules "
    "e package.json.",
    "Não como imagem com tag. O estágio builder vira camadas no cache do BuildKit (por isso o "
    "segundo build é instantâneo), mas não aparece em docker image ls e não é enviado num push. "
    "Ele ocupa espaço em disco como cache de build (docker builder du), que dá para limpar com "
    "docker builder prune. Só vira imagem se eu pedir com --target builder -t ...",
    "Não prova. O curl mostra que as duas respondem à rota / igual, mas a base é diferente: glibc "
    "na Debian e musl na Alpine, com bibliotecas e versões de pacotes distintas. Um caso de borda "
    "(módulo nativo, fuso horário/locale, DNS, consumo de memória: a :multi usou 44 MB de RSS e a "
    ":single 39 MB) pode se comportar diferente. Equivalência para produção pede testes "
    "automatizados rodando NA imagem final, carga, segurança etc. Foi esse o motivo do estágio de "
    "teste no desafio.",
    # ---------------- P12 ----------------
    "O bind mount ./app-react:/app esconderia o node_modules da imagem com a pasta do host, que "
    "está vazia (contei 0 itens em app-react/node_modules no Mac). Testei rodando a mesma imagem "
    "só com o bind mount, e o npm run dev falhou com \"sh: vite: not found\". Com o volume, o "
    "container enxerga os 36 pacotes (42,7 MB) instalados no build.",
    "O Dockerfile.dev copia SÓ o package.json e roda npm install (com devDependencies, porque o "
    "Vite é necessário); o código-fonte chega depois pelo bind mount, e o CMD é o servidor de "
    "desenvolvimento. O Dockerfile de produção copia o código inteiro para o estágio build, gera "
    "o dist/ e a imagem final (nginx:alpine) recebe apenas os arquivos estáticos (index.html, um "
    ".js e um .css) mais o nginx.conf. Não há Node, node_modules nem código-fonte.",
    "O npm run dev é um servidor de desenvolvimento: não minifica, recompila sob demanda, abre "
    "WebSocket de HMR, observa arquivos (com polling) e não foi feito para carga, cache nem "
    "segurança. O npm run preview serve só para conferir o build localmente. Para arquivos "
    "estáticos, o Nginx é muito mais leve e rápido, com cache, gzip e o try_files para SPA (uma "
    "rota inexistente devolveu o index.html). Também dispensa o Node na imagem: 26,3 MB contra "
    "89,4 MB da alternativa com Vite.",
    # ---------------- P13 ----------------
    "Porque limita o estrago se o processo for comprometido: um atacante herda o usuário do "
    "processo. Como root (UID 0) dentro do container, ele poderia escrever em qualquer arquivo do "
    "container e de volumes montados, e qualquer falha de isolamento do kernel vira root no host. "
    "Com appuser (uid=100), ele não instala pacotes nem altera o sistema. Mesmo em laboratório "
    "vale criar o hábito, porque o mesmo Dockerfile depois vai para produção.",
    "Como secret. A única variável de ambiente é DB_PASSWORD_FILE=/run/secrets/db_password, que é "
    "o CAMINHO e não a senha; o docker inspect mostrou isso e a senha não aparece. Uma variável "
    "comum com a senha ficaria visível em docker inspect, em docker compose config, em "
    "/proc/<pid>/environ e em qualquer log que despeje o ambiente. O secret fica num arquivo "
    "montado em /run/secrets, lido só pelo processo e fora da configuração do container.",
    "O kernel aciona o OOM killer da cgroup e mata um processo do container. Forcei isso: "
    "alocando 20 MB a cada 100 ms, o node do exec morreu com exit code 137 (SIGKILL), o "
    "docker inspect passou a mostrar OOMKilled=true e o compose events registrou \"oom\". Chegou a "
    "220 MB porque, sem memswap_limit, o Docker permite swap igual ao limite (128M + 128M). Como "
    "o processo morto foi o do exec, o servidor principal continuou healthy. Se fosse o PID 1, o "
    "container cairia e reiniciaria só com uma restart policy.",
    # ---------------- P14 ----------------
    "Navegador (host) -> localhost:8084, publicado pelo Docker -> container frontend (Nginx, porta "
    "80): o location /api/ casa e remove o prefixo -> rede rede-integrador, DNS resolve backend "
    "para 172.21.0.3 -> container backend (Node, porta 4000) recebe GET /alunos -> o driver pg "
    "usa PGHOST=db, resolvido para 172.21.0.2 -> container db (PostgreSQL, porta 5432) executa o "
    "SELECT. A resposta volta pelo mesmo caminho: db -> backend (JSON) -> Nginx -> navegador. O "
    "log do frontend registrou \"GET /api/alunos HTTP/1.1\" 200 316.",
    "ports: publica no host, então só tem quem precisa ser acessado de FORA do Docker: o frontend "
    "(o site, 8084) e o pgAdmin (ferramenta do administrador, 8083). backend e db só são "
    "chamados por outros containers da rede interna, então não publicar diminui a superfície de "
    "ataque: o banco e a API não ficam acessíveis pela rede da máquina. O Docker mostra "
    "\"4000/tcp\" e \"5432/tcp\" sem mapeamento.",
    "O backend subiria enquanto o Postgres ainda roda initdb e os scripts de init. Os primeiros "
    "GET /alunos retornariam 500 (\"connection refused\" ou \"the database system is starting "
    "up\"), e o healthcheck do backend poderia oscilar. Acontece só na primeira subida, porque "
    "depois o volume já está inicializado e o Postgres fica pronto em menos de um segundo. Com "
    "service_healthy, o up mostrou \"db-1 Waiting\", \"Healthy\" e só então \"backend-1 "
    "Starting\". Também fiz o frontend esperar o backend ficar healthy.",
    "Não. O React roda no NAVEGADOR, fora do Docker, e só conhece a origem localhost:8084. Ele "
    "faz fetch(\"/api/alunos\") para o Nginx. O db não tem porta publicada, então o navegador não "
    "teria como alcançá-lo, e as credenciais (PGPASSWORD) existem só no ambiente do container "
    "backend. Quem fala com o banco é sempre a API.",
]

# ---------------------------------------------------------------------------
# Desafios: texto explicativo + blocos de evidência + imagens
# ---------------------------------------------------------------------------
DESAFIOS = [
    # P01
    dict(texto=[
        "Usei o prefixo hb-sd- (minhas iniciais + a disciplina) e o filtro por expressão regular "
        "name=^hb-sd-. O ^ garante que só entram nomes que COMEÇAM com o prefixo.",
    ], ev=("p01", ["for n in 1 2 3; do docker run -d --name hb-sd-$n", "docker ps --filter \"name=^hb-sd-\""], 8)),
    # P02
    dict(texto=[
        "Sem commit: montei a pasta saida/ do host em /saida por bind mount, instalei o figlet num "
        "container descartável e gravei o banner com tee. O container sumiu (--rm), mas o arquivo "
        "ficou no meu Mac em labs/02-ubuntu-container/saida/banner-turma.txt.",
    ], ev=("p02", ["docker run --rm -v \"$(pwd)/saida:/saida\"", "ls -l saida/"], 20)),
    # P03
    dict(texto=[
        "Adicionei HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 com "
        "wget -q --spider http://localhost:${PORTA}/. Usei o wget porque a imagem alpine não tem "
        "curl, mas tem o wget do busybox. Construí como app-fundamentos:1.1 e acompanhei a "
        "coluna STATUS passar de (health: starting) para (healthy).",
    ], ev=("p03", ["docker run -d --name app03-health", "docker inspect --format \"{{json .State.Health.Status}}"], 6)),
    # P04
    dict(texto=[
        "Removi o volume e montei de novo pelo mesmo nome. O Docker criou silenciosamente um volume "
        "NOVO e vazio com esse nome, e o contador voltou para 1: os dados anteriores (contador = 2) "
        "foram perdidos de vez. Lição: -v nome:/caminho cria o volume se ele não existir, então "
        "apagar um volume não dá erro depois, só perde dados.",
    ], ev=("p04", ["docker volume ls --filter name=dados-contador", "docker volume rm dados-contador", "docker run --rm -v \"$(pwd)/scripts:/scripts:ro\" -v dados-contador:/dados alpine sh /scripts/contador.sh\nContador atual: 1\n--- historico (log.txt) ---\n2026-11-18 14:05:36"], 6)),
    # P05
    dict(texto=[
        "Criei rede-lab05-b e usei docker network connect para ligar o container servidor também a "
        "ela. O inspect mostra um IP em cada rede (172.21.0.2 e 172.22.0.2), e um busybox na rede "
        "nova também alcançou o servidor pelo nome.",
    ], ev=("p05", ["docker network create rede-lab05-b", "docker inspect servidor --format", "docker network inspect rede-lab05-b", "docker run --rm --network rede-lab05-b"], 6)),
    # P06
    dict(texto=[
        "Criei site/sobre.html com o container rodando, e ele respondeu 200 na hora. Para mostrar "
        "o efeito do Options, criei a pasta site/materiais/ sem index.html: com Indexes, o Apache "
        "listava os arquivos (\"Index of /materiais\"). Troquei para Options -Indexes "
        "+FollowSymLinks no <Directory> do htdocs, validei com httpd -t e recarreguei com "
        "httpd -k graceful (sem reiniciar o container). A listagem passou a dar 403, mas os "
        "arquivos e o sobre.html continuam acessíveis.",
    ], ev=("p06", ["curl -s -o /dev/null -w \"sobre.html", "curl -s http://localhost:8080/materiais/ |", "docker exec lab-apache httpd -t && docker exec lab-apache httpd -k graceful", "curl -s -o /dev/null -w \"materiais/", "docker logs lab-apache 2>&1 | tail"], 6)),
    # P07
    dict(texto=[
        "Adicionei location /saude/ { proxy_pass http://backend:4000/status; } e, para comparar, "
        "location /bruto/ { proxy_pass http://backend:4000; }, sem URI nenhuma. Recarreguei com "
        "nginx -s reload. Regra: se o proxy_pass TEM URI (mesmo que seja só \"/\"), o Nginx "
        "substitui o prefixo do location por ela. É o caso de /api/ -> / e de /saude/ -> /status. "
        "Se NÃO tem URI, a requisição original vai inteira: /bruto/status chegou como "
        "/bruto/status.",
    ], ev=("p07", ["docker exec lab-nginx nginx -t && docker exec lab-nginx nginx -s reload", "for u in /api/status /saude/ /bruto/status"], 6)),
    # P08
    dict(texto=[
        "No nginx usei NGINX_HOST: ${NGINX_HOST:-sd-higor.local} (valor padrão, que pode ser "
        "sobrescrito pelo shell ou pelo .env). O docker compose config mostra a variável resolvida "
        "nos dois casos. No backend, adicionei healthcheck com wget em /status e mudei o nginx "
        "para depends_on: condition: service_healthy. O up mostra o Compose esperando o backend "
        "ficar Healthy antes de iniciar o proxy.",
    ], ev=("p08", ["docker compose config | grep", "NGINX_HOST=lab08.unifeg.test", "docker compose up -d 2>&1 | grep", "docker compose ps --format \"table {{.Service}}\\t{{.Status}}\"", "docker compose exec nginx printenv"], 8)),
    # P09
    dict(texto=[
        "Criei init/03-indice.sql com CREATE INDEX IF NOT EXISTS idx_alunos_ra ON alunos (ra). "
        "Primeiro mostrei que um restart com o volume antigo NÃO roda o script; depois removi o "
        "volume e recriei o container. O \\d alunos lista o índice, e o EXPLAIN (com seqscan "
        "desligado, porque a tabela é minúscula) mostra o planner usando o índice. Observação: a "
        "constraint UNIQUE de ra já cria o índice alunos_ra_key, então em produção esse índice "
        "seria redundante.",
    ], ev=("p09", ["docker restart lab-postgres", "docker logs lab-postgres 2>&1 | grep -E \"running /docker-entrypoint|CREATE INDEX\"", "docker exec lab-postgres psql -U unifeg -d lab_sistemas_distribuidos -c \"\\d alunos\"", "docker exec lab-postgres psql -U unifeg -d lab_sistemas_distribuidos -c \"SET enable_seqscan"], 16)),
    # P10
    dict(texto=[
        "No pgadmin adicionei um healthcheck com wget em http://localhost/misc/ping (rota que "
        "responde PING sem login), com start_period de 40s para cobrir o boot. Criei um serviço "
        "\"monitor\" (busybox) que depende do pgadmin com condition: service_healthy e registra o "
        "ping a cada 15s. O up mostra a cadeia db Healthy -> pgadmin Healthy -> monitor Started.",
        "Normalmente isso não é necessário para o pgAdmin: ele é uma ferramenta humana, que fica no "
        "fim da cadeia. Nenhum serviço depende dele e, se a página demorar, o usuário só recarrega. "
        "Um healthcheck nele teria valor para monitoramento ou para um proxy que precise saber se "
        "pode encaminhar tráfego.",
    ], ev=("p10", ["docker compose up -d 2>&1 | grep -E \"Waiting", "docker compose ps --format \"table {{.Service}}\\t{{.Status}}\"\nSERVICE   STATUS\ndb        Up 2", "docker compose logs monitor"], 8)),
    # P11
    dict(texto=[
        "Adicionei o estágio \"FROM builder AS test\", que sobe a API compilada e faz um smoke test "
        "(curl + grep por \"compilado\":true). Como o BuildKit só constrói os estágios de que o alvo "
        "precisa, o teste roda com --target test (num CI, antes do build final), e a imagem :multi "
        "ficou com exatamente o mesmo tamanho: 52.525.057 bytes antes e depois.",
    ], ev=("p11", ["docker build --progress=plain --no-cache --target test", "docker build -q -f Dockerfile -t app-multistage:multi . &&", "docker image ls app-multistage\nWARNING: This output is designed for human readability. For machine-readable output, please use --format.\nIMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA\napp-multistage:multi    4b08"], 8)),
    # P12
    dict(texto=[
        "Criei Dockerfile.dev-em-producao, um anti-exemplo que leva Node, node_modules completo e o "
        "código para rodar o Vite em \"produção\". A imagem multi-stage com Nginx ficou com "
        "26,3 MB de conteúdo (93,4 MB em disco), contra 89,4 MB (416 MB) da alternativa, cerca "
        "de 3,4 vezes maior, além de mais lenta e com mais superfície de ataque.",
        "Troubleshooting real durante a prática: o primeiro build de produção falhou com \"Code is "
        "nested too deeply\" no react-dom. Investiguei e descobri que o npm tinha instalado o "
        "rollup 4.68.6, publicado na manhã do mesmo dia (18/11/2026). Com 4.68.5 e 4.68.0 o build "
        "passou, então fixei a versão com \"overrides\": {\"rollup\": \"4.68.5\"} no package.json "
        "e acrescentei um .dockerignore. O dev server não tinha sido afetado porque usa esbuild, "
        "e não o rollup.",
        "IMG:p12-dev-hot-reload.png",
        "IMG:p12-prod-nginx.png",
    ], ev=("p12", ["docker image ls app-react-lab12\nWARNING: This output is designed for human readability. For machine-readable output, please use --format.\nIMAGE                         ID             DISK USAGE   CONTENT SIZE   EXTRA\napp-react-lab12:dev-em-prod   1783", "docker image inspect -f \"{{.RepoTags}} -> {{.Size}} bytes\" app-react-lab12:prod", "docker build -q -t app-react-lab12:prod .\nDockerfile:8"], 12)),
    # P13
    dict(texto=[
        "Falha 1: troquei DB_PASSWORD_FILE para /run/secrets/db_pasword (erro de digitação). O "
        "container continua healthy, porque o /saude não depende do segredo, o que já é uma lição "
        "sobre healthchecks rasos. O diagnóstico veio só das ferramentas: docker compose logs "
        "mostrou \"AVISO: segredo NAO encontrado em /run/secrets/db_pasword\", e o docker inspect "
        "comparou a variável (…/db_pasword) com o mount real (/run/secrets/db_password).",
        "Falha 2: matei o processo com docker compose kill -s SIGKILL. O docker compose ps mostrou "
        "\"Exited (137)\", e o inspect deu ExitCode=137 com OOMKilled=false. 137 = 128 + 9 (SIGKILL), "
        "e o OOMKilled=false descarta falta de memória, ao contrário do teste da pergunta 3. O "
        "docker compose events dá a linha do tempo (oom, kill, die, start...).",
    ], ev=("p13", ["docker compose logs app | tail -n 2", "docker inspect $(docker compose ps -q app) --format \"Env DB_PASSWORD_FILE", "docker compose kill -s SIGKILL app", "docker inspect $(docker compose ps -aq app)", "docker compose events --since 2m"], 24)),
    # P14
    dict(texto=[
        "No backend criei a rota DELETE /alunos/:id: valida o id numérico, executa DELETE ... "
        "RETURNING e devolve 404 se o aluno não existir. No React, adicionei um botão Excluir por "
        "linha (fetch DELETE /api/alunos/:id e recarrega a lista), além de um formulário de "
        "cadastro. O frontend agora também espera o backend ficar healthy.",
        "Teste ponta a ponta sem reiniciar nenhum container: abri a página num Chrome headless, "
        "controlado pelo DevTools Protocol (script em Node), cadastrei \"Aluno Teste Exclusao\" "
        "pelo formulário e cliquei no botão Excluir dele. A tela, o log do Nginx "
        "(DELETE /api/alunos/7 200, com user-agent HeadlessChrome) e o log do backend (\"aluno 7 "
        "removido\") confirmam o caminho tela -> Nginx -> API -> Postgres. Depois a consulta pelo "
        "pgAdmin mostrou os 5 alunos restantes.",
        "IMG:p14-ui-antes-de-excluir.png",
        "IMG:p14-ui-depois-de-excluir.png",
    ], ev=("p14", ["node --experimental-websocket", "docker compose logs backend | grep removido", "curl -s -X DELETE http://localhost:8084/api/alunos/999"], 30)),
]

# Quadro extra (pré-requisitos): saída de docker version
PRE_REQ = ("docker version / docker info", [
    "$ docker version --format 'Client {{.Client.Version}} ({{.Client.Os}}/{{.Client.Arch}}) | Server {{.Server.Version}} ({{.Server.Os}}/{{.Server.Arch}})'",
])
