#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste do Visual Sem Sombras
Verifica como ficou a interface após remoção das sombras
"""

import pygame
import sys
import os

# Adicionar o diretório atual ao path para importar a interface
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import desenhar_menu, desenhar_config

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste - Visual Sem Sombras")

# Cores originais do jogo
COR_FUNDO_PRINCIPAL = (249, 235, 199)
COR_TEXTO_CLARO = (95, 111, 82)
COR_TEXTO_CLARO_DESTACADO = (196, 102, 31)

# Fontes
FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# Estados
TELA_MENU = 0
TELA_CONFIG = 1
tela_atual = TELA_MENU

# Classe de botão simples para demo
class BotaoDemo:
    def __init__(self, texto, x, y, w, h):
        self.texto = texto
        self.rect = pygame.Rect(x, y, w, h)
        self.hover = False
    
    def desenhar(self, surface):
        pass

# Botões de demonstração
botoes_demo = [
    BotaoDemo("Menu Principal", WIDTH//2 - 180, 250, 360, 60),
    BotaoDemo("Configurações", WIDTH//2 - 180, 320, 360, 60),
    BotaoDemo("Ranking", WIDTH//2 - 180, 390, 360, 60),
    BotaoDemo("Sair", WIDTH//2 - 180, 460, 360, 60),
]

# Loop de teste
clock = pygame.time.Clock()
rodando = True

print("🎨 Testando Visual Sem Sombras")
print("✨ Sombras removidas para visual mais limpo")
print("\n🎮 Controles:")
print("   • ESPAÇO: Alternar entre Menu e Configurações")
print("   • ESC: Sair do teste")

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
            elif event.key == pygame.K_SPACE:
                tela_atual = 1 - tela_atual  # Alternar entre 0 e 1
    
    try:
        if tela_atual == TELA_MENU:
            desenhar_menu(
                screen, FONT_BIG, FONT_MED,
                COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO,
                botoes_demo
            )
            
            # Indicador
            fonte_indicador = pygame.font.SysFont("arial", 18, bold=True)
            indicador_text = "MENU PRINCIPAL (sem sombras) - ESPAÇO: Configurações | ESC: Sair"
            indicador_surface = fonte_indicador.render(indicador_text, True, (80, 70, 50))
            
        else:  # TELA_CONFIG
            btn1, btn2, btn3 = desenhar_config(
                screen, FONT_BIG, FONT_MED, FONT_SMALL,
                COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO,
                True, True, 0.7, 0.5, "1920x1080"
            )
            
            # Indicador
            fonte_indicador = pygame.font.SysFont("arial", 18, bold=True)
            indicador_text = "CONFIGURAÇÕES (sem sombras) - ESPAÇO: Menu | ESC: Sair"
            indicador_surface = fonte_indicador.render(indicador_text, True, (80, 70, 50))
        
        # Fundo do indicador
        fundo_indicador = pygame.Surface((WIDTH, 30), pygame.SRCALPHA)
        fundo_indicador.fill((255, 255, 255, 180))
        screen.blit(fundo_indicador, (0, 0))
        screen.blit(indicador_surface, (10, 8))
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        screen.fill(COR_FUNDO_PRINCIPAL)
        
        fonte_erro = pygame.font.SysFont("arial", 32)
        erro_text = f"❌ Erro: {str(e)}"
        erro_surface = fonte_erro.render(erro_text, True, (200, 50, 50))
        screen.blit(erro_surface, (WIDTH//2 - erro_surface.get_width()//2, HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✅ Teste finalizado! Visual sem sombras implementado.")