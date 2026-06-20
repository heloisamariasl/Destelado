import pygame as pg
from personagem import Personagem
from inimigo import Cachorro
from coletaveis import Coletaveis

pg.init()
janela = pg.display.set_mode((800, 600))
pg.display.set_caption("Destelado")

#controlar a velocidade de atualização do personagem
clock = pg.time.Clock()

gato = Personagem()
cao = Cachorro(400,306,100,500)

#Coletável 
#peixe
peixe = Coletaveis("peixe", 1, 0) # acao é 'peixe', valor é 1, e tempo é 0

sair = False
peixe_coletado = False

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
                cao = Cachorro(400,306,100,500)
                peixe_coletado = False
        
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

    
    if not peixe_coletado and gato.rect.colliderect(peixe.rect): #Se o peixe ainda não foi coletado e o gato encostou nele
        peixe.peixe(gato)
        peixe_coletado = True #Define como coletado para impedir novas colisões e sumir com o peixe
    if cao.cao_vivo and gato.gato_vivo and gato.rect.colliderect(cao.rect) and not gato.invulneravel:
        if gato.atacando_agora:
            cao.cao_vivo = False
        elif not gato.pulando_agora:
            gato.tomar_dano()

    janela.fill((30,30,30))
     
    gato.desenhar(janela)
    cao.desenhar_cao(janela)
    if not peixe_coletado: #Se o peixe não for coletado ele continua no mesmo lugar 
        janela.blit(peixe.imagem, peixe.rect)

    pg.display.flip()
        
    clock.tick(15)
pg.quit()