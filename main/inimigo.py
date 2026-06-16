import pygame as pg
from pygame.locals import *

class Cachorro:
    def __init__(self, x, y, ponto_inicial, ponto_final):
        #sprite sheet da animação andando
        self.cao_andando = pg.image.load('assets/Dog/dog_3_walk_sheet.png').convert_alpha()
        
        self.frame = 0
        
        #define qual lado o sprite começa (nesse caso, esqueda)
        self.virado_esquerda = True
        self.velocidade = 2
        
        #posição inicial do cao (vai ser definido na main)
        self.x_inimigo = x
        self.y_inimigo = y
        
        self.ponto_inicial = ponto_inicial
        self.ponto_final = ponto_final

        #tamanho de cada sprite
        self.largura_frame_cao_andando = 94 
        self.altura_frame_cao_andando = 62
        
        self.total_frames = self.cao_andando.get_width() // self.largura_frame_cao_andando
        
    def atualizar(self):
        self.x_inimigo += self.velocidade
        
        if self.velocidade > 0:
            self.virado_esquerda = False
        else:
            self.virado_esquerda = True
        
        if self.x_inimigo >= self.ponto_final:
            self.velocidade *= -1
        
        if self.x_inimigo <= self.ponto_inicial:
            self.velocidade *= -1
    
    def desenhar_cao(self,janela):
        self.frame_cao = self.cao_andando.subsurface(self.frame*self.largura_frame_cao_andando, 0, self.largura_frame_cao_andando, self.altura_frame_cao_andando)
        
        if self.virado_esquerda:
            self.frame_cao = pg.transform.flip(self.frame_cao, True, False)
            
        janela.blit(self.frame_cao, (self.x_inimigo, self.y_inimigo))        
        
        self.frame +=1
    
        if self.frame >= self.total_frames:
            self.frame = 0
    