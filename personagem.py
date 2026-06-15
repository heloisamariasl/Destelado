import pygame as pg
from pygame.locals import *

pg.init()

janela = pg.display.set_mode((800, 600))
pg.display.set_caption("Destelado")

parado = pg.image.load('./Cat Game Assets/Tilesets/Cat1_Standing.png').convert_alpha()
andando = pg.image.load('./Cat Game Assets/Tilesets/Cat1_Walking.png').convert_alpha()
pulando = pg.image.load('./Cat Game Assets/Tilesets/Cat1_Jumping.png').convert_alpha()
ult = pg.image.load('./Cat Game Assets/Tilesets/Cat1_Attack3.png').convert_alpha()
ataque1 = pg.image.load('./Cat Game Assets/Tilesets/Cat1_Attack1.png').convert_alpha()
ataque2 = pg.image.load('./Cat Game Assets/Tilesets/Cat1_Attack2.png').convert_alpha()


sair = False

frame = 0
x_gato = 400
y_gato = 300

#dimensões dos frames para cada estado do gato
largura_frame_parado, altura_frame_parado = 50, 64
largura_frame_andando, altura_frame_andando = 64, 64
largura_frame_pulando, altura_frame_pulando = 80, 80
largura_frame_ult, altura_frame_ult = 80, 80
largura_frame_ataque1, altura_frame_ataque1 = 80, 64
largura_frame_ataque2, altura_frame_ataque2 = 80, 80

#flag para controlar a direção do gato
virado_esquerda = False

#variáveis de controle de pulo
pulando_agora = False
velocidade_y = 0
gravidade = 3
chao_y = 300

#flag para controlar o estado de ataque
atacando_agora = False

#controlar a velocidade de atualização do personagem
clock = pg.time.Clock()


while not sair:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sair = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sair = True
                frame = 0   
            #iniciar o ataque se a barra de espaço for pressionada
            if (event.key == pg.K_SPACE or event.key == pg.K_q or event.key == pg.K_e) and not atacando_agora:
                atacando_agora = True
                frame = 0

    tecla = pg.key.get_pressed()

    #iniciar o pulo se 'w' ou seta para cima for pressionada e o gato não estiver pulando
    if tecla[K_w] or tecla[K_UP] and not pulando_agora:
        pulando_agora = True
        velocidade_y = -12
        frame = 0
       
    #define o sprite atual para "parado" por padrão
    #depois atualiza para "andando" ou "pulando" conforme as teclas pressionadas
    sprite_atual = parado
    largura_frame_atual = largura_frame_parado
    altura_frame_atual = altura_frame_parado
    ajuste_y = 0

    #movimentação para a direita (quando a tecla de seta para a direita ou 'd' for pressionada)
    #atualizando o sprite para andando
    if tecla[K_RIGHT] or tecla[K_d]:
        x_gato += 5
        virado_esquerda = False
        sprite_atual = andando
        largura_frame_atual = largura_frame_andando
        altura_frame_atual = altura_frame_andando

    #movimentação para a esquerda (quando a tecla de seta para a esquerda ou 'a' for pressionada)
    #atualizando o sprite para andando
    if tecla[K_LEFT] or tecla[K_a]:
        x_gato -= 5
        virado_esquerda = True
        sprite_atual = andando
        largura_frame_atual = largura_frame_andando
        altura_frame_atual = altura_frame_andando

    #atualizando o sprite para estado "pulando" se o gato estiver pulando
    if pulando_agora:
        sprite_atual = pulando
        largura_frame_atual = largura_frame_pulando
        altura_frame_atual = altura_frame_pulando
        ajuste_y = -16

    #atualiza a posição vertical do gato durante o pulo e aplica a gravidade
    if pulando_agora:
        y_gato += velocidade_y
        velocidade_y += gravidade

        #impede que o gato caia abaixo do chão definido
        if y_gato >= chao_y:
            y_gato = chao_y
            pulando_agora = False
            velocidade_y = 0
            frame = 0
    
    #atualiza o sprite para estado "atacando" verifica qual o ataque
    if atacando_agora:
        if tecla[K_SPACE]:
            sprite_atual = ult
            largura_frame_atual = largura_frame_ult
            altura_frame_atual = altura_frame_ult
            ajuste_y = -16
        elif tecla[K_q]:
            sprite_atual = ataque1
            largura_frame_atual = largura_frame_ataque1
            altura_frame_atual = altura_frame_ataque1
        elif tecla[K_e]:
            sprite_atual = ataque2
            largura_frame_atual = largura_frame_ataque2
            altura_frame_atual = altura_frame_ataque2
            ajuste_y = -16

    #calcula o número total de frames no sprite atual para controlar a animação
    #(os estados do gato têm diferentes quantidades de frames,
    #então usamos a largura do sprite para calcular quantos frames ele tem)
    total_frames = sprite_atual.get_width() // largura_frame_atual
    
    #encerrar o estado de ataque quando a animação de ataque terminar
    if atacando_agora:
        if frame >= total_frames-1:
            atacando_agora = False
            frame = 0

    #reseta para 0 quando chega no último frame
    if frame >= total_frames:
        frame = 0

    #extrai o frame atual do sprite para exibição
    frame_gato = sprite_atual.subsurface(frame * largura_frame_atual, 0, largura_frame_atual, altura_frame_atual)

    #espelha o frame quando tiver virado pra esquerda
    if virado_esquerda:
        frame_gato = pg.transform.flip(frame_gato, True, False)

    #mostra o frame atual do gato na janela
    janela.fill((0, 0, 0))
    janela.blit(frame_gato, (x_gato, y_gato + ajuste_y))
    pg.display.flip()

    frame += 1
    
    #fica no último frame do sprite de pulo enquanto estiver pulando
    #e reseta para o primeiro frame do sprite de andando/parado quando não estiver mais pulando
    if pulando_agora:
        if frame >= total_frames:
            frame  = total_frames - 1
    else:
        if frame >= total_frames:
            frame = 0

    clock.tick(15)

pg.quit()