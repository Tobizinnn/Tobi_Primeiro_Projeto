import pygame
import sys
import datetime
import threading
import os

from openai import OpenAI


# ============================================================
# CONFIGURAÇÕES
# ============================================================

pygame.init()

LARGURA = 1100
ALTURA = 700
FPS = 60

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Assistente Virtual")

RELOGIO = pygame.time.Clock()


# ============================================================
# CORES
# ============================================================

FUNDO = (18, 20, 28)
PAINEL = (28, 31, 42)
PAINEL_2 = (35, 39, 52)

BRANCO = (240, 240, 245)
CINZA = (160, 165, 175)
CINZA_ESCURO = (80, 85, 95)

AZUL = (80, 140, 255)
AZUL_ESCURO = (55, 100, 190)

VERDE = (70, 200, 130)
VERMELHO = (220, 80, 90)
AMARELO = (240, 200, 80)
ROXO = (160, 100, 240)


# ============================================================
# FONTES
# ============================================================

FONTE_GRANDE = pygame.font.SysFont(
    "arial",
    36,
    bold=True
)

FONTE_TITULO = pygame.font.SysFont(
    "arial",
    28,
    bold=True
)

FONTE_MEDIA = pygame.font.SysFont(
    "arial",
    21,
    bold=True
)

FONTE_NORMAL = pygame.font.SysFont(
    "arial",
    18
)

FONTE_PEQUENA = pygame.font.SysFont(
    "arial",
    15
)


# ============================================================
# API
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY")

cliente = None

if API_KEY:
    try:
        cliente = OpenAI(
            api_key=API_KEY
        )
    except Exception:
        cliente = None


MODELO = "gpt-6-luna"


# ============================================================
# ESTADO
# ============================================================

tela_atual = "inicio"

mensagem_usuario = ""

chat_mensagens = [
    {
        "role": "assistant",
        "content": "Olá! Eu sou sua assistente virtual. Como posso ajudar?"
    }
]

historico_api = []

resposta_carregando = False

erro_api = ""

tarefas = []


# ============================================================
# FUNÇÕES VISUAIS
# ============================================================

def desenhar_texto(
    texto,
    fonte,
    cor,
    x,
    y,
    centralizado=False
):

    imagem = fonte.render(
        str(texto),
        True,
        cor
    )

    if centralizado:

        rect = imagem.get_rect(
            center=(x, y)
        )

    else:

        rect = imagem.get_rect(
            topleft=(x, y)
        )

    TELA.blit(
        imagem,
        rect
    )


def quebrar_texto(
    texto,
    fonte,
    largura
):

    palavras = texto.split(" ")

    linhas = []
    linha = ""

    for palavra in palavras:

        teste = (
            linha + " " + palavra
        ).strip()

        if fonte.size(teste)[0] <= largura:

            linha = teste

        else:

            if linha:
                linhas.append(linha)

            linha = palavra

    if linha:
        linhas.append(linha)

    return linhas


def desenhar_botao(
    texto,
    rect,
    cor=PAINEL_2
):

    pygame.draw.rect(
        TELA,
        cor,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        TELA,
        CINZA_ESCURO,
        rect,
        1,
        border_radius=10
    )

    desenhar_texto(
        texto,
        FONTE_NORMAL,
        BRANCO,
        rect.centerx,
        rect.centery,
        True
    )


# ============================================================
# MENU LATERAL
# ============================================================

def desenhar_menu():

    pygame.draw.rect(
        TELA,
        PAINEL,
        (0, 0, 220, ALTURA)
    )

    desenhar_texto(
        "ASSISTENTE",
        FONTE_TITULO,
        AZUL,
        25,
        30
    )

    itens = [
        ("Início", "inicio"),
        ("Assistente", "chat"),
        ("Tarefas", "tarefas"),
        ("Relógio", "relogio"),
        ("Configurações", "config")
    ]

    y = 110

    for nome, identificador in itens:

        rect = pygame.Rect(
            15,
            y,
            190,
            48
        )

        if tela_atual == identificador:

            pygame.draw.rect(
                TELA,
                AZUL_ESCURO,
                rect,
                border_radius=10
            )

        desenhar_texto(
            nome,
            FONTE_NORMAL,
            BRANCO,
            35,
            y + 14
        )

        y += 60


# ============================================================
# CABEÇALHO
# ============================================================

def desenhar_cabecalho(titulo):

    desenhar_texto(
        titulo,
        FONTE_GRANDE,
        BRANCO,
        250,
        30
    )

    agora = datetime.datetime.now()

    desenhar_texto(
        agora.strftime("%H:%M"),
        FONTE_NORMAL,
        CINZA,
        1010,
        45
    )


# ============================================================
# INÍCIO
# ============================================================

def tela_inicio():

    desenhar_cabecalho(
        "Início"
    )

    desenhar_texto(
        "Olá! 👋",
        FONTE_GRANDE,
        BRANCO,
        250,
        120
    )

    desenhar_texto(
        "Sua assistente virtual pessoal.",
        FONTE_NORMAL,
        CINZA,
        250,
        175
    )

    cards = [
        (
            "Conversas",
            len(chat_mensagens),
            AZUL
        ),
        (
            "Tarefas",
            len(tarefas),
            VERDE
        ),
        (
            "Status",
            "Online" if cliente else "Sem API",
            AMARELO
        )
    ]

    x = 250

    for titulo, valor, cor in cards:

        rect = pygame.Rect(
            x,
            250,
            220,
            130
        )

        pygame.draw.rect(
            TELA,
            PAINEL,
            rect,
            border_radius=15
        )

        pygame.draw.rect(
            TELA,
            cor,
            (
                x,
                250,
                220,
                6
            ),
            border_radius=5
        )

        desenhar_texto(
            titulo,
            FONTE_NORMAL,
            CINZA,
            x + 20,
            275
        )

        desenhar_texto(
            valor,
            FONTE_MEDIA,
            BRANCO,
            x + 20,
            320
        )

        x += 245

    if cliente:

        texto_status = (
            "A IA está configurada e pronta."
        )

        cor_status = VERDE

    else:

        texto_status = (
            "Configure OPENAI_API_KEY para ativar a IA."
        )

        cor_status = VERMELHO

    desenhar_texto(
        texto_status,
        FONTE_NORMAL,
        cor_status,
        250,
        440
    )


# ============================================================
# CHAT
# ============================================================

def enviar_para_ia(pergunta):

    global resposta_carregando
    global erro_api
    global historico_api

    resposta_carregando = True
    erro_api = ""

    try:

        if cliente is None:

            raise Exception(
                "OPENAI_API_KEY não configurada."
            )

        historico_api.append(
            {
                "role": "user",
                "content": pergunta
            }
        )

        resposta = cliente.responses.create(

            model=MODELO,

            instructions=(
                "Você é uma assistente virtual amigável, "
                "educada e útil. "
                "Responda em português do Brasil por padrão. "
                "Explique assuntos de forma clara. "
                "Quando a pergunta for complexa, organize "
                "a resposta em etapas. "
                "Não invente informações quando não tiver "
                "certeza. "
                "O usuário é adolescente, então mantenha "
                "as respostas apropriadas para a idade."
            ),

            input=historico_api
        )

        texto_resposta = resposta.output_text

        historico_api.append(
            {
                "role": "assistant",
                "content": texto_resposta
            }
        )

        chat_mensagens.append(
            {
                "role": "assistant",
                "content": texto_resposta
            }
        )

    except Exception as erro:

        erro_api = str(erro)

        chat_mensagens.append(
            {
                "role": "assistant",
                "content": (
                    "Não consegui acessar a IA agora.\n\n"
                    f"Erro: {erro_api}"
                )
            }
        )

    resposta_carregando = False


def mandar_mensagem():

    global mensagem_usuario

    texto = mensagem_usuario.strip()

    if not texto:
        return

    if resposta_carregando:
        return

    chat_mensagens.append(
        {
            "role": "user",
            "content": texto
        }
    )

    mensagem_usuario = ""

    thread = threading.Thread(
        target=enviar_para_ia,
        args=(texto,),
        daemon=True
    )

    thread.start()


def tela_chat():

    desenhar_cabecalho(
        "Assistente"
    )

    # área do chat

    chat_area = pygame.Rect(
        250,
        95,
        800,
        480
    )

    pygame.draw.rect(
        TELA,
        (13, 15, 22),
        chat_area,
        border_radius=15
    )

    # mostra últimas mensagens

    mensagens = chat_mensagens[-8:]

    y = 115

    for mensagem in mensagens:

        texto = mensagem["content"]

        eh_usuario = (
            mensagem["role"] == "user"
        )

        if eh_usuario:

            cor = AZUL
            x = 500
            largura = 500

        else:

            cor = PAINEL_2
            x = 275
            largura = 650

        linhas = []

        for paragrafo in texto.split("\n"):

            if paragrafo.strip():

                linhas.extend(
                    quebrar_texto(
                        paragrafo,
                        FONTE_PEQUENA,
                        largura - 30
                    )
                )

            else:

                linhas.append("")

        altura = max(
            45,
            len(linhas) * 21 + 20
        )

        if y + altura > 565:
            break

        rect = pygame.Rect(
            x,
            y,
            largura,
            altura
        )

        pygame.draw.rect(
            TELA,
            cor,
            rect,
            border_radius=12
        )

        texto_y = y + 10

        for linha in linhas:

            desenhar_texto(
                linha,
                FONTE_PEQUENA,
                BRANCO,
                x + 15,
                texto_y
            )

            texto_y += 21

        y += altura + 10

    if resposta_carregando:

        desenhar_texto(
            "Assistente está pensando...",
            FONTE_PEQUENA,
            AMARELO,
            275,
            550
        )

    # campo

    campo = pygame.Rect(
        250,
        595,
        680,
        50
    )

    pygame.draw.rect(
        TELA,
        PAINEL,
        campo,
        border_radius=10
    )

    pygame.draw.rect(
        TELA,
        AZUL,
        campo,
        1,
        border_radius=10
    )

    texto_digitado = mensagem_usuario

    if not texto_digitado:

        texto_digitado = (
            "Digite sua pergunta..."
        )

        cor = CINZA

    else:

        cor = BRANCO

    desenhar_texto(
        texto_digitado,
        FONTE_NORMAL,
        cor,
        265,
        610
    )

    enviar = pygame.Rect(
        945,
        595,
        105,
        50
    )

    desenhar_botao(
        "Enviar",
        enviar,
        AZUL
    )

    desenhar_texto(
        "ENTER = enviar",
        FONTE_PEQUENA,
        CINZA,
        250,
        660
    )


# ============================================================
# TAREFAS
# ============================================================

def tela_tarefas():

    desenhar_cabecalho(
        "Tarefas"
    )

    desenhar_texto(
        "Suas tarefas",
        FONTE_TITULO,
        BRANCO,
        250,
        100
    )

    y = 160

    for i, tarefa in enumerate(tarefas):

        rect = pygame.Rect(
            250,
            y,
            700,
            55
        )

        pygame.draw.rect(
            TELA,
            PAINEL,
            rect,
            border_radius=10
        )

        desenhar_texto(
            f"{i + 1}. {tarefa}",
            FONTE_NORMAL,
            BRANCO,
            275,
            y + 17
        )

        y += 70

    if not tarefas:

        desenhar_texto(
            "Nenhuma tarefa cadastrada.",
            FONTE_NORMAL,
            CINZA,
            250,
            160
        )

    adicionar = pygame.Rect(
        250,
        570,
        180,
        45
    )

    limpar = pygame.Rect(
        450,
        570,
        180,
        45
    )

    desenhar_botao(
        "Adicionar",
        adicionar,
        VERDE
    )

    desenhar_botao(
        "Limpar tudo",
        limpar,
        VERMELHO
    )

    desenhar_texto(
        "Use o botão Adicionar para criar uma tarefa.",
        FONTE_PEQUENA,
        CINZA,
        250,
        635
    )


# ============================================================
# RELÓGIO
# ============================================================

def tela_relogio():

    desenhar_cabecalho(
        "Relógio"
    )

    agora = datetime.datetime.now()

    hora = agora.strftime(
        "%H:%M:%S"
    )

    data = agora.strftime(
        "%d/%m/%Y"
    )

    desenhar_texto(
        hora,
        pygame.font.SysFont(
            "arial",
            80,
            bold=True
        ),
        AZUL,
        650,
        260,
        True
    )

    desenhar_texto(
        data,
        FONTE_TITULO,
        BRANCO,
        650,
        350,
        True
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

def tela_config():

    desenhar_cabecalho(
        "Configurações"
    )

    desenhar_texto(
        "Configuração da IA",
        FONTE_TITULO,
        BRANCO,
        250,
        110
    )

    if cliente:

        desenhar_texto(
            "● API configurada",
            FONTE_NORMAL,
            VERDE,
            250,
            165
        )

    else:

        desenhar_texto(
            "● API não configurada",
            FONTE_NORMAL,
            VERMELHO,
            250,
            165
        )

    desenhar_texto(
        f"Modelo: {MODELO}",
        FONTE_NORMAL,
        CINZA,
        250,
        215
    )

    desenhar_texto(
        "A chave da API é lida pela variável",
        FONTE_NORMAL,
        CINZA,
        250,
        270
    )

    desenhar_texto(
        "OPENAI_API_KEY.",
        FONTE_NORMAL,
        AMARELO,
        250,
        300
    )

    desenhar_texto(
        "Ela não fica armazenada neste programa.",
        FONTE_NORMAL,
        CINZA,
        250,
        345
    )


# ============================================================
# ADICIONAR TAREFA
# ============================================================

def adicionar_tarefa():

    global mensagem_usuario

    tarefa = mensagem_usuario.strip()

    if tarefa:

        tarefas.append(
            tarefa
        )

        mensagem_usuario = ""


# ============================================================
# EVENTOS
# ============================================================

def processar_eventos():

    global tela_atual
    global mensagem_usuario

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # ====================================================
        # TECLADO
        # ====================================================

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                if tela_atual != "inicio":

                    tela_atual = "inicio"

                else:

                    pygame.quit()
                    sys.exit()

            # CHAT

            elif tela_atual == "chat":

                if evento.key == pygame.K_RETURN:

                    mandar_mensagem()

                elif evento.key == pygame.K_BACKSPACE:

                    mensagem_usuario = (
                        mensagem_usuario[:-1]
                    )

                else:

                    if evento.unicode.isprintable():

                        if len(mensagem_usuario) < 500:

                            mensagem_usuario += (
                                evento.unicode
                            )

        # ====================================================
        # MOUSE
        # ====================================================

        if evento.type == pygame.MOUSEBUTTONDOWN:

            mouse = evento.pos

            # -----------------------------------------------
            # MENU
            # -----------------------------------------------

            if mouse[0] <= 220:

                if 110 <= mouse[1] < 158:

                    tela_atual = "inicio"

                elif 170 <= mouse[1] < 218:

                    tela_atual = "chat"

                elif 230 <= mouse[1] < 278:

                    tela_atual = "tarefas"

                elif 290 <= mouse[1] < 338:

                    tela_atual = "relogio"

                elif 350 <= mouse[1] < 398:

                    tela_atual = "config"

                continue

            # -----------------------------------------------
            # CHAT
            # -----------------------------------------------

            if tela_atual == "chat":

                enviar = pygame.Rect(
                    945,
                    595,
                    105,
                    50
                )

                campo = pygame.Rect(
                    250,
                    595,
                    680,
                    50
                )

                if enviar.collidepoint(mouse):

                    mandar_mensagem()

                elif campo.collidepoint(mouse):

                    pass

            # -----------------------------------------------
            # TAREFAS
            # -----------------------------------------------

            elif tela_atual == "tarefas":

                adicionar = pygame.Rect(
                    250,
                    570,
                    180,
                    45
                )

                limpar = pygame.Rect(
                    450,
                    570,
                    180,
                    45
                )

                if adicionar.collidepoint(mouse):

                    # Usamos uma caixa simples pelo teclado.
                    mensagem_usuario = ""

                    # Como não existe outro campo,
                    # a próxima entrada pelo teclado
                    # será usada para a tarefa.
                    tela_atual = "chat"

                elif limpar.collidepoint(mouse):

                    tarefas.clear()


# ============================================================
# LOOP PRINCIPAL
# ============================================================

rodando = True

while rodando:

    RELOGIO.tick(FPS)

    processar_eventos()

    TELA.fill(
        FUNDO
    )

    desenhar_menu()

    if tela_atual == "inicio":

        tela_inicio()

    elif tela_atual == "chat":

        tela_chat()

    elif tela_atual == "tarefas":

        tela_tarefas()

    elif tela_atual == "relogio":

        tela_relogio()

    elif tela_atual == "config":

        tela_config()

    pygame.display.flip()


pygame.quit()
sys.exit()
