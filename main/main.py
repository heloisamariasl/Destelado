import pygame as pg
import random
from personagem import Personagem
from inimigo import Cachorro
from coletaveis import Peixe, Novelo, Bota, Catnip, posicao_aleatoria
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

# blocos espalhados pelo mundo (x, y, largura, altura)
def gerar_blocos():
    dados = []
    grupos = []
    x = 400
    y = 450

    while x < LARGURA_MUNDO - 300:
        inicio_grupo = x
        quantidade_blocos = random.randint(2, 4)
        for _ in range(quantidade_blocos):
            largura = random.choice([100, 120, 150])
            dados.append((x, y, largura, 60))
            ultimo_x = x
            ultimo_y = y
            ultima_largura = largura
            x += largura + random.randint(20, 60)
            y += random.choice([-30, 0, 30])
            y = max(300, min(y, 450))
        fim_grupo = ultimo_x + ultima_largura
        grupos.append((inicio_grupo, fim_grupo, ultimo_y))
        x += random.randint(180, 260)
        y = 450

    return dados, grupos

dados_blocos, grupos_blocos = gerar_blocos()

blocos = [Bloco("assets/cenário/bloco_pequeno.png", x, y, w, h) for x, y, w, h in dados_blocos]

# inimigos espalhados pelo mundo
caes = []
posicao_x_inicial = 800
for _ in range(7):
    x_cao = random.randint(posicao_x_inicial, posicao_x_inicial + 300)
    y_cao = 466
    
    ponto_ini = x_cao - 150
    ponto_fim = x_cao + 150

    caes.append(Cachorro(x_cao, y_cao, ponto_ini, ponto_fim))
    posicao_x_inicial += 550
    
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

            coletaveis = []
            nivel_completo = False
            
            dados_blocos, grupos_blocos = gerar_blocos()
            blocos = [Bloco("assets/cenário/bloco_pequeno.png", x, y, w, h) for x, y, w, h in dados_blocos]
            caes = []
            posicao_x_inicial = 800
            for _ in range(7):
                x_cao = random.randint(posicao_x_inicial, posicao_x_inicial + 300)
                y_cao = 466
                
                ponto_ini = x_cao - 150
                ponto_fim = x_cao + 150

                caes.append(Cachorro(x_cao, y_cao, ponto_ini, ponto_fim))
                posicao_x_inicial += 550
 
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
    gato.rect.x = gato.x_gato
    gato.rect.y = gato.y_gato
    
    gato.chao_y = CHAO_PADRAO
    gato.no_chao = (gato.y_gato >= CHAO_PADRAO)
    gato.no_bloco = False
    
    gato_pe_esquerdo = gato.rect.left + 10
    gato_pe_direito = gato.rect.right - 10

    for bloco in blocos:
        
        if gato_pe_direito > bloco.rect.left and gato_pe_esquerdo < bloco.rect.right:
            if gato.velocidade_y >= 0:
                if gato.rect.bottom <= bloco.rect.top + 15:
                    if gato.rect.bottom + gato.velocidade_y >= bloco.rect.top:
                        gato.chao_y = bloco.rect.top - gato.rect.height
                        gato.no_chao = True
                        gato.no_bloco = True
            elif gato.velocidade_y < 0:
                if gato.rect.top >= bloco.rect.bottom - 15:
                    if gato.rect.top + gato.velocidade_y <= bloco.rect.bottom:
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
    
    def gerar_posicao():
        while True:
            if random.random() < 0.5:
                x = random.randint(50, LARGURA_MUNDO - 200)
                y = CHAO_PADRAO
            else:
                bloco = random.choice(blocos)
                x = random.randint(bloco.rect.left, bloco.rect.right - 50)
                y = bloco.rect.top - 50
            if all(abs(x - c.rect.x) > 150 or abs(y - c.rect.y) > 50 for c in coletaveis):
                return (x, y)
    
    # spawn de coletáveis no mundo
    tempo_atual = pg.time.get_ticks()
    if tempo_atual >= proximo:
        tipo = random.choice(tipos_coletaveis)
        # spawna em posição aleatória no mundo, na altura do chão
        posicao = gerar_posicao()
        obj = tipo(posicao=posicao)
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