import pygame as pg
from personagem import Personagem
from inimigo import Cachorro
from coletaveis import Peixe, Novelo, Bota

pg.init()

janela = pg.display.set_mode((800, 600))
pg.display.set_caption("Destelado")

fundo = pg.image.load("assets/cenário/background.png").convert()
fundo = pg.transform.scale(fundo, (800, 600))

#controlar a velocidade de atualização do personagem
clock = pg.time.Clock()

gato = Personagem()
cao = Cachorro(400,466,100,500)

#Coletável 
#peixe
peixe = Peixe((600, 460)) 
#Novelo
novelo = Novelo((300, 465))

bota = Bota((150,460))

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
                cao = Cachorro(400,466,100,500)
                peixe_coletado = False
                bota_coletada = False
                novelo_coletado = False
        
        gato.eventos(event)
    gato.atualizar()
    cao.atualizar(gato)
    
    if not gato.gato_vivo:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_morte >= 3000:
            janela.fill((0,0,0))

            fonte = pg.font.Font(None,50)
            texto = fonte.render("Deseja reiniciar? (Y) Sim (ESC) Sair", True,(255,255,255))

            janela.blit(texto,(100,255)) 
            pg.display.flip()

            continue        
    if gato.enrolado:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_enrolado >= gato.duracao_enrolado:
            gato.enrolado = False
    if not peixe_coletado and gato.rect.colliderect(peixe.rect): #Se o peixe ainda não foi coletado e o gato encostou nele
        peixe.acao(gato)
        peixe_coletado = True #Define como coletado para impedir novas colisões e sumir com o peixe
    if not novelo_coletado and gato.rect.colliderect(novelo.rect):
        novelo.acao(gato)
        novelo_coletado = True
    if not bota_coletada and gato.rect.colliderect(bota.rect):
        bota.acao(gato)
        bota_coletada = True
    if cao.cao_vivo and gato.gato_vivo and gato.rect.colliderect(cao.rect) and not gato.invulneravel:
        if gato.atacando_agora:
            cao.cao_vivo = False
        elif not gato.pulando_agora:
            gato.tomar_dano()
    
    if gato.correndo_flag:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_bota >= gato.duracao_bota:
            gato.correndo_flag = False
            gato.velocidade_atual = gato.velocidade
        
    janela.blit(fundo,(0,0))
     
    gato.desenhar(janela)
    cao.desenhar_cao(janela)
    if not peixe_coletado: #Se o peixe não for coletado ele continua no mesmo lugar 
        janela.blit(peixe.imagem, peixe.rect)
    if not novelo_coletado:
        janela.blit(novelo.imagem, novelo.rect)
    if not bota_coletada:
        janela.blit(bota.imagem, bota.rect)

    pg.display.flip()
        
    clock.tick(15)
pg.quit()