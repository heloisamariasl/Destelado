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
        
        gato.eventos(event)
    gato.atualizar()
    cao.atualizar(gato)
    
    if not peixe_coletado and gato.rect.colliderect(peixe.rect): #Se o peixe ainda não foi coletado e o gato encostou nele
        peixe.peixe(gato)
        peixe_coletado = True #Define como coletado para impedir novas colisões e sumir com o peixe
    if cao.cao_vivo and gato.rect.colliderect(cao.rect) and not gato.invulneravel:
        if gato.atacando_agora:
            cao.cao_vivo = False
        
        elif not gato.invulneravel:
            gato.tomar_dano()
          
    janela.fill((30,30,30)) #Limpa a tela quando o peixe for coletado
     
    gato.desenhar(janela)
    cao.desenhar_cao(janela)
    if not peixe_coletado: #Se o peixe não for coletado ele continua no mesmo lugar 
        janela.blit(peixe.imagem, peixe.rect)

    pg.display.flip()
        
    clock.tick(15)
pg.quit()