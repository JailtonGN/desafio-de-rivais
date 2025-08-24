#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da Tela de Configurações Corrigida
Verifica se a correção do gradiente resolve o erro de cor inválida
"""

import pygame
import sys
import os

# Adicionar o diretório atual ao path para importar a interface
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import desenhar_config

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste - Tela de Configurações Corrigida")

# Cores originais do jogo
COR_FUNDO_PRINCIPAL = (249, 235, 199)
COR_TEXTO_CLARO = (95, 111, 82)

# Fontes
FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# Loop de teste
clock = pygame.time.Clock()
rodando = True

print("🔧 Testando Tela de Configurações Corrigida")
print("✨ Verificando se o erro de cor inválida foi resolvido...")
print("\n🎮 ESC para sair do teste")

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
    
    try:
        # Testar a função de configurações
        btn1, btn2, btn3 = desenhar_config(
            screen, FONT_BIG, FONT_MED, FONT_SMALL,
            COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO,
            True,  # SOM_ATIVO
            True,  # MUSICA_ATIVA
            0.7,   # VOLUME_SOM
            0.5,   # VOLUME_MUSICA
            "1920x1080"  # RESOLUCAO_ATUAL
        )
        
        # Se chegou até aqui, funcionou!
        fonte_sucesso = pygame.font.SysFont("arial", 24, bold=True)
        sucesso_text = "✅ CORREÇÃO FUNCIONOU! Gradientes carregando corretamente."
        sucesso_surface = fonte_sucesso.render(sucesso_text, True, (0, 150, 0))
        screen.blit(sucesso_surface, (10, HEIGHT - 40))
        
    except Exception as e:
        # Se ainda houver erro, mostrar na tela
        print(f"❌ Erro ainda presente: {e}")
        screen.fill(COR_FUNDO_PRINCIPAL)
        
        fonte_erro = pygame.font.SysFont("arial", 32)
        erro_text = f"❌ Erro: {str(e)}"
        erro_surface = fonte_erro.render(erro_text, True, (200, 50, 50))
        screen.blit(erro_surface, (WIDTH//2 - erro_surface.get_width()//2, HEIGHT//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✅ Teste finalizado!")