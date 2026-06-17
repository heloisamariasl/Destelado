import pygame as pg
from personagem import Personagem
from inimigo import Cachorro

pg.init()
janela = pg.display.set_mode((800, 600))
pg.display.set_caption("Destelado")

#controlar a velocidade de atualização do personagem
clock = pg.time.Clock()

gato = Personagem()
cao = Cachorro(400,306,100,500)

sair = False
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
    
    if cao.cao_vivo and gato.rect.colliderect(cao.rect) and not gato.invulneravel:
        if gato.atacando_agora:
            cao.cao_vivo = False
        
        elif not gato.invulneravel:
            gato.tomar_dano()
          
    janela.fill((30,30,30))
     
    gato.desenhar(janela)
    cao.desenhar_cao(janela)
    
    pg.display.flip()
        
    clock.tick(15)
pg.quit()