import pygame

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Destelado")

# Carrega o cenário
cenario = pygame.image.load("Destelado/assets/cenário/background.png")

# Ajusta o cenário para caber na tela
cenario = pygame.transform.scale(cenario, (LARGURA, ALTURA))

# Loop principal
rodando = True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Desenha o cenário
    tela.blit(cenario, (0, 0))

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()