import pygame
import sys
import random
import time
import string
import requests
from bs4 import BeautifulSoup
import os
import json
from interface import (
    desenhar_menu,
    desenhar_config,
    desenhar_placar,
    desenhar_dificuldade,
    desenhar_carregando_palavra,
    desenhar_carregando_palavra_animado,
    desenhar_tela_final,
    desenhar_jogo,
    desenhar_nome_solo,
    desenhar_config_multiplayer_config,
    desenhar_config_multiplayer_nomes,
    desenhar_espera_multiplayer,
    desenhar_definir_palavra_multiplayer
)
import difflib
import math

# Definir diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Inicialização do Pygame
pygame.init()

# Inicialização do mixer de áudio (deve vir antes de usar sons)
pygame.mixer.init()

# Carregar efeitos sonoros logo após inicialização
try:
    SOM_ACERTO = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sons', 'acerto_letra.wav'))
    SOM_ERRO = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sons', 'erro_letra.wav'))
    SOM_INICIAR = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sons', 'iniciar_rodada.wav'))
    SOM_FIM = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sons', 'fim_jogo.wav'))
    SOM_VITORIA = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sons', 'vitoria_palavra.wav'))
    SOM_CLIQUE = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sons', 'teclado.wav'))
except pygame.error as e:
    print(f"Erro ao carregar sons: {e}")
    # Criar sons vazios como fallback
    SOM_ACERTO = SOM_ERRO = SOM_INICIAR = SOM_FIM = SOM_VITORIA = SOM_CLIQUE = None

# Música de fundo
MUSICA_MENU_PATH = os.path.join(BASE_DIR, 'sons', 'musica_menu.mp3')

# Configurações de tela
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Jogo de Adivinhação de Palavras - Pygame")
# Maximizar a janela ao iniciar (opcional, depende do SO)
try:
    pygame.display.toggle_fullscreen()
except Exception:
    pass
WIDTH, HEIGHT = screen.get_size()

# Cores (paleta semelhante ao seu jogo)
COR_FUNDO_PRINCIPAL = (249, 235, 199)
COR_TEXTO_CLARO = (95, 111, 82)
COR_TEXTO_CLARO_DESTACADO = (196, 102, 31)
COR_BOTAO = (169, 179, 136)
COR_BOTAO_HOVER = (185, 148, 112)
COR_BOTAO_TEXTO = (60, 60, 60)

# Cores para letras
COR_LETRA_PADRAO = (210, 180, 140)  # marrom claro
COR_LETRA_ACERTADA = (60, 180, 75)  # verde
COR_LETRA_BORDA = (185, 148, 112)
COR_LETRA_TEXTO = (255, 255, 255)  # branco

# Fontes
FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# Estados de tela
TELA_MENU = "menu"
TELA_JOGO = "jogo"
TELA_CONFIG = "config"
TELA_PLACAR = "placar"
TELA_NOME_SOLO = "nome_solo"
TELA_DIFICULDADE = "dificuldade"

tela_atual = TELA_MENU

# Variáveis de estado
nome_jogador = ""
input_ativo = False
input_rect = pygame.Rect(WIDTH//2 - 180, 300, 360, 60)
cor_input_inativo = (230, 226, 195)
cor_input_ativo = (255, 255, 255)
cor_input_borda = (185, 148, 112)

# Variáveis globais da rodada
palavra_original = ""
palavra_embaralhada = ""
letras_adivinhadas = []
indice_atual = 0
nome_jogador_exemplo = ""
tempo_exemplo = 0.0
erros_exemplo = 0

# Adicionar variáveis de estado para o modo solo
rodada_ativa = False
inicio_tempo = 0.0
fim_rodada = False
mensagem_final = ""
venceu_rodada = False

PENALIDADE_ERRO = 3.0

letras_tentadas = set()
letras_erradas = set()
feedback_erro_idx = -1
feedback_erro_timer = 0
FEEDBACK_ERRO_DURATION = 350  # ms

# Adicione variáveis globais para o feedback do círculo
feedback_erro_circulo_idx = -1
feedback_erro_circulo_timer = 0

# Variáveis de controle de estado global
som_iniciar_tocou = False
som_fim_tocou = False
fim_rodada_anterior = False
rodada_finalizada = False
mensagem_config = ""
mensagem_timer = 0

# Dicionário de palavras por dificuldade

def embaralhar_palavra(palavra):
    letras = list(palavra)
    random.shuffle(letras)
    return "".join(letras)

# Função para carregar dicionario de arquivo

def carregar_dicionario_arquivo():
    caminho_dic = "pt_BR.dic"
    palavras = []
    if os.path.exists(caminho_dic):
        try:
            with open(caminho_dic, "r", encoding="utf-8") as f:
                for linha in f:
                    palavra = linha.strip().lower()
                    if not palavra or not palavra.isalpha():
                        continue
                    if '/' in palavra:
                        palavra = palavra.split('/')[0]
                    if 4 <= len(palavra) <= 20:
                        palavras.append(palavra.upper())
        except (FileNotFoundError, UnicodeDecodeError, IOError) as e:
            print(f"Erro ao carregar dicionário {caminho_dic}: {e}")
    return palavras

# Carregar dicionário ao iniciar
import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_PALAVRAS_JSON = os.path.join(BASE_DIR, "palavras.json")

# Definir caminhos de arquivos essenciais
PALAVRAS_USADAS_PATH = os.path.join(BASE_DIR, 'palavras_usadas.json')
CONFIG_PATH = os.path.join(BASE_DIR, 'configuracoes.json')
if os.path.exists(ARQUIVO_PALAVRAS_JSON):
    with open(ARQUIVO_PALAVRAS_JSON, "r", encoding="utf-8") as f:
        palavras_dicionario = json.load(f)
    print("Usando palavras do arquivo palavras.json!")
else:
    raise FileNotFoundError(f"Arquivo de palavras não encontrado! Esperado em: {ARQUIVO_PALAVRAS_JSON}")

# Carregar dicionário de palavras mais buscadas, se existir
ARQUIVO_MAIS_BUSCADAS = "palavras_mais_buscadas_dificuldade.json"
use_simplified_validation = False
if os.path.exists(ARQUIVO_MAIS_BUSCADAS):
    with open(ARQUIVO_MAIS_BUSCADAS, "r", encoding="utf-8") as f:
        palavras_dicionario = json.load(f)
    print("Usando palavras do arquivo palavras_mais_buscadas_dificuldade.json!")
    # Desabilitar validação Dicio para essas palavras
    use_simplified_validation = True
else:
    # ... manter carregamento do pt_BR.dic e função tem_definicao_dicio original ...
    pass

# Adicione no início do arquivo:
def carregar_dicionario_existente(nome_arquivo=None):
    return set()
def adicionar_palavra_ao_dicionario(palavra, nome_arquivo=None):
    pass
dicionario_multiplayer = set()
for lista in palavras_dicionario.values():
    dicionario_multiplayer.update(p.upper() for p in lista)

# Botão utilitário
class Botao:
    def __init__(self, texto, x, y, w, h, callback):
        self.texto = texto
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.hover = False
    def desenhar(self, surface):
        cor = COR_BOTAO_HOVER if self.hover else COR_BOTAO
        pygame.draw.rect(surface, cor, self.rect, border_radius=12)
        label = FONT_MED.render(self.texto, True, COR_BOTAO_TEXTO)
        surface.blit(label, (self.rect.x + (self.rect.w - label.get_width())//2, self.rect.y + (self.rect.h - label.get_height())//2))
    def checar_evento(self, evento):
        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.callback()

# Funções de troca de tela

def ir_para_jogo():
    global tela_atual
    tela_atual = TELA_JOGO

def ir_para_config():
    global tela_atual
    tela_atual = TELA_CONFIG

def ir_para_placar():
    global tela_atual
    tela_atual = TELA_PLACAR

def voltar_menu():
    global tela_atual
    tela_atual = TELA_MENU

def sair():
    pygame.quit()
    sys.exit()

def ir_para_nome_solo():
    global tela_atual, nome_jogador, input_ativo, cursor_timer, cursor_visible
    nome_jogador = ""
    input_ativo = True  # Foco automático
    tela_atual = TELA_NOME_SOLO
    cursor_timer = 0
    cursor_visible = True

# Variáveis para cursor piscando
cursor_timer = 0
cursor_visible = True
CURSOR_BLINK_INTERVAL = 500  # ms

# Atualizar input_rect para novo y
input_rect.y = 240

# Botões do menu
botoes_menu = [
    Botao("Iniciar Jogo Solo", WIDTH//2 - 180, 220, 360, 60, ir_para_nome_solo),
    Botao("Iniciar Jogo Multiplayer", WIDTH//2 - 180, 290, 360, 60, lambda: set_tela_config_multiplayer()),
    Botao("Configurações", WIDTH//2 - 180, 360, 360, 60, ir_para_config),
    Botao("Ranking", WIDTH//2 - 180, 430, 360, 60, ir_para_placar),
    Botao("Sair", WIDTH//2 - 180, 500, 360, 60, sair),
]

# Função para ir para a tela de configuração multiplayer

def set_tela_config_multiplayer():
    global tela_atual, subtela_multiplayer
    subtela_multiplayer = 1
    tela_atual = "config_multiplayer"

# Função para mostrar tela de dificuldade

def ir_para_dificuldade():
    global tela_atual, dificuldade_escolhida
    dificuldade_escolhida = ""
    tela_atual = TELA_DIFICULDADE

# Botões de dificuldade (PALETA PADRÃO)
btns_dificuldade = [
    {"label": "Fácil", "desc": "Palavras de 4-5 letras", "cor": (120, 160, 60), "hover": (140, 180, 80)},    # Verde suave
    {"label": "Médio", "desc": "Palavras de 6-7 letras", "cor": (196, 102, 31), "hover": (220, 120, 50)},   # Laranja terroso
    {"label": "Difícil", "desc": "Palavras de 8+ letras", "cor": (160, 100, 50), "hover": (180, 120, 70)}, # Marrom suave
]
btn_dificuldade_hover = None
carregando_palavra = False

# Função para desenhar tela de carregando palavra (removida - usando versão do interface.py)

# Remover a função duplicada de interface:
# def desenhar_carregando_palavra_animado():
#     screen.fill(COR_FUNDO_PRINCIPAL)
#     # Animação de reticências
#     t = pygame.time.get_ticks() // 400 % 4
#     pontos = '.' * t
#     msg = FONT_BIG.render(f"Carregando palavra{pontos}", True, COR_TEXTO_CLARO)
#     screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
#     pygame.display.flip()
# (Função removida para evitar conflito)

dicio_cache = {}
palavras_usadas = set()
palavras_invalidas = set()

DICIO_CACHE_FILE = "dicio_cache.json"
PALAVRAS_INVALIDAS_FILE = "palavras_invalidas.json"
LOG_SORTEIO_FILE = "log_sorteio_palavras.txt"

def carregar_cache():
    global dicio_cache, palavras_invalidas
    try:
        with open(DICIO_CACHE_FILE, "r", encoding="utf-8") as f:
            dicio_cache = json.load(f)
    except Exception:
        dicio_cache = {}
    try:
        with open(PALAVRAS_INVALIDAS_FILE, "r", encoding="utf-8") as f:
            palavras_invalidas = set(json.load(f))
    except Exception:
        palavras_invalidas = set()

def salvar_cache():
    try:
        with open(DICIO_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(dicio_cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    try:
        with open(PALAVRAS_INVALIDAS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(palavras_invalidas), f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def log_sorteio(palavra, status):
    try:
        with open(LOG_SORTEIO_FILE, "a", encoding="utf-8") as f:
            f.write(f"{palavra}: {status}\n")
    except Exception:
        pass

carregar_cache()

# Atualizar tem_definicao_dicio para salvar cache e logar

def tem_definicao_dicio(palavra):
    # Use simplified validation if palavras_mais_buscadas file exists
    if use_simplified_validation:
        return True
        
    palavra = palavra.upper()
    if palavra in dicio_cache:
        return dicio_cache[palavra]
    definicao = buscar_definicao_dicio(palavra)
    if not definicao:
        dicio_cache[palavra] = False
        palavras_invalidas.add(palavra)
        salvar_cache()
        log_sorteio(palavra, "REJEITADA - sem definição")
        return False
    texto = definicao.lower()
    if (
        'não encontrada' in texto or
        'erro' in texto or
        'flexão de' in texto or
        'variante de' in texto or
        'ver também' in texto or
        'não encontrado' in texto or
        'ainda não temos o significado' in texto or
        'você pode ajudar a melhorar o dicio' in texto or
        'sugerindo uma definição' in texto or
        'não tem definição' in texto or
        'não possui definição' in texto or
        'não foi encontrada' in texto or
        'definição não encontrada' in texto or
        len(definicao.strip()) < 10
    ):
        dicio_cache[palavra] = False
        palavras_invalidas.add(palavra)
        salvar_cache()
        log_sorteio(palavra, "REJEITADA - filtro")
        return False
    dicio_cache[palavra] = True
    salvar_cache()
    log_sorteio(palavra, "ACEITA")
    return True

def iniciar_jogo_solo():
    global tela_atual, palavra_original, palavra_embaralhada, letras_adivinhadas, indice_atual, nome_jogador_exemplo, tempo_exemplo, erros_exemplo, rodada_ativa, inicio_tempo, fim_rodada, mensagem_final, venceu_rodada, letras_tentadas, letras_erradas, feedback_erro_idx, feedback_erro_timer, letras_embaralhadas_usadas, letras_embaralhadas_pos, palavras_usadas, palavras_invalidas
    if nome_jogador.strip() and dificuldade_escolhida:
        lista_base = palavras_dicionario.get(dificuldade_escolhida, [])
        lista_palavras = [p for p in lista_base if p not in palavras_usadas and p not in palavras_invalidas]
        if not lista_palavras:
            palavras_usadas.clear()
            with open(PALAVRAS_USADAS_PATH, 'w', encoding='utf-8') as f:
                json.dump(list(palavras_usadas), f, ensure_ascii=False, indent=2)
            lista_palavras = [p for p in lista_base if p not in palavras_invalidas]
            if not lista_palavras:
                tela_atual = TELA_DIFICULDADE
                return
        if tem_definicao_dicio.__code__.co_code == (lambda x: True).__code__.co_code:
            palavra_escolhida = random.choice(lista_palavras).upper()
            # Loga a palavra sorteada
            try:
                with open("log_sorteio_palavras.txt", "a", encoding="utf-8") as f:
                    f.write(f"{palavra_escolhida}: ACEITA (sem validação)\n")
            except Exception:
                pass
        else:
            palavra_escolhida = None
            palavra_candidata = None  # Inicializar a variável
            tentativas = 0
            while tentativas < 10 and lista_palavras:
                palavra_candidata = random.choice(lista_palavras).upper()
                if tem_definicao_dicio(palavra_candidata):
                    palavra_escolhida = palavra_candidata
                    break
                tentativas += 1
                lista_palavras.remove(palavra_candidata)
            if not palavra_escolhida and palavra_candidata:
                palavra_escolhida = palavra_candidata  # usa a última sorteada
        
        # Garantir que sempre temos uma palavra válida
        if not palavra_escolhida:
            palavra_escolhida = "PYTHON"  # palavra de fallback
            
        palavra_original = palavra_escolhida
        palavras_usadas.add(palavra_original)
        with open(PALAVRAS_USADAS_PATH, 'w', encoding='utf-8') as f:
            json.dump(list(palavras_usadas), f, ensure_ascii=False, indent=2)
        palavra_embaralhada = embaralhar_palavra(palavra_original)
        letras_adivinhadas = ["" for _ in palavra_original]
        indice_atual = 0
        nome_jogador_exemplo = nome_jogador.upper()
        tempo_exemplo = 0.0
        erros_exemplo = 0
        rodada_ativa = True
        inicio_tempo = time.time()
        fim_rodada = False
        mensagem_final = ""
        venceu_rodada = False
        letras_tentadas = set()
        letras_erradas = set()
        feedback_erro_idx = -1
        feedback_erro_timer = 0
        letras_embaralhadas_usadas = [False] * len(palavra_embaralhada)
        letras_embaralhadas_pos = []
        tela_atual = TELA_JOGO

dificuldade_escolhida = ""
botao_iniciar_nome = Botao("Iniciar", WIDTH//2 - 80, 400, 160, 60, ir_para_dificuldade)

# Botão desistir
botao_desistir_rect = pygame.Rect(WIDTH - 200, HEIGHT - 80, 160, 60)

def finalizar_rodada(vitoria):
    global rodada_ativa, fim_rodada, mensagem_final, venceu_rodada, som_fim_tocou, rodada_finalizada
    if rodada_finalizada:
        return
    rodada_finalizada = True
    rodada_ativa = False
    fim_rodada = True
    venceu_rodada = vitoria
    if vitoria:
        mensagem_final = f"Parabéns! Você acertou a palavra '{palavra_original}'!"
        salvar_ranking_solo(nome_jogador, palavra_original, tempo_exemplo, dificuldade_escolhida)
    else:
        mensagem_final = f"Você desistiu! A palavra era '{palavra_original}'."
    print('[SOM] Fim do jogo (solo)')
    if SOM_FIM:  # Verificação de segurança
        SOM_FIM.play()
    som_fim_tocou = True

def buscar_definicao_dicio(palavra):
    url = f'https://www.dicio.com.br/{palavra.lower()}/'
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            definicao_tag = soup.find('p', class_='significado')
            if definicao_tag:
                return definicao_tag.get_text(separator=" ", strip=True)
            p_tags = soup.find_all('p')
            if p_tags:
                return p_tags[0].get_text(separator=" ", strip=True)
        return ''
    except Exception:
        return ''

# Função para popup de definição

def popup_definicao(palavra):
    definicao = buscar_definicao_dicio(palavra)
    largura, altura = 540, 340
    popup_surface = pygame.Surface((largura, altura))
    popup_surface.fill((230, 226, 195))
    pygame.draw.rect(popup_surface, COR_BOTAO, (0, 0, largura, altura), 4, border_radius=16)
    titulo = FONT_MED.render(f'Definição: {palavra.upper()}', True, COR_TEXTO_CLARO)
    popup_surface.blit(titulo, (largura//2 - titulo.get_width()//2, 18))
    # Quebra a definição em linhas
    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = line + word + ' '
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)
        return lines
    linhas = wrap_text(definicao, FONT_SMALL, largura-40)
    y0 = 60
    linhas_visiveis = 8
    scroll = 0
    total_linhas = len(linhas)
    # Botão fechar
    btn_rect = pygame.Rect(largura//2 - 60, altura - 60, 120, 40)
    rodando = True
    while rodando:
        popup_surface.fill((230, 226, 195))
        pygame.draw.rect(popup_surface, COR_BOTAO, (0, 0, largura, altura), 4, border_radius=16)
        popup_surface.blit(titulo, (largura//2 - titulo.get_width()//2, 18))
        # Desenha linhas visíveis
        y = y0
        for i in range(scroll, min(scroll+linhas_visiveis, total_linhas)):
            l = FONT_SMALL.render(linhas[i], True, COR_TEXTO_CLARO)
            popup_surface.blit(l, (20, y))
            y += 28
        # Botão fechar
        pygame.draw.rect(popup_surface, COR_BOTAO, btn_rect, border_radius=8)
        fechar_label = FONT_SMALL.render('Fechar', True, COR_BOTAO_TEXTO)
        popup_surface.blit(fechar_label, (btn_rect.x + (btn_rect.w - fechar_label.get_width())//2, btn_rect.y + 8))
        # Setas de rolagem
        if scroll > 0:
            seta_cima = FONT_SMALL.render('▲', True, COR_TEXTO_CLARO)
            popup_surface.blit(seta_cima, (largura-40, y0))
        if scroll + linhas_visiveis < total_linhas:
            seta_baixo = FONT_SMALL.render('▼', True, COR_TEXTO_CLARO)
            popup_surface.blit(seta_baixo, (largura-40, y0 + (linhas_visiveis-1)*28))
        # Loop do popup
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                rel_x = mx - (WIDTH//2 - largura//2)
                rel_y = my - (HEIGHT//2 - altura//2)
                if btn_rect.collidepoint(rel_x, rel_y):
                    rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll + linhas_visiveis < total_linhas:
                    scroll += 1
                if event.key == pygame.K_UP and scroll > 0:
                    scroll -= 1
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0 and scroll + linhas_visiveis < total_linhas:
                    scroll += 1
                if event.y > 0 and scroll > 0:
                    scroll -= 1
        screen.blit(popup_surface, (WIDTH//2 - largura//2, HEIGHT//2 - altura//2))
        pygame.display.flip()

# No loop principal, troque:
# if tela_atual == "config_multiplayer":
#     loop_config_multiplayer(events)
# por:
# if tela_atual == "config_multiplayer":
#     tratar_multiplayer(events)


# --- Função para desenhar a tela de nomes (tela 2) ---
# def desenhar_config_multiplayer_nomes(foco_idx):
#     screen.fill(COR_FUNDO_PRINCIPAL)
#     mouse_x, mouse_y = pygame.mouse.get_pos()
#     titulo = FONT_BIG.render("Nomes dos Jogadores", True, COR_TEXTO_CLARO)
#     screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 40))
#     bloco_top = 120
#     campo_largura = 380
#     campo_altura = 44
#     bloco_nomes_top = bloco_top + 20
#     input_nomes = []
#     for i in range(num_jogadores):
#         y = bloco_nomes_top + i*(campo_altura + 18)
#         label = FONT_SMALL.render(f"Jogador {i+1}:", True, COR_TEXTO_CLARO)
#         screen.blit(label, (WIDTH//2 - 260, y + 8))
#         rect = pygame.Rect(WIDTH//2 - campo_largura//2 + 40, y, campo_largura, campo_altura)
#         cor_borda = (185, 148, 112) if foco_idx != i else (196, 102, 31)
#         pygame.draw.rect(screen, cor_input_inativo, rect, border_radius=10)
#         pygame.draw.rect(screen, cor_borda, rect, 3, border_radius=10)
#         nome = nomes_jogadores[i] if i < len(nomes_jogadores) else ""
#         nome_render = FONT_MED.render(nome.upper(), True, COR_TEXTO_CLARO)
#         screen.blit(nome_render, (rect.x + (campo_largura - nome_render.get_width())//2, rect.y + 6))
#         input_nomes.append((rect, i))
#     # Botão iniciar
#     btn_iniciar_rect = pygame.Rect(WIDTH//2 + 20, bloco_nomes_top + num_jogadores*(campo_altura + 18) + 32, 180, 56)
#     nomes_ok = all(n.strip() for n in nomes_jogadores[:num_jogadores])
#     cor_btn = COR_BOTAO_HOVER if btn_iniciar_rect.collidepoint(mouse_x, mouse_y) and nomes_ok else COR_BOTAO
#     pygame.draw.rect(screen, cor_btn, btn_iniciar_rect, border_radius=14)
#     pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_iniciar_rect, 3, border_radius=14)
#     iniciar_label = FONT_MED.render("Iniciar Multiplayer", True, COR_BOTAO_TEXTO)
#     screen.blit(iniciar_label, (btn_iniciar_rect.x + (btn_iniciar_rect.w - iniciar_label.get_width())//2, btn_iniciar_rect.y + 12))
#     # Botão voltar
#     btn_voltar_rect = pygame.Rect(WIDTH//2 - 200, bloco_nomes_top + num_jogadores*(campo_altura + 18) + 32, 140, 56)
#     cor_voltar = COR_BOTAO_HOVER if btn_voltar_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
#     pygame.draw.rect(screen, cor_voltar, btn_voltar_rect, border_radius=14)
#     pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_voltar_rect, 3, border_radius=14)
#     voltar_label = FONT_MED.render("Voltar", True, COR_BOTAO_TEXTO)
#     screen.blit(voltar_label, (btn_voltar_rect.x + (btn_voltar_rect.w - voltar_label.get_width())//2, btn_voltar_rect.y + 12))
#     # Mensagem de erro
#     if multiplayer_erro_msg:
#         erro_label = FONT_SMALL.render(multiplayer_erro_msg, True, (196, 102, 31))
#         screen.blit(erro_label, (WIDTH//2 - erro_label.get_width()//2, btn_iniciar_rect.y + 64))
#     return btn_iniciar_rect, btn_voltar_rect, input_nomes

# def desenhar_espera_multiplayer(jogador_adivinha):
#     screen.fill(COR_FUNDO_PRINCIPAL)
#     titulo = FONT_BIG.render("Passe para o próximo jogador!", True, COR_TEXTO_CLARO)
#     screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 100))
#     instr = FONT_MED.render(f"{jogador_adivinha}, clique em Pronto para começar", True, COR_TEXTO_CLARO)
#     screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 200))
#     btn_pronto_rect = pygame.Rect(WIDTH//2 - 100, 320, 200, 60)
#     mouse_x, mouse_y = pygame.mouse.get_pos()
#     cor_btn = COR_BOTAO_HOVER if btn_pronto_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
#     pygame.draw.rect(screen, cor_btn, btn_pronto_rect, border_radius=14)
#     pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_pronto_rect, 2, border_radius=14)
#     pronto_label = FONT_MED.render("Pronto", True, COR_BOTAO_TEXTO)
#     screen.blit(pronto_label, (btn_pronto_rect.x + (btn_pronto_rect.w - pronto_label.get_width())//2, btn_pronto_rect.y + 12))
#     return btn_pronto_rect

# Função para iniciar o jogo multiplayer
def iniciar_multiplayer():
    global estado_multiplayer, rodada_idx, pares, tempos, erros, palavras
    global multiplayer_palavra_atual, multiplayer_letras_adivinhadas, multiplayer_indice_atual
    global multiplayer_letras_embaralhadas, multiplayer_letras_embaralhadas_usadas
    global multiplayer_letras_tentadas, multiplayer_letras_erradas, multiplayer_erros, multiplayer_tempo_inicio
    pares = [(i, (i+1)%num_jogadores) for i in range(num_jogadores)]
    rodada_idx = 0
    tempos = [0.0 for _ in range(num_jogadores)]
    erros = [0 for _ in range(num_jogadores)]
    palavras = ["" for _ in range(num_jogadores)]
    estado_multiplayer = "definir_palavra"
    multiplayer_palavra_atual = ""
    multiplayer_letras_adivinhadas = []
    multiplayer_indice_atual = 0
    multiplayer_letras_embaralhadas = []
    multiplayer_letras_embaralhadas_usadas = []
    multiplayer_letras_tentadas = set()
    multiplayer_letras_erradas = set()
    multiplayer_erros = 0
    multiplayer_tempo_inicio = 0

# Adicione o controle de FPS do Pygame
clock = pygame.time.Clock()

# Inicialize o shake_timer
shake_timer = 0

# Defina SHAKE_DURATION para uso no loop
SHAKE_DURATION = 200  # ms
SHAKE_INTENSITY = 8   # pixels

# Inicialize o estado do multiplayer
estado_multiplayer = "config"

# Inicialize o número de jogadores do multiplayer
num_jogadores = 2

# Inicialize a lista de nomes dos jogadores do multiplayer
nomes_jogadores = []

# Mensagem de erro do multiplayer
multiplayer_erro_msg = ""

# Inicialize variáveis de controle do multiplayer
rodada_idx = 0
pares = []
tempos = []
erros = []
palavras = []

# Variáveis globais para o estado do multiplayer
multiplayer_palavra_atual = ""
multiplayer_letras_adivinhadas = []
multiplayer_indice_atual = 0
multiplayer_letras_embaralhadas = []
multiplayer_letras_embaralhadas_usadas = []
multiplayer_letras_tentadas = set()
multiplayer_letras_erradas = set()
multiplayer_erros = 0
multiplayer_tempo_inicio = 0
multiplayer_foco_idx = 0
multiplayer_foco_inicializado = False
multiplayer_feedback_erro_idx = -1
multiplayer_feedback_erro_timer = 0
multiplayer_feedback_erro_circulo_idx = -1
multiplayer_feedback_erro_circulo_timer = 0
multiplayer_shake_timer = 0
multiplayer_erro_palavra = ""
multiplayer_palavra_secreta = ""
multiplayer_sugestoes = []
multiplayer_btns_sugestoes = []
multiplayer_btn_add_rect = None
multiplayer_btn_fechar_rect = None
multiplayer_mensagem_final = ""
multiplayer_tempo_final = 0.0
multiplayer_erros_final = 0
multiplayer_som_iniciar_tocou = False
multiplayer_som_vitoria_tocou = False

# Inicialize o número máximo de letras por rodada do multiplayer
default_max_letras = 6
max_letras_rodada = default_max_letras

# 1. Adicionar variável de controle para transição
transicao_multiplayer_timer = 0
transicao_multiplayer_msg = ""

def tratar_multiplayer(events):
    global estado_multiplayer, rodada_idx, pares, nomes_jogadores, tempos, erros, palavras, num_jogadores, max_letras_rodada
    global transicao_multiplayer_msg, transicao_multiplayer_timer
    global multiplayer_erro_msg, multiplayer_foco_idx, multiplayer_foco_inicializado
    global multiplayer_feedback_erro_idx, multiplayer_feedback_erro_timer
    global multiplayer_feedback_erro_circulo_idx, multiplayer_feedback_erro_circulo_timer, multiplayer_shake_timer
    global multiplayer_indice_atual, multiplayer_letras_adivinhadas, multiplayer_letras_tentadas
    global multiplayer_letras_erradas, multiplayer_erros, multiplayer_letras_embaralhadas_usadas
    global multiplayer_mensagem_final, multiplayer_tempo_final, multiplayer_erros_final
    global multiplayer_palavra_atual, multiplayer_erro_palavra, multiplayer_palavra_secreta
    global multiplayer_sugestoes, multiplayer_btns_sugestoes, multiplayer_btn_add_rect, multiplayer_btn_fechar_rect
    global multiplayer_letras_embaralhadas, multiplayer_tempo_inicio
    if estado_multiplayer == "config":
        menos_rect, mais_rect, menos_l_rect, mais_l_rect, btn_avancar_rect, btn_voltar_rect = desenhar_config_multiplayer_config(
            screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_BOTAO, COR_BOTAO_HOVER, COR_TEXTO_CLARO_DESTACADO, num_jogadores, max_letras_rodada
        )
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                voltar_menu()
                estado_multiplayer = "config"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if menos_rect.collidepoint(mx, my):
                    if num_jogadores > 2:
                        num_jogadores -= 1
                        nomes_jogadores = nomes_jogadores[:num_jogadores]
                        if multiplayer_foco_idx >= num_jogadores:
                            multiplayer_foco_idx = num_jogadores - 1
                elif mais_rect.collidepoint(mx, my):
                    if num_jogadores < 6:
                        num_jogadores += 1
                        while len(nomes_jogadores) < num_jogadores:
                            nomes_jogadores.append("")
                elif menos_l_rect.collidepoint(mx, my):
                    if max_letras_rodada > 4:
                        max_letras_rodada -= 1
                elif mais_l_rect.collidepoint(mx, my):
                    if max_letras_rodada < 20:
                        max_letras_rodada += 1
                elif btn_avancar_rect.collidepoint(mx, my) and (2 <= num_jogadores <= 6 and 4 <= max_letras_rodada <= 20):
                    estado_multiplayer = "nomes"
                elif btn_voltar_rect.collidepoint(mx, my):
                    voltar_menu()
        pygame.display.flip()
    elif estado_multiplayer == "nomes":
        if multiplayer_foco_idx >= num_jogadores:
            multiplayer_foco_idx = num_jogadores - 1
        nomes_jogadores[:] = nomes_jogadores[:num_jogadores]
        while len(nomes_jogadores) < num_jogadores:
            nomes_jogadores.append("")
        btn_iniciar_rect, btn_voltar_rect, input_nomes = desenhar_config_multiplayer_nomes(
            screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO,
            cor_input_inativo, cor_input_borda, COR_BOTAO, COR_BOTAO_HOVER, num_jogadores, nomes_jogadores, multiplayer_foco_idx, multiplayer_erro_msg
        )
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    voltar_menu()
                    estado_multiplayer = "config"
                elif event.key in (pygame.K_TAB, pygame.K_RETURN):
                    if multiplayer_foco_idx < num_jogadores - 1:
                        multiplayer_foco_idx += 1
                    else:
                        if all(n.strip() for n in nomes_jogadores[:num_jogadores]):
                            iniciar_multiplayer()
                            estado_multiplayer = "definir_palavra"
                elif event.key == pygame.K_BACKSPACE:
                    idx = multiplayer_foco_idx
                    if 0 <= idx < len(nomes_jogadores):
                        nomes_jogadores[idx] = nomes_jogadores[idx][:-1]
                elif 0 <= multiplayer_foco_idx < len(nomes_jogadores) and len(nomes_jogadores[multiplayer_foco_idx]) < 20 and event.unicode.isprintable():
                    idx = multiplayer_foco_idx
                    nomes_jogadores[idx] += event.unicode.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for rect, idx in input_nomes:
                    if rect.collidepoint(mx, my):
                        multiplayer_foco_idx = idx
                        break
                if btn_iniciar_rect.collidepoint(mx, my) and all(n.strip() for n in nomes_jogadores[:num_jogadores]):
                    if not all(n.strip() for n in nomes_jogadores[:num_jogadores]):
                        multiplayer_erro_msg = "Preencha o nome de todos os jogadores!"
                    else:
                        iniciar_multiplayer()
                        estado_multiplayer = "definir_palavra"
                elif btn_voltar_rect.collidepoint(mx, my):
                    estado_multiplayer = "config"
        if not multiplayer_foco_inicializado:
            multiplayer_foco_idx = 0
            multiplayer_foco_inicializado = True
        pygame.display.flip()
    elif estado_multiplayer == "definir_palavra":
        definidor, adivinha = 0, 1  # Exemplo para 2 jogadores
        jogador_definidor = nomes_jogadores[definidor]
        jogador_adivinha = nomes_jogadores[adivinha]
        input_rect, btn_confirmar_rect = desenhar_definir_palavra_multiplayer(
            screen, FONT_BIG, FONT_MED, cor_input_inativo, jogador_definidor, jogador_adivinha, multiplayer_palavra_atual
        )
        if multiplayer_erro_palavra:
            # Caixa de sugestões
            caixa_largura = input_rect.width + 60  # aumentada
            caixa_x = input_rect.x - 30
            altura_sugestoes = 50 * 5 + 60  # altura maior por sugestão e mais espaço
            caixa_altura = altura_sugestoes + 60
            caixa_y = btn_confirmar_rect.y + btn_confirmar_rect.height + 20  # 20px abaixo do botão confirmar
            pygame.draw.rect(screen, (245, 240, 210), (caixa_x, caixa_y, caixa_largura, caixa_altura), border_radius=18)
            pygame.draw.rect(screen, (185, 148, 112), (caixa_x, caixa_y, caixa_largura, caixa_altura), 3, border_radius=18)
            # Texto de erro centralizado no topo da caixa
            erro_label = FONT_SMALL.render(multiplayer_erro_palavra, True, (196, 102, 31))
            erro_x = caixa_x + (caixa_largura - erro_label.get_width()) // 2
            erro_y = caixa_y + 12
            screen.blit(erro_label, (erro_x, erro_y))
            # Sugestões de palavras parecidas
            palavra_tentativa = multiplayer_palavra_atual.strip().upper()
            letras_esperadas = len(palavra_tentativa)
            # Filtrar dicionario_multiplayer para o tamanho correto
            palavras_filtradas = [p for p in dicionario_multiplayer if len(p) == letras_esperadas]
            multiplayer_sugestoes = difflib.get_close_matches(palavra_tentativa, palavras_filtradas, n=5, cutoff=0.7)
            btns_sugestoes = []
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, sugestao in enumerate(multiplayer_sugestoes):
                btn_rect = pygame.Rect(caixa_x + 25, caixa_y + 40 + i*55, caixa_largura - 50, 44)
                hover = btn_rect.collidepoint(mouse_x, mouse_y)
                cor_btn = (185, 148, 112) if hover else COR_BOTAO
                cor_borda = (196, 102, 31) if hover else COR_BOTAO_HOVER
                pygame.draw.rect(screen, cor_btn, btn_rect, border_radius=12)
                pygame.draw.rect(screen, cor_borda, btn_rect, 2, border_radius=12)
                label = FONT_SMALL.render(f"Usar: {sugestao}", True, COR_BOTAO_TEXTO)
                screen.blit(label, (btn_rect.x + 16, btn_rect.y + 10))
                btns_sugestoes.append((btn_rect, sugestao))
            # Botão para adicionar ao dicionário
            btn_add_rect = pygame.Rect(caixa_x + 25, caixa_y + 40 + len(multiplayer_sugestoes)*55, caixa_largura - 50, 44)
            hover_add = btn_add_rect.collidepoint(mouse_x, mouse_y)
            cor_add = (120, 180, 60) if not hover_add else (80, 200, 80)
            cor_add_borda = (80, 140, 40) if not hover_add else (40, 100, 40)
            pygame.draw.rect(screen, cor_add, btn_add_rect, border_radius=12)
            pygame.draw.rect(screen, cor_add_borda, btn_add_rect, 2, border_radius=12)
            label_add = FONT_SMALL.render("Adicionar ao dicionário", True, (30, 60, 30))
            screen.blit(label_add, (btn_add_rect.x + 16, btn_add_rect.y + 10))
            # Após desenhar o botão 'Adicionar ao dicionário', adicione o botão 'Fechar' logo abaixo dele:
            btn_fechar_largura = 90
            btn_fechar_altura = 36
            btn_fechar_margin = 10
            btn_fechar_rect = pygame.Rect(
                btn_add_rect.x,
                btn_add_rect.y + btn_add_rect.height + btn_fechar_margin,
                btn_fechar_largura,
                btn_fechar_altura
            )
            hover_fechar = btn_fechar_rect.collidepoint(mouse_x, mouse_y)
            cor_fechar = (120, 170, 220) if not hover_fechar else (100, 140, 200)  # azul suave
            cor_fechar_borda = (80, 120, 180)
            pygame.draw.rect(screen, cor_fechar, btn_fechar_rect, border_radius=10)
            pygame.draw.rect(screen, cor_fechar_borda, btn_fechar_rect, 2, border_radius=10)
            label_fechar = FONT_SMALL.render("Fechar", True, (255,255,255))
            screen.blit(label_fechar, (btn_fechar_rect.x + (btn_fechar_rect.w - label_fechar.get_width())//2, btn_fechar_rect.y + 7))
            multiplayer_btns_sugestoes = btns_sugestoes
            multiplayer_btn_add_rect = btn_add_rect
            multiplayer_btn_fechar_rect = btn_fechar_rect
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    voltar_menu()
                    estado_multiplayer = "config"
                    return
                elif event.key == pygame.K_RETURN:
                    if 4 <= len(multiplayer_palavra_atual.strip()) <= max_letras_rodada:
                        palavra_tentativa = multiplayer_palavra_atual.strip().upper()
                        if palavra_tentativa in dicionario_multiplayer:
                            multiplayer_palavra_secreta = palavra_tentativa
                            estado_multiplayer = "espera"
                            multiplayer_palavra_atual = ""
                            multiplayer_erro_palavra = ""
                        else:
                            multiplayer_erro_palavra = "Palavra não encontrada no dicionário!"
                elif event.key == pygame.K_BACKSPACE:
                    multiplayer_palavra_atual = multiplayer_palavra_atual[:-1]
                elif len(multiplayer_palavra_atual) < max_letras_rodada and event.unicode.isalpha():
                    multiplayer_palavra_atual += event.unicode.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if input_rect.collidepoint(mx, my):
                    pass
                elif btn_confirmar_rect.collidepoint(mx, my):
                    if 4 <= len(multiplayer_palavra_atual.strip()) <= max_letras_rodada:
                        palavra_tentativa = multiplayer_palavra_atual.strip().upper()
                        if palavra_tentativa in dicionario_multiplayer:
                            multiplayer_palavra_secreta = palavra_tentativa
                            estado_multiplayer = "espera"
                            multiplayer_palavra_atual = ""
                            multiplayer_erro_palavra = ""
                        else:
                            multiplayer_erro_palavra = "Palavra não encontrada no dicionário!"
                # Bloco de sugestões e adicionar ao dicionário deve estar aqui:
                if multiplayer_erro_palavra:
                    # Verifica se clicou em uma sugestão
                    for btn_rect, sugestao in multiplayer_btns_sugestoes:
                        if btn_rect.collidepoint(mx, my):
                            multiplayer_palavra_secreta = sugestao
                            estado_multiplayer = "espera"
                            multiplayer_palavra_atual = ""
                            multiplayer_erro_palavra = ""
                            return
                    # Verifica se clicou em adicionar ao dicionário
                    if multiplayer_btn_add_rect and multiplayer_btn_add_rect.collidepoint(mx, my):
                        palavra_tentativa = multiplayer_palavra_atual.strip().upper()
                        adicionar_palavra_ao_dicionario(palavra_tentativa)
                        multiplayer_palavra_secreta = palavra_tentativa
                        estado_multiplayer = "espera"
                        multiplayer_palavra_atual = ""
                        multiplayer_erro_palavra = ""
                        return
                    # Verifica se clicou em fechar
                    if multiplayer_btn_fechar_rect and multiplayer_btn_fechar_rect.collidepoint(mx, my):
                        multiplayer_erro_palavra = ""
                        return
        pygame.display.flip()
    elif estado_multiplayer == "espera":
        global multiplayer_letras_adivinhadas, multiplayer_indice_atual, multiplayer_letras_embaralhadas
        global multiplayer_letras_embaralhadas_usadas, multiplayer_letras_tentadas, multiplayer_letras_erradas
        global multiplayer_erros, multiplayer_tempo_inicio
        definidor, adivinha = 0, 1  # Exemplo para 2 jogadores
        jogador_adivinha = nomes_jogadores[adivinha]
        btn_pronto_rect = desenhar_espera_multiplayer(
            screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_BOTAO, COR_BOTAO_HOVER, jogador_adivinha
        )
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    voltar_menu()
                    estado_multiplayer = "config"
                    return
                elif event.key == pygame.K_RETURN:
                    # Ativa o botão Pronto
                    estado_multiplayer = "adivinhar"
                    multiplayer_letras_adivinhadas = ["" for _ in multiplayer_palavra_secreta]
                    multiplayer_indice_atual = 0
                    letras = list(multiplayer_palavra_secreta)
                    while True:
                        random.shuffle(letras)
                        if ''.join(letras) != multiplayer_palavra_secreta:
                            break
                    multiplayer_letras_embaralhadas = letras
                    multiplayer_letras_embaralhadas_usadas = [False] * len(multiplayer_palavra_secreta)
                    multiplayer_letras_tentadas = set()
                    multiplayer_letras_erradas = set()
                    multiplayer_erros = 0
                    multiplayer_tempo_inicio = time.time()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn_pronto_rect.collidepoint(mx, my):
                    estado_multiplayer = "adivinhar"
                    multiplayer_letras_adivinhadas = ["" for _ in multiplayer_palavra_secreta]
                    multiplayer_indice_atual = 0
                    letras = list(multiplayer_palavra_secreta)
                    while True:
                        random.shuffle(letras)
                        if ''.join(letras) != multiplayer_palavra_secreta:
                            break
                    multiplayer_letras_embaralhadas = letras
                    multiplayer_letras_embaralhadas_usadas = [False] * len(multiplayer_palavra_secreta)
                    multiplayer_letras_tentadas = set()
                    multiplayer_letras_erradas = set()
                    multiplayer_erros = 0
                    multiplayer_tempo_inicio = time.time()
        pygame.display.flip()
    elif estado_multiplayer == "adivinhar":
        # Interface de adivinhação multiplayer (com animação de erro)
        screen.fill(COR_FUNDO_PRINCIPAL)
        tempo_atual = time.time() - multiplayer_tempo_inicio + multiplayer_erros * PENALIDADE_ERRO
        info = FONT_SMALL.render(f"Tempo: {tempo_atual:.2f}s   Erros: {multiplayer_erros}", True, COR_TEXTO_CLARO)
        screen.blit(info, (40, 30))
        # Tremor
        shake_x, shake_y = 0, 0
        if multiplayer_shake_timer > 0:
            shake_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
            shake_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        # Letras embaralhadas
        letras_embaralhadas_pos = []
        cx = WIDTH//2 - (len(multiplayer_letras_embaralhadas)*60)//2 + shake_x
        cy = 120 + shake_y
        for i, letra in enumerate(multiplayer_letras_embaralhadas):
            center = (cx + i*60 + 30, cy + 30)
            rect = pygame.Rect(center[0]-30, center[1]-30, 60, 60)
            if i == multiplayer_feedback_erro_circulo_idx and multiplayer_feedback_erro_circulo_timer > 0:
                cor = (196, 102, 31)
            elif not multiplayer_letras_embaralhadas_usadas[i]:
                cor = (210, 180, 140)  # marrom claro
            else:
                cor = (100, 200, 120)  # verde suave
            pygame.draw.circle(screen, cor, center, 30)
            l = FONT_BIG.render(letra, True, (255,255,255))
            screen.blit(l, (center[0] - l.get_width()//2, center[1] - l.get_height()//2))
            letras_embaralhadas_pos.append((rect, letra, i))
        # Espaços para adivinhar
        cx2 = WIDTH//2 - (len(multiplayer_palavra_secreta)*60)//2 + shake_x
        cy2 = 250 + shake_y
        for i in range(len(multiplayer_palavra_secreta)):
            rect = pygame.Rect(cx2 + i*60, cy2, 50, 60)
            if i == multiplayer_feedback_erro_idx and multiplayer_feedback_erro_timer > 0:
                pygame.draw.rect(screen, (196, 102, 31), rect, border_radius=8)
            elif multiplayer_letras_adivinhadas[i]:
                pygame.draw.rect(screen, (160, 130, 90), rect, border_radius=8)  # marrom mais escuro
            else:
                pygame.draw.rect(screen, (210, 180, 140), rect, border_radius=8)  # marrom claro
            pygame.draw.rect(screen, cor_input_borda, rect, 2, border_radius=8)
            letra = multiplayer_letras_adivinhadas[i]
            letra_render = FONT_BIG.render(letra, True, (255,255,255)) if letra else None
            if letra_render:
                screen.blit(letra_render, (rect.x + (rect.w - letra_render.get_width())//2, rect.y + (rect.h - letra_render.get_height())//2))
        btn_desistir_rect = pygame.Rect(WIDTH - 220, HEIGHT - 80, 160, 60)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cor_desistir = COR_BOTAO_HOVER if btn_desistir_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
        pygame.draw.rect(screen, cor_desistir, btn_desistir_rect, border_radius=10)
        desistir_label = FONT_MED.render("Desistir", True, (255,255,255))
        screen.blit(desistir_label, (btn_desistir_rect.x + (btn_desistir_rect.w - desistir_label.get_width())//2, btn_desistir_rect.y + 10))
        instr = FONT_SMALL.render("Clique nas letras embaralhadas ou digite. ESC volta ao menu.", True, COR_TEXTO_CLARO)
        screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT - 40))
        # Atualizar timers de feedback
        dt = clock.get_time()
        if multiplayer_feedback_erro_timer > 0:
            multiplayer_feedback_erro_timer -= dt
            if multiplayer_feedback_erro_timer <= 0:
                multiplayer_feedback_erro_idx = -1
        if multiplayer_feedback_erro_circulo_timer > 0:
            multiplayer_feedback_erro_circulo_timer -= dt
            if multiplayer_feedback_erro_circulo_timer <= 0:
                multiplayer_feedback_erro_circulo_idx = -1
        if multiplayer_shake_timer > 0:
            multiplayer_shake_timer -= dt
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    voltar_menu()
                    estado_multiplayer = "config"
                    return
                elif event.key == pygame.K_BACKSPACE:
                    if multiplayer_letras_adivinhadas[multiplayer_indice_atual]:
                        multiplayer_letras_adivinhadas[multiplayer_indice_atual] = ""
                    elif multiplayer_indice_atual > 0:
                        multiplayer_indice_atual -= 1
                        multiplayer_letras_adivinhadas[multiplayer_indice_atual] = ""
                elif event.unicode.isalpha() and len(event.unicode) == 1:
                    letra_digitada = event.unicode.upper()
                    multiplayer_letras_tentadas.add(letra_digitada)
                    if letra_digitada == multiplayer_palavra_secreta[multiplayer_indice_atual]:
                        print('[SOM] Acerto de letra')
                        if SOM_ACERTO:
                            SOM_ACERTO.play()
                        multiplayer_letras_adivinhadas[multiplayer_indice_atual] = letra_digitada
                        for i, l in enumerate(multiplayer_letras_embaralhadas):
                            if l == letra_digitada and not multiplayer_letras_embaralhadas_usadas[i]:
                                multiplayer_letras_embaralhadas_usadas[i] = True
                                break
                        if multiplayer_indice_atual < len(multiplayer_letras_adivinhadas) - 1:
                            multiplayer_indice_atual += 1
                        else:
                            if "".join(multiplayer_letras_adivinhadas) == multiplayer_palavra_secreta:
                                tempo = time.time() - multiplayer_tempo_inicio + multiplayer_erros * PENALIDADE_ERRO
                                definidor, adivinha = pares[rodada_idx]
                                tempos[adivinha] = tempo
                                erros[adivinha] = multiplayer_erros
                                palavras[adivinha] = multiplayer_palavra_secreta
                                rodada_idx += 1
                                # 2. No final da rodada (acerto ou desistência), antes de mudar o estado, iniciar a transição:
                                transicao_multiplayer_timer = pygame.time.get_ticks() + 2000  # 2 segundos de transição
                                if rodada_idx >= len(pares):
                                    transicao_multiplayer_msg = "Exibindo ranking..."
                                    estado_multiplayer = "transicao_ranking"
                                else:
                                    transicao_multiplayer_msg = f"Próxima rodada ({rodada_idx+1}) em 2 segundos..."
                                    estado_multiplayer = "transicao_rodada"
                                return
                    else:
                        print('[SOM] Erro de letra')
                        if SOM_ERRO:
                            SOM_ERRO.play()
                        multiplayer_erros += 1
                        multiplayer_letras_erradas.add(letra_digitada)
                        multiplayer_feedback_erro_idx = multiplayer_indice_atual
                        multiplayer_feedback_erro_timer = FEEDBACK_ERRO_DURATION
                        multiplayer_shake_timer = SHAKE_DURATION
                elif event.key == pygame.K_LEFT:
                    if multiplayer_indice_atual > 0:
                        multiplayer_indice_atual -= 1
                elif event.key == pygame.K_RIGHT:
                    if multiplayer_indice_atual < len(multiplayer_letras_adivinhadas) - 1:
                        multiplayer_indice_atual += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_desistir_rect.collidepoint(event.pos):
                    multiplayer_mensagem_final = f"Você desistiu! A palavra era '{multiplayer_palavra_secreta}'."
                    multiplayer_tempo_final = tempo_atual
                    multiplayer_erros_final = multiplayer_erros
                    estado_multiplayer = "final_multiplayer"
                    return
                for rect, letra, idx in letras_embaralhadas_pos:
                    if rect.collidepoint(event.pos) and not multiplayer_letras_embaralhadas_usadas[idx]:
                        if letra == multiplayer_palavra_secreta[multiplayer_indice_atual]:
                            print('[SOM] Acerto de letra')
                            if SOM_ACERTO:
                                SOM_ACERTO.play()
                            multiplayer_letras_adivinhadas[multiplayer_indice_atual] = letra
                            multiplayer_letras_embaralhadas_usadas[idx] = True
                            multiplayer_letras_tentadas.add(letra)
                            if multiplayer_indice_atual < len(multiplayer_letras_adivinhadas) - 1:
                                multiplayer_indice_atual += 1
                            else:
                                if "".join(multiplayer_letras_adivinhadas) == multiplayer_palavra_secreta:
                                    tempo = time.time() - multiplayer_tempo_inicio + multiplayer_erros * PENALIDADE_ERRO
                                    definidor, adivinha = pares[rodada_idx]
                                    tempos[adivinha] = tempo
                                    erros[adivinha] = multiplayer_erros
                                    palavras[adivinha] = multiplayer_palavra_secreta
                                    rodada_idx += 1
                                    # 2. No final da rodada (acerto ou desistência), antes de mudar o estado, iniciar a transição:
                                    transicao_multiplayer_timer = pygame.time.get_ticks() + 2000  # 2 segundos de transição
                                    if rodada_idx >= len(pares):
                                        transicao_multiplayer_msg = "Exibindo ranking..."
                                        estado_multiplayer = "transicao_ranking"
                                    else:
                                        transicao_multiplayer_msg = f"Próxima rodada ({rodada_idx+1}) em 2 segundos..."
                                        estado_multiplayer = "transicao_rodada"
                                    return
                        else:
                            print('[SOM] Erro de letra')
                            if SOM_ERRO:
                                SOM_ERRO.play()
                            multiplayer_erros += 1
                            multiplayer_letras_erradas.add(letra)
                            multiplayer_feedback_erro_idx = multiplayer_indice_atual
                            multiplayer_feedback_erro_timer = FEEDBACK_ERRO_DURATION
                            multiplayer_feedback_erro_circulo_idx = idx  # círculo da letra clicada
                            multiplayer_feedback_erro_circulo_timer = FEEDBACK_ERRO_DURATION
                            multiplayer_shake_timer = SHAKE_DURATION
                        break
        pygame.display.flip()
    elif estado_multiplayer == "ranking":
        screen.fill(COR_FUNDO_PRINCIPAL)
        btn_menu_rect = desenhar_tela_final_multiplayer(
            screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO,
            nomes_jogadores, tempos, palavras, erros
        )
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                voltar_menu()
                estado_multiplayer = "config"
                rodada_idx = 0
                tempos.clear()
                erros.clear()
                palavras.clear()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn_menu_rect.collidepoint(mx, my):
                    voltar_menu()
                    estado_multiplayer = "config"
                    rodada_idx = 0
                    tempos.clear()
                    erros.clear()
                    palavras.clear()
                    return
        pygame.display.flip()
    # 3. Adicionar blocos para os estados 'transicao_rodada' e 'transicao_ranking' em tratar_multiplayer:
    elif estado_multiplayer == "transicao_rodada":
        screen.fill(COR_FUNDO_PRINCIPAL)
        msg = FONT_BIG.render(transicao_multiplayer_msg, True, (0,0,0))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
        if pygame.time.get_ticks() >= transicao_multiplayer_timer:
            estado_multiplayer = "definir_palavra"
        pygame.display.flip()
    elif estado_multiplayer == "transicao_ranking":
        screen.fill(COR_FUNDO_PRINCIPAL)
        msg = FONT_BIG.render(transicao_multiplayer_msg, True, (0,0,0))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
        if pygame.time.get_ticks() >= transicao_multiplayer_timer:
            estado_multiplayer = "ranking"
        pygame.display.flip()


# Inicialize o número de jogadores do multiplayer
num_jogadores = 2

# Inicialize o número máximo de letras por rodada do multiplayer
default_max_letras = 6
max_letras_rodada = default_max_letras

def desenhar_tela_final_multiplayer(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, nomes_jogadores, tempos, palavras, erros):
    # Gradiente de fundo (PALETA PADRÃO)
    screen_width, screen_height = screen.get_size()
    from interface import criar_gradiente_vertical, desenhar_particulas_fundo
    gradiente = criar_gradiente_vertical(screen_width, screen_height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    import pygame
    tempo = pygame.time.get_ticks()
    desenhar_particulas_fundo(screen, tempo)
    
    # Caixa centralizada (cores da paleta padrão)
    largura, altura = 700, 500
    x = (screen.get_width() - largura) // 2
    y = (screen.get_height() - altura) // 2
    pygame.draw.rect(screen, (235, 220, 190), (x, y, largura, altura), border_radius=24)  # Bege da paleta
    pygame.draw.rect(screen, (120, 100, 80), (x, y, largura, altura), 4, border_radius=24)  # Borda terrosa
    # Determinar ganhador
    ranking = sorted([(nomes_jogadores[i], tempos[i], palavras[i]) for i in range(len(nomes_jogadores))], key=lambda x: x[1])
    ganhador = ranking[0][0]
    frase = f"Parabéns, {ganhador}! Você foi o grande vencedor!"
    # Efeito de onda
    amplitude = 18  # altura da onda
    frequencia = 0.25  # velocidade da onda
    base_x = screen.get_width() // 2 - FONT_BIG.size(frase)[0] // 2
    base_y = 80
    t = time.time()
    x_letra = base_x
    for i, letra in enumerate(frase):
        offset_y = int(math.sin(t * 2 * math.pi * frequencia + i * 0.3) * amplitude)
        letra_surf = FONT_BIG.render(letra, True, COR_TEXTO_CLARO_DESTACADO)
        screen.blit(letra_surf, (x_letra, base_y + offset_y))
        x_letra += letra_surf.get_width()
    # Título
    fonte_titulo = pygame.font.SysFont("arial", 36, bold=True)
    titulo = fonte_titulo.render("Ranking Final", True, (196, 102, 31))  # Laranja destacado
    screen.blit(titulo, (x + (largura - titulo.get_width())//2, y + 24))
    # Ranking melhorado
    y0 = y + 120
    linha_h = 60  # Aumentado espaçamento
    for i, (nome, tempo, palavra) in enumerate(ranking):
        # Fontes mais amigáveis
        fonte_nome = pygame.font.SysFont("arial", 28, bold=True)
        fonte_tempo = pygame.font.SysFont("arial", 26, bold=False)
        fonte_palavra = pygame.font.SysFont("arial", 24, bold=False)
        
        # Cores mais amigáveis
        cor_nome = (95, 111, 82)  # Verde escuro
        cor_tempo = (196, 102, 31)  # Laranja
        cor_palavra = (120, 100, 60)  # Marrom suave
        cor_rank = (80, 80, 80)  # Cinza escuro
        
        # Renderizar cada parte separadamente
        rank_label = fonte_nome.render(f"{i+1}. ", True, cor_rank)
        nome_label = fonte_nome.render(f"{nome} - ", True, cor_nome)
        tempo_str = f"{tempo:.2f}s"
        tempo_label = fonte_tempo.render(tempo_str, True, cor_tempo)
        palavra_label = fonte_palavra.render(f" ({palavra})", True, cor_palavra)
        
        # Calcular posição centralizada
        x_centro = x + (largura - (rank_label.get_width() + nome_label.get_width() + tempo_label.get_width() + palavra_label.get_width())) // 2
        y_linha = y0 + i*linha_h
        
        # Desenhar cada parte
        screen.blit(rank_label, (x_centro, y_linha))
        screen.blit(nome_label, (x_centro + rank_label.get_width(), y_linha))
        screen.blit(tempo_label, (x_centro + rank_label.get_width() + nome_label.get_width(), y_linha))
        screen.blit(palavra_label, (x_centro + rank_label.get_width() + nome_label.get_width() + tempo_label.get_width(), y_linha))
    
    # Botão Menu (paleta padrão)
    btn_w, btn_h = 200, 60
    btn_menu_rect = pygame.Rect(x + largura//2 - btn_w//2, y + altura - 80, btn_w, btn_h)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover = btn_menu_rect.collidepoint(mouse_x, mouse_y)
    
    # Usar aplicação de gradiente sem vazamento
    from interface import aplicar_gradiente_com_bordas
    cor_btn_topo = (180, 120, 60) if hover else (160, 100, 50)  # Laranja da paleta
    cor_btn_baixo = (160, 100, 40) if hover else (140, 80, 30)
    
    aplicar_gradiente_com_bordas(screen, btn_menu_rect, cor_btn_topo, cor_btn_baixo, 14)
    pygame.draw.rect(screen, (120, 70, 30), btn_menu_rect, 3, border_radius=14)
    
    fonte_btn = pygame.font.SysFont("arial", 24, bold=True)
    menu_label = fonte_btn.render("Menu", True, (255,255,255))
    screen.blit(menu_label, (btn_menu_rect.x + (btn_menu_rect.w - menu_label.get_width())//2, btn_menu_rect.y + (btn_menu_rect.h - menu_label.get_height())//2))
    return btn_menu_rect

# Carregamento de configurações
def carregar_config():
    global VOLUME_SOM, VOLUME_MUSICA, SOM_ATIVO, MUSICA_ATIVA, MODO_TELA_CHEIA, RESOLUCAO_ATUAL
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            VOLUME_SOM = cfg.get('VOLUME_SOM', 1.0)
            VOLUME_MUSICA = cfg.get('VOLUME_MUSICA', 1.0)
            SOM_ATIVO = cfg.get('SOM_ATIVO', True)
            MUSICA_ATIVA = cfg.get('MUSICA_ATIVA', True)
            MODO_TELA_CHEIA = cfg.get('MODO_TELA_CHEIA', False)
            RESOLUCAO_ATUAL = tuple(cfg.get('RESOLUCAO_ATUAL', (800,600)))
    except Exception:
        pass
def salvar_config():
    cfg = {
        'VOLUME_SOM': VOLUME_SOM,
        'VOLUME_MUSICA': VOLUME_MUSICA,
        'SOM_ATIVO': SOM_ATIVO,
        'MUSICA_ATIVA': MUSICA_ATIVA,
        'MODO_TELA_CHEIA': MODO_TELA_CHEIA,
        'RESOLUCAO_ATUAL': RESOLUCAO_ATUAL
    }
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

# Inicialização das configurações
VOLUME_SOM = 1.0
VOLUME_MUSICA = 1.0
SOM_ATIVO = True
MUSICA_ATIVA = True
MODO_TELA_CHEIA = False
RESOLUCAO_ATUAL = (800, 600)

# Carregar configurações salvas
carregar_config()

# Aplicar volumes carregados aos sons (com verificação de segurança)
if SOM_ACERTO:  # Verifica se os sons foram carregados com sucesso
    for s in [SOM_ACERTO, SOM_ERRO, SOM_INICIAR, SOM_FIM, SOM_VITORIA, SOM_CLIQUE]:
        if s:  # Verificação adicional para cada som
            s.set_volume(VOLUME_SOM if SOM_ATIVO else 0)
pygame.mixer.music.set_volume(VOLUME_MUSICA if MUSICA_ATIVA else 0)

# Carregar palavras usadas de arquivo
try:
    with open(PALAVRAS_USADAS_PATH, 'r', encoding='utf-8') as f:
        palavras_usadas = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Aviso: {e}. Criando novo arquivo de palavras usadas.")
    palavras_usadas = set()

# Variáveis de estado para sliders e botões
slider_som_drag = False
slider_mus_drag = False
btn_som_pressed = False
btn_mus_pressed = False

def salvar_ranking_solo(nome, palavra, tempo, dificuldade):
    registro = {
        "nome": nome,
        "palavra": palavra,
        "tempo": tempo,
        "dificuldade": dificuldade
    }
    try:
        with open('ranking_solo.json', 'r', encoding='utf-8') as f:
            ranking = json.load(f)
    except Exception:
        ranking = []
    ranking.append(registro)
    with open('ranking_solo.json', 'w', encoding='utf-8') as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

def mostrar_ranking_dificuldade_atual(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, dificuldade):
    import json
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render(f"Ranking - {dificuldade}", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))
    try:
        with open('ranking_solo.json', 'r', encoding='utf-8') as f:
            ranking = json.load(f)
    except Exception:
        ranking = []
    top10 = [r for r in ranking if r.get('dificuldade') == dificuldade]
    top10 = sorted(top10, key=lambda x: x.get('tempo', 9999))[:10]
    y_base = 160
    espacamento = 48
    for i, r in enumerate(top10):
        nome = r.get('nome', '-')
        tempo = r.get('tempo', 0)
        tempo_str = f"{tempo:.2f}s"
        linha = f"{i+1}. {nome} - {tempo_str}"
        label = FONT_MED.render(linha, True, COR_TEXTO_CLARO)
        screen.blit(label, (screen.get_width()//2 - label.get_width()//2, y_base + i*espacamento))
    voltar = FONT_SMALL.render("Pressione qualquer tecla para continuar", True, COR_TEXTO_CLARO)
    y_voltar = y_base + len(top10)*espacamento + 40
    screen.blit(voltar, (screen.get_width()//2 - voltar.get_width()//2, y_voltar))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

while True:
    try:
        dt = clock.tick(60)
        if feedback_erro_timer > 0:
            feedback_erro_timer -= dt
            if feedback_erro_timer <= 0:
                feedback_erro_idx = -1
        if feedback_erro_circulo_timer > 0:
            feedback_erro_circulo_timer -= dt
            if feedback_erro_circulo_timer <= 0:
                feedback_erro_circulo_idx = -1
        if shake_timer > 0:
            shake_timer -= dt
        if tela_atual == TELA_NOME_SOLO:
            cursor_timer += dt
            if cursor_timer >= CURSOR_BLINK_INTERVAL:
                cursor_visible = not cursor_visible
                cursor_timer = 0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sair()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if tela_atual != TELA_CONFIG:
                    voltar_menu()
                    if 'estado_multiplayer' in globals():
                        estado_multiplayer = "config"
                        if 'rodada_idx' in globals(): rodada_idx = 0
                        if 'tempos' in globals(): tempos.clear()
                        if 'erros' in globals(): erros.clear()
                        if 'palavras' in globals(): palavras.clear()
                    fim_rodada = False
                    continue
            if tela_atual == TELA_MENU:
                for botao in botoes_menu:
                    botao.checar_evento(event)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(MUSICA_MENU_PATH)
                    pygame.mixer.music.play(-1)
            elif tela_atual == TELA_NOME_SOLO:
                if event.type == pygame.MOUSEMOTION:
                    botao_iniciar_nome.checar_evento(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        input_ativo = True
                    else:
                        input_ativo = False
                    # Só processar clique do botão se o nome não estiver vazio
                    if nome_jogador.strip() != "":
                        botao_iniciar_nome.checar_evento(event)
                if event.type == pygame.KEYDOWN:
                    if input_ativo:
                        if SOM_CLIQUE:  # Verificação de segurança
                            SOM_CLIQUE.play()
                        if event.key == pygame.K_RETURN:
                            # Só permitir avançar se o nome não estiver vazio
                            if nome_jogador.strip() != "":
                                ir_para_dificuldade()
                        elif event.key == pygame.K_BACKSPACE:
                            nome_jogador = nome_jogador[:-1]
                        elif len(nome_jogador) < 20 and event.unicode.isprintable():
                            nome_jogador += event.unicode.upper()
            elif tela_atual == TELA_DIFICULDADE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in btns_dificuldade:
                        if btn["rect"].collidepoint(event.pos):
                            dificuldade_escolhida = btn["label"]
                            lista_base = palavras_dicionario.get(dificuldade_escolhida, [])
                            carregando_palavra = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    voltar_menu()
            elif tela_atual == TELA_JOGO:
                if rodada_ativa:
                    if event.type == pygame.KEYDOWN and rodada_ativa:
                        if SOM_CLIQUE:
                            SOM_CLIQUE.play()
                        if event.unicode.isalpha() and len(event.unicode) == 1:
                            letra_digitada = event.unicode.upper()
                            letras_tentadas.add(letra_digitada)
                            if letra_digitada == palavra_original[indice_atual]:
                                print('[SOM] Acerto de letra (solo)')
                                if SOM_ACERTO:
                                    SOM_ACERTO.play()
                                letras_adivinhadas[indice_atual] = letra_digitada
                                # Marca a primeira letra embaralhada disponível como usada
                                for i, (l) in enumerate(palavra_embaralhada):
                                    if l == letra_digitada and not letras_embaralhadas_usadas[i]:
                                        letras_embaralhadas_usadas[i] = True
                                        break
                                if indice_atual < len(letras_adivinhadas) - 1:
                                    indice_atual += 1
                                else:
                                    if "".join(letras_adivinhadas) == palavra_original:
                                        finalizar_rodada(True)
                            else:
                                print('[SOM] Erro de letra (solo)')
                                if SOM_ERRO:
                                    SOM_ERRO.play()
                                erros_exemplo += 1
                                letras_erradas.add(letra_digitada)
                                feedback_erro_idx = indice_atual
                                feedback_erro_timer = FEEDBACK_ERRO_DURATION
                                shake_timer = SHAKE_DURATION
                        elif event.key == pygame.K_LEFT:
                            if indice_atual > 0:
                                indice_atual -= 1
                        elif event.key == pygame.K_RIGHT:
                            if indice_atual < len(letras_adivinhadas) - 1:
                                indice_atual += 1
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if botao_desistir_rect.collidepoint(event.pos):
                            for i, l in enumerate(palavra_original):
                                letras_adivinhadas[i] = l
                                # Marca todas as letras embaralhadas como usadas
                                for j, (le) in enumerate(palavra_embaralhada):
                                    if le == l:
                                        letras_embaralhadas_usadas[j] = True
                            finalizar_rodada(False)
                        # Clique nas letras embaralhadas
                        for rect, letra, idx in letras_embaralhadas_pos:
                            if rect.collidepoint(event.pos) and not letras_embaralhadas_usadas[idx]:
                                if letra == palavra_original[indice_atual]:
                                    print('[SOM] Acerto de letra (solo)')
                                    if SOM_ACERTO:
                                        SOM_ACERTO.play()
                                    letras_adivinhadas[indice_atual] = letra
                                    letras_embaralhadas_usadas[idx] = True
                                    letras_tentadas.add(letra)
                                    if indice_atual < len(letras_adivinhadas) - 1:
                                        indice_atual += 1
                                    else:
                                        if "".join(letras_adivinhadas) == palavra_original:
                                            finalizar_rodada(True)
                                else:
                                    print('[SOM] Erro de letra (solo)')
                                    if SOM_ERRO:
                                        SOM_ERRO.play()
                                    erros_exemplo += 1
                                    letras_erradas.add(letra)
                                    feedback_erro_idx = indice_atual  # quadrado da posição atual
                                    feedback_erro_timer = FEEDBACK_ERRO_DURATION
                                    feedback_erro_circulo_idx = idx  # círculo da letra clicada
                                    feedback_erro_circulo_timer = FEEDBACK_ERRO_DURATION
                                    shake_timer = SHAKE_DURATION
                                break
                elif fim_rodada:
                    btn_jogar_rect, btn_menu_rect, btn_def_rect = desenhar_tela_final(
                        screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO,
                        mensagem_final, tempo_exemplo, erros_exemplo, dificuldade_escolhida
                    )
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_jogar_rect.collidepoint(event.pos):
                            palavras_usadas.add(palavra_original)
                            desenhar_carregando_palavra_animado(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO)
                            pygame.display.flip()
                            iniciar_jogo_solo()
                        elif btn_menu_rect.collidepoint(event.pos):
                            voltar_menu()
                        elif btn_def_rect.collidepoint(event.pos):
                            popup_definicao(palavra_original)
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
            if tela_atual == "rodada_multiplayer":
                tratar_multiplayer(events)
        if tela_atual == TELA_MENU:
            desenhar_menu(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, botoes_menu)
        elif tela_atual == TELA_CONFIG:
            RESOLUCAO_ATUAL = screen.get_size()
            btn_reset_palavras, btn_reset_ranking, btn_salvar_sair = desenhar_config(
                screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO,
                SOM_ATIVO, MUSICA_ATIVA, VOLUME_SOM, VOLUME_MUSICA, RESOLUCAO_ATUAL
            )
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    voltar_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    y_base = 140 + 48 + 44 + 60 + 48
                    altura_btn = 36
                    # Botões de volume efeitos
                    btn_menos_som = pygame.Rect(370, 140+48, 36, 32)
                    btn_mais_som = pygame.Rect(370+36+8, 140+48, 36, 32)
                    if btn_menos_som.collidepoint(mx, my):
                        VOLUME_SOM = max(0.0, VOLUME_SOM - 0.1)
                        for s in [SOM_ACERTO, SOM_ERRO, SOM_INICIAR, SOM_FIM, SOM_VITORIA, SOM_CLIQUE]:
                            if s:  # Verificação de segurança
                                s.set_volume(VOLUME_SOM if SOM_ATIVO else 0)
                        salvar_config()
                    if btn_mais_som.collidepoint(mx, my):
                        VOLUME_SOM = min(1.0, VOLUME_SOM + 0.1)
                        for s in [SOM_ACERTO, SOM_ERRO, SOM_INICIAR, SOM_FIM, SOM_VITORIA, SOM_CLIQUE]:
                            if s:  # Verificação de segurança
                                s.set_volume(VOLUME_SOM if SOM_ATIVO else 0)
                        salvar_config()
                    # Botões de volume música
                    btn_menos_mus = pygame.Rect(370, 140+48+44, 36, 32)
                    btn_mais_mus = pygame.Rect(370+36+8, 140+48+44, 36, 32)
                    if btn_menos_mus.collidepoint(mx, my):
                        VOLUME_MUSICA = max(0.0, VOLUME_MUSICA - 0.1)
                        pygame.mixer.music.set_volume(VOLUME_MUSICA if MUSICA_ATIVA else 0)
                        salvar_config()
                    if btn_mais_mus.collidepoint(mx, my):
                        VOLUME_MUSICA = min(1.0, VOLUME_MUSICA + 0.1)
                        pygame.mixer.music.set_volume(VOLUME_MUSICA if MUSICA_ATIVA else 0)
                        salvar_config()
                    # Botões de ativar/desativar som/música
                    x_btn = 620
                    altura_btn_peq = 32
                    y_som_slider = 140 + 48
                    y_mus_slider = y_som_slider + 44
                    btn_som_w = FONT_SMALL.size("Ativo")[0] + 24 if SOM_ATIVO else FONT_SMALL.size("Inativo")[0] + 24
                    btn_som = pygame.Rect(x_btn, y_som_slider-8, btn_som_w, altura_btn_peq)
                    btn_mus_w = FONT_SMALL.size("Ativo")[0] + 24 if MUSICA_ATIVA else FONT_SMALL.size("Inativo")[0] + 24
                    btn_mus = pygame.Rect(x_btn, y_mus_slider-8, btn_mus_w, altura_btn_peq)
                    if btn_som.collidepoint(mx, my):
                        SOM_ATIVO = not SOM_ATIVO
                        for s in [SOM_ACERTO, SOM_ERRO, SOM_INICIAR, SOM_FIM, SOM_VITORIA, SOM_CLIQUE]:
                            if s:  # Verificação de segurança
                                s.set_volume(VOLUME_SOM if SOM_ATIVO else 0)
                        salvar_config()
                    if btn_mus.collidepoint(mx, my):
                        MUSICA_ATIVA = not MUSICA_ATIVA
                        if MUSICA_ATIVA:
                            pygame.mixer.music.set_volume(VOLUME_MUSICA)
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.set_volume(0)
                            pygame.mixer.music.stop()
                        salvar_config()
                    # Botão limpar palavras usadas
                    if btn_reset_palavras.collidepoint(mx, my):
                        palavras_usadas.clear()
                        with open('palavras_usadas.json', 'w', encoding='utf-8') as f:
                            json.dump(list(palavras_usadas), f, ensure_ascii=False, indent=2)
                        mensagem_config = "Palavras usadas limpas!"
                        mensagem_timer = pygame.time.get_ticks()
                    # Botão resetar ranking
                    if btn_reset_ranking.collidepoint(mx, my):
                        try:
                            with open('ranking_solo.json', 'w', encoding='utf-8') as f:
                                json.dump([], f)
                            mensagem_config = "Ranking resetado!"
                            mensagem_timer = pygame.time.get_ticks()
                        except Exception:
                            mensagem_config = "Erro ao resetar ranking."
                            mensagem_timer = pygame.time.get_ticks()
                    # Botão Salvar e Sair
                    if btn_salvar_sair.collidepoint(mx, my):
                        salvar_config()
                        voltar_menu()
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    x_slider = 370
                    altura_slider = 16
                    y_som_slider = 140 + 48
                    y_mus_slider = y_som_slider + 44 + 60
                    if slider_som_drag:
                        VOLUME_SOM = min(max((mx-x_slider)/200, 0), 1)
                        for s in [SOM_ACERTO, SOM_ERRO, SOM_INICIAR, SOM_FIM, SOM_VITORIA, SOM_CLIQUE]:
                            if s:  # Verificação de segurança
                                s.set_volume(VOLUME_SOM if SOM_ATIVO else 0)
                        salvar_config()
                    if slider_mus_drag:
                        VOLUME_MUSICA = min(max((mx-x_slider)/200, 0), 1)
                        pygame.mixer.music.set_volume(VOLUME_MUSICA if MUSICA_ATIVA else 0)
                        salvar_config()
                elif event.type == pygame.MOUSEBUTTONUP:
                    slider_som_drag = False
                    slider_mus_drag = False
        elif tela_atual == TELA_PLACAR:
                desenhar_placar(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO)
        elif tela_atual == TELA_DIFICULDADE:
                if carregando_palavra:
                    desenhar_carregando_palavra_animado(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO)
                    pygame.display.flip()
                    iniciar_jogo_solo()
                    carregando_palavra = False
                else:
                    desenhar_dificuldade(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, btns_dificuldade, btn_dificuldade_hover)
        elif tela_atual == TELA_JOGO:
                if fim_rodada:
                    btn_jogar_rect, btn_menu_rect, btn_def_rect = desenhar_tela_final(
                        screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO,
                        mensagem_final, tempo_exemplo, erros_exemplo, dificuldade_escolhida
                    )
                else:
                    desenhar_jogo(
                        screen, FONT_SMALL, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, cor_input_inativo, cor_input_borda,
                        rodada_ativa, nome_jogador_exemplo, tempo_exemplo, erros_exemplo, palavra_embaralhada, letras_embaralhadas_usadas,
                        letras_embaralhadas_pos, palavra_original, letras_adivinhadas, indice_atual, feedback_erro_idx, feedback_erro_timer,
                        FEEDBACK_ERRO_DURATION, feedback_erro_circulo_idx, feedback_erro_circulo_timer, botao_desistir_rect, fim_rodada, shake_timer
                    )
        elif tela_atual == TELA_NOME_SOLO:
                desenhar_nome_solo(
                    screen, FONT_BIG, FONT_SMALL, cor_input_ativo, cor_input_inativo, cor_input_borda, input_rect, input_ativo,
                    nome_jogador, cursor_visible, botao_iniciar_nome
                )
            # ADICIONAR SUPORTE À TELA DE CONFIG MULTIPLAYER
        elif tela_atual == "config_multiplayer":
                tratar_multiplayer(events)
        pygame.display.flip()
        # --- Som de iniciar rodada (solo) ---
        if tela_atual == TELA_JOGO and rodada_ativa and not som_iniciar_tocou:
            print('[SOM] Iniciar rodada (solo)')
            if SOM_INICIAR:  # Verificação de segurança
                SOM_INICIAR.play()
            som_iniciar_tocou = True
        # Resetar flags ao iniciar nova rodada
        if tela_atual == TELA_JOGO and not rodada_ativa:
            som_iniciar_tocou = False
            som_fim_tocou = False
        # --- Som de iniciar rodada (multiplayer) ---
        if 'estado_multiplayer' in globals() and estado_multiplayer == 'adivinhar' and not multiplayer_som_iniciar_tocou:
            print('[SOM] Iniciar rodada (multiplayer)')
            if SOM_INICIAR:
                SOM_INICIAR.play()
            multiplayer_som_iniciar_tocou = True
        # --- Som de vitória multiplayer ---
        if 'estado_multiplayer' in globals() and estado_multiplayer == 'adivinhar' and len(multiplayer_letras_adivinhadas) > 0 and \
           ''.join(multiplayer_letras_adivinhadas) == multiplayer_palavra_secreta and rodada_idx < len(pares) - 1 and not multiplayer_som_vitoria_tocou:
            print('[SOM] Vitória multiplayer')
            if SOM_VITORIA:
                SOM_VITORIA.play()
            multiplayer_som_vitoria_tocou = True
        # Resetar flags multiplayer ao iniciar nova rodada
        if 'estado_multiplayer' in globals() and estado_multiplayer == 'definir_palavra':
            multiplayer_som_iniciar_tocou = False
            multiplayer_som_vitoria_tocou = False
        # Detectar transição de fim_rodada: False -> True (solo)
        if tela_atual == TELA_JOGO and fim_rodada and not fim_rodada_anterior:
            print('[SOM] Fim do jogo (solo)')
            # SOM_FIM.play()  # Removido para evitar repetição
        fim_rodada_anterior = fim_rodada
        # Resetar rodada_finalizada ao iniciar nova rodada ou voltar ao menu
        if tela_atual != TELA_JOGO or (tela_atual == TELA_JOGO and not fim_rodada):
            rodada_finalizada = False
        # Atualizar tempo no modo solo
        if tela_atual == TELA_JOGO and rodada_ativa:
            tempo_exemplo = time.time() - inicio_tempo
        # Exibir mensagem de feedback
        x_slider = 370  # Inicializar variáveis para evitar erro unbound
        y_base = 140 + 48 + 44 + 60 + 48
        altura_btn = 36
        if mensagem_config and pygame.time.get_ticks() - mensagem_timer < 2000:
            txt_msg = FONT_SMALL.render(mensagem_config, True, (80, 80, 80))
            screen.blit(txt_msg, (x_slider, y_base+altura_btn+80))
        elif mensagem_config:
            mensagem_config = ""

    except Exception as e:
            import traceback
            print("\n[ERRO NO LOOP PRINCIPAL]:", e)
            traceback.print_exc()
            pygame.quit()
            input("Pressione ENTER para sair...")
            break 