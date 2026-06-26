import pygame as pg
import random
from personagem import Personagem
from inimigo import Cachorro
from coletaveis import Peixe, Novelo, Bota
from blocos import Bloco

pg.init()

janela = pg.display.set_mode((800, 600))
pg.display.set_caption("Destelado")

fundo = pg.image.load("assets/cenário/background.png").convert()
fundo = pg.transform.scale(fundo, (800, 600))

clock = pg.time.Clock()

CHAO_PADRAO = 460

gato = Personagem()
cao = Cachorro(400, 466, 100, 500)

bloco_pequeno = Bloco("assets/cenário/bloco_pequeno.png", 200, 440, 100, 70)

# adicione mais blocos aqui
blocos = [bloco_pequeno]

tipos_coletaveis = [Peixe, Novelo, Bota]
coletaveis = []
proximo = pg.time.get_ticks() + random.randint(3000, 7000)

sair = False
peixe_coletado = False
novelo_coletado = False
bota_coletada = False

while not sair:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sair = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sair = True

            if not gato.gato_vivo:
                if event.key == pg.K_y:
                    gato = Personagem()
                    cao = Cachorro(400, 466, 100, 500)
                    coletaveis = []
                    peixe_coletado = False
                    bota_coletada = False
                    novelo_coletado = False

        gato.eventos(event)

    # ── Colisão com blocos ANTES de atualizar ───────────────────────────────
    # Reseta o chão para o padrão
    gato.chao_y = CHAO_PADRAO
    gato.no_chao = gato.y_gato >= CHAO_PADRAO  # atualiza no_chao para o chão padrão

    for bloco in blocos:
        # Rect antecipado: onde o gato estará depois de aplicar a gravidade
        rect_previsto = pg.Rect(gato.x_gato, gato.y_gato + gato.velocidade_y + gato.gravidade, 50, 64)

        if rect_previsto.colliderect(bloco.rect):
            # vindo de cima
            if gato.velocidade_y >= 0 and gato.rect.bottom <= bloco.rect.top + 12:
                gato.chao_y = bloco.rect.top - 64
                gato.no_chao = True

            # vindo de baixo
            elif gato.velocidade_y < 0 and gato.rect.top >= bloco.rect.bottom - 12:
                gato.y_gato = bloco.rect.bottom
                gato.velocidade_y = 0

        # colisão lateral (usa rect atual, não previsto)
        if gato.rect.colliderect(bloco.rect):
            if gato.velocidade_y >= 0 and gato.rect.bottom <= bloco.rect.top + 12:
                pass  # já tratado acima
            elif gato.rect.centerx < bloco.rect.centerx:
                gato.x_gato = bloco.rect.left - 50
            else:
                gato.x_gato = bloco.rect.right
    # ────────────────────────────────────────────────────────────────────────

    gato.atualizar()
    cao.atualizar(gato)

    # spawn de coletáveis
    tempo_atual = pg.time.get_ticks()
    if tempo_atual >= proximo:
        tipo = random.choice(tipos_coletaveis)
        coletaveis.append(tipo())
        proximo = tempo_atual + random.randint(3000, 7000)

    # tela de morte
    if not gato.gato_vivo:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_morte >= 3000:
            janela.fill((0, 0, 0))
            fonte = pg.font.Font(None, 50)
            texto = fonte.render("Deseja reiniciar? (Y) Sim (ESC) Sair", True, (255, 255, 255))
            janela.blit(texto, (100, 255))
            pg.display.flip()
            continue

    # coletáveis
    for coletavel in coletaveis[:]:
        if gato.rect.colliderect(coletavel.rect):
            coletavel.acao(gato)
            coletaveis.remove(coletavel)

    # colisão com cachorro
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

    # ── Desenho ─────────────────────────────────────────────────────────────
    janela.blit(fundo, (0, 0))

    for bloco in blocos:
        bloco.desenhar(janela)

    gato.desenhar(janela)
    cao.desenhar_cao(janela)

    for coletavel in coletaveis:
        janela.blit(coletavel.imagem, coletavel.rect)

    pg.display.flip()
    clock.tick(15)

pg.quit()