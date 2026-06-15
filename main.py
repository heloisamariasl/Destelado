import pygame as pg
from personagem import Personagem

pg.init()
janela = pg.display.set_mode((800, 600))
pg.display.set_caption("Destelado")

#controlar a velocidade de atualização do personagem
clock = pg.time.Clock()

gato = Personagem()

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

    janela.fill((30,30,30))
    
    gato.desenhar(janela)
    
    pg.display.flip()
        
    clock.tick(15)
pg.quit()