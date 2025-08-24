#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo Completo - Todas as Telas Modernizadas
Demonstra todas as melhorias visuais implementadas no jogo
"""

import pygame
import sys
import os
import time

# Adicionar o diretório atual ao path para importar a interface
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import *

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo Completo - Jogo Modernizado")

# Cores originais do jogo
COR_FUNDO_PRINCIPAL = (249, 235, 199)
COR_TEXTO_CLARO = (95, 111, 82)
COR_TEXTO_CLARO_DESTACADO = (196, 102, 31)
COR_BOTAO = (169, 179, 136)
COR_BOTAO_HOVER = (185, 148, 112)
COR_BOTAO_TEXTO = (60, 60, 60)

# Fontes
FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# Estados da demo
DEMO_MENU = "menu"
DEMO_CONFIG = "config"
DEMO_PLACAR = "placar"
DEMO_DIFICULDADE = "dificuldade"
DEMO_JOGO = "jogo"
DEMO_CARREGANDO = "carregando"

estado_demo = DEMO_MENU
tempo_troca_automatica = pygame.time.get_ticks() + 5000  # 5 segundos por tela

# Classe de botão simples para demo
class BotaoDemo:
    def __init__(self, texto, x, y, w, h):
        self.texto = texto
        self.rect = pygame.Rect(x, y, w, h)
        self.hover = False
    
    def desenhar(self, surface):
        pass

# Dados de demonstração
botoes_demo = [
    BotaoDemo("Iniciar Jogo Solo", WIDTH//2 - 180, 250, 360, 60),
    BotaoDemo("Iniciar Jogo Multiplayer", WIDTH//2 - 180, 320, 360, 60),
    BotaoDemo("Configurações", WIDTH//2 - 180, 390, 360, 60),
    BotaoDemo("Ranking", WIDTH//2 - 180, 460, 360, 60),
    BotaoDemo("Sair", WIDTH//2 - 180, 530, 360, 60),
]

btns_dificuldade_demo = [
    {"label": "Fácil", "desc": "Palavras de 4-5 letras", "cor": (159, 180, 85), "hover": (120, 150, 60)},
    {"label": "Médio", "desc": "Palavras de 6-7 letras", "cor": (196, 102, 31), "hover": (160, 80, 20)},
    {"label": "Difícil", "desc": "Palavras de 8+ letras", "cor": (185, 148, 112), "hover": (140, 120, 80)},
]

# Loop principal da demonstração
clock = pygame.time.Clock()
rodando = True

def proxima_tela():
    global estado_demo, tempo_troca_automatica
    estados = [DEMO_MENU, DEMO_CONFIG, DEMO_PLACAR, DEMO_DIFICULDADE, DEMO_JOGO, DEMO_CARREGANDO]
    idx_atual = estados.index(estado_demo)
    estado_demo = estados[(idx_atual + 1) % len(estados)]
    tempo_troca_automatica = pygame.time.get_ticks() + 5000

def tela_anterior():
    global estado_demo, tempo_troca_automatica
    estados = [DEMO_MENU, DEMO_CONFIG, DEMO_PLACAR, DEMO_DIFICULDADE, DEMO_JOGO, DEMO_CARREGANDO]
    idx_atual = estados.index(estado_demo)
    estado_demo = estados[(idx_atual - 1) % len(estados)]
    tempo_troca_automatica = pygame.time.get_ticks() + 5000

print("🎨 Demo Completo - Jogo Modernizado")
print("✨ Todas as telas foram modernizadas com:")
print("   • Gradientes de fundo")
print("   • Partículas sutis")
print("   • Efeitos de sombra e glow")
print("   • Botões com animações")
print("   • Transições suaves")
print("   • Visual profissional")
print("\n🎮 Controles:")
print("   • ESPAÇO: Próxima tela")
print("   • BACKSPACE: Tela anterior")
print("   • ESC: Sair da demo")
print("   • Troca automática a cada 5 segundos")

while rodando:
    tempo_atual = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
            elif event.key == pygame.K_SPACE:
                proxima_tela()
            elif event.key == pygame.K_BACKSPACE:
                tela_anterior()
    
    # Troca automática de tela
    if tempo_atual >= tempo_troca_automatica:
        proxima_tela()
    
    # Desenhar tela atual
    try:
        if estado_demo == DEMO_MENU:
            desenhar_menu(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, 
                         COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, botoes_demo)
            
        elif estado_demo == DEMO_CONFIG:
            # Simular configurações
            btn1, btn2, btn3 = desenhar_config(screen, FONT_BIG, FONT_MED, FONT_SMALL, 
                                              COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, 
                                              True, True, 0.7, 0.5, "1920x1080")
            
        elif estado_demo == DEMO_PLACAR:
            desenhar_placar(screen, FONT_BIG, FONT_MED, FONT_SMALL, 
                           COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO)
            
        elif estado_demo == DEMO_DIFICULDADE:
            desenhar_dificuldade(screen, FONT_BIG, FONT_MED, FONT_SMALL, 
                                 COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, 
                                 btns_dificuldade_demo, None)
            
        elif estado_demo == DEMO_JOGO:
            # Simular jogo em andamento
            palavra_embaralhada = "NOPYHT"
            palavra_original = "PYTHON" 
            letras_adivinhadas = ["P", "Y", "", "", "", ""]
            letras_embaralhadas_usadas = [True, True, False, False, False, False]
            letras_embaralhadas_pos = []
            botao_desistir_rect = pygame.Rect(WIDTH - 200, HEIGHT - 100, 160, 60)
            
            desenhar_jogo(screen, FONT_SMALL, FONT_BIG, COR_FUNDO_PRINCIPAL, 
                         COR_TEXTO_CLARO, (230, 226, 195), (185, 148, 112),
                         True, "JOGADOR", 45.67, 2, palavra_embaralhada,
                         letras_embaralhadas_usadas, letras_embaralhadas_pos,
                         palavra_original, letras_adivinhadas, 2, -1, 0, 350,
                         -1, 0, botao_desistir_rect, False, 0)
            
        elif estado_demo == DEMO_CARREGANDO:
            desenhar_carregando_palavra_animado(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO)
            
    except Exception as e:
        print(f"Erro na tela {estado_demo}: {e}")
        # Fallback para tela em branco
        screen.fill(COR_FUNDO_PRINCIPAL)
        erro_font = pygame.font.SysFont("arial", 32)
        erro_text = erro_font.render(f"Erro na tela: {estado_demo}", True, (200, 50, 50))
        screen.blit(erro_text, (WIDTH//2 - erro_text.get_width()//2, HEIGHT//2))
    
    # Indicador da tela atual
    fonte_indicador = pygame.font.SysFont("arial", 18, bold=True)
    tempo_restante = max(0, (tempo_troca_automatica - tempo_atual) // 1000 + 1)
    
    indicador_text = f"Tela: {estado_demo.upper()} ({tempo_restante}s) - ESPAÇO: próxima | BACKSPACE: anterior | ESC: sair"
    indicador_surface = fonte_indicador.render(indicador_text, True, (80, 70, 50))
    
    # Fundo semi-transparente para o indicador
    fundo_indicador = pygame.Surface((WIDTH, 30), pygame.SRCALPHA)
    fundo_indicador.fill((255, 255, 255, 180))
    screen.blit(fundo_indicador, (0, 0))
    
    screen.blit(indicador_surface, (10, 8))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✅ Demo finalizada! Todas as telas estão modernizadas e prontas para uso.")