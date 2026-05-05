# # ===== Inicialização =====
# # ----- Importa e inicia pacotes
import pygame

pygame.init()

LARGURA = 800
ALTURA = 600
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Hello World!')
costas = pygame.image.load("costas.png")
frente = pygame.image.load("frente.png")
direita = pygame.image.load("direita.png")
esquerda = pygame.image.load("esquerda.png")

tamanho = 40
img_cima = pygame.transform.scale(frente, (tamanho, tamanho))
img_baixo = pygame.transform.scale(costas, (tamanho, tamanho))
img_esquerda = pygame.transform.scale(esquerda, (tamanho, tamanho))
img_direita = pygame.transform.scale(direita, (tamanho, tamanho))

imagem = img_baixo

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
                imagem = img_baixo
            if event.key == pygame.K_s:
                y += tamanho
                imagem = img_cima
            if event.key == pygame.K_a:
                x -= tamanho
                imagem = img_esquerda
            if event.key == pygame.K_d:
                x += tamanho
                imagem = img_direita

    x = max(0, min(LARGURA - tamanho, x))
    y = max(0, min(ALTURA - tamanho, y))

    # ----- Gera saídas
    window.fill((0,0,0))
    window.blit(imagem, (x, y))
    pygame.display.update()