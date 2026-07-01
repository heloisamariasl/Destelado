import pygame as pg

class Botao:
    def __init__(self, texto, x, y, largura, altura):
        self.texto = texto
        self.rect = pg.Rect(x, y, largura, altura)

        self.cor_normal = (255, 255, 255)
        self.cor_hover = (170, 210, 255)

        self.fonte = pg.font.SysFont("arial", 40, bold=True)

    def desenhar(self, tela):
        mouse = pg.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)

        # fundo do botão
        cor = (35, 60, 120) if hover else (25, 45, 90)

        pg.draw.rect(tela, cor, self.rect, border_radius=8)
        pg.draw.rect(tela, (110, 180, 255), self.rect, 3, border_radius=8)

        texto = self.fonte.render(
            self.texto,
            True,
            self.cor_hover if hover else self.cor_normal
        )

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

        # logo
        self.logo = pg.image.load(
            "assets/menu/logo_destelado.png"
        ).convert_alpha()

        largura_logo = 400
        altura_logo = int(
            self.logo.get_height() *
            (largura_logo / self.logo.get_width())
        )

        self.logo = pg.transform.smoothscale(
            self.logo,
            (largura_logo, altura_logo)
        )

        # estado da tela
        self.tela_atual = "principal"

        # volumes
        self.volume_musica = 0.5
        self.volume_efeitos = 0.5

        # botões menu principal
        self.botao_jogar = Botao(
            "JOGAR",
            self.largura // 2 - 150,
            220,
            300,
            60
        )

        self.botao_opcoes = Botao(
            "OPÇÕES",
            self.largura // 2 - 150,
            310,
            300,
            60
        )

        self.botao_sair = Botao(
            "SAIR",
            self.largura // 2 - 150,
            400,
            300,
            60
        )

        # botão voltar opções
        self.botao_voltar = Botao(
            "VOLTAR",
            self.largura // 2 - 150,
            500,
            300,
            60
        )

        # botões game over
        self.botao_reiniciar = Botao(
            "REINICIAR",
            self.largura // 2 - 150,
            280,
            300,
            60
        )

        # botões vitória
        self.botao_jogar_novamente = Botao(
            "JOGAR NOVAMENTE",
            self.largura // 2 - 150,
            280,
            300,
            60
        )

        self.botao_menu_vitoria = Botao(
            "MENU PRINCIPAL",
            self.largura // 2 - 150,
            370,
            300,
            60
        )

        self.botao_menu = Botao(
            "MENU PRINCIPAL",
            self.largura // 2 - 150,
            370,
            300,
            60
        )

        self.fonte = pg.font.SysFont("arial", 34, bold=True)

    # ------------------------------------------------

    def desenhar(self):
        self.tela.fill((20, 25, 40))

        if self.tela_atual == "principal":
            self.desenhar_menu()

        elif self.tela_atual == "opcoes":
            self.desenhar_opcoes()

        elif self.tela_atual == "game_over":
            self.desenhar_game_over()

        elif self.tela_atual == "vitoria":
            self.desenhar_vitoria()

    # ------------------------------------------------

    def desenhar_menu(self):
        logo_rect = self.logo.get_rect(center=(self.largura // 2, 110))
        self.tela.blit(self.logo, logo_rect)

        self.botao_jogar.desenhar(self.tela)
        self.botao_opcoes.desenhar(self.tela)
        self.botao_sair.desenhar(self.tela)

    # ------------------------------------------------

    def desenhar_slider(self, y, valor):
        x = 300
        largura = 250

        pg.draw.rect(
            self.tela,
            (70, 70, 70),
            (x, y, largura, 8),
            border_radius=4
        )

        pg.draw.rect(
            self.tela,
            (90, 170, 255),
            (x, y, valor * largura, 8),
            border_radius=4
        )

        cursor_x = x + valor * largura

        pg.draw.circle(
            self.tela,
            (170, 220, 255),
            (int(cursor_x), y + 4),
            11
        )

    # ------------------------------------------------

    def desenhar_opcoes(self):
        titulo = self.fonte.render(
            "OPÇÕES",
            True,
            (255, 255, 255)
        )

        self.tela.blit(titulo, (305, 70))

        texto = self.fonte.render(
            "Música",
            True,
            (255, 255, 255)
        )

        self.tela.blit(texto, (110, 170))
        self.desenhar_slider(185, self.volume_musica)

        texto = self.fonte.render(
            "Efeitos",
            True,
            (255, 255, 255)
        )

        self.tela.blit(texto, (110, 290))
        self.desenhar_slider(305, self.volume_efeitos)

        self.botao_voltar.desenhar(self.tela)

    # ------------------------------------------------

    def desenhar_game_over(self):
        fonte_titulo = pg.font.SysFont("arial", 60, bold=True)

        titulo = fonte_titulo.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        titulo_rect = titulo.get_rect(center=(self.largura // 2, 120))
        self.tela.blit(titulo, titulo_rect)

        fonte = pg.font.SysFont("arial", 30)

        texto = fonte.render(
            "Você foi derrotado.",
            True,
            (255, 255, 255)
        )

        texto_rect = texto.get_rect(center=(self.largura // 2, 190))
        self.tela.blit(texto, texto_rect)

        self.botao_reiniciar.desenhar(self.tela)
        self.botao_menu.desenhar(self.tela)

    # ------------------------------------------------

    def desenhar_vitoria(self):

        fonte_titulo = pg.font.SysFont("arial", 60, bold=True)

        titulo = fonte_titulo.render(
            "VOCÊ VENCEU!",
            True,
            (255, 220, 0)
        )

        titulo_rect = titulo.get_rect(
            center=(self.largura // 2, 120)
        )

        self.tela.blit(titulo, titulo_rect)

        fonte = pg.font.SysFont("arial", 30)

        texto = fonte.render(
            "Parabéns por chegar ao final!",
            True,
            (255,255,255)
        )

        texto_rect = texto.get_rect(
            center=(self.largura // 2,190)
        )

        self.tela.blit(texto, texto_rect)

        self.botao_jogar_novamente.desenhar(self.tela)
        self.botao_menu_vitoria.desenhar(self.tela)

# ------------------------------------------------

    def tratar_eventos(self, evento):

        if self.tela_atual == "principal":

            if self.botao_jogar.clicou(evento):
                return "jogar"

            if self.botao_opcoes.clicou(evento):
                self.tela_atual = "opcoes"

            if self.botao_sair.clicou(evento):
                return "sair"

        elif self.tela_atual == "opcoes":

            if self.botao_voltar.clicou(evento):
                self.tela_atual = "principal"

            if evento.type == pg.MOUSEBUTTONDOWN:
                mx, my = evento.pos

                if 300 <= mx <= 550 and 175 <= my <= 200:
                    self.volume_musica = (mx - 300) / 250
                    pg.mixer.music.set_volume(self.volume_musica)

                if 300 <= mx <= 550 and 295 <= my <= 320:
                    self.volume_efeitos = (mx - 300) / 250

        elif self.tela_atual == "game_over":

            if self.botao_reiniciar.clicou(evento):
                return "reiniciar"

            if self.botao_menu.clicou(evento):
                self.tela_atual = "principal"
                return "menu"
            
        elif self.tela_atual == "vitoria":

            if self.botao_jogar_novamente.clicou(evento):
                return "reiniciar"

            if self.botao_menu_vitoria.clicou(evento):
                self.tela_atual = "principal"
                return "menu"

        return None