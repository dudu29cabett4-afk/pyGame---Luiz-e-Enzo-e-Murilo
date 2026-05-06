import os
import pygame
import random

pygame.init()
info = pygame.display.Info()
ALTURA = 700
LARGURA = 500
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Hello World!')
base = os.path.dirname(__file__)

# ── Carregamento de imagens ────────────────────────────────────────────────────
costas        = pygame.image.load(os.path.join(base, "pasta_imagens/costas.png"))
frente        = pygame.image.load(os.path.join(base, "pasta_imagens/frente.png"))
direita       = pygame.image.load(os.path.join(base, "pasta_imagens/direita.png"))
esquerda      = pygame.image.load(os.path.join(base, "pasta_imagens/esquerda.png"))
estrada       = pygame.image.load(os.path.join(base, "pasta_imagens/EstradaTeste.png"))
grama         = pygame.image.load(os.path.join(base, "pasta_imagens/GramaTeste.png"))
fundo_img     = pygame.image.load(os.path.join(base, "pasta_imagens/fundo.png"))
carro_amarelo = pygame.image.load(os.path.join(base, "pasta_imagens/amarelo.png"))
carro_vermelho= pygame.image.load(os.path.join(base, "pasta_imagens/vermelho.png"))
carro_rosa    = pygame.image.load(os.path.join(base, "pasta_imagens/rosa.png"))
carro_azul    = pygame.image.load(os.path.join(base, "pasta_imagens/azul.png"))
carro_preto   = pygame.image.load(os.path.join(base, "pasta_imagens/preto.png"))
carro_branco  = pygame.image.load(os.path.join(base, "pasta_imagens/brancop.png"))

tamanho       = 40
LARGURA_CARRO = 60
ALTURA_CARRO  = 35

img_cima     = pygame.transform.scale(frente,   (tamanho, tamanho))
img_baixo    = pygame.transform.scale(costas,   (tamanho, tamanho))
img_esquerda = pygame.transform.scale(esquerda, (tamanho, tamanho))
img_direita  = pygame.transform.scale(direita,  (tamanho, tamanho))
img_estrada  = pygame.transform.scale(estrada,  (LARGURA, tamanho))
img_grama    = pygame.transform.scale(grama,    (LARGURA, tamanho))
img_fundo    = pygame.transform.scale(fundo_img,(LARGURA, ALTURA))

carros_disp = [
    pygame.transform.scale(c, (LARGURA_CARRO, ALTURA_CARRO))
    for c in (carro_amarelo, carro_rosa, carro_vermelho,
              carro_azul, carro_branco, carro_preto)
]

# ══════════════════════════════════════════════════════════════════════════════
#  SISTEMA DE CÂMERA / MUNDO
#
#  • O MUNDO tem coordenadas Y crescendo para BAIXO (igual à tela).
#  • "Frente" = pressionar W = personagem sobe no mundo (world_y diminui).
#  • camera_y = coordenada Y do MUNDO exibida no TOPO da tela.
#        screen_y  =  world_y  -  camera_y
#  • Auto-scroll: camera_y diminui a cada frame (câmera sobe, revelando o
#    caminho à frente). Se o personagem ficar parado, ele desce na tela
#    até sair pela base → game over.
#  • Quando o personagem avança (W), a câmera segue imediatamente.
# ══════════════════════════════════════════════════════════════════════════════

VELOCIDADE_CAMERA = 2            # pixels / frame — avanço automático da câmera
PLAYER_ALVO_Y     = ALTURA * 2 // 3 -100 # posição Y desejada do personagem na tela

# Posição do personagem no ESPAÇO DE MUNDO (floats para suavidade)
player_wx: float = LARGURA / 2 
player_wy: float = float(PLAYER_ALVO_Y)   # começa na posição alvo

# camera_y: a câmera começa posicionada de modo que o personagem apareça
# exatamente em PLAYER_ALVO_Y na tela.
camera_y: float = player_wy - PLAYER_ALVO_Y   # = 0.0

# ── Geração procedural de tiles ───────────────────────────────────────────────
# Cada "linha" do mundo (row = world_y // tamanho) recebe um tile aleatório
# que fica memorizado no dicionário para ser consistente entre frames.
tile_map: dict[int, pygame.Surface] = {}

def gerar_tile(linha: int) -> pygame.Surface:
    """Retorna (e armazena) o tile de uma linha do mundo."""
    if linha not in tile_map:
        tile_map[linha] = random.choices(
            [img_grama, img_estrada], weights=[2, 1]
        )[0]
    return tile_map[linha]

# ── Estado inicial ────────────────────────────────────────────────────────────
imagem = img_baixo
game   = True
clock  = pygame.time.Clock()

# ══════════════════════════════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
while game:
    clock.tick(30)

    # ── 1. Eventos ────────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_wy -= tamanho   # avança (sobe no mundo)
                imagem = img_baixo     # personagem de costas para câmera
            if event.key == pygame.K_s:
                player_wy += tamanho   # recua (desce no mundo)
                imagem = img_cima      # personagem de frente para câmera
            if event.key == pygame.K_a:
                player_wx -= tamanho
                imagem = img_esquerda
            if event.key == pygame.K_d:
                player_wx += tamanho
                imagem = img_direita

    # ── 2. Auto-scroll: câmera avança sozinha (sobe) ──────────────────────────
    camera_y -= VELOCIDADE_CAMERA

    # ── 3. Câmera segue o personagem quando ele vai à frente ─────────────────
    # target_cam = câmera ideal para manter personagem em PLAYER_ALVO_Y
    target_cam = player_wy - PLAYER_ALVO_Y
    # Se o personagem está à frente (camera_y ainda está "atrás"), câmera salta
    if camera_y > target_cam:
        camera_y = target_cam

    # ── 4. Limites ────────────────────────────────────────────────────────────
    player_wx = max(0.0, min(float(LARGURA - tamanho), player_wx))

    # Coordenadas de tela do personagem
    player_screen_y = player_wy - camera_y
    player_screen_x = int(player_wx)

    # Game over: personagem saiu pela base (ficou para trás) ou pelo topo
    if player_screen_y >= ALTURA or player_screen_y < -tamanho:
        game = False

    # ── 5. Desenho ────────────────────────────────────────────────────────────
    window.blit(img_fundo, (0, 0))

    # Renderiza apenas as linhas de tile visíveis na tela
    linha_ini = int(camera_y // tamanho) - 1
    linha_fim = int((camera_y + ALTURA) // tamanho) + 1
    for linha in range(linha_ini, linha_fim + 1):
        sy = int(linha * tamanho - camera_y)
        window.blit(gerar_tile(linha), (0, sy))

    # Renderiza o personagem
    window.blit(imagem, (player_screen_x, int(player_screen_y)))

    pygame.display.update()

pygame.quit()