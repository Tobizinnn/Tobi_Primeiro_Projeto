import pygame
import random
import sys
import datetime

pygame.init()

# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 1100
ALTURA = 700
FPS = 60

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Game Hub")

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
VERDE_ESCURO = (40, 140, 90)

VERMELHO = (220, 80, 90)
VERMELHO_ESCURO = (160, 50, 60)

AMARELO = (240, 200, 80)
ROXO = (160, 100, 240)
LARANJA = (240, 140, 60)
CIANO = (70, 200, 220)

# ============================================================
# FONTES
# ============================================================

FONTE_GRANDE = pygame.font.SysFont("arial", 38, bold=True)
FONTE_TITULO = pygame.font.SysFont("arial", 28, bold=True)
FONTE_MEDIA = pygame.font.SysFont("arial", 22, bold=True)
FONTE_NORMAL = pygame.font.SysFont("arial", 18)
FONTE_PEQUENA = pygame.font.SysFont("arial", 15)

# ============================================================
# ESTADO DO SISTEMA
# ============================================================

tela_atual = "inicio"
jogo_atual = None

favoritos = []

recordes = {
    "Snake": 0,
    "Pong": 0,
    "Jogo da Velha": 0,
    "Breakout": 0,
    "Space Shooter": 0,
    "Corrida": 0,
    "Dino Runner": 0,
    "Quiz": 0
}

jogos = [
    {
        "nome": "Snake",
        "descricao": "Controle a cobrinha",
        "cor": VERDE
    },
    {
        "nome": "Pong",
        "descricao": "Derrote o computador",
        "cor": AZUL
    },
    {
        "nome": "Jogo da Velha",
        "descricao": "X contra O",
        "cor": AMARELO
    },
    {
        "nome": "Breakout",
        "descricao": "Destrua os blocos",
        "cor": ROXO
    },
    {
        "nome": "Space Shooter",
        "descricao": "Defenda o espaço",
        "cor": CIANO
    },
    {
        "nome": "Corrida",
        "descricao": "Desvie dos carros",
        "cor": LARANJA
    },
    {
        "nome": "Dino Runner",
        "descricao": "Corra e pule",
        "cor": VERDE
    },
    {
        "nome": "Quiz",
        "descricao": "Teste seus conhecimentos",
        "cor": AMARELO
    }
]

# ============================================================
# FUNÇÕES GERAIS
# ============================================================

def desenhar_texto(texto, fonte, cor, x, y, centralizado=False):
    imagem = fonte.render(str(texto), True, cor)

    if centralizado:
        rect = imagem.get_rect(center=(x, y))
    else:
        rect = imagem.get_rect(topleft=(x, y))

    TELA.blit(imagem, rect)


def desenhar_botao(texto, rect, cor=PAINEL_2, cor_texto=BRANCO):
    pygame.draw.rect(TELA, cor, rect, border_radius=10)
    pygame.draw.rect(TELA, CINZA_ESCURO, rect, 1, border_radius=10)

    desenhar_texto(
        texto,
        FONTE_NORMAL,
        cor_texto,
        rect.centerx,
        rect.centery,
        True
    )


def mouse_sobre(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


def atualizar_recorde(nome, pontos):
    if pontos > recordes[nome]:
        recordes[nome] = pontos


def adicionar_favorito(nome):
    if nome in favoritos:
        favoritos.remove(nome)
    else:
        favoritos.append(nome)


# ============================================================
# MENU LATERAL
# ============================================================

def desenhar_menu():
    pygame.draw.rect(TELA, PAINEL, (0, 0, 220, ALTURA))

    desenhar_texto(
        "GAME HUB",
        FONTE_TITULO,
        AZUL,
        25,
        30
    )

    itens = [
        ("Início", "inicio"),
        ("Jogos", "jogos"),
        ("Ranking", "ranking"),
        ("Favoritos", "favoritos")
    ]

    y = 110

    for nome, identificador in itens:

        rect = pygame.Rect(15, y, 190, 48)

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

    hora = agora.strftime("%H:%M")

    desenhar_texto(
        hora,
        FONTE_NORMAL,
        CINZA,
        1010,
        45
    )


# ============================================================
# TELA INICIAL
# ============================================================

def tela_inicio():
    desenhar_cabecalho("Início")

    desenhar_texto(
        "Bem-vindo ao Game Hub!",
        FONTE_GRANDE,
        BRANCO,
        250,
        120
    )

    desenhar_texto(
        "Uma plataforma com vários jogos em um único programa.",
        FONTE_NORMAL,
        CINZA,
        250,
        175
    )

    total_jogos = len(jogos)
    total_favoritos = len(favoritos)

    cards = [
        ("Jogos", total_jogos, AZUL),
        ("Favoritos", total_favoritos, AMARELO),
        ("Recordes", sum(1 for x in recordes.values() if x > 0), VERDE)
    ]

    x = 250

    for titulo, valor, cor in cards:

        rect = pygame.Rect(x, 240, 220, 130)

        pygame.draw.rect(
            TELA,
            PAINEL,
            rect,
            border_radius=15
        )

        pygame.draw.rect(
            TELA,
            cor,
            (x, 240, 220, 6),
            border_radius=5
        )

        desenhar_texto(
            titulo,
            FONTE_NORMAL,
            CINZA,
            x + 20,
            270
        )

        desenhar_texto(
            valor,
            FONTE_GRANDE,
            BRANCO,
            x + 20,
            305
        )

        x += 245

    desenhar_texto(
        "Use o menu lateral para escolher um jogo.",
        FONTE_NORMAL,
        CINZA,
        250,
        430
    )


# ============================================================
# TELA DE JOGOS
# ============================================================

def tela_jogos():
    desenhar_cabecalho("Jogos")

    x = 250
    y = 100

    largura = 250
    altura = 150

    for i, jogo in enumerate(jogos):

        coluna = i % 3
        linha = i // 3

        x = 250 + coluna * 270
        y = 100 + linha * 180

        rect = pygame.Rect(x, y, largura, altura)

        pygame.draw.rect(
            TELA,
            PAINEL,
            rect,
            border_radius=15
        )

        pygame.draw.rect(
            TELA,
            jogo["cor"],
            (x, y, largura, 6),
            border_radius=5
        )

        desenhar_texto(
            jogo["nome"],
            FONTE_MEDIA,
            BRANCO,
            x + 18,
            y + 20
        )

        desenhar_texto(
            jogo["descricao"],
            FONTE_PEQUENA,
            CINZA,
            x + 18,
            y + 55
        )

        estrela = "★" if jogo["nome"] in favoritos else "☆"

        desenhar_texto(
            estrela,
            FONTE_MEDIA,
            AMARELO,
            x + 215,
            y + 18
        )

        jogar = pygame.Rect(
            x + 18,
            y + 95,
            100,
            35
        )

        desenhar_botao(
            "Jogar",
            jogar,
            jogo["cor"]
        )


# ============================================================
# RANKING
# ============================================================

def tela_ranking():
    desenhar_cabecalho("Ranking")

    ordenados = sorted(
        recordes.items(),
        key=lambda item: item[1],
        reverse=True
    )

    y = 100

    for posicao, (nome, pontos) in enumerate(ordenados, start=1):

        rect = pygame.Rect(
            250,
            y,
            650,
            55
        )

        pygame.draw.rect(
            TELA,
            PAINEL,
            rect,
            border_radius=10
        )

        desenhar_texto(
            f"#{posicao}",
            FONTE_MEDIA,
            AMARELO if posicao <= 3 else CINZA,
            275,
            y + 15
        )

        desenhar_texto(
            nome,
            FONTE_NORMAL,
            BRANCO,
            350,
            y + 17
        )

        desenhar_texto(
            pontos,
            FONTE_NORMAL,
            VERDE,
            820,
            y + 17
        )

        y += 65


# ============================================================
# FAVORITOS
# ============================================================

def tela_favoritos():
    desenhar_cabecalho("Favoritos")

    if not favoritos:
        desenhar_texto(
            "Você ainda não possui favoritos.",
            FONTE_NORMAL,
            CINZA,
            250,
            130
        )
        return

    y = 120

    for nome in favoritos:

        jogo = next(
            (j for j in jogos if j["nome"] == nome),
            None
        )

        if jogo is None:
            continue

        rect = pygame.Rect(
            250,
            y,
            650,
            70
        )

        pygame.draw.rect(
            TELA,
            PAINEL,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            TELA,
            jogo["cor"],
            (250, y, 6, 70),
            border_radius=3
        )

        desenhar_texto(
            nome,
            FONTE_MEDIA,
            BRANCO,
            275,
            y + 20
        )

        jogar = pygame.Rect(
            760,
            y + 17,
            110,
            36
        )

        desenhar_botao(
            "Jogar",
            jogar,
            jogo["cor"]
        )

        y += 85


# ============================================================
# VARIÁVEIS DOS JOGOS
# ============================================================

# ---------------- SNAKE ----------------

snake = []
snake_direcao = (1, 0)
snake_comida = (0, 0)
snake_timer = 0
snake_velocidade = 8
snake_pontos = 0
snake_game_over = False

# ---------------- PONG ----------------

pong_player_y = 300
pong_cpu_y = 300
pong_ball_x = 550
pong_ball_y = 350
pong_ball_dx = 5
pong_ball_dy = 4
pong_pontos = 0
pong_cpu_pontos = 0
pong_game_over = False

# ---------------- VELHA ----------------

velha_tabuleiro = [""] * 9
velha_turno = "X"
velha_game_over = False
velha_resultado = ""
velha_pontos = 0

# ---------------- BREAKOUT ----------------

breakout_bola_x = 550
breakout_bola_y = 500
breakout_dx = 5
breakout_dy = -5
breakout_player_x = 500
breakout_blocos = []
breakout_vidas = 3
breakout_pontos = 0
breakout_game_over = False

# ---------------- SHOOTER ----------------

shooter_player_x = 550
shooter_player_y = 620
shooter_tiros = []
shooter_inimigos = []
shooter_timer = 0
shooter_pontos = 0
shooter_vidas = 3
shooter_game_over = False

# ---------------- CORRIDA ----------------

corrida_player_x = 550
corrida_inimigos = []
corrida_timer = 0
corrida_pontos = 0
corrida_velocidade = 5
corrida_game_over = False

# ---------------- DINO ----------------

dino_x = 300
dino_y = 560
dino_vel_y = 0
dino_no_chao = True
dino_obstaculos = []
dino_timer = 0
dino_pontos = 0
dino_velocidade = 7
dino_game_over = False

# ---------------- QUIZ ----------------

quiz_perguntas = [
    {
        "pergunta": "Qual é a capital do Brasil?",
        "opcoes": ["Brasília", "São Paulo", "Rio de Janeiro", "Salvador"],
        "resposta": 0
    },
    {
        "pergunta": "Quanto é 8 x 7?",
        "opcoes": ["54", "56", "64", "48"],
        "resposta": 1
    },
    {
        "pergunta": "Qual planeta é conhecido como planeta vermelho?",
        "opcoes": ["Vênus", "Júpiter", "Marte", "Saturno"],
        "resposta": 2
    },
    {
        "pergunta": "Qual linguagem estamos usando?",
        "opcoes": ["Python", "Java", "HTML", "C++"],
        "resposta": 0
    },
    {
        "pergunta": "Quantos lados tem um hexágono?",
        "opcoes": ["5", "6", "7", "8"],
        "resposta": 1
    },
    {
        "pergunta": "Qual destes é um mamífero?",
        "opcoes": ["Tubarão", "Golfinho", "Pinguim", "Crocodilo"],
        "resposta": 1
    },
    {
        "pergunta": "Quanto é 12 + 15?",
        "opcoes": ["25", "26", "27", "28"],
        "resposta": 2
    }
]

quiz_index = 0
quiz_pontos = 0
quiz_game_over = False

# ============================================================
# SNAKE
# ============================================================

def iniciar_snake():
    global snake, snake_direcao, snake_comida
    global snake_pontos, snake_game_over, snake_timer

    snake = [
        (10, 10),
        (9, 10),
        (8, 10)
    ]

    snake_direcao = (1, 0)

    snake_comida = (
        random.randint(0, 24),
        random.randint(0, 19)
    )

    snake_pontos = 0
    snake_game_over = False
    snake_timer = 0


def atualizar_snake():
    global snake, snake_comida
    global snake_pontos, snake_game_over
    global snake_timer, snake_velocidade

    if snake_game_over:
        return

    snake_timer += 1

    if snake_timer < max(3, 11 - snake_pontos // 50):
        return

    snake_timer = 0

    cabeca_x, cabeca_y = snake[0]
    dx, dy = snake_direcao

    nova_cabeca = (
        cabeca_x + dx,
        cabeca_y + dy
    )

    if (
        nova_cabeca[0] < 0
        or nova_cabeca[0] >= 25
        or nova_cabeca[1] < 0
        or nova_cabeca[1] >= 20
        or nova_cabeca in snake
    ):
        snake_game_over = True
        atualizar_recorde("Snake", snake_pontos)
        return

    snake.insert(0, nova_cabeca)

    if nova_cabeca == snake_comida:

        snake_pontos += 10

        while True:
            nova_comida = (
                random.randint(0, 24),
                random.randint(0, 19)
            )

            if nova_comida not in snake:
                snake_comida = nova_comida
                break

    else:
        snake.pop()


def desenhar_snake():
    desenhar_cabecalho("Snake")

    area = pygame.Rect(300, 100, 750, 550)

    pygame.draw.rect(
        TELA,
        (10, 12, 18),
        area,
        border_radius=10
    )

    tamanho = 30

    for i, parte in enumerate(snake):

        x = 300 + parte[0] * tamanho
        y = 100 + parte[1] * tamanho

        cor = VERDE if i == 0 else VERDE_ESCURO

        pygame.draw.rect(
            TELA,
            cor,
            (x + 2, y + 2, 26, 26),
            border_radius=6
        )

    fx = 300 + snake_comida[0] * tamanho
    fy = 100 + snake_comida[1] * tamanho

    pygame.draw.circle(
        TELA,
        VERMELHO,
        (fx + 15, fy + 15),
        10
    )

    desenhar_texto(
        f"Pontos: {snake_pontos}",
        FONTE_NORMAL,
        BRANCO,
        300,
        665
    )

    desenhar_texto(
        "Setas = mover | ESC = voltar",
        FONTE_PEQUENA,
        CINZA,
        700,
        670
    )

    if snake_game_over:
        desenhar_game_over("Snake", snake_pontos)


# ============================================================
# PONG
# ============================================================

def iniciar_pong():
    global pong_player_y, pong_cpu_y
    global pong_ball_x, pong_ball_y
    global pong_ball_dx, pong_ball_dy
    global pong_pontos, pong_cpu_pontos
    global pong_game_over

    pong_player_y = 300
    pong_cpu_y = 300

    pong_ball_x = 550
    pong_ball_y = 350

    pong_ball_dx = random.choice([-5, 5])
    pong_ball_dy = random.choice([-4, 4])

    pong_pontos = 0
    pong_cpu_pontos = 0

    pong_game_over = False


def atualizar_pong():
    global pong_player_y, pong_cpu_y
    global pong_ball_x, pong_ball_y
    global pong_ball_dx, pong_ball_dy
    global pong_pontos, pong_cpu_pontos
    global pong_game_over

    if pong_game_over:
        return

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w]:
        pong_player_y -= 7

    if teclas[pygame.K_s]:
        pong_player_y += 7

    pong_player_y = max(100, min(570, pong_player_y))

    if pong_cpu_y + 45 < pong_ball_y:
        pong_cpu_y += 5

    elif pong_cpu_y + 45 > pong_ball_y:
        pong_cpu_y -= 5

    pong_cpu_y = max(100, min(570, pong_cpu_y))

    pong_ball_x += pong_ball_dx
    pong_ball_y += pong_ball_dy

    if pong_ball_y <= 100 or pong_ball_y >= 640:
        pong_ball_dy *= -1

    player_rect = pygame.Rect(
        280,
        pong_player_y,
        15,
        90
    )

    cpu_rect = pygame.Rect(
        1020,
        pong_cpu_y,
        15,
        90
    )

    ball_rect = pygame.Rect(
        pong_ball_x - 10,
        pong_ball_y - 10,
        20,
        20
    )

    if ball_rect.colliderect(player_rect) and pong_ball_dx < 0:
        pong_ball_dx *= -1

    if ball_rect.colliderect(cpu_rect) and pong_ball_dx > 0:
        pong_ball_dx *= -1

    if pong_ball_x < 240:
        pong_cpu_pontos += 1
        pong_ball_x = 550
        pong_ball_y = 350
        pong_ball_dx = 5

    if pong_ball_x > 1060:
        pong_pontos += 1
        pong_ball_x = 550
        pong_ball_y = 350
        pong_ball_dx = -5

    if pong_pontos >= 5 or pong_cpu_pontos >= 5:
        pong_game_over = True
        atualizar_recorde("Pong", pong_pontos * 10)


def desenhar_pong():
    desenhar_cabecalho("Pong")

    pygame.draw.rect(
        TELA,
        (10, 12, 18),
        (250, 100, 800, 550),
        border_radius=10
    )

    pygame.draw.line(
        TELA,
        CINZA_ESCURO,
        (650, 100),
        (650, 650),
        2
    )

    pygame.draw.rect(
        TELA,
        AZUL,
        (280, pong_player_y, 15, 90),
        border_radius=5
    )

    pygame.draw.rect(
        TELA,
        VERMELHO,
        (1020, pong_cpu_y, 15, 90),
        border_radius=5
    )

    pygame.draw.circle(
        TELA,
        BRANCO,
        (pong_ball_x, pong_ball_y),
        10
    )

    desenhar_texto(
        f"{pong_pontos}   x   {pong_cpu_pontos}",
        FONTE_GRANDE,
        BRANCO,
        650,
        125,
        True
    )

    desenhar_texto(
        "W/S = mover | ESC = voltar",
        FONTE_PEQUENA,
        CINZA,
        250,
        665
    )

    if pong_game_over:
        desenhar_game_over(
            "Pong",
            pong_pontos * 10
        )


# ============================================================
# JOGO DA VELHA
# ============================================================

def iniciar_velha():
    global velha_tabuleiro
    global velha_turno
    global velha_game_over
    global velha_resultado
    global velha_pontos

    velha_tabuleiro = [""] * 9
    velha_turno = "X"
    velha_game_over = False
    velha_resultado = ""
    velha_pontos = 0


def verificar_vencedor(tab):
    combinacoes = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in combinacoes:

        if (
            tab[a]
            and tab[a] == tab[b]
            and tab[a] == tab[c]
        ):
            return tab[a]

    if "" not in tab:
        return "EMPATE"

    return None


def jogada_cpu_velha():
    global velha_tabuleiro

    vazios = [
        i for i, valor in enumerate(velha_tabuleiro)
        if valor == ""
    ]

    if not vazios:
        return

    # Tenta vencer
    for pos in vazios:

        teste = velha_tabuleiro.copy()
        teste[pos] = "O"

        if verificar_vencedor(teste) == "O":
            velha_tabuleiro[pos] = "O"
            return

    # Tenta bloquear
    for pos in vazios:

        teste = velha_tabuleiro.copy()
        teste[pos] = "X"

        if verificar_vencedor(teste) == "X":
            velha_tabuleiro[pos] = "O"
            return

    # Centro
    if 4 in vazios and random.random() < 0.6:
        velha_tabuleiro[4] = "O"
        return

    velha_tabuleiro[random.choice(vazios)] = "O"


def desenhar_velha():
    desenhar_cabecalho("Jogo da Velha")

    inicio_x = 430
    inicio_y = 140
    tamanho = 100

    for i in range(10):
        if i <= 3:
            pass

    for linha in range(4):
        pygame.draw.line(
            TELA,
            CINZA,
            (inicio_x, inicio_y + linha * tamanho),
            (inicio_x + 300, inicio_y + linha * tamanho),
            3
        )

        pygame.draw.line(
            TELA,
            CINZA,
            (inicio_x + linha * tamanho, inicio_y),
            (inicio_x + linha * tamanho, inicio_y + 300),
            3
        )

    for i, valor in enumerate(velha_tabuleiro):

        if valor == "":
            continue

        linha = i // 3
        coluna = i % 3

        cx = inicio_x + coluna * tamanho + 50
        cy = inicio_y + linha * tamanho + 50

        desenhar_texto(
            valor,
            FONTE_GRANDE,
            AZUL if valor == "X" else VERMELHO,
            cx,
            cy,
            True
        )

    desenhar_texto(
        "Clique para jogar",
        FONTE_NORMAL,
        CINZA,
        430,
        475
    )

    if velha_game_over:

        desenhar_texto(
            velha_resultado,
            FONTE_MEDIA,
            AMARELO,
            580,
            530,
            True
        )

        desenhar_texto(
            "ENTER = jogar novamente | ESC = voltar",
            FONTE_PEQUENA,
            CINZA,
            580,
            565,
            True
        )


# ============================================================
# BREAKOUT
# ============================================================

def iniciar_breakout():
    global breakout_bola_x, breakout_bola_y
    global breakout_dx, breakout_dy
    global breakout_player_x
    global breakout_blocos
    global breakout_vidas
    global breakout_pontos
    global breakout_game_over

    breakout_bola_x = 550
    breakout_bola_y = 500

    breakout_dx = random.choice([-5, 5])
    breakout_dy = -5

    breakout_player_x = 500

    breakout_blocos = []

    for linha in range(5):

        for coluna in range(10):

            rect = pygame.Rect(
                270 + coluna * 75,
                120 + linha * 35,
                65,
                25
            )

            breakout_blocos.append(rect)

    breakout_vidas = 3
    breakout_pontos = 0
    breakout_game_over = False


def atualizar_breakout():
    global breakout_bola_x, breakout_bola_y
    global breakout_dx, breakout_dy
    global breakout_player_x
    global breakout_vidas
    global breakout_pontos
    global breakout_game_over

    if breakout_game_over:
        return

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        breakout_player_x -= 8

    if teclas[pygame.K_RIGHT]:
        breakout_player_x += 8

    breakout_player_x = max(
        260,
        min(910, breakout_player_x)
    )

    breakout_bola_x += breakout_dx
    breakout_bola_y += breakout_dy

    if breakout_bola_x <= 260 or breakout_bola_x >= 1040:
        breakout_dx *= -1

    if breakout_bola_y <= 100:
        breakout_dy *= -1

    player = pygame.Rect(
        breakout_player_x,
        620,
        130,
        15
    )

    bola = pygame.Rect(
        breakout_bola_x - 8,
        breakout_bola_y - 8,
        16,
        16
    )

    if bola.colliderect(player) and breakout_dy > 0:
        breakout_dy *= -1

    for bloco in breakout_blocos[:]:

        if bola.colliderect(bloco):

            breakout_blocos.remove(bloco)
            breakout_dy *= -1
            breakout_pontos += 10
            break

    if breakout_bola_y > 670:

        breakout_vidas -= 1

        if breakout_vidas <= 0:

            breakout_game_over = True

            atualizar_recorde(
                "Breakout",
                breakout_pontos
            )

        else:

            breakout_bola_x = 550
            breakout_bola_y = 500
            breakout_dy = -5

    if not breakout_blocos:

        breakout_game_over = True

        atualizar_recorde(
            "Breakout",
            breakout_pontos
        )


def desenhar_breakout():
    desenhar_cabecalho("Breakout")

    pygame.draw.rect(
        TELA,
        (10, 12, 18),
        (250, 100, 800, 550),
        border_radius=10
    )

    for bloco in breakout_blocos:

        pygame.draw.rect(
            TELA,
            ROXO,
            bloco,
            border_radius=5
        )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (
            breakout_player_x,
            620,
            130,
            15
        ),
        border_radius=5
    )

    pygame.draw.circle(
        TELA,
        AMARELO,
        (
            int(breakout_bola_x),
            int(breakout_bola_y)
        ),
        8
    )

    desenhar_texto(
        f"Pontos: {breakout_pontos}",
        FONTE_NORMAL,
        BRANCO,
        260,
        665
    )

    desenhar_texto(
        f"Vidas: {breakout_vidas}",
        FONTE_NORMAL,
        VERMELHO,
        450,
        665
    )

    desenhar_texto(
        "Setas = mover | ESC = voltar",
        FONTE_PEQUENA,
        CINZA,
        750,
        670
    )

    if breakout_game_over:

        mensagem = (
            "VOCÊ VENCEU!"
            if len(breakout_blocos) == 0
            else "GAME OVER"
        )

        desenhar_game_over(
            mensagem,
            breakout_pontos,
            atualizar=False
        )


# ============================================================
# SPACE SHOOTER
# ============================================================

def iniciar_shooter():
    global shooter_player_x, shooter_player_y
    global shooter_tiros, shooter_inimigos
    global shooter_timer
    global shooter_pontos, shooter_vidas
    global shooter_game_over

    shooter_player_x = 550
    shooter_player_y = 620

    shooter_tiros = []
    shooter_inimigos = []

    shooter_timer = 0

    shooter_pontos = 0
    shooter_vidas = 3

    shooter_game_over = False


def atualizar_shooter():
    global shooter_player_x
    global shooter_tiros
    global shooter_inimigos
    global shooter_timer
    global shooter_pontos
    global shooter_vidas
    global shooter_game_over

    if shooter_game_over:
        return

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        shooter_player_x -= 7

    if teclas[pygame.K_RIGHT]:
        shooter_player_x += 7

    shooter_player_x = max(
        260,
        min(1040, shooter_player_x)
    )

    shooter_timer += 1

    if shooter_timer >= max(
        15,
        40 - shooter_pontos // 100
    ):

        shooter_timer = 0

        shooter_inimigos.append([
            random.randint(270, 1020),
            110
        ])

    for tiro in shooter_tiros:
        tiro[1] -= 10

    shooter_tiros = [
        tiro for tiro in shooter_tiros
        if tiro[1] > 90
    ]

    for inimigo in shooter_inimigos:
        inimigo[1] += 3 + shooter_pontos // 300

    player_rect = pygame.Rect(
        shooter_player_x - 20,
        shooter_player_y - 20,
        40,
        40
    )

    for inimigo in shooter_inimigos[:]:

        enemy_rect = pygame.Rect(
            inimigo[0] - 18,
            inimigo[1] - 18,
            36,
            36
        )

        if enemy_rect.colliderect(player_rect):

            shooter_inimigos.remove(inimigo)
            shooter_vidas -= 1

            if shooter_vidas <= 0:

                shooter_game_over = True

                atualizar_recorde(
                    "Space Shooter",
                    shooter_pontos
                )

    for tiro in shooter_tiros[:]:

        tiro_rect = pygame.Rect(
            tiro[0] - 4,
            tiro[1] - 10,
            8,
            20
        )

        for inimigo in shooter_inimigos[:]:

            enemy_rect = pygame.Rect(
                inimigo[0] - 18,
                inimigo[1] - 18,
                36,
                36
            )

            if tiro_rect.colliderect(enemy_rect):

                if tiro in shooter_tiros:
                    shooter_tiros.remove(tiro)

                shooter_inimigos.remove(inimigo)

                shooter_pontos += 10

                break

    for inimigo in shooter_inimigos[:]:

        if inimigo[1] > 680:

            shooter_inimigos.remove(inimigo)
            shooter_vidas -= 1

            if shooter_vidas <= 0:

                shooter_game_over = True

                atualizar_recorde(
                    "Space Shooter",
                    shooter_pontos
                )


def desenhar_shooter():
    desenhar_cabecalho("Space Shooter")

    pygame.draw.rect(
        TELA,
        (5, 8, 18),
        (250, 100, 800, 550),
        border_radius=10
    )

    # estrelas
    random.seed(10)

    for _ in range(70):

        x = random.randint(260, 1040)
        y = random.randint(105, 645)

        pygame.draw.circle(
            TELA,
            CINZA,
            (x, y),
            1
        )

    random.seed()

    # jogador
    pygame.draw.polygon(
        TELA,
        CIANO,
        [
            (shooter_player_x, shooter_player_y - 25),
            (shooter_player_x - 22, shooter_player_y + 20),
            (shooter_player_x + 22, shooter_player_y + 20)
        ]
    )

    # tiros
    for tiro in shooter_tiros:

        pygame.draw.rect(
            TELA,
            AMARELO,
            (
                tiro[0] - 3,
                tiro[1] - 10,
                6,
                20
            )
        )

    # inimigos
    for inimigo in shooter_inimigos:

        pygame.draw.circle(
            TELA,
            VERMELHO,
            (
                int(inimigo[0]),
                int(inimigo[1])
            ),
            18
        )

    desenhar_texto(
        f"Pontos: {shooter_pontos}",
        FONTE_NORMAL,
        BRANCO,
        260,
        665
    )

    desenhar_texto(
        f"Vidas: {shooter_vidas}",
        FONTE_NORMAL,
        VERMELHO,
        450,
        665
    )

    desenhar_texto(
        "Setas + ESPAÇO | ESC = voltar",
        FONTE_PEQUENA,
        CINZA,
        720,
        670
    )

    if shooter_game_over:
        desenhar_game_over(
            "Space Shooter",
            shooter_pontos
        )


# ============================================================
# CORRIDA
# ============================================================

def iniciar_corrida():
    global corrida_player_x
    global corrida_inimigos
    global corrida_timer
    global corrida_pontos
    global corrida_velocidade
    global corrida_game_over

    corrida_player_x = 550

    corrida_inimigos = []

    corrida_timer = 0
    corrida_pontos = 0
    corrida_velocidade = 5

    corrida_game_over = False


def atualizar_corrida():
    global corrida_player_x
    global corrida_inimigos
    global corrida_timer
    global corrida_pontos
    global corrida_velocidade
    global corrida_game_over

    if corrida_game_over:
        return

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        corrida_player_x -= 8

    if teclas[pygame.K_RIGHT]:
        corrida_player_x += 8

    corrida_player_x = max(
        400,
        min(800, corrida_player_x)
    )

    corrida_timer += 1

    corrida_velocidade = 5 + corrida_pontos // 100

    if corrida_timer >= max(
        20,
        60 - corrida_pontos // 40
    ):

        corrida_timer = 0

        faixa = random.choice([
            430,
            530,
            630,
            730
        ])

        corrida_inimigos.append([
            faixa,
            -100
        ])

    player = pygame.Rect(
        corrida_player_x - 25,
        570,
        50,
        80
    )

    for carro in corrida_inimigos[:]:

        carro[1] += corrida_velocidade

        enemy = pygame.Rect(
            carro[0] - 25,
            carro[1],
            50,
            80
        )

        if player.colliderect(enemy):

            corrida_game_over = True

            atualizar_recorde(
                "Corrida",
                corrida_pontos
            )

        if carro[1] > 700:

            corrida_inimigos.remove(carro)

            corrida_pontos += 10


def desenhar_corrida():
    desenhar_cabecalho("Corrida")

    # estrada
    pygame.draw.rect(
        TELA,
        (45, 45, 48),
        (380, 100, 450, 550)
    )

    # bordas
    pygame.draw.rect(
        TELA,
        BRANCO,
        (380, 100, 8, 550)
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (822, 100, 8, 550)
    )

    # linhas
    for y in range(100, 650, 70):

        pygame.draw.rect(
            TELA,
            CINZA,
            (492, y, 8, 35)
        )

        pygame.draw.rect(
            TELA,
            CINZA,
            (604, y, 8, 35)
        )

        pygame.draw.rect(
            TELA,
            CINZA,
            (716, y, 8, 35)
        )

    # jogador
    pygame.draw.rect(
        TELA,
        AZUL,
        (
            corrida_player_x - 25,
            570,
            50,
            80
        ),
        border_radius=8
    )

    # inimigos
    for carro in corrida_inimigos:

        pygame.draw.rect(
            TELA,
            VERMELHO,
            (
                carro[0] - 25,
                carro[1],
                50,
                80
            ),
            border_radius=8
        )

    desenhar_texto(
        f"Pontos: {corrida_pontos}",
        FONTE_NORMAL,
        BRANCO,
        250,
        665
    )

    desenhar_texto(
        f"Velocidade: {corrida_velocidade}",
        FONTE_NORMAL,
        LARANJA,
        450,
        665
    )

    desenhar_texto(
        "Setas = mover | ESC = voltar",
        FONTE_PEQUENA,
        CINZA,
        760,
        670
    )

    if corrida_game_over:
        desenhar_game_over(
            "Corrida",
            corrida_pontos
        )


# ============================================================
# DINO RUNNER
# ============================================================

def iniciar_dino():
    global dino_x, dino_y
    global dino_vel_y, dino_no_chao
    global dino_obstaculos
    global dino_timer
    global dino_pontos
    global dino_velocidade
    global dino_game_over

    dino_x = 300
    dino_y = 560

    dino_vel_y = 0
    dino_no_chao = True

    dino_obstaculos = []

    dino_timer = 0
    dino_pontos = 0
    dino_velocidade = 7

    dino_game_over = False


def atualizar_dino():
    global dino_y, dino_vel_y
    global dino_no_chao
    global dino_obstaculos
    global dino_timer
    global dino_pontos
    global dino_velocidade
    global dino_game_over

    if dino_game_over:
        return

    teclas = pygame.key.get_pressed()

    if (
        (teclas[pygame.K_SPACE] or teclas[pygame.K_UP])
        and dino_no_chao
    ):

        dino_vel_y = -14
        dino_no_chao = False

    dino_vel_y += 0.7
    dino_y += dino_vel_y

    if dino_y >= 560:

        dino_y = 560
        dino_vel_y = 0
        dino_no_chao = True

    dino_timer += 1

    dino_velocidade = 7 + dino_pontos // 100

    if dino_timer >= max(
        35,
        80 - dino_pontos // 30
    ):

        dino_timer = 0

        dino_obstaculos.append([
            1050,
            570
        ])

    player = pygame.Rect(
        dino_x,
        dino_y,
        45,
        60
    )

    for obstaculo in dino_obstaculos[:]:

        obstaculo[0] -= dino_velocidade

        enemy = pygame.Rect(
            obstaculo[0],
            obstaculo[1],
            35,
            50
        )

        if player.colliderect(enemy):

            dino_game_over = True

            atualizar_recorde(
                "Dino Runner",
                dino_pontos
            )

        if obstaculo[0] < -50:

            dino_obstaculos.remove(obstaculo)

            dino_pontos += 10


def desenhar_dino():
    desenhar_cabecalho("Dino Runner")

    pygame.draw.rect(
        TELA,
        (235, 235, 235),
        (250, 100, 800, 550),
        border_radius=10
    )

    # chão
    pygame.draw.rect(
        TELA,
        (60, 60, 60),
        (250, 620, 800, 4)
    )

    # dino
    pygame.draw.rect(
        TELA,
        VERDE_ESCURO,
        (
            dino_x,
            dino_y,
            45,
            60
        ),
        border_radius=6
    )

    pygame.draw.circle(
        TELA,
        BRANCO,
        (
            dino_x + 32,
            dino_y + 15
        ),
        5
    )

    # obstáculos
    for obstaculo in dino_obstaculos:

        pygame.draw.rect(
            TELA,
            VERDE_ESCURO,
            (
                obstaculo[0],
                obstaculo[1],
                35,
                50
            )
        )

    desenhar_texto(
        f"Pontos: {dino_pontos}",
        FONTE_NORMAL,
        (30, 30, 30),
        270,
        130
    )

    desenhar_texto(
        "ESPAÇO / ↑ = pular | ESC = voltar",
        FONTE_PEQUENA,
        (80, 80, 80),
        700,
        665
    )

    if dino_game_over:
        desenhar_game_over(
            "Dino Runner",
            dino_pontos
        )


# ============================================================
# QUIZ
# ============================================================

def iniciar_quiz():
    global quiz_index
    global quiz_pontos
    global quiz_game_over

    quiz_index = 0
    quiz_pontos = 0
    quiz_game_over = False


def desenhar_quiz():
    desenhar_cabecalho("Quiz")

    if quiz_game_over:

        desenhar_texto(
            "QUIZ FINALIZADO!",
            FONTE_GRANDE,
            AMARELO,
            650,
            200,
            True
        )

        desenhar_texto(
            f"Pontuação: {quiz_pontos}",
            FONTE_MEDIA,
            BRANCO,
            650,
            270,
            True
        )

        desenhar_texto(
            "ENTER = jogar novamente",
            FONTE_NORMAL,
            CINZA,
            650,
            330,
            True
        )

        desenhar_texto(
            "ESC = voltar",
            FONTE_NORMAL,
            CINZA,
            650,
            370,
            True
        )

        return

    pergunta = quiz_perguntas[quiz_index]

    pygame.draw.rect(
        TELA,
        PAINEL,
        (280, 120, 740, 150),
        border_radius=15
    )

    desenhar_texto(
        f"Pergunta {quiz_index + 1}/{len(quiz_perguntas)}",
        FONTE_PEQUENA,
        AMARELO,
        310,
        145
    )

    desenhar_texto(
        pergunta["pergunta"],
        FONTE_MEDIA,
        BRANCO,
        310,
        190
    )

    for i, opcao in enumerate(pergunta["opcoes"]):

        rect = pygame.Rect(
            300,
            310 + i * 75,
            680,
            55
        )

        desenhar_botao(
            f"{chr(65 + i)}) {opcao}",
            rect,
            PAINEL_2
        )

    desenhar_texto(
        f"Pontos: {quiz_pontos}",
        FONTE_NORMAL,
        VERDE,
        300,
        625
    )

    desenhar_texto(
        "Clique em uma resposta | ESC = voltar",
        FONTE_PEQUENA,
        CINZA,
        650,
        670
    )


# ============================================================
# GAME OVER
# ============================================================

def desenhar_game_over(nome, pontos, atualizar=True):

    if atualizar:
        atualizar_recorde(nome, pontos)

    overlay = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))

    TELA.blit(
        overlay,
        (0, 0)
    )

    pygame.draw.rect(
        TELA,
        PAINEL,
        (350, 220, 400, 240),
        border_radius=20
    )

    desenhar_texto(
        "GAME OVER",
        FONTE_GRANDE,
        VERMELHO,
        550,
        270,
        True
    )

    desenhar_texto(
        f"Pontos: {pontos}",
        FONTE_MEDIA,
        BRANCO,
        550,
        330,
        True
    )

    desenhar_texto(
        "ENTER = jogar novamente",
        FONTE_NORMAL,
        CINZA,
        550,
        380,
        True
    )

    desenhar_texto(
        "ESC = voltar",
        FONTE_NORMAL,
        CINZA,
        550,
        415,
        True
    )


# ============================================================
# INICIAR JOGO
# ============================================================

def iniciar_jogo(nome):

    global jogo_atual

    jogo_atual = nome

    if nome == "Snake":
        iniciar_snake()

    elif nome == "Pong":
        iniciar_pong()

    elif nome == "Jogo da Velha":
        iniciar_velha()

    elif nome == "Breakout":
        iniciar_breakout()

    elif nome == "Space Shooter":
        iniciar_shooter()

    elif nome == "Corrida":
        iniciar_corrida()

    elif nome == "Dino Runner":
        iniciar_dino()

    elif nome == "Quiz":
        iniciar_quiz()


# ============================================================
# PROCESSAMENTO DOS JOGOS
# ============================================================

def atualizar_jogo():

    if jogo_atual == "Snake":
        atualizar_snake()

    elif jogo_atual == "Pong":
        atualizar_pong()

    elif jogo_atual == "Breakout":
        atualizar_breakout()

    elif jogo_atual == "Space Shooter":
        atualizar_shooter()

    elif jogo_atual == "Corrida":
        atualizar_corrida()

    elif jogo_atual == "Dino Runner":
        atualizar_dino()


def desenhar_jogo():

    if jogo_atual == "Snake":
        desenhar_snake()

    elif jogo_atual == "Pong":
        desenhar_pong()

    elif jogo_atual == "Jogo da Velha":
        desenhar_velha()

    elif jogo_atual == "Breakout":
        desenhar_breakout()

    elif jogo_atual == "Space Shooter":
        desenhar_shooter()

    elif jogo_atual == "Corrida":
        desenhar_corrida()

    elif jogo_atual == "Dino Runner":
        desenhar_dino()

    elif jogo_atual == "Quiz":
        desenhar_quiz()


# ============================================================
# EVENTOS
# ============================================================

def processar_eventos():

    global tela_atual
    global jogo_atual

    global snake_direcao
    global velha_turno
    global velha_game_over
    global velha_resultado
    global velha_pontos

    global quiz_index
    global quiz_pontos
    global quiz_game_over

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ====================================================
        # JOGO ABERTO
        # ====================================================

        if jogo_atual is not None:

            # ESC volta
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    jogo_atual = None
                    tela_atual = "jogos"
                    continue

                # ---------------- SNAKE ----------------

                if jogo_atual == "Snake":

                    if evento.key == pygame.K_UP and snake_direcao != (0, 1):
                        snake_direcao = (0, -1)

                    elif evento.key == pygame.K_DOWN and snake_direcao != (0, -1):
                        snake_direcao = (0, 1)

                    elif evento.key == pygame.K_LEFT and snake_direcao != (1, 0):
                        snake_direcao = (-1, 0)

                    elif evento.key == pygame.K_RIGHT and snake_direcao != (-1, 0):
                        snake_direcao = (1, 0)

                    elif evento.key == pygame.K_RETURN and snake_game_over:
                        iniciar_snake()

                # ---------------- PONG ----------------

                elif jogo_atual == "Pong":

                    if evento.key == pygame.K_RETURN and pong_game_over:
                        iniciar_pong()

                # ---------------- VELHA ----------------

                elif jogo_atual == "Jogo da Velha":

                    if evento.key == pygame.K_RETURN and velha_game_over:
                        iniciar_velha()

                # ---------------- BREAKOUT ----------------

                elif jogo_atual == "Breakout":

                    if evento.key == pygame.K_RETURN and breakout_game_over:
                        iniciar_breakout()

                # ---------------- SHOOTER ----------------

                elif jogo_atual == "Space Shooter":

                    if evento.key == pygame.K_SPACE and not shooter_game_over:

                        shooter_tiros.append([
                            shooter_player_x,
                            shooter_player_y - 30
                        ])

                    elif evento.key == pygame.K_RETURN and shooter_game_over:
                        iniciar_shooter()

                # ---------------- CORRIDA ----------------

                elif jogo_atual == "Corrida":

                    if evento.key == pygame.K_RETURN and corrida_game_over:
                        iniciar_corrida()

                # ---------------- DINO ----------------

                elif jogo_atual == "Dino Runner":

                    if evento.key == pygame.K_RETURN and dino_game_over:
                        iniciar_dino()

                # ---------------- QUIZ ----------------

                elif jogo_atual == "Quiz":

                    if evento.key == pygame.K_RETURN and quiz_game_over:
                        iniciar_quiz()

            # =================================================
            # MOUSE NOS JOGOS
            # =================================================

            if evento.type == pygame.MOUSEBUTTONDOWN:

                # Jogo da velha
                if jogo_atual == "Jogo da Velha":

                    if (
                        not velha_game_over
                        and velha_turno == "X"
                    ):

                        inicio_x = 430
                        inicio_y = 140
                        tamanho = 100

                        mouse_x, mouse_y = evento.pos

                        if (
                            inicio_x <= mouse_x <= inicio_x + 300
                            and inicio_y <= mouse_y <= inicio_y + 300
                        ):

                            coluna = (
                                mouse_x - inicio_x
                            ) // tamanho

                            linha = (
                                mouse_y - inicio_y
                            ) // tamanho

                            posicao = linha * 3 + coluna

                            if velha_tabuleiro[posicao] == "":

                                velha_tabuleiro[posicao] = "X"

                                resultado = verificar_vencedor(
                                    velha_tabuleiro
                                )

                                if resultado:

                                    velha_game_over = True

                                    if resultado == "X":
                                        velha_resultado = "VOCÊ VENCEU!"
                                        velha_pontos = 100
                                    else:
                                        velha_resultado = "EMPATE"
                                        velha_pontos = 20

                                    atualizar_recorde(
                                        "Jogo da Velha",
                                        velha_pontos
                                    )

                                else:

                                    velha_turno = "O"

                                    jogada_cpu_velha()

                                    resultado = verificar_vencedor(
                                        velha_tabuleiro
                                    )

                                    if resultado:

                                        velha_game_over = True

                                        if resultado == "O":
                                            velha_resultado = "COMPUTADOR VENCEU!"
                                            velha_pontos = 0

                                        else:
                                            velha_resultado = "EMPATE"
                                            velha_pontos = 20

                                        atualizar_recorde(
                                            "Jogo da Velha",
                                            velha_pontos
                                        )

                                    velha_turno = "X"

                # Quiz
                elif jogo_atual == "Quiz":

                    if not quiz_game_over:

                        for i in range(4):

                            rect = pygame.Rect(
                                300,
                                310 + i * 75,
                                680,
                                55
                            )

                            if rect.collidepoint(evento.pos):

                                pergunta = quiz_perguntas[
                                    quiz_index
                                ]

                                if i == pergunta["resposta"]:

                                    quiz_pontos += 10

                                quiz_index += 1

                                if (
                                    quiz_index
                                    >= len(quiz_perguntas)
                                ):

                                    quiz_game_over = True

                                    atualizar_recorde(
                                        "Quiz",
                                        quiz_pontos
                                    )

            continue

        # ====================================================
        # MENU PRINCIPAL
        # ====================================================

        if evento.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = evento.pos

            # Menu lateral
            if 0 <= mouse_x <= 220:

                if 110 <= mouse_y < 158:
                    tela_atual = "inicio"

                elif 170 <= mouse_y < 218:
                    tela_atual = "jogos"

                elif 230 <= mouse_y < 278:
                    tela_atual = "ranking"

                elif 290 <= mouse_y < 338:
                    tela_atual = "favoritos"

            # =================================================
            # JOGOS
            # =================================================

            elif tela_atual == "jogos":

                for i, jogo in enumerate(jogos):

                    coluna = i % 3
                    linha = i // 3

                    x = 250 + coluna * 270
                    y = 100 + linha * 180

                    jogar_rect = pygame.Rect(
                        x + 18,
                        y + 95,
                        100,
                        35
                    )

                    favorito_rect = pygame.Rect(
                        x + 195,
                        y + 5,
                        45,
                        45
                    )

                    if jogar_rect.collidepoint(
                        evento.pos
                    ):

                        iniciar_jogo(
                            jogo["nome"]
                        )

                        break

                    if favorito_rect.collidepoint(
                        evento.pos
                    ):

                        adicionar_favorito(
                            jogo["nome"]
                        )

                        break

            # =================================================
            # FAVORITOS
            # =================================================

            elif tela_atual == "favoritos":

                for i, nome in enumerate(favoritos):

                    rect = pygame.Rect(
                        760,
                        120 + i * 85 + 17,
                        110,
                        36
                    )

                    if rect.collidepoint(evento.pos):

                        iniciar_jogo(nome)
                        break


# ============================================================
# LOOP PRINCIPAL
# ============================================================

rodando = True

while rodando:

    RELOGIO.tick(FPS)

    processar_eventos()

    # Fundo
    TELA.fill(FUNDO)

    # ========================================================
    # JOGO
    # ========================================================

    if jogo_atual is not None:

        atualizar_jogo()
        desenhar_jogo()

    # ========================================================
    # MENU
    # ========================================================

    else:

        desenhar_menu()

        if tela_atual == "inicio":
            tela_inicio()

        elif tela_atual == "jogos":
            tela_jogos()

        elif tela_atual == "ranking":
            tela_ranking()

        elif tela_atual == "favoritos":
            tela_favoritos()

    pygame.display.flip()


pygame.quit()
sys.exit()
