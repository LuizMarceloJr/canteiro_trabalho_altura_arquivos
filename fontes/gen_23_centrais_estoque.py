# gen_23_centrais_estoque.py - centrais de armacao e carpintaria, baias de agregados e estoque de materiais
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
V = sys.modules["veiculos"]


def galpao(mb, x0, y0, x1, y1, h0=3.2, h1=3.8, cor_roof="cinza_claro", cor_post="cinza_escuro"):
    nx = max(1, int(round((x1 - x0) / 4.0)))
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        for (y, h) in ((y0, h0), (y1, h1)):
            mb.box((x - 0.08, y - 0.08, 0.0), (x + 0.08, y + 0.08, h), cor_post, nobottom=True)
        mb.strut((x, y0, h0 - 0.1), (x, y1, h1 - 0.1), 0.1, cor_post, h=0.18)
    mb.hull([(x0 - 0.4, y0 - 0.5, h0), (x1 + 0.4, y0 - 0.5, h0), (x0 - 0.4, y1 + 0.5, h1), (x1 + 0.4, y1 + 0.5, h1),
             (x0 - 0.4, y0 - 0.5, h0 + 0.06), (x1 + 0.4, y0 - 0.5, h0 + 0.06), (x0 - 0.4, y1 + 0.5, h1 + 0.06), (x1 + 0.4, y1 + 0.5, h1 + 0.06)], cor_roof)
    k = x0 - 0.2
    while k < x1 + 0.3:
        mb.hull([(k, y0 - 0.5, h0 + 0.06), (k + 0.08, y0 - 0.5, h0 + 0.06), (k, y1 + 0.5, h1 + 0.06), (k + 0.08, y1 + 0.5, h1 + 0.06),
                 (k, y0 - 0.5, h0 + 0.1), (k + 0.08, y0 - 0.5, h0 + 0.1), (k, y1 + 0.5, h1 + 0.1), (k + 0.08, y1 + 0.5, h1 + 0.1)], cor_roof)
        k += 0.6
    mb.box((x0 - 0.2, y0 - 0.2, 0.0), (x1 + 0.2, y1 + 0.2, 0.1), "concreto", nobottom=True)


def feixe_vergalhao(mb, x0, y, z, comp=12.0, n=3, rng=None):
    for sx in (x0 + 1.0, x0 + comp / 2, x0 + comp - 1.0):
        mb.box((sx - 0.08, y - 0.25, z), (sx + 0.08, y + 0.25 + 0.45 * (n - 1), z + 0.1), "madeira_escura")
    for k in range(n):
        yy = y + k * 0.45
        mb.box((x0, yy - 0.16, z + 0.1), (x0 + comp, yy + 0.16, z + 0.22), "vergalhao")
        for j in range(4):
            by = yy - 0.12 + j * 0.08
            mb.box((x0 - 0.05, by - 0.012, z + 0.22), (x0 + comp + 0.05, by + 0.012, z + 0.245), "ferrugem")
        for tx in (x0 + 2.0, x0 + comp - 2.0):
            mb.box((tx - 0.02, yy - 0.18, z + 0.1), (tx + 0.02, yy + 0.18, z + 0.25), "cinza_escuro")


def palete_blocos(mb, x, y, rz=0.0, cor="bloco_ceramico", h=0.9):
    with mb.at((x, y, 0.0), rz=rz):
        mb.box((-0.55, -0.55, 0.0), (0.55, 0.55, 0.13), "pallet")
        mb.box((-0.5, -0.5, 0.13), (0.5, 0.5, 0.13 + h), "filme_plastico", top=cor)
        mb.box((-0.51, -0.51, 0.13 + h * 0.35), (0.51, 0.51, 0.13 + h * 0.4), "cinza_escuro")


def palete_cimento(mb, x, y, rz=0.0, lona=False):
    with mb.at((x, y, 0.0), rz=rz):
        mb.box((-0.6, -0.5, 0.0), (0.6, 0.5, 0.13), "pallet")
        if lona:
            mb.rbox((-0.66, -0.56, 0.13), (0.66, 0.56, 1.05), "lona_azul", r=0.12)
        else:
            for k in range(6):
                for i in range(2):
                    for j in range(2):
                        rot = (k % 2 == 0)
                        mb.rbox((-0.58 + i * 0.59, -0.48 + j * 0.49, 0.13 + k * 0.14), (-0.01 + i * 0.59, 0.0 + j * 0.49, 0.26 + k * 0.14), "saco_cimento", r=0.03)
                mb.box((-0.59, -0.49, 0.2 + k * 0.14), (0.59, -0.47, 0.23 + k * 0.14), "saco_faixa")


def tubo_concreto(mb, x, y, z, comp=2.5, r=0.55, rz=0.0):
    with mb.at((x, y, z), rz=rz):
        mb.cyl((-comp / 2, 0, 0), (comp / 2, 0, 0), r, "tubo_concreto", n=12, caps=False)
        mb.cyl((-comp / 2, 0, 0), (comp / 2, 0, 0), r * 0.8, "concreto_escuro", n=12, caps=False)
        for sx in (-comp / 2, comp / 2):
            sg = 1.0 if sx > 0 else -1.0
            with mb.at((sx, 0, 0), ry=90.0 * sg):
                mb.lathe([(r * 0.8, 0.0), (r, 0.0)], "concreto", n=12, cap0=False, cap1=False, smooth=False)
            mb.cyl((sx - sg * 0.35, 0, 0), (sx - sg * 0.36, 0, 0), r * 0.8, "preto_suave", n=12, cap="preto_suave")


def build():
    C = K.coll("23_Centrais_Estoque_Materiais")
    K.clear_coll(C)
    rng = random.Random(33)
    P = lambda tipo, **kw: dict({"categoria": "material_estoque", "tipo": tipo}, **kw)

    # ---------------- central de armacao
    mb = MB()
    galpao(mb, -38.0, 20.5, -27.0, 27.5)
    mb.box((-37.0, 23.2, 0.1), (-29.0, 24.0, 0.95), "madeira", top="madeira_clara")
    for i in range(16):
        mb.cyl((-36.6 + i * 0.5, 23.6, 0.95), (-36.6 + i * 0.5, 23.6, 1.05), 0.025, "cromado", n=5)
    for k in range(6):
        mb.box((-36.5, 23.3 + k * 0.1, 0.96), (-30.0, 23.33 + k * 0.1, 0.99), "vergalhao")
    mb.box((-28.5, 22.0, 0.1), (-27.6, 22.8, 1.0), "laranja_escuro", top="grafite")
    mb.cyl((-28.05, 22.4, 1.0), (-28.05, 22.4, 1.2), 0.2, "cromado", n=10)
    for k in range(3):
        y = 25.2 + k * 0.7
        for j in range(8):
            x = -37.2 + j * 0.9
            mb.ring_box(x - 0.2, y - 0.15, x + 0.2, y + 0.15, 0.1 + 0.02 * (j % 3), 0.13 + 0.02 * (j % 3), 0.02, "vergalhao")
    for x in (-37.5, -33.0, -28.5):
        mb.box((x - 0.05, 21.0, 0.1), (x + 0.05, 21.2, 1.2), "cinza_escuro")
    mb.box((-37.8, 21.0, 1.1), (-28.2, 21.2, 1.18), "cinza_escuro")
    K.finish(mb, "Central_Armacao_Galpao", C, props=P("central_de_armacao", nr_ref="NR-18 18.10 / NR-12 maquinas de corte e dobra"))
    mb = MB()
    feixe_vergalhao(mb, -38.0, 17.2, 0.0, 12.0, n=4, rng=rng)
    K.finish(mb, "Estoque_Vergalhoes_12m_Feixes", C, props=P("vergalhao_CA50"))

    # ---------------- central de carpintaria (serra circular com coifa)
    mb = MB()
    galpao(mb, -24.0, 20.5, -14.5, 27.5)
    mb.box((-20.5, 23.0, 0.1), (-18.3, 24.1, 0.95), "madeira", top="madeira_clara")
    for (px, py) in ((-20.4, 23.1), (-18.4, 23.1), (-18.4, 24.0), (-20.4, 24.0)):
        mb.box((px - 0.04, py - 0.04, 0.1), (px + 0.04, py + 0.04, 0.9), "grafite")
    mb.cyl((-19.4, 23.5, 0.95), (-19.4, 23.52, 0.95), 0.2, "cromado", n=12)
    mb.box((-19.75, 23.43, 1.05), (-19.05, 23.59, 1.35), "amarelo_maquina")
    mb.box((-19.55, 23.1, 1.3), (-19.25, 23.15, 1.55), "amarelo_maquina")
    mb.box((-20.4, 24.2, 0.1), (-19.6, 24.8, 0.6), "vermelho_seguranca", top="grafite")
    for k in range(12):
        mb.box((-23.5, 21.0, 0.1 + k * 0.05), (-21.06, 22.22, 0.1 + (k + 1) * 0.05 - 0.004), "compensado", sides="forma_resinada")
    for k in range(5):
        for i in range(8):
            mb.box((-17.8, 21.0 + i * 0.13, 0.1 + k * 0.12), (-14.8, 21.07 + i * 0.13, 0.21 + k * 0.12), "madeira")
    for i in range(5):
        x = -23.6 + i * 0.35
        mb.hull([(x, 26.8, 0.1), (x + 0.04, 26.8, 0.1), (x, 27.4, 0.1), (x + 0.04, 27.4, 0.1),
                 (x + 0.25, 26.8, 2.3), (x + 0.29, 26.8, 2.3), (x + 0.25, 27.4, 2.3), (x + 0.29, 27.4, 2.3)], "forma_resinada")
    K.finish(mb, "Central_Carpintaria_Galpao", C, props=P("central_de_carpintaria", nr_ref="NR-18 / NR-12 serra circular com coifa protetora", interativo=True))

    # ---------------- estoque no patio (escoras, andaimes, formas, blocos, cimento, big bags)
    mb = MB()
    for layer in range(3):
        for i in range(8 - layer):
            y = 6.0 + i * 0.11 + layer * 0.055
            mb.cyl((-37.5, y, 0.1 + layer * 0.095), (-34.5, y, 0.1 + layer * 0.095), 0.05, "aco", n=6, cap="grafite")
    for (sx) in (-37.2, -34.8):
        mb.box((sx - 0.08, 5.8, 0.0), (sx + 0.08, 7.0, 0.06), "madeira_escura")
    for k in range(8):
        mb.box((-33.5, 5.9, 0.08 + k * 0.1), (-31.5, 6.9, 0.16 + k * 0.1), "azul_andaime")
        mb.box((-33.4, 6.0, 0.16 + k * 0.1), (-31.6, 6.8, 0.18 + k * 0.1), "aco")
    for layer in range(4):
        for i in range(6):
            y = 8.2 + i * 0.12
            mb.cyl((-33.8, y, 0.06 + layer * 0.1), (-30.8, y, 0.06 + layer * 0.1), 0.024, "azul_andaime", n=6, cap="grafite")
    for k in range(14):
        mb.box((-37.5, 9.0, 0.05 + k * 0.08), (-35.0, 10.2, 0.12 + k * 0.08), "forma_resinada", sides="madeira_escura")
    K.finish(mb, "Estoque_Escoras_Andaimes_Formas", C, props=P("escoras_andaimes_formas"))
    mb = MB()
    for i in range(4):
        for j in range(2):
            palete_blocos(mb, -29.5 + i * 1.3, 13.2 + j * 1.3, rz=rng.uniform(-4, 4))
    for i in range(3):
        palete_blocos(mb, -24.2 + i * 1.3, 14.5, rz=rng.uniform(-4, 4), cor="tijolo", h=0.75)
    for i in range(3):
        palete_cimento(mb, -29.0 + i * 1.4, 9.5, lona=(i == 2))
    for i in range(3):
        with mb.at((-24.6 + i * 1.25, 10.5, 0.0)):
            mb.rbox((-0.5, -0.5, 0.0), (0.5, 0.5, 0.95), "big_bag", r=0.15)
            mb.blob((0.0, 0.0, 0.95), 0.42, "areia", sub=1, noise=0.1, rng=rng, squash=(1.0, 1.0, 0.3))
            for (lx, ly) in ((-0.4, -0.4), (0.4, 0.4)):
                mb.strut((lx, ly, 0.9), (lx * 0.6, ly * 0.6, 1.25), 0.05, "big_bag", h=0.02)
    K.finish(mb, "Estoque_Paletes_Blocos_Cimento_BigBags", C, props=P("paletes_blocos_cimento_areia"))

    # conteineres maritimos junto ao Bloco B
    g22 = sys.modules["gen_22"]
    for (nm, loc, rz, cor, z0) in (("01_Vermelho", (-36.5, -10.8, 0.0), 0.0, "vermelho_caminhao", 0.0), ("02_Verde_Empilhado", (-36.5, -10.8, 0.0), 0.0, "verde_escuro", 2.59),
                                   ("03_Laranja", (-36.5, -7.4, 0.0), 0.0, "laranja_caminhao", 0.0)):
        mb = MB()
        g22.container(mb, Lc=6.06, W=2.44, H=2.59, cor=cor, trim=cor, doors=[("E", 0.0, 2.3)], z0=z0, marit=True)
        K.finish(mb, "Estoque_Conteiner_Maritimo_" + nm, C, loc=loc, rz=rz, props=P("conteiner_maritimo_deposito"))

    # tubos de concreto (pilhas) junto a cava
    mb = MB()
    for stack, (bx, by) in enumerate(((13.5, -23.4), (17.2, -23.4))):
        for layer, nrow in enumerate((3, 2, 1)):
            for i in range(nrow):
                yy = by - (nrow - 1) * 0.56 + i * 1.12
                tubo_concreto(mb, bx, yy, 0.55 + layer * 0.95, comp=2.5, r=0.55, rz=0.0)
        for yy in (by - 1.4, by + 1.4):
            mb.box((bx - 1.0, yy - 0.08, 0.0), (bx + 1.0, yy + 0.08, 0.3), "madeira_escura")
    K.finish(mb, "Estoque_Tubos_Concreto_Pilhas", C, props=P("tubos_de_concreto", nr_ref="NR-18 - pilhas calcadas a distancia da borda da cava"))

    # baias de agregados + betoneira
    mb = MB()
    bx0, bx1, by0, by1 = -39.5, -32.2, -26.0, -18.0
    mb.box((bx0, by0, 0.0), (bx1, by1, 0.1), "concreto", nobottom=True)
    for y in (by0, (by0 + by1) / 2, by1):
        mb.box((bx0, y - 0.1, 0.1), (bx1 - 2.0, y + 0.1, 1.3), "concreto_escuro", top="concreto")
    mb.box((bx0, by0, 0.1), (bx0 + 0.2, by1, 1.3), "concreto_escuro", top="concreto")
    mb.blob((-37.0, -24.0, 0.1), 2.0, "areia", sub=2, noise=0.12, rng=rng, squash=(1.3, 0.85, 0.55))
    mb.blob((-37.0, -20.0, 0.1), 1.9, "brita", sub=2, noise=0.15, rng=rng, squash=(1.3, 0.85, 0.5))
    K.finish(mb, "Central_Baias_Areia_Brita", C, props=P("baias_de_agregados"))
    K.finish(V.betoneira if False else _betoneira_pequena(), "Central_Betoneira_400L", C, loc=(-33.3, -21.8, 0.0), rz=90.0,
             props=P("betoneira_400L", nr_ref="NR-12 / NR-18"))
    mb = MB()
    palete_cimento(mb, -33.6, -24.8, lona=False)
    K.finish(mb, "Central_Palete_Cimento_Betoneira", C, props=P("cimento"))

    # carreteis de cabo e quadro eletrico perto da portaria
    mb = MB()
    for (x, y, r) in ((25.6, -25.2, 0.55), (26.6, -25.6, 0.45)):
        with mb.at((x, y, r), rz=20):
            mb.cyl((0, -0.35, 0), (0, -0.3, 0), r, "madeira", n=12)
            mb.cyl((0, 0.3, 0), (0, 0.35, 0), r, "madeira", n=12)
            mb.cyl((0, -0.3, 0), (0, 0.3, 0), r * 0.7, "preto_suave", n=12, caps=False)
    mb.box((27.5, -26.6, 0.0), (27.62, -26.48, 1.9), "grafite", nobottom=True)
    mb.box((27.0, -26.48, 0.9), (28.1, -26.2, 1.9), "cinza_claro", top="grafite")
    mb.box((27.1, -26.2, 1.05), (28.0, -26.18, 1.8), "amarelo_linha_vida")
    K.finish(mb, "Central_Quadro_Eletrico_QGD_Carreteis", C, props=P("quadro_eletrico_QGD", nr_ref="NR-10 / NR-18 instalacoes eletricas", interativo=True))
    return {"objetos": len(C.objects)}


def _betoneira_pequena():
    mb = MB()
    mb.box((-0.6, -0.4, 0.0), (0.6, 0.4, 0.1), "amarelo_escuro")
    for sx in (-0.5, 0.5):
        mb.cyl((sx, -0.46, 0.25), (sx, -0.36, 0.25), 0.25, "pneu", n=10)
    mb.box((-0.12, -0.12, 0.1), (0.12, 0.12, 0.9), "amarelo_maquina")
    mb.box((-0.55, 0.2, 0.3), (-0.2, 0.45, 0.75), "grafite")
    with mb.at((0.15, 0.0, 1.2), ry=-35.0):
        mb.lathe([(0.22, -0.55), (0.52, -0.3), (0.55, 0.08), (0.4, 0.42), (0.25, 0.55)], "amarelo_maquina", n=12, cap0=True, cap1="grafite")
    mb.cyl((-0.1, -0.5, 1.0), (-0.1, -0.9, 1.3), 0.02, "grafite", n=5)
    return mb
