# # ===== Inicialização =====
# # ----- Importa e inicia pacotes

import os
import pygame
import random

pygame.init()
info = pygame.display.Info()
ALTURA = info.current_h - 60
LARGURA = 800
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Hello World!')
base = os.path.dirname(__file__)

costas = pygame.image.load(os.path.join(base, "costas.png"))
frente = pygame.image.load(os.path.join(base, "frente.png"))
direita = pygame.image.load(os.path.join(base, "direita.png"))
esquerda = pygame.image.load(os.path.join(base, "esquerda.png"))

estrada = pygame.image.load(os.path.join(base, "EstradaTeste.png"))
grama = pygame.image.load(os.path.join(base, "GramaTeste.png"))
fundo = pygame.image.load(os.path.join(base, "fundo.png"))

carro_amarelo = pygame.image.load(os.path.join(base, "amarelo.png"))
carro_vermelho = pygame.image.load(os.path.join(base, "vermelho.png"))
carro_rosa = pygame.image.load(os.path.join(base, "rosa.png"))
carro_azul = pygame.image.load(os.path.join(base, "azul.png"))
carro_preto = pygame.image.load(os.path.join(base, "preto.png"))
carro_branco = pygame.image.load(os.path.join(base, "brancop.png"))


tamanho = 40
altura_faixa = 80

img_cima = pygame.transform.scale(frente, (tamanho, tamanho))
img_baixo = pygame.transform.scale(costas, (tamanho, tamanho))
img_esquerda = pygame.transform.scale(esquerda, (tamanho, tamanho))
img_direita = pygame.transform.scale(direita, (tamanho, tamanho))
img_estrada = pygame.transform.scale(estrada, (LARGURA, tamanho))
img_grama = pygame.transform.scale(grama, (LARGURA, tamanho))
img_fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
imagem = img_baixo

blocos = [[img_grama, 0], [img_estrada, 80]]
velocidade = 2
raio = 20
diametro = raio * 2
x = LARGURA // 2
y = ALTURA // 2

LARGURA_CARRO = 60
ALTURA_CARRO  = 35

carros_disp = [pygame.transform.scale(carro_amarelo ,(LARGURA_CARRO, ALTURA_CARRO)), pygame.transform.scale(carro_rosa ,(LARGURA_CARRO, ALTURA_CARRO)), pygame.transform.scale(carro_vermelho ,(LARGURA_CARRO, ALTURA_CARRO)), pygame.transform.scale(carro_azul ,(LARGURA_CARRO, ALTURA_CARRO)), pygame.transform.scale(carro_branco ,(LARGURA_CARRO, ALTURA_CARRO)), pygame.transform.scale(carro_preto ,(LARGURA_CARRO, ALTURA_CARRO))]
# ----- Inicia estruturas de dados


game = True
clock = pygame.time.Clock()
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
    for bloco in blocos:
        bloco[1] += velocidade

        if bloco[1] >= ALTURA:
            bloco[1] = -altura_faixa
            bloco[0] = random.choice([img_grama, img_estrada])
    y += velocidade

    x = max(0, min(LARGURA - tamanho, x))
    if y >= ALTURA - tamanho:
        game = False

    # ----- Gera saídas
    window.blit(fundo, (0, 0))
    for bloco in blocos:
        window.blit(bloco[0], (0, bloco[1]))
    window.blit(imagem, (x, y))
    pygame.display.update()
    clock.tick(30)