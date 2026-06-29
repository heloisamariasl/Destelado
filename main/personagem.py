import pygame as pg
from pygame.locals import *
 
class Personagem:
    def __init__(self):
        self.parado = pg.image.load('assets/Cat/Tilesets/Cat1_Standing.png').convert_alpha()
        self.andando = pg.image.load('assets/Cat/Tilesets/Cat1_Walking.png').convert_alpha()
        self.pulando = pg.image.load('assets/Cat/Tilesets/Cat1_Jumping.png').convert_alpha()
        self.ult = pg.image.load('assets/Cat/Tilesets/Cat1_Attack3.png').convert_alpha()
        self.ataque1 = pg.image.load('assets/Cat/Tilesets/Cat1_Attack1.png').convert_alpha()
        self.ataque2 = pg.image.load('assets/Cat/Tilesets/Cat1_Attack2.png').convert_alpha()
        self.dano_gato = pg.image.load('assets/Cat/Tilesets/Cat1_Hurt.png').convert_alpha()
        self.gato_morrendo = pg.image.load('assets/Cat/Tilesets/Cat1_Death.png').convert_alpha()
        self.gato_correndo = pg.image.load('assets/Cat/Tilesets/Cat1_Running.png').convert_alpha()
        self.coracao_cheio = pg.image.load('assets/vida/coracao_cheio.png').convert_alpha()
        self.coracao_vazio = pg.image.load('assets/vida/coracao_vazio.png').convert_alpha()
    

        self.frame = 0
        self.x_gato = 100
        self.y_gato = 460
 
        self.velocidade = 5
 
        self.vida_gato = 7
        self.vida_gato_max = 7
 
        self.gato_vivo = True
 
        self.velocidade_morte = 0
        self.tempo_morte = 0
        self.contador_ani_pulo = 0
 
        self.virado_esquerda = False
        self.andando_flag = False
 
        self.correndo_flag = False
        self.tempo_bota = 0
        self.duracao_bota = 0
 
        self.tomando_dano = False
        self.invulneravel = False
        self.tempo_invulneravel = 0

        self.dormindo = False
        self.tempo_dormindo = 0
        self.duracao_dormindo = 0


        self.pulando_agora = False
        self.no_chao = True
        self.velocidade_y = 0
        self.gravidade = 2
        self.chao_y = 460
 
        self.atacando_agora = False
        self.tipo_ataque = ''
 
        self.largura_frame_parado = 50
        self.altura_frame_parado = 64
 
        self.largura_frame_andando = 64
        self.altura_frame_andando = 64
 
        self.largura_frame_pulando = 80
        self.altura_frame_pulando = 80
 
        self.largura_frame_ult = 80
        self.altura_frame_ult = 80
 
        self.largura_frame_ataque1 = 80
        self.altura_frame_ataque1 = 64
 
        self.largura_frame_ataque2 = 80
        self.altura_frame_ataque2 = 80
 
        self.largura_frame_dano = 64
        self.altura_frame_dano = 64
 
        self.largura_frame_morte = 80
        self.altura_frame_morte = 80
 
        self.largura_frame_correndo = 48
        self.altura_frame_correndo = 64
 
        self.largura_frame_atual = 50
        self.altura_frame_atual = 64
 
        self.enrolado = False
        self.tempo_enrolado = 0
        self.duracao_enrolado = 0
 
        self.rect = pg.Rect(self.x_gato, self.y_gato, 50, 64)
 
    def eventos(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and not self.atacando_agora:
                self.atacando_agora = True
                self.tipo_ataque = 'ult'
                self.frame = 0
            elif event.key == pg.K_q and not self.atacando_agora:
                self.atacando_agora = True
                self.tipo_ataque = 'ataque1'
                self.frame = 0
            elif event.key == pg.K_e and not self.atacando_agora:
                self.atacando_agora = True
                self.tipo_ataque = 'ataque2'
                self.frame = 0
 
    def atualizar(self):

        if not self.gato_vivo:
            return

        if self.dormindo:
            tempo_atual = pg.time.get_ticks()

            if tempo_atual - self.tempo_dormindo >= self.duracao_dormindo:
                self.dormindo = False
            else:
                self.andando_flag = False
                self.atacando_agora = False

                self.velocidade_y += self.gravidade
                self.y_gato += self.velocidade_y

                if self.y_gato >= self.chao_y:
                    self.y_gato = self.chao_y
                    self.velocidade_y = 0
                    self.no_chao = True
                    self.pulando_agora = False

                self.rect = pg.Rect(self.x_gato, self.y_gato, 50, 64)
                return

        tecla = pg.key.get_pressed()

        self.andando_flag = False
        self.velocidade_atual = self.velocidade

 
        if self.correndo_flag:
            self.velocidade_atual = self.velocidade * 1.5
        elif self.enrolado:
            self.velocidade_atual = self.velocidade * 0.5
 
        if (tecla[K_w] or tecla[K_UP]) and self.no_chao:
            self.pulando_agora = True
            self.no_chao = False
            self.velocidade_y = -17
            self.frame = 0
            self.contador_ani_pulo = 0
 
        if tecla[K_RIGHT] or tecla[K_d]:
            self.x_gato += self.velocidade_atual
            self.virado_esquerda = False
            self.andando_flag = True
 
        if tecla[K_LEFT] or tecla[K_a]:
            self.x_gato -= self.velocidade_atual
            self.virado_esquerda = True
            self.andando_flag = True
 
        self.velocidade_y += self.gravidade
        self.y_gato += self.velocidade_y           
 
        if self.y_gato >= self.chao_y:
            self.y_gato = self.chao_y
            self.velocidade_y = 0
            self.pulando_agora = False
            self.no_chao = True
 
        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False
 
        self.rect = pg.Rect(self.x_gato, self.y_gato, 50, 64)

 
    # camera_x é novo parâmetro — desloca o desenho na tela
    def desenhar(self, janela, camera_x=0):
        x_tela = self.x_gato - camera_x   # posição visual na tela
 
        self.sprite_atual = self.parado
        self.largura_frame_atual = self.largura_frame_parado
        self.altura_frame_atual = self.altura_frame_parado
        self.ajuste_y = 0
 
        if not self.gato_vivo:
            self.sprite_atual = self.gato_morrendo
            self.largura_frame_atual = self.largura_frame_morte
            self.altura_frame_atual = self.altura_frame_morte
 
        elif self.tomando_dano:
            self.sprite_atual = self.dano_gato
            self.largura_frame_atual = self.largura_frame_dano
            self.altura_frame_atual = self.altura_frame_dano
 
        elif self.pulando_agora or not self.no_chao:
            self.sprite_atual = self.pulando
            self.largura_frame_atual = self.largura_frame_pulando
            self.altura_frame_atual = self.altura_frame_pulando
            self.ajuste_y = -16
            self.contador_ani_pulo += 1
            if self.contador_ani_pulo % 2 == 0:
                self.frame -= 1
 
        elif self.atacando_agora:
            if self.tipo_ataque == 'ult':
                self.sprite_atual = self.ult
                self.largura_frame_atual = self.largura_frame_ult
                self.altura_frame_atual = self.altura_frame_ult
                self.ajuste_y = -16
            elif self.tipo_ataque == 'ataque1':
                self.sprite_atual = self.ataque1
                self.largura_frame_atual = self.largura_frame_ataque1
                self.altura_frame_atual = self.altura_frame_ataque1
            elif self.tipo_ataque == 'ataque2':
                self.sprite_atual = self.ataque2
                self.largura_frame_atual = self.largura_frame_ataque2
                self.altura_frame_atual = self.altura_frame_ataque2
                self.ajuste_y = -16
 
        elif self.correndo_flag and self.andando_flag:
            self.sprite_atual = self.gato_correndo
            self.largura_frame_atual = self.largura_frame_correndo
            self.altura_frame_atual = self.altura_frame_correndo
 
        elif self.andando_flag:
            self.sprite_atual = self.andando
            self.largura_frame_atual = self.largura_frame_andando
            self.altura_frame_atual = self.altura_frame_andando
 
        self.total_frames = self.sprite_atual.get_width() // self.largura_frame_atual
 
        if not self.gato_vivo:
            self.velocidade_morte += 1
            if self.velocidade_morte >= 3:
                if self.frame < self.total_frames - 1:
                    self.frame += 1
                self.velocidade_morte = 0
            self.frame_gato = self.sprite_atual.subsurface(
                self.frame * self.largura_frame_atual, 0,
                self.largura_frame_atual, self.altura_frame_atual
            )
            janela.blit(self.frame_gato, (x_tela, self.y_gato - 15))
            return
 
        if self.atacando_agora and self.frame >= self.total_frames - 1:
            self.atacando_agora = False
            self.frame = 0
 
        if self.tomando_dano and self.frame >= self.total_frames - 1:
            self.tomando_dano = False
            self.frame = 0
 
        if self.frame >= self.total_frames:
            self.frame = 0
 
        self.frame_gato = self.sprite_atual.subsurface(
            self.frame * self.largura_frame_atual, 0,
            self.largura_frame_atual, self.altura_frame_atual
        )
 
        if self.virado_esquerda:
            self.frame_gato = pg.transform.flip(self.frame_gato, True, False)
 
        janela.blit(self.frame_gato, (x_tela, self.y_gato + self.ajuste_y))
 
        self.barra_vida(janela)  # HUD fica fixo na tela, sem camera_x
 
        if not self.gato_vivo:
            if self.frame < self.total_frames - 1:
                self.frame += 1
            else:
                self.frame = self.total_frames - 1
        else:
            self.frame += 1
 
    def tomar_dano(self):
        if not self.gato_vivo:
            return
        self.vida_gato -= 1
        if self.vida_gato <= 0:
            self.gato_vivo = False
            self.tomando_dano = False
            self.atacando_agora = False
            self.pulando_agora = False
            self.tempo_morte = pg.time.get_ticks()
            self.frame = 0
            return
        self.tomando_dano = True
        self.invulneravel = True
        self.tempo_invulneravel = 60
        self.frame = 0
 
    def barra_vida(self, janela):
        tamanho_coracao = 46
        x = 20
        y = 20
        for i in range(self.vida_gato_max):
            coracao_x = x + i * tamanho_coracao
            imagem = self.coracao_cheio if i < self.vida_gato else self.coracao_vazio
            imagem_redimensionada = pg.transform.scale(imagem, (tamanho_coracao, tamanho_coracao))
            janela.blit(imagem_redimensionada, (coracao_x, y))