#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo das Telas Finais Modernizadas
Testa as telas de nome solo e tela final que foram recém implementadas
"""

import pygame
import sys
import os

# Adicionar o diretório atual ao path para importar a interface
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import desenhar_nome_solo, desenhar_tela_final

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo - Telas Finais Modernizadas")

# Cores originais do jogo
COR_FUNDO_PRINCIPAL = (249, 235, 199)
COR_TEXTO_CLARO = (95, 111, 82)
COR_TEXTO_CLARO_DESTACADO = (196, 102, 31)

# Fontes
FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# Estados da demo
DEMO_NOME = "nome"
DEMO_FINAL_VITORIA = "final_vitoria"
DEMO_FINAL_DERROTA = "final_derrota"

estado_demo = DEMO_NOME
tempo_troca_automatica = pygame.time.get_ticks() + 4000  # 4 segundos por tela

# Classe de botão simples para demo
class BotaoDemo:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
    
    def desenhar(self, surface):
        pass

# Dados de demonstração
nome_demo = "JOGADOR"
input_rect = pygame.Rect(WIDTH//2 - 200, 240, 400, 60)
input_ativo = True
cursor_visible = True
botao_demo = BotaoDemo()

# Loop principal da demonstração
clock = pygame.time.Clock()
rodando = True

def proxima_tela():
    global estado_demo, tempo_troca_automatica
    estados = [DEMO_NOME, DEMO_FINAL_VITORIA, DEMO_FINAL_DERROTA]
    idx_atual = estados.index(estado_demo)
    estado_demo = estados[(idx_atual + 1) % len(estados)]
    tempo_troca_automatica = pygame.time.get_ticks() + 4000

def tela_anterior():
    global estado_demo, tempo_troca_automatica
    estados = [DEMO_NOME, DEMO_FINAL_VITORIA, DEMO_FINAL_DERROTA]
    idx_atual = estados.index(estado_demo)
    estado_demo = estados[(idx_atual - 1) % len(estados)]
    tempo_troca_automatica = pygame.time.get_ticks() + 4000

print("🎨 Demo das Telas Finais Modernizadas")
print("✨ Telas implementadas:")
print("   • Tela de digitação de nome (modo solo)")
print("   • Tela final de vitória")
print("   • Tela final de derrota")
print("\n🎮 Controles:")
print("   • ESPAÇO: Próxima tela")
print("   • BACKSPACE: Tela anterior")
print("   • ESC: Sair da demo")
print("   • Troca automática a cada 4 segundos")

cursor_timer = 0

while rodando:
    tempo_atual = pygame.time.get_ticks()
    dt = clock.get_time()
    
    # Controlar cursor piscante
    cursor_timer += dt
    if cursor_timer >= 500:  # 500ms
        cursor_visible = not cursor_visible
        cursor_timer = 0
    
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
        if estado_demo == DEMO_NOME:
            desenhar_nome_solo(
                screen, FONT_BIG, FONT_SMALL,
                (255, 255, 255), (230, 226, 195), (185, 148, 112),
                input_rect, input_ativo, nome_demo, cursor_visible, botao_demo
            )
            
        elif estado_demo == DEMO_FINAL_VITORIA:
            btn1, btn2, btn3 = desenhar_tela_final(
                screen, FONT_BIG, FONT_MED, FONT_SMALL,
                COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO,
                "Parabéns! Você acertou a palavra 'PYTHON'!", 45.67, 2, "Médio"
            )
            
        elif estado_demo == DEMO_FINAL_DERROTA:
            btn1, btn2, btn3 = desenhar_tela_final(
                screen, FONT_BIG, FONT_MED, FONT_SMALL,
                COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO,
                "Você desistiu! A palavra era 'PYGAME'.", 73.45, 5, "Difícil"
            )
            
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
    
    nomes_telas = {
        DEMO_NOME: "DIGITAÇÃO DE NOME",
        DEMO_FINAL_VITORIA: "TELA FINAL - VITÓRIA", 
        DEMO_FINAL_DERROTA: "TELA FINAL - DERROTA"
    }
    
    indicador_text = f"Tela: {nomes_telas.get(estado_demo, estado_demo)} ({tempo_restante}s) - ESPAÇO: próxima | BACKSPACE: anterior | ESC: sair"
    indicador_surface = fonte_indicador.render(indicador_text, True, (80, 70, 50))
    
    # Fundo semi-transparente para o indicador
    fundo_indicador = pygame.Surface((WIDTH, 30), pygame.SRCALPHA)
    fundo_indicador.fill((255, 255, 255, 180))
    screen.blit(fundo_indicador, (0, 0))
    
    screen.blit(indicador_surface, (10, 8))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✅ Demo finalizada! As telas de nome e final estão modernizadas.")