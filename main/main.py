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

#controlar a velocidade de atualização do personagem
clock = pg.time.Clock()

gato = Personagem()
cao = Cachorro(400,466,100,500)

bloco_grande = Bloco(
    "assets/cenário/bloco_grande.png",
    250,
    350,
    200,
    200
)

bloco_pequeno = Bloco(
    "assets/cenário/bloco_pequeno.png",
    200,
    450,
    100,
    70
)

#Coletável de maneira aleatória e intercalável para que não fique um muito próximo do outro
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
                cao = Cachorro(400,466,100,500)
                coletaveis = [Peixe(), Novelo(), Bota()]
                peixe_coletado = False
                bota_coletada = False
                novelo_coletado = False
        
        gato.eventos(event)
    gato.atualizar()
    cao.atualizar(gato)

    tempo_atual = pg.time.get_ticks()
    if tempo_atual >= proximo:
        tipo = random.choice(tipos_coletaveis)
        coletaveis.append(tipo())
        proximo = tempo_atual + random.randint(3000, 7000)
    
    if not gato.gato_vivo:
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - gato.tempo_morte >= 3000:
            janela.fill((0,0,0))

            fonte = pg.font.Font(None,50)
            texto = fonte.render("Deseja reiniciar? (Y) Sim (ESC) Sair", True,(255,255,255))

            janela.blit(texto,(100,255)) 
            pg.display.flip()

            continue        
    for coletavel in coletaveis[:]:
        if gato.rect.colliderect(coletavel.rect):
            coletavel.acao(gato)
            coletaveis.remove(coletavel)

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

    bloco_grande.desenhar(janela)
    bloco_pequeno.desenhar(janela)

    gato.desenhar(janela)
    cao.desenhar_cao(janela)
    for coletavel in coletaveis:
        janela.blit(coletavel.imagem, coletavel.rect)
   
    pg.display.flip()
        
    clock.tick(15)
pg.quit()