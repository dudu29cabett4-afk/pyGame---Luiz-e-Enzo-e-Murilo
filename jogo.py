import os
import pygame
import random
pygame.init()
ALTURA  = 700
LARGURA = 500
window  = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Cruze Quatá!')
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
TAMANHO_TILE  = 48
PLAYER_ALVO_Y = ALTURA * 2 // 3 - 100
def escalar_carro(img):
    nova_altura  = TAMANHO_TILE
    orig_w, orig_h = img.get_size()
    nova_largura = int(orig_w * (nova_altura / orig_h))
    return pygame.transform.scale(img, (nova_largura, nova_altura))
img_cima     = pygame.transform.scale(costas,   (TAMANHO_TILE, TAMANHO_TILE))
img_baixo    = pygame.transform.scale(frente,   (TAMANHO_TILE, TAMANHO_TILE))
img_esquerda = pygame.transform.scale(esquerda, (TAMANHO_TILE, TAMANHO_TILE))
img_direita  = pygame.transform.scale(direita,  (TAMANHO_TILE, TAMANHO_TILE))
img_estrada  = pygame.transform.scale(estrada,  (LARGURA, TAMANHO_TILE))
img_grama    = pygame.transform.scale(grama,    (LARGURA, TAMANHO_TILE))
img_fundo    = pygame.transform.scale(fundo_img,      (LARGURA, ALTURA))
img_fundo_fim= pygame.transform.scale(fundo_fim_img,  (LARGURA, ALTURA))
img_rio = pygame.Surface((LARGURA, TAMANHO_TILE))
img_rio.fill((30, 100, 200))
for i in range(0, LARGURA, 30):
    pygame.draw.ellipse(img_rio, (60, 140, 230), (i, TAMANHO_TILE//2 - 4, 20, 8))
carros_disp_r = [escalar_carro(c) for c in (carro_amarelo, carro_rosa, carro_vermelho, carro_azul, carro_branco, carro_preto)]
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
ALTURA_CARRO  = TAMANHO_TILE
VELOCIDADE_CAMERA = 2
SAFE_ZONE_LINHAS  = 1
fonte       = pygame.font.SysFont("arial", 28, bold=True)
fonte_botao = pygame.font.SysFont("arial", 30, bold=True)
tile_map:      dict = {}
lane_data:     dict = {}
carros_ativos: list = []
troncos_ativos: list = []
TIPO_GRAMA   = "grama"
TIPO_ESTRADA = "estrada"
TIPO_RIO     = "rio"
def resetar_mundo():
    tile_map.clear()
    lane_data.clear()
    carros_ativos.clear()
    troncos_ativos.clear()
def gerar_tile(linha: int):
    if linha not in tile_map:
        linha_base  = int(PLAYER_ALVO_Y // TAMANHO_TILE)
        safe_inicio = linha_base - SAFE_ZONE_LINHAS
        if linha >= safe_inicio:
            tile_map[linha] = (img_grama, TIPO_GRAMA)
        else:
            escolha = random.choices(
                [TIPO_GRAMA, TIPO_ESTRADA, TIPO_RIO], weights=[2, 3, 2]
            )[0]
            if escolha == TIPO_GRAMA:
                tile_map[linha] = (img_grama, TIPO_GRAMA)
            elif escolha == TIPO_ESTRADA:
                tile_map[linha] = (img_estrada, TIPO_ESTRADA)
            else:
                tile_map[linha] = (img_rio, TIPO_RIO)
    return tile_map[linha]
def obter_lane_data(linha: int) -> dict:
    if linha not in lane_data:
        direcao    = 1 if linha % 2 == 0 else -1
        tipo = gerar_tile(linha)[1]
        if tipo == TIPO_RIO:
            velocidade = random.uniform(2.0, 4.5)
            spawn_gap  = random.randint(int(LARGURA * 0.35), int(LARGURA * 0.6))
        else:
            velocidade = random.uniform(4.5, 9.0)
            spawn_gap  = random.randint(int(LARGURA * 0.35), int(LARGURA * 0.65))
        proximo_x  = float(-LARGURA_CARRO) if direcao == 1 else float(LARGURA)
        lane_data[linha] = {
            "direcao":         direcao,
            "velocidade":      velocidade,
            "spawn_gap":       spawn_gap,
            "proximo_spawn_x": proximo_x,
        }
    return lane_data[linha]
class Carro:
    __slots__ = ("linha", "x", "velocidade", "direcao", "img", "largura")
    def __init__(self, linha, x, velocidade, direcao, img):
        self.linha      = linha
        self.x          = x
        self.velocidade = velocidade
        self.direcao    = direcao
        self.img        = img
        self.largura    = img.get_width()
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
            ALTURA_CARRO  - m * 2,
        )
def tentar_spawnar_carros(linha_ini: int, linha_fim: int):
    linha_base  = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    safe_inicio = linha_base - SAFE_ZONE_LINHAS
    for linha in range(linha_ini, linha_fim + 1):
        if linha >= safe_inicio:
            continue
        surf, tipo = gerar_tile(linha)
        if tipo == TIPO_ESTRADA:
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
        elif tipo == TIPO_RIO:
            ld = obter_lane_data(linha)
            d  = ld["direcao"]
            v  = ld["velocidade"]
            ja_existem = [t for t in troncos_ativos if t.linha == linha]
            if not ja_existem:
                img = random.choice(troncos_disp_r if d == 1 else troncos_disp_l)
                x0  = float(-img.get_width()) if d == 1 else float(LARGURA)
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
def tela_game_over() -> str:
    clock_go = pygame.time.Clock()
    btn_w, btn_h = 160, 55
    btn_retry = pygame.Rect(LARGURA // 2 - btn_w - 20, ALTURA // 2 + 60, btn_w, btn_h)
    btn_menu  = pygame.Rect(LARGURA // 2 + 20,          ALTURA // 2 + 60, btn_w, btn_h)
    COR_NORMAL = (30,  30,  30,  190)
    COR_HOVER  = (200, 80,  20,  230)
    COR_TEXTO  = (255, 255, 255)
    COR_BORDA  = (255, 255, 255)
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
        btn_surf.fill(COR_HOVER if btn_retry.collidepoint(mouse) else COR_NORMAL)
        window.blit(btn_surf, btn_retry.topleft)
        pygame.draw.rect(window, COR_BORDA, btn_retry, 2, border_radius=8)
        t = fonte_botao.render("RETRY", True, COR_TEXTO)
        window.blit(t, t.get_rect(center=btn_retry.center))
        btn_surf.fill(COR_HOVER if btn_menu.collidepoint(mouse) else COR_NORMAL)
        window.blit(btn_surf, btn_menu.topleft)
        pygame.draw.rect(window, COR_BORDA, btn_menu, 2, border_radius=8)
        t = fonte_botao.render("MENU", True, COR_TEXTO)
        window.blit(t, t.get_rect(center=btn_menu.center))
        pygame.display.update()
        clock_go.tick(30)
def iniciar_jogo() -> str:
    resetar_mundo()
    player_linha = int(PLAYER_ALVO_Y // TAMANHO_TILE)
    player_wx: float = float((LARGURA // TAMANHO_TILE // 2) * TAMANHO_TILE)
    player_wy: float = float(player_linha * TAMANHO_TILE)
    camera_y:  float = player_wy - PLAYER_ALVO_Y
    camera_ativa = False
    imagem = img_baixo
    clock  = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_wy   -= TAMANHO_TILE
                    imagem       = img_cima
                    camera_ativa = True
                if event.key == pygame.K_s:
                    player_wy  += TAMANHO_TILE
                    imagem      = img_baixo
                if event.key == pygame.K_a:
                    player_wx  -= TAMANHO_TILE
                    imagem      = img_esquerda
                if event.key == pygame.K_d:
                    player_wx  += TAMANHO_TILE
                    imagem      = img_direita
        if camera_ativa:
            camera_y -= VELOCIDADE_CAMERA
        target_cam = player_wy - PLAYER_ALVO_Y
        if camera_y > target_cam:
            camera_y = target_cam
        player_screen_y = player_wy - camera_y
        player_screen_x = int(player_wx)
        if player_screen_y >= ALTURA or player_screen_y < -TAMANHO_TILE:
            return tela_game_over()
        linha_ini = int(camera_y // TAMANHO_TILE) - 1
        linha_fim = int((camera_y + ALTURA) // TAMANHO_TILE) + 1
        tentar_spawnar_carros(linha_ini, linha_fim)
        for c in carros_ativos:
            c.update()
        carros_ativos[:] = [c for c in carros_ativos if not c.fora_da_tela()]
        for t in troncos_ativos:
            t.update()
        troncos_ativos[:] = [t for t in troncos_ativos if not t.fora_da_tela()]
        player_linha_atual = int(player_wy // TAMANHO_TILE)
        tile_atual, tipo_atual = gerar_tile(player_linha_atual)
        player_rect = pygame.Rect(
            player_screen_x + 4,
            int(player_screen_y) + 4,
            TAMANHO_TILE - 8,
            TAMANHO_TILE - 8,
        )
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
        morreu = False
        if tipo_atual == TIPO_ESTRADA:
            for c in carros_ativos:
                if c.rect(camera_y).colliderect(player_rect):
                    morreu = True
                    break
        elif tipo_atual == TIPO_RIO:
            em_tronco = False
            for t in troncos_ativos:
                if t.linha == player_linha_atual and t.rect(camera_y).colliderect(player_rect):
                    em_tronco = True
                    break
            if not em_tronco:
                morreu = True
        if morreu:
            return tela_game_over()
        window.blit(img_fundo, (0, 0))
        for linha in range(linha_ini, linha_fim + 1):
            sy = int(linha * TAMANHO_TILE - camera_y)
            surf, tipo = gerar_tile(linha)
            window.blit(surf, (0, sy))
            if tipo == TIPO_RIO:
                onda = pygame.Surface((LARGURA, TAMANHO_TILE), pygame.SRCALPHA)
                t_off = pygame.time.get_ticks() // 200
                for xi in range((t_off * 3) % 30 - 30, LARGURA, 30):
                    pygame.draw.ellipse(onda, (100, 180, 255, 80), (xi, TAMANHO_TILE//2 - 3, 18, 6))
                window.blit(onda, (0, sy))
        for t in troncos_ativos:
            sy = t.screen_y(camera_y)
            if -TAMANHO_TILE <= sy <= ALTURA:
                t.draw(window, camera_y)
        for c in carros_ativos:
            sy = c.screen_y(camera_y)
            if -ALTURA_CARRO <= sy <= ALTURA:
                c.draw(window, camera_y)
        window.blit(imagem, (player_screen_x, int(player_screen_y)))
        pygame.display.update()
tela_inicial()
while True:
    resultado = iniciar_jogo()
    if resultado == "menu":
        tela_inicial()