# # ===== Inicialização =====
# # ----- Importa e inicia pacotes
# import pygame

# pygame.init()

# # ----- Gera tela principal

# largura = 700
# altura = 600
# window = pygame.display.set_mode((largura, altura))
# pygame.display.set_caption('Hello World!')

# x = largura // 2
# y = altura // 2
# raio = 12
# # ----- Inicia estruturas de dados
# game = True

# # ===== Loop principal =====
# while game:
#     # ----- Trata eventos
#     for event in pygame.event.get():
#         # ----- Verifica consequências
#         if event.type == pygame.QUIT:
#             game = False
    
#     tecla = pygame.key.get_pressed()

#     if tecla[pygame.K_w]:
#         y -= raio
#     if tecla[pygame.K_s]:
#         y += raio
#     if tecla[pygame.K_a]:
#         x -= raio
#     if tecla[pygame.K_d]:
#         x += raio

#     # Limita dentro da tela
#     x = max(raio, min(largura - raio, x))
#     y = max(raio, min(altura - raio, y))


#     # ----- Gera saídas
#     window.fill((255, 255, 255))  # Preenche com a cor branca
#     pygame.draw.circle(window, (106,90,205), (x, y), 12)

#     # ----- Atualiza estado do jogo
#     pygame.display.update()  # Mostra o novo frame para o jogador

# # ===== Finalização =====
# pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

# # ===== Inicialização =====
# # ----- Importa e inicia pacotes
import pygame
pygame.init()

LARGURA = 800
ALTURA = 600
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Hello World!')


raio = 20
diametro = raio * 2
x = LARGURA // 2
y = ALTURA // 2
# ----- Inicia estruturas de dados

game = True
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y -= diametro
            if event.key == pygame.K_s:
                y += diametro
            if event.key == pygame.K_a:
                x -= diametro
            if event.key == pygame.K_d:
                x += diametro

    x = max(raio, min(LARGURA - raio, x))
    y = max(raio, min(ALTURA - raio, y))

    # ----- Gera saídas
    window.fill((0,0,0))
    pygame.draw.circle(window, (106,90,205), (x, y), raio)
    pygame.display.update()