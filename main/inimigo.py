import pygame as pg
from pygame.locals import *

class Cachorro:
    def __init__(self, x, y, ponto_inicial, ponto_final):
        #sprite sheet da animação andando
        self.cao_andando = pg.image.load('assets/Dog/Dog_Walking.png').convert_alpha()
        self.cao_latindo = pg.image.load('assets/Dog/Dog_Barking.png').convert_alpha()
        self.cao_correndo = pg.image.load('assets/Dog/Dog_Running.png').convert_alpha()
        
        self.frame = 0
        self.cao_vivo = True
        
        self.estado_cao = 'patrulhando'
        
        self.x_retorno = x
        
        self.tempo_latindo = 0
        
        self.tempo_correndo = 0
        
        self.olhando_gato = False
        
        self.direcao_ataque = 1
    
        
        #define qual lado o sprite começa (nesse caso, esqueda)
        self.virado_direita = True
        self.velocidade = 3
        
        #posição inicial do cao (vai ser definido na main)
        self.x_inimigo = x
        self.y_inimigo = y
        
        self.ponto_inicial = ponto_inicial
        self.ponto_final = ponto_final

        #tamanho de cada sprite
        self.largura_frame_cao_andando = 90 
        self.altura_frame_cao_andando = 48
        
        self.largura_frame_cao_latindo = 88 
        self.altura_frame_cao_latindo = 48
        
        self.largura_frame_cao_correndo = 86 
        self.altura_frame_cao_correndo = 51
        
        self.total_frames = self.cao_andando.get_width() // self.largura_frame_cao_andando
        
    def atualizar(self, gato):
        
        if not self.cao_vivo:
            return
        
        self.centro_gato = gato.x_gato + gato.rect.width // 2
        self.centro_cao = self.x_inimigo + self.largura_frame_cao_andando // 2
        
        self.distancia_x = abs(self.centro_gato - self.centro_cao)
                
        if self.distancia_x <= 150 and (self.estado_cao == 'patrulhando' or self.estado_cao == 'retornando') and gato.gato_vivo:
            if gato.x_gato > self.x_inimigo:
                self.virado_direita = True
            else:
                self.virado_direita = False
            self.estado_cao = 'latindo'
            self.tempo_latindo = 15
            self.frame = 0
        elif self.distancia_x > 150 and self.estado_cao == 'latindo' and gato.gato_vivo:
            self.estado_cao = 'patrulhando'
            self.frame = 0
        
        if self.estado_cao == 'latindo':
            self.tempo_latindo -=1
            if self.tempo_latindo <= 0:
                if gato.x_gato > self.x_inimigo:
                    self.direcao_ataque = 1
                    self.virado_direita = True
                else:
                    self.direcao_ataque = -1
                    self.virado_direita = False
                self.estado_cao = 'correndo'
                self.tempo_correndo = 30
                self.frame = 0
        
        if self.estado_cao == 'correndo':
            self.tempo_correndo -= 1            
            self.x_inimigo +=6 * self.direcao_ataque
            
            if self.virado_direita and gato.x_gato > self.x_inimigo:
                self.olhando_gato = True
            elif not self.virado_direita and gato.x_gato < self.x_inimigo:
                self.olhando_gato = True
            else:
                self.olhando_gato = False
            
            if self.distancia_x <= 20 and self.olhando_gato and not gato.pulando_agora:
                if not gato.invulneravel:
                    gato.tomar_dano()
                self.estado_cao = 'retornando'
                self.frame = 0
            elif self.tempo_correndo <= 0:
                self.estado_cao = 'retornando'
                self.frame = 0
        
        if self.estado_cao == 'retornando':
            if self.x_inimigo < self.x_retorno:
                self.x_inimigo += 3
                self.virado_direita = True
            elif self.x_inimigo > self.x_retorno:
                self.x_inimigo -= 3
                self.virado_direita = False
            if abs(self.x_inimigo - self.x_retorno) < 5:
                self.x_inimigo = self.x_retorno
                self.estado_cao = 'patrulhando'
        
        if self.estado_cao == 'patrulhando':
            self.x_inimigo += self.velocidade
        
            if self.velocidade > 0:
                self.virado_direita = True
            else:
                self.virado_direita = False
        
            if self.x_inimigo >= self.ponto_final:
                self.velocidade *= -1
        
            if self.x_inimigo <= self.ponto_inicial:
                self.velocidade *= -1
        
        self.rect = pg.Rect(self.x_inimigo, self.y_inimigo, self.largura_frame_cao_andando, self.altura_frame_cao_andando)
    
    def desenhar_cao(self,janela):
        if not self.cao_vivo:
            return
    
        if self.estado_cao == 'latindo':
            self.largura_frame_atual = self.largura_frame_cao_latindo
            self.altura_frame_atual = self.altura_frame_cao_latindo
            self.sprite_atual = self.cao_latindo
        
        elif self.estado_cao == 'correndo':
            self.largura_frame_atual = self.largura_frame_cao_correndo
            self.altura_frame_atual = self.altura_frame_cao_correndo
            self.sprite_atual = self.cao_correndo
        
        else:
            self.largura_frame_atual = self.largura_frame_cao_andando
            self.altura_frame_atual = self.altura_frame_cao_andando
            self.sprite_atual = self.cao_andando
        
        self.total_frames = self.sprite_atual.get_width() // self.largura_frame_atual
        
        self.frame_cao = self.sprite_atual.subsurface(self.frame*self.largura_frame_atual, 0, self.largura_frame_atual, self.altura_frame_atual)
        
        if self.virado_direita:
            self.frame_cao = pg.transform.flip(self.frame_cao, True, False)
            
        janela.blit(self.frame_cao, (self.x_inimigo, self.y_inimigo))        
        
        self.frame +=1
    
        if self.frame >= self.total_frames:
            self.frame = 0
    