import pygame as pg

class Botao:
    def __init__(self, texto, x, y, largura, altura):
        self.texto = texto
        self.rect = pg.Rect(x, y, largura, altura)

        self.cor_normal = (255, 255, 255)
        self.cor_hover = (255, 215, 0)

        self.fonte = pg.font.SysFont("arial", 40, bold=True)

    def desenhar(self, tela):
        mouse = pg.mouse.get_pos()
        cor = self.cor_normal

        if self.rect.collidepoint(mouse):
            cor = self.cor_hover

        texto = self.fonte.render(self.texto, True, cor)
        texto_rect = texto.get_rect(center=self.rect.center)

        tela.blit(texto, texto_rect)

    def clicou(self, evento):
        if evento.type == pg.MOUSEBUTTONDOWN:
            if evento.button == 1:
                return self.rect.collidepoint(evento.pos)
        return False


class MenuPrincipal:
    def __init__(self, tela):
        self.tela = tela
        self.largura = tela.get_width()
        self.altura = tela.get_height()

        self.fonte_titulo = pg.font.SysFont("arial", 80, bold=True)

        self.botao_jogar = Botao(
            "JOGAR",
            self.largura // 2 - 150,
            260,
            300,
            60
        )

        self.botao_opcoes = Botao(
            "OPÇÕES",
            self.largura // 2 - 150,
            350,
            300,
            60
        )

        self.botao_sair = Botao(
            "SAIR",
            self.largura // 2 - 150,
            440,
            300,
            60
        )

    def desenhar(self):
        self.tela.fill((30, 30, 30))

        titulo = self.fonte_titulo.render(
            "DESTELADO",
            True,
            (255, 255, 255)
        )

        titulo_rect = titulo.get_rect(center=(self.largura // 2, 120))
        self.tela.blit(titulo, titulo_rect)

        self.botao_jogar.desenhar(self.tela)
        self.botao_opcoes.desenhar(self.tela)
        self.botao_sair.desenhar(self.tela)

    def tratar_eventos(self, evento):
        if self.botao_jogar.clicou(evento):
            return "jogar"
        if self.botao_opcoes.clicou(evento):
            return "opcoes"
        if self.botao_sair.clicou(evento):
            return "sair"

        return None