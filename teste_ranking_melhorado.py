#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste do Ranking Melhorado
Verifica as melhorias no alinhamento e fonte única para colocações
"""

import pygame
import sys
import os
import json

# Adicionar o diretório atual ao path para importar a interface
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface import desenhar_placar

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1400, 900  # Resolução maior para ver melhor as 3 colunas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teste - Ranking Melhorado")

# Cores do jogo
COR_FUNDO_PRINCIPAL = (249, 235, 199)
COR_TEXTO_CLARO = (95, 111, 82)

# Fontes
FONT_BIG = pygame.font.SysFont("arial", 48, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("arial", 24)

# Criar dados de teste para o ranking
dados_teste = [
    # Fácil
    {"nome": "João Silva", "tempo": 15.2, "palavra": "CASA", "dificuldade": "Fácil"},
    {"nome": "Maria", "tempo": 18.7, "palavra": "GATO", "dificuldade": "Fácil"},
    {"nome": "Pedro", "tempo": 22.1, "palavra": "FLOR", "dificuldade": "Fácil"},
    {"nome": "Ana Carolina", "tempo": 25.8, "palavra": "LIVRO", "dificuldade": "Fácil"},
    {"nome": "Carlos", "tempo": 28.3, "palavra": "MESA", "dificuldade": "Fácil"},
    
    # Médio
    {"nome": "Roberta", "tempo": 32.1, "palavra": "COMPUTADOR", "dificuldade": "Médio"},
    {"nome": "Alexandre", "tempo": 35.7, "palavra": "TELEFONE", "dificuldade": "Médio"},
    {"nome": "Fernanda", "tempo": 41.2, "palavra": "BICICLETA", "dificuldade": "Médio"},
    {"nome": "Ricardo", "tempo": 45.8, "palavra": "CADERNO", "dificuldade": "Médio"},
    
    # Difícil  
    {"nome": "Patricia", "tempo": 67.3, "palavra": "EXTRAORDINÁRIO", "dificuldade": "Difícil"},
    {"nome": "Guilherme", "tempo": 72.8, "palavra": "INCONSTITUCIONAL", "dificuldade": "Difícil"},
    {"nome": "Daniela", "tempo": 89.4, "palavra": "PARALELEPÍPEDO", "dificuldade": "Difícil"},
    {"nome": "Mauricio", "tempo": 95.1, "palavra": "ARQUITETURA", "dificuldade": "Difícil"}
]

# Salvar dados de teste no arquivo de ranking
try:
    with open('ranking_solo.json', 'w', encoding='utf-8') as f:
        json.dump(dados_teste, f, ensure_ascii=False, indent=2)
    print("✅ Dados de teste criados no ranking_solo.json")
except Exception as e:
    print(f"❌ Erro ao criar dados de teste: {e}")

# Loop principal
clock = pygame.time.Clock()
rodando = True

print("\n🎮 TESTE - TRUNCAMENTO INTELIGENTE")
print("="*50)
print("🧠 Truncamento otimizado:")
print("   • Cálculo dinâmico do espaço disponível")
print("   • Palavras só truncadas quando necessário")
print("   • Aproveita melhor o espaço das colunas")
print("   • 60% do espaço para nome, resto para palavra")
print("\n💡 Pressione ESC para sair")

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
    
    try:
        # Desenhar o ranking melhorado
        desenhar_placar(
            screen, 
            FONT_BIG, 
            FONT_MED, 
            FONT_SMALL, 
            COR_FUNDO_PRINCIPAL, 
            COR_TEXTO_CLARO
        )
        
        # Instruções na tela
        font_instrucao = pygame.font.SysFont("arial", 16)
        instrucoes = [
            "TRUNCAMENTO INTELIGENTE - Melhorias:",
            "✓ Cálculo dinâmico do espaço disponível",
            "✓ Palavras mostradas completas quando possível",
            "✓ Truncamento apenas quando necessário",
            "✓ Melhor aproveitamento do espaço das colunas",
            "✓ Balanço 60/40 entre nome e palavra"
        ]
        
        y_inst = 10
        for instrucao in instrucoes:
            cor = (60, 80, 40) if "✓" in instrucao else (80, 70, 50)
            instrucao_surface = font_instrucao.render(instrucao, True, cor)
            screen.blit(instrucao_surface, (10, y_inst))
            y_inst += 20
            
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
print("✅ Teste finalizado! Ranking melhorado implementado.")