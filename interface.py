import pygame
import json
import math
# Removido: from JogoPygame import SOM_CLIQUE

# Função auxiliar para aplicar gradiente com bordas arredondadas
def aplicar_gradiente_com_bordas(screen, rect, cor_topo, cor_baixo, border_radius=0):
    """Aplica gradiente com bordas arredondadas sem vazamento de cores"""
    # Para bordas arredondadas, usar cor sólida para evitar problemas
    if border_radius > 0:
        # Usar cor intermediária entre topo e baixo
        # Suporte para cores RGBA (transparência)
        if len(cor_topo) == 4 and len(cor_baixo) == 4:
            # Cores com alpha
            cor_media = (
                (cor_topo[0] + cor_baixo[0]) // 2,
                (cor_topo[1] + cor_baixo[1]) // 2,
                (cor_topo[2] + cor_baixo[2]) // 2,
                (cor_topo[3] + cor_baixo[3]) // 2
            )
            # Criar surface com alpha para bordas arredondadas
            temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, cor_media, 
                           pygame.Rect(0, 0, rect.width, rect.height), 
                           border_radius=border_radius)
            screen.blit(temp_surface, rect)
        else:
            # Cores RGB normais
            cor_media = (
                (cor_topo[0] + cor_baixo[0]) // 2,
                (cor_topo[1] + cor_baixo[1]) // 2,
                (cor_topo[2] + cor_baixo[2]) // 2
            )
            pygame.draw.rect(screen, cor_media, rect, border_radius=border_radius)
    else:
        # Se não tem bordas arredondadas, usar gradiente normal
        # Verificar se é RGBA
        if len(cor_topo) == 4 and len(cor_baixo) == 4:
            # Para RGBA, usar apenas RGB no gradiente
            cor_topo_rgb = cor_topo[:3]
            cor_baixo_rgb = cor_baixo[:3]
            gradiente = criar_gradiente_vertical(rect.width, rect.height, cor_topo_rgb, cor_baixo_rgb)
            # Aplicar alpha através de set_alpha na surface
            alpha_medio = (cor_topo[3] + cor_baixo[3]) // 2
            gradiente.set_alpha(alpha_medio)
            screen.blit(gradiente, rect)
        else:
            gradiente = criar_gradiente_vertical(rect.width, rect.height, cor_topo, cor_baixo)
            screen.blit(gradiente, rect)

# Função auxiliar para criar gradiente
def criar_gradiente_vertical(width, height, cor_topo, cor_baixo):
    """Cria uma surface com gradiente vertical"""
    gradient = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = int(cor_topo[0] * (1 - ratio) + cor_baixo[0] * ratio)
        g = int(cor_topo[1] * (1 - ratio) + cor_baixo[1] * ratio)
        b = int(cor_topo[2] * (1 - ratio) + cor_baixo[2] * ratio)
        
        # Garantir que os valores estão no range válido (0-255)
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        cor = (r, g, b)
        pygame.draw.line(gradient, cor, (0, y), (width, y))
    return gradient

# Função auxiliar para desenhar texto simples
def desenhar_texto_simples(surface, font, texto, cor_texto, x, y):
    """Desenha texto sem efeito de sombra"""
    # Garantir que a cor é válida
    def validar_cor(cor):
        if len(cor) >= 3:
            return (max(0, min(255, int(cor[0]))), 
                   max(0, min(255, int(cor[1]))), 
                   max(0, min(255, int(cor[2]))))
        return (0, 0, 0)
    
    cor_texto_valida = validar_cor(cor_texto)
    
    # Texto principal
    texto_surface = font.render(texto, True, cor_texto_valida)
    surface.blit(texto_surface, (x, y))
    return texto_surface

# Função auxiliar para desenhar retângulo simples
def desenhar_rect_simples(surface, cor_rect, rect, border_radius=0):
    """Desenha retângulo sem sombra projetada"""
    # Garantir que a cor é válida
    def validar_cor(cor):
        if len(cor) >= 3:
            return (max(0, min(255, int(cor[0]))), 
                   max(0, min(255, int(cor[1]))), 
                   max(0, min(255, int(cor[2]))))
        return (0, 0, 0)
    
    cor_valida = validar_cor(cor_rect)
    pygame.draw.rect(surface, cor_valida, rect, border_radius=border_radius)

# Função auxiliar para efeito de partículas
def desenhar_particulas_fundo(surface, tempo):
    """Desenha partículas sutis no fundo"""
    width, height = surface.get_size()
    for i in range(20):
        # Movimento suave das partículas
        x = (i * 97 + tempo * 0.5) % width
        y = (i * 73 + math.sin(tempo * 0.01 + i) * 20) % height
        alpha = int(30 + 20 * math.sin(tempo * 0.02 + i))
        
        # Criar surface temporária para transparência
        particle = pygame.Surface((4, 4), pygame.SRCALPHA)
        particle.fill((255, 255, 255, alpha))
        surface.blit(particle, (x, y))

# Função para desenhar o menu com visual moderno
def desenhar_menu(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, botoes_menu):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # === FUNDO COM GRADIENTE (PALETA PADRÃO) ===
    # Usando a mesma paleta da tela final para consistência
    cor_gradiente_topo = (240, 225, 195)  # Bege suave
    cor_gradiente_baixo = (210, 195, 165)  # Bege terroso
    gradiente = criar_gradiente_vertical(width, height, cor_gradiente_topo, cor_gradiente_baixo)
    screen.blit(gradiente, (0, 0))
    
    # === PARTÍCULAS SUTIS DE FUNDO ===
    desenhar_particulas_fundo(screen, tempo)
    
    # === TÍTULO PRINCIPAL COM SOMBRA E GLOW ===
    # Fonte maior e mais impactante para o título
    fonte_titulo_grande = pygame.font.SysFont("arial", 58, bold=True)
    
    # Efeito glow (múltiplas sombras)
    titulo_texto = "JOGO DE ADIVINHAÇÃO"
    x_titulo = width//2
    y_titulo = 60
    
    # Glow effect - múltiplas camadas
    for i in range(8, 0, -1):
        alpha = 30 - i * 3
        glow_surface = pygame.Surface((width, 100), pygame.SRCALPHA)
        glow_texto = fonte_titulo_grande.render(titulo_texto, True, COR_TEXTO_CLARO_DESTACADO)
        glow_x = x_titulo - glow_texto.get_width()//2
        glow_y = y_titulo
        glow_surface.blit(glow_texto, (glow_x + i, glow_y + i))
        screen.blit(glow_surface, (0, 0))
    
    # Título principal
    titulo_surface = desenhar_texto_simples(
        screen, fonte_titulo_grande, titulo_texto,
        COR_TEXTO_CLARO,
        x_titulo - fonte_titulo_grande.size(titulo_texto)[0]//2, y_titulo
    )
    
    # === SUBTÍTULO ESTILIZADO ===
    fonte_subtitulo = pygame.font.SysFont("arial", 36, bold=False, italic=True)
    subtitulo_texto = "Desafio de Rivais"
    x_subtitulo = width//2 - fonte_subtitulo.size(subtitulo_texto)[0]//2
    y_subtitulo = 135
    
    # Animação sutil do subtítulo
    offset_animacao = int(math.sin(tempo * 0.003) * 2)
    
    desenhar_texto_simples(
        screen, fonte_subtitulo, subtitulo_texto,
        COR_TEXTO_CLARO_DESTACADO,
        x_subtitulo, y_subtitulo + offset_animacao
    )
    
    # === LINHA DECORATIVA ===
    linha_y = y_subtitulo + 50
    linha_width = 300
    linha_x = width//2 - linha_width//2
    
    # Gradiente para a linha
    for i in range(linha_width):
        ratio = abs(i - linha_width//2) / (linha_width//2)
        alpha = int(150 * (1 - ratio))
        cor_linha = COR_TEXTO_CLARO
        linha_surface = pygame.Surface((2, 3), pygame.SRCALPHA)
        linha_surface.fill((*cor_linha, alpha))
        screen.blit(linha_surface, (linha_x + i, linha_y))
    
    # === MELHORIAS NOS BOTÕES ===
    # Vamos melhorar visualmente cada botão
    mouse_pos = pygame.mouse.get_pos()
    
    for i, botao in enumerate(botoes_menu):
        # Animação de entrada dos botões (delay baseado no índice)
        aparicao = min(1.0, max(0.0, (tempo - 500 - i * 150) / 800))
        if aparicao <= 0:
            continue
            
        # Efeito de hover
        hover = botao.rect.collidepoint(mouse_pos)
        scale = 1.05 if hover else 1.0
        
        # Posição com animação
        original_rect = botao.rect.copy()
        scaled_width = int(original_rect.width * scale)
        scaled_height = int(original_rect.height * scale)
        
        # Centralizar botão escalado
        scaled_rect = pygame.Rect(
            original_rect.centerx - scaled_width//2,
            original_rect.centery - scaled_height//2,
            scaled_width,
            scaled_height
        )
        
        # Aplicar animação de entrada
        entrada_offset = int((1 - aparicao) * 50)
        scaled_rect.x += entrada_offset
        
        # Cores do botão com gradiente (PALETA PADRÃO)
        if hover:
            # Hover - tons mais claros (similar ao botão "Jogar Novamente")
            cor_botao_topo = (140, 180, 70)
            cor_botao_baixo = (120, 160, 50)
            cor_borda = (80, 120, 40)
        else:
            # Estado normal - tons suaves (similar ao padrão da tela final)
            cor_botao_topo = (120, 160, 60)
            cor_botao_baixo = (100, 140, 40)
            cor_borda = (70, 100, 30)
        
        # Aplicar gradiente com bordas arredondadas sem vazamento
        # Usar transparência baseada na animação de entrada
        if aparicao < 1.0:
            # Usar alpha nas cores para animação suave
            alpha_value = int(255 * aparicao)
            cor_topo_alpha = (*cor_botao_topo, alpha_value)
            cor_baixo_alpha = (*cor_botao_baixo, alpha_value)
            aplicar_gradiente_com_bordas(
                screen, scaled_rect, cor_topo_alpha, cor_baixo_alpha, 15
            )
        else:
            # Aplicar gradiente normal quando totalmente aparecido
            aplicar_gradiente_com_bordas(
                screen, scaled_rect, cor_botao_topo, cor_botao_baixo, 15
            )
        
        # Borda do botão
        pygame.draw.rect(screen, cor_borda, scaled_rect, 3, border_radius=15)
        
        # Texto do botão (cor terrosa padrão)
        fonte_botao = pygame.font.SysFont("arial", 28, bold=True)
        texto_botao = fonte_botao.render(botao.texto, True, (255, 255, 255))  # Texto branco para contraste
        
        # Centralizar texto
        texto_x = scaled_rect.centerx - texto_botao.get_width()//2
        texto_y = scaled_rect.centery - texto_botao.get_height()//2
        
        # Sombra do texto
        sombra_texto = fonte_botao.render(botao.texto, True, (200, 200, 200))
        # screen.blit(sombra_texto, (texto_x + 1, texto_y + 1))  # Removido
        
        # Texto principal
        screen.blit(texto_botao, (texto_x, texto_y))
        
        # Efeito de brilho no hover
        if hover:
            brilho_surface = pygame.Surface(scaled_rect.size, pygame.SRCALPHA)
            brilho_alpha = int(20 + 10 * math.sin(tempo * 0.01))
            brilho_surface.fill((255, 255, 255, brilho_alpha))
            screen.blit(brilho_surface, scaled_rect)
    
    # === RODAPÉ ESTILIZADO ===
    fonte_rodape = pygame.font.SysFont("arial", 18, italic=True)
    rodape_texto = "Desenvolvido com carinho em Python + Pygame"
    rodape_surface = fonte_rodape.render(rodape_texto, True, (120, 100, 80))
    rodape_x = width//2 - rodape_surface.get_width()//2
    rodape_y = height - 40
    
    # Animação sutil do rodapé
    alpha_rodape = int(180 + 50 * math.sin(tempo * 0.002))
    rodape_surface.set_alpha(alpha_rodape)
    screen.blit(rodape_surface, (rodape_x, rodape_y))

# Função para desenhar a tela de configurações

def desenhar_config(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, SOM_ATIVO, MUSICA_ATIVA, VOLUME_SOM, VOLUME_MUSICA, RESOLUCAO_ATUAL):
    import pygame
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Título sem sombra
    fonte_titulo = pygame.font.SysFont("arial", 52, bold=True)
    desenhar_texto_simples(
        screen, fonte_titulo, "Configurações",
        COR_TEXTO_CLARO,
        width//2 - fonte_titulo.size("Configurações")[0]//2, 40
    )
    
    y = 120
    mx, my = pygame.mouse.get_pos()
    x_label = 100
    x_btn = 620
    altura_btn = 36
    altura_btn_peq = 32
    
    # === Seção Áudio (cores padrão terrosas) ===
    fonte_secao = pygame.font.SysFont("arial", 28, bold=True)
    desenhar_texto_simples(
        screen, fonte_secao, "AUDIO",
        (120, 100, 80),  # Tom terroso padrão
        x_label-20, y
    )
    y += 48
    
    # Volume dos Efeitos Sonoros
    label_som = FONT_SMALL.render("Volume dos Efeitos Sonoros:", True, COR_TEXTO_CLARO)
    screen.blit(label_som, (x_label, y+2))
    
    # Botões de volume com gradiente
    btn_menos_som = pygame.Rect(370, y, 36, altura_btn_peq)
    btn_mais_som = pygame.Rect(370+36+8, y, 36, altura_btn_peq)
    
    # Efeitos hover
    hover_menos = btn_menos_som.collidepoint(mx, my)
    hover_mais = btn_mais_som.collidepoint(mx, my)
    
    # Desenhar botões com gradiente
    cor_menos_topo = (200, 200, 200) if hover_menos else (160, 160, 160)
    cor_menos_baixo = (160, 160, 160) if hover_menos else (120, 120, 120)
    cor_mais_topo = (200, 200, 200) if hover_mais else (160, 160, 160)
    cor_mais_baixo = (160, 160, 160) if hover_mais else (120, 120, 120)
    botao_menos_grad = criar_gradiente_vertical(36, altura_btn_peq, cor_menos_topo, cor_menos_baixo)
    
    # Aplicar gradientes com bordas sem vazamento
    aplicar_gradiente_com_bordas(screen, btn_menos_som, cor_menos_topo, cor_menos_baixo, 8)
    pygame.draw.rect(screen, (100, 100, 100), btn_menos_som, 2, border_radius=8)
    
    aplicar_gradiente_com_bordas(screen, btn_mais_som, cor_mais_topo, cor_mais_baixo, 8)
    pygame.draw.rect(screen, (100, 100, 100), btn_mais_som, 2, border_radius=8)
    
    # Textos dos botões
    menos_label = FONT_SMALL.render("-", True, (60,60,60))
    mais_label = FONT_SMALL.render("+", True, (60,60,60))
    screen.blit(menos_label, (btn_menos_som.x + (btn_menos_som.w - menos_label.get_width())//2, btn_menos_som.y + 4))
    screen.blit(mais_label, (btn_mais_som.x + (btn_mais_som.w - mais_label.get_width())//2, btn_mais_som.y + 4))
    
    # Valor do volume com destaque
    fonte_volume = pygame.font.SysFont("arial", 20, bold=True)
    vol_som_label = fonte_volume.render(f"{int(VOLUME_SOM*100)}%", True, (196, 102, 31))
    screen.blit(vol_som_label, (btn_mais_som.x + btn_mais_som.w + 12, y+2))
    
    # Botão ativar/desativar som com efeito
    btn_som_w = FONT_SMALL.size("Ativo")[0] + 24 if SOM_ATIVO else FONT_SMALL.size("Inativo")[0] + 24
    btn_som = pygame.Rect(x_btn, y, btn_som_w, altura_btn_peq)
    hover_som = btn_som.collidepoint(mx, my)
    
    if SOM_ATIVO:
        # Verde suave da paleta padrão
        cor_som_topo = (120, 160, 60) if hover_som else (100, 140, 40)
        cor_som_baixo = (100, 140, 40) if hover_som else (80, 120, 20)
        txt_som = FONT_SMALL.render("Ativo", True, (255, 255, 255))
    else:
        # Vermelho suave da paleta padrão
        cor_som_topo = (180, 100, 50) if hover_som else (160, 80, 30)
        cor_som_baixo = (160, 80, 30) if hover_som else (140, 70, 20)
        txt_som = FONT_SMALL.render("Inativo", True, (255, 255, 255))
    
    # Aplicar gradiente com bordas sem vazamento
    aplicar_gradiente_com_bordas(screen, btn_som, cor_som_topo, cor_som_baixo, 8)
    pygame.draw.rect(screen, (100, 100, 100), btn_som, 2, border_radius=8)
    screen.blit(txt_som, (btn_som.x+12, btn_som.y + (btn_som.height - txt_som.get_height()) // 2))
    
    y += 44
    
    # Música (similar ao som)
    label_mus = FONT_SMALL.render("Volume da Música:", True, COR_TEXTO_CLARO)
    screen.blit(label_mus, (x_label, y+2))
    
    btn_menos_mus = pygame.Rect(370, y, 36, altura_btn_peq)
    btn_mais_mus = pygame.Rect(370+36+8, y, 36, altura_btn_peq)
    
    hover_menos_m = btn_menos_mus.collidepoint(mx, my)
    hover_mais_m = btn_mais_mus.collidepoint(mx, my)
    
    # Cores dos botões música
    cor_menos_m_topo = (200, 200, 200) if hover_menos_m else (160, 160, 160)
    cor_menos_m_baixo = (160, 160, 160) if hover_menos_m else (120, 120, 120)
    cor_mais_m_topo = (200, 200, 200) if hover_mais_m else (160, 160, 160)
    cor_mais_m_baixo = (160, 160, 160) if hover_mais_m else (120, 120, 120)
    
    # Botões música com gradiente sem vazamento
    aplicar_gradiente_com_bordas(screen, btn_menos_mus, cor_menos_m_topo, cor_menos_m_baixo, 8)
    pygame.draw.rect(screen, (100, 100, 100), btn_menos_mus, 2, border_radius=8)
    
    aplicar_gradiente_com_bordas(screen, btn_mais_mus, cor_mais_m_topo, cor_mais_m_baixo, 8)
    pygame.draw.rect(screen, (100, 100, 100), btn_mais_mus, 2, border_radius=8)
    
    screen.blit(menos_label, (btn_menos_mus.x + (btn_menos_mus.w - menos_label.get_width())//2, btn_menos_mus.y + 4))
    screen.blit(mais_label, (btn_mais_mus.x + (btn_mais_mus.w - mais_label.get_width())//2, btn_mais_mus.y + 4))
    
    vol_mus_label = fonte_volume.render(f"{int(VOLUME_MUSICA*100)}%", True, (196, 102, 31))
    screen.blit(vol_mus_label, (btn_mais_mus.x + btn_mais_mus.w + 12, y+2))
    
    # Botão música
    btn_mus_w = FONT_SMALL.size("Ativo")[0] + 24 if MUSICA_ATIVA else FONT_SMALL.size("Inativo")[0] + 24
    btn_mus = pygame.Rect(x_btn, y, btn_mus_w, altura_btn_peq)
    hover_mus = btn_mus.collidepoint(mx, my)
    
    if MUSICA_ATIVA:
        # Verde suave da paleta padrão
        cor_mus_topo = (120, 160, 60) if hover_mus else (100, 140, 40)
        cor_mus_baixo = (100, 140, 40) if hover_mus else (80, 120, 20)
        txt_mus = FONT_SMALL.render("Ativo", True, (255, 255, 255))
    else:
        # Vermelho suave da paleta padrão
        cor_mus_topo = (180, 100, 50) if hover_mus else (160, 80, 30)
        cor_mus_baixo = (160, 80, 30) if hover_mus else (140, 70, 20)
        txt_mus = FONT_SMALL.render("Inativo", True, (255, 255, 255))
    
    # Aplicar gradiente com bordas sem vazamento
    aplicar_gradiente_com_bordas(screen, btn_mus, cor_mus_topo, cor_mus_baixo, 8)
    pygame.draw.rect(screen, (100, 100, 100), btn_mus, 2, border_radius=8)
    screen.blit(txt_mus, (btn_mus.x+12, btn_mus.y + (btn_mus.height - txt_mus.get_height()) // 2))
    
    # === Seção Progresso (cores padrão terrosas) ===
    y += 60
    desenhar_texto_simples(
        screen, fonte_secao, "PROGRESSO",
        (120, 100, 80),  # Tom terroso padrão
        x_label-20, y
    )
    y += 48
    
    # Botões de reset com estilo moderno
    txt_reset_palavras = FONT_SMALL.render("Limpar Palavras Usadas", True, (60,60,60))
    btn_reset_palavras_w = txt_reset_palavras.get_width() + 28
    btn_reset_palavras = pygame.Rect(x_label, y, btn_reset_palavras_w, altura_btn)
    hover_reset_p = btn_reset_palavras.collidepoint(mx, my)
    
    cor_reset_p_topo = (180, 120, 60) if hover_reset_p else (160, 100, 40)
    cor_reset_p_baixo = (160, 100, 40) if hover_reset_p else (140, 80, 20)
    # Aplicar gradientes com bordas sem vazamento
    aplicar_gradiente_com_bordas(screen, btn_reset_palavras, cor_reset_p_topo, cor_reset_p_baixo, 8)
    pygame.draw.rect(screen, (120, 70, 30), btn_reset_palavras, 2, border_radius=8)
    screen.blit(txt_reset_palavras, (btn_reset_palavras.x+14, btn_reset_palavras.y + (btn_reset_palavras.height - txt_reset_palavras.get_height()) // 2))
    
    txt_reset_ranking = FONT_SMALL.render("Resetar Ranking", True, (60,60,60))
    btn_reset_ranking_w = txt_reset_ranking.get_width() + 28
    espacamento_progresso = 60
    btn_reset_ranking = pygame.Rect(x_label+btn_reset_palavras_w+espacamento_progresso, y, btn_reset_ranking_w, altura_btn)
    hover_reset_r = btn_reset_ranking.collidepoint(mx, my)
    
    cor_reset_r_topo = (180, 120, 60) if hover_reset_r else (160, 100, 40)
    cor_reset_r_baixo = (160, 100, 40) if hover_reset_r else (140, 80, 20)
    aplicar_gradiente_com_bordas(screen, btn_reset_ranking, cor_reset_r_topo, cor_reset_r_baixo, 8)
    pygame.draw.rect(screen, (120, 70, 30), btn_reset_ranking, 2, border_radius=8)
    screen.blit(txt_reset_ranking, (btn_reset_ranking.x+14, btn_reset_ranking.y + (btn_reset_ranking.height - txt_reset_ranking.get_height()) // 2))
    
    # === Botão Salvar e Sair Elegante ===
    btn_salvar_sair_w = 200
    btn_salvar_sair_h = 50
    btn_salvar_sair_x = width//2 - btn_salvar_sair_w//2
    btn_salvar_sair_y = y + 80
    btn_salvar_sair = pygame.Rect(btn_salvar_sair_x, btn_salvar_sair_y, btn_salvar_sair_w, btn_salvar_sair_h)
    hover_salvar = btn_salvar_sair.collidepoint(mx, my)
    
    cor_salvar_topo = (120, 140, 180) if hover_salvar else (100, 120, 160)
    cor_salvar_baixo = (100, 120, 160) if hover_salvar else (80, 100, 140)
    aplicar_gradiente_com_bordas(screen, btn_salvar_sair, cor_salvar_topo, cor_salvar_baixo, 12)
    pygame.draw.rect(screen, (80, 100, 140), btn_salvar_sair, 3, border_radius=12)
    
    fonte_salvar = pygame.font.SysFont("arial", 28, bold=True)
    txt_salvar_sair = fonte_salvar.render("Salvar e Sair", True, (255,255,255))
    screen.blit(txt_salvar_sair, (btn_salvar_sair.x + (btn_salvar_sair.w - txt_salvar_sair.get_width())//2, btn_salvar_sair.y + (btn_salvar_sair.h - txt_salvar_sair.get_height())//2))
    
    return btn_reset_palavras, btn_reset_ranking, btn_salvar_sair
    # --- Ajuda ---
    y += 64
    sec_ajuda = FONT_SMALL.render("Ajuda", True, COR_TEXTO_CLARO)
    screen.blit(sec_ajuda, (x_label-20, y))
    y += 48
    txt_ajuda = FONT_SMALL.render("Instruções do Jogo", True, (60,60,60))
    btn_ajuda_w = txt_ajuda.get_width() + 24
    btn_ajuda = pygame.Rect(x_label, y, btn_ajuda_w, altura_btn)
    cor_ajuda = (180,240,180) if btn_ajuda.collidepoint(mx, my) else (160,200,160)
    pygame.draw.rect(screen, cor_ajuda, btn_ajuda, border_radius=8)
    screen.blit(txt_ajuda, (btn_ajuda.x+12, btn_ajuda.y + (btn_ajuda.height - txt_ajuda.get_height()) // 2))
    txt_creditos = FONT_SMALL.render("Créditos", True, (60,60,60))
    btn_creditos_w = txt_creditos.get_width() + 24
    btn_creditos = pygame.Rect(x_label+btn_ajuda_w+36, y, btn_creditos_w, altura_btn)
    cor_creditos = (180,240,180) if btn_creditos.collidepoint(mx, my) else (160,200,160)
    pygame.draw.rect(screen, cor_creditos, btn_creditos, border_radius=8)
    screen.blit(txt_creditos, (btn_creditos.x+12, btn_creditos.y + (btn_creditos.height - txt_creditos.get_height()) // 2))
    # Não desenhar botão voltar, tela cheia, janela ou resolução

# Função para desenhar a tela de placar

def desenhar_placar(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo (PALETA PADRÃO)
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Título com efeito especial
    fonte_titulo = pygame.font.SysFont("arial", 56, bold=True)
    desenhar_texto_simples(
        screen, fonte_titulo, "RANKING",
        COR_TEXTO_CLARO,
        width//2 - fonte_titulo.size("RANKING")[0]//2, 50
    )
    
    # Carregar ranking do arquivo
    try:
        with open('ranking_solo.json', 'r', encoding='utf-8') as f:
            ranking = json.load(f)
    except Exception:
        ranking = []
    
    # Separar por dificuldade com cores temáticas (PALETA PADRÃO)
    dificuldades = [
        {'nome': 'Fácil', 'cor_titulo': (120, 160, 60), 'cor_fundo': (245, 250, 240)},     # Verde suave
        {'nome': 'Médio', 'cor_titulo': (196, 102, 31), 'cor_fundo': (250, 245, 235)},    # Laranja terroso
        {'nome': 'Difícil', 'cor_titulo': (180, 60, 60), 'cor_fundo': (250, 240, 240)}   # Vermelho suave
    ]
    
    y_base = 140
    # Ajustar largura das colunas baseado na resolução
    if width >= 1920:
        col_width = 360  # Reduzido para dar mais espaço
        spacing = 40     # Aumentado para evitar que se toquem
    elif width >= 1200:
        col_width = 320  # Reduzido para dar mais espaço
        spacing = 30     # Aumentado para evitar que se toquem
    else:
        col_width = 280  # Reduzido para dar mais espaço
        spacing = 20     # Aumentado para evitar que se toquem
        
    total_width = (col_width * len(dificuldades)) + (spacing * (len(dificuldades) - 1))
    x_start = width//2 - total_width//2
    
    for idx, dif_info in enumerate(dificuldades):
        dif = dif_info['nome']
        cor_titulo = dif_info['cor_titulo']
        cor_fundo = dif_info['cor_fundo']
        
        top10 = [r for r in ranking if r.get('dificuldade') == dif]
        top10 = sorted(top10, key=lambda x: x.get('tempo', 9999))[:10]
        
        # Calcular posição da coluna com espaçamento correto
        x_dif = x_start + idx * (col_width + spacing)
        
        # Container da coluna com fundo sutil - aumentado para 10 jogadores
        container_padding = 10  # Reduzido para evitar vazamento
        coluna_rect = pygame.Rect(
            x_dif - container_padding, 
            y_base - 20, 
            col_width + (container_padding * 2), 
            520  # Aumentado para comportar 10 jogadores (10 * 42 + margem)
        )
        
        # Fundo da coluna com bordas arredondadas usando função auxiliar
        cor_fundo_topo = cor_fundo
        cor_fundo_baixo = (cor_fundo[0]-15, cor_fundo[1]-15, cor_fundo[2]-15)
        
        # Aplicar gradiente com bordas arredondadas para evitar cantos brancos
        aplicar_gradiente_com_bordas(screen, coluna_rect, cor_fundo_topo, cor_fundo_baixo, 12)
        
        # Borda mais sutil para evitar vazamento
        pygame.draw.rect(screen, cor_titulo, coluna_rect, 2, border_radius=12)  # Borda mais fina e raio menor
        
        # Título da dificuldade sem efeito glow
        fonte_dificuldade = pygame.font.SysFont("arial", 32, bold=True)
        
        # Título principal sem sombra - centralizado no container
        titulo_dif = fonte_dificuldade.render(dif, True, cor_titulo)
        titulo_x = coluna_rect.x + (coluna_rect.width - titulo_dif.get_width()) // 2
        screen.blit(titulo_dif, (titulo_x, y_base))
        
        # Linha decorativa sob o título
        linha_y = y_base + 45
        linha_x = titulo_x + 20
        linha_w = titulo_dif.get_width() - 40
        for i in range(linha_w):
            alpha = int(150 * (1 - abs(i - linha_w//2) / (linha_w//2)))
            pixel_color = (*cor_titulo, alpha)
            linha_surface = pygame.Surface((1, 2), pygame.SRCALPHA)
            linha_surface.fill(pixel_color)
            screen.blit(linha_surface, (linha_x + i, linha_y))
        
        # Entradas do ranking
        for i, r in enumerate(top10):
            nome = r.get('nome', '-')
            tempo_val = r.get('tempo', 0)
            palavra = r.get('palavra', '-')
            tempo_str = f"{tempo_val:.2f}s"
            
            # Posição da linha com espaçamento adequado para 10 jogadores
            y_linha = y_base + 75 + i*40  # Espaçamento ajustado para 10 jogadores
            
            # Fundo da linha (alternado) - removido o branco para evitar vazamento
            if i % 2 == 0:
                linha_bg = pygame.Rect(
                    coluna_rect.x + 8,   # Mais margem interna
                    y_linha - 6, 
                    coluna_rect.width - 16,  # Margem em ambos os lados
                    32
                )
                # Usar uma cor sutil da paleta em vez de branco
                linha_bg_color = (cor_fundo[0]-10, cor_fundo[1]-10, cor_fundo[2]-10, 15)  # Cor da dificuldade mais escura
                linha_surface = pygame.Surface((linha_bg.width, linha_bg.height), pygame.SRCALPHA)
                linha_surface.fill(linha_bg_color)
                screen.blit(linha_surface, linha_bg)
                # Sem borda para evitar vazamento completamente
            
            # === FONTE ÚNICA PERSONALIZADA PARA COLOCAÇÃO ===
            fonte_colocacao = pygame.font.SysFont("arial", 22, bold=True)
            fonte_nome = pygame.font.SysFont("arial", 18, bold=True)  # Mesma fonte para nome e palavra
            fonte_tempo = pygame.font.SysFont("arial", 16, bold=False)
            
            # Cores especiais para os 3 primeiros, normal para os demais
            if i < 3:
                cores_colocacao = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]  # Ouro, Prata, Bronze
                cor_colocacao = cores_colocacao[i]
                simbolos_colocacao = ['1º', '2º', '3º']
                colocacao_text = simbolos_colocacao[i]
            else:
                cor_colocacao = (80, 80, 80)
                colocacao_text = f"{i+1}º"
            
            # === LAYOUT ALINHADO EM UMA LINHA ===
            x_base = coluna_rect.x + 12  # Mais espaço da borda
            
            # 1. COLOCAÇÃO (posição fixa)
            colocacao_label = fonte_colocacao.render(colocacao_text, True, cor_colocacao)
            screen.blit(colocacao_label, (x_base, y_linha + 2))
            
            # 2. NOME - PALAVRA (ajuste inteligente de tamanho baseado no espaço disponível)
            nome_x = x_base + 50
            
            # Calcular espaço disponível para nome + palavra
            tempo_label_temp = fonte_tempo.render(tempo_str, True, (196, 102, 31))
            espaco_tempo = tempo_label_temp.get_width() + 20  # Largura do tempo + margem
            espaco_disponivel = coluna_rect.width - (nome_x - coluna_rect.x) - espaco_tempo
            
            # Truncamento inteligente para o nome
            nome_truncado = nome
            for i in range(len(nome), 0, -1):
                nome_test = nome[:i] + ('...' if i < len(nome) else '')
                nome_width = fonte_nome.size(nome_test)[0]
                if nome_width <= espaco_disponivel * 0.6:  # 60% do espaço para o nome
                    nome_truncado = nome_test
                    break
            
            # Truncamento inteligente para a palavra
            palavra_truncada = palavra
            separador_width = fonte_nome.size(" - ")[0]
            nome_final_width = fonte_nome.size(nome_truncado)[0]
            espaco_palavra = espaco_disponivel - nome_final_width - separador_width
            
            for i in range(len(palavra), 0, -1):
                palavra_test = palavra[:i] + ('...' if i < len(palavra) else '')
                palavra_width = fonte_nome.size(palavra_test)[0]
                if palavra_width <= espaco_palavra:
                    palavra_truncada = palavra_test
                    break
            
            # Texto combinado: Nome - Palavra
            texto_combinado = f"{nome_truncado} - {palavra_truncada}"
            
            # Renderizar nome
            nome_label = fonte_nome.render(nome_truncado, True, cor_titulo)
            screen.blit(nome_label, (nome_x, y_linha + 2))
            
            # Renderizar separador
            separador_x = nome_x + nome_label.get_width() + 6
            separador_label = fonte_nome.render(" - ", True, (120, 100, 80))  # Cor neutra
            screen.blit(separador_label, (separador_x, y_linha + 2))
            
            # Renderizar palavra com cor diferente
            palavra_x = separador_x + separador_label.get_width()
            palavra_label = fonte_nome.render(palavra_truncada, True, (150, 80, 40))  # Cor laranja terrosa
            screen.blit(palavra_label, (palavra_x, y_linha + 2))
            
            # 3. TEMPO (alinhado à direita do container, com mais margem)
            tempo_label = fonte_tempo.render(tempo_str, True, (196, 102, 31))
            tempo_x = coluna_rect.x + coluna_rect.width - tempo_label.get_width() - 15  # Mais margem
            screen.blit(tempo_label, (tempo_x, y_linha + 6))  # Centralizado verticalmente
    
    # Instrução elegante - ranking
    fonte_instrucao = pygame.font.SysFont("arial", 20, italic=True)
    instrucao_text = "← Pressione ESC para voltar"
    desenhar_texto_simples(
        screen, fonte_instrucao, instrucao_text,
        (100, 90, 70),
        40, height-60
    )

def desenhar_dificuldade(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, btns_dificuldade, btn_dificuldade_hover):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo (PALETA PADRÃO)
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Título com efeito especial
    fonte_titulo = pygame.font.SysFont("arial", 52, bold=True)
    titulo_text = "Escolha a Dificuldade"
    
    # Animação do título
    offset_titulo = int(math.sin(tempo * 0.003) * 3)
    
    desenhar_texto_simples(
        screen, fonte_titulo, titulo_text,
        COR_TEXTO_CLARO,
        width//2 - fonte_titulo.size(titulo_text)[0]//2, 80 + offset_titulo
    )
    
    mx, my = pygame.mouse.get_pos()
    
    # Melhorar os botões de dificuldade
    for i, btn in enumerate(btns_dificuldade):
        # Posição com animação de entrada
        aparicao = min(1.0, max(0.0, (tempo - 300 - i * 200) / 600))
        if aparicao <= 0:
            continue
            
        rect = pygame.Rect(width//2 - 200, 200 + i*120, 400, 90)
        
        # Animação de entrada
        entrada_offset = int((1 - aparicao) * 80)
        rect.x += entrada_offset
        
        # Efeito hover
        hover = rect.collidepoint(mx, my)
        scale = 1.03 if hover else 1.0
        
        # Aplicar escala
        if hover:
            scaled_width = int(rect.width * scale)
            scaled_height = int(rect.height * scale)
            rect = pygame.Rect(
                rect.centerx - scaled_width//2,
                rect.centery - scaled_height//2,
                scaled_width,
                scaled_height
            )
        
        # Cores com gradiente
        cor_base = btn["cor"]
        cor_hover = btn["hover"]
        
        if hover:
            cor_topo = cor_hover
            cor_baixo = (max(0, cor_hover[0]-30), max(0, cor_hover[1]-30), max(0, cor_hover[2]-30))
        else:
            cor_topo = cor_base
            cor_baixo = (max(0, cor_base[0]-25), max(0, cor_base[1]-25), max(0, cor_base[2]-25))
        
        # Aplicar gradiente com bordas arredondadas sem vazamento
        aplicar_gradiente_com_bordas(
            screen, rect, cor_topo, cor_baixo, 18
        )
        
        # Aplicar transparência na entrada
        if aparicao < 1.0:
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, int(255 * (1 - aparicao))))
            screen.blit(overlay, rect)
        
        # Borda elegante
        borda_cor = (max(0, cor_topo[0]-40), max(0, cor_topo[1]-40), max(0, cor_topo[2]-40))
        pygame.draw.rect(screen, borda_cor, rect, 4, border_radius=18)
        
        # Ícone da dificuldade
        icones = ['[F]', '[M]', '[D]']  # Fácil, Médio, Difícil
        fonte_icone = pygame.font.SysFont("arial", 32)
        icone_surface = fonte_icone.render(icones[i], True, (255, 255, 255))
        screen.blit(icone_surface, (rect.x + 20, rect.y + 15))
        
        # Título da dificuldade
        fonte_label = pygame.font.SysFont("arial", 32, bold=True)
        label_surface = fonte_label.render(btn["label"], True, (255, 255, 255))
        
        # Texto principal sem sombra
        screen.blit(label_surface, (rect.x + 70, rect.y + 15))
        
        # Descrição
        fonte_desc = pygame.font.SysFont("arial", 22, italic=True)
        desc_surface = fonte_desc.render(btn["desc"], True, (240, 240, 240))
        screen.blit(desc_surface, (rect.x + 70, rect.y + 50))
        
        # Efeito de brilho no hover
        if hover:
            brilho_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            brilho_alpha = int(15 + 10 * math.sin(tempo * 0.008))
            brilho_surface.fill((255, 255, 255, brilho_alpha))
            screen.blit(brilho_surface, rect)
        
        # Salvar rect para detecção de clique
        btn["rect"] = rect
    
    # Instrução elegante - dificuldade
    fonte_instrucao = pygame.font.SysFont("arial", 20, italic=True)
    instrucao_text = "← Pressione ESC para voltar"
    desenhar_texto_simples(
        screen, fonte_instrucao, instrucao_text,
        (100, 90, 70),
        40, height-60
    )

def desenhar_carregando_palavra(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Texto com animação de pulsação
    fonte_carregando = pygame.font.SysFont("arial", 48, bold=True)
    alpha = int(180 + 75 * math.sin(tempo * 0.005))
    
    # Criar surface com alpha
    texto_surface = pygame.Surface(fonte_carregando.size("Carregando palavra..."), pygame.SRCALPHA)
    msg = fonte_carregando.render("Carregando palavra...", True, (*COR_TEXTO_CLARO, alpha))
    texto_surface.blit(msg, (0, 0))
    
    # Centralizar
    x = width//2 - texto_surface.get_width()//2
    y = height//2 - texto_surface.get_height()//2
    
    # Remover sombra do texto carregando
    # Texto principal
    screen.blit(texto_surface, (x, y))
    
    # Barra de carregamento animada
    barra_width = 300
    barra_height = 8
    barra_x = width//2 - barra_width//2
    barra_y = y + 80
    
    # Fundo da barra
    pygame.draw.rect(screen, (200, 200, 200), (barra_x, barra_y, barra_width, barra_height), border_radius=4)
    
    # Progresso animado
    progresso = (tempo * 0.003) % 1.0
    progresso_width = int(barra_width * progresso)
    
    # Gradiente da barra de progresso
    if progresso_width > 0:
        barra_grad = criar_gradiente_vertical(progresso_width, barra_height, (100, 200, 100), (70, 170, 70))
        screen.blit(barra_grad, (barra_x, barra_y))

# Função para desenhar tela de carregando palavra animado

def desenhar_carregando_palavra_animado(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Animação de reticências
    t = tempo // 400 % 4
    pontos = '.' * t
    
    # Texto base
    texto_base = "Carregando palavra"
    fonte_carregando = pygame.font.SysFont("arial", 48, bold=True)
    
    # Animação de cores
    r = int(COR_TEXTO_CLARO[0] + 30 * math.sin(tempo * 0.005))
    g = int(COR_TEXTO_CLARO[1] + 20 * math.sin(tempo * 0.007))
    b = int(COR_TEXTO_CLARO[2] + 10 * math.sin(tempo * 0.003))
    cor_animada = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    # Texto completo
    texto_completo = f"{texto_base}{pontos}"
    
    # Texto sem sombra
    
    # Texto principal
    msg = fonte_carregando.render(texto_completo, True, cor_animada)
    x = width//2 - msg.get_width()//2
    y = height//2 - msg.get_height()//2
    screen.blit(msg, (x, y))
    
    # Spinner animado
    centro_spinner = (width//2, y + 100)
    raio_spinner = 20
    
    for i in range(8):
        angulo = (tempo * 0.01 + i * math.pi / 4) % (2 * math.pi)
        x_ponto = centro_spinner[0] + raio_spinner * math.cos(angulo)
        y_ponto = centro_spinner[1] + raio_spinner * math.sin(angulo)
        
        # Fade baseado na posição
        alpha = int(255 * (i + 1) / 8)
        ponto_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
        ponto_surface.fill((*COR_TEXTO_CLARO, alpha))
        screen.blit(ponto_surface, (x_ponto - 3, y_ponto - 3))

# Função para desenhar tela final

def desenhar_tela_final(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, mensagem_final, tempo_exemplo, erros_exemplo, dificuldade=None):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    mx, my = pygame.mouse.get_pos()
    
    # Gradiente de fundo especial
    if "Parabéns" in mensagem_final or "acertou" in mensagem_final:
        # Fundo de vitória - verde suave
        gradiente = criar_gradiente_vertical(width, height, (240, 255, 240), (220, 240, 220))
    else:
        # Fundo normal/derrota
        gradiente = criar_gradiente_vertical(width, height, (255, 240, 240), (240, 220, 220))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Título com efeito especial
    fonte_titulo = pygame.font.SysFont("arial", 58, bold=True)
    
    if "Parabéns" in mensagem_final or "acertou" in mensagem_final:
        titulo_text = "VITORIA!"
        cor_titulo = (100, 180, 100)
    else:
        titulo_text = "FIM DE JOGO"
        cor_titulo = COR_TEXTO_CLARO
    
    # Animação do título
    offset_titulo = int(math.sin(tempo * 0.005) * 4)
    
    # Título sem efeito glow
    desenhar_texto_simples(
        screen, fonte_titulo, titulo_text,
        cor_titulo,
        width//2 - fonte_titulo.size(titulo_text)[0]//2, 60 + offset_titulo
    )
    
    # Container da mensagem principal
    container_y = 160
    container_height = 120
    container_rect = pygame.Rect(60, container_y, width - 120, container_height)
    
    # Fundo do container
    container_surface = pygame.Surface((container_rect.width, container_rect.height), pygame.SRCALPHA)
    container_surface.fill((255, 255, 255, 80))
    screen.blit(container_surface, container_rect)
    pygame.draw.rect(screen, (200, 200, 200, 150), container_rect, 3, border_radius=20)
    
    # Mensagem principal
    fonte_mensagem = pygame.font.SysFont("arial", 32, bold=True)
    
    # Quebrar mensagem em linhas se necessário
    palavras = mensagem_final.split()
    linhas = []
    linha_atual = ""
    
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        if fonte_mensagem.size(teste_linha)[0] < container_rect.width - 40:
            linha_atual = teste_linha
        else:
            if linha_atual:
                linhas.append(linha_atual.strip())
            linha_atual = palavra + " "
    if linha_atual:
        linhas.append(linha_atual.strip())
    
    # Desenhar linhas centralizadas
    total_height = len(linhas) * 40
    start_y = container_rect.y + (container_rect.height - total_height) // 2
    
    for i, linha in enumerate(linhas):
        y_linha = start_y + i * 40
        desenhar_texto_simples(
            screen, fonte_mensagem, linha,
            COR_TEXTO_CLARO_DESTACADO,
            width//2 - fonte_mensagem.size(linha)[0]//2, y_linha
        )
    
    # Estatísticas elegantes
    stats_y = container_y + container_height + 40
    
    # Container das estatísticas
    stats_rect = pygame.Rect(width//2 - 200, stats_y, 400, 80)
    stats_surface = pygame.Surface((stats_rect.width, stats_rect.height), pygame.SRCALPHA)
    stats_surface.fill((255, 255, 255, 60))
    screen.blit(stats_surface, stats_rect)
    pygame.draw.rect(screen, (180, 180, 180), stats_rect, 2, border_radius=15)
    
    # Tempo com ícone
    fonte_stats = pygame.font.SysFont("arial", 28, bold=True)
    tempo_text = f"Tempo: {tempo_exemplo:.2f}s"
    tempo_surface = fonte_stats.render(tempo_text, True, (196, 102, 31))
    tempo_x = stats_rect.x + (stats_rect.width - tempo_surface.get_width()) // 2
    screen.blit(tempo_surface, (tempo_x, stats_rect.y + 15))
    
    # Erros com ícone
    erros_text = f"Erros: {erros_exemplo}"
    erros_surface = fonte_stats.render(erros_text, True, (180, 60, 60))
    erros_x = stats_rect.x + (stats_rect.width - erros_surface.get_width()) // 2
    screen.blit(erros_surface, (erros_x, stats_rect.y + 50))
    
    # Botões modernos
    botoes_y = stats_y + 120
    btn_w, btn_h = 240, 70
    espacamento = 50
    total_w = btn_w * 2 + espacamento
    x0 = width//2 - total_w//2
    
    # Botão Jogar Novamente
    btn_jogar_rect = pygame.Rect(x0, botoes_y, btn_w, btn_h)
    hover_jogar = btn_jogar_rect.collidepoint(mx, my)
    
    if hover_jogar:
        cor_jogar_topo = (140, 180, 70)
        cor_jogar_baixo = (120, 160, 50)
    else:
        cor_jogar_topo = (120, 160, 60)
        cor_jogar_baixo = (100, 140, 40)
    
    # Botão Jogar Novamente - usar função correta
    aplicar_gradiente_com_bordas(
        screen, btn_jogar_rect, cor_jogar_topo, cor_jogar_baixo, 18
    )
    pygame.draw.rect(screen, (80, 120, 40), btn_jogar_rect, 3, border_radius=18)
    
    fonte_botao = pygame.font.SysFont("arial", 26, bold=True)
    jogar_text = "Jogar Novamente"
    jogar_surface = fonte_botao.render(jogar_text, True, (255, 255, 255))
    
    screen.blit(jogar_surface, (btn_jogar_rect.x + (btn_jogar_rect.w - jogar_surface.get_width())//2, 
                               btn_jogar_rect.y + (btn_jogar_rect.h - jogar_surface.get_height())//2))
    
    # Botão Menu
    btn_menu_rect = pygame.Rect(x0 + btn_w + espacamento, botoes_y, btn_w, btn_h)
    hover_menu = btn_menu_rect.collidepoint(mx, my)
    
    if hover_menu:
        cor_menu_topo = (180, 120, 60)
        cor_menu_baixo = (160, 100, 40)
    else:
        cor_menu_topo = (160, 100, 50)
        cor_menu_baixo = (140, 80, 30)
    
    # Botão Menu - usar função correta
    aplicar_gradiente_com_bordas(
        screen, btn_menu_rect, cor_menu_topo, cor_menu_baixo, 18
    )
    pygame.draw.rect(screen, (120, 70, 30), btn_menu_rect, 3, border_radius=18)
    
    menu_text = "Menu Principal"
    menu_surface = fonte_botao.render(menu_text, True, (255, 255, 255))
    
    screen.blit(menu_surface, (btn_menu_rect.x + (btn_menu_rect.w - menu_surface.get_width())//2, 
                              btn_menu_rect.y + (btn_menu_rect.h - menu_surface.get_height())//2))
    
    # Botão Ver Definição
    btn_def_rect = pygame.Rect(width//2 - 140, botoes_y + 90, 280, 50)
    hover_def = btn_def_rect.collidepoint(mx, my)
    
    if hover_def:
        cor_def_topo = (140, 160, 200)
        cor_def_baixo = (120, 140, 180)
    else:
        cor_def_topo = (120, 140, 180)
        cor_def_baixo = (100, 120, 160)
    
    # Botão Ver Definição - usar função correta
    aplicar_gradiente_com_bordas(
        screen, btn_def_rect, cor_def_topo, cor_def_baixo, 12
    )
    pygame.draw.rect(screen, (80, 100, 140), btn_def_rect, 2, border_radius=12)
    
    fonte_def = pygame.font.SysFont("arial", 22, bold=True)
    def_text = "Ver definição da palavra"
    def_surface = fonte_def.render(def_text, True, (255, 255, 255))
    
    # Texto sem sombra
    
    screen.blit(def_surface, (btn_def_rect.x + (btn_def_rect.w - def_surface.get_width())//2, 
                             btn_def_rect.y + (btn_def_rect.h - def_surface.get_height())//2))
    
    # Ranking do nível jogado (se disponível)
    if dificuldade:
        import json
        try:
            with open('ranking_solo.json', 'r', encoding='utf-8') as f:
                ranking = json.load(f)
        except Exception:
            ranking = []
        
        top5 = [r for r in ranking if r.get('dificuldade') == dificuldade]
        top5 = sorted(top5, key=lambda x: x.get('tempo', 9999))[:5]  # Top 5 apenas
        
        if top5:
            ranking_y = btn_def_rect.y + btn_def_rect.height + 40
            
            # Título do ranking
            fonte_ranking_titulo = pygame.font.SysFont("arial", 36, bold=True)
            ranking_titulo_text = f"TOP 5 - {dificuldade}"
            desenhar_texto_simples(
                screen, fonte_ranking_titulo, ranking_titulo_text,
                COR_TEXTO_CLARO_DESTACADO,
                width//2 - fonte_ranking_titulo.size(ranking_titulo_text)[0]//2, ranking_y
            )
            
            # Container do ranking
            ranking_container_y = ranking_y + 50
            ranking_container = pygame.Rect(width//2 - 300, ranking_container_y, 600, 200)
            
            container_ranking_surface = pygame.Surface((ranking_container.width, ranking_container.height), pygame.SRCALPHA)
            container_ranking_surface.fill((255, 255, 255, 50))
            screen.blit(container_ranking_surface, ranking_container)
            pygame.draw.rect(screen, (180, 180, 180, 120), ranking_container, 2, border_radius=15)
            
            # Entradas do ranking
            for i, r in enumerate(top5):
                nome = r.get('nome', '-')
                tempo_val = r.get('tempo', 0)
                palavra = r.get('palavra', '-')
                tempo_str = f"{tempo_val:.2f}s"
                
                y_entrada = ranking_container.y + 20 + i * 35
                
                # Medalhas para os 3 primeiros - usando texto
                medalhas_texto = ['1°', '2°', '3°', '4°', '5°']
                fonte_medalha = pygame.font.SysFont("arial", 20, bold=True)
                cores_medalha = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (160, 160, 160), (120, 120, 120)]
                medalha_surface = fonte_medalha.render(medalhas_texto[i], True, cores_medalha[i])
                screen.blit(medalha_surface, (ranking_container.x + 20, y_entrada))
                
                # Dados do jogador
                fonte_ranking = pygame.font.SysFont("arial", 20, bold=True)
                
                # Nome
                nome_truncado = nome[:15] + '...' if len(nome) > 15 else nome
                nome_surface = fonte_ranking.render(f"{i+1}. {nome_truncado}", True, (80, 100, 60))
                screen.blit(nome_surface, (ranking_container.x + 60, y_entrada))
                
                # Tempo
                tempo_surface = fonte_ranking.render(tempo_str, True, (196, 102, 31))
                screen.blit(tempo_surface, (ranking_container.x + 300, y_entrada))
                
                # Palavra
                palavra_truncada = palavra[:10] + '...' if len(palavra) > 10 else palavra
                fonte_palavra = pygame.font.SysFont("arial", 18, italic=True)
                palavra_surface = fonte_palavra.render(f"({palavra_truncada})", True, (120, 100, 80))
                screen.blit(palavra_surface, (ranking_container.x + 420, y_entrada + 2))
    
    return btn_jogar_rect, btn_menu_rect, btn_def_rect

# Função para desenhar o jogo (modo solo)

def desenhar_jogo(screen, FONT_SMALL, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, cor_input_inativo, cor_input_borda, rodada_ativa, nome_jogador_exemplo, tempo_exemplo, erros_exemplo, palavra_embaralhada, letras_embaralhadas_usadas, letras_embaralhadas_pos, palavra_original, letras_adivinhadas, indice_atual, feedback_erro_idx, feedback_erro_timer, FEEDBACK_ERRO_DURATION, feedback_erro_circulo_idx, feedback_erro_circulo_timer, botao_desistir_rect, fim_rodada, shake_timer=0):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo dinâmico (PALETA PADRÃO)
    if rodada_ativa:
        gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    else:
        gradiente = criar_gradiente_vertical(width, height, (235, 220, 190), (205, 190, 160))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Topo: informações do jogador com estilo
    if rodada_ativa:
        # Container das informações
        info_rect = pygame.Rect(20, 15, width - 40, 50)
        
        # Fundo semi-transparente
        info_surface = pygame.Surface((info_rect.width, info_rect.height), pygame.SRCALPHA)
        info_surface.fill((255, 255, 255, 60))
        screen.blit(info_surface, info_rect)
        pygame.draw.rect(screen, (200, 200, 200, 100), info_rect, 2, border_radius=10)
        
        # Textos das informações
        fonte_info = pygame.font.SysFont("arial", 22, bold=True)
        
        # Nome do jogador
        nome_text = f"Jogador: {nome_jogador_exemplo}"
        nome_surface = fonte_info.render(nome_text, True, (80, 100, 60))
        screen.blit(nome_surface, (info_rect.x + 20, info_rect.y + 15))
        
        # Tempo
        tempo_text = f"{tempo_exemplo:.2f}s"
        tempo_surface = fonte_info.render(tempo_text, True, (196, 102, 31))
        tempo_x = info_rect.centerx - tempo_surface.get_width()//2
        screen.blit(tempo_surface, (tempo_x, info_rect.y + 15))
        
        # Erros
        erros_text = f"❌ {erros_exemplo}"
        erros_surface = fonte_info.render(erros_text, True, (180, 60, 60))
        erros_x = info_rect.right - erros_surface.get_width() - 20
        screen.blit(erros_surface, (erros_x, info_rect.y + 15))
    
    # Palavra embaralhada (letras em círculos modernos)
    letras_embaralhadas_pos.clear()
    shake_x, shake_y = 0, 0
    if shake_timer > 0:
        import random
        shake_x = random.randint(-8, 8)
        shake_y = random.randint(-8, 8)
    
    # Posição das letras embaralhadas
    cx = width//2 - (len(palavra_embaralhada)*70)//2 + shake_x
    cy = 120 + shake_y
    
    # Título das letras embaralhadas
    fonte_secao = pygame.font.SysFont("arial", 20, bold=True)
    titulo_embaralhadas = fonte_secao.render("Letras Disponíveis:", True, COR_TEXTO_CLARO)
    screen.blit(titulo_embaralhadas, (width//2 - titulo_embaralhadas.get_width()//2, cy - 30))
    
    for i, letra in enumerate(palavra_embaralhada):
        center = (cx + i*70 + 35, cy + 35)
        
        # Efeito hover (simular para demonstração)
        mouse_pos = pygame.mouse.get_pos()
        distancia = math.sqrt((center[0] - mouse_pos[0])**2 + (center[1] - mouse_pos[1])**2)
        hover = distancia < 35
        
        # Raio baseado no estado
        raio_base = 32
        if hover and not letras_embaralhadas_usadas[i]:
            raio = raio_base + 3
        else:
            raio = raio_base
        
        # Cores baseadas no estado (PALETA PADRÃO)
        if i == feedback_erro_circulo_idx and feedback_erro_circulo_timer > 0:
            # Erro - vermelho pulsante
            pulse = math.sin(tempo * 0.02) * 0.3 + 0.7
            cor_topo = (int(180 * pulse), int(60 * pulse), int(60 * pulse))
            cor_baixo = (int(160 * pulse), int(50 * pulse), int(50 * pulse))
        elif letras_embaralhadas_usadas[i]:
            # Usado - verde suave da paleta
            cor_topo = (120, 160, 60)
            cor_baixo = (100, 140, 40)
        elif hover:
            # Hover - azul suave da paleta
            cor_topo = (140, 160, 200)
            cor_baixo = (120, 140, 180)
        else:
            # Padrão - bege terroso da paleta
            cor_topo = (210, 195, 165)
            cor_baixo = (190, 175, 145)
        
        # Sombra removida do círculo
        # Círculo com gradiente (simular com múltiplos círculos)
        for r in range(raio, 0, -1):
            ratio = r / raio
            cor_atual = (
                int(cor_topo[0] * ratio + cor_baixo[0] * (1 - ratio)),
                int(cor_topo[1] * ratio + cor_baixo[1] * (1 - ratio)),
                int(cor_topo[2] * ratio + cor_baixo[2] * (1 - ratio))
            )
            pygame.draw.circle(screen, cor_atual, center, r)
        
        # Borda do círculo
        pygame.draw.circle(screen, (100, 100, 100), center, raio, 3)
        
        # Letra com sombra
        fonte_letra = pygame.font.SysFont("arial", 36, bold=True)
        
        # Letra principal
        letra_surface = fonte_letra.render(letra, True, (255, 255, 255))
        letra_pos = (center[0] - letra_surface.get_width()//2, center[1] - letra_surface.get_height()//2)
        screen.blit(letra_surface, letra_pos)
        
        # Adicionar à lista para detecção de clique
        rect = pygame.Rect(center[0]-raio, center[1]-raio, raio*2, raio*2)
        letras_embaralhadas_pos.append((rect, letra, i))
    
    # Espaços para adivinhar (caixas modernas)
    cy2 = 280 + shake_y
    cx2 = width//2 - (len(palavra_original)*65)//2 + shake_x
    
    # Título da palavra
    titulo_palavra = fonte_secao.render(f"Palavra ({len(palavra_original)} letras):", True, COR_TEXTO_CLARO)
    screen.blit(titulo_palavra, (width//2 - titulo_palavra.get_width()//2, cy2 - 30))
    
    for i in range(len(palavra_original)):
        rect = pygame.Rect(cx2 + i*65, cy2, 55, 70)
        
        # Estado da caixa (PALETA PADRÃO)
        if i == feedback_erro_idx and feedback_erro_timer > 0:
            # Erro - vermelho suave
            cor_topo = (180, 60, 60)
            cor_baixo = (160, 50, 50)
        elif letras_adivinhadas[i]:
            # Preenchido - verde suave da paleta
            cor_topo = (120, 160, 60)
            cor_baixo = (100, 140, 40)
        elif i == indice_atual:
            # Atual - azul suave da paleta
            cor_topo = (120, 140, 180)
            cor_baixo = (100, 120, 160)
        else:
            # Vazio - bege da paleta
            cor_topo = (210, 195, 165)
            cor_baixo = (190, 175, 145)
        
        # Caixa sem sombra
        # Gradiente da caixa
        caixa_gradiente = criar_gradiente_vertical(rect.width, rect.height, cor_topo, cor_baixo)
        screen.blit(caixa_gradiente, rect)
        
        # Borda da caixa
        pygame.draw.rect(screen, (120, 100, 80), rect, 3, border_radius=12)
        
        # Letra se houver
        letra = letras_adivinhadas[i]
        if letra:
            fonte_caixa = pygame.font.SysFont("arial", 36, bold=True)
            
            # Letra principal
            letra_render = fonte_caixa.render(letra, True, (255, 255, 255))
            letra_x = rect.x + (rect.w - letra_render.get_width())//2
            letra_y = rect.y + (rect.h - letra_render.get_height())//2
            screen.blit(letra_render, (letra_x, letra_y))
    
    # Botão desistir moderno
    if rodada_ativa:
        hover_desistir = botao_desistir_rect.collidepoint(pygame.mouse.get_pos())
        
        if hover_desistir:
            # Hover - vermelho da paleta
            cor_desistir_topo = (180, 100, 50)
            cor_desistir_baixo = (160, 80, 30)
        else:
            # Normal - laranja suave da paleta
            cor_desistir_topo = (160, 100, 40)
            cor_desistir_baixo = (140, 80, 20)
        
        # Sombra removida - botão sem sombra
        
        # Gradiente do botão
        desistir_grad = criar_gradiente_vertical(
            botao_desistir_rect.width, botao_desistir_rect.height,
            cor_desistir_topo, cor_desistir_baixo
        )
        screen.blit(desistir_grad, botao_desistir_rect)
        
        # Borda
        pygame.draw.rect(screen, (150, 80, 80), botao_desistir_rect, 3, border_radius=12)
        
        # Texto do botão
        fonte_desistir = pygame.font.SysFont("arial", 26, bold=True)
        desistir_text = "Desistir"
        desistir_label = fonte_desistir.render(desistir_text, True, (255, 255, 255))
        
        # Texto principal
        texto_x = botao_desistir_rect.x + (botao_desistir_rect.w - desistir_label.get_width())//2
        texto_y = botao_desistir_rect.y + (botao_desistir_rect.h - desistir_label.get_height())//2
        screen.blit(desistir_label, (texto_x, texto_y))
    
    # Instrução elegante
    if rodada_ativa:
        fonte_instrucao = pygame.font.SysFont("arial", 20, italic=True)
        instr_text = "Clique nas letras ou digite • ESC para menu"
        desenhar_texto_simples(
            screen, fonte_instrucao, instr_text,
            (100, 90, 70),
            width//2 - fonte_instrucao.size(instr_text)[0]//2, height - 50
        )
    else:
        fonte_instrucao = pygame.font.SysFont("arial", 24, bold=True)
        instr_text = "Rodada Finalizada"
        desenhar_texto_simples(
            screen, fonte_instrucao, instr_text,
            (150, 100, 50),
            width//2 - fonte_instrucao.size(instr_text)[0]//2, height - 50
        )

# Função para desenhar tela de nome solo

def desenhar_nome_solo(screen, FONT_BIG, FONT_SMALL, cor_input_ativo, cor_input_inativo, cor_input_borda, input_rect, input_ativo, nome_jogador, cursor_visible, botao_iniciar_nome):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    
    # Gradiente de fundo (PALETA PADRÃO)
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    # Título com efeito especial
    fonte_titulo = pygame.font.SysFont("arial", 52, bold=True)
    titulo_text = "Digite seu Nome"
    
    # Animação sutil do título
    offset_titulo = int(math.sin(tempo * 0.003) * 2)
    
    desenhar_texto_simples(
        screen, fonte_titulo, titulo_text,
        (120, 100, 80),  # Tom terroso da paleta padrão
        width//2 - fonte_titulo.size(titulo_text)[0]//2, 80 + offset_titulo
    )
    
    # Linha decorativa
    linha_y = 150
    linha_width = 280
    linha_x = width//2 - linha_width//2
    
    for i in range(linha_width):
        ratio = abs(i - linha_width//2) / (linha_width//2)
        alpha = int(120 * (1 - ratio))
        linha_surface = pygame.Surface((2, 3), pygame.SRCALPHA)
        linha_surface.fill((95, 111, 82, alpha))
        screen.blit(linha_surface, (linha_x + i, linha_y))
    
    # Campo de input moderno
    input_y = 220
    input_width = 420
    input_height = 70
    
    # Reposicionar input_rect
    input_rect.x = width//2 - input_width//2
    input_rect.y = input_y
    input_rect.width = input_width
    input_rect.height = input_height
    
    # Cores baseadas no estado
    if input_ativo:
        cor_fundo_topo = (255, 255, 255)
        cor_fundo_baixo = (245, 245, 245)
        cor_borda = (196, 102, 31)
        borda_width = 4
    else:
        cor_fundo_topo = (240, 235, 220)
        cor_fundo_baixo = (220, 215, 200)
        cor_borda = (185, 148, 112)
        borda_width = 3
    
    # Sombra removida do input
    # input_rect sem sombra
    
    # Gradiente do input
    input_gradiente = criar_gradiente_vertical(input_width, input_height, cor_fundo_topo, cor_fundo_baixo)
    screen.blit(input_gradiente, input_rect)
    
    # Borda do input
    pygame.draw.rect(screen, cor_borda, input_rect, borda_width, border_radius=15)
    
    # Texto do nome com estilo
    nome_upper = nome_jogador.upper()
    fonte_nome = pygame.font.SysFont("arial", 36, bold=True)
    
    if nome_upper:
        # Texto principal
        nome_render = fonte_nome.render(nome_upper, True, (80, 100, 60))
        nome_x = input_rect.x + (input_rect.w - nome_render.get_width()) // 2
        nome_y = input_rect.y + (input_rect.h - nome_render.get_height()) // 2
        screen.blit(nome_render, (nome_x, nome_y))
        
        # Cursor animado
        if input_ativo and cursor_visible:
            cursor_x = nome_x + nome_render.get_width() + 8
            cursor_y = nome_y + 6
            cursor_h = nome_render.get_height() - 12
            
            # Cor do cursor com animação
            alpha = int(200 + 55 * math.sin(tempo * 0.008))
            cursor_surface = pygame.Surface((3, cursor_h), pygame.SRCALPHA)
            cursor_surface.fill((196, 102, 31, alpha))
            screen.blit(cursor_surface, (cursor_x, cursor_y))
    else:
        # Placeholder
        fonte_placeholder = pygame.font.SysFont("arial", 28, italic=True)
        placeholder_text = "Digite aqui seu nome..."
        placeholder_render = fonte_placeholder.render(placeholder_text, True, (160, 160, 160))
        placeholder_x = input_rect.x + (input_rect.w - placeholder_render.get_width()) // 2
        placeholder_y = input_rect.y + (input_rect.h - placeholder_render.get_height()) // 2
        screen.blit(placeholder_render, (placeholder_x, placeholder_y))
        
        # Cursor inicial
        if input_ativo and cursor_visible:
            cursor_x = placeholder_x + placeholder_render.get_width() + 5
            cursor_y = placeholder_y + 4
            cursor_h = placeholder_render.get_height() - 8
            
            alpha = int(150 + 50 * math.sin(tempo * 0.008))
            cursor_surface = pygame.Surface((2, cursor_h), pygame.SRCALPHA)
            cursor_surface.fill((196, 102, 31, alpha))
            screen.blit(cursor_surface, (cursor_x, cursor_y))
    
    # Dicas elegantes
    fonte_dica = pygame.font.SysFont("arial", 22, italic=True)
    dica_text = "Pressione ENTER para iniciar ou clique no botão abaixo"
    dica_y = input_y + input_height + 35
    
    desenhar_texto_simples(
        screen, fonte_dica, dica_text,
        (120, 100, 80),
        width//2 - fonte_dica.size(dica_text)[0]//2, dica_y
    )
    
    # Botão iniciar moderno
    botao_y = dica_y + 50
    botao_width = 220
    botao_height = 65
    
    # Atualizar posição do botão
    botao_iniciar_nome.rect.y = botao_y
    botao_iniciar_nome.rect.x = width//2 - botao_width//2
    botao_iniciar_nome.rect.width = botao_width
    botao_iniciar_nome.rect.height = botao_height
    
    # Estado do botão
    mouse_pos = pygame.mouse.get_pos()
    botao_ativo = nome_jogador.strip() != ""
    hover_botao = botao_iniciar_nome.rect.collidepoint(mouse_pos) and botao_ativo  # Só hover se ativo
    
    if botao_ativo:
        if hover_botao:
            cor_botao_topo = (140, 200, 140)
            cor_botao_baixo = (120, 180, 120)
        else:
            cor_botao_topo = (120, 180, 120)
            cor_botao_baixo = (100, 160, 100)
        cor_texto_botao = (255, 255, 255)
        borda_cor = (80, 120, 80)
    else:
        # Botão completamente desabilitado - cinza sem gradiente
        cor_botao_topo = (140, 140, 140)
        cor_botao_baixo = (140, 140, 140)  # Mesmo cor para não ter gradiente
        cor_texto_botao = (100, 100, 100)
        borda_cor = (100, 100, 100)
    
    # Botão iniciar - usar sempre a função de gradiente para consistência
    aplicar_gradiente_com_bordas(
        screen, botao_iniciar_nome.rect, cor_botao_topo, cor_botao_baixo, 18
    )
    
    # Borda do botão
    pygame.draw.rect(screen, borda_cor, botao_iniciar_nome.rect, 3, border_radius=18)
    
    # Texto do botão - sempre mostrar mas com cor diferente
    fonte_botao = pygame.font.SysFont("arial", 30, bold=True)
    botao_text = "Iniciar Jogo"
    botao_label = fonte_botao.render(botao_text, True, cor_texto_botao)
    texto_x = botao_iniciar_nome.rect.x + (botao_iniciar_nome.rect.w - botao_label.get_width())//2
    texto_y = botao_iniciar_nome.rect.y + (botao_iniciar_nome.rect.h - botao_label.get_height())//2
    screen.blit(botao_label, (texto_x, texto_y))
    
    # Efeito de brilho no hover
    if hover_botao and botao_ativo:
        brilho_surface = pygame.Surface(botao_iniciar_nome.rect.size, pygame.SRCALPHA)
        brilho_alpha = int(20 + 15 * math.sin(tempo * 0.01))
        brilho_surface.fill((255, 255, 255, brilho_alpha))
        screen.blit(brilho_surface, botao_iniciar_nome.rect)
    
    # Instrução de volta
    fonte_voltar = pygame.font.SysFont("arial", 18, italic=True)
    voltar_text = "Pressione ESC para voltar ao menu"
    desenhar_texto_simples(
        screen, fonte_voltar, voltar_text,
        (100, 90, 70),
        40, height-60
    ) 

def desenhar_config_multiplayer_config(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_BOTAO, COR_BOTAO_HOVER, COR_TEXTO_CLARO_DESTACADO, num_jogadores, max_letras_rodada):
    width, height = screen.get_size()
    tempo = pygame.time.get_ticks()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Gradiente de fundo (PALETA PADRÃO)
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    desenhar_particulas_fundo(screen, tempo)
    
    bloco_top = height//2 - 120
    espacamento_linha = 60
    btn_size = 36
    
    # Título com efeito moderno
    fonte_titulo = pygame.font.SysFont("arial", 52, bold=True)
    titulo_text = "Configuração Multiplayer"
    desenhar_texto_simples(
        screen, fonte_titulo, titulo_text,
        COR_TEXTO_CLARO,
        width//2 - fonte_titulo.size(titulo_text)[0]//2, bloco_top - 80
    )
    
    # Seção jogadores
    fonte_label = pygame.font.SysFont("arial", 28, bold=True)
    label_jog_text = "Número de jogadores (2-6):"
    label_x = width//2 - 280
    label_y = bloco_top
    
    desenhar_texto_simples(
        screen, fonte_label, label_jog_text,
        COR_TEXTO_CLARO,
        label_x, label_y
    )
    
    # Controles centralizados com estilo
    centro_x = width//2 + 120
    offset = 18
    btn_size_small = 28
    
    menos_rect = pygame.Rect(centro_x - btn_size_small - offset, label_y + 4, btn_size_small, btn_size_small)
    mais_rect = pygame.Rect(centro_x + offset, label_y + 4, btn_size_small, btn_size_small)
    
    # Botões com gradiente
    hover_menos = menos_rect.collidepoint(mouse_x, mouse_y)
    hover_mais = mais_rect.collidepoint(mouse_x, mouse_y)
    
    # Botão menos com gradiente e bordas arredondadas (sem vazamento)
    cor_menos_topo = (160, 100, 40) if hover_menos else (140, 80, 20)  # Paleta padrão
    cor_menos_baixo = (140, 80, 20) if hover_menos else (120, 60, 10)
    
    # Usar função que previne vazamento
    aplicar_gradiente_com_bordas(screen, menos_rect, cor_menos_topo, cor_menos_baixo, btn_size_small//2)
    pygame.draw.circle(screen, (100, 100, 100), menos_rect.center, btn_size_small//2, 2)
    
    # Botão mais com gradiente e bordas arredondadas (sem vazamento)
    cor_mais_topo = (160, 100, 40) if hover_mais else (140, 80, 20)  # Paleta padrão
    cor_mais_baixo = (140, 80, 20) if hover_mais else (120, 60, 10)
    
    aplicar_gradiente_com_bordas(screen, mais_rect, cor_mais_topo, cor_mais_baixo, btn_size_small//2)
    pygame.draw.circle(screen, (100, 100, 100), mais_rect.center, btn_size_small//2, 2)
    
    # Setas
    fonte_seta = pygame.font.SysFont("arial", 18, bold=True)
    seta_esq = fonte_seta.render("<", True, (60, 60, 60))
    seta_dir = fonte_seta.render(">", True, (60, 60, 60))
    screen.blit(seta_esq, (menos_rect.x + (btn_size_small - seta_esq.get_width())//2, menos_rect.y + (btn_size_small - seta_esq.get_height())//2))
    screen.blit(seta_dir, (mais_rect.x + (btn_size_small - seta_dir.get_width())//2, mais_rect.y + (btn_size_small - seta_dir.get_height())//2))
    
    # Número de jogadores destacado
    fonte_numero = pygame.font.SysFont("arial", 32, bold=True)
    num_label = fonte_numero.render(str(num_jogadores), True, COR_TEXTO_CLARO_DESTACADO)
    num_x = centro_x - num_label.get_width()//2
    
    # Fundo para o número
    num_bg = pygame.Rect(num_x - 10, label_y, num_label.get_width() + 20, 36)
    num_surface = pygame.Surface((num_bg.width, num_bg.height), pygame.SRCALPHA)
    num_surface.fill((255, 255, 255, 80))
    screen.blit(num_surface, num_bg)
    pygame.draw.rect(screen, COR_TEXTO_CLARO_DESTACADO, num_bg, 2, border_radius=8)
    
    screen.blit(num_label, (num_x, label_y + 2))
    
    # Seção letras
    label_letras_text = "Máximo de letras (4-20):"
    label_ly = bloco_top + espacamento_linha
    
    desenhar_texto_simples(
        screen, fonte_label, label_letras_text,
        COR_TEXTO_CLARO,
        label_x, label_ly
    )
    
    menos_l_rect = pygame.Rect(centro_x - btn_size_small - offset, label_ly + 4, btn_size_small, btn_size_small)
    mais_l_rect = pygame.Rect(centro_x + offset, label_ly + 4, btn_size_small, btn_size_small)
    
    hover_menos_l = menos_l_rect.collidepoint(mouse_x, mouse_y)
    hover_mais_l = mais_l_rect.collidepoint(mouse_x, mouse_y)
    
    # Botões de letras com gradiente (paleta padrão, sem vazamento)
    cor_menos_l_topo = (160, 100, 40) if hover_menos_l else (140, 80, 20)
    cor_menos_l_baixo = (140, 80, 20) if hover_menos_l else (120, 60, 10)
    aplicar_gradiente_com_bordas(screen, menos_l_rect, cor_menos_l_topo, cor_menos_l_baixo, btn_size_small//2)
    pygame.draw.circle(screen, (100, 100, 100), menos_l_rect.center, btn_size_small//2, 2)
    
    cor_mais_l_topo = (160, 100, 40) if hover_mais_l else (140, 80, 20)
    cor_mais_l_baixo = (140, 80, 20) if hover_mais_l else (120, 60, 10)
    aplicar_gradiente_com_bordas(screen, mais_l_rect, cor_mais_l_topo, cor_mais_l_baixo, btn_size_small//2)
    pygame.draw.circle(screen, (100, 100, 100), mais_l_rect.center, btn_size_small//2, 2)
    
    screen.blit(seta_esq, (menos_l_rect.x + (btn_size_small - seta_esq.get_width())//2, menos_l_rect.y + (btn_size_small - seta_esq.get_height())//2))
    screen.blit(seta_dir, (mais_l_rect.x + (btn_size_small - seta_dir.get_width())//2, mais_l_rect.y + (btn_size_small - seta_dir.get_height())//2))
    
    # Número de letras
    max_label = fonte_numero.render(str(max_letras_rodada), True, COR_TEXTO_CLARO_DESTACADO)
    max_x = centro_x - max_label.get_width()//2
    
    max_bg = pygame.Rect(max_x - 10, label_ly, max_label.get_width() + 20, 36)
    max_surface = pygame.Surface((max_bg.width, max_bg.height), pygame.SRCALPHA)
    max_surface.fill((255, 255, 255, 80))
    screen.blit(max_surface, max_bg)
    pygame.draw.rect(screen, COR_TEXTO_CLARO_DESTACADO, max_bg, 2, border_radius=8)
    
    screen.blit(max_label, (max_x, label_ly + 2))
    
    # Botões principais
    btn_avancar_rect = pygame.Rect(width//2 + 40, bloco_top + espacamento_linha*2 + 40, 180, 60)
    btn_voltar_rect = pygame.Rect(width//2 - 220, bloco_top + espacamento_linha*2 + 40, 160, 60)
    
    hover_avancar = btn_avancar_rect.collidepoint(mouse_x, mouse_y) and (2 <= num_jogadores <= 6 and 4 <= max_letras_rodada <= 20)
    hover_voltar = btn_voltar_rect.collidepoint(mouse_x, mouse_y)
    
    # Botão avançar (paleta padrão)
    if 2 <= num_jogadores <= 6 and 4 <= max_letras_rodada <= 20:
        cor_avancar_topo = (140, 180, 70) if hover_avancar else (120, 160, 60)  # Verde da paleta
        cor_avancar_baixo = (120, 160, 50) if hover_avancar else (100, 140, 40)
        borda_cor = (80, 120, 40)
    else:
        cor_avancar_topo = (160, 160, 160)
        cor_avancar_baixo = (140, 140, 140)
        borda_cor = (100, 100, 100)
    
    aplicar_gradiente_com_bordas(screen, btn_avancar_rect, cor_avancar_topo, cor_avancar_baixo, 16)
    pygame.draw.rect(screen, borda_cor, btn_avancar_rect, 3, border_radius=16)
    
    fonte_botao = pygame.font.SysFont("arial", 26, bold=True)
    avancar_text = "Avançar"
    avancar_label = fonte_botao.render(avancar_text, True, (255, 255, 255))
    screen.blit(avancar_label, (btn_avancar_rect.x + (btn_avancar_rect.w - avancar_label.get_width())//2, btn_avancar_rect.y + 15))
    
    # Botão voltar (paleta padrão)
    cor_voltar_topo = (180, 120, 60) if hover_voltar else (160, 100, 50)  # Laranja da paleta
    cor_voltar_baixo = (160, 100, 40) if hover_voltar else (140, 80, 30)
    
    aplicar_gradiente_com_bordas(screen, btn_voltar_rect, cor_voltar_topo, cor_voltar_baixo, 16)
    pygame.draw.rect(screen, (120, 70, 30), btn_voltar_rect, 3, border_radius=16)
    
    voltar_text = "Voltar"
    voltar_label = fonte_botao.render(voltar_text, True, (255, 255, 255))
    screen.blit(voltar_label, (btn_voltar_rect.x + (btn_voltar_rect.w - voltar_label.get_width())//2, btn_voltar_rect.y + 15))
    
    return menos_rect, mais_rect, menos_l_rect, mais_l_rect, btn_avancar_rect, btn_voltar_rect

def desenhar_config_multiplayer_nomes(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, cor_input_inativo, cor_input_borda, COR_BOTAO, COR_BOTAO_HOVER, num_jogadores, nomes_jogadores, foco_idx, multiplayer_erro_msg):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Gradiente de fundo (PALETA PADRÃO)
    width, height = screen.get_size()
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    tempo = pygame.time.get_ticks()
    desenhar_particulas_fundo(screen, tempo)
    
    titulo = FONT_BIG.render("Nomes dos Jogadores", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 40))
    bloco_top = 120
    campo_largura = 380
    campo_altura = 44
    bloco_nomes_top = bloco_top + 20
    input_nomes = []
    for i in range(num_jogadores):
        y = bloco_nomes_top + i*(campo_altura + 18)
        label = FONT_SMALL.render(f"Jogador {i+1}:", True, COR_TEXTO_CLARO)
        screen.blit(label, (screen.get_width()//2 - 260, y + 8))
        rect = pygame.Rect(screen.get_width()//2 - campo_largura//2 + 40, y, campo_largura, campo_altura)
        cor_borda = (185, 148, 112) if foco_idx != i else (196, 102, 31)
        pygame.draw.rect(screen, cor_input_inativo, rect, border_radius=10)
        pygame.draw.rect(screen, cor_borda, rect, 3, border_radius=10)
        nome = nomes_jogadores[i] if i < len(nomes_jogadores) else ""
        nome_render = FONT_MED.render(nome.upper(), True, COR_TEXTO_CLARO)
        screen.blit(nome_render, (rect.x + (campo_largura - nome_render.get_width())//2, rect.y + 6))
        input_nomes.append((rect, i))
    
    # Centralizar botões
    btn_w, btn_h = 180, 56
    espacamento = 60
    centro_x = screen.get_width()//2
    y_btns = bloco_nomes_top + num_jogadores*(campo_altura + 18) + 48
    btn_voltar_rect = pygame.Rect(centro_x - btn_w - espacamento//2, y_btns, btn_w, btn_h)
    btn_iniciar_rect = pygame.Rect(centro_x + espacamento//2, y_btns, btn_w, btn_h)
    
    # Botões com paleta padrão e gradiente sem vazamento
    nomes_ok = all(n.strip() for n in nomes_jogadores[:num_jogadores])
    
    # Botão iniciar
    hover_iniciar = btn_iniciar_rect.collidepoint(mouse_x, mouse_y) and nomes_ok
    if nomes_ok:
        cor_iniciar_topo = (140, 180, 70) if hover_iniciar else (120, 160, 60)  # Verde da paleta
        cor_iniciar_baixo = (120, 160, 50) if hover_iniciar else (100, 140, 40)
        borda_iniciar = (80, 120, 40)
    else:
        cor_iniciar_topo = (160, 160, 160)
        cor_iniciar_baixo = (140, 140, 140)
        borda_iniciar = (100, 100, 100)
    
    aplicar_gradiente_com_bordas(screen, btn_iniciar_rect, cor_iniciar_topo, cor_iniciar_baixo, 14)
    pygame.draw.rect(screen, borda_iniciar, btn_iniciar_rect, 3, border_radius=14)
    
    # Botão voltar
    hover_voltar = btn_voltar_rect.collidepoint(mouse_x, mouse_y)
    cor_voltar_topo = (180, 120, 60) if hover_voltar else (160, 100, 50)  # Laranja da paleta
    cor_voltar_baixo = (160, 100, 40) if hover_voltar else (140, 80, 30)
    
    aplicar_gradiente_com_bordas(screen, btn_voltar_rect, cor_voltar_topo, cor_voltar_baixo, 14)
    pygame.draw.rect(screen, (120, 70, 30), btn_voltar_rect, 3, border_radius=14)
    iniciar_label = FONT_MED.render("Iniciar", True, (60, 60, 60))
    voltar_label = FONT_MED.render("Voltar", True, (60, 60, 60))
    screen.blit(iniciar_label, (btn_iniciar_rect.x + (btn_iniciar_rect.w - iniciar_label.get_width())//2, btn_iniciar_rect.y + 10))
    screen.blit(voltar_label, (btn_voltar_rect.x + (btn_voltar_rect.w - voltar_label.get_width())//2, btn_voltar_rect.y + 10))
    if multiplayer_erro_msg:
        erro_label = FONT_SMALL.render(multiplayer_erro_msg, True, (196, 102, 31))
        screen.blit(erro_label, (screen.get_width()//2 - erro_label.get_width()//2, btn_iniciar_rect.y + 64))
    return btn_iniciar_rect, btn_voltar_rect, input_nomes

def desenhar_espera_multiplayer(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_BOTAO, COR_BOTAO_HOVER, jogador_adivinha):
    # Gradiente de fundo (PALETA PADRÃO)
    width, height = screen.get_size()
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    tempo = pygame.time.get_ticks()
    desenhar_particulas_fundo(screen, tempo)
    
    titulo = FONT_BIG.render("Passe para o próximo jogador!", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 100))
    instr = FONT_MED.render(f"{jogador_adivinha}, clique em Pronto para começar", True, COR_TEXTO_CLARO)
    screen.blit(instr, (screen.get_width()//2 - instr.get_width()//2, 200))
    
    btn_pronto_rect = pygame.Rect(screen.get_width()//2 - 100, 320, 200, 60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_pronto = btn_pronto_rect.collidepoint(mouse_x, mouse_y)
    
    # Botão com paleta padrão e gradiente sem vazamento
    cor_pronto_topo = (140, 180, 70) if hover_pronto else (120, 160, 60)  # Verde da paleta
    cor_pronto_baixo = (120, 160, 50) if hover_pronto else (100, 140, 40)
    
    aplicar_gradiente_com_bordas(screen, btn_pronto_rect, cor_pronto_topo, cor_pronto_baixo, 14)
    pygame.draw.rect(screen, (80, 120, 40), btn_pronto_rect, 2, border_radius=14)
    pronto_label = FONT_MED.render("Pronto", True, (60, 60, 60))
    screen.blit(pronto_label, (btn_pronto_rect.x + (btn_pronto_rect.w - pronto_label.get_width())//2, btn_pronto_rect.y + 12))
    return btn_pronto_rect

def desenhar_definir_palavra_multiplayer(screen, FONT_BIG, FONT_MED, cor_input_inativo, jogador_definidor, jogador_adivinha, palavra_atual):
    # Gradiente de fundo (PALETA PADRÃO)
    width, height = screen.get_size()
    gradiente = criar_gradiente_vertical(width, height, (240, 225, 195), (210, 195, 165))
    screen.blit(gradiente, (0, 0))
    
    # Partículas de fundo
    tempo = pygame.time.get_ticks()
    desenhar_particulas_fundo(screen, tempo)
    
    titulo = FONT_BIG.render(f"{jogador_definidor} define a palavra para {jogador_adivinha}", True, (120, 100, 80))  # Cor terrosa da paleta
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))
    instr = FONT_MED.render("DIGITE A PALAVRA SECRETA, MÍNIMO 4 LETRAS", True, (120, 100, 80))
    screen.blit(instr, (screen.get_width()//2 - instr.get_width()//2, 180))
    campo_largura = 340
    campo_altura = 54
    input_rect = pygame.Rect(screen.get_width()//2 - campo_largura//2, 260, campo_largura, campo_altura)
    pygame.draw.rect(screen, cor_input_inativo, input_rect, border_radius=12)
    pygame.draw.rect(screen, (196, 102, 31), input_rect, 3, border_radius=12)
    palavra_render = FONT_MED.render(palavra_atual.upper(), True, (95, 111, 82))
    screen.blit(palavra_render, (input_rect.x + (campo_largura - palavra_render.get_width())//2, input_rect.y + 10))
    btn_confirmar_rect = pygame.Rect(screen.get_width()//2 - 80, 340, 160, 48)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_confirmar = btn_confirmar_rect.collidepoint(mouse_x, mouse_y)
    
    # Botão confirmar com paleta padrão
    cor_confirmar_topo = (140, 180, 70) if hover_confirmar else (120, 160, 60)  # Verde da paleta
    cor_confirmar_baixo = (120, 160, 50) if hover_confirmar else (100, 140, 40)
    
    aplicar_gradiente_com_bordas(screen, btn_confirmar_rect, cor_confirmar_topo, cor_confirmar_baixo, 12)
    pygame.draw.rect(screen, (80, 120, 40), btn_confirmar_rect, 2, border_radius=12)
    confirmar_label = FONT_MED.render("Confirmar", True, (255, 255, 255))
    screen.blit(confirmar_label, (btn_confirmar_rect.x + (btn_confirmar_rect.w - confirmar_label.get_width())//2, btn_confirmar_rect.y + 8))
    return input_rect, btn_confirmar_rect 

if __name__ == '__main__':
    pass 