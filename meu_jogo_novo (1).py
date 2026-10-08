import pygame
import time
import json
import sqlite3
import os
import random
import math
import hashlib

pygame.init()

# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 1000
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Jogo de Plataforma")

RELOGIO = pygame.time.Clock()
FPS = 60

ARQUIVO_SAVE = "save_jogo.json"

BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
CINZA = (100, 100, 100)
CINZA_CLARO = (180, 180, 180)
VERDE = (40, 180, 70)
VERDE_ESCURO = (25, 110, 55)
VERDE_CLARO = (120, 230, 130)
AMARELO = (255, 220, 40)
LARANJA = (255, 110, 20)
VERMELHO = (220, 50, 50)
AZUL = (50, 120, 255)
ROXO = (150, 60, 220)
ROSA = (255, 90, 170)
CIANO = (40, 220, 220)
DOURADO = (255, 190, 30)

# ============================================================
# SKINS COMPRÁVEIS
# ============================================================

SKINS_COMPRAVEIS = [
    {"id": "azul", "preco": 0, "cor": (60, 130, 255), "tipo": "normal"},
    {"id": "aventureiro", "preco": 50, "cor": (170, 110, 60), "tipo": "heroi"},
    {"id": "pirata", "preco": 60, "cor": (170, 60, 60), "tipo": "pirata"},
    {"id": "ninja", "preco": 70, "cor": (50, 50, 60), "tipo": "ninja"},
    {"id": "robo", "preco": 80, "cor": (150, 160, 170), "tipo": "robo"},
    {"id": "astronauta", "preco": 90, "cor": (230, 230, 240), "tipo": "astronauta"},
    {"id": "dinossauro", "preco": 100, "cor": (70, 180, 80), "tipo": "dino"},
    {"id": "fantasma", "preco": 50, "cor": (210, 220, 255), "tipo": "fantasma"},
    {"id": "vulcao", "preco": 80, "cor": (220, 60, 30), "tipo": "vulcao"},
    {"id": "gelo", "preco": 70, "cor": (100, 210, 255), "tipo": "gelo"},
    {"id": "rainbow", "preco": 100, "cor": (255, 100, 180), "tipo": "rainbow"},
    {"id": "rei", "preco": 120, "cor": (180, 100, 240), "tipo": "rei"},
    {"id": "sombra", "preco": 90, "cor": (40, 40, 50), "tipo": "sombra"},
    {"id": "neon", "preco": 100, "cor": (20, 240, 230), "tipo": "neon"},
    {"id": "ouro", "preco": 500, "cor": (255, 200, 30), "tipo": "ouro"},

    # NOVAS SKINS DE HERÓIS
    {"id": "heroi_vermelho", "preco": 50, "cor": (220, 50, 50), "tipo": "heroi_vermelho"},
    {"id": "heroi_azul", "preco": 55, "cor": (50, 100, 230), "tipo": "heroi_azul"},
    {"id": "heroi_verde", "preco": 45, "cor": (50, 190, 90), "tipo": "heroi_verde"},
    {"id": "heroi_roxo", "preco": 60, "cor": (150, 60, 220), "tipo": "heroi_roxo"},
    {"id": "heroi_laranja", "preco": 50, "cor": (255, 120, 30), "tipo": "heroi_laranja"},
    {"id": "heroi_ciano", "preco": 65, "cor": (30, 210, 220), "tipo": "heroi_ciano"},
    {"id": "guardiao", "preco": 75, "cor": (70, 80, 100), "tipo": "guardiao"},
    {"id": "velocista", "preco": 60, "cor": (230, 230, 40), "tipo": "velocista"},
    {"id": "mago", "preco": 70, "cor": (100, 50, 200), "tipo": "mago"},
    {"id": "guerreiro", "preco": 65, "cor": (150, 70, 40), "tipo": "guerreiro"},
]

# Skins EXCLUSIVAS da roleta
SKINS_ROLETA = [
    {"id": "heroi_lendario", "cor": (255, 70, 70), "tipo": "lendario"},
    {"id": "heroi_galaxia", "cor": (100, 50, 220), "tipo": "galaxia"},
    {"id": "cavaleiro_neon", "cor": (30, 240, 220), "tipo": "neon"},
    {"id": "rei_trovao", "cor": (255, 190, 40), "tipo": "trovao"},
    {"id": "heroi_sombrio", "cor": (40, 40, 60), "tipo": "sombrio"},
    {"id": "mestre_gelo", "cor": (80, 220, 255), "tipo": "gelo_lendario"},
]

# ============================================================
# ITENS
# ============================================================

ITENS = {
    "mola": {
        "preco": 1000,
        "nome": "MOLA",
    },
    "mochila_jato": {
        "preco": 5000,
        "nome": "MOCHILA A JATO",
    },
    "teleporte": {
        "preco": 8500,
        "nome": "TELEPORTE",
    }
}

# ============================================================
# CONTAS / SAVE
# ============================================================

ARQUIVO_BANCO = "jogo.db"


def conectar_banco():
    con = sqlite3.connect(ARQUIVO_BANCO)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def inicializar_banco():
    con = conectar_banco()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nome_normalizado TEXT NOT NULL,
            senha_hash TEXT NOT NULL,
            moedas INTEGER NOT NULL DEFAULT 0,
            moedas_infinitas INTEGER NOT NULL DEFAULT 0,
            roupa_atual TEXT NOT NULL DEFAULT 'azul',
            melhor_tempo REAL,
            dois_pulos INTEGER NOT NULL DEFAULT 0,
            UNIQUE(nome_normalizado, senha_hash)
        );
        CREATE TABLE IF NOT EXISTS jogadores_skins (
            jogador_id INTEGER NOT NULL,
            skin_id TEXT NOT NULL,
            PRIMARY KEY(jogador_id, skin_id),
            FOREIGN KEY(jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS jogadores_itens (
            jogador_id INTEGER NOT NULL,
            item_id TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(jogador_id, item_id),
            FOREIGN KEY(jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE
        );
    """)
    con.commit()
    con.close()


def senha_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def criar_id_conta(nome, senha):
    return hashlib.sha256((nome.strip().lower() + "\0" + senha).encode("utf-8")).hexdigest()


def carregar_save_jogador(jogador_id):
    con = conectar_banco()
    row = con.execute("SELECT * FROM jogadores WHERE id = ?", (jogador_id,)).fetchone()
    compradas = [r[0] for r in con.execute("SELECT skin_id FROM jogadores_skins WHERE jogador_id = ?", (jogador_id,)).fetchall()]
    itens = {item: 0 for item in ITENS}
    for r in con.execute("SELECT item_id, quantidade FROM jogadores_itens WHERE jogador_id = ?", (jogador_id,)).fetchall():
        itens[r[0]] = int(r[1])
    con.close()
    if row is None:
        return save_padrao()
    dados = {
        "moedas": int(row["moedas"]),
        "moedas_infinitas": bool(row["moedas_infinitas"]),
        "compradas": compradas or ["azul"],
        "roupa_atual": row["roupa_atual"],
        "melhor_tempo": row["melhor_tempo"],
        "dois_pulos": bool(row["dois_pulos"]),
        "itens": itens,
    }
    return preparar_save(dados)


def salvar_conta_sql(jogador_id, nome, senha_hash_atual, dados):
    dados = preparar_save(dados)
    con = conectar_banco()
    con.execute("""UPDATE jogadores SET nome=?, senha_hash=?, moedas=?, moedas_infinitas=?, roupa_atual=?, melhor_tempo=?, dois_pulos=? WHERE id=?""",
                (nome, senha_hash_atual, dados["moedas"], int(dados["moedas_infinitas"]), dados["roupa_atual"], dados["melhor_tempo"], int(dados["dois_pulos"]), jogador_id))
    con.execute("DELETE FROM jogadores_skins WHERE jogador_id=?", (jogador_id,))
    con.executemany("INSERT INTO jogadores_skins(jogador_id, skin_id) VALUES(?,?)", [(jogador_id, x) for x in dados["compradas"]])
    con.execute("DELETE FROM jogadores_itens WHERE jogador_id=?", (jogador_id,))
    con.executemany("INSERT INTO jogadores_itens(jogador_id, item_id, quantidade) VALUES(?,?,?)", [(jogador_id, x, int(dados["itens"].get(x, 0))) for x in ITENS])
    con.commit()
    con.close()


inicializar_banco()
conta_atual_id = None
conta_atual_nome = ""
conta_atual_hash = ""
save = save_padrao()


def atualizar_conta_atual():
    if conta_atual_id is not None:
        salvar_conta_sql(conta_atual_id, conta_atual_nome, conta_atual_hash, save)


def salvar_save():
    atualizar_conta_atual()


def processar_conta(nome, senha, criar=False):
    global save, conta_atual_id, conta_atual_nome, conta_atual_hash
    nome = nome.strip()
    if len(nome) < 2:
        return "O nome precisa ter pelo menos 2 caracteres."
    if len(senha) < 3:
        return "A senha precisa ter pelo menos 3 caracteres."
    shash = senha_hash(senha)
    con = conectar_banco()
    row = con.execute("SELECT * FROM jogadores WHERE nome_normalizado=? AND senha_hash=?", (nome.lower(), shash)).fetchone()
    if row:
        con.close()
        conta_atual_id = row["id"]
        conta_atual_nome = row["nome"]
        conta_atual_hash = shash
        save = carregar_save_jogador(conta_atual_id)
        return "entrou"
    if not criar:
        con.close()
        return False
    con.execute("INSERT INTO jogadores(nome,nome_normalizado,senha_hash) VALUES(?,?,?)", (nome, nome.lower(), shash))
    jogador_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    con.commit()
    con.close()
    conta_atual_id = jogador_id
    conta_atual_nome = nome
    conta_atual_hash = shash
    save = save_padrao()
    salvar_save()
    return "criada"


def processar_codigo_secreto(codigo):
    if codigo != "674267":
        return False
    return processar_conta("VoidT0bzinn", "Mtoct2020", True) in ("criada", "entrou")


# ============================================================
# TEXTOS
# ============================================================

def texto(msg, tamanho, cor=BRANCO):
    fonte = pygame.font.SysFont("arial", tamanho, bold=True)
    return fonte.render(str(msg), True, cor)


def escrever(msg, x, y, tamanho=25, cor=BRANCO):
    TELA.blit(texto(msg, tamanho, cor), (x, y))


# ============================================================
# BOTÃO
# ============================================================

def botao(rect, nome, mouse, tamanho=25):
    cor = (60, 60, 70)

    if rect.collidepoint(mouse):
        cor = (90, 90, 110)

    pygame.draw.rect(TELA, cor, rect, border_radius=10)
    pygame.draw.rect(TELA, BRANCO, rect, 2, border_radius=10)

    fonte = texto(nome, tamanho)
    TELA.blit(
        fonte,
        (
            rect.centerx - fonte.get_width() // 2,
            rect.centery - fonte.get_height() // 2
        )
    )


# ============================================================
# DESENHO DO PERSONAGEM
# ============================================================

def desenhar_personagem(superficie, x, y, escala=1, roupa=None):
    if roupa is None:
        roupa = save["roupa_atual"]

    info = None

    for skin in SKINS_COMPRAVEIS:
        if skin["id"] == roupa:
            info = skin
            break

    if info is None:
        for skin in SKINS_ROLETA:
            if skin["id"] == roupa:
                info = skin
                break

    if info is None:
        info = SKINS_COMPRAVEIS[0]

    cor = info["cor"]
    tipo = info["tipo"]

    x = int(x)
    y = int(y)

    # Aura da skin ouro
    if tipo == "ouro":
        aura = pygame.Surface((100, 120), pygame.SRCALPHA)
        pygame.draw.circle(
            aura,
            (255, 215, 50, 70),
            (50, 60),
            48
        )
        superficie.blit(aura, (x - 30, y - 25))

    # Aura das skins lendárias
    if tipo in ["lendario", "galaxia", "trovao"]:
        aura = pygame.Surface((100, 120), pygame.SRCALPHA)
        pygame.draw.circle(
            aura,
            (*cor, 65),
            (50, 60),
            45
        )
        superficie.blit(aura, (x - 30, y - 25))

    # pernas
    pygame.draw.rect(
        superficie,
        (30, 30, 40),
        (x + 17, y + 65, 10, 30)
    )
    pygame.draw.rect(
        superficie,
        (30, 30, 40),
        (x + 38, y + 65, 10, 30)
    )

    # braços
    pygame.draw.rect(
        superficie,
        cor,
        (x + 2, y + 35, 13, 35),
        border_radius=5
    )

    pygame.draw.rect(
        superficie,
        cor,
        (x + 50, y + 35, 13, 35),
        border_radius=5
    )

    # corpo
    pygame.draw.rect(
        superficie,
        cor,
        (x + 13, y + 30, 40, 45),
        border_radius=8
    )

    # detalhes de heróis
    if "heroi" in tipo or tipo in [
        "guardiao",
        "velocista",
        "mago",
        "guerreiro",
        "lendario",
        "galaxia",
        "trovao",
        "sombrio"
    ]:
        pygame.draw.polygon(
            superficie,
            BRANCO,
            [
                (x + 33, y + 35),
                (x + 42, y + 55),
                (x + 33, y + 65),
                (x + 24, y + 55)
            ]
        )

    # capa
    if tipo in [
        "heroi_vermelho",
        "heroi_roxo",
        "guardiao",
        "rei",
        "ouro",
        "lendario",
        "trovao",
        "guerreiro"
    ]:
        pygame.draw.polygon(
            superficie,
            (25, 25, 30),
            [
                (x + 13, y + 35),
                (x - 3, y + 80),
                (x + 13, y + 72)
            ]
        )

    # cabeça
    pygame.draw.circle(
        superficie,
        (245, 195, 150),
        (x + 33, y + 22),
        23
    )

    # cabelo / capacete
    if tipo == "ninja":
        pygame.draw.rect(
            superficie,
            (30, 30, 35),
            (x + 10, y + 5, 46, 17),
            border_radius=8
        )

    elif tipo == "robo":
        pygame.draw.rect(
            superficie,
            (100, 110, 120),
            (x + 11, y + 2, 44, 40),
            border_radius=8
        )
        pygame.draw.circle(
            superficie,
            CIANO,
            (x + 25, y + 21),
            4
        )
        pygame.draw.circle(
            superficie,
            CIANO,
            (x + 41, y + 21),
            4
        )

    elif tipo in ["astronauta", "guardiao"]:
        pygame.draw.circle(
            superficie,
            (210, 220, 230),
            (x + 33, y + 20),
            26,
            5
        )

    elif tipo == "mago":
        pygame.draw.polygon(
            superficie,
            (70, 30, 150),
            [
                (x + 8, y + 7),
                (x + 58, y + 7),
                (x + 33, y - 30)
            ]
        )

    elif tipo == "dino":
        pygame.draw.circle(
            superficie,
            (40, 130, 50),
            (x + 33, y + 10),
            22
        )

    elif tipo == "pirata":
        pygame.draw.rect(
            superficie,
            (25, 25, 25),
            (x + 9, y + 5, 48, 13)
        )

    else:
        pygame.draw.arc(
            superficie,
            (50, 40, 30),
            (x + 10, y + 2, 46, 32),
            math.pi,
            math.pi * 2,
            7
        )

    # olhos
    if tipo != "robo":
        pygame.draw.circle(
            superficie,
            PRETO,
            (x + 25, y + 23),
            3
        )
        pygame.draw.circle(
            superficie,
            PRETO,
            (x + 41, y + 23),
            3
        )

    # coroa
    if tipo == "rei":
        pygame.draw.polygon(
            superficie,
            DOURADO,
            [
                (x + 8, y + 2),
                (x + 15, y - 15),
                (x + 25, y),
                (x + 33, y - 17),
                (x + 41, y),
                (x + 52, y - 15),
                (x + 58, y + 2)
            ]
        )

    # detalhes ouro
    if tipo == "ouro":
        pygame.draw.rect(
            superficie,
            PRETO,
            (x - 5, y + 28, 10, 55)
        )


# ============================================================
# PREVIEW
# ============================================================

def preview_skin(roupa, x, y, escala=1.5):
    desenhar_personagem(
        TELA,
        x,
        y,
        escala,
        roupa
    )


# ============================================================
# BANDEIRA
# ============================================================

def desenhar_bandeira(x, y):
    pygame.draw.rect(
        TELA,
        (80, 50, 30),
        (x, y, 7, 70)
    )

    pygame.draw.polygon(
        TELA,
        AMARELO,
        [
            (x + 7, y),
            (x + 50, y + 15),
            (x + 7, y + 30)
        ]
    )


# ============================================================
# CRIAÇÃO DAS FASES
# ============================================================

def criar_fase(numero, modo):
    plataformas = []

    if modo == "EXTRA HARD":
        # Antigo HARD: fases muito longas com plataformas fantasmas.
        quantidade = 26 + numero * 3
        distancia = 150

    elif modo == "HARD":
        # HARD: difícil, sem fantasmas e sem bandeira fugitiva.
        # Sequência: 1 normal, 2 móveis, 1 normal, 2 móveis...
        quantidade = 17 + numero * 2
        distancia = 165

    elif modo == "MEDIO":
        quantidade = 13 + numero
        distancia = 180

    else:
        quantidade = 10 + numero
        distancia = 190

    # primeira plataforma SEMPRE FIXA
    plataformas.append({
        "rect": pygame.Rect(40, 480, 150, 30),
        "tipo": "fixa",
        "indice": 1
    })

    x = 230
    altura_base = 430

    for i in range(2, quantidade + 1):

        if modo == "HARD":
            # HARD tem um padrão fixo e seguro:
            # plataforma fixa -> móvel -> móvel -> fixa -> móvel -> móvel...
            # Cada grupo ocupa um corredor próprio. Os móveis nunca alcançam
            # a plataforma fixa nem encostam um no outro.
            grupo = (i - 2) // 3
            posicao = (i - 2) % 3

            if posicao == 0:
                tipo = "movel"
                x = 230 + grupo * 720
                largura = 110
                limite = 70
            elif posicao == 1:
                tipo = "movel"
                x = 480 + grupo * 720
                largura = 110
                limite = 70
            else:
                tipo = "fixa"
                x = 730 + grupo * 720
                largura = 150
                limite = 0

            # Pequenas diferenças de altura, mas sem alterar o corredor horizontal.
            y = altura_base - random.randint(0, 55)

        else:
            y = altura_base - random.randint(-70, 80)

            if modo == "EXTRA HARD":
                # 1, 5, 9, 13, 17... sempre fixas; as demais são fantasmas.
                if (i - 1) % 4 == 0:
                    tipo = "fixa"
                else:
                    tipo = "fantasma"
            else:
                tipo = "fixa"

            largura = random.randint(110, 165)
            limite = random.randint(65, 105) if tipo == "movel" else 0

        plataformas.append({
            "rect": pygame.Rect(
                x,
                y,
                largura,
                25
            ),
            "tipo": tipo,
            "indice": i,
            "x_inicial": x,
            "direcao": 1,
            "velocidade": random.choice([3, 4, 4]),
            "limite": limite
        })

        if modo != "HARD":
            x += distancia + random.randint(-35, 40)

    return plataformas


# ============================================================
# PLATAFORMAS MÓVEIS DO HARD
# ============================================================

def atualizar_plataformas_moveis(plataformas, modo):
    if modo != "HARD":
        return

    for plataforma in plataformas:
        if plataforma["tipo"] != "movel":
            continue

        plataforma["rect"].x += plataforma["direcao"] * plataforma["velocidade"]

        esquerda = plataforma["x_inicial"] - plataforma["limite"]
        direita = plataforma["x_inicial"] + plataforma["limite"]

        if plataforma["rect"].x <= esquerda:
            plataforma["rect"].x = esquerda
            plataforma["direcao"] = 1
        elif plataforma["rect"].x >= direita:
            plataforma["rect"].x = direita
            plataforma["direcao"] = -1


# ============================================================
# ESTADO DAS PLATAFORMAS FANTASMAS
# ============================================================

def plataforma_solida(plataforma, tempo_fase, modo):
    if plataforma["tipo"] == "fixa":
        return True

    if modo != "EXTRA HARD":
        return True

    indice = plataforma["indice"]

    # As plataformas 1, 5, 9, 13... nunca são fantasmas.
    if (indice - 1) % 4 == 0:
        return True

    # Começa normal durante os primeiros 3 segundos.
    ciclo = int(tempo_fase // 3)

    # Cada grupo alterna.
    grupo = (indice - 2) // 3

    return (ciclo + grupo) % 2 == 0


# ============================================================
# INIMIGOS FANTASMAS
# ============================================================

def criar_inimigos(plataformas, modo):
    inimigos = []

    if modo != "EXTRA HARD":
        return inimigos

    for p in plataformas[4::5]:
        inimigos.append({
            "x": p["rect"].x + 20,
            "y": p["rect"].y - 55,
            "direcao": 1,
            "inicio": p["rect"].x - 50,
            "fim": p["rect"].x + 100
        })

    return inimigos


def atualizar_inimigos(inimigos):
    for inimigo in inimigos:
        inimigo["x"] += inimigo["direcao"] * 2

        if inimigo["x"] <= inimigo["inicio"]:
            inimigo["direcao"] = 1

        if inimigo["x"] >= inimigo["fim"]:
            inimigo["direcao"] = -1


def desenhar_inimigos(inimigos, camera_x):
    for inimigo in inimigos:
        x = inimigo["x"] - camera_x
        y = inimigo["y"]

        pygame.draw.circle(
            TELA,
            (180, 180, 255),
            (int(x + 25), int(y + 25)),
            25
        )

        pygame.draw.circle(
            TELA,
            PRETO,
            (int(x + 17), int(y + 22)),
            4
        )

        pygame.draw.circle(
            TELA,
            PRETO,
            (int(x + 33), int(y + 22)),
            4
        )


# ============================================================
# LOGIN / CRIAÇÃO DE CONTA
# ============================================================

def tela_conta():
    global save, conta_atual_id, conta_atual_nome, conta_atual_hash

    nome = ""
    senha = ""
    codigo_secreto = ""
    campo = "nome"
    mensagem = ""
    mensagem_cor = CINZA_CLARO

    while True:
        TELA.fill((20, 20, 35))
        mouse = pygame.mouse.get_pos()

        escrever("BEM-VINDO AO MEU JOGO", 235, 40, 42, AMARELO)
        escrever("Sua carreira fica salva nesta conta", 300, 92, 20, CINZA_CLARO)

        caixa_nome = pygame.Rect(270, 145, 460, 58)
        caixa_senha = pygame.Rect(270, 235, 460, 58)
        botao_entrar = pygame.Rect(270, 330, 220, 58)
        botao_criar = pygame.Rect(510, 330, 220, 58)

        pygame.draw.rect(TELA, (45, 45, 65), caixa_nome, border_radius=10)
        pygame.draw.rect(
            TELA,
            AMARELO if campo == "nome" else CINZA,
            caixa_nome,
            3,
            border_radius=10
        )
        pygame.draw.rect(TELA, (45, 45, 65), caixa_senha, border_radius=10)
        pygame.draw.rect(
            TELA,
            AMARELO if campo == "senha" else CINZA,
            caixa_senha,
            3,
            border_radius=10
        )

        escrever("NOME DO JOGADOR", 270, 118, 18, BRANCO)
        escrever(
            nome if nome else "Digite seu nome...",
            290,
            162,
            25,
            BRANCO if nome else CINZA_CLARO
        )

        escrever("SENHA", 270, 208, 18, BRANCO)
        senha_visual = "*" * len(senha) if senha else "Digite sua senha..."
        escrever(
            senha_visual,
            290,
            252,
            25,
            BRANCO if senha else CINZA_CLARO
        )

        botao(botao_entrar, "ENTRAR", mouse)
        botao(botao_criar, "CRIAR CONTA", mouse)

        escrever(
            "Se nome + senha já existem, só é possível ENTRAR nessa conta.",
            245,
            405,
            16,
            CINZA_CLARO
        )

        if mensagem:
            escrever(mensagem, 250, 435, 17, mensagem_cor)

        # Barra secreta EXTRA, quase invisível.
        caixa_codigo = pygame.Rect(865, 570, 110, 20)
        pygame.draw.rect(TELA, (21, 21, 35), caixa_codigo, border_radius=4)
        pygame.draw.rect(
            TELA,
            (32, 32, 46),
            caixa_codigo,
            1,
            border_radius=4
        )
        codigo_visual = "•" * len(codigo_secreto) if codigo_secreto else ""
        if codigo_secreto:
            escrever(codigo_visual, 874, 571, 10, (75, 75, 90))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

                if evento.key == pygame.K_TAB:
                    if campo == "nome":
                        campo = "senha"
                    elif campo == "senha":
                        campo = "codigo"
                    else:
                        campo = "nome"

                elif evento.key == pygame.K_BACKSPACE:
                    if campo == "nome":
                        nome = nome[:-1]
                    elif campo == "senha":
                        senha = senha[:-1]
                    else:
                        codigo_secreto = codigo_secreto[:-1]

                elif evento.key == pygame.K_RETURN:
                    if campo == "codigo":
                        resultado = processar_codigo_secreto(codigo_secreto)
                        if resultado:
                            return
                        mensagem = "Código secreto inválido."
                        mensagem_cor = VERMELHO
                    else:
                        resultado = processar_conta(nome, senha, False)
                        if resultado == "entrou":
                            return
                        mensagem = (
                            "Conta não encontrada. Para uma conta nova, clique em CRIAR CONTA."
                            if resultado is False
                            else resultado
                        )
                        mensagem_cor = VERMELHO

                elif evento.unicode and evento.unicode.isprintable():
                    if campo == "nome" and len(nome) < 20:
                        if evento.unicode not in '\\/:*?"<>|':
                            nome += evento.unicode
                    elif campo == "senha" and len(senha) < 32:
                        senha += evento.unicode
                    elif campo == "codigo" and len(codigo_secreto) < 32:
                        codigo_secreto += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if caixa_nome.collidepoint(evento.pos):
                    campo = "nome"
                elif caixa_senha.collidepoint(evento.pos):
                    campo = "senha"
                elif caixa_codigo.collidepoint(evento.pos):
                    campo = "codigo"
                elif botao_entrar.collidepoint(evento.pos):
                    resultado = processar_conta(nome, senha, False)
                    if resultado != "entrou":
                        mensagem = (
                            "Conta não encontrada ou senha incorreta."
                            if resultado is False or resultado == "Senha incorreta."
                            else resultado
                        )
                        mensagem_cor = VERMELHO
                    else:
                        return
                elif botao_criar.collidepoint(evento.pos):
                    resultado = processar_conta(nome, senha, True)
                    if resultado in ("criada", "entrou"):
                        return
                    mensagem = resultado
                    mensagem_cor = VERMELHO

        pygame.display.flip()
        RELOGIO.tick(FPS)


def processar_conta(nome, senha, criar=False):
    global save, conta_atual_id, conta_atual_nome, conta_atual_hash

    nome = nome.strip()
    if len(nome) < 2:
        return "O nome precisa ter pelo menos 2 caracteres."
    if len(senha) < 3:
        return "A senha precisa ter pelo menos 3 caracteres."

    cid = criar_id_conta(nome, senha)
    shash = senha_hash(senha)

    # A combinação exata nome + senha identifica uma conta.
    # Se ela já existe, NUNCA cria outra: apenas entra.
    if cid in contas:
        conta = contas[cid]
        if conta.get("senha") == shash:
            conta_atual_id = cid
            conta_atual_nome = conta.get("nome", nome)
            conta_atual_hash = shash
            save = preparar_save(conta.get("save", {}))
            return "entrou"
        return "Senha incorreta."

    if not criar:
        return False

    # Nomes iguais continuam permitidos quando a senha é diferente.
    contas[cid] = {
        "nome": nome,
        "senha": shash,
        "save": save_padrao()
    }
    salvar_contas()

    conta_atual_id = cid
    conta_atual_nome = nome
    conta_atual_hash = shash
    save = preparar_save(contas[cid]["save"])
    return "criada"


def processar_codigo_secreto(codigo):
    """Acesso discreto à conta especial usando o código secreto da tela de login."""
    global save, conta_atual_id, conta_atual_nome, conta_atual_hash

    if codigo != "674267":
        return False

    nome_especial = "VoidT0bzinn"
    senha_especial = "Mtoct2020"
    cid = criar_id_conta(nome_especial, senha_especial)
    shash = senha_hash(senha_especial)

    # A combinação secreta sempre aponta para a conta VoidT0bzinn.
    # Se ela ainda não estiver no arquivo de contas, ela é criada automaticamente
    # com o save padrão e, em seguida, o acesso é feito normalmente.
    if cid not in contas:
        contas[cid] = {
            "nome": nome_especial,
            "senha": shash,
            "save": save_padrao()
        }
        salvar_contas()

    conta = contas[cid]
    if conta.get("senha") != shash:
        return False

    conta_atual_id = cid
    conta_atual_nome = conta.get("nome", nome_especial)
    conta_atual_hash = shash
    save = preparar_save(conta.get("save", {}))
    return True


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():
    while True:
        TELA.fill((25, 25, 40))

        mouse = pygame.mouse.get_pos()

        escrever("MEU JOGO", 340, 70, 60, AMARELO)

        escrever(
            "MOEDAS: " +
            ("∞" if save["moedas_infinitas"] else str(save["moedas"])),
            30,
            25,
            25,
            DOURADO
        )

        botoes = [
            (pygame.Rect(350, 170, 300, 60), "JOGAR"),
            (pygame.Rect(350, 250, 300, 60), "LOJA"),
            (pygame.Rect(350, 330, 300, 60), "INVENTARIO"),
            (pygame.Rect(350, 410, 300, 60), "SAIR")
        ]

        for rect, nome in botoes:
            botao(rect, nome, mouse)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    if botoes[0][0].collidepoint(mouse):
                        modo = selecionar_modo()

                        if modo:
                            jogar(modo)

                    elif botoes[1][0].collidepoint(mouse):
                        loja()

                    elif botoes[2][0].collidepoint(mouse):
                        inventario()

                    elif botoes[3][0].collidepoint(mouse):
                        salvar_save()
                        pygame.quit()
                        raise SystemExit

        pygame.display.flip()
        RELOGIO.tick(FPS)


# ============================================================
# SELEÇÃO DE MODO
# ============================================================

def selecionar_modo():
    while True:
        TELA.fill((25, 25, 40))

        mouse = pygame.mouse.get_pos()

        escrever("ESCOLHA O MODO", 315, 70, 45)

        botoes = [
            (pygame.Rect(350, 160, 300, 60), "FACIL"),
            (pygame.Rect(350, 240, 300, 60), "MEDIO"),
            (pygame.Rect(350, 320, 300, 60), "HARD"),
            (pygame.Rect(350, 400, 300, 60), "EXTRA HARD"),
            (pygame.Rect(350, 480, 300, 60), "VOLTAR")
        ]

        for rect, nome in botoes:
            botao(rect, nome, mouse)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    if botoes[0][0].collidepoint(mouse):
                        return "FACIL"

                    if botoes[1][0].collidepoint(mouse):
                        return "MEDIO"

                    if botoes[2][0].collidepoint(mouse):
                        return "HARD"

                    if botoes[3][0].collidepoint(mouse):
                        return "EXTRA HARD"

                    if botoes[4][0].collidepoint(mouse):
                        return None

        pygame.display.flip()
        RELOGIO.tick(FPS)


# ============================================================
# COMPRAR SKIN
# ============================================================

def comprar_skin(skin):
    if skin["id"] in save["compradas"]:
        save["roupa_atual"] = skin["id"]
        salvar_save()
        return

    preco = skin["preco"]

    if save["moedas_infinitas"] or save["moedas"] >= preco:
        if not save["moedas_infinitas"]:
            save["moedas"] -= preco

        save["compradas"].append(skin["id"])
        save["roupa_atual"] = skin["id"]

        salvar_save()


# ============================================================
# COMPRAR ITEM
# ============================================================

def comprar_item(item):
    if save["itens"].get(item, 0) > 0:
        return

    preco = ITENS[item]["preco"]

    if save["moedas_infinitas"] or save["moedas"] >= preco:

        if not save["moedas_infinitas"]:
            save["moedas"] -= preco

        save["itens"][item] = 1
        salvar_save()


# ============================================================
# ROLETА
# ============================================================

def girar_roleta():
    custo = 10

    if not save["moedas_infinitas"] and save["moedas"] < custo:
        return None

    if not save["moedas_infinitas"]:
        save["moedas"] -= custo

    escolhido = random.choice(SKINS_ROLETA)
    id_skin = escolhido["id"]

    if id_skin in save["compradas"]:

        # devolve SOMENTE 5
        if not save["moedas_infinitas"]:
            save["moedas"] += 5

        salvar_save()
        return "REPETIDA"

    save["compradas"].append(id_skin)
    salvar_save()

    return id_skin


# ============================================================
# TELA DA ROLETA
# ============================================================

def tela_roleta():
    resultado = None

    while True:
        TELA.fill((25, 20, 45))

        mouse = pygame.mouse.get_pos()

        escrever("ROLETA DE SKINS", 285, 35, 45, AMARELO)

        escrever(
            "Giro: 10 moedas",
            360,
            90,
            25,
            BRANCO
        )

        escrever(
            "Se repetir: +5 moedas",
            340,
            120,
            20,
            CINZA_CLARO
        )

        # roleta
        pygame.draw.circle(
            TELA,
            (70, 50, 100),
            (300, 300),
            130
        )

        pygame.draw.circle(
            TELA,
            (30, 25, 50),
            (300, 300),
            100
        )

        for i in range(12):
            ang = i * math.pi / 6
            x = 300 + math.cos(ang) * 100
            y = 300 + math.sin(ang) * 100

            pygame.draw.circle(
                TELA,
                [
                    VERMELHO,
                    AZUL,
                    VERDE,
                    AMARELO,
                    ROXO,
                    CIANO
                ][i % 6],
                (int(x), int(y)),
                15
            )

        escrever("★", 280, 265, 50, DOURADO)

        # skins possíveis
        escrever("SKINS POSSÍVEIS", 580, 150, 28)

        for i, skin in enumerate(SKINS_ROLETA):
            x = 580 + (i % 3) * 120
            y = 210 + (i // 3) * 130

            pygame.draw.rect(
                TELA,
                (45, 45, 60),
                (x, y, 100, 100),
                border_radius=10
            )

            desenhar_personagem(
                TELA,
                x + 20,
                y + 10,
                1,
                skin["id"]
            )

        botao_girar = pygame.Rect(150, 460, 300, 60)
        botao_voltar = pygame.Rect(550, 460, 300, 60)

        botao(
            botao_girar,
            "GIRAR - 10",
            mouse
        )

        botao(
            botao_voltar,
            "VOLTAR",
            mouse
        )

        if resultado:
            if resultado == "REPETIDA":
                escrever(
                    "SKIN REPETIDA! +5",
                    250,
                    400,
                    25,
                    AMARELO
                )
            else:
                escrever(
                    "VOCÊ GANHOU UMA SKIN!",
                    200,
                    400,
                    25,
                    VERDE_CLARO
                )

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_save()
                pygame.quit()
                raise SystemExit

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    if botao_girar.collidepoint(mouse):
                        resultado = girar_roleta()

                    elif botao_voltar.collidepoint(mouse):
                        return

        pygame.display.flip()
        RELOGIO.tick(FPS)


# ============================================================
# LOJA
# ============================================================


# ============================================================
# CÓDIGOS SECRETOS
# ============================================================

def ativar_codigo_secreto(codigo):
    codigo = codigo.strip().lower()
    if codigo == "6742infinitymoney":
        save["moedas_infinitas"] = True
        salvar_save()
        return "DINHEIRO INFINITO ATIVADO!"
    if codigo == "dublesidejump":
        save["dois_pulos"] = True
        salvar_save()
        return "DUPLO PULO ATIVADO!"
    return "CÓDIGO INVÁLIDO"

def loja():
    aba = "SKINS"
    scroll = 0
    codigo = ""
    codigo_ativo = False
    mensagem_codigo = ""
    mensagem_codigo_cor = CINZA_CLARO

    while True:
        TELA.fill((22, 22, 32))
        mouse = pygame.mouse.get_pos()

        escrever("LOJA", 40, 25, 45, AMARELO)
        escrever("MOEDAS: " + ("∞" if save["moedas_infinitas"] else str(save["moedas"])), 700, 35, 25, DOURADO)

        aba_skins = pygame.Rect(30, 90, 180, 50)
        aba_itens = pygame.Rect(220, 90, 180, 50)
        aba_roleta = pygame.Rect(410, 90, 180, 50)
        voltar = pygame.Rect(780, 90, 180, 50)

        botao(aba_skins, "SKINS", mouse, 20)
        botao(aba_itens, "ITENS", mouse, 20)
        botao(aba_roleta, "ROLETA", mouse, 20)
        botao(voltar, "VOLTAR", mouse, 20)

        # Barra discreta para os códigos secretos. Clique nela para revelar/usar.
        codigo_rect = pygame.Rect(700, 545, 260, 35)
        pygame.draw.rect(TELA, (18, 18, 28), codigo_rect, border_radius=8)
        pygame.draw.rect(TELA, AMARELO if codigo_ativo else (55, 55, 70), codigo_rect, 2, border_radius=8)
        codigo_visual = codigo if codigo else "código secreto..."
        escrever(codigo_visual, 710, 552, 15, BRANCO if codigo else CINZA)
        if mensagem_codigo:
            escrever(mensagem_codigo, 40, 555, 16, mensagem_codigo_cor)

        area = pygame.Rect(20, 155, 960, 365)
        pygame.draw.rect(TELA, (30, 30, 42), area, border_radius=10)
        TELA.set_clip(area)

        if aba == "SKINS":
            # Mostra TODAS as skins compráveis e, abaixo, as skins ganhas na roleta.
            escrever("SKINS DA LOJA", 40, 165 - scroll, 26, BRANCO)

            y0 = 205 - scroll
            for i, skin in enumerate(SKINS_COMPRAVEIS):
                coluna = i % 4
                linha = i // 4
                x = 35 + coluna * 230
                y = y0 + linha * 180
                card = pygame.Rect(x, y, 210, 165)
                pygame.draw.rect(TELA, (50, 50, 65), card, border_radius=12)
                desenhar_personagem(TELA, x + 75, y + 25, 1, skin["id"])

                if skin["id"] == save["roupa_atual"]:
                    estado = "EQUIPADA"
                    cor_estado = VERDE_CLARO
                elif skin["id"] in save["compradas"]:
                    estado = "EQUIPAR"
                    cor_estado = BRANCO
                else:
                    estado = str(skin["preco"]) + " moedas"
                    cor_estado = DOURADO
                escrever(estado, x + 105 - texto(estado, 17).get_width() // 2, y + 128, 17, cor_estado)

            linhas_loja = math.ceil(len(SKINS_COMPRAVEIS) / 4)
            base_role = y0 + linhas_loja * 180 + 10
            escrever("SKINS GANHAS NA ROLETA", 40, base_role, 26, AMARELO)
            escrever("Estas skins ficam disponíveis no inventário e podem ser equipadas.", 40, base_role + 32, 17, CINZA_CLARO)

            roleta_possuidas = [s for s in SKINS_ROLETA if s["id"] in save["compradas"]]
            if not roleta_possuidas:
                escrever("Você ainda não ganhou nenhuma skin da roleta.", 40, base_role + 75, 20, CINZA_CLARO)
            else:
                for i, skin in enumerate(roleta_possuidas):
                    coluna = i % 4
                    linha = i // 4
                    x = 35 + coluna * 230
                    y = base_role + 70 + linha * 180
                    card = pygame.Rect(x, y, 210, 165)
                    pygame.draw.rect(TELA, (65, 45, 85), card, border_radius=12)
                    desenhar_personagem(TELA, x + 75, y + 25, 1, skin["id"])
                    if skin["id"] == save["roupa_atual"]:
                        estado = "EQUIPADA"
                        cor = VERDE_CLARO
                    else:
                        estado = "EQUIPAR"
                        cor = BRANCO
                    escrever(estado, x + 105 - texto(estado, 17).get_width() // 2, y + 128, 17, cor)

        elif aba == "ITENS":
            itens_lista = [("mola", 1000), ("mochila_jato", 5000), ("teleporte", 8500)]
            for i, (item, preco) in enumerate(itens_lista):
                y = 175 + i * 180 - scroll
                card = pygame.Rect(80, y, 840, 150)
                pygame.draw.rect(TELA, (50, 50, 65), card, border_radius=12)

                if item == "mola":
                    pygame.draw.arc(TELA, VERDE_CLARO, (130, y + 35, 70, 70), 0, math.pi * 2, 7)
                elif item == "mochila_jato":
                    pygame.draw.rect(TELA, CINZA, (130, y + 30, 70, 85), border_radius=12)
                    pygame.draw.polygon(TELA, LARANJA, [(145, y + 115), (155, y + 145), (165, y + 115)])
                    pygame.draw.polygon(TELA, LARANJA, [(170, y + 115), (180, y + 145), (190, y + 115)])
                else:
                    pygame.draw.circle(TELA, ROXO, (165, y + 70), 40)
                    pygame.draw.circle(TELA, CIANO, (165, y + 70), 25, 4)

                escrever(ITENS[item]["nome"], 250, y + 25, 28)
                escrever("Preço: " + str(preco), 250, y + 65, 22, DOURADO)
                if save["itens"].get(item, 0) > 0:
                    escrever("COMPRADO", 700, y + 60, 22, VERDE_CLARO)
                else:
                    escrever("COMPRAR", 700, y + 60, 22, BRANCO)

        TELA.set_clip(None)

        if aba == "SKINS":
            linhas = math.ceil(len(SKINS_COMPRAVEIS) / 4)
            qtd_roleta = len([s for s in SKINS_ROLETA if s["id"] in save["compradas"]])
            linhas_roleta = max(1, math.ceil(qtd_roleta / 4))
            conteudo = 205 + linhas * 180 + 120 + linhas_roleta * 180
            visivel = 365
        elif aba == "ITENS":
            conteudo = 3 * 180
            visivel = 365
        else:
            conteudo = 0
            visivel = 365

        scroll_max = max(0, conteudo - visivel)
        scroll = max(0, min(scroll, scroll_max))

        if aba != "ROLETA":
            pygame.draw.rect(TELA, (70, 70, 80), (965, 160, 10, 350), border_radius=5)
            if scroll_max > 0:
                tamanho_barra = max(40, int(350 * visivel / conteudo))
                pos_barra = 160 + int(350 * (scroll / scroll_max) * ((350 - tamanho_barra) / 350))
                pygame.draw.rect(TELA, CINZA_CLARO, (965, pos_barra, 10, tamanho_barra), border_radius=5)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_save()
                pygame.quit()
                raise SystemExit

            if evento.type == pygame.KEYDOWN and codigo_ativo:
                if evento.key == pygame.K_ESCAPE:
                    codigo_ativo = False
                    codigo = ""
                    mensagem_codigo = ""
                elif evento.key == pygame.K_BACKSPACE:
                    codigo = codigo[:-1]
                elif evento.key == pygame.K_RETURN:
                    mensagem_codigo = ativar_codigo_secreto(codigo)
                    mensagem_codigo_cor = VERDE_CLARO if mensagem_codigo != "CÓDIGO INVÁLIDO" else VERMELHO
                    codigo = ""
                    codigo_ativo = False
                elif evento.unicode and evento.unicode.isprintable() and len(codigo) < 30:
                    codigo += evento.unicode.lower()

            if evento.type == pygame.MOUSEWHEEL and aba != "ROLETA":
                scroll -= evento.y * 50
                scroll = max(0, min(scroll, scroll_max))

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if codigo_rect.collidepoint(evento.pos):
                    codigo_ativo = True
                    mensagem_codigo = ""
                elif aba_skins.collidepoint(mouse):
                    aba = "SKINS"
                    scroll = 0
                elif aba_itens.collidepoint(mouse):
                    aba = "ITENS"
                    scroll = 0
                elif aba_roleta.collidepoint(mouse):
                    tela_roleta()
                elif voltar.collidepoint(mouse):
                    salvar_save()
                    return
                elif aba == "SKINS":
                    # Compra/equipa skins normais.
                    for i, skin in enumerate(SKINS_COMPRAVEIS):
                        coluna = i % 4
                        linha = i // 4
                        card = pygame.Rect(35 + coluna * 230, 205 + linha * 180 - scroll, 210, 165)
                        if card.collidepoint(mouse):
                            comprar_skin(skin)
                            break
                    else:
                        # Equipa skins ganhas na roleta.
                        linhas_loja = math.ceil(len(SKINS_COMPRAVEIS) / 4)
                        base_role = 205 - scroll + linhas_loja * 180 + 10
                        roleta_possuidas = [s for s in SKINS_ROLETA if s["id"] in save["compradas"]]
                        for i, skin in enumerate(roleta_possuidas):
                            coluna = i % 4
                            linha = i // 4
                            card = pygame.Rect(35 + coluna * 230, base_role + 70 + linha * 180, 210, 165)
                            if card.collidepoint(mouse):
                                save["roupa_atual"] = skin["id"]
                                salvar_save()
                                break
                elif aba == "ITENS":
                    for i, (item, preco) in enumerate([("mola", 1000), ("mochila_jato", 5000), ("teleporte", 8500)]):
                        card = pygame.Rect(80, 175 + i * 180 - scroll, 840, 150)
                        if card.collidepoint(mouse):
                            comprar_item(item)
                            break

        pygame.display.flip()
        RELOGIO.tick(FPS)


def inventario():
    aba = "SKINS"
    scroll = 0

    while True:
        TELA.fill((22, 22, 32))
        mouse = pygame.mouse.get_pos()

        escrever("INVENTÁRIO", 35, 25, 45, AMARELO)

        aba_skins = pygame.Rect(30, 90, 220, 50)
        aba_itens = pygame.Rect(260, 90, 220, 50)
        voltar = pygame.Rect(780, 25, 180, 50)
        botao(aba_skins, "SKINS", mouse, 20)
        botao(aba_itens, "ITENS", mouse, 20)
        botao(voltar, "VOLTAR", mouse, 20)

        area = pygame.Rect(20, 155, 960, 400)
        pygame.draw.rect(TELA, (30, 30, 42), area, border_radius=10)
        TELA.set_clip(area)

        if aba == "SKINS":
            escrever("SKINS POSSUÍDAS", 40, 170 - scroll, 28, BRANCO)
            todas = [s for s in SKINS_COMPRAVEIS if s["id"] in save["compradas"]]
            todas += [s for s in SKINS_ROLETA if s["id"] in save["compradas"]]
            for i, skin in enumerate(todas):
                coluna = i % 5
                linha = i // 5
                x = 40 + coluna * 185
                y = 215 + linha * 150 - scroll
                card = pygame.Rect(x, y, 160, 125)
                pygame.draw.rect(TELA, (50, 50, 65), card, border_radius=10)
                desenhar_personagem(TELA, x + 50, y + 5, 1, skin["id"])
                estado = "EQUIPADA" if skin["id"] == save["roupa_atual"] else "EQUIPAR"
                cor = VERDE_CLARO if estado == "EQUIPADA" else BRANCO
                escrever(estado, x + 80 - texto(estado, 15).get_width() // 2, y + 96, 15, cor)

        else:
            escrever("ITENS POSSUÍDOS", 40, 170 - scroll, 28, BRANCO)
            lista = [item for item in ITENS if save["itens"].get(item, 0) > 0]
            if not lista:
                escrever("Nenhum item comprado.", 40, 220 - scroll, 21, CINZA_CLARO)
            for i, item in enumerate(lista):
                x = 55 + (i % 3) * 300
                y = 220 + (i // 3) * 160 - scroll
                pygame.draw.rect(TELA, (55, 55, 70), (x, y, 270, 130), border_radius=10)
                escrever(ITENS[item]["nome"], x + 15, y + 18, 21)
                if item == "mola":
                    escrever("AUTOMÁTICA", x + 15, y + 60, 18, VERDE_CLARO)
                elif item == "mochila_jato":
                    escrever("Q = ativar/desativar", x + 15, y + 60, 18, AMARELO)
                    escrever("SPACE = voar", x + 15, y + 88, 16, CINZA_CLARO)
                else:
                    escrever("F = ativar", x + 15, y + 60, 18, AMARELO)
                    escrever("Clique para teleportar", x + 15, y + 88, 16, CINZA_CLARO)

        TELA.set_clip(None)

        if aba == "SKINS":
            linhas = max(1, math.ceil(len([s for s in SKINS_COMPRAVEIS + SKINS_ROLETA if s["id"] in save["compradas"]]) / 5))
            conteudo = 215 + linhas * 150
        else:
            linhas = max(1, math.ceil(len([i for i in ITENS if save["itens"].get(i, 0) > 0]) / 3))
            conteudo = 220 + linhas * 160
        scroll_max = max(0, conteudo - 400)
        scroll = max(0, min(scroll, scroll_max))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salvar_save()
                pygame.quit()
                raise SystemExit
            if evento.type == pygame.MOUSEWHEEL:
                scroll = max(0, min(scroll - evento.y * 50, scroll_max))
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if aba_skins.collidepoint(mouse):
                    aba = "SKINS"
                    scroll = 0
                elif aba_itens.collidepoint(mouse):
                    aba = "ITENS"
                    scroll = 0
                elif voltar.collidepoint(mouse):
                    return
                elif aba == "SKINS":
                    todas = [s for s in SKINS_COMPRAVEIS if s["id"] in save["compradas"]]
                    todas += [s for s in SKINS_ROLETA if s["id"] in save["compradas"]]
                    for i, skin in enumerate(todas):
                        coluna = i % 5
                        linha = i // 5
                        card = pygame.Rect(40 + coluna * 185, 215 + linha * 150 - scroll, 160, 125)
                        if card.collidepoint(mouse):
                            save["roupa_atual"] = skin["id"]
                            salvar_save()
                            break

        pygame.display.flip()
        RELOGIO.tick(FPS)


# ============================================================
# TELA DE MORTE
# ============================================================

def tela_morte():
    inicio = time.time()

    while time.time() - inicio < 1.2:

        TELA.fill((80, 20, 20))

        escrever(
            "VOCÊ MORREU!",
            330,
            230,
            55,
            BRANCO
        )

        escrever(
            "Voltando...",
            400,
            300,
            25
        )

        pygame.display.flip()
        RELOGIO.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


# ============================================================
# VITÓRIA
# ============================================================

def tela_vitoria(tempos, mortes):

    tempo_total = sum(tempos)
    mortes_total = sum(mortes)

    novo_recorde = False

    if save["melhor_tempo"] is None:
        novo_recorde = True
    elif tempo_total < save["melhor_tempo"]:
        novo_recorde = True

    if novo_recorde:
        save["melhor_tempo"] = tempo_total

        if not save["moedas_infinitas"]:
            save["moedas"] += 20

        salvar_save()

    inicio = time.time()

    while time.time() - inicio < 7:

        TELA.fill((20, 45, 30))

        escrever(
            "VOCÊ VENCEU!",
            320,
            45,
            55,
            AMARELO
        )

        escrever(
            "TEMPO TOTAL: " + f"{tempo_total:.2f}s",
            320,
            125,
            27
        )

        escrever(
            "FALHAS TOTAIS: " + str(mortes_total),
            320,
            165,
            27
        )

        if novo_recorde:
            escrever(
                "NOVO RECORDE! +20 MOEDAS",
                270,
                220,
                28,
                DOURADO
            )

        escrever(
            "TEMPOS DAS FASES",
            350,
            280,
            25
        )

        for i, tempo in enumerate(tempos):
            escrever(
                "Fase " + str(i + 1) +
                ": " + f"{tempo:.2f}s" +
                " | Falhas: " + str(mortes[i]),
                330,
                320 + i * 23,
                17
            )

        pygame.display.flip()
        RELOGIO.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


# ============================================================
# JOGO
# ============================================================

def jogar(modo):
    tempos_fases = []
    mortes_fases = []

    for numero_fase in range(1, 11):
        plataformas = criar_fase(numero_fase, modo)
        inimigos = criar_inimigos(plataformas, modo)

        primeira = plataformas[0]["rect"]
        player = pygame.Rect(primeira.centerx - 25, primeira.top - 80, 50, 80)
        velocidade_y = 0
        gravidade = 0.65
        forca_pulo_normal = -14
        forca_pulo_mola = -21
        no_chao = True
        pulos_disponiveis = 1
        coyote_tempo = 0.0
        pulo_pendente = False
        mortes = 0
        inicio_fase = time.time()
        camera_x = 0

        # Cada item funciona separadamente e os três podem ser usados na mesma partida.
        mola_possui = save["itens"].get("mola", 0) > 0
        mola_ativa = mola_possui
        jetpack_possui = save["itens"].get("mochila_jato", 0) > 0
        teleporte_possui = save["itens"].get("teleporte", 0) > 0

        jetpack_ativo = False
        jetpack_tempo = 0.0
        jetpack_recarga = 0.0
        teleporte_ativo = False
        teleporte_recarga = 0.0

        while True:
            tempo_fase = time.time() - inicio_fase
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    salvar_save()
                    pygame.quit()
                    raise SystemExit

                if evento.type == pygame.KEYDOWN:
                    # ESC abandona a partida imediatamente e volta para o lobby.
                    if evento.key == pygame.K_ESCAPE:
                        salvar_save()
                        return

                    # 1 liga/desliga a mola. Ela começa ligada e fica assim
                    # até o jogador apertar M novamente.
                    if evento.key == pygame.K_1 and mola_possui:
                        mola_ativa = not mola_ativa

                    # Q liga a mochila a jato quando a recarga terminou.
                    if evento.key == pygame.K_q and jetpack_possui and jetpack_recarga <= 0 and jetpack_tempo < 5.0:
                        jetpack_ativo = not jetpack_ativo

                    # F ativa o teleporte quando a recarga terminou.
                    if evento.key == pygame.K_f and teleporte_possui and teleporte_recarga <= 0:
                        teleporte_ativo = not teleporte_ativo

                    if evento.key == pygame.K_SPACE:
                        pulo_pendente = True

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and teleporte_ativo and teleporte_possui:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mundo_x = mouse_x + camera_x
                    dx = mundo_x - player.centerx
                    dy = mouse_y - player.centery
                    if math.sqrt(dx * dx + dy * dy) <= 500:
                        player.centerx = int(mundo_x)
                        player.centery = int(mouse_y)
                        velocidade_y = 0
                        teleporte_ativo = False
                        teleporte_recarga = 8.0

            teclas = pygame.key.get_pressed()

            # Recargas dos itens. A mola é infinita e não possui recarga.
            jetpack_recarga = max(0.0, jetpack_recarga - 1 / FPS)
            teleporte_recarga = max(0.0, teleporte_recarga - 1 / FPS)
            atualizar_plataformas_moveis(plataformas, modo)

            # Pulo mais responsivo: pequena janela de tolerância na borda.
            if no_chao:
                coyote_tempo = 0.12
            else:
                coyote_tempo = max(0.0, coyote_tempo - 1 / FPS)

            if pulo_pendente:
                if no_chao or coyote_tempo > 0:
                    velocidade_y = forca_pulo_mola if mola_ativa else forca_pulo_normal
                    no_chao = False
                    pulos_disponiveis = 1 if not save["dois_pulos"] else 2
                    pulos_disponiveis -= 1
                    coyote_tempo = 0.0
                    pulo_pendente = False
                elif save["dois_pulos"] and pulos_disponiveis > 0:
                    velocidade_y = forca_pulo_mola if mola_ativa else forca_pulo_normal
                    pulos_disponiveis -= 1
                    pulo_pendente = False

            velocidade_x = 0
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                velocidade_x = -5
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                velocidade_x = 5
            player.x += velocidade_x

            # Mochila a jato: cada uso dura até 5 segundos. Depois entra em recarga de 10s.
            if jetpack_ativo and teclas[pygame.K_SPACE] and jetpack_tempo < 5.0:
                jetpack_tempo += 1 / FPS
                velocidade_y = -5
                if jetpack_tempo >= 5.0:
                    jetpack_ativo = False
                    jetpack_tempo = 0.0
                    jetpack_recarga = 10.0
            else:
                velocidade_y += gravidade

            antigo_bottom = player.bottom
            player.y += int(velocidade_y)
            no_chao = False

            for plataforma in plataformas:
                rect = plataforma["rect"]
                if not plataforma_solida(plataforma, tempo_fase, modo):
                    continue
                if player.colliderect(rect) and antigo_bottom <= rect.top + 8 and player.bottom >= rect.top and velocidade_y >= 0:
                    player.bottom = rect.top
                    velocidade_y = 0
                    no_chao = True
                    pulos_disponiveis = 2 if save["dois_pulos"] else 1

            atualizar_inimigos(inimigos)
            morreu = False
            for inimigo in inimigos:
                inimigo_rect = pygame.Rect(int(inimigo["x"]), int(inimigo["y"]), 50, 50)
                if player.colliderect(inimigo_rect):
                    morreu = True

            lava_y = 545
            if player.bottom >= lava_y or player.top > ALTURA + 150:
                morreu = True

            if morreu:
                mortes += 1
                player.x = primeira.centerx - 25
                player.y = primeira.top - 80
                velocidade_y = 0
                no_chao = True
                camera_x = 0
                teleporte_ativo = False
                teleporte_recarga = 0.0
                jetpack_ativo = False
                jetpack_tempo = 0.0
                jetpack_recarga = 0.0
                tela_morte()
                continue

            # A câmera acompanha o jogador em TODOS os modos.
            alvo_camera = player.centerx - 350
            max_camera = max(0, plataformas[-1]["rect"].right - LARGURA + 180)
            alvo_camera = max(0, min(alvo_camera, max_camera))
            camera_x += (alvo_camera - camera_x) * 0.12

            ultima = plataformas[-1]["rect"]
            bandeira_x = ultima.right + 30
            bandeira_y = ultima.top - 70

            # Somente no EXTRA HARD, nas fases 1, 3, 5, 7 e 9,
            # a bandeira foge para o começo quando o jogador chega perto.
            if modo == "EXTRA HARD" and numero_fase in (1, 3, 5, 7, 9):
                if abs(player.centerx - bandeira_x) < 250:
                    bandeira_x = primeira.left - 30
                    bandeira_y = primeira.top - 70
            bandeira_rect = pygame.Rect(bandeira_x, bandeira_y, 50, 70)

            if player.colliderect(bandeira_rect):
                tempos_fases.append(time.time() - inicio_fase)
                mortes_fases.append(mortes)
                if not save["moedas_infinitas"]:
                    save["moedas"] += 2
                salvar_save()
                break

            TELA.fill((105, 190, 235))
            pygame.draw.circle(TELA, (255, 240, 130), (850, 80), 45)
            for cx, cy in [(150, 100), (500, 130), (800, 180)]:
                pygame.draw.circle(TELA, BRANCO, (cx, cy), 25)
                pygame.draw.circle(TELA, BRANCO, (cx + 30, cy), 30)
                pygame.draw.circle(TELA, BRANCO, (cx + 60, cy), 22)

            for plataforma in plataformas:
                rect = plataforma["rect"]
                desenhar_rect = pygame.Rect(rect.x - camera_x, rect.y, rect.width, rect.height)
                solida = plataforma_solida(plataforma, tempo_fase, modo)
                cor = VERDE_ESCURO if plataforma["tipo"] == "fixa" or solida else VERDE_CLARO
                pygame.draw.rect(TELA, cor, desenhar_rect, border_radius=7)
                pygame.draw.rect(TELA, (20, 80, 40), desenhar_rect, 2, border_radius=7)

            pygame.draw.rect(TELA, LARANJA, (0, lava_y, LARGURA, ALTURA - lava_y))
            desenhar_bandeira(bandeira_x - camera_x, bandeira_y)
            desenhar_inimigos(inimigos, camera_x)
            desenhar_personagem(TELA, player.x - camera_x, player.y, 1, save["roupa_atual"])

            escrever("FASE: " + str(numero_fase) + "/10", 20, 20, 24)
            escrever("TEMPO: " + f"{tempo_fase:.1f}s", 20, 50, 22)
            escrever("FALHAS: " + str(mortes), 20, 78, 22)
            escrever("MOEDAS: " + ("∞" if save["moedas_infinitas"] else str(save["moedas"])), 20, 108, 20, DOURADO)

            # Painel pequeno dos itens e das respectivas recargas.
            pygame.draw.rect(TELA, (30, 30, 40), (690, 15, 290, 112), border_radius=10)
            escrever("ITENS", 705, 20, 18, AMARELO)

            if mola_possui:
                estado_mola = "LIGADA" if mola_ativa else "DESLIGADA"
                escrever(f"1 MOLA: {estado_mola}", 705, 45, 16, VERDE_CLARO if mola_ativa else CINZA_CLARO)
            else:
                escrever("1 MOLA: NÃO POSSUI", 705, 45, 16, CINZA_CLARO)

            if jetpack_possui:
                if jetpack_ativo:
                    texto_jato = f"Q JATO: {max(0, 5 - jetpack_tempo):.1f}s"
                elif jetpack_recarga > 0:
                    texto_jato = f"Q JATO: RECARGA {jetpack_recarga:.1f}s"
                else:
                    texto_jato = "Q JATO: PRONTO"
                escrever(texto_jato, 705, 69, 15, VERDE_CLARO if jetpack_recarga <= 0 else CINZA_CLARO)
            else:
                escrever("Q JATO: NÃO POSSUI", 705, 69, 15, CINZA_CLARO)

            if teleporte_possui:
                if teleporte_recarga > 0:
                    texto_tp = f"F TELEPORTE: {teleporte_recarga:.1f}s"
                else:
                    texto_tp = "F TELEPORTE: PRONTO"
                escrever(texto_tp, 705, 93, 15, CIANO if teleporte_recarga <= 0 else CINZA_CLARO)
            else:
                escrever("F TELEPORTE: NÃO POSSUI", 705, 93, 15, CINZA_CLARO)

            if teleporte_ativo:
                escrever("TELEPORTE: CLIQUE EM UM DESTINO (até 500 px)", 240, 550, 18, AMARELO)
                pygame.draw.circle(TELA, BRANCO, (int(player.centerx - camera_x), int(player.centery)), 500, 1)

            pygame.display.flip()
            RELOGIO.tick(FPS)

    tela_vitoria(tempos_fases, mortes_fases)


# ============================================================
# INÍCIO
# ============================================================

if __name__ == "__main__":
    tela_conta()
    menu_principal()