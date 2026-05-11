import os
import random
import pygame

pygame.init()

ALTURA = 700
LARGURA = 500
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cruze Quatá!")

base = os.path.dirname(__file__)

costas         = pygame.image.load(os.path.join(base, "pasta_imagens/costas.png"))
frente         = pygame.image.load(os.path.join(base, "pasta_imagens/frente.png"))
direita        = pygame.image.load(os.path.join(base, "pasta_imagens/direita.png"))
esquerda       = pygame.image.load(os.path.join(base, "pasta_imagens/esquerda.png"))
estrada        = pygame.image.load(os.path.join(base, "pasta_imagens/EstradaTeste.png"))
grama          = pygame.image.load(os.path.join(base, "pasta_imagens/GramaTeste.png"))
fundo_img      = pygame.image.load(os.path.join(base, "pasta_imagens/fundoGame.png"))
fundo_fim_img  = pygame.image.load(os.path.join(base, "pasta_imagens/gameover.png"))
carro_amarelo  = pygame.image.load(os.path.join(base, "pasta_imagens/amarelo.png"))
carro_vermelho = pygame.image.load(os.path.join(base, "pasta_imagens/vermelho.png"))
carro_rosa     = pygame.image.load(os.path.join(base, "pasta_imagens/rosa.png"))
carro_azul     = pygame.image.load(os.path.join(base, "pasta_imagens/azul.png"))
carro_preto    = pygame.image.load(os.path.join(base, "pasta_imagens/preto.png"))
carro_branco   = pygame.image.load(os.path.join(base, "pasta_imagens/brancop.png"))

TAMANHO_TILE = 48
PLAYER_ALVO_Y = ALTURA * 2 // 3 - 100

def escalar_carro(img):
    nova_altura = TAMANHO_TILE
    orig_w, orig_h = img.get_size()
    nova_largura = int(orig_w * (nova_altura / orig_h))
    return pygame.transform.scale(img, (nova_largura, nova_altura))

img_cima     = pygame.transform.scale(costas,   (TAMANHO_TILE, TAMANHO_TILE))
img_baixo    = pygame.transform.scale(frente,   (TAMANHO_TILE, TAMANHO_TILE))
img_esquerda = pygame.transform.scale(esquerda, (TAMANHO_TILE, TAMANHO_TILE))
img_direita  = pygame.transform.scale(direita,  (TAMANHO_TILE, TAMANHO_TILE))
img_estrada  = pygame.transform.scale(estrada,  (LARGURA, TAMANHO_TILE))
img_grama    = pygame.transform.scale(grama,    (LARGURA, TAMANHO_TILE))
img_fundo    = pygame.transform.scale(fundo_img,     (LARGURA, ALTURA))
img_fundo_fim = pygame.transform.scale(fundo_fim_img, (LARGURA, ALTURA))

img_rio = pygame.Surface((LARGURA, TAMANHO_TILE))
img_rio.fill((80, 170, 230))
for i in range(0, LARGURA, 30):
    pygame.draw.ellipse(img_rio, (130, 200, 255), (i, TAMANHO_TILE // 2 - 4, 20, 8))

carros_disp_r = [escalar_carro(c) for c in (
    carro_amarelo, carro_rosa, carro_vermelho, carro_azul, carro_branco, carro_preto
)]
carros_disp_l = [pygame.transform.flip(img, True, False) for img in carros_disp_r]

troncos_disp_r = []
troncos_disp_l = []
for largura_tronco in [96, 120, 144]:
    surf = pygame.Surface((largura_tronco, TAMANHO_TILE), pygame.SRCALPHA)
    pygame.draw.rect(surf, (101, 67, 33), (0, 6, largura_tronco, TAMANHO_TILE - 12), border_radius=10)
    pygame.draw.rect(surf, (120, 80, 40), (4, 10, largura_tronco - 8, TAMANHO_TILE - 20), border_radius=8)
    for xi in range(8, largura_tronco - 8, 20):
        pygame.draw.ellipse(surf, (80, 50, 25), (xi, 14, 12, 8))
    troncos_disp_r.append(surf)
    troncos_disp_l.append(pygame.transform.flip(surf, True, False))

LARGURA_CARRO = carros_disp_r[0].get_width()
ALTURA_CARRO = TAMANHO_TILE
SAFE_ZONE_LINHAS = 1

fonte = pygame.font.SysFont("arial", 28, bold=True)
fonte_botao = pygame.font.SysFont("arial", 28, bold=True)
fonte_score = pygame.font.SysFont("arial", 24, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 19)
fonte_hud = pygame.font.SysFont("arial", 20, bold=True)
fonte_kbd = pygame.font.SysFont("arial", 14, bold=True)

tile_map = {}
lane_data = {}
carros_ativos = []
troncos_ativos = []

TIPO_GRAMA = "grama"
TIPO_ESTRADA = "estrada"
TIPO_RIO = "rio"

# ----------------------------------------------------
# Power-ups
# ----------------------------------------------------

POWERUP_ESCUDO_DURACAO_MS = 6_000
POWERUP_XP2_DURACAO_MS = 8_000
MAX_POWERUPS_ATIVOS = 1

def criar_img_powerup_escudo():
    size = 36
    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    import math
    cx, cy = size // 2, size // 2
    pontos = []
    for i in range(10):
        angulo = math.pi / 2 + i * math.pi / 5
        r = (size // 2 - 2) if i % 2 == 0 else (size // 4)
        pontos.append((cx + r * math.cos(angulo), cy - r * math.sin(angulo)))

    pygame.draw.polygon(surf, (255, 220, 30), pontos)
    pygame.draw.polygon(surf, (255, 160, 0), pontos, 2)
    pygame.draw.circle(surf, (255, 255, 180), (cx, cy), 6)
    return surf

def criar_img_powerup_xp2():
    size = 36
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2

    pygame.draw.circle(surf, (255, 190, 70), (cx, cy), 15)
    pygame.draw.circle(surf, (70, 35, 10), (cx, cy), 13)
    pygame.draw.circle(surf, (255, 235, 170), (cx, cy), 13, 2)

    f = pygame.font.SysFont("arial", 18, bold=True)
    txt = f.render("x2", True, (255, 240, 220))
    surf.blit(txt, txt.get_rect(center=(cx, cy)))
    return surf

img_powerup_escudo = criar_img_powerup_escudo()
img_powerup_xp2 = criar_img_powerup_xp2()

def resetar_mundo():
    tile_map.clear()
    lane_data.clear()
    carros_ativos.clear()
    troncos_ativos.clear()

def gerar_tile(linha: int):
    if linha not in tile_map:
        linha_base = int(PLAYER_ALVO_Y // TAMANHO_TILE)
        safe_inicio = linha_base - SAFE_ZONE_LINHAS

        if linha >= safe_inicio:
            tile_map[linha] = (img_grama, TIPO_GRAMA)
        else:
            escolha = random.choices(
                [TIPO_GRAMA, TIPO_ESTRADA, TIPO_RIO],
                weights=[3, 4, 1]
            )[0]

            if escolha == TIPO_GRAMA:
                tile_map[linha] = (img_grama, TIPO_GRAMA)
            elif escolha == TIPO_ESTRADA:
                tile_map[linha] = (img_estrada, TIPO_ESTRADA)
            else:
                tile_map[linha] = (img_rio, TIPO_RIO)

    return tile_map[linha]

def calcular_multiplicador_velocidade(score: int) -> float:
    return 1.0 + min(score / 1200.0, 0.25)

def obter_lane_data(linha: int, score: int = 0) -> dict:
    if linha not in lane_data:
        direcao = 1 if linha % 2 == 0 else -1
        tipo = gerar_tile(linha)[1]
        mult = calcular_multiplicador_velocidade(score)

        if tipo == TIPO_RIO:
            velocidade = random.uniform(2.0, 4.5) * mult
            spawn_gap = random.randint(int(LARGURA * 0.35), int(LARGURA * 0.6))
        else:
            velocidade = random.uniform(4.5, 9.0) * mult
            spawn_gap = random.randint(int(LARGURA * 0.35), int(LARGURA * 0.65))

        proximo_x = float(-LARGURA_CARRO) if direcao == 1 else float(LARGURA)
        lane_data[linha] = {
            "direcao": direcao,
            "velocidade": velocidade,
            "spawn_gap": spawn_gap,
            "proximo_spawn_x": proximo_x,
        }

    return lane_data[linha]

class Carro:
    __slots__ = ("linha", "x", "velocidade", "direcao", "img", "largura")

    def __init__(self, linha, x, velocidade, direcao, img):
        self.linha = linha
        self.x = x
        self.velocidade = velocidade
        self.direcao = direcao
        self.img = img
        self.largura = img.get_width()

    def update(self):
        self.x += self.velocidade * self.direcao

    def fora_da_tela(self):
        if self.direcao == 1:
            return self.x > LARGURA + self.largura
        return self.x < -self.largura * 2

    def screen_y(self, camera_y):
        return int(self.linha * TAMANHO_TILE - camera_y)

    def draw(self, surface, camera_y):
        surface.blit(self.img, (int(self.x), self.screen_y(camera_y)))

    def rect(self, camera_y):
        m = 4
        return pygame.Rect(
            int(self.x) + m,
            self.screen_y(camera_y) + m,
            self.largura - m * 2,
            ALTURA_CARRO - m * 2,
        )

class PowerUp:
    TAMANHO = 36

    def __init__(self, wx: float, wy: float, tipo: str):
        self.wx = wx
        self.wy = wy
        self.tipo = tipo   # "escudo" ou "xp2"
        self.coletado = False

    def screen_pos(self, camera_y):
        return int(self.wx), int(self.wy - camera_y)

    def rect_mundo(self):
        m = 4
        return pygame.Rect(
            int(self.wx) + m,
            int(self.wy) + m,
            self.TAMANHO - m * 2,
            self.TAMANHO - m * 2
        )

    def draw(self, surface, camera_y):
        if self.coletado:
            return

        sx, sy = self.screen_pos(camera_y)
        if -self.TAMANHO <= sy <= ALTURA:
            t = pygame.time.get_ticks()
            alpha = int(120 + 80 * abs((t % 800) / 400.0 - 1))

            if self.tipo == "xp2":
                icon = img_powerup_xp2
                glow_cor = (255, 190, 70, alpha)
            else:
                icon = img_powerup_escudo
                glow_cor = (255, 230, 80, alpha)

            glow = pygame.Surface((self.TAMANHO + 16, self.TAMANHO + 16), pygame.SRCALPHA)
            pygame.draw.circle(
                glow,
                glow_cor,
                (self.TAMANHO // 2 + 8, self.TAMANHO // 2 + 8),
                self.TAMANHO // 2 + 6
            )
            surface.blit(glow, (sx - 8, sy - 8))
            surface.blit(icon, (sx, sy))

def tentar_spawnar_carros(linha_ini: int, linha_fim: int, score: int = 0):
    linha_base = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    safe_inicio = linha_base - SAFE_ZONE_LINHAS

    for linha in range(linha_ini, linha_fim + 1):
        if linha >= safe_inicio:
            continue

        _, tipo = gerar_tile(linha)

        if tipo == TIPO_ESTRADA:
            ld = obter_lane_data(linha, score)
            d = ld["direcao"]
            v = ld["velocidade"]
            ja_existem = [c for c in carros_ativos if c.linha == linha]

            if not ja_existem:
                x0 = float(-LARGURA_CARRO) if d == 1 else float(LARGURA)
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

        elif tipo == TIPO_RIO:
            ld = obter_lane_data(linha, score)
            d = ld["direcao"]
            v = ld["velocidade"]
            ja_existem = [t for t in troncos_ativos if t.linha == linha]

            if not ja_existem:
                img = random.choice(troncos_disp_r if d == 1 else troncos_disp_l)
                x0 = float(-img.get_width()) if d == 1 else float(LARGURA)
                troncos_ativos.append(Carro(linha, x0, v, d, img))
                ld["proximo_spawn_x"] = x0 + d * ld["spawn_gap"]
            else:
                ultimo = max(ja_existem, key=lambda c: c.x * d)

                if d == 1 and ultimo.x >= ld["proximo_spawn_x"]:
                    img = random.choice(troncos_disp_r)
                    troncos_ativos.append(Carro(linha, float(-img.get_width()), v, d, img))
                    ld["proximo_spawn_x"] += ld["spawn_gap"]
                elif d == -1 and ultimo.x <= ld["proximo_spawn_x"]:
                    img = random.choice(troncos_disp_l)
                    troncos_ativos.append(Carro(linha, float(LARGURA), v, d, img))
                    ld["proximo_spawn_x"] -= ld["spawn_gap"]

def gerar_powerups_para_linhas(linha_ini, linha_fim, powerups: list, linhas_com_powerup: set, score: int):
    """Gera power-ups raros em linhas de grama visíveis."""
    if len([p for p in powerups if not p.coletado]) >= MAX_POWERUPS_ATIVOS:
        return

    linha_base = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    safe_inicio = linha_base - SAFE_ZONE_LINHAS

    for linha in range(linha_ini, linha_fim + 1):
        if linha >= safe_inicio:
            continue
        if linha in linhas_com_powerup:
            continue

        _, tipo = gerar_tile(linha)
        if tipo != TIPO_GRAMA:
            continue

        chance_escudo = 0.007 + min(score / 5000.0, 0.003)
        chance_xp2 = 0.006 + min(score / 5000.0, 0.003)

        roll = random.random()
        tipo_powerup = None

        if roll < chance_escudo:
            tipo_powerup = "escudo"
        elif roll < chance_escudo + chance_xp2:
            tipo_powerup = "xp2"

        if tipo_powerup is not None:
            col = random.randint(1, LARGURA // TAMANHO_TILE - 2)
            wx = float(col * TAMANHO_TILE)
            wy = float(linha * TAMANHO_TILE + (TAMANHO_TILE - PowerUp.TAMANHO) // 2)
            powerups.append(PowerUp(wx, wy, tipo_powerup))
            linhas_com_powerup.add(linha)

# ----------------------------------------------------
# UI
# ----------------------------------------------------

def desenhar_botao(surface, rect, label, kbd_hint, hover,
                   cor_normal=(30, 30, 60), cor_hover=(180, 70, 10),
                   cor_borda=(255, 200, 50), cor_texto=(255, 255, 255)):
    cor = cor_hover if hover else cor_normal
    pygame.draw.rect(surface, cor, rect, border_radius=10)
    pygame.draw.rect(surface, cor_borda, rect, 2, border_radius=10)

    t = fonte_botao.render(label, True, cor_texto)
    surface.blit(t, t.get_rect(center=(rect.centerx, rect.centery - 7)))

    hint = fonte_kbd.render(f"[{kbd_hint}]", True, (220, 200, 100))
    surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.centery + 13)))

def desenhar_painel_como_jogar():
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 195))
    window.blit(overlay, (0, 0))

    painel_w, painel_h = 430, 470
    painel_x = (LARGURA - painel_w) // 2
    painel_y = (ALTURA - painel_h) // 2

    painel = pygame.Surface((painel_w, painel_h), pygame.SRCALPHA)
    painel.fill((15, 18, 42, 230))
    pygame.draw.rect(painel, (255, 200, 50), (0, 0, painel_w, painel_h), 3, border_radius=14)
    window.blit(painel, (painel_x, painel_y))

    titulo = fonte_botao.render("COMO JOGAR", True, (255, 210, 50))
    window.blit(titulo, titulo.get_rect(center=(LARGURA // 2, painel_y + 32)))

    pygame.draw.line(
        window,
        (255, 200, 50, 180),
        (painel_x + 20, painel_y + 52),
        (painel_x + painel_w - 20, painel_y + 52),
        1
    )

    secoes = [
        ("MOVIMENTAÇÃO", [
            ("W", "Andar para cima  (+1 ponto)"),
            ("S", "Andar para baixo"),
            ("A", "Andar para esquerda"),
            ("D", "Andar para direita"),
        ]),
        ("OBSTÁCULOS", [
            ("🚗", "Desvie dos carros na estrada!"),
            ("🌊", "Atravesse rios em cima de troncos!"),
            ("💀", "Cair na água = morte!"),
        ]),
        ("POWER-UPS", [
            ("★", "Escudo dourado: imunidade por 6s."),
            ("x2", "Moeda dourada: vale 2 pontos por 8s."),
            ("",  "Todos os power-ups estão mais raros."),
        ]),
        ("DIFICULDADE", [
            ("📈", "Quanto mais longe, mais rápido!"),
        ]),
    ]

    y_cur = painel_y + 68
    limite_texto = painel_y + painel_h - 76

    for titulo_sec, itens in secoes:
        if y_cur > limite_texto:
            break

        hdr = fonte_hud.render(titulo_sec, True, (255, 180, 40))
        window.blit(hdr, (painel_x + 18, y_cur))
        y_cur += 22

        for icone, texto in itens:
            if y_cur > limite_texto:
                break

            if icone:
                ic = fonte_titulo.render(icone, True, (160, 220, 255))
                window.blit(ic, (painel_x + 22, y_cur))

            tx = fonte_titulo.render(texto, True, (210, 225, 255))
            window.blit(tx, (painel_x + 50, y_cur))
            y_cur += 21

        y_cur += 8

    btn_fechar = pygame.Rect(LARGURA // 2 - 75, painel_y + painel_h - 52, 150, 42)
    mouse = pygame.mouse.get_pos()
    desenhar_botao(
        window, btn_fechar, "FECHAR", "ESC",
        btn_fechar.collidepoint(mouse),
        cor_normal=(50, 20, 70),
        cor_hover=(160, 40, 10)
    )
    return btn_fechar

def tela_inicial():
    clock_menu = pygame.time.Clock()
    btn_w, btn_h = 220, 58
    btn_como_jogar = pygame.Rect(LARGURA // 2 - btn_w // 2, ALTURA // 2 + 30, btn_w, btn_h)
    mostrar_como_jogar = False

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not mostrar_como_jogar:
                    return
                if event.key == pygame.K_h and not mostrar_como_jogar:
                    mostrar_como_jogar = True
                if event.key == pygame.K_ESCAPE:
                    mostrar_como_jogar = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mostrar_como_jogar:
                    panel_h = 470
                    btn_fechar_rect = pygame.Rect(
                        LARGURA // 2 - 75,
                        (ALTURA - panel_h) // 2 + panel_h - 52,
                        150,
                        42
                    )
                    if btn_fechar_rect.collidepoint(mouse):
                        mostrar_como_jogar = False
                else:
                    if btn_como_jogar.collidepoint(mouse):
                        mostrar_como_jogar = True

        window.blit(img_fundo, (0, 0))

        if pygame.time.get_ticks() % 1000 < 500:
            texto = fonte.render("ESPAÇO para começar", True, (255, 255, 255))
            rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20))
            sombra = fonte.render("ESPAÇO para começar", True, (0, 0, 0))
            window.blit(sombra, (rect.x + 2, rect.y + 2))
            window.blit(texto, rect)

        desenhar_botao(window, btn_como_jogar, "Como Jogar", "H",
                       btn_como_jogar.collidepoint(mouse))

        if mostrar_como_jogar:
            desenhar_painel_como_jogar()

        pygame.display.update()
        clock_menu.tick(30)

def tela_game_over(score: int) -> str:
    clock_go = pygame.time.Clock()
    btn_w, btn_h = 170, 58
    btn_retry = pygame.Rect(LARGURA // 2 - btn_w - 15, ALTURA // 2 + 65, btn_w, btn_h)
    btn_menu = pygame.Rect(LARGURA // 2 + 15, ALTURA // 2 + 65, btn_w, btn_h)

    texto_score = fonte.render(f"Pontuação: {score}", True, (255, 220, 50))
    sombra_score = fonte.render(f"Pontuação: {score}", True, (0, 0, 0))

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "retry"
                if event.key == pygame.K_m:
                    return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_retry.collidepoint(mouse):
                    return "retry"
                if btn_menu.collidepoint(mouse):
                    return "menu"

        window.blit(img_fundo_fim, (0, 0))

        sr = texto_score.get_rect(center=(LARGURA // 2, ALTURA // 2 + 15))
        window.blit(sombra_score, (sr.x + 2, sr.y + 2))
        window.blit(texto_score, sr)

        desenhar_botao(window, btn_retry, "RETRY", "R",
                       btn_retry.collidepoint(mouse),
                       cor_hover=(20, 140, 20))
        desenhar_botao(window, btn_menu, "MENU", "M",
                       btn_menu.collidepoint(mouse),
                       cor_hover=(140, 40, 10))

        pygame.display.update()
        clock_go.tick(30)

# ----------------------------------------------------
# HUD dos power-ups
# ----------------------------------------------------

def desenhar_hud_status(bx: int, by: int, icon, restante_ms: int, total_ms: int,
                        texto: str, cor_barra, cor_borda=(255, 220, 80)):
    frac = max(0.0, restante_ms / total_ms)

    bw, bh = 130, 18
    window.blit(icon, (bx - 40, by - 8))

    pygame.draw.rect(window, (30, 30, 60), (bx, by, bw, bh), border_radius=5)
    pygame.draw.rect(window, cor_barra, (bx, by, int(bw * frac), bh), border_radius=5)
    pygame.draw.rect(window, cor_borda, (bx, by, bw, bh), 2, border_radius=5)

    t = fonte_kbd.render(texto, True, (255, 255, 255))
    window.blit(t, t.get_rect(center=(bx + bw // 2, by + bh // 2)))

def desenhar_hud_escudo(restante_ms: int):
    secs = max(0, restante_ms // 1000 + 1)
    cor = (80, 220, 255) if restante_ms > 3000 else (255, 160, 30)
    desenhar_hud_status(
        LARGURA - 130 - 10, 10,
        img_powerup_escudo,
        restante_ms,
        POWERUP_ESCUDO_DURACAO_MS,
        f"ESCUDO {secs}s",
        cor
    )

def desenhar_hud_xp2(restante_ms: int):
    secs = max(0, restante_ms // 1000 + 1)
    cor = (255, 210, 80) if restante_ms > 3000 else (255, 160, 30)
    desenhar_hud_status(
        LARGURA - 130 - 10, 38,
        img_powerup_xp2,
        restante_ms,
        POWERUP_XP2_DURACAO_MS,
        f"XP x2 {secs}s",
        cor
    )

# ----------------------------------------------------
# Loop principal
# ----------------------------------------------------

def iniciar_jogo() -> str:
    resetar_mundo()

    player_linha = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    player_wx = float((LARGURA // TAMANHO_TILE // 2) * TAMANHO_TILE)
    player_wy = float(player_linha * TAMANHO_TILE)
    camera_y = player_wy - PLAYER_ALVO_Y
    camera_ativa = False
    imagem = img_baixo
    clock = pygame.time.Clock()
    score = 0

    powerups = []
    linhas_com_powerup = set()

    imune_ate = 0
    xp2_ate = 0

    while True:
        clock.tick(30)
        agora = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_wy -= TAMANHO_TILE
                    imagem = img_cima
                    camera_ativa = True
                    if agora < xp2_ate:
                        score += 2
                    else:
                        score += 1

                if event.key == pygame.K_s:
                    player_wy += TAMANHO_TILE
                    imagem = img_baixo

                if event.key == pygame.K_a:
                    player_wx -= TAMANHO_TILE
                    imagem = img_esquerda

                if event.key == pygame.K_d:
                    player_wx += TAMANHO_TILE
                    imagem = img_direita

        target_cam = player_wy - PLAYER_ALVO_Y

        if camera_ativa:
            if target_cam < camera_y:
                diff = camera_y - target_cam
                passo = max(1.0, diff * 0.18)
                camera_y -= passo
                if camera_y < target_cam:
                    camera_y = target_cam

        player_screen_y = player_wy - camera_y
        player_screen_x = int(player_wx)

        if player_screen_y >= ALTURA or player_screen_y < -TAMANHO_TILE:
            return tela_game_over(score)

        linha_ini = int(camera_y // TAMANHO_TILE) - 1
        linha_fim = int((camera_y + ALTURA) // TAMANHO_TILE) + 1

        tentar_spawnar_carros(linha_ini, linha_fim, score)
        gerar_powerups_para_linhas(linha_ini, linha_fim, powerups, linhas_com_powerup, score)

        for c in carros_ativos:
            c.update()
        carros_ativos[:] = [c for c in carros_ativos if not c.fora_da_tela()]

        for t in troncos_ativos:
            t.update()
        troncos_ativos[:] = [t for t in troncos_ativos if not t.fora_da_tela()]

        player_linha_atual = int(player_wy // TAMANHO_TILE)
        _, tipo_atual = gerar_tile(player_linha_atual)

        player_rect_mundo = pygame.Rect(
            int(player_wx) + 4,
            int(player_wy) + 4,
            TAMANHO_TILE - 8,
            TAMANHO_TILE - 8,
        )
        player_rect = pygame.Rect(
            player_screen_x + 4,
            int(player_screen_y) + 4,
            TAMANHO_TILE - 8,
            TAMANHO_TILE - 8,
        )

        for pu in powerups:
            if not pu.coletado and player_rect_mundo.colliderect(pu.rect_mundo()):
                pu.coletado = True

                if pu.tipo == "escudo":
                    if agora >= imune_ate:
                        imune_ate = agora + POWERUP_ESCUDO_DURACAO_MS

                elif pu.tipo == "xp2":
                    if agora >= xp2_ate:
                        xp2_ate = agora + POWERUP_XP2_DURACAO_MS

        powerups[:] = [
            p for p in powerups
            if not p.coletado and -TAMANHO_TILE <= p.wy - camera_y <= ALTURA + TAMANHO_TILE
        ]

        if tipo_atual == TIPO_RIO:
            for t in troncos_ativos:
                if t.linha == player_linha_atual and t.rect(camera_y).colliderect(player_rect):
                    player_wx += t.velocidade * t.direcao
                    break

        player_wx = max(0.0, min(float(LARGURA - TAMANHO_TILE), player_wx))
        player_screen_x = int(player_wx)
        player_rect = pygame.Rect(
            player_screen_x + 4,
            int(player_screen_y) + 4,
            TAMANHO_TILE - 8,
            TAMANHO_TILE - 8,
        )

        imune = agora < imune_ate

        morreu = False
        if not imune:
            if tipo_atual == TIPO_ESTRADA:
                for c in carros_ativos:
                    if c.rect(camera_y).colliderect(player_rect):
                        morreu = True
                        break

            elif tipo_atual == TIPO_RIO:
                em_tronco = any(
                    t.linha == player_linha_atual and t.rect(camera_y).colliderect(player_rect)
                    for t in troncos_ativos
                )
                if not em_tronco:
                    morreu = True

        if morreu:
            return tela_game_over(score)

        window.blit(img_fundo, (0, 0))

        for linha in range(linha_ini, linha_fim + 1):
            sy = int(linha * TAMANHO_TILE - camera_y)
            surf, tipo = gerar_tile(linha)
            window.blit(surf, (0, sy))

            if tipo == TIPO_RIO:
                onda = pygame.Surface((LARGURA, TAMANHO_TILE), pygame.SRCALPHA)
                t_off = pygame.time.get_ticks() // 200
                for xi in range((t_off * 3) % 30 - 30, LARGURA, 30):
                    pygame.draw.ellipse(onda, (180, 220, 255, 90), (xi, TAMANHO_TILE // 2 - 3, 18, 6))
                window.blit(onda, (0, sy))

        for pu in powerups:
            pu.draw(window, camera_y)

        for t in troncos_ativos:
            sy = t.screen_y(camera_y)
            if -TAMANHO_TILE <= sy <= ALTURA:
                t.draw(window, camera_y)

        for c in carros_ativos:
            sy = c.screen_y(camera_y)
            if -ALTURA_CARRO <= sy <= ALTURA:
                c.draw(window, camera_y)

        if imune:
            aura = pygame.Surface((TAMANHO_TILE + 16, TAMANHO_TILE + 16), pygame.SRCALPHA)
            pulso = int(120 + 80 * abs((agora % 600) / 300.0 - 1))
            pygame.draw.circle(
                aura,
                (100, 220, 255, pulso),
                (TAMANHO_TILE // 2 + 8, TAMANHO_TILE // 2 + 8),
                TAMANHO_TILE // 2 + 6
            )
            window.blit(aura, (player_screen_x - 8, int(player_screen_y) - 8))

            if (agora // 100) % 2 == 0:
                window.blit(imagem, (player_screen_x, int(player_screen_y)))
        else:
            window.blit(imagem, (player_screen_x, int(player_screen_y)))

        score_texto = fonte_score.render(f"Score: {score}", True, (255, 255, 255))
        score_sombra = fonte_score.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_sombra, (12, 12))
        window.blit(score_texto, (10, 10))

        if imune:
            desenhar_hud_escudo(imune_ate - agora)

        if agora < xp2_ate:
            desenhar_hud_xp2(xp2_ate - agora)

        pygame.display.update()

if __name__ == "__main__":
    tela_inicial()
    while True:
        resultado = iniciar_jogo()
        if resultado == "menu":
            tela_inicial()