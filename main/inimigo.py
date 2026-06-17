import pygame as pg
from pygame.locals import *

class Cachorro:
    def __init__(self, x, y, ponto_inicial, ponto_final):
        #sprite sheet da animação andando
        self.cao_andando = pg.image.load('assets/Dog/Dog_Walking.png').convert_alpha()
        self.cao_latindo = pg.image.load('assets/Dog/Dog_Barking.png').convert_alpha()
        
        self.frame = 0
        self.cao_vivo = True
        
        self.estado_cao = 'patrulhando'
        
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
        
        self.total_frames = self.cao_andando.get_width() // self.largura_frame_cao_andando
        
    def atualizar(self, gato):
        
        if not self.cao_vivo:
            return
        
        self.distancia = abs(gato.x_gato - self.x_inimigo)
        
        if self.distancia <= 150 and self.estado_cao != 'latindo':
            self.estado_cao = 'latindo'
            print('au')
            self.frame = 0
        elif self.distancia > 150 and self.estado_cao != 'patrulhando':
            self.estado_cao = 'patrulhando'
            self.frame = 0
        
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
    