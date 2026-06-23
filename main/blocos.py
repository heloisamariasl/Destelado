import pygame as pg

class Bloco:
    def __init__(self, imagem, x, y, largura, altura):

        self.imagem = pg.image.load(imagem).convert_alpha()

        self.imagem = pg.transform.scale(
            self.imagem,
            (largura, altura)
        )

        self.rect = self.imagem.get_rect(
            topleft=(x, y)
        )

    def desenhar(self, janela):
        janela.blit(self.imagem, self.rect)