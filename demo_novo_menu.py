#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo da Nova Interface do Menu
Mostra as melhorias visuais implementadas
"""

import pygame
import sys
import os

# Adicionar o diretório atual ao path para importar a interface
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import desenhar_menu

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo - Novo Menu Moderno")

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

# Classe de botão simples para demo
class BotaoDemo:
    def __init__(self, texto, x, y, w, h):
        self.texto = texto
        self.rect = pygame.Rect(x, y, w, h)
        self.hover = False
    
    def desenhar(self, surface):
        # Esta função não será usada no novo design,
        # mas precisa existir para compatibilidade
        pass

# Criar botões de demonstração
botoes_demo = [
    BotaoDemo("Iniciar Jogo Solo", WIDTH//2 - 180, 250, 360, 60),
    BotaoDemo("Iniciar Jogo Multiplayer", WIDTH//2 - 180, 320, 360, 60),
    BotaoDemo("Configurações", WIDTH//2 - 180, 390, 360, 60),
    BotaoDemo("Ranking", WIDTH//2 - 180, 460, 360, 60),
    BotaoDemo("Sair", WIDTH//2 - 180, 530, 360, 60),
]

# Loop principal da demonstração
clock = pygame.time.Clock()
rodando = True

print("🎨 Demo do Novo Menu Moderno")
print("✨ Melhorias implementadas:")
print("   • Gradiente de fundo")
print("   • Partículas sutis")
print("   • Texto com sombra e glow")
print("   • Botões com animações")
print("   • Efeitos de hover")
print("   • Visual profissional")
print("\n🎮 Pressione ESC para sair da demo")

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("🖱️  Clique detectado! (No jogo real, os botões funcionariam normalmente)")
    
    # Desenhar o novo menu
    desenhar_menu(
        screen, 
        FONT_BIG, 
        FONT_MED, 
        COR_FUNDO_PRINCIPAL, 
        COR_TEXTO_CLARO, 
        COR_TEXTO_CLARO_DESTACADO, 
        botoes_demo
    )
    
    # Instruções na tela
    font_instrucao = pygame.font.SysFont("arial", 16)
    instrucao = font_instrucao.render("Passe o mouse sobre os botões • ESC para sair", True, (80, 70, 50))
    screen.blit(instrucao, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)  # 60 FPS para animações suaves

pygame.quit()
print("\n✅ Demo finalizada! O novo visual está pronto para uso no jogo.")