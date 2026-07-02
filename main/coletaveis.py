"""
Coletáveis do jogo Destelado são:
1) O peixinho que ajuda o personagem do gatinho a sobreviver, ganhando uma vida;
2) A bota, que aumenta a velocidade do personagem por 10 segundos;
3) Catnip, a erva dos gatos, com ela o personagem dorme no jogo durante 5 segundos;
4) Com o brinquero de lã, o gatinho ficará enroscado por 5 segundos, assim, ficando mais lento;
"""

import pygame as pg
import random

def posicao_aleatoria():
    x = random.randint(50, 750)
    y = 460
    return(x,y)

class Coletaveis:
    def __init__(self, caminho_imagem, posicao, valor= 0, tempo = 0):
        self.valor = valor
        self.tempo = tempo
        self.imagem = pg.transform.scale(pg.image.load(caminho_imagem).convert_alpha(), (50, 50))
        self.rect = self.imagem.get_rect(topleft=posicao)

    def acao(self,gato):#Cada classe que representa um coletável decide qual a sua ação e efeito para o personagem
        pass

class Peixe(Coletaveis):
    def __init__(self, posicao = None):
        if posicao is None:
            posicao = posicao_aleatoria()
        super().__init__("assets/coletaveis/peixe.png", posicao)

    def acao(self, gato):
        gato.vida_gato += 1
        if gato.vida_gato > gato.vida_gato_max:
            gato.vida_gato = gato.vida_gato_max

class Novelo(Coletaveis):
    def __init__(self, posicao = None, tempo=5):
        if posicao is None:
            posicao = posicao_aleatoria()
        super().__init__("assets/coletaveis/novelo.png", posicao, tempo=tempo)
        
        self.imagem = pg.transform.scale(self.imagem, (30,30))
        self.rect = self.imagem.get_rect(topleft=posicao)
        self.rect.y += 20

    def acao(self, gato):
        # ativa o efeito
        gato.enrolado = True

        # salva o instante em que o efeito começou
        gato.tempo_enrolado = pg.time.get_ticks()

        # duração do efeito em milissegundos
        gato.duracao_enrolado = self.tempo * 1000


class Bota(Coletaveis):
    def __init__(self, posicao=None, tempo=3):
        if posicao is None:
            posicao = posicao_aleatoria()

        self.tempo = 10

        self.imagem = pg.transform.scale(
            pg.image.load("assets/coletaveis/bota.png").convert_alpha(),
            (60, 60)
        )

        self.rect = self.imagem.get_rect(topleft=posicao)

    def acao(self, gato):
        gato.correndo_flag = True
        gato.bota_ativa = True
        gato.tempo_bota = pg.time.get_ticks()
        gato.duracao_bota = self.tempo * 1000


class Catnip(Coletaveis):
    def __init__(self, posicao=None, tempo=5):
        if posicao is None:
            posicao = posicao_aleatoria()

        super().__init__(
            "assets/coletaveis/catnip.png",
            posicao,
            tempo=tempo
        )

    def acao(self, gato):
        gato.dormindo = True
        gato.frame = 0
        gato.tempo_dormindo = pg.time.get_ticks()
        gato.duracao_dormindo = self.tempo * 1000