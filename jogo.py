import os
import pygame
import random

pygame.init()

ALTURA  = 700
LARGURA = 500
window  = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Cruze Quatá!')
base = os.path.dirname(__file__)

# ── Imagens ────────────────────────────────────────────────────────────────
costas         = pygame.image.load(os.path.join(base, "pasta_imagens/costas.png"))
frente         = pygame.image.load(os.path.join(base, "pasta_imagens/frente.png"))
direita        = pygame.image.load(os.path.join(base, "pasta_imagens/direita.png"))
esquerda       = pygame.image.load(os.path.join(base, "pasta_imagens/esquerda.png"))
estrada        = pygame.image.load(os.path.join(base, "pasta_imagens/EstradaTeste.png"))
grama          = pygame.image.load(os.path.join(base, "pasta_imagens/GramaTeste.png"))
fundo_img      = pygame.image.load(os.path.join(base, "pasta_imagens/fundoGame.png"))
fundo_fim_img  = pygame.image.load(os.path.join(base, "pasta_imagens/gameover.png"))   # tela de fim
carro_amarelo  = pygame.image.load(os.path.join(base, "pasta_imagens/amarelo.png"))
carro_vermelho = pygame.image.load(os.path.join(base, "pasta_imagens/vermelho.png"))
carro_rosa     = pygame.image.load(os.path.join(base, "pasta_imagens/rosa.png"))
carro_azul     = pygame.image.load(os.path.join(base, "pasta_imagens/azul.png"))
carro_preto    = pygame.image.load(os.path.join(base, "pasta_imagens/preto.png"))
carro_branco   = pygame.image.load(os.path.join(base, "pasta_imagens/brancop.png"))

# ── Tamanhos ───────────────────────────────────────────────────────────────
tamanho       = 40
LARGURA_CARRO = 60
ALTURA_CARRO  = 35

# ── Superfícies escaladas ──────────────────────────────────────────────────
# [ALTERAÇÃO 4] W → costas (boneco de costas ao subir), S → frente (de frente ao descer)
img_cima      = pygame.transform.scale(costas,   (tamanho, tamanho))  # era frente
img_baixo     = pygame.transform.scale(frente,   (tamanho, tamanho))  # era costas
img_esquerda  = pygame.transform.scale(esquerda, (tamanho, tamanho))
img_direita   = pygame.transform.scale(direita,  (tamanho, tamanho))
img_estrada   = pygame.transform.scale(estrada,  (LARGURA, tamanho))
img_grama     = pygame.transform.scale(grama,    (LARGURA, tamanho))
img_fundo     = pygame.transform.scale(fundo_img,     (LARGURA, ALTURA))
img_fundo_fim = pygame.transform.scale(fundo_fim_img, (LARGURA, ALTURA))  # fim de jogo

# Carros: versão direita e versão espelhada (esquerda)
carros_disp_r = [
    pygame.transform.scale(c, (LARGURA_CARRO, ALTURA_CARRO))
    for c in (carro_amarelo, carro_rosa, carro_vermelho,
              carro_azul, carro_branco, carro_preto)
]
carros_disp_l = [pygame.transform.flip(img, True, False) for img in carros_disp_r]

# ── Constantes ─────────────────────────────────────────────────────────────
VELOCIDADE_CAMERA = 2
PLAYER_ALVO_Y     = ALTURA * 2 // 3 - 100

# [ALTERAÇÃO 2] Quantidade de linhas iniciais que só geram grama (safe zone)
SAFE_ZONE_LINHAS = 6

# ── Fontes ─────────────────────────────────────────────────────────────────
fonte       = pygame.font.SysFont("arial", 28, bold=True)
fonte_botao = pygame.font.SysFont("arial", 30, bold=True)

# ══════════════════════════════════════════════════════════════════════════
# ESTADO DO MUNDO  (dicionários limpos a cada novo jogo)
# ══════════════════════════════════════════════════════════════════════════
tile_map:      dict = {}
lane_data:     dict = {}
carros_ativos: list = []

def resetar_mundo():
    """Limpa tiles, lane data e carros para reiniciar o jogo."""
    tile_map.clear()
    lane_data.clear()
    carros_ativos.clear()

def gerar_tile(linha: int) -> pygame.Surface:
    """
    Retorna o tile da linha.
    [ALTERAÇÃO 2] Linhas dentro da safe zone sempre retornam grama.
    """
    if linha not in tile_map:
        linha_base  = int(PLAYER_ALVO_Y // tamanho)
        safe_inicio = linha_base - SAFE_ZONE_LINHAS
        if linha >= safe_inicio:          # dentro da safe zone → só grama
            tile_map[linha] = img_grama
        else:                             # fora da safe zone → geração normal
            tile_map[linha] = random.choices(
                [img_grama, img_estrada], weights=[2, 1]
            )[0]
    return tile_map[linha]

def obter_lane_data(linha: int) -> dict:
    """Retorna e inicializa os dados de tráfego de uma faixa de estrada."""
    if linha not in lane_data:
        direcao   = 1 if linha % 2 == 0 else -1
        velocidade= random.uniform(2.5, 6.0)
        spawn_gap = random.randint(int(LARGURA * 0.55), int(LARGURA * 1.1))
        proximo_x = float(-LARGURA_CARRO) if direcao == 1 else float(LARGURA)
        lane_data[linha] = {
            "direcao":         direcao,
            "velocidade":      velocidade,
            "spawn_gap":       spawn_gap,
            "proximo_spawn_x": proximo_x,
        }
    return lane_data[linha]

# ── Classe Carro ───────────────────────────────────────────────────────────
class Carro:
    __slots__ = ("linha", "x", "velocidade", "direcao", "img")

    def __init__(self, linha, x, velocidade, direcao, img):
        self.linha      = linha
        self.x          = x
        self.velocidade = velocidade
        self.direcao    = direcao
        self.img        = img

    def update(self):
        self.x += self.velocidade * self.direcao

    def fora_da_tela(self):
        if self.direcao == 1:
            return self.x > LARGURA + LARGURA_CARRO
        return self.x < -LARGURA_CARRO * 2

    def screen_y(self, camera_y):
        return int(self.linha * tamanho - camera_y)

    def draw(self, surface, camera_y):
        surface.blit(self.img, (int(self.x), self.screen_y(camera_y)))

    def rect(self, camera_y):
        m = 4
        return pygame.Rect(
            int(self.x) + m,
            self.screen_y(camera_y) + m,
            LARGURA_CARRO - m * 2,
            ALTURA_CARRO  - m * 2,
        )

def tentar_spawnar_carros(linha_ini: int, linha_fim: int):
    """
    Spawna carros nas faixas de estrada visíveis.
    [ALTERAÇÃO 2] Nunca spawna dentro da safe zone.
    """
    linha_base   = int(PLAYER_ALVO_Y // tamanho)
    safe_inicio  = linha_base - SAFE_ZONE_LINHAS

    for linha in range(linha_ini, linha_fim + 1):
        if linha >= safe_inicio:           # safe zone: sem carros
            continue
        if gerar_tile(linha) is not img_estrada:
            continue

        ld = obter_lane_data(linha)
        d  = ld["direcao"]
        v  = ld["velocidade"]
        ja_existem = [c for c in carros_ativos if c.linha == linha]

        if not ja_existem:
            x0  = float(-LARGURA_CARRO) if d == 1 else float(LARGURA)
            img = random.choice(carros_disp_r if d == 1 else carros_disp_l)
            carros_ativos.append(Carro(linha, x0, v, d, img))
            ld["proximo_spawn_x"] = x0 + d * ld["spawn_gap"]
        else:
            ultimo = max(ja_existem, key=lambda c: c.x * d)
            if d == 1 and ultimo.x >= ld["proximo_spawn_x"]:
                img = random.choice(carros_disp_r)
                carros_ativos.append(Carro(linha, float(-LARGURA_CARRO), v, d, img))
                ld["proximo_spawn_x"] += ld["spawn_gap"]
            elif d == -1 and ultimo.x <= ld["proximo_spawn_x"]:
                img = random.choice(carros_disp_l)
                carros_ativos.append(Carro(linha, float(LARGURA), v, d, img))
                ld["proximo_spawn_x"] -= ld["spawn_gap"]

# ══════════════════════════════════════════════════════════════════════════
# TELA INICIAL
# ══════════════════════════════════════════════════════════════════════════
def tela_inicial():
    clock_menu = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        window.blit(img_fundo, (0, 0))

        if pygame.time.get_ticks() % 1000 < 500:
            texto  = fonte.render("Pressione ESPAÇO para começar", True, (255, 255, 255))
            rect   = texto.get_rect(center=(LARGURA // 2, 50))
            sombra = fonte.render("Pressione ESPAÇO para começar", True, (0, 0, 0))
            window.blit(sombra, (rect.x + 2, rect.y + 2))
            window.blit(texto, rect)

        pygame.display.update()
        clock_menu.tick(30)

# ══════════════════════════════════════════════════════════════════════════
# [ALTERAÇÃO 1] TELA DE GAME OVER com botões RETRY e MENU
# ══════════════════════════════════════════════════════════════════════════
def tela_game_over() -> str:
    """
    Exibe a tela de fim de jogo sobre a imagem 'fim jogo.png'.
    Retorna 'retry' ou 'menu' conforme o botão clicado.
    """
    clock_go = pygame.time.Clock()

    # Posição dos botões (centralizados horizontalmente)
    btn_w, btn_h = 160, 55
    btn_retry = pygame.Rect(LARGURA // 2 - btn_w - 20, ALTURA // 2 + 60, btn_w, btn_h)
    btn_menu  = pygame.Rect(LARGURA // 2 + 20,          ALTURA // 2 + 60, btn_w, btn_h)

    COR_NORMAL = (30,  30,  30,  190)
    COR_HOVER  = (200, 80,  20,  230)
    COR_TEXTO  = (255, 255, 255)
    COR_BORDA  = (255, 255, 255)

    # Surface auxiliar para desenhar retângulos semi-transparentes
    btn_surf = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_retry.collidepoint(mouse):
                    return "retry"
                if btn_menu.collidepoint(mouse):
                    return "menu"

        window.blit(img_fundo_fim, (0, 0))

        # Botão RETRY
        btn_surf.fill(COR_HOVER if btn_retry.collidepoint(mouse) else COR_NORMAL)
        window.blit(btn_surf, btn_retry.topleft)
        pygame.draw.rect(window, COR_BORDA, btn_retry, 2, border_radius=8)
        t = fonte_botao.render("RETRY", True, COR_TEXTO)
        window.blit(t, t.get_rect(center=btn_retry.center))

        # Botão MENU
        btn_surf.fill(COR_HOVER if btn_menu.collidepoint(mouse) else COR_NORMAL)
        window.blit(btn_surf, btn_menu.topleft)
        pygame.draw.rect(window, COR_BORDA, btn_menu, 2, border_radius=8)
        t = fonte_botao.render("MENU", True, COR_TEXTO)
        window.blit(t, t.get_rect(center=btn_menu.center))

        pygame.display.update()
        clock_go.tick(30)

# ══════════════════════════════════════════════════════════════════════════
# LOOP PRINCIPAL (encapsulado para ser reiniciável)
# ══════════════════════════════════════════════════════════════════════════
def iniciar_jogo() -> str:
    """
    Executa o loop principal do jogo.
    Retorna 'retry' ou 'menu' após o game over.
    """
    resetar_mundo()

    player_wx: float = LARGURA / 2
    player_wy: float = float(PLAYER_ALVO_Y)
    camera_y:  float = player_wy - PLAYER_ALVO_Y  # câmera alinhada ao jogador

    # [ALTERAÇÃO 3] câmera só começa a se mover depois que o jogador pressiona W
    camera_ativa = False

    imagem = img_baixo   # começa de frente (olhando para a câmera)
    clock  = pygame.time.Clock()

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_wy   -= tamanho
                    imagem       = img_cima    # [ALTERAÇÃO 4] W → costas
                    camera_ativa = True        # [ALTERAÇÃO 3] ativa câmera
                if event.key == pygame.K_s:
                    player_wy  += tamanho
                    imagem      = img_baixo    # [ALTERAÇÃO 4] S → frente
                if event.key == pygame.K_a:
                    player_wx  -= tamanho
                    imagem      = img_esquerda
                if event.key == pygame.K_d:
                    player_wx  += tamanho
                    imagem      = img_direita

        # [ALTERAÇÃO 3] câmera avança só se ativada
        if camera_ativa:
            camera_y -= VELOCIDADE_CAMERA

        target_cam = player_wy - PLAYER_ALVO_Y
        if camera_y > target_cam:
            camera_y = target_cam

        player_wx = max(0.0, min(float(LARGURA - tamanho), player_wx))

        player_screen_y = player_wy - camera_y
        player_screen_x = int(player_wx)

        # Game over por sair da tela
        if player_screen_y >= ALTURA or player_screen_y < -tamanho:
            return tela_game_over()

        linha_ini = int(camera_y // tamanho) - 1
        linha_fim = int((camera_y + ALTURA) // tamanho) + 1

        tentar_spawnar_carros(linha_ini, linha_fim)

        for c in carros_ativos:
            c.update()
        carros_ativos[:] = [c for c in carros_ativos if not c.fora_da_tela()]

        # Game over por colisão com carro
        player_rect = pygame.Rect(
            player_screen_x + 4,
            int(player_screen_y) + 4,
            tamanho - 8,
            tamanho - 8,
        )
        for c in carros_ativos:
            if c.rect(camera_y).colliderect(player_rect):
                return tela_game_over()

        # ── Desenho ────────────────────────────────────────────────────
        window.blit(img_fundo, (0, 0))

        for linha in range(linha_ini, linha_fim + 1):
            sy = int(linha * tamanho - camera_y)
            window.blit(gerar_tile(linha), (0, sy))

        for c in carros_ativos:
            sy = c.screen_y(camera_y)
            if -ALTURA_CARRO <= sy <= ALTURA:
                c.draw(window, camera_y)

        window.blit(imagem, (player_screen_x, int(player_screen_y)))

        pygame.display.update()

# ══════════════════════════════════════════════════════════════════════════
# LOOP MESTRE — gerencia telas: inicial → jogo → game over → retry/menu
# ══════════════════════════════════════════════════════════════════════════
tela_inicial()

while True:
    resultado = iniciar_jogo()     # devolve "retry" ou "menu"
    if resultado == "menu":
        tela_inicial()             # volta para o menu
    # se "retry", reinicia direto sem passar pelo menu