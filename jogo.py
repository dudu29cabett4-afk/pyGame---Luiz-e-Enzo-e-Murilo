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
tronco_img_raw = pygame.image.load(os.path.join(base, "pasta_imagens/tronco.png"))

TAMANHO_TILE = 48
PLAYER_ALVO_Y = ALTURA * 2 // 3 - 100

TRONCO_SLOTS_OPCOES = [2, 3]

def escalar_carro(img):
    nova_altura = TAMANHO_TILE
    orig_w, orig_h = img.get_size()
    nova_largura = int(orig_w * (nova_altura / orig_h))
    return pygame.transform.scale(img, (nova_largura, nova_altura))

img_cima      = pygame.transform.scale(costas,   (TAMANHO_TILE, TAMANHO_TILE))
img_baixo     = pygame.transform.scale(frente,   (TAMANHO_TILE, TAMANHO_TILE))
img_esquerda  = pygame.transform.scale(esquerda, (TAMANHO_TILE, TAMANHO_TILE))
img_direita   = pygame.transform.scale(direita,  (TAMANHO_TILE, TAMANHO_TILE))
img_estrada   = pygame.transform.scale(estrada,  (LARGURA, TAMANHO_TILE))
img_grama     = pygame.transform.scale(grama,    (LARGURA, TAMANHO_TILE))
img_fundo     = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))
img_fundo_fim = pygame.transform.scale(fundo_fim_img, (LARGURA, ALTURA))

img_rio = pygame.Surface((LARGURA, TAMANHO_TILE))
img_rio.fill((80, 170, 230))
for i in range(0, LARGURA, 30):
    pygame.draw.ellipse(img_rio, (130, 200, 255), (i, TAMANHO_TILE // 2 - 4, 20, 8))

carros_disp_r = [escalar_carro(c) for c in (
    carro_amarelo, carro_rosa, carro_vermelho, carro_azul, carro_branco, carro_preto
)]
carros_disp_l = [pygame.transform.flip(img, True, False) for img in carros_disp_r]

def fazer_img_tronco(num_slots: int) -> pygame.Surface:
    largura = num_slots * TAMANHO_TILE
    return pygame.transform.scale(tronco_img_raw, (largura, TAMANHO_TILE))

troncos_img = {
    2: fazer_img_tronco(2),
    3: fazer_img_tronco(3),
}
troncos_img_flip = {
    k: pygame.transform.flip(v, True, False) for k, v in troncos_img.items()
}

LARGURA_CARRO = carros_disp_r[0].get_width()
ALTURA_CARRO = TAMANHO_TILE
SAFE_ZONE_LINHAS = 1

VEL_SCROLL_INICIAL = 0.25
VEL_SCROLL_MAX     = 3.0
SCORE_PARA_MAX_VEL = 80

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
arvores_ativas = []
vitorias_ativas = []

TIPO_GRAMA = "grama"
TIPO_ESTRADA = "estrada"
TIPO_RIO = "rio"

# ----------------------------------------------------
# Power-ups
# ----------------------------------------------------

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
    arvores_ativas.clear()
    vitorias_ativas.clear()

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

def linha_tem_rio_vizinho(linha: int) -> bool:
    for d in (-1, 1):
        nl = linha + d
        if nl >= 0 and gerar_tile(nl)[1] == TIPO_RIO:
            return True
    return False

def obter_lane_data(linha: int, score: int = 0) -> dict:
    if linha not in lane_data:
        direcao = 1 if linha % 2 == 0 else -1
        tipo = gerar_tile(linha)[1]
        mult = calcular_multiplicador_velocidade(score)

        if tipo == TIPO_RIO:
            tem_rio_vizinho = linha_tem_rio_vizinho(linha)

            if tem_rio_vizinho and random.random() < 0.35:
                modo_rio = "vitoria_regia"
                velocidade = 0.0
                spawn_gap = 0
                num_slots = 0
            else:
                modo_rio = "troncos"
                velocidade = random.uniform(2.0, 4.5) * mult
                spawn_gap = random.randint(int(LARGURA * 0.35), int(LARGURA * 0.6))
                num_slots = random.choice(TRONCO_SLOTS_OPCOES)
        else:
            modo_rio = None
            velocidade = random.uniform(4.5, 9.0) * mult
            spawn_gap = random.randint(int(LARGURA * 0.35), int(LARGURA * 0.65))
            num_slots = 0

        proximo_x = float(-LARGURA_CARRO) if direcao == 1 else float(LARGURA)
        lane_data[linha] = {
            "direcao": direcao,
            "velocidade": velocidade,
            "spawn_gap": spawn_gap,
            "proximo_spawn_x": proximo_x,
            "num_slots": num_slots,
            "modo_rio": modo_rio,
            "vitorias_cols": [],
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

class Tronco:
    def __init__(self, linha, x, velocidade, direcao, num_slots):
        self.linha = linha
        self.x = float(x)
        self.velocidade = velocidade
        self.direcao = direcao
        self.num_slots = num_slots
        self.largura = num_slots * TAMANHO_TILE

        if direcao == 1:
            self.img = troncos_img[num_slots]
        else:
            self.img = troncos_img_flip[num_slots]

    def update(self):
        self.x += self.velocidade * self.direcao

    def fora_da_tela(self):
        if self.direcao == 1:
            return self.x > LARGURA + self.largura
        return self.x < -self.largura * 2

    def screen_y(self, camera_y):
        return int(self.linha * TAMANHO_TILE - camera_y)

    def draw(self, surface, camera_y):
        sy = self.screen_y(camera_y)
        if -self.largura <= sy <= ALTURA:
            surface.blit(self.img, (int(self.x), sy))

    def rect(self, camera_y):
        m = 4
        return pygame.Rect(
            int(self.x) + m,
            self.screen_y(camera_y) + m,
            self.largura - m * 2,
            TAMANHO_TILE - m * 2,
        )

    def slot_x_mundo(self, slot: int) -> float:
        return self.x + slot * TAMANHO_TILE

    def slot_do_x(self, wx: float) -> int:
        slot = round((wx - self.x) / TAMANHO_TILE)
        return max(0, min(self.num_slots - 1, slot))

class PowerUp:
    TAMANHO = 36

    def __init__(self, wx: float, wy: float, tipo: str):
        self.wx = wx
        self.wy = wy
        self.tipo = tipo
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

class Arvore:
    def __init__(self, linha, wx):
        self.linha = linha
        self.wx = float(wx)
        self.wy = float(linha * TAMANHO_TILE)

    def screen_y(self, camera_y):
        return int(self.wy - camera_y)

    def rect_mundo(self):
        return pygame.Rect(
            int(self.wx) + 6,
            int(self.wy) + 2,
            TAMANHO_TILE - 12,
            TAMANHO_TILE - 2
        )

    def draw(self, surface, camera_y):
        sy = self.screen_y(camera_y)
        if -TAMANHO_TILE <= sy <= ALTURA:
            sx = int(self.wx)

            pygame.draw.circle(surface, (40, 150, 50), (sx + 24, sy + 16), 16)
            pygame.draw.circle(surface, (55, 180, 65), (sx + 16, sy + 18), 13)
            pygame.draw.circle(surface, (35, 120, 40), (sx + 31, sy + 20), 12)
            pygame.draw.rect(surface, (110, 70, 35), (sx + 19, sy + 22, 10, 22), border_radius=3)
            pygame.draw.rect(surface, (80, 50, 25), (sx + 19, sy + 22, 10, 22), 2, border_radius=3)

class VitoriaRegia:
    TAMANHO = 28

    def __init__(self, linha, wx):
        self.linha = linha
        self.wx = float(wx)
        self.wy = float(linha * TAMANHO_TILE + (TAMANHO_TILE - self.TAMANHO) // 2)

    def screen_y(self, camera_y):
        return int(self.wy - camera_y)

    def rect_mundo(self):
        return pygame.Rect(
            int(self.wx),
            int(self.wy),
            self.TAMANHO,
            self.TAMANHO
        )

    def draw(self, surface, camera_y):
        sy = self.screen_y(camera_y)
        if -self.TAMANHO <= sy <= ALTURA:
            sx = int(self.wx)
            pygame.draw.rect(surface, (60, 180, 70), (sx, sy, self.TAMANHO, self.TAMANHO), border_radius=5)
            pygame.draw.rect(surface, (25, 110, 35), (sx, sy, self.TAMANHO, self.TAMANHO), 2, border_radius=5)

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

            if ld.get("modo_rio") == "vitoria_regia":
                continue

            d = ld["direcao"]
            v = ld["velocidade"]
            ns = ld["num_slots"]
            largura_t = ns * TAMANHO_TILE
            ja_existem = [t for t in troncos_ativos if t.linha == linha]

            if not ja_existem:
                x0 = float(-largura_t) if d == 1 else float(LARGURA)
                troncos_ativos.append(Tronco(linha, x0, v, d, ns))
                ld["proximo_spawn_x"] = x0 + d * ld["spawn_gap"]
            else:
                ultimo = max(ja_existem, key=lambda c: c.x * d)

                if d == 1 and ultimo.x >= ld["proximo_spawn_x"]:
                    troncos_ativos.append(Tronco(linha, float(-largura_t), v, d, ns))
                    ld["proximo_spawn_x"] += ld["spawn_gap"]
                elif d == -1 and ultimo.x <= ld["proximo_spawn_x"]:
                    troncos_ativos.append(Tronco(linha, float(LARGURA), v, d, ns))
                    ld["proximo_spawn_x"] -= ld["spawn_gap"]

def gerar_arvores_para_linhas(linha_ini: int, linha_fim: int, score: int = 0):
    linha_base = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    safe_inicio = linha_base - SAFE_ZONE_LINHAS

    for linha in range(linha_ini, linha_fim + 1):
        if linha >= safe_inicio:
            continue

        _, tipo = gerar_tile(linha)
        if tipo != TIPO_GRAMA:
            continue

        if any(a.linha == linha for a in arvores_ativas):
            continue

        chance_arvore = 0.08 + min(score / 12000.0, 0.04)
        if random.random() < chance_arvore:
            col = random.randint(1, (LARGURA // TAMANHO_TILE) - 2)
            wx = float(col * TAMANHO_TILE)
            arvores_ativas.append(Arvore(linha, wx))

def gerar_vitorias_regias_para_linhas(linha_ini: int, linha_fim: int, score: int = 0):
    linha_base = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    safe_inicio = linha_base - SAFE_ZONE_LINHAS

    for linha in range(linha_ini, linha_fim + 1):
        if linha >= safe_inicio:
            continue

        _, tipo = gerar_tile(linha)
        if tipo != TIPO_RIO:
            continue

        ld = obter_lane_data(linha, score)
        if ld.get("modo_rio") != "vitoria_regia":
            continue

        if "vitorias_cols" not in ld:
            total_cols = (LARGURA // TAMANHO_TILE)
            qtd = random.randint(2, 4)
            ld["vitorias_cols"] = sorted(random.sample(range(1, total_cols - 1), qtd))

        for col in ld["vitorias_cols"]:
            wx = float(col * TAMANHO_TILE + (TAMANHO_TILE - VitoriaRegia.TAMANHO) // 2)

            if not any(v.linha == linha and abs(v.wx - wx) < 1 for v in vitorias_ativas):
                vitorias_ativas.append(VitoriaRegia(linha, wx))

def gerar_powerups_para_linhas(linha_ini, linha_fim, powerups: list, linhas_com_powerup: set, score: int):
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
            col_total = LARGURA // TAMANHO_TILE
            colunas_livres = [
                c for c in range(1, col_total - 1)
                if not any(
                    arv.linha == linha and int(arv.wx // TAMANHO_TILE) == c
                    for arv in arvores_ativas
                )
            ]

            if not colunas_livres:
                continue

            col = random.choice(colunas_livres)
            wx = float(col * TAMANHO_TILE)
            wy = float(linha * TAMANHO_TILE + (TAMANHO_TILE - PowerUp.TAMANHO) // 2)
            powerups.append(PowerUp(wx, wy, tipo_powerup))
            linhas_com_powerup.add(linha)

def colide_com_arvore(rect_mundo):
    return any(arv.rect_mundo().colliderect(rect_mundo) for arv in arvores_ativas)

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

    painel_w, painel_h = 430, 490
    painel_x = (LARGURA - painel_w) // 2
    painel_y = (ALTURA - painel_h) // 2

    painel = pygame.Surface((painel_w, painel_h), pygame.SRCALPHA)
    painel.fill((15, 18, 42, 230))
    pygame.draw.rect(painel, (255, 200, 50), (0, 0, painel_w, painel_h), 3, border_radius=14)
    window.blit(painel, (painel_x, painel_y))

    titulo = fonte_botao.render("COMO JOGAR", True, (255, 210, 50))
    window.blit(titulo, titulo.get_rect(center=(LARGURA // 2, painel_y + 30)))

    pygame.draw.line(
        window, (255, 200, 50),
        (painel_x + 20, painel_y + 50),
        (painel_x + painel_w - 20, painel_y + 50), 1
    )

    secoes = [
        ("MOVIMENTAÇÃO", [
            ("W", "Andar para cima  (+1 ponto)"),
            ("S", "Andar para baixo"),
            ("A", "Andar para esquerda"),
            ("D", "Andar para direita"),
        ]),
        ("CÂMERA", [
            (">>", "Câmera começa parada no início"),
            (">>", "Ao mover, ela rola sozinha para cima"),
            (">>", "Fique pra trás = morte!"),
            (">>", "Quanto mais pontos, mais rápida!"),
        ]),
        ("OBSTÁCULOS", [
            ("!!", "Desvie dos carros na estrada!"),
            ("~~", "Atravesse rios em cima de troncos!"),
            ("A/D", "Mude de slot no tronco (cuidado!)"),
            ("XX", "Cair na água = morte!"),
            ("##", "Árvore = parede, não deixa passar."),
        ]),
        ("POWER-UPS", [
            ("★", "Escudo dourado: absorve 1 golpe fatal."),
            ("x2", "Moeda dourada: vale 2 pontos por 8s."),
        ]),
    ]

    BTN_H      = 42
    BTN_MARGIN = 12
    y_ini  = painel_y + 60
    y_max  = painel_y + painel_h - BTN_H - BTN_MARGIN - 8

    HDR_H  = 21
    ITEM_H = 20
    SEC_GAP = 7

    total_linhas = sum(HDR_H + len(itens) * ITEM_H for _, itens in secoes)
    total_gaps   = SEC_GAP * (len(secoes) - 1)
    total_h      = total_linhas + total_gaps
    espaco       = y_max - y_ini
    extra        = max(0, (espaco - total_h) // max(1, len(secoes) - 1))

    y_cur = y_ini
    for idx, (titulo_sec, itens) in enumerate(secoes):
        hdr = fonte_hud.render(titulo_sec, True, (255, 180, 40))
        window.blit(hdr, (painel_x + 18, y_cur))
        y_cur += HDR_H

        for icone, texto in itens:
            ic = fonte_titulo.render(icone, True, (130, 200, 255))
            window.blit(ic, (painel_x + 22, y_cur))
            tx = fonte_titulo.render(texto, True, (210, 225, 255))
            window.blit(tx, (painel_x + 52, y_cur))
            y_cur += ITEM_H

        if idx < len(secoes) - 1:
            y_cur += SEC_GAP + extra

    btn_fechar = pygame.Rect(LARGURA // 2 - 75, painel_y + painel_h - BTN_H - BTN_MARGIN, 150, BTN_H)
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
                    panel_h = 490
                    btn_fechar_rect = pygame.Rect(
                        LARGURA // 2 - 75,
                        (ALTURA - panel_h) // 2 + panel_h - 42 - 12,
                        150, 42
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

def desenhar_hud_escudo():
    bx = LARGURA - 130 - 10
    by = 10
    bw, bh = 130, 18
    window.blit(img_powerup_escudo, (bx - 40, by - 8))
    pygame.draw.rect(window, (60, 30, 10), (bx, by, bw, bh), border_radius=5)
    pygame.draw.rect(window, (255, 210, 50), (bx, by, bw, bh), border_radius=5)
    pygame.draw.rect(window, (255, 240, 120), (bx, by, bw, bh), 2, border_radius=5)
    t = fonte_kbd.render("ESCUDO ATIVO", True, (60, 30, 0))
    window.blit(t, t.get_rect(center=(bx + bw // 2, by + bh // 2)))

def desenhar_hud_xp2(restante_ms: int):
    secs = max(0, restante_ms // 1000 + 1)
    desenhar_hud_status(
        LARGURA - 130 - 10, 38,
        img_powerup_xp2,
        restante_ms, POWERUP_XP2_DURACAO_MS,
        f"XP x2 {secs}s", (255, 210, 80)
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

    tem_escudo = False
    graca_ate  = 0
    xp2_ate = 0

    tronco_atual = None
    slot_atual = 0

    while True:
        clock.tick(30)
        agora = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    novo_wy = player_wy - TAMANHO_TILE
                    teste_rect = pygame.Rect(
                        int(player_wx) + 4, int(novo_wy) + 4,
                        TAMANHO_TILE - 8, TAMANHO_TILE - 8
                    )

                    if not colide_com_arvore(teste_rect):
                        tronco_atual = None
                        player_wy = novo_wy
                        imagem = img_cima
                        camera_ativa = True
                        if agora < xp2_ate:
                            score += 2
                        else:
                            score += 1

                elif event.key == pygame.K_s:
                    novo_wy = player_wy + TAMANHO_TILE
                    teste_rect = pygame.Rect(
                        int(player_wx) + 4, int(novo_wy) + 4,
                        TAMANHO_TILE - 8, TAMANHO_TILE - 8
                    )

                    if not colide_com_arvore(teste_rect):
                        tronco_atual = None
                        player_wy = novo_wy
                        imagem = img_baixo

                elif event.key == pygame.K_a:
                    imagem = img_esquerda
                    if tronco_atual is not None:
                        novo_slot = slot_atual - 1
                        if novo_slot < 0:
                            tronco_atual = None
                        else:
                            slot_atual = novo_slot
                    else:
                        novo_wx = player_wx - TAMANHO_TILE
                        teste_rect = pygame.Rect(
                            int(novo_wx) + 4, int(player_wy) + 4,
                            TAMANHO_TILE - 8, TAMANHO_TILE - 8
                        )
                        if not colide_com_arvore(teste_rect):
                            player_wx = novo_wx

                elif event.key == pygame.K_d:
                    imagem = img_direita
                    if tronco_atual is not None:
                        novo_slot = slot_atual + 1
                        if novo_slot >= tronco_atual.num_slots:
                            tronco_atual = None
                        else:
                            slot_atual = novo_slot
                    else:
                        novo_wx = player_wx + TAMANHO_TILE
                        teste_rect = pygame.Rect(
                            int(novo_wx) + 4, int(player_wy) + 4,
                            TAMANHO_TILE - 8, TAMANHO_TILE - 8
                        )
                        if not colide_com_arvore(teste_rect):
                            player_wx = novo_wx

        vel_scroll = VEL_SCROLL_INICIAL + (VEL_SCROLL_MAX - VEL_SCROLL_INICIAL) * min(
            score / SCORE_PARA_MAX_VEL, 1.0
        )

        if camera_ativa:
            camera_y -= vel_scroll

        target_cam = player_wy - PLAYER_ALVO_Y
        if camera_y > target_cam:
            diff = camera_y - target_cam
            passo = max(vel_scroll + 1.0, diff * 0.22)
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
        gerar_arvores_para_linhas(linha_ini, linha_fim, score)
        gerar_vitorias_regias_para_linhas(linha_ini, linha_fim, score)
        gerar_powerups_para_linhas(linha_ini, linha_fim, powerups, linhas_com_powerup, score)

        for c in carros_ativos:
            c.update()
        carros_ativos[:] = [c for c in carros_ativos if not c.fora_da_tela()]

        for t in troncos_ativos:
            t.update()
        troncos_ativos[:] = [t for t in troncos_ativos if not t.fora_da_tela()]

        arvores_ativas[:] = [
            a for a in arvores_ativas
            if -TAMANHO_TILE <= a.screen_y(camera_y) <= ALTURA + TAMANHO_TILE
        ]

        vitorias_ativas[:] = [
            v for v in vitorias_ativas
            if -TAMANHO_TILE <= v.screen_y(camera_y) <= ALTURA + TAMANHO_TILE
        ]

        if tronco_atual is not None and tronco_atual not in troncos_ativos:
            tronco_atual = None

        player_linha_atual = int(player_wy // TAMANHO_TILE)
        _, tipo_atual = gerar_tile(player_linha_atual)

        if tipo_atual == TIPO_RIO:
            if tronco_atual is not None:
                player_wx = tronco_atual.slot_x_mundo(slot_atual)
                player_wx = max(0.0, min(float(LARGURA - TAMANHO_TILE), player_wx))
            else:
                troncos_da_linha = [t for t in troncos_ativos if t.linha == player_linha_atual]
                for t in troncos_da_linha:
                    if t.x <= player_wx < t.x + t.largura:
                        tronco_atual = t
                        slot_atual = t.slot_do_x(player_wx)
                        player_wx = t.slot_x_mundo(slot_atual)
                        break
        else:
            tronco_atual = None

        player_wx = max(0.0, min(float(LARGURA - TAMANHO_TILE), player_wx))
        player_screen_x = int(player_wx)

        player_rect_mundo = pygame.Rect(
            int(player_wx) + 4, int(player_wy) + 4,
            TAMANHO_TILE - 8, TAMANHO_TILE - 8,
        )
        player_rect = pygame.Rect(
            player_screen_x + 4, int(player_screen_y) + 4,
            TAMANHO_TILE - 8, TAMANHO_TILE - 8,
        )

        for pu in powerups:
            if not pu.coletado and player_rect_mundo.colliderect(pu.rect_mundo()):
                pu.coletado = True
                if pu.tipo == "escudo":
                    tem_escudo = True
                elif pu.tipo == "xp2":
                    if agora >= xp2_ate:
                        xp2_ate = agora + POWERUP_XP2_DURACAO_MS

        powerups[:] = [
            p for p in powerups
            if not p.coletado and -TAMANHO_TILE <= p.wy - camera_y <= ALTURA + TAMANHO_TILE
        ]

        morreu = False

        def checa_morte_real():
            nonlocal morreu
            if tipo_atual == TIPO_ESTRADA:
                for c in carros_ativos:
                    if c.rect(camera_y).colliderect(player_rect):
                        morreu = True
                        return
            elif tipo_atual == TIPO_RIO:
                em_vitoria = any(
                    v.rect_mundo().colliderect(player_rect_mundo)
                    for v in vitorias_ativas
                    if v.linha == player_linha_atual
                )
                if tronco_atual is None and not em_vitoria:
                    morreu = True

        if not tem_escudo and agora >= graca_ate:
            checa_morte_real()
        elif tem_escudo:
            golpe_fatal = False
            if tipo_atual == TIPO_ESTRADA:
                for c in carros_ativos:
                    if c.rect(camera_y).colliderect(player_rect):
                        golpe_fatal = True
                        break
            elif tipo_atual == TIPO_RIO:
                em_vitoria = any(
                    v.rect_mundo().colliderect(player_rect_mundo)
                    for v in vitorias_ativas
                    if v.linha == player_linha_atual
                )
                if tronco_atual is None and not em_vitoria:
                    golpe_fatal = True

            if golpe_fatal:
                tem_escudo = False
                graca_ate = agora + 600

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

        for arv in arvores_ativas:
            arv.draw(window, camera_y)

        for v in vitorias_ativas:
            v.draw(window, camera_y)

        for pu in powerups:
            pu.draw(window, camera_y)

        for t in troncos_ativos:
            t.draw(window, camera_y)

        for c in carros_ativos:
            sy = c.screen_y(camera_y)
            if -ALTURA_CARRO <= sy <= ALTURA:
                c.draw(window, camera_y)

        if tronco_atual is not None and tipo_atual == TIPO_RIO:
            sy_t = tronco_atual.screen_y(camera_y)
            for s in range(tronco_atual.num_slots):
                sx_slot = int(tronco_atual.slot_x_mundo(s))
                cor_slot = (255, 255, 100, 160) if s == slot_atual else (255, 255, 255, 60)
                indicador = pygame.Surface((TAMANHO_TILE - 8, 4), pygame.SRCALPHA)
                indicador.fill(cor_slot)
                window.blit(indicador, (sx_slot + 4, sy_t + TAMANHO_TILE - 6))

        if tem_escudo:
            aura = pygame.Surface((TAMANHO_TILE + 16, TAMANHO_TILE + 16), pygame.SRCALPHA)
            pulso = int(120 + 80 * abs((agora % 600) / 300.0 - 1))
            pygame.draw.circle(
                aura,
                (255, 220, 60, pulso),
                (TAMANHO_TILE // 2 + 8, TAMANHO_TILE // 2 + 8),
                TAMANHO_TILE // 2 + 6
            )
            window.blit(aura, (player_screen_x - 8, int(player_screen_y) - 8))
            window.blit(imagem, (player_screen_x, int(player_screen_y)))
        elif agora < graca_ate:
            if (agora // 80) % 2 == 0:
                window.blit(imagem, (player_screen_x, int(player_screen_y)))
        else:
            window.blit(imagem, (player_screen_x, int(player_screen_y)))

        score_texto = fonte_score.render(f"Score: {score}", True, (255, 255, 255))
        score_sombra = fonte_score.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_sombra, (12, 12))
        window.blit(score_texto, (10, 10))

        if tem_escudo:
            desenhar_hud_escudo()

        if agora < xp2_ate:
            desenhar_hud_xp2(xp2_ate - agora)

        pygame.display.update()

if __name__ == "__main__":
    tela_inicial()
    while True:
        resultado = iniciar_jogo()
        if resultado == "menu":
            tela_inicial()