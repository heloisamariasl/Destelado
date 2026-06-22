"""
Coletáveis do jogo Destelado são:
1) O peixinho que ajuda o personagem do gatinho a sobreviver, ganhando uma vida;
2) A bota, que aumenta a velocidade do personagem por 10 segundos;
3) Catnip, a erva dos gatos, com ela o personagem dorme no jogo durante 5 segundos;
4) Com o brinquero de lã, o gatinho ficará enroscado por 5 segundos, assim, ficand mais lento;

Além do inventário e da barra de vida;
"""

import pygame as pg

class Coletaveis:
    def __init__(self, acao, valor, tempo):
        self.acao = acao
        self.valor = valor
        self.tempo = tempo
        self.imagem = pg.transform.scale(pg.image.load("assets/coletaveis/peixe_azul.png").convert_alpha(),(60,60))
        self.rect = self.imagem.get_rect(topleft=(600, 300))
        
    def peixe(self, gato):
        gato.vida_gato += 1
        if gato.vida_gato > gato.vida_gato_max:
            gato.vida_gato = gato.vida_gato_max

    def __init__(self, acao, valor, tempo):
        self.acao = acao
        self.valor = valor
        self.tempo = tempo

        self.imagem = pg.transform.scale(
            pg.image.load("assets/coletaveis/novelo.png").convert_alpha(),
            (60, 60)
        )

        self.rect = self.imagem.get_rect(topleft=(600, 300))

    def novelo(self, gato):
        # reduz a velocidade do gato
        gato.velocidade_original = gato.velocidade
        gato.velocidade *= 0.5  # reduz para 50%

        # ativa o efeito
        gato.enrolado = True

        # salva o instante em que o efeito começou
        gato.tempo_enrolado = pg.time.get_ticks()

        # duração do efeito em milissegundos
        gato.duracao_enrolado = self.tempo * 1000


class Bota:
    def __init__(self):
        self.tempo = 10  # duração do efeito em segundos

        self.imagem = pg.transform.scale(
            pg.image.load("assets/coletaveis/bota.png").convert_alpha(),
            (60, 60)
        )

        self.rect = self.imagem.get_rect(topleft=(600, 300))

    def aplicar_efeito(self, gato):
        # guarda a velocidade original
        gato.velocidade_original = gato.velocidade

        # aumenta a velocidade em 50%
        gato.velocidade *= 1.5

        # ativa o efeito
        gato.bota_ativa = True

        # registra o momento da coleta
        gato.tempo_bota = pg.time.get_ticks()

        # converte segundos para milissegundos
        gato.duracao_bota = self.tempo * 1000