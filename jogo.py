# # ===== Inicialização =====
# # ----- Importa e inicia pacotes
import pygame

pygame.init()

LARGURA = 800
ALTURA = 600
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Hello World!')
imagem = pygame.image.load("New Piskel.png")
imagem = pygame.transform.scale(imagem, (40, 40))

raio = 20
diametro = raio * 2
x = LARGURA // 2
y = ALTURA // 2
# ----- Inicia estruturas de dados
tamanho = 40

game = True
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y -= tamanho
            if event.key == pygame.K_s:
                y += tamanho
            if event.key == pygame.K_a:
                x -= tamanho
            if event.key == pygame.K_d:
                x += tamanho

    x = max(0, min(LARGURA - tamanho, x))
    y = max(0, min(ALTURA - tamanho, y))

    # ----- Gera saídas
    window.fill((0,0,0))
    window.blit(imagem, (x, y))
    pygame.display.update()