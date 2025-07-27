import pygame
import json
# Removido: from JogoPygame import SOM_CLIQUE

# Função para desenhar o menu

def desenhar_menu(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, botoes_menu):
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("JOGO DE ADIVINHAÇÃO", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))
    subtitulo = FONT_MED.render("Desafio de Rivais", True, COR_TEXTO_CLARO_DESTACADO)
    screen.blit(subtitulo, (screen.get_width()//2 - subtitulo.get_width()//2, 150))
    for botao in botoes_menu:
        botao.desenhar(screen)

# Função para desenhar a tela de configurações

def desenhar_config(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, SOM_ATIVO, MUSICA_ATIVA, VOLUME_SOM, VOLUME_MUSICA, RESOLUCAO_ATUAL):
    import pygame
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("Configurações", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 60))
    y = 140
    mx, my = pygame.mouse.get_pos()
    x_label = 100
    x_btn = 620
    altura_btn = 36
    altura_btn_peq = 32
    # --- Áudio ---
    sec_audio = FONT_SMALL.render("Áudio", True, COR_TEXTO_CLARO)
    screen.blit(sec_audio, (x_label-20, y))
    y += 48
    label_som = FONT_SMALL.render("Volume dos Efeitos Sonoros:", True, COR_TEXTO_CLARO)
    screen.blit(label_som, (x_label, y+2))
    # Botões de volume efeitos
    btn_menos_som = pygame.Rect(370, y, 36, altura_btn_peq)
    btn_mais_som = pygame.Rect(370+36+8, y, 36, altura_btn_peq)
    cor_menos_som = (180,180,180) if btn_menos_som.collidepoint(mx, my) else (140,140,140)
    cor_mais_som = (180,180,180) if btn_mais_som.collidepoint(mx, my) else (140,140,140)
    pygame.draw.rect(screen, cor_menos_som, btn_menos_som, border_radius=8)
    pygame.draw.rect(screen, cor_mais_som, btn_mais_som, border_radius=8)
    menos_label = FONT_SMALL.render("-", True, (60,60,60))
    mais_label = FONT_SMALL.render("+", True, (60,60,60))
    screen.blit(menos_label, (btn_menos_som.x + (btn_menos_som.w - menos_label.get_width())//2, btn_menos_som.y + 4))
    screen.blit(mais_label, (btn_mais_som.x + (btn_mais_som.w - mais_label.get_width())//2, btn_mais_som.y + 4))
    # Valor do volume
    vol_som_label = FONT_SMALL.render(f"{int(VOLUME_SOM*100)}%", True, (60,60,60))
    screen.blit(vol_som_label, (btn_mais_som.x + btn_mais_som.w + 12, y+4))
    # Botão ativar/desativar som
    btn_som_w = FONT_SMALL.size("Ativo")[0] + 24 if SOM_ATIVO else FONT_SMALL.size("Inativo")[0] + 24
    btn_som = pygame.Rect(x_btn, y, btn_som_w, altura_btn_peq)
    if SOM_ATIVO:
        txt_som = FONT_SMALL.render("Ativo", True, (60,60,60))
        cor_som = (100,220,100) if btn_som.collidepoint(mx, my) else (120,200,120)
    else:
        txt_som = FONT_SMALL.render("Inativo", True, (255,255,255))
        cor_som = (180,100,100) if btn_som.collidepoint(mx, my) else (160,120,120)
    pygame.draw.rect(screen, cor_som, btn_som, border_radius=8)
    screen.blit(txt_som, (btn_som.x+12, btn_som.y + (btn_som.height - txt_som.get_height()) // 2))
    y += 44
    label_mus = FONT_SMALL.render("Volume da Música:", True, COR_TEXTO_CLARO)
    screen.blit(label_mus, (x_label, y+2))
    # Botões de volume música
    btn_menos_mus = pygame.Rect(370, y, 36, altura_btn_peq)
    btn_mais_mus = pygame.Rect(370+36+8, y, 36, altura_btn_peq)
    cor_menos_mus = (180,180,180) if btn_menos_mus.collidepoint(mx, my) else (140,140,140)
    cor_mais_mus = (180,180,180) if btn_mais_mus.collidepoint(mx, my) else (140,140,140)
    pygame.draw.rect(screen, cor_menos_mus, btn_menos_mus, border_radius=8)
    pygame.draw.rect(screen, cor_mais_mus, btn_mais_mus, border_radius=8)
    screen.blit(menos_label, (btn_menos_mus.x + (btn_menos_mus.w - menos_label.get_width())//2, btn_menos_mus.y + 4))
    screen.blit(mais_label, (btn_mais_mus.x + (btn_mais_mus.w - mais_label.get_width())//2, btn_mais_mus.y + 4))
    # Valor do volume
    vol_mus_label = FONT_SMALL.render(f"{int(VOLUME_MUSICA*100)}%", True, (60,60,60))
    screen.blit(vol_mus_label, (btn_mais_mus.x + btn_mais_mus.w + 12, y+4))
    # Botão ativar/desativar música
    btn_mus_w = FONT_SMALL.size("Ativo")[0] + 24 if MUSICA_ATIVA else FONT_SMALL.size("Inativo")[0] + 24
    btn_mus = pygame.Rect(x_btn, y, btn_mus_w, altura_btn_peq)
    if MUSICA_ATIVA:
        txt_mus = FONT_SMALL.render("Ativo", True, (60,60,60))
        cor_mus = (100,220,100) if btn_mus.collidepoint(mx, my) else (120,200,120)
    else:
        txt_mus = FONT_SMALL.render("Inativo", True, (255,255,255))
        cor_mus = (180,100,100) if btn_mus.collidepoint(mx, my) else (160,120,120)
    pygame.draw.rect(screen, cor_mus, btn_mus, border_radius=8)
    screen.blit(txt_mus, (btn_mus.x+12, btn_mus.y + (btn_mus.height - txt_mus.get_height()) // 2))
    # --- Progresso ---
    y += 60
    sec_prog = FONT_SMALL.render("Progresso", True, COR_TEXTO_CLARO)
    screen.blit(sec_prog, (x_label-20, y))
    y += 48
    txt_reset_palavras = FONT_SMALL.render("Limpar Palavras Usadas", True, (60,60,60))
    btn_reset_palavras_w = txt_reset_palavras.get_width() + 28
    btn_reset_palavras = pygame.Rect(x_label, y, btn_reset_palavras_w, altura_btn)
    cor_reset_palavras = (220,140,140) if btn_reset_palavras.collidepoint(mx, my) else (200,120,120)
    pygame.draw.rect(screen, cor_reset_palavras, btn_reset_palavras, border_radius=8)
    screen.blit(txt_reset_palavras, (btn_reset_palavras.x+14, btn_reset_palavras.y + (btn_reset_palavras.height - txt_reset_palavras.get_height()) // 2))
    txt_reset_ranking = FONT_SMALL.render("Resetar Ranking", True, (60,60,60))
    btn_reset_ranking_w = txt_reset_ranking.get_width() + 28
    espacamento_progresso = 60
    btn_reset_ranking = pygame.Rect(x_label+btn_reset_palavras_w+espacamento_progresso, y, btn_reset_ranking_w, altura_btn)
    cor_reset_ranking = (220,140,140) if btn_reset_ranking.collidepoint(mx, my) else (200,120,120)
    pygame.draw.rect(screen, cor_reset_ranking, btn_reset_ranking, border_radius=8)
    screen.blit(txt_reset_ranking, (btn_reset_ranking.x+14, btn_reset_ranking.y + (btn_reset_ranking.height - txt_reset_ranking.get_height()) // 2))
    # --- Botão Salvar e Sair ---
    btn_salvar_sair_w = 180
    btn_salvar_sair_h = 40
    btn_salvar_sair_x = screen.get_width()//2 - btn_salvar_sair_w//2
    btn_salvar_sair_y = y + 100
    btn_salvar_sair = pygame.Rect(btn_salvar_sair_x, btn_salvar_sair_y, btn_salvar_sair_w, btn_salvar_sair_h)
    cor_salvar_sair = (120, 180, 240) if btn_salvar_sair.collidepoint(mx, my) else (80, 140, 200)
    pygame.draw.rect(screen, cor_salvar_sair, btn_salvar_sair, border_radius=10)
    pygame.draw.rect(screen, (60, 100, 160), btn_salvar_sair, 2, border_radius=10)
    txt_salvar_sair = FONT_MED.render("Salvar e Sair", True, (255,255,255))
    screen.blit(txt_salvar_sair, (btn_salvar_sair.x + (btn_salvar_sair.w - txt_salvar_sair.get_width())//2, btn_salvar_sair.y + (btn_salvar_sair.h - txt_salvar_sair.get_height())//2))
    # Retorne o retângulo do botão para uso no evento
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
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("Ranking", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))
    # Carregar ranking do arquivo (exemplo: ranking_solo.json)
    try:
        with open('ranking_solo.json', 'r', encoding='utf-8') as f:
            ranking = json.load(f)
    except Exception:
        ranking = []
    # Separar por dificuldade
    dificuldades = ['Fácil', 'Médio', 'Difícil']
    y_base = 160
    col_width = 320
    total_width = col_width * len(dificuldades)
    x_start = screen.get_width()//2 - total_width//2
    for idx, dif in enumerate(dificuldades):
        top10 = [r for r in ranking if r.get('dificuldade') == dif]
        top10 = sorted(top10, key=lambda x: x.get('tempo', 9999))[:10]
        x_dif = x_start + idx * col_width
        
        # Título da dificuldade com destaque
        fonte_dificuldade = pygame.font.SysFont("arial", 28, bold=True)
        cor_dificuldade = (196, 102, 31)  # Laranja destacado
        titulo_dif = fonte_dificuldade.render(dif, True, cor_dificuldade)
        screen.blit(titulo_dif, (x_dif + col_width//2 - titulo_dif.get_width()//2, y_base))
        
        for i, r in enumerate(top10):
            nome = r.get('nome', '-')
            tempo = r.get('tempo', 0)
            palavra = r.get('palavra', '-')
            tempo_str = f"{tempo:.2f}s"
            
            # Fontes maiores e mais amigáveis
            fonte_nome = pygame.font.SysFont("arial", 22, bold=True)
            fonte_tempo = pygame.font.SysFont("arial", 20, bold=False)
            fonte_palavra = pygame.font.SysFont("arial", 18, bold=False)
            
            # Cores mais amigáveis
            cor_nome = (95, 111, 82)  # Verde escuro
            cor_tempo = (196, 102, 31)  # Laranja
            cor_palavra = (120, 100, 60)  # Marrom suave
            
            # Renderizar cada parte separadamente
            nome_label = fonte_nome.render(f"{i+1}. {nome} - ", True, cor_nome)
            tempo_label = fonte_tempo.render(tempo_str, True, cor_tempo)
            palavra_label = fonte_palavra.render(f" ({palavra})", True, cor_palavra)
            
            # Calcular posição centralizada
            x_centro = x_dif + (col_width - (nome_label.get_width() + tempo_label.get_width() + palavra_label.get_width())) // 2
            y_linha = y_base + 50 + i*35  # Aumentado espaçamento vertical
            
            # Desenhar cada parte
            screen.blit(nome_label, (x_centro, y_linha))
            screen.blit(tempo_label, (x_centro + nome_label.get_width(), y_linha))
            screen.blit(palavra_label, (x_centro + nome_label.get_width() + tempo_label.get_width(), y_linha))
    
    voltar = FONT_SMALL.render("Pressione ESC para voltar", True, COR_TEXTO_CLARO)
    screen.blit(voltar, (40, screen.get_height()-50))

# Função para desenhar a tela de dificuldade

def desenhar_dificuldade(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, btns_dificuldade, btn_dificuldade_hover):
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("Escolha a Dificuldade", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 120))
    mx, my = pygame.mouse.get_pos()
    for i, btn in enumerate(btns_dificuldade):
        rect = pygame.Rect(screen.get_width()//2 - 180, 220 + i*110, 360, 80)
        cor = btn["cor"]
        if rect.collidepoint(mx, my):
            cor = btn["hover"]
        pygame.draw.rect(screen, cor, rect, border_radius=14)
        label = FONT_MED.render(btn["label"], True, (60, 60, 60))
        desc = FONT_SMALL.render(btn["desc"], True, (60, 60, 60))
        screen.blit(label, (rect.x + 30, rect.y + 10))
        screen.blit(desc, (rect.x + 30, rect.y + 45))
        btn["rect"] = rect
    voltar = FONT_SMALL.render("Pressione ESC para voltar", True, COR_TEXTO_CLARO)
    screen.blit(voltar, (40, screen.get_height()-50))

# Função para desenhar tela de carregando palavra

def desenhar_carregando_palavra(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO):
    screen.fill(COR_FUNDO_PRINCIPAL)
    msg = FONT_BIG.render("Carregando palavra...", True, COR_TEXTO_CLARO)
    screen.blit(msg, (screen.get_width()//2 - msg.get_width()//2, screen.get_height()//2 - msg.get_height()//2))

# Função para desenhar tela de carregando palavra animado

def desenhar_carregando_palavra_animado(screen, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO):
    screen.fill(COR_FUNDO_PRINCIPAL)
    t = pygame.time.get_ticks() // 400 % 4
    pontos = '.' * t
    msg = FONT_BIG.render(f"Carregando palavra{pontos}", True, COR_TEXTO_CLARO)
    screen.blit(msg, (screen.get_width()//2 - msg.get_width()//2, screen.get_height()//2 - msg.get_height()//2))

# Função para desenhar tela final

def desenhar_tela_final(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_TEXTO_CLARO_DESTACADO, mensagem_final, tempo_exemplo, erros_exemplo, dificuldade=None):
    mx, my = pygame.mouse.get_pos()
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("FIM DE JOGO", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))
    msg = FONT_MED.render(mensagem_final, True, COR_TEXTO_CLARO_DESTACADO)
    screen.blit(msg, (screen.get_width()//2 - msg.get_width()//2, 180))
    tempo_str = f"Tempo: {tempo_exemplo:.2f}s"
    erros_str = f"Erros: {erros_exemplo}"
    tempo_label = FONT_MED.render(tempo_str, True, COR_TEXTO_CLARO)
    erros_label = FONT_MED.render(erros_str, True, COR_TEXTO_CLARO)
    screen.blit(tempo_label, (screen.get_width()//2 - tempo_label.get_width()//2, 260))
    screen.blit(erros_label, (screen.get_width()//2 - erros_label.get_width()//2, 310))
    # Botões organizados e mais largos
    btn_w, btn_h = 220, 60
    espacamento = 40
    total_w = btn_w * 2 + espacamento
    x0 = screen.get_width()//2 - total_w//2
    y0 = 400
    btn_jogar_rect = pygame.Rect(x0, y0, btn_w, btn_h)
    btn_menu_rect = pygame.Rect(x0 + btn_w + espacamento, y0, btn_w, btn_h)
    btn_def_rect = pygame.Rect(screen.get_width()//2 - 110, y0 + 80, 220, 44)
    # Hover
    cor_jogar = (120, 150, 60) if btn_jogar_rect.collidepoint(mx, my) else (169, 179, 136)
    cor_menu = (160, 80, 20) if btn_menu_rect.collidepoint(mx, my) else (169, 179, 136)
    cor_def = (140, 120, 80) if btn_def_rect.collidepoint(mx, my) else (169, 179, 136)
    pygame.draw.rect(screen, cor_jogar, btn_jogar_rect, border_radius=12)
    pygame.draw.rect(screen, cor_menu, btn_menu_rect, border_radius=12)
    pygame.draw.rect(screen, cor_def, btn_def_rect, border_radius=10)
    jogar_label = FONT_MED.render("Jogar Novamente", True, (60, 60, 60))
    menu_label = FONT_MED.render("Menu", True, (60, 60, 60))
    def_label = FONT_SMALL.render("Ver definição da palavra", True, (60, 60, 60))
    screen.blit(jogar_label, (btn_jogar_rect.x + (btn_jogar_rect.w - jogar_label.get_width())//2, btn_jogar_rect.y + (btn_jogar_rect.h - jogar_label.get_height())//2))
    screen.blit(menu_label, (btn_menu_rect.x + (btn_menu_rect.w - menu_label.get_width())//2, btn_menu_rect.y + (btn_menu_rect.h - menu_label.get_height())//2))
    screen.blit(def_label, (btn_def_rect.x + (btn_def_rect.w - def_label.get_width())//2, btn_def_rect.y + 10))
    # Ranking do nível jogado
    if dificuldade:
        import json
        try:
            with open('ranking_solo.json', 'r', encoding='utf-8') as f:
                ranking = json.load(f)
        except Exception:
            ranking = []
        top10 = [r for r in ranking if r.get('dificuldade') == dificuldade]
        top10 = sorted(top10, key=lambda x: x.get('tempo', 9999))[:10]
        y_base = btn_def_rect.y + btn_def_rect.height + 50  # aproxima o ranking dos botões
        ranking_titulo = FONT_BIG.render(f"Ranking - {dificuldade}", True, COR_TEXTO_CLARO_DESTACADO)
        screen.blit(ranking_titulo, (screen.get_width()//2 - ranking_titulo.get_width()//2, y_base))
        for i, r in enumerate(top10):
            nome = r.get('nome', '-')
            tempo = r.get('tempo', 0)
            palavra = r.get('palavra', '-')
            tempo_str = f"{tempo:.2f}s"
            fonte_nome = pygame.font.SysFont("arial", 28, bold=True)
            fonte_tempo = pygame.font.SysFont("arial", 28, bold=False)
            fonte_palavra = pygame.font.SysFont("arial", 24, bold=False)
            nome_label = fonte_nome.render(f"{i+1}. {nome} - ", True, (95, 111, 82))
            tempo_label = fonte_tempo.render(tempo_str, True, (196, 102, 31))
            palavra_label = fonte_palavra.render(f" ({palavra})", True, (120, 100, 60))
            x_centro = screen.get_width()//2 - (nome_label.get_width() + tempo_label.get_width() + palavra_label.get_width())//2
            y_linha = y_base + 60 + i*36
            screen.blit(nome_label, (x_centro, y_linha))
            screen.blit(tempo_label, (x_centro + nome_label.get_width(), y_linha))
            screen.blit(palavra_label, (x_centro + nome_label.get_width() + tempo_label.get_width(), y_linha))
    return btn_jogar_rect, btn_menu_rect, btn_def_rect

# Função para desenhar o jogo (modo solo)

def desenhar_jogo(screen, FONT_SMALL, FONT_BIG, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, cor_input_inativo, cor_input_borda, rodada_ativa, nome_jogador_exemplo, tempo_exemplo, erros_exemplo, palavra_embaralhada, letras_embaralhadas_usadas, letras_embaralhadas_pos, palavra_original, letras_adivinhadas, indice_atual, feedback_erro_idx, feedback_erro_timer, FEEDBACK_ERRO_DURATION, feedback_erro_circulo_idx, feedback_erro_circulo_timer, botao_desistir_rect, fim_rodada, shake_timer=0):
    screen.fill(COR_FUNDO_PRINCIPAL)
    # Topo: nome, tempo, erros
    if rodada_ativa:
        info = FONT_SMALL.render(f"Jogador: {nome_jogador_exemplo}   Tempo: {tempo_exemplo:.2f}s   Erros: {erros_exemplo}", True, COR_TEXTO_CLARO)
        screen.blit(info, (40, 30))
    # Palavra embaralhada (letras em círculos)
    letras_embaralhadas_pos.clear()
    shake_x, shake_y = 0, 0
    if shake_timer > 0:
        import random
        shake_x = random.randint(-8, 8)
        shake_y = random.randint(-8, 8)
    cx = screen.get_width()//2 - (len(palavra_embaralhada)*60)//2 + shake_x
    cy = 120 + shake_y
    for i, letra in enumerate(palavra_embaralhada):
        center = (cx + i*60 + 30, cy + 30)
        rect = pygame.Rect(center[0]-30, center[1]-30, 60, 60)
        if i == feedback_erro_circulo_idx and feedback_erro_circulo_timer > 0:
            cor = (196, 102, 31)  # laranja para erro
        elif letras_embaralhadas_usadas[i]:
            cor = (100, 200, 120)  # verde suave
        else:
            cor = (210, 180, 140)  # marrom claro
        pygame.draw.circle(screen, cor, center, 30)
        l = FONT_BIG.render(letra, True, (255, 255, 255))
        screen.blit(l, (center[0] - l.get_width()//2, center[1] - l.get_height()//2))
        letras_embaralhadas_pos.append((rect, letra, i))
    # Espaços para adivinhar (caixas)
    cx2 = screen.get_width()//2 - (len(palavra_original)*60)//2 + shake_x
    cy2 = 250 + shake_y
    for i in range(len(palavra_original)):
        rect = pygame.Rect(cx2 + i*60, cy2, 50, 60)
        if i == feedback_erro_idx and feedback_erro_timer > 0:
            pygame.draw.rect(screen, (196, 102, 31), rect, border_radius=8)
        elif letras_adivinhadas[i]:
            pygame.draw.rect(screen, (160, 130, 90), rect, border_radius=8)  # marrom escuro
        else:
            pygame.draw.rect(screen, (210, 180, 140), rect, border_radius=8)  # marrom claro
        pygame.draw.rect(screen, cor_input_borda, rect, 2, border_radius=8)
        letra = letras_adivinhadas[i]
        letra_render = FONT_BIG.render(letra, True, (255,255,255)) if letra else None
        if letra_render:
            screen.blit(letra_render, (rect.x + (rect.w - letra_render.get_width())//2, rect.y + (rect.h - letra_render.get_height())//2))
    # Botão desistir
    if rodada_ativa:
        pygame.draw.rect(screen, (169, 179, 136), botao_desistir_rect, border_radius=10)
        fonte_desistir = pygame.font.SysFont("arial", 24, bold=True)
        desistir_label = fonte_desistir.render("Desistir", True, (255,255,255))
        screen.blit(desistir_label, (botao_desistir_rect.x + (botao_desistir_rect.w - desistir_label.get_width())//2, botao_desistir_rect.y + (botao_desistir_rect.h - desistir_label.get_height())//2))
    # Instrução
    if rodada_ativa:
        instr = FONT_SMALL.render("Clique nas letras embaralhadas ou digite. ESC volta ao menu.", True, COR_TEXTO_CLARO)
        screen.blit(instr, (screen.get_width()//2 - instr.get_width()//2, screen.get_height() - 40))
    else:
        instr = FONT_SMALL.render("Rodada finalizada.", True, COR_TEXTO_CLARO)
        screen.blit(instr, (screen.get_width()//2 - instr.get_width()//2, screen.get_height() - 40))

# Função para desenhar tela de nome solo

def desenhar_nome_solo(screen, FONT_BIG, FONT_SMALL, cor_input_ativo, cor_input_inativo, cor_input_borda, input_rect, input_ativo, nome_jogador, cursor_visible, botao_iniciar_nome):
    screen.fill((249, 235, 199))
    titulo = FONT_BIG.render("Digite seu nome", True, (95, 111, 82))
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 120))
    input_y = 240
    pygame.draw.rect(screen, cor_input_ativo if input_ativo else cor_input_inativo, (input_rect.x, input_y, input_rect.w, input_rect.h), border_radius=10)
    pygame.draw.rect(screen, cor_input_borda, (input_rect.x, input_y, input_rect.w, input_rect.h), 2, border_radius=10)
    nome_upper = nome_jogador.upper()
    nome_render = pygame.font.SysFont("arial", 32, bold=True).render(nome_upper, True, (95, 111, 82))
    nome_x = input_rect.x + (input_rect.w - nome_render.get_width()) // 2
    nome_y = input_y + (input_rect.h - nome_render.get_height()) // 2
    screen.blit(nome_render, (nome_x, nome_y))
    if input_ativo and cursor_visible:
        cursor_x = nome_x + nome_render.get_width() + 4
        cursor_y = nome_y + 4
        cursor_h = nome_render.get_height() - 8
        pygame.draw.rect(screen, (95, 111, 82), (cursor_x, cursor_y, 2, cursor_h))
    dica = FONT_SMALL.render("Pressione ENTER para iniciar ou clique no botão", True, (95, 111, 82))
    dica_y = input_y + input_rect.h + 28
    screen.blit(dica, (screen.get_width()//2 - dica.get_width()//2, dica_y))
    botao_y = dica_y + 40
    botao_iniciar_nome.rect.y = botao_y
    botao_iniciar_nome.rect.x = screen.get_width()//2 - botao_iniciar_nome.rect.w//2
    botao_iniciar_nome.desenhar(screen)
    voltar = FONT_SMALL.render("Pressione ESC para voltar", True, (95, 111, 82))
    screen.blit(voltar, (40, screen.get_height()-50)) 

def desenhar_config_multiplayer_config(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_BOTAO, COR_BOTAO_HOVER, COR_TEXTO_CLARO_DESTACADO, num_jogadores, max_letras_rodada):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    bloco_top = screen.get_height()//2 - 120
    espacamento_linha = 60
    btn_size = 36
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("Configuração do Multiplayer", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, bloco_top - 80))
    # --- Linha de número de jogadores ---
    label_jog = FONT_MED.render("Número de jogadores (2-6):", True, COR_TEXTO_CLARO)
    label_x = screen.get_width()//2 - 260
    label_y = bloco_top
    screen.blit(label_jog, (label_x, label_y))
    # Centralizar controles
    centro_x = screen.get_width()//2 + 120
    # Reduzir espaço entre setas e número
    offset = 18  # era 40
    btn_size_small = 28  # era 36
    menos_rect = pygame.Rect(centro_x - btn_size_small - offset, label_y + 4, btn_size_small, btn_size_small)
    mais_rect = pygame.Rect(centro_x + offset, label_y + 4, btn_size_small, btn_size_small)
    cor_menos = COR_BOTAO_HOVER if menos_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    cor_mais = COR_BOTAO_HOVER if mais_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    pygame.draw.circle(screen, cor_menos, menos_rect.center, btn_size_small//2)
    pygame.draw.circle(screen, cor_mais, mais_rect.center, btn_size_small//2)
    seta_esq = FONT_MED.render("<", True, (60, 60, 60))
    seta_dir = FONT_MED.render(">", True, (60, 60, 60))
    screen.blit(seta_esq, (menos_rect.x + (btn_size_small - seta_esq.get_width())//2, menos_rect.y + (btn_size_small - seta_esq.get_height())//2))
    screen.blit(seta_dir, (mais_rect.x + (btn_size_small - seta_dir.get_width())//2, mais_rect.y + (btn_size_small - seta_dir.get_height())//2))
    num_label = FONT_MED.render(str(num_jogadores), True, COR_TEXTO_CLARO_DESTACADO)
    num_x = centro_x - num_label.get_width()//2
    screen.blit(num_label, (num_x, label_y + (btn_size_small - num_label.get_height())//2 + 4))
    # --- Linha de máximo de letras ---
    label_letras = FONT_MED.render("Máximo de letras (4-20):", True, COR_TEXTO_CLARO)
    label_ly = bloco_top + espacamento_linha
    screen.blit(label_letras, (label_x, label_ly))
    menos_l_rect = pygame.Rect(centro_x - btn_size_small - offset, label_ly + 4, btn_size_small, btn_size_small)
    mais_l_rect = pygame.Rect(centro_x + offset, label_ly + 4, btn_size_small, btn_size_small)
    cor_menos_l = COR_BOTAO_HOVER if menos_l_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    cor_mais_l = COR_BOTAO_HOVER if mais_l_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    pygame.draw.circle(screen, cor_menos_l, menos_l_rect.center, btn_size_small//2)
    pygame.draw.circle(screen, cor_mais_l, mais_l_rect.center, btn_size_small//2)
    screen.blit(seta_esq, (menos_l_rect.x + (btn_size_small - seta_esq.get_width())//2, menos_l_rect.y + (btn_size_small - seta_esq.get_height())//2))
    screen.blit(seta_dir, (mais_l_rect.x + (btn_size_small - seta_dir.get_width())//2, mais_l_rect.y + (btn_size_small - seta_dir.get_height())//2))
    max_label = FONT_MED.render(str(max_letras_rodada), True, COR_TEXTO_CLARO_DESTACADO)
    max_x = centro_x - max_label.get_width()//2
    screen.blit(max_label, (max_x, label_ly + (btn_size_small - max_label.get_height())//2 + 4))
    # --- Botões ---
    btn_avancar_rect = pygame.Rect(screen.get_width()//2 + 40, bloco_top + espacamento_linha*2 + 40, 160, 54)
    btn_voltar_rect = pygame.Rect(screen.get_width()//2 - 200, bloco_top + espacamento_linha*2 + 40, 140, 54)
    cor_avancar = COR_BOTAO_HOVER if btn_avancar_rect.collidepoint(mouse_x, mouse_y) and (2 <= num_jogadores <= 6 and 4 <= max_letras_rodada <= 20) else COR_BOTAO
    cor_voltar = COR_BOTAO_HOVER if btn_voltar_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    pygame.draw.rect(screen, cor_avancar, btn_avancar_rect, border_radius=14)
    pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_avancar_rect, 2, border_radius=14)
    pygame.draw.rect(screen, cor_voltar, btn_voltar_rect, border_radius=14)
    pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_voltar_rect, 2, border_radius=14)
    avancar_label = FONT_MED.render("Avançar", True, (60, 60, 60))
    voltar_label = FONT_MED.render("Voltar", True, (60, 60, 60))
    screen.blit(avancar_label, (btn_avancar_rect.x + (btn_avancar_rect.w - avancar_label.get_width())//2, btn_avancar_rect.y + 10))
    screen.blit(voltar_label, (btn_voltar_rect.x + (btn_voltar_rect.w - voltar_label.get_width())//2, btn_voltar_rect.y + 10))
    return menos_rect, mais_rect, menos_l_rect, mais_l_rect, btn_avancar_rect, btn_voltar_rect

def desenhar_config_multiplayer_nomes(screen, FONT_BIG, FONT_MED, FONT_SMALL, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, cor_input_inativo, cor_input_borda, COR_BOTAO, COR_BOTAO_HOVER, num_jogadores, nomes_jogadores, foco_idx, multiplayer_erro_msg):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill(COR_FUNDO_PRINCIPAL)
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
    nomes_ok = all(n.strip() for n in nomes_jogadores[:num_jogadores])
    cor_btn_iniciar = COR_BOTAO_HOVER if btn_iniciar_rect.collidepoint(mouse_x, mouse_y) and nomes_ok else COR_BOTAO
    cor_btn_voltar = COR_BOTAO_HOVER if btn_voltar_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    pygame.draw.rect(screen, cor_btn_iniciar, btn_iniciar_rect, border_radius=14)
    pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_iniciar_rect, 3, border_radius=14)
    pygame.draw.rect(screen, cor_btn_voltar, btn_voltar_rect, border_radius=14)
    pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_voltar_rect, 3, border_radius=14)
    iniciar_label = FONT_MED.render("Iniciar", True, (60, 60, 60))
    voltar_label = FONT_MED.render("Voltar", True, (60, 60, 60))
    screen.blit(iniciar_label, (btn_iniciar_rect.x + (btn_iniciar_rect.w - iniciar_label.get_width())//2, btn_iniciar_rect.y + 10))
    screen.blit(voltar_label, (btn_voltar_rect.x + (btn_voltar_rect.w - voltar_label.get_width())//2, btn_voltar_rect.y + 10))
    if multiplayer_erro_msg:
        erro_label = FONT_SMALL.render(multiplayer_erro_msg, True, (196, 102, 31))
        screen.blit(erro_label, (screen.get_width()//2 - erro_label.get_width()//2, btn_iniciar_rect.y + 64))
    return btn_iniciar_rect, btn_voltar_rect, input_nomes

def desenhar_espera_multiplayer(screen, FONT_BIG, FONT_MED, COR_FUNDO_PRINCIPAL, COR_TEXTO_CLARO, COR_BOTAO, COR_BOTAO_HOVER, jogador_adivinha):
    screen.fill(COR_FUNDO_PRINCIPAL)
    titulo = FONT_BIG.render("Passe para o próximo jogador!", True, COR_TEXTO_CLARO)
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 100))
    instr = FONT_MED.render(f"{jogador_adivinha}, clique em Pronto para começar", True, COR_TEXTO_CLARO)
    screen.blit(instr, (screen.get_width()//2 - instr.get_width()//2, 200))
    btn_pronto_rect = pygame.Rect(screen.get_width()//2 - 100, 320, 200, 60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cor_btn = COR_BOTAO_HOVER if btn_pronto_rect.collidepoint(mouse_x, mouse_y) else COR_BOTAO
    pygame.draw.rect(screen, cor_btn, btn_pronto_rect, border_radius=14)
    pygame.draw.rect(screen, COR_BOTAO_HOVER, btn_pronto_rect, 2, border_radius=14)
    pronto_label = FONT_MED.render("Pronto", True, (60, 60, 60))
    screen.blit(pronto_label, (btn_pronto_rect.x + (btn_pronto_rect.w - pronto_label.get_width())//2, btn_pronto_rect.y + 12))
    return btn_pronto_rect

def desenhar_definir_palavra_multiplayer(screen, FONT_BIG, FONT_MED, cor_input_inativo, jogador_definidor, jogador_adivinha, palavra_atual):
    screen.fill((249, 235, 199))
    titulo = FONT_BIG.render(f"{jogador_definidor} define a palavra para {jogador_adivinha}", True, (95, 111, 82))
    screen.blit(titulo, (screen.get_width()//2 - titulo.get_width()//2, 80))
    instr = FONT_MED.render("DIGITE A PALAVRA SECRETA, MÍNIMO 4 LETRAS", True, (95, 111, 82))
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
    cor_btn = (185, 148, 112) if btn_confirmar_rect.collidepoint(mouse_x, mouse_y) else (169, 179, 136)
    pygame.draw.rect(screen, cor_btn, btn_confirmar_rect, border_radius=12)
    pygame.draw.rect(screen, (185, 148, 112), btn_confirmar_rect, 2, border_radius=12)
    confirmar_label = FONT_MED.render("Confirmar", True, (60, 60, 60))
    screen.blit(confirmar_label, (btn_confirmar_rect.x + (btn_confirmar_rect.w - confirmar_label.get_width())//2, btn_confirmar_rect.y + 8))
    return input_rect, btn_confirmar_rect 

if __name__ == '__main__':
    pass 