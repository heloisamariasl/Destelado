import pygame as pg
import random
from personagem import Personagem
from inimigo import Cachorro
from coletaveis import Peixe, Novelo, Bota, Catnip 
from blocos import Bloco
from menu import MenuPrincipal

pg.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
LARGURA_MUNDO = 4800   # 6 telas de largura
CHAO_PADRAO = 460

janela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pg.display.set_caption("Destelado")

# menu
menu = MenuPrincipal(janela)
estado = "menu"

fundo = pg.image.load("assets/cenário/background.png").convert()
fundo = pg.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))

# imagem da casa (linha de chegada)
casa_img = pg.image.load("assets/cenário/casa.png").convert_alpha()

clock = pg.time.Clock()

gato = Personagem()
gato.x_gato = 100

# inimigos espalhados pelo mundo
caes = [
    Cachorro(800,  466, 700,  1000),
    Cachorro(1600, 466, 1500, 1900),
    Cachorro(2800, 466, 2600, 3100),
    Cachorro(3800, 466, 3600, 4100),
]

# blocos espalhados pelo mundo (x, y, largura, altura)
dados_blocos = [
    (400,  450, 120, 60),
    (600,  420, 120, 60),
    (1200, 450, 120, 60),
    (1350, 420, 150, 60),
    (2000, 450, 120, 60),
    (2400, 450, 120, 60),
    (2550, 440, 150, 60),
    (3300, 450, 120, 60),
    (3450, 390, 120, 60),
    (3600, 370, 150, 60),
]
blocos = [Bloco("assets/cenário/bloco_pequeno.png", x, y, w, h) for x, y, w, h in dados_blocos]

# ponto de chegada (bandeira / fim do nível)
x_fim = LARGURA_MUNDO - 100

tipos_coletaveis = [Peixe, Novelo, Bota, Catnip]
coletaveis = []
proximo = pg.time.get_ticks() + random.randint(3000, 7000)

sair = False
nivel_completo = False

while not sair:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sair = True

        acao = menu.tratar_eventos(event)

        if acao == "jogar":
            estado = "jogo"
        elif acao == "reiniciar":
            gato = Personagem()
            gato.x_gato = 100

            caes = [
                Cachorro(800,466,700,1000),
                Cachorro(1600,466,1500,1900),
                Cachorro(2800,466,2600,3100),
                Cachorro(3800,466,3600,4100),
            ]

            coletaveis = []
            nivel_completo = False

            menu.tela_atual = "principal"
            estado = "jogo"

        elif acao == "sair":
            sair = True
       
        elif acao == "menu":
            menu.tela_atual = "principal"
            estado = "menu"

        gato.eventos(event)

        if event.type == pg.QUIT:
            sair = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sair = True

        gato.eventos(event)

    # ── câmera centralizada no gato, limitada às bordas do mundo ────────────
    if estado == "menu":
        menu.desenhar()
        pg.display.flip()
        clock.tick(60)
        continue

    camera_x = gato.x_gato - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))
    # ────────────────────────────────────────────────────────────────────────

    # limita o gato às bordas do mundo
    gato.x_gato = max(0, min(gato.x_gato, LARGURA_MUNDO - 50))

    # ── colisão com blocos ANTES de atualizar ────────────────────────────────
    gato.chao_y = CHAO_PADRAO
    gato.no_chao = gato.y_gato >= CHAO_PADRAO

    for bloco in blocos:
        rect_previsto = pg.Rect(gato.x_gato, gato.y_gato + gato.velocidade_y + gato.gravidade, 50, 64)

        if rect_previsto.colliderect(bloco.rect):
            if gato.velocidade_y >= 0 and gato.rect.bottom <= bloco.rect.top + 12:
                gato.chao_y = bloco.rect.top - gato.rect.height
                gato.no_chao = True
            elif gato.velocidade_y < 0 and gato.rect.top >= bloco.rect.bottom - 12:
                gato.y_gato = bloco.rect.bottom
                gato.velocidade_y = 0

    gato.atualizar()
    
    gato.no_chao = True
    gato.no_bloco = False
    gato.chao_y = CHAO_PADRAO
    
    for plataforma in blocos:
        if (gato.velocidade_y >= 0 and
            gato.rect.bottom >= plataforma.rect.top and 
            gato.rect.bottom - gato.velocidade_y <= plataforma.rect.top and 
            gato.rect.right > plataforma.rect.left and gato.rect.left < plataforma.rect.right):
            gato.chao_y = plataforma.rect.top - gato.rect.height
            gato.no_chao = True
            gato.no_bloco = True
    
    for plataforma in blocos:
        pg.draw.rect(janela, (255,0,0), (plataforma.rect.x - camera_x, plataforma.rect.y, plataforma.rect.width, plataforma.rect.height), 2)
    
    for cao in caes:
        cao.atualizar(gato)

    # verifica se chegou ao fim
    if gato.x_gato >= x_fim and not nivel_completo:
        nivel_completo = True

    # spawn de coletáveis no mundo
    tempo_atual = pg.time.get_ticks()
    if tempo_atual >= proximo:
        tipo = random.choice(tipos_coletaveis)
        # spawna em posição aleatória no mundo, na altura do chão
        obj = tipo()
        obj.rect.x = random.randint(200, LARGURA_MUNDO - 200)
        coletaveis.append(obj)
        proximo = tempo_atual + random.randint(3000, 7000)

    # tela de game over
    if not gato.gato_vivo:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_morte >= 3000:
            menu.tela_atual = "game_over"
            estado = "menu"
            continue

    # tela de vitória
    if nivel_completo:
        menu.tela_atual = "vitoria"
        estado = "menu"
        continue

    # coletáveis
    for coletavel in coletaveis[:]:
        if gato.rect.colliderect(coletavel.rect):
            coletavel.acao(gato)
            coletaveis.remove(coletavel)

    # colisão com cachorros
    for cao in caes:
        if cao.cao_vivo and gato.gato_vivo and gato.rect.colliderect(cao.rect) and not gato.invulneravel:

            if gato.atacando_agora:
                cao.cao_vivo = False
            elif not gato.pulando_agora:
                gato.tomar_dano()

    # expirar bota
    if gato.correndo_flag:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_bota >= gato.duracao_bota:
            gato.correndo_flag = False
            gato.velocidade_atual = gato.velocidade

    # expirar catnip
    if gato.dormindo:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_dormindo >= gato.duracao_dormindo:
            gato.dormindo = False

    # expirar novelo
    if gato.enrolado:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_enrolado >= gato.duracao_enrolado:
            gato.enrolado = False

    # ── Desenho (tudo deslocado por camera_x) ───────────────────────────────
    # fundo em tile para cobrir o mundo inteiro
    for i in range(LARGURA_MUNDO // LARGURA_TELA + 1):
        janela.blit(fundo, (i * LARGURA_TELA - camera_x, 0))

    # blocos
    for bloco in blocos:
        janela.blit(bloco.imagem, (bloco.rect.x - camera_x, bloco.rect.y))

    # marca o fim do nível
    janela.blit(casa_img, (x_fim - camera_x - casa_img.get_width() // 2, CHAO_PADRAO + 64 - casa_img.get_height()))

    # gato — desenhado na posição de tela (x_gato - camera_x)
    gato.desenhar(janela, camera_x)

    # cachorros
    for cao in caes:
        cao.desenhar_cao(janela, camera_x)

    # coletáveis
    for coletavel in coletaveis:
        janela.blit(coletavel.imagem, (coletavel.rect.x - camera_x, coletavel.rect.y))

    pg.display.flip()
    clock.tick(15)

pg.quit()