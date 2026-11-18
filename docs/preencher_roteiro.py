# -*- coding: utf-8 -*-
"""Preenche o Roteiro_Docker_Aluno.docx com evidências reais, respostas e desafios.

Uso:  python3 docs/preencher_roteiro.py <pasta_docx_descompactado>
Lê:   docs/respostas.py, evidencias/pXX.txt e evidencias/prints/*.png
"""
import os
import re
import struct
import sys
from xml.sax.saxutils import escape

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "docs"))
import respostas as R  # noqa: E402

UN = sys.argv[1]
DOC = os.path.join(UN, "word", "document.xml")
EVID = os.path.join(RAIZ, "evidencias")
DATA_ENTREGA = "18/11/2026"
NOME_ALUNO = "Higor Bachião Madeira de Castro"
RA_ALUNO = "23327029"

# ------------------------------------------------------------------ evidências
_blocos_cache = {}


def blocos(arq):
    """Divide evidencias/<arq>.txt em blocos que começam com '$ '."""
    if arq not in _blocos_cache:
        txt = open(os.path.join(EVID, arq + ".txt"), encoding="utf8").read()
        partes, atual = [], []
        for linha in txt.split("\n"):
            if linha.startswith("$ ") and atual:
                partes.append("\n".join(atual).rstrip())
                atual = []
            if linha.startswith("### "):
                continue
            atual.append(linha)
        if atual:
            partes.append("\n".join(atual).rstrip())
        _blocos_cache[arq] = [p for p in partes if p.startswith("$ ")]
    return _blocos_cache[arq]


def bloco(arq, prefixo, max_linhas):
    for b in blocos(arq):
        if b[2:].startswith(prefixo):
            linhas = b.split("\n")
            if len(linhas) > max_linhas + 1:
                linhas = linhas[: max_linhas + 1] + ["[...]"]
            return "\n".join(linhas)
    raise SystemExit(f"bloco não encontrado em {arq}: {prefixo[:70]!r}")


def evidencia(arq, prefixos, max_linhas):
    return "\n".join(bloco(arq, p, max_linhas) for p in prefixos)


# ------------------------------------------------------------------ XML helpers
AZUL = "262626"  # cor das respostas (tema preto)


def run(texto, bold=False, italic=False, cor=None, mono=False, tam=None, highlight=None):
    rpr = ""
    if mono:
        rpr += '<w:rFonts w:ascii="Consolas" w:eastAsia="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
    if bold:
        rpr += "<w:b/><w:bCs/>"
    if italic:
        rpr += "<w:i/><w:iCs/>"
    if cor:
        rpr += f'<w:color w:val="{cor}"/>'
    if tam:
        rpr += f'<w:sz w:val="{tam}"/><w:szCs w:val="{tam}"/>'
    if highlight:
        rpr += f'<w:highlight w:val="{highlight}"/>'
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(texto)}</w:t></w:r>'


def par(runs, before=0, after=120, ind=0, keep=False):
    ppr = f'<w:spacing w:before="{before}" w:after="{after}"/>'
    if ind:
        ppr += f'<w:ind w:left="{ind}"/>'
    if keep:
        ppr = "<w:keepNext/>" + ppr
    return f"<w:p><w:pPr>{ppr}</w:pPr>{''.join(runs)}</w:p>"


def par_codigo(linha):
    # sem espaço extra entre linhas, fonte monoespaçada 7,5 pt
    return ('<w:p><w:pPr><w:spacing w:after="0" w:line="228" w:lineRule="auto"/></w:pPr>'
            + run(linha if linha else " ", mono=True, tam=15) + "</w:p>")


def codigo(texto):
    return "".join(par_codigo(l) for l in texto.split("\n"))


def caixa_codigo(texto, titulo=None):
    """Tabela de 1 célula, cinza claro, com o texto em Consolas."""
    cab = par([run(titulo, italic=True, cor="5B5B5B", tam=17)], after=60) if titulo else ""
    return (
        '<w:tbl><w:tblPr><w:tblW w:w="9350" w:type="dxa"/>'
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/></w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="9350"/></w:tblGrid><w:tr><w:tc>'
        '<w:tcPr><w:tcW w:w="9350" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="F5F5F5"/></w:tcPr>'
        + cab + codigo(texto) + "</w:tc></w:tr></w:tbl>"
        + par([], after=60)
    )


# ------------------------------------------------------------------ imagens
IMAGENS = []  # (rId, nome_arquivo)


def png_tamanho(caminho):
    with open(caminho, "rb") as f:
        cab = f.read(24)
    return struct.unpack(">II", cab[16:24])


def imagem(nome, largura_pol=5.6):
    caminho = os.path.join(EVID, "prints", nome)
    w, h = png_tamanho(caminho)
    cx = int(largura_pol * 914400)
    cy = int(cx * h / w)
    idx = len(IMAGENS) + 1
    rid = f"rIdPrint{idx}"
    IMAGENS.append((rid, nome))
    pid = 9000 + idx
    desenho = (
        '<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{pid}" name="Print {idx}" descr="{escape(nome)}"/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{pid}" name="{escape(nome)}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        "</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
    )
    legenda = par([run(f"Print: evidencias/prints/{nome}", italic=True, cor="5B5B5B", tam=16)], after=160)
    return f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="40"/></w:pPr>{desenho}</w:p>' + legenda


def itens_texto(lista, ind=0):
    """Converte lista de textos (com prefixos IMG:/CODE:) em XML."""
    out = ""
    for t in lista:
        if t.startswith("IMG:"):
            out += imagem(t[4:])
        elif t.startswith("CODE:"):
            out += caixa_codigo(t[5:])
        else:
            out += par([run(t)], after=100, ind=ind)
    return out


# ------------------------------------------------------------------ montagem
s = open(DOC, encoding="utf8").read()
original_len = len(s)

# 1) Capa: nome, RA, turma, data
VAZIO = r'<w:p w14:paraId="[0-9A-F]+" w14:textId="77777777" w:rsidR="006854BB" w:rsidRDefault="006854BB"/>'


def preencher_celula(s, rotulo, conteudo_runs):
    i = s.index(f"<w:t>{rotulo}</w:t>")
    m = re.compile(VAZIO).search(s, i)
    return s[: m.start()] + f"<w:p>{conteudo_runs}</w:p>" + s[m.end():]


s = preencher_celula(s, "Nome do aluno", run(NOME_ALUNO, tam=20))
s = preencher_celula(s, "RA", run(RA_ALUNO, tam=20))
s = preencher_celula(s, "Turma", run("PREENCHER", tam=20, highlight="yellow"))
s = preencher_celula(s, "Data", run(DATA_ENTREGA, tam=20))

# 2) Ambiente + evidência dos pré-requisitos
ancora = "Antes de iniciar a Prática 01, confirme que o ambiente está pronto."
i = s.index(ancora)
fim = s.index("</w:p>", i) + len("</w:p>")
bloco_amb = par([run("Meu ambiente: ", bold=True, cor=AZUL), run(R.AMBIENTE[0], cor=AZUL)], before=60, after=80)
bloco_amb += par([run(R.AMBIENTE[1], cor=AZUL)], after=80)
bloco_amb += caixa_codigo("\n".join(blocos("p00")), "📎 Verificação do ambiente (saída real)")
s = s[:fim] + bloco_amb + s[fim:]

# 3) Quadros 📎: troca as linhas em branco pela saída real
pos = 0
for n, (arq, prefixos, maxl) in enumerate(R.QUADROS, start=1):
    i = s.index("<w:t>📎 ", pos)
    fim_p = s.index("</w:p>", i) + len("</w:p>")
    fim_tc = s.index("</w:tc>", fim_p)
    if arq == "TEXTO_P14_TELA":
        conteudo = ""
        for t in R.TEXTO_P14_TELA:
            if t.startswith("IMG:"):
                conteudo += imagem(t[4:], largura_pol=5.3)
            elif t.startswith("CODE:"):
                conteudo += codigo(t[5:])
            else:
                conteudo += par([run(t, tam=19)], after=80)
    else:
        conteudo = codigo(evidencia(arq, prefixos, maxl))
    s = s[:fim_p] + conteudo + s[fim_tc:]
    pos = fim_p + len(conteudo)
assert "<w:t>📎 " not in s[pos:], "sobrou quadro 📎 sem preencher"
print(f"quadros preenchidos: {n}")

# 4) Respostas: depois de cada pergunta numerada
padrao_pergunta = re.compile(r'<w:p [^>]*><w:pPr><w:spacing w:before="120" w:after="60"/></w:pPr>.*?</w:p>', re.S)
perguntas = list(padrao_pergunta.finditer(s))
assert len(perguntas) == len(R.RESPOSTAS) == 45, (len(perguntas), len(R.RESPOSTAS))
for m, resp in reversed(list(zip(perguntas, R.RESPOSTAS))):
    xml = par([run("Resposta: ", bold=True, cor=AZUL), run(resp, cor=AZUL)], before=20, after=140, ind=360)
    s = s[: m.end()] + xml + s[m.end():]
print("respostas inseridas: 45")

# 5) Desafios: depois do enunciado (parágrafo seguinte ao título "Desafio")
padrao_desafio = re.compile(r'<w:pStyle w:val="Ttulo2"/></w:pPr><w:bookmarkStart[^>]*/><w:r><w:t>Desafio</w:t>')
titulos = list(padrao_desafio.finditer(s))
assert len(titulos) == len(R.DESAFIOS) == 14, (len(titulos), len(R.DESAFIOS))
for m, d in reversed(list(zip(titulos, R.DESAFIOS))):
    fim_titulo = s.index("</w:p>", m.end()) + len("</w:p>")
    fim_enunciado = s.index("</w:p>", fim_titulo) + len("</w:p>")
    xml = par([run("Resolução do desafio", bold=True, cor=AZUL)], before=120, after=60, keep=True)
    xml += itens_texto(d["texto"])
    arq, prefixos, maxl = d["ev"]
    xml += caixa_codigo(evidencia(arq, prefixos, maxl), "Evidência do desafio (saída real)")
    s = s[:fim_enunciado] + xml + s[fim_enunciado:]
print("desafios inseridos: 14")

# 6) Checklists: marca cada item como concluído
n_check = 0
# Pré-requisitos de Windows/Ubuntu: situação real no meu Mac (não marco o que não se aplica)
PRE_REQ_MAC = {
    "Windows 10/11": ("  — não se aplica: uso macOS 27 (Apple Silicon)", "7F7F7F"),
    "WSL2 instalado": ("  — não se aplica: no macOS o Docker Desktop usa a própria VM Linux", "7F7F7F"),
    "Docker Desktop instalado, configurado": ("  ✔ equivalente: Docker Desktop 29.0.1 para macOS", "2E7D32"),
    "Ubuntu 22.04 LTS": ("  — não se aplica: uso macOS 27 (Apple Silicon)", "7F7F7F"),
    "Docker Engine instalado a partir": ("  ✔ equivalente: Docker Engine 29.0.1 (via Docker Desktop)", "2E7D32"),
    "Usuário do laboratório incluído no grupo": ("  — não se aplica: o Docker Desktop expõe o socket ao meu usuário", "7F7F7F"),
}


def marcar(m):
    global n_check
    n_check += 1
    corpo = m.group(0)
    sufixo, cor = "  ✔ concluído", "2E7D32"
    for chave, (txt, c) in PRE_REQ_MAC.items():
        if chave in corpo:
            sufixo, cor = txt, c
    return corpo[: -len("</w:p>")] + run(sufixo, bold=True, cor=cor) + "</w:p>"


s = re.sub(r'<w:p [^>]*><w:pPr><w:pStyle w:val="PargrafodaLista"/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="3"/></w:numPr>(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?</w:pPr>.*?</w:p>', marcar, s, flags=re.S)
print(f"itens de checklist marcados: {n_check}")

# 7) Ficha de entrega: data em cada linha 01..14
i_ficha = s.rindex("Ficha de entrega</w:t>")
for k in range(1, 15):
    rot = f"<w:t>{k:02d}</w:t>"
    i = s.index(rot, i_ficha)
    m = re.compile(VAZIO).search(s, i)
    s = s[: m.start()] + f"<w:p>{run(DATA_ENTREGA, tam=20)}</w:p>" + s[m.end():]
    i_ficha = m.start()
print("ficha de entrega: datas preenchidas")

# namespaces usados pelas imagens
if 'xmlns:wp="' not in s[:3000]:
    s = s.replace("<w:document ", '<w:document xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" ', 1)
if 'xmlns:r="' not in s[:3000]:
    s = s.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
open(DOC, "w", encoding="utf8").write(s)

# 8) Tema preto: troca a paleta azul do template por preto/cinzas
PALETA = {
    "1B3A6B": "000000",  # navy: título da capa e cabeçalho das tabelas
    "2E75B6": "1A1A1A",  # azul dos títulos de seção, bordas e "ROTEIRO DO ALUNO"
    "2E74B5": "1A1A1A",
    "1F4D78": "1A1A1A",
    "1F4E79": "262626",
    "0563C1": "333333",  # hiperlinks
    "EEF3FB": "EDEDED",  # fundo do painel Windows
    "EAF2FA": "F2F2F2",  # fundo das notas
}


def trocar_paleta(xml):
    for azul, preto in PALETA.items():
        xml = xml.replace(f'"{azul}"', f'"{preto}"')
    return xml


for parte in ["document.xml", "styles.xml", "header1.xml", "footer1.xml"]:
    cam = os.path.join(UN, "word", parte)
    conteudo = trocar_paleta(open(cam, encoding="utf8").read())
    open(cam, "w", encoding="utf8").write(conteudo)
print("tema: azul -> preto aplicado")

# 9) Imagens: media + relacionamentos + content type
os.makedirs(os.path.join(UN, "word", "media"), exist_ok=True)
rels_p = os.path.join(UN, "word", "_rels", "document.xml.rels")
rels = open(rels_p, encoding="utf8").read()
for rid, nome in IMAGENS:
    dados = open(os.path.join(EVID, "prints", nome), "rb").read()
    open(os.path.join(UN, "word", "media", nome), "wb").write(dados)
    rels = rels.replace(
        "</Relationships>",
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{nome}"/></Relationships>',
    )
open(rels_p, "w", encoding="utf8").write(rels)
ct_p = os.path.join(UN, "[Content_Types].xml")
ct = open(ct_p, encoding="utf8").read()
if 'Extension="png"' not in ct:
    ct = ct.replace("<Default Extension=\"xml\"", '<Default Extension="png" ContentType="image/png"/><Default Extension="xml"', 1)
open(ct_p, "w", encoding="utf8").write(ct)
print(f"imagens embutidas: {len(IMAGENS)}  |  document.xml: {original_len} -> {len(s)} bytes")
