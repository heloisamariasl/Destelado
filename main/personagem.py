import pygame as pg
from pygame.locals import *

class Personagem:
    def __init__(self):
        #sprites para cada estado do personagem
        self.parado = pg.image.load('assets/Cat/Tilesets/Cat1_Standing.png').convert_alpha()
        self.andando = pg.image.load('assets/Cat/Tilesets/Cat1_Walking.png').convert_alpha()
        self.pulando = pg.image.load('assets/Cat/Tilesets/Cat1_Jumping.png').convert_alpha()
        self.ult = pg.image.load('assets/Cat/Tilesets/Cat1_Attack3.png').convert_alpha()
        self.ataque1 = pg.image.load('assets/Cat/Tilesets/Cat1_Attack1.png').convert_alpha()
        self.ataque2 = pg.image.load('assets/Cat/Tilesets/Cat1_Attack2.png').convert_alpha()
        self.dano_gato = pg.image.load('assets/Cat/Tilesets/Cat1_Hurt.png').convert_alpha()
        self.coracao_cheio = pg.image.load('assets/vida/coracao_cheio.png').convert_alpha()
        self.coracao_vazio = pg.image.load('assets/vida/coracao_vazio.png').convert_alpha()

        self.frame = 0
        self.x_gato = 100
        self.y_gato = 300
        
        self.vida_gato = 7
        self.vida_gato_max = 7

        #flag para controlar a direção do gato
        self.virado_esquerda = False
        
        #flag para ver se está andando
        self.andando_flag = False
        
        #variaveis para dano
        self.tomando_dano = False
        self.invulneravel = False
        self.tempo_invulneravel = 0
                
        #variaveis para controlar o pulo
        self.pulando_agora = False
        self.velocidade_y = 0
        self.gravidade = 3
        self.chao_y = 300
        
        #flag para ver se está atacando
        self.atacando_agora = False
        self.tipo_ataque = ''
        
        #dimensões dos frames para cada estado do gato
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
        
    
    def eventos(self,event):
        #verifica se a tecla para ataque foi acionada    
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
        tecla = pg.key.get_pressed()
        
        self.andando_flag = False
        
        #iniciar o pulo se 'w' ou seta para cima for pressionada e o gato não estiver pulando
        if (tecla[K_w] or tecla[K_UP]) and not self.pulando_agora:
            self.pulando_agora = True
            self.velocidade_y = -15
            self.frame = 0
        
        #movimentação para a direita quando a tecla de seta para a direita ou 'd' for pressionada
        if tecla[K_RIGHT] or tecla[K_d]:
            self.x_gato += 5
            self.virado_esquerda = False
            self.andando_flag = True
        
        #movimentação para a esquerda quando a tecla de seta para a esquerda ou 'a' for pressionada
        if tecla[K_LEFT] or tecla[K_a]:
            self.x_gato -= 5
            self.virado_esquerda = True
            self.andando_flag = True
                    
        #atualiza a posição vertical do gato durante o pulo e aplica a gravidade
        if self.pulando_agora:
            self.y_gato += self.velocidade_y
            self.velocidade_y += self.gravidade

        #impede que o gato caia abaixo do chão definido
        if self.y_gato >= self.chao_y:
            self.y_gato = self.chao_y
            self.pulando_agora = False
            self.velocidade_y = 0
        
        if self.invulneravel:
            self.tempo_invulneravel -=1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False
        
        self.rect = pg.Rect(self.x_gato, self.y_gato, 50, 64)
        
    #função para ver qual o estado do personagem e qual frame imprimir
    def desenhar(self,janela):
        #define o sprite atual para "parado" por padrão
        #depois atualiza para "andando" ou "pulando" conforme as teclas pressionadas
        self.sprite_atual = self.parado
        self.largura_frame_atual = self.largura_frame_parado
        self.altura_frame_atual = self.altura_frame_parado
        self.ajuste_y = 0

        #atualiza o sprite para o dano
        if self.tomando_dano:
            self.sprite_atual = self.dano_gato
            self.largura_frame_atual = self.largura_frame_dano
            self.altura_frame_atual = self.altura_frame_dano
            
        #atualizando o sprite para estado "pulando" se o gato estiver pulando       
        elif self.pulando_agora:
            self.sprite_atual = self.pulando
            self.largura_frame_atual = self.largura_frame_pulando
            self.altura_frame_atual = self.altura_frame_pulando
            self.ajuste_y = -16
        
        #atualiza o sprite para estado "atacando" verifica qual o ataque
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
        
        #atualiza o sprite para estado de andando    
        elif self.andando_flag:
            self.sprite_atual = self.andando
            self.largura_frame_atual = self.largura_frame_andando
            self.altura_frame_atual = self.altura_frame_andando
        
        #calcula o número total de frames no sprite atual para controlar a animação
        #(os estados do gato têm diferentes quantidades de frames,
        #então usamos a largura do sprite para calcular quantos frames ele tem)
        self.total_frames = self.sprite_atual.get_width() // self.largura_frame_atual
        
        #encerrar o estado de ataque quando a animação de ataque terminar
        if self.atacando_agora:
            if self.frame >= self.total_frames-1:
                self.atacando_agora = False
                self.frame = 0

        if self.tomando_dano:
            if self.frame >= self.total_frames-1:
                self.tomando_dano = False
                self.frame = 0
        
        #reseta para 0 quando chega no último frame
        if self.frame >= self.total_frames:
            self.frame = 0

        #extrai o frame atual do sprite para exibição
        self.frame_gato = self.sprite_atual.subsurface(self.frame * self.largura_frame_atual, 0, self.largura_frame_atual, self.altura_frame_atual)
    
        #espelha o frame quando tiver virado pra esquerda
        if self.virado_esquerda:
            self.frame_gato = pg.transform.flip(self.frame_gato, True, False)
        
        self.rect = pg.Rect(self.x_gato, self.y_gato, self.largura_frame_atual, self.altura_frame_atual)

        #mostra o frame atual do gato na janela
        janela.blit(self.frame_gato, (self.x_gato, self.y_gato + self.ajuste_y))
        #pg.display.flip()

        self.barra_vida(janela) #Mostra a barra de vida

        self.frame += 1
    
    #função de dano do gato
    def tomar_dano(self):
        self.vida_gato -=1
        self.tomando_dano = True
        self.invulneravel = True
        self.tempo_invulneravel = 60
        self.frame = 0

     # Função para visualização das vidas do gato   
    def barra_vida(self,janela):
        tamanho_coracao = 46
        espaco_entre_coracao = 0
        x = 20 #Distância da borda esquerda
        y = 20 #Distância do topo

        vidas_atuais = self.vida_gato / self.vida_gato_max
        for i in range(self.vida_gato_max):
            coracao = x + i * (tamanho_coracao + espaco_entre_coracao)
            if i < self.vida_gato:
                imagem = self.coracao_cheio
            else:
                imagem = self.coracao_vazio
            imagem_redimensionada = pg.transform.scale(imagem, (tamanho_coracao, tamanho_coracao))
            janela.blit(imagem_redimensionada, (coracao, y)) # A imagem está sendo posta na tela do jogo

        