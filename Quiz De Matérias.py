import tkinter as tk
import random
import os

# ============================================================
# ÁUDIO
# ============================================================

try:
    import pygame

    pygame.mixer.init()

    AUDIO_OK = True

except Exception as erro:

    AUDIO_OK = False

    print(
        "Erro ao iniciar o áudio:",
        erro
    )


PASTA_JOGO = os.path.dirname(
    os.path.abspath(__file__)
)

ARQUIVO_MUSICA = os.path.join(
    PASTA_JOGO,
    "on_on.mp3"
)


def iniciar_musica():

    if not AUDIO_OK:
        return

    if not os.path.exists(
        ARQUIVO_MUSICA
    ):
        print(
            "Coloque o arquivo on_on.mp3 "
            "na mesma pasta do jogo."
        )
        return

    try:

        pygame.mixer.music.load(
            ARQUIVO_MUSICA
        )

        pygame.mixer.music.set_volume(
            0.45
        )

        pygame.mixer.music.play(
            loops=-1
        )

    except Exception as erro:

        print(
            "Erro ao tocar música:",
            erro
        )


def parar_musica():

    if not AUDIO_OK:
        return

    try:

        pygame.mixer.music.stop()

    except:
        pass


def tocar_som_acerto():

    if not AUDIO_OK:
        return

    try:

        frequencia = 880
        duracao = 120

        pygame.mixer.Sound(
            buffer=b""
        )

    except:
        pass


# ============================================================
# PERGUNTAS
# ============================================================

PERGUNTAS = {

    "História": {

        "1º Ano": [
            ("Quem foi Pedro Álvares Cabral?",
             ["Um navegador português",
              "Um rei francês",
              "Um imperador romano",
              "Um cientista inglês"],
             0),

            ("Onde os portugueses chegaram em 1500?",
             ["Brasil",
              "Índia",
              "China",
              "Egito"],
             0),
        ],

        "2º Ano": [
            ("Qual povo construiu as pirâmides de Gizé?",
             ["Egípcios",
              "Romanos",
              "Gregos",
              "Maias"],
             0),

            ("Onde surgiu a democracia antiga?",
             ["Atenas",
              "Roma",
              "Paris",
              "Londres"],
             0),
        ],

        "3º Ano": [
            ("Quem foi conhecido como o Rei do Cangaço?",
             ["Lampião",
              "Tiradentes",
              "Dom Pedro II",
              "Getúlio Vargas"],
             0),

            ("Qual foi o primeiro imperador do Brasil?",
             ["Dom Pedro I",
              "Dom Pedro II",
              "Tiradentes",
              "Deodoro da Fonseca"],
             0),
        ],

        "4º Ano": [
            ("Em que ano aconteceu a Independência do Brasil?",
             ["1822",
              "1500",
              "1889",
              "1964"],
             0),

            ("Quem proclamou a Independência do Brasil?",
             ["Dom Pedro I",
              "Dom Pedro II",
              "Tiradentes",
              "Getúlio Vargas"],
             0),
        ],

        "5º Ano": [
            ("Em que ano foi proclamada a República do Brasil?",
             ["1889",
              "1822",
              "1500",
              "1930"],
             0),

            ("Quem proclamou a República?",
             ["Marechal Deodoro da Fonseca",
              "Dom Pedro I",
              "Tiradentes",
              "Getúlio Vargas"],
             0),
        ],

        "6º Ano": [
            ("Qual civilização criou o Coliseu?",
             ["Roma",
              "Egito",
              "China",
              "Grécia"],
             0),

            ("Qual povo criou a democracia em Atenas?",
             ["Gregos",
              "Romanos",
              "Egípcios",
              "Persas"],
             0),
        ],

        "7º Ano": [
            ("Qual acontecimento marcou o início da Revolução Francesa?",
             ["Queda da Bastilha",
              "Descobrimento do Brasil",
              "Queda de Roma",
              "Revolução Industrial"],
             0),

            ("Quem era o rei da França durante a Revolução Francesa?",
             ["Luís XVI",
              "Napoleão",
              "Carlos Magno",
              "Henrique VIII"],
             0),
        ],

        "8º Ano": [
            ("Quem foi Napoleão Bonaparte?",
             ["Imperador francês",
              "Rei português",
              "Presidente americano",
              "Filósofo grego"],
             0),

            ("Em que país começou a Revolução Industrial?",
             ["Inglaterra",
              "Brasil",
              "França",
              "Espanha"],
             0),
        ],

        "9º Ano": [
            ("Em que ano terminou a Segunda Guerra Mundial?",
             ["1945",
              "1939",
              "1918",
              "1950"],
             0),

            ("Qual organização foi criada após a Segunda Guerra Mundial?",
             ["ONU",
              "OTAN",
              "Mercosul",
              "União Europeia"],
             0),
        ],
    },


    "Geografia": {

        "1º Ano": [
            ("Qual é o maior continente?",
             ["Ásia",
              "África",
              "Europa",
              "Oceania"],
             0),

            ("Qual é o maior oceano?",
             ["Pacífico",
              "Atlântico",
              "Índico",
              "Ártico"],
             0),
        ],

        "2º Ano": [
            ("Qual é a capital do Brasil?",
             ["Brasília",
              "São Paulo",
              "Rio de Janeiro",
              "Salvador"],
             0),

            ("Qual é o maior país da América do Sul?",
             ["Brasil",
              "Argentina",
              "Chile",
              "Peru"],
             0),
        ],

        "3º Ano": [
            ("Qual é o rio mais extenso do Brasil?",
             ["Rio Amazonas",
              "Rio Paraná",
              "Rio São Francisco",
              "Rio Tietê"],
             0),

            ("Qual bioma ocupa grande parte do norte do Brasil?",
             ["Amazônia",
              "Pampa",
              "Pantanal",
              "Caatinga"],
             0),
        ],

        "4º Ano": [
            ("Quantos estados possui o Brasil?",
             ["26",
              "25",
              "27",
              "24"],
             0),

            ("Qual é a capital de Santa Catarina?",
             ["Florianópolis",
              "Joinville",
              "Blumenau",
              "Itajaí"],
             0),
        ],

        "5º Ano": [
            ("Qual é o menor estado brasileiro em área?",
             ["Sergipe",
              "Alagoas",
              "Espírito Santo",
              "Rio de Janeiro"],
             0),

            ("Qual região brasileira possui mais estados?",
             ["Nordeste",
              "Sul",
              "Sudeste",
              "Centro-Oeste"],
             0),
        ],

        "6º Ano": [
            ("O que é latitude?",
             ["Distância em relação ao Equador",
              "Distância em relação ao mar",
              "Altura de uma montanha",
              "Profundidade de um rio"],
             0),

            ("O que é longitude?",
             ["Distância em relação a Greenwich",
              "Distância do Equador",
              "Altura de uma cidade",
              "Profundidade do oceano"],
             0),
        ],

        "7º Ano": [
            ("Qual é o clima predominante na Amazônia?",
             ["Equatorial",
              "Polar",
              "Desértico",
              "Mediterrâneo"],
             0),

            ("Qual bioma é típico do Nordeste brasileiro?",
             ["Caatinga",
              "Pampa",
              "Pantanal",
              "Araucária"],
             0),
        ],

        "8º Ano": [
            ("Qual é o país mais populoso do mundo?",
             ["Índia",
              "Brasil",
              "Rússia",
              "Japão"],
             0),

            ("Qual continente possui maior população?",
             ["Ásia",
              "Europa",
              "África",
              "América"],
             0),
        ],

        "9º Ano": [
            ("O que é globalização?",
             ["Maior integração mundial",
              "Separação dos países",
              "Fim do comércio",
              "Fim das tecnologias"],
             0),

            ("Qual país possui a maior extensão territorial?",
             ["Rússia",
              "Canadá",
              "China",
              "Estados Unidos"],
             0),
        ],
    },


    "Matemática": {

        "1º Ano": [
            ("Quanto é 5 + 7?",
             ["12",
              "10",
              "11",
              "13"],
             0),

            ("Quanto é 10 - 4?",
             ["6",
              "5",
              "7",
              "8"],
             0),
        ],

        "2º Ano": [
            ("Quanto é 6 + 8?",
             ["14",
              "13",
              "15",
              "16"],
             0),

            ("Quanto é 20 - 9?",
             ["11",
              "10",
              "12",
              "13"],
             0),
        ],

        "3º Ano": [
            ("Quanto é 7 × 8?",
             ["56",
              "54",
              "48",
              "64"],
             0),

            ("Quanto é 72 ÷ 8?",
             ["9",
              "8",
              "7",
              "10"],
             0),
        ],

        "4º Ano": [
            ("Quanto é 125 + 275?",
             ["400",
              "390",
              "410",
              "450"],
             0),

            ("Quanto é 600 - 245?",
             ["355",
              "345",
              "365",
              "375"],
             0),
        ],

        "5º Ano": [
            ("Quanto é 12 × 12?",
             ["144",
              "124",
              "134",
              "154"],
             0),

            ("Quanto é 225 ÷ 15?",
             ["15",
              "10",
              "20",
              "25"],
             0),
        ],

        "6º Ano": [
            ("Quanto é 3²?",
             ["9",
              "6",
              "8",
              "12"],
             0),

            ("Qual é a metade de 50?",
             ["25",
              "20",
              "30",
              "15"],
             0),
        ],

        "7º Ano": [
            ("Quanto é 2³?",
             ["8",
              "6",
              "9",
              "12"],
             0),

            ("Quanto é 15% de 200?",
             ["30",
              "20",
              "25",
              "35"],
             0),
        ],

        "8º Ano": [
            ("Qual é o valor de x em x + 7 = 15?",
             ["8",
              "7",
              "9",
              "6"],
             0),

            ("Quanto é 3 × (4 + 2)?",
             ["18",
              "14",
              "12",
              "20"],
             0),
        ],

        "9º Ano": [
            ("Qual é a raiz quadrada de 144?",
             ["12",
              "14",
              "10",
              "16"],
             0),

            ("Quanto é 2x + 4 = 12?",
             ["4",
              "3",
              "5",
              "6"],
             0),
        ],
    },
}


# ============================================================
# LÍNGUAS
# ============================================================

PERGUNTAS_LINGUAS = {

    "Português": [

        ("Qual é o plural de 'cão'?",
         ["Cães",
          "Cãos",
          "Cãeses",
          "Cãos"],
         0),

        ("Qual palavra é um substantivo?",
         ["Casa",
          "Bonito",
          "Correr",
          "Rapidamente"],
         0),

        ("Qual é o contrário de 'alto'?",
         ["Baixo",
          "Grande",
          "Largo",
          "Forte"],
         0),

        ("Qual palavra é um verbo?",
         ["Correr",
          "Casa",
          "Azul",
          "Bonito"],
         0),

        ("Qual é o feminino de 'ator'?",
         ["Atriz",
          "Atoresa",
          "Atora",
          "Atriza"],
         0),

        ("Qual é o plural de 'papel'?",
         ["Papéis",
          "Papeis",
          "Papels",
          "Papéus"],
         0),

        ("Qual palavra é um adjetivo?",
         ["Bonito",
          "Casa",
          "Correr",
          "Ontem"],
         0),

        ("Qual é um sinônimo de 'feliz'?",
         ["Alegre",
          "Triste",
          "Bravo",
          "Cansado"],
         0),

        ("Qual é o contrário de 'rápido'?",
         ["Lento",
          "Forte",
          "Alto",
          "Grande"],
         0),

        ("Qual é o plural de 'flor'?",
         ["Flores",
          "Flors",
          "Florais",
          "Flore"],
         0),
    ],


    "Inglês": [

        ("O que significa 'house'?",
         ["Casa",
          "Carro",
          "Escola",
          "Livro"],
         0),

        ("O que significa 'dog'?",
         ["Cachorro",
          "Gato",
          "Pássaro",
          "Cavalo"],
         0),

        ("Como se diz 'azul' em inglês?",
         ["Blue",
          "Red",
          "Green",
          "Yellow"],
         0),

        ("Como se diz 'obrigado' em inglês?",
         ["Thank you",
          "Goodbye",
          "Hello",
          "Please"],
         0),

        ("O que significa 'book'?",
         ["Livro",
          "Caneta",
          "Mesa",
          "Caderno"],
         0),

        ("Como se diz 'água' em inglês?",
         ["Water",
          "Fire",
          "Earth",
          "Air"],
         0),

        ("O que significa 'school'?",
         ["Escola",
          "Hospital",
          "Casa",
          "Mercado"],
         0),

        ("Como se diz 'vermelho' em inglês?",
         ["Red",
          "Blue",
          "White",
          "Black"],
         0),

        ("O que significa 'friend'?",
         ["Amigo",
          "Irmão",
          "Professor",
          "Pai"],
         0),

        ("Como se diz 'bom dia' em inglês?",
         ["Good morning",
          "Good night",
          "Goodbye",
          "Good afternoon"],
         0),
    ],


    "Latim": [

        ("O que significa 'aqua'?",
         ["Água",
          "Terra",
          "Fogo",
          "Ar"],
         0),

        ("O que significa 'terra'?",
         ["Terra",
          "Água",
          "Casa",
          "Sol"],
         0),

        ("O que significa 'amicus'?",
         ["Amigo",
          "Inimigo",
          "Professor",
          "Rei"],
         0),

        ("O que significa 'vita'?",
         ["Vida",
          "Morte",
          "Casa",
          "Livro"],
         0),

        ("O que significa 'luna'?",
         ["Lua",
          "Sol",
          "Estrela",
          "Terra"],
         0),

        ("O que significa 'sol'?",
         ["Sol",
          "Lua",
          "Céu",
          "Mar"],
         0),

        ("O que significa 'rex'?",
         ["Rei",
          "Soldado",
          "Cidadão",
          "Professor"],
         0),

        ("O que significa 'mater'?",
         ["Mãe",
          "Pai",
          "Filha",
          "Irmã"],
         0),

        ("O que significa 'pater'?",
         ["Pai",
          "Mãe",
          "Irmão",
          "Filho"],
         0),

        ("O que significa 'bonus'?",
         ["Bom",
          "Grande",
          "Rápido",
          "Forte"],
         0),
    ],


    "Espanhol": [

        ("O que significa 'casa'?",
         ["Casa",
          "Carro",
          "Escola",
          "Livro"],
         0),

        ("O que significa 'perro'?",
         ["Cachorro",
          "Gato",
          "Cavalo",
          "Pássaro"],
         0),

        ("Como se diz 'vermelho' em espanhol?",
         ["Rojo",
          "Azul",
          "Verde",
          "Amarillo"],
         0),

        ("O que significa 'agua'?",
         ["Água",
          "Fogo",
          "Terra",
          "Ar"],
         0),

        ("Como se diz 'amigo' em espanhol?",
         ["Amigo",
          "Hermano",
          "Padre",
          "Maestro"],
         0),

        ("O que significa 'escuela'?",
         ["Escola",
          "Casa",
          "Igreja",
          "Mercado"],
         0),

        ("Como se diz 'obrigado' em espanhol?",
         ["Gracias",
          "Hola",
          "Adiós",
          "Buenos días"],
         0),

        ("O que significa 'libro'?",
         ["Livro",
          "Caneta",
          "Mesa",
          "Caderno"],
         0),

        ("Como se diz 'bom dia' em espanhol?",
         ["Buenos días",
          "Buenas noches",
          "Hola",
          "Adiós"],
         0),

        ("O que significa 'feliz'?",
         ["Feliz",
          "Triste",
          "Bravo",
          "Cansado"],
         0),
    ],


    "Italiano": [

        ("O que significa 'casa' em italiano?",
         ["Casa",
          "Carro",
          "Escola",
          "Livro"],
         0),

        ("Como se diz 'obrigado' em italiano?",
         ["Grazie",
          "Ciao",
          "Prego",
          "Buongiorno"],
         0),

        ("O que significa 'ciao'?",
         ["Olá/Tchau",
          "Obrigado",
          "Casa",
          "Amigo"],
         0),

        ("Como se diz 'água' em italiano?",
         ["Acqua",
          "Fuoco",
          "Terra",
          "Aria"],
         0),

        ("O que significa 'amico'?",
         ["Amigo",
          "Pai",
          "Irmão",
          "Professor"],
         0),

        ("Como se diz 'bom dia' em italiano?",
         ["Buongiorno",
          "Buonanotte",
          "Grazie",
          "Ciao"],
         0),

        ("O que significa 'libro'?",
         ["Livro",
          "Casa",
          "Mesa",
          "Escola"],
         0),

        ("Como se diz 'vermelho' em italiano?",
         ["Rosso",
          "Blu",
          "Verde",
          "Giallo"],
         0),

        ("O que significa 'famiglia'?",
         ["Família",
          "Amigo",
          "Escola",
          "Cidade"],
         0),

        ("Como se diz 'sim' em italiano?",
         ["Sì",
          "No",
          "Ciao",
          "Grazie"],
         0),
    ],
}


# ============================================================
# CONFIGURAÇÕES
# ============================================================

TEMPO_INICIAL = 12
TEMPO_COM_RELOGIO = 17

CUSTO_DICA = 10
CUSTO_RELOGIO = 5

TOTAL_PERGUNTAS = 10

TEMPO_RESPOSTA_GRUPO = 3


# ============================================================
# VARIÁVEIS
# ============================================================

modo = None
materia = None
ano = None

pergunta_atual = None

numero_pergunta = 0
pontuacao = 0
moedas = 0

tempo_restante = TEMPO_INICIAL

timer_id = None
proximo_id = None

dica_usada = False
relogio_usado = False
respondida = False

perguntas_usadas = {}

botoes_resposta = []

correta_atual = 0

animacao_resposta_id = None
animacao_resposta_estado = False

overlay_resposta = None


# ============================================================
# JANELA
# ============================================================

root = tk.Tk()

root.title(
    "O Super Quiz"
)

root.geometry(
    "1100x700"
)

root.minsize(
    800,
    600
)

root.configure(
    bg="#101522"
)

fullscreen = False


# ============================================================
# FULLSCREEN
# ============================================================

def alternar_fullscreen(event=None):

    global fullscreen

    fullscreen = not fullscreen

    root.attributes(
        "-fullscreen",
        fullscreen
    )


root.bind(
    "<F11>",
    alternar_fullscreen
)


# ============================================================
# ESC VOLTA AO MENU
# ============================================================

def tecla_escape(event=None):

    parar_musica()

    menu_principal()


root.bind(
    "<Escape>",
    tecla_escape
)


# ============================================================
# LIMPAR TELA
# ============================================================

def limpar_tela():

    global timer_id
    global proximo_id
    global animacao_resposta_id
    global overlay_resposta

    if timer_id is not None:

        try:
            root.after_cancel(
                timer_id
            )
        except:
            pass

        timer_id = None

    if proximo_id is not None:

        try:
            root.after_cancel(
                proximo_id
            )
        except:
            pass

        proximo_id = None

    if animacao_resposta_id is not None:

        try:
            root.after_cancel(
                animacao_resposta_id
            )
        except:
            pass

        animacao_resposta_id = None

    parar_musica()

    if overlay_resposta is not None:

        try:
            overlay_resposta.destroy()
        except:
            pass

        overlay_resposta = None

    for widget in root.winfo_children():

        widget.destroy()


# ============================================================
# BOTÃO PADRÃO
# ============================================================

def criar_botao(
    parent,
    texto,
    comando,
    largura=20
):

    return tk.Button(
        parent,
        text=texto,
        command=comando,
        font=(
            "Arial",
            16,
            "bold"
        ),
        bg="#24304A",
        fg="white",
        activebackground="#35466B",
        activeforeground="white",
        relief="flat",
        bd=0,
        width=largura,
        height=2,
        cursor="hand2"
    )


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():

    global modo

    limpar_tela()

    modo = None

    titulo = tk.Label(
        root,
        text="🎮 O Super Quiz",
        font=(
            "Arial",
            42,
            "bold"
        ),
        bg="#101522",
        fg="#65E6FF"
    )

    titulo.pack(
        pady=(70, 20)
    )

    subtitulo = tk.Label(
        root,
        text="Escolha o modo de jogo",
        font=(
            "Arial",
            20
        ),
        bg="#101522",
        fg="white"
    )

    subtitulo.pack(
        pady=20
    )

    botao_individual = criar_botao(
        root,
        "👤 Modo Individual",
        escolher_materia,
        25
    )

    botao_individual.pack(
        pady=12
    )

    botao_grupo = criar_botao(
        root,
        "👥 Modo Grupo",
        escolher_materia_grupo,
        25
    )

    botao_grupo.pack(
        pady=12
    )


# ============================================================
# ESCOLHER MATÉRIA
# ============================================================

def escolher_materia():

    global modo

    modo = "individual"

    tela_materias()


def escolher_materia_grupo():

    global modo

    modo = "grupo"

    tela_materias()


def tela_materias():

    limpar_tela()

    titulo = tk.Label(
        root,
        text="📚 Escolha a matéria",
        font=(
            "Arial",
            32,
            "bold"
        ),
        bg="#101522",
        fg="white"
    )

    titulo.pack(
        pady=40
    )

    frame = tk.Frame(
        root,
        bg="#101522"
    )

    frame.pack()

    materias = [
        "História",
        "Geografia",
        "Matemática",
        "Línguas"
    ]

    for i, nome in enumerate(
        materias
    ):

        botao = criar_botao(
            frame,
            nome,
            lambda n=nome:
                escolher_materia_nome(n),
            18
        )

        botao.grid(
            row=i // 2,
            column=i % 2,
            padx=15,
            pady=15
        )

    voltar = criar_botao(
        root,
        "⬅ Voltar",
        menu_principal,
        15
    )

    voltar.pack(
        pady=30
    )


def escolher_materia_nome(nome):

    global materia

    materia = nome

    if nome == "Línguas":

        escolher_lingua()

    else:

        escolher_ano()


# ============================================================
# LÍNGUAS
# ============================================================

def escolher_lingua():

    limpar_tela()

    titulo = tk.Label(
        root,
        text="🌎 Escolha a língua",
        font=(
            "Arial",
            32,
            "bold"
        ),
        bg="#101522",
        fg="white"
    )

    titulo.pack(
        pady=40
    )

    frame = tk.Frame(
        root,
        bg="#101522"
    )

    frame.pack()

    linguas = [
        "Português",
        "Inglês",
        "Latim",
        "Espanhol",
        "Italiano"
    ]

    for i, lingua in enumerate(
        linguas
    ):

        botao = criar_botao(
            frame,
            lingua,
            lambda n=lingua:
                escolher_lingua_nome(n),
            18
        )

        botao.grid(
            row=i // 2,
            column=i % 2,
            padx=15,
            pady=15
        )

    voltar = criar_botao(
        root,
        "⬅ Voltar",
        tela_materias,
        15
    )

    voltar.pack(
        pady=30
    )


def escolher_lingua_nome(nome):

    global materia
    global ano

    materia = nome

    ano = "Língua"

    iniciar_jogo()


# ============================================================
# ESCOLHER ANO
# ============================================================

def escolher_ano():

    limpar_tela()

    titulo = tk.Label(
        root,
        text="🎓 Escolha o ano",
        font=(
            "Arial",
            32,
            "bold"
        ),
        bg="#101522",
        fg="white"
    )

    titulo.pack(
        pady=35
    )

    frame = tk.Frame(
        root,
        bg="#101522"
    )

    frame.pack()

    anos = [
        "1º Ano",
        "2º Ano",
        "3º Ano",
        "4º Ano",
        "5º Ano",
        "6º Ano",
        "7º Ano",
        "8º Ano",
        "9º Ano"
    ]

    for i, nome in enumerate(
        anos
    ):

        botao = criar_botao(
            frame,
            nome,
            lambda n=nome:
                escolher_ano_nome(n),
            15
        )

        botao.grid(
            row=i // 3,
            column=i % 3,
            padx=10,
            pady=10
        )

    voltar = criar_botao(
        root,
        "⬅ Voltar",
        tela_materias,
        15
    )

    voltar.pack(
        pady=25
    )


def escolher_ano_nome(nome):

    global ano

    ano = nome

    iniciar_jogo()


# ============================================================
# INICIAR JOGO
# ============================================================

def iniciar_jogo():

    global numero_pergunta
    global pontuacao

    numero_pergunta = 0
    pontuacao = 0

    mostrar_pergunta()


# ============================================================
# PEGAR BANCO DE PERGUNTAS
# ============================================================

def obter_perguntas():

    if materia == "Línguas":

        return PERGUNTAS_LINGUAS.get(
            materia,
            []
        )

    return PERGUNTAS.get(
        materia,
        {}
    ).get(
        ano,
        []
    )


# ============================================================
# PEGAR PERGUNTA SEM REPETIR
# ============================================================

def pegar_pergunta():

    chave = (
        materia,
        ano
    )

    banco = obter_perguntas()

    if not banco:

        return (
            "Pergunta de teste",
            [
                "Alternativa A",
                "Alternativa B",
                "Alternativa C",
                "Alternativa D"
            ],
            0
        )

    if chave not in perguntas_usadas:

        perguntas_usadas[chave] = []

    disponiveis = [
        i
        for i in range(
            len(banco)
        )
        if i not in perguntas_usadas[chave]
    ]

    if not disponiveis:

        perguntas_usadas[chave] = []

        disponiveis = list(
            range(
                len(banco)
            )
        )

    indice = random.choice(
        disponiveis
    )

    perguntas_usadas[chave].append(
        indice
    )

    return banco[indice]


# ============================================================
# MOSTRAR PERGUNTA
# ============================================================

def mostrar_pergunta():

    global pergunta_atual
    global numero_pergunta
    global tempo_restante
    global dica_usada
    global relogio_usado
    global respondida
    global botoes_resposta
    global correta_atual

    limpar_tela()

    if numero_pergunta >= TOTAL_PERGUNTAS:

        finalizar_jogo()

        return

    dica_usada = False
    relogio_usado = False
    respondida = False

    tempo_restante = TEMPO_INICIAL

    pergunta_atual = pegar_pergunta()

    texto_pergunta = pergunta_atual[0]
    alternativas = pergunta_atual[1]
    indice_correto_original = pergunta_atual[2]

    alternativas_com_indices = list(
        enumerate(alternativas)
    )

    random.shuffle(
        alternativas_com_indices
    )

    alternativas_novas = [
        item[1]
        for item in alternativas_com_indices
    ]

    correta_atual = next(
        i
        for i, item in enumerate(
            alternativas_com_indices
        )
        if item[0] == indice_correto_original
    )

    # ========================================================
    # TOPO
    # ========================================================

    topo = tk.Frame(
        root,
        bg="#101522"
    )

    topo.pack(
        fill="x",
        padx=25,
        pady=15
    )

    label_pergunta = tk.Label(
        topo,
        text=(
            f"Pergunta "
            f"{numero_pergunta + 1}"
            f"/{TOTAL_PERGUNTAS}"
        ),
        font=(
            "Arial",
            18,
            "bold"
        ),
        bg="#101522",
        fg="white"
    )

    label_pergunta.pack(
        side="left"
    )

    label_materia = tk.Label(
        topo,
        text=f"{materia} • {ano}",
        font=(
            "Arial",
            18,
            "bold"
        ),
        bg="#101522",
        fg="#A9C7FF"
    )

    label_materia.pack(
        side="left",
        padx=30
    )

    label_moedas = tk.Label(
        topo,
        text=f"🪙 {moedas}",
        font=(
            "Arial",
            18,
            "bold"
        ),
        bg="#101522",
        fg="#FFD54A"
    )

    label_moedas.pack(
        side="right"
    )

    # ========================================================
    # TIMER
    # ========================================================

    label_tempo = tk.Label(
        root,
        text=f"⏱ {tempo_restante}s",
        font=(
            "Arial",
            30,
            "bold"
        ),
        bg="#101522",
        fg="#55DD77"
    )

    label_tempo.pack(
        pady=5
    )

    root.label_tempo = label_tempo

    # ========================================================
    # PERGUNTA
    # ========================================================

    label_questao = tk.Label(
        root,
        text=texto_pergunta,
        font=(
            "Arial",
            24,
            "bold"
        ),
        bg="#101522",
        fg="white",
        wraplength=900,
        justify="center"
    )

    label_questao.pack(
        pady=25
    )

    # ========================================================
    # BOTÕES
    # ========================================================

    frame_respostas = tk.Frame(
        root,
        bg="#101522"
    )

    frame_respostas.pack(
        fill="x",
        padx=100
    )

    botoes_resposta = []

    letras = [
        "A",
        "B",
        "C",
        "D"
    ]

    for i in range(4):

        botao = tk.Button(
            frame_respostas,
            text=(
                f"{letras[i]}) "
                f"{alternativas_novas[i]}"
            ),
            command=lambda x=i:
                responder(x),
            font=(
                "Arial",
                17,
                "bold"
            ),
            bg="#24304A",
            fg="white",
            activebackground="#35466B",
            activeforeground="white",
            relief="flat",
            bd=0,
            height=2,
            cursor="hand2"
        )

        botao.grid(
            row=i // 2,
            column=i % 2,
            sticky="ew",
            padx=8,
            pady=8
        )

        botoes_resposta.append(
            botao
        )

    frame_respostas.grid_columnconfigure(
        0,
        weight=1
    )

    frame_respostas.grid_columnconfigure(
        1,
        weight=1
    )

    # ========================================================
    # FEEDBACK
    # ========================================================

    label_feedback = tk.Label(
        root,
        text="",
        font=(
            "Arial",
            18,
            "bold"
        ),
        bg="#101522",
        fg="white"
    )

    label_feedback.pack(
        pady=12
    )

    root.label_feedback = label_feedback

    # ========================================================
    # AJUDAS INDIVIDUAIS
    # ========================================================

    if modo == "individual":

        frame_ajuda = tk.Frame(
            root,
            bg="#101522"
        )

        frame_ajuda.pack(
            pady=5
        )

        botao_dica = tk.Button(
            frame_ajuda,
            text="🔦 Dica - 10 🪙",
            command=usar_dica,
            font=(
                "Arial",
                14,
                "bold"
            ),
            bg="#7A5C00",
            fg="white",
            activebackground="#9B7600",
            relief="flat",
            width=18,
            height=2
        )

        botao_dica.grid(
            row=0,
            column=0,
            padx=8
        )

        botao_relogio = tk.Button(
            frame_ajuda,
            text="⏰ +5 segundos - 5 🪙",
            command=usar_relogio,
            font=(
                "Arial",
                14,
                "bold"
            ),
            bg="#155B7A",
            fg="white",
            activebackground="#1D789F",
            relief="flat",
            width=20,
            height=2
        )

        botao_relogio.grid(
            row=0,
            column=1,
            padx=8
        )

    # ========================================================
    # MODO GRUPO
    # ========================================================

    else:

        for botao in botoes_resposta:

            botao.config(
                state="disabled",
                cursor="arrow"
            )

    # ========================================================
    # MÚSICA
    # ========================================================

    iniciar_musica()

    atualizar_tempo()


# ============================================================
# ATUALIZAR TEMPO
# ============================================================

def atualizar_tempo():

    global tempo_restante
    global timer_id

    if respondida:

        return

    if tempo_restante <= 0:

        tempo_esgotado()

        return

    if tempo_restante <= 4:

        root.label_tempo.config(
            fg="#FF4D4D"
        )

    elif tempo_restante <= 7:

        root.label_tempo.config(
            fg="#FFD54A"
        )

    else:

        root.label_tempo.config(
            fg="#55DD77"
        )

    root.label_tempo.config(
        text=f"⏱ {tempo_restante}s"
    )

    tempo_restante -= 1

    timer_id = root.after(
        1000,
        atualizar_tempo
    )


# ============================================================
# RESPONDER
# ============================================================

def responder(indice):

    global pontuacao
    global moedas
    global respondida
    global numero_pergunta
    global proximo_id

    if respondida:

        return

    respondida = True

    parar_musica()

    for botao in botoes_resposta:

        botao.config(
            state="disabled"
        )

    texto_correto = (
        botoes_resposta[
            correta_atual
        ].cget("text")
    )

    if len(texto_correto) > 3:

        texto_correto = texto_correto[3:]

    if indice == correta_atual:

        pontuacao += 1

        moedas += 1

        botoes_resposta[
            indice
        ].config(
            bg="#168A3A",
            fg="white"
        )

        tocar_som_acerto()

        mostrar_resposta_no_centro(
            texto_correto
        )

        numero_pergunta += 1

        proximo_id = root.after(
            1800,
            mostrar_pergunta
        )

    else:

        botoes_resposta[
            indice
        ].config(
            bg="#B52B2B",
            fg="white"
        )

        botoes_resposta[
            correta_atual
        ].config(
            bg="#168A3A",
            fg="white"
        )

        root.label_feedback.config(
            text=(
                "✗ ERRADO!\n"
                f"Resposta correta: "
                f"{texto_correto}"
            ),
            fg="#FF6666"
        )

        numero_pergunta += 1

        proximo_id = root.after(
            1400,
            mostrar_pergunta
        )


# ============================================================
# TEMPO ESGOTADO
# ============================================================

def tempo_esgotado():

    global respondida

    if respondida:

        return

    respondida = True

    parar_musica()

    for botao in botoes_resposta:

        botao.config(
            state="disabled"
        )

    if modo == "grupo":

        revelar_resposta_grupo()

    else:

        texto_correto = (
            botoes_resposta[
                correta_atual
            ].cget("text")
        )

        if len(texto_correto) > 3:

            texto_correto = texto_correto[3:]

        botoes_resposta[
            correta_atual
        ].config(
            bg="#168A3A",
            fg="white"
        )

        root.label_feedback.config(
            text=(
                "⏰ TEMPO ESGOTADO!\n"
                f"Resposta correta: "
                f"{texto_correto}"
            ),
            fg="#FFD54A"
        )

        root.after(
            1800,
            mostrar_pergunta
        )


# ============================================================
# RESPOSTA DO MODO GRUPO
# ============================================================

def revelar_resposta_grupo():

    global numero_pergunta

    parar_musica()

    tocar_som_acerto()

    texto_resposta = (
        botoes_resposta[
            correta_atual
        ].cget("text")
    )

    if len(texto_resposta) > 3:

        texto_resposta = texto_resposta[3:]

    botoes_resposta[
        correta_atual
    ].config(
        bg="#168A3A",
        fg="white",
        font=(
            "Arial",
            23,
            "bold"
        ),
        height=2
    )

    for botao in botoes_resposta:

        botao.config(
            state="disabled"
        )

    mostrar_resposta_no_centro(
        texto_resposta,
        texto_personalizado=(
            'A resposta certa é:\n\n'
            f'"{texto_resposta}"'
        )
    )

    numero_pergunta += 1

    agendar_proxima_pergunta(
        TEMPO_RESPOSTA_GRUPO * 1000
    )


# ============================================================
# MOSTRAR RESPOSTA NO CENTRO
# ============================================================

def mostrar_resposta_no_centro(
    texto_resposta,
    texto_personalizado=None
):

    global overlay_resposta

    if overlay_resposta is not None:

        try:
            overlay_resposta.destroy()
        except:
            pass

    overlay_resposta = tk.Frame(
        root,
        bg="#101522"
    )

    overlay_resposta.place(
        relx=0.5,
        rely=0.50,
        anchor="center",
        relwidth=0.90,
        relheight=0.50
    )

    texto = (
        texto_personalizado
        if texto_personalizado
        else (
            "✓ CORRETO!\n\n"
            f"{texto_resposta}"
        )
    )

    label = tk.Label(
        overlay_resposta,
        text=texto,
        font=(
            "Arial",
            38,
            "bold"
        ),
        fg="#65E86A",
        bg="#101522",
        justify="center"
    )

    label.pack(
        expand=True
    )

    overlay_resposta.label = label

    piscar_resposta_correta()


# ============================================================
# PISCAR RESPOSTA
# ============================================================

def piscar_resposta_correta():

    global animacao_resposta_id
    global animacao_resposta_estado

    if overlay_resposta is None:

        return

    try:

        animacao_resposta_estado = (
            not animacao_resposta_estado
        )

        if animacao_resposta_estado:

            overlay_resposta.config(
                bg="#103A20"
            )

            overlay_resposta.label.config(
                fg="#00FF44",
                bg="#103A20"
            )

        else:

            overlay_resposta.config(
                bg="#101522"
            )

            overlay_resposta.label.config(
                fg="#65E86A",
                bg="#101522"
            )

        animacao_resposta_id = root.after(
            180,
            piscar_resposta_correta
        )

    except:

        pass


# ============================================================
# AGENDAR PRÓXIMA
# ============================================================

def agendar_proxima_pergunta(
    tempo
):

    global proximo_id

    proximo_id = root.after(
        tempo,
        mostrar_pergunta
    )


# ============================================================
# DICA
# ============================================================

def usar_dica():

    global moedas
    global dica_usada

    if dica_usada:

        return

    if moedas < CUSTO_DICA:

        root.label_feedback.config(
            text="Você não tem moedas suficientes!",
            fg="#FF6666"
        )

        return

    moedas -= CUSTO_DICA

    dica_usada = True

    erradas = [
        i
        for i in range(4)
        if i != correta_atual
    ]

    eliminar = random.choice(
        erradas
    )

    botoes_resposta[
        eliminar
    ].config(
        state="disabled",
        bg="#161C29",
        fg="#555B68",
        text="❌ Eliminada"
    )

    root.label_feedback.config(
        text="🔦 Dica usada!",
        fg="#FFD54A"
    )


# ============================================================
# +5 SEGUNDOS
# ============================================================

def usar_relogio():

    global moedas
    global relogio_usado
    global tempo_restante

    if relogio_usado:

        return

    if moedas < CUSTO_RELOGIO:

        root.label_feedback.config(
            text="Você não tem moedas suficientes!",
            fg="#FF6666"
        )

        return

    moedas -= CUSTO_RELOGIO

    relogio_usado = True

    tempo_restante = TEMPO_COM_RELOGIO

    root.label_tempo.config(
        text=f"⏱ {tempo_restante}s",
        fg="#55DD77"
    )

    root.label_feedback.config(
        text="⏰ +5 segundos!",
        fg="#55DD77"
    )


# ============================================================
# FINALIZAR JOGO
# ============================================================

def finalizar_jogo():

    limpar_tela()

    titulo = tk.Label(
        root,
        text="🏆 Fim do jogo!",
        font=(
            "Arial",
            38,
            "bold"
        ),
        bg="#101522",
        fg="#FFD54A"
    )

    titulo.pack(
        pady=50
    )

    resultado = tk.Label(
        root,
        text=(
            f"Pontuação: "
            f"{pontuacao}/{TOTAL_PERGUNTAS}\n\n"
            f"🪙 Moedas: {moedas}"
        ),
        font=(
            "Arial",
            25,
            "bold"
        ),
        bg="#101522",
        fg="white",
        justify="center"
    )

    resultado.pack(
        pady=20
    )

    jogar_novamente = criar_botao(
        root,
        "🔄 Jogar novamente",
        iniciar_jogo,
        22
    )

    jogar_novamente.pack(
        pady=10
    )

    menu = criar_botao(
        root,
        "🏠 Menu principal",
        menu_principal,
        22
    )

    menu.pack(
        pady=10
    )


# ============================================================
# INICIAR
# ============================================================

menu_principal()

root.mainloop()
