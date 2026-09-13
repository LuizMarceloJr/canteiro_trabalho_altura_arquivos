# veiculos.py - biblioteca de veiculos e maquinas low-poly (frente = +X, origem no chao, centro)
import bpy, sys, math, random
K = sys.modules["sitekit"]
MB = K.MB


def roda(mb, x, y, zc, r=0.5, w=0.32, c_pneu="pneu", c_aro="aro", n=10):
    mb.cyl((x, y - w / 2, zc), (x, y + w / 2, zc), r, c_pneu, n=n, cap=c_pneu)
    s = 1 if y >= 0 else -1
    yo = y + s * w / 2
    mb.cyl((x, yo, zc), (x, yo + s * 0.025, zc), r * 0.55, c_aro, n=n)
    mb.cyl((x, yo + s * 0.025, zc), (x, yo + s * 0.05, zc), r * 0.18, "grafite", n=6)


def cabine_caminhao(mb, xr, xf, hw, z0, z1, cor, beacon=False):
    h = z1 - z0
    zm = z0 + h * 0.55
    mb.hull([(xr, -hw, z0), (xf, -hw, z0), (xf, hw, z0), (xr, hw, z0),
             (xr, -hw, z1), (xf - 0.38, -hw + 0.04, z1), (xf - 0.38, hw - 0.04, z1), (xr, hw, z1),
             (xf, -hw, zm), (xf, hw, zm)], cor)
    t = 0.03
    mb.hull([(xf + 0.005, -hw + 0.12, zm + 0.06), (xf + 0.005, hw - 0.12, zm + 0.06),
             (xf - 0.35, hw - 0.14, z1 - 0.08), (xf - 0.35, -hw + 0.14, z1 - 0.08),
             (xf + 0.005 + t, -hw + 0.12, zm + 0.06), (xf + 0.005 + t, hw - 0.12, zm + 0.06),
             (xf - 0.35 + t, hw - 0.14, z1 - 0.08 + t * 0.4), (xf - 0.35 + t, -hw + 0.14, z1 - 0.08 + t * 0.4)], "g:vidro_veiculo")
    for s in (-1, 1):
        y = s * (hw + 0.012)
        mb.box((xr + 0.25, y - 0.012, zm + 0.08), (xf - 0.55, y + 0.012, z1 - 0.15), "g:vidro_veiculo")
        mb.box((xf - 0.2, s * (hw + 0.05), zm + 0.1), (xf - 0.1, s * (hw + 0.32), zm + 0.12), "grafite")
        mb.box((xf - 0.2, s * (hw + 0.28), zm - 0.05), (xf - 0.14, s * (hw + 0.36), zm + 0.45), "grafite")
        mb.box((xf - 0.02, s * (hw - 0.45) - 0.18, z0 + 0.45), (xf + 0.03, s * (hw - 0.45) + 0.18, z0 + 0.7), "farol")
    mb.box((xf - 0.06, -hw - 0.02, z0 - 0.15), (xf + 0.14, hw + 0.02, z0 + 0.25), "grafite")
    mb.box((xf - 0.01, -0.65, z0 + 0.35), (xf + 0.02, 0.65, z0 + 0.95), "grafite")
    mb.box((xr + 0.1, -hw + 0.1, z1), (xr + 0.9, hw - 0.1, z1 + 0.12), cor)
    if beacon:
        mb.box((xr + 0.35, -0.15, z1 + 0.12), (xr + 0.6, 0.15, z1 + 0.3), "e:orelhao_laranja")


def betoneira(cor_cab="branco", listra=("verde_betoneira", "branco")):
    mb = MB()
    mb.box((-4.2, -0.55, 0.75), (3.0, 0.55, 1.05), "grafite")
    for x in (2.75, -1.55, -2.95):
        for y in (-1.02, 1.02):
            roda(mb, x, y, 0.52, 0.52, 0.36)
    for x0, x1 in ((2.2, 3.3), (-3.6, -0.9)):
        for s in (-1, 1):
            mb.box((x0, s * 0.82, 1.05), (x1, s * 1.25, 1.12), "grafite")
    cabine_caminhao(mb, 2.25, 4.25, 1.2, 0.95, 3.05, cor_cab, beacon=True)
    mb.cyl((1.85, -0.7, 2.1), (1.85, 0.7, 2.1), 0.42, "branco", n=10)
    mb.box((1.15, -0.75, 1.05), (1.55, 0.75, 2.2), "grafite")
    mb.box((-3.75, -0.85, 1.05), (-3.35, 0.85, 2.85), "grafite")
    prof = [(0.3, 0.0), (0.85, 0.45), (1.18, 1.4), (1.2, 2.6), (1.05, 3.7), (0.72, 4.7), (0.46, 5.25), (0.44, 5.55)]
    with mb.at((1.35, 0.0, 2.05), ry=-82.5):
        mb.lathe(prof, listra[0], n=12, cap0=listra[1], cap1="grafite",
                 color_fn=lambda k, i: listra[((i + 2 * k) // 3) % 2])
    mb.strut((-4.3, 0.0, 2.2), (-4.95, 0.35, 1.55), 0.38, "grafite", h=0.08)
    for s in (-0.25, 0.25):
        mb.box((-4.35, s - 0.02, 1.05), (-4.31, s + 0.02, 3.2), "cinza_claro")
    for z in (1.3, 1.6, 1.9, 2.2, 2.5, 2.8, 3.1):
        mb.box((-4.35, -0.25, z), (-4.31, 0.25, z + 0.03), "cinza_claro")
    mb.cyl((0.2, 1.15, 0.95), (1.1, 1.15, 0.95), 0.25, "aco", n=8)
    return mb


def basculante(cor="laranja_caminhao", carregado=True, cor_cacamba=None):
    mb = MB()
    cc = cor_cacamba or cor
    mb.box((-4.0, -0.55, 0.75), (3.0, 0.55, 1.05), "grafite")
    for x in (2.8, -1.7, -3.1):
        for y in (-1.02, 1.02):
            roda(mb, x, y, 0.52, 0.52, 0.38)
    cabine_caminhao(mb, 2.3, 4.25, 1.2, 0.95, 3.0, cor, beacon=True)
    xb0, xb1, hw = -4.35, 1.95, 1.22
    zb0, zb1 = 1.2, 2.55
    mb.box((xb0, -hw, zb0), (xb1, hw, zb0 + 0.12), cc)
    mb.box((xb0, -hw, zb0), (xb1, -hw + 0.08, zb1), cc)
    mb.box((xb0, hw - 0.08, zb0), (xb1, hw, zb1), cc)
    mb.box((xb1 - 0.1, -hw, zb0), (xb1, hw, zb1 + 0.45), cc)
    mb.box((xb1 - 0.1, -hw, zb1 + 0.3), (xb1 + 0.35, hw, zb1 + 0.45), cc)
    mb.box((xb0, -hw, zb0), (xb0 + 0.1, hw, zb1 - 0.1), cc)
    for x in (-3.4, -2.2, -1.0, 0.2, 1.3):
        for s in (-1, 1):
            mb.box((x, s * hw - 0.05, zb0 + 0.1), (x + 0.12, s * hw + 0.05, zb1), "grafite")
    mb.box((xb0 - 0.02, -hw - 0.02, zb1 - 0.08), (xb1, -hw + 0.1, zb1), "grafite")
    mb.box((xb0 - 0.02, hw - 0.1, zb1 - 0.08), (xb1, hw + 0.02, zb1), "grafite")
    if carregado:
        mb.blob((-1.2, 0.0, zb1 - 0.35), 1.0, "terra_escura", sub=2, noise=0.1, rng=random.Random(3), squash=(3.0, 1.15, 0.55))
    mb.box((-4.5, -1.1, 0.95), (-4.3, 1.1, 1.12), "grafite")
    for s in (-1, 1):
        mb.box((-4.52, s * 0.95 - 0.12, 1.0), (-4.5, s * 0.95 + 0.12, 1.08), "lanterna")
    return mb


def escavadeira(boom=True):
    mb = MB()
    for s in (-1, 1):
        mb.rbox((-2.35, s * 1.1 - 0.36, 0.0), (2.35, s * 1.1 + 0.36, 0.9), "pneu", r=0.28)
        mb.box((-1.9, s * 1.1 - 0.2, 0.35), (1.9, s * 1.1 + 0.2, 0.92), "grafite")
        for x in (-2.0, 2.0):
            mb.cyl((x, s * 1.1 - 0.38, 0.45), (x, s * 1.1 + 0.38, 0.45), 0.3, "cinza_escuro", n=8)
    mb.cyl((0, 0, 0.9), (0, 0, 1.12), 0.95, "grafite", n=12, smooth=False)
    mb.rbox((-2.2, -1.45, 1.12), (1.0, 1.45, 2.25), "amarelo_maquina", r=0.08)
    mb.rbox((-2.95, -1.45, 1.12), (-2.0, 1.45, 2.15), "amarelo_escuro", r=0.25)
    mb.box((-2.1, -1.0, 2.25), (-0.7, 0.2, 2.45), "grafite")
    mb.cyl((-1.2, -1.1, 2.25), (-1.2, -1.1, 2.95), 0.06, "grafite", n=6)
    mb.rbox((-0.1, 0.3, 2.25), (1.3, 1.42, 3.5), "amarelo_maquina", r=0.06)
    mb.box((1.3, 0.38, 2.45), (1.33, 1.34, 3.38), "g:vidro_veiculo")
    mb.box((0.0, 1.42, 2.55), (1.2, 1.45, 3.35), "g:vidro_veiculo")
    mb.box((-0.05, 0.28, 3.5), (1.35, 1.44, 3.56), "grafite")
    mb.box((0.3, 0.9, 3.56), (0.5, 1.1, 3.72), "e:orelhao_laranja")
    if boom:
        mb.xprism([(0.7, 1.35), (1.45, 1.35), (4.15, 4.2), (4.35, 4.95), (3.8, 5.05), (0.75, 2.2)], -0.62, -0.12, "amarelo_maquina")
        mb.xprism([(3.85, 4.9), (4.4, 4.75), (6.2, 1.55), (5.9, 1.3), (4.9, 3.0)], -0.57, -0.17, "amarelo_maquina")
        mb.cyl((1.3, -0.9, 1.6), (2.55, -0.9, 3.3), 0.12, "grafite", n=8)
        mb.cyl((2.55, -0.9, 3.3), (3.15, -0.9, 4.1), 0.07, "cromado", n=8)
        mb.cyl((1.3, 0.2, 1.6), (2.55, 0.2, 3.3), 0.12, "grafite", n=8)
        mb.cyl((2.55, 0.2, 3.3), (3.15, 0.2, 4.1), 0.07, "cromado", n=8)
        mb.cyl((3.5, -0.37, 5.2), (4.6, -0.37, 4.5), 0.1, "grafite", n=8)
        mb.hull([(5.7, -0.75, 1.55), (6.6, -0.75, 1.25), (6.5, -0.75, 0.35), (5.9, -0.75, 0.55),
                 (5.7, 0.35, 1.55), (6.6, 0.35, 1.25), (6.5, 0.35, 0.35), (5.9, 0.35, 0.55)], "amarelo_escuro")
        for k in range(5):
            y = -0.65 + k * 0.23
            mb.box((6.45, y, 0.22), (6.58, y + 0.1, 0.4), "grafite")
    return mb


def pa_carregadeira():
    mb = MB()
    for x in (1.5, -1.6):
        for y in (-1.05, 1.05):
            roda(mb, x, y, 0.78, 0.78, 0.55, n=12)
    mb.rbox((-3.1, -0.9, 0.7), (-0.4, 0.9, 2.0), "amarelo_maquina", r=0.15)
    mb.rbox((-3.3, -0.95, 0.9), (-2.6, 0.95, 1.8), "amarelo_escuro", r=0.2)
    mb.rbox((0.0, -0.75, 0.6), (2.4, 0.75, 1.5), "amarelo_maquina", r=0.1)
    mb.box((-0.45, -0.3, 0.8), (0.05, 0.3, 1.3), "grafite")
    mb.rbox((-1.5, -0.8, 2.0), (0.0, 0.8, 3.35), "amarelo_maquina", r=0.06)
    mb.box((0.0, -0.7, 2.2), (0.03, 0.7, 3.2), "g:vidro_veiculo")
    for s in (-1, 1):
        mb.box((-1.4, s * 0.81 - 0.01, 2.3), (-0.1, s * 0.81 + 0.01, 3.2), "g:vidro_veiculo")
    mb.box((-1.55, -0.85, 3.35), (0.05, 0.85, 3.42), "grafite")
    mb.cyl((-2.6, 0.5, 2.0), (-2.6, 0.5, 2.6), 0.07, "grafite", n=6)
    for s in (-1, 1):
        mb.strut((1.2, s * 0.6, 1.3), (3.2, s * 0.6, 2.2), 0.22, "amarelo_maquina", h=0.35)
        mb.cyl((1.0, s * 0.35, 1.0), (2.6, s * 0.35, 1.9), 0.09, "cromado", n=8)
    mb.hull([(3.0, -1.35, 1.6), (3.0, 1.35, 1.6), (3.9, -1.35, 1.3), (3.9, 1.35, 1.3), (3.3, -1.35, 2.7), (3.3, 1.35, 2.7), (3.9, -1.35, 2.2), (3.9, 1.35, 2.2)], "amarelo_escuro")
    mb.box((3.85, -1.35, 1.25), (4.05, 1.35, 1.35), "grafite")
    return mb


def mini_carregadeira():
    mb = MB()
    for x in (0.55, -0.55):
        for y in (-0.72, 0.72):
            roda(mb, x, y, 0.36, 0.36, 0.28, n=10)
    mb.rbox((-1.2, -0.58, 0.3), (0.9, 0.58, 1.1), "amarelo_maquina", r=0.08)
    mb.rbox((-1.35, -0.55, 0.35), (-0.9, 0.55, 1.2), "grafite", r=0.1)
    for (x, y) in ((-0.8, -0.55), (0.55, -0.55), (0.55, 0.55), (-0.8, 0.55)):
        mb.box((x - 0.04, y - 0.04, 1.1), (x + 0.04, y + 0.04, 2.0), "grafite")
    mb.box((-0.85, -0.6, 2.0), (0.6, 0.6, 2.06), "amarelo_maquina")
    for s in (-1, 1):
        mb.strut((-0.7, s * 0.66, 1.75), (1.05, s * 0.66, 0.55), 0.1, "amarelo_maquina", h=0.18)
    mb.hull([(1.0, -0.85, 0.05), (1.0, 0.85, 0.05), (1.6, -0.85, 0.05), (1.6, 0.85, 0.05), (1.0, -0.85, 0.75), (1.0, 0.85, 0.75), (1.2, -0.85, 0.75), (1.2, 0.85, 0.75)], "grafite")
    return mb


def rolo_compactador():
    mb = MB()
    mb.cyl((1.6, -1.05, 0.75), (1.6, 1.05, 0.75), 0.75, "cinza_escuro", n=14, cap="amarelo_maquina")
    mb.box((1.0, -1.2, 0.5), (2.3, -1.08, 1.6), "amarelo_maquina")
    mb.box((1.0, 1.08, 0.5), (2.3, 1.2, 1.6), "amarelo_maquina")
    mb.box((1.0, -1.2, 1.5), (2.3, 1.2, 1.62), "amarelo_maquina")
    mb.box((0.35, -0.3, 0.7), (1.05, 0.3, 1.3), "grafite")
    mb.rbox((-2.2, -0.9, 0.7), (0.4, 0.9, 1.9), "amarelo_maquina", r=0.12)
    for y in (-0.95, 0.95):
        roda(mb, -1.5, y, 0.72, 0.72, 0.5, n=12)
    for (x, y) in ((-1.0, -0.75), (0.2, -0.75), (0.2, 0.75), (-1.0, 0.75)):
        mb.box((x - 0.04, y - 0.04, 1.9), (x + 0.04, y + 0.04, 3.0), "grafite")
    mb.box((-1.1, -0.85, 3.0), (0.3, 0.85, 3.08), "amarelo_maquina")
    mb.box((-0.7, -0.3, 1.9), (-0.2, 0.3, 2.3), "grafite")
    return mb


def pta_tesoura(altura=2.6, cor="laranja_seguranca"):
    mb = MB()
    L2, W2 = 1.2, 0.6
    mb.rbox((-L2, -W2, 0.12), (L2, W2, 0.62), cor, r=0.05)
    for x in (-0.85, 0.85):
        for y in (-0.5, 0.5):
            roda(mb, x, y, 0.15, 0.15, 0.12, n=8)
    top = 0.62 + altura - 0.15
    stages = 4
    dz = (top - 0.7) / stages
    for s in (-1, 1):
        y = s * 0.52
        for k in range(stages):
            za, zb = 0.7 + k * dz, 0.7 + (k + 1) * dz
            mb.strut((-0.95, y, za), (0.95, y, zb), 0.08, "grafite", h=0.08, up=(0, 1, 0))
            mb.strut((0.95, y, za), (-0.95, y, zb), 0.08, "grafite", h=0.08, up=(0, 1, 0))
    mb.box((-1.25, -0.62, top), (1.25, 0.62, top + 0.1), cor)
    for (a, b) in (((-1.25, -0.62), (1.25, -0.62)), ((1.25, -0.62), (1.25, 0.62)), ((1.25, 0.62), (-1.25, 0.62)), ((-1.25, 0.62), (-1.25, -0.62))):
        for hz in (0.55, 1.1):
            mb.strut((a[0], a[1], top + 0.1 + hz), (b[0], b[1], top + 0.1 + hz), 0.04, "amarelo_linha_vida")
        mb.strut((a[0], a[1], top + 0.17), (b[0], b[1], top + 0.17), 0.02, "amarelo_linha_vida", h=0.15)
    for (x, y) in ((-1.25, -0.62), (0, -0.62), (1.25, -0.62), (1.25, 0.62), (0, 0.62), (-1.25, 0.62)):
        mb.box((x - 0.025, y - 0.025, top + 0.1), (x + 0.025, y + 0.025, top + 1.22), "amarelo_linha_vida")
    mb.box((0.9, -0.55, top + 0.1), (1.2, -0.3, top + 1.0), "grafite")
    return mb, top + 0.1


def empilhadeira(com_pallet=True):
    mb = MB()
    for x, r in ((0.55, 0.33), (-0.75, 0.28)):
        for y in (-0.52, 0.52):
            roda(mb, x, y, r, r, 0.22, n=10)
    mb.rbox((-1.2, -0.58, 0.25), (0.8, 0.58, 1.05), "amarelo_maquina", r=0.08)
    mb.rbox((-1.35, -0.6, 0.3), (-0.8, 0.6, 1.25), "grafite", r=0.15)
    for (x, y) in ((-0.6, -0.5), (0.45, -0.5), (0.45, 0.5), (-0.6, 0.5)):
        mb.box((x - 0.03, y - 0.03, 1.05), (x + 0.03, y + 0.03, 2.1), "grafite")
    mb.box((-0.65, -0.55, 2.1), (0.5, 0.55, 2.16), "grafite")
    for y in (-0.3, 0.3):
        mb.box((0.85, y - 0.04, 0.1), (0.95, y + 0.04, 2.3), "grafite")
    mb.box((0.95, -0.45, 0.15), (1.05, 0.45, 1.0), "grafite")
    for y in (-0.3, 0.3):
        mb.box((1.05, y - 0.05, 0.15), (2.1, y + 0.05, 0.2), "cinza_escuro")
    if com_pallet:
        mb.box((1.05, -0.55, 0.2), (2.15, 0.55, 0.33), "pallet")
        mb.box((1.1, -0.5, 0.33), (2.1, 0.5, 1.1), "filme_plastico", top="bloco_ceramico")
    return mb


def carrinho_mao(carga=None):
    mb = MB()
    mb.hull([(-0.45, -0.3, 0.35), (0.3, -0.3, 0.35), (-0.45, 0.3, 0.35), (0.3, 0.3, 0.35),
             (-0.6, -0.4, 0.62), (0.5, -0.4, 0.62), (-0.6, 0.4, 0.62), (0.5, 0.4, 0.62)], "verde_escuro")
    mb.cyl((0.55, -0.05, 0.2), (0.55, 0.05, 0.2), 0.2, "pneu", n=8)
    for s in (-1, 1):
        mb.strut((0.55, s * 0.12, 0.2), (-1.0, s * 0.28, 0.55), 0.035, "grafite")
        mb.box((-0.35, s * 0.24 - 0.02, 0.0), (-0.3, s * 0.24 + 0.02, 0.4), "grafite")
    if carga:
        mb.blob((-0.05, 0.0, 0.55), 0.35, carga, sub=1, noise=0.15, rng=random.Random(9), squash=(1.3, 1.0, 0.45))
    return mb


def gerador():
    mb = MB()
    mb.box((-1.3, -0.6, 0.0), (1.3, 0.6, 0.12), "grafite")
    mb.rbox((-1.25, -0.55, 0.12), (1.25, 0.55, 1.45), "verde_escuro", r=0.05)
    for x in (-0.9, -0.6, -0.3):
        mb.box((x, -0.56, 0.5), (x + 0.15, -0.54, 1.2), "grafite")
    mb.cyl((0.8, 0.2, 1.45), (0.8, 0.2, 1.8), 0.06, "grafite", n=6)
    mb.box((0.7, -0.57, 0.8), (1.1, -0.55, 1.2), "cinza_claro")
    return mb


def guindaste_movel(boom_ang=58.0, boom_len=21.0, giro=0.0, patolas=3.2):
    """retorna (mb_chassi, mb_superestrutura_local, info). Superestrutura em coordenadas locais do giro."""
    ch = MB()
    ch.box((-5.8, -1.2, 0.95), (5.2, 1.2, 1.55), "amarelo_maquina", top="grafite")
    for x in (4.0, 2.6, -2.6, -4.0):
        for y in (-1.02, 1.02):
            roda(ch, x, y, 0.62, 0.62, 0.45, n=12)
    cabine_caminhao(ch, 5.2, 6.6, 1.1, 0.9, 2.9, "amarelo_maquina", beacon=True)
    for xo in (3.4, -4.9):
        for s in (-1, 1):
            ch.box((xo - 0.25, s * 1.2, 1.0), (xo + 0.25, s * (1.2 + patolas), 1.4), "grafite")
            ch.box((xo - 0.18, s * (1.0 + patolas) , 0.25), (xo + 0.18, s * (1.35 + patolas), 1.4), "amarelo_escuro")
            ch.cyl((xo, s * (1.18 + patolas), 0.08), (xo, s * (1.18 + patolas), 0.25), 0.35, "grafite", n=10)
            ch.box((xo - 0.7, s * (1.18 + patolas) - 0.7, 0.0), (xo + 0.7, s * (1.18 + patolas) + 0.7, 0.08), "madeira_escura")
    for k in range(4):
        ch.box((-5.9 + k * 0.01, -1.25, 1.2 + k * 0.001), (-5.7, 1.25, 1.35), "zebrado_preto" if k % 2 else "amarelo_linha_vida")
    sup = MB()
    sup.cyl((0, 0, 0.0), (0, 0, 0.25), 1.1, "grafite", n=12, smooth=False)
    sup.rbox((-3.2, -1.15, 0.25), (1.2, 1.15, 1.35), "amarelo_maquina", r=0.08)
    sup.rbox((-3.6, -1.2, 0.3), (-2.4, 1.2, 1.5), "grafite", r=0.1)
    sup.rbox((0.2, 1.2, 0.3), (2.2, 2.1, 2.3), "amarelo_maquina", r=0.08)
    sup.box((2.2, 1.28, 0.9), (2.23, 2.02, 2.1), "g:vidro_veiculo")
    sup.box((0.35, 2.1, 1.1), (2.0, 2.13, 2.1), "g:vidro_veiculo")
    a = math.radians(boom_ang)
    ux, uz = math.cos(a), math.sin(a)
    p0 = (-2.0, 0.0, 1.6)
    secs = [(0.62, 0.78, 0.0, 0.42), (0.52, 0.66, 0.38, 0.72), (0.43, 0.55, 0.68, 1.0)]
    for (hw, hh, f0, f1) in secs:
        sa = (p0[0] + ux * boom_len * f0, 0.0, p0[2] + uz * boom_len * f0)
        sb = (p0[0] + ux * boom_len * f1, 0.0, p0[2] + uz * boom_len * f1)
        sup.strut(sa, sb, hw * 2 * 0.62, "amarelo_maquina", h=hh, up=(0, 1, 0))
    tip = (p0[0] + ux * boom_len, 0.0, p0[2] + uz * boom_len)
    sup.cyl((tip[0], -0.3, tip[2]), (tip[0], 0.3, tip[2]), 0.35, "grafite", n=10)
    sup.cyl((0.0, -0.9, 1.3), (p0[0] + ux * 7.0, -0.9, p0[2] + uz * 7.0 - 0.5), 0.16, "grafite", n=8)
    sup.cyl((0.0, 0.9, 1.3), (p0[0] + ux * 7.0, 0.9, p0[2] + uz * 7.0 - 0.5), 0.16, "grafite", n=8)
    return ch, sup, tip


# ---------------------------------------------------------------- carros de passeio e urbanos
PERFIS = {
    "sedan": dict(L=4.5, W=1.76, r=0.33, body=[(-2.25, 0.32), (2.25, 0.32), (2.3, 0.72), (1.25, 0.9), (0.55, 1.4), (-0.95, 1.43), (-1.85, 1.0), (-2.3, 0.95)],
                  win=[(1.05, 0.93), (0.5, 1.33), (-0.9, 1.36), (-1.7, 0.98)], axles=(1.4, -1.35)),
    "hatch": dict(L=3.9, W=1.7, r=0.31, body=[(-1.95, 0.3), (1.95, 0.3), (2.0, 0.7), (1.05, 0.88), (0.35, 1.42), (-1.55, 1.45), (-1.95, 1.05)],
                  win=[(0.85, 0.92), (0.3, 1.35), (-1.45, 1.38), (-1.8, 1.02)], axles=(1.25, -1.2)),
    "suv": dict(L=4.5, W=1.82, r=0.36, body=[(-2.25, 0.4), (2.25, 0.4), (2.3, 0.9), (1.4, 1.05), (0.8, 1.65), (-2.0, 1.7), (-2.3, 1.2)],
                win=[(1.2, 1.08), (0.72, 1.58), (-1.9, 1.62), (-2.15, 1.15)], axles=(1.45, -1.4)),
    "pickup": dict(L=4.9, W=1.8, r=0.36, body=[(-2.45, 0.42), (2.45, 0.42), (2.5, 0.9), (1.55, 1.05), (1.0, 1.65), (-0.3, 1.68), (-0.45, 1.05), (-2.5, 1.05)],
                   win=[(1.4, 1.08), (0.95, 1.58), (-0.2, 1.6), (-0.3, 1.08)], axles=(1.6, -1.55)),
    "van": dict(L=5.2, W=1.95, r=0.36, body=[(-2.6, 0.4), (2.6, 0.4), (2.65, 1.0), (2.0, 1.25), (1.5, 2.25), (-2.6, 2.3)],
                win=[(1.9, 1.3), (1.45, 2.12), (0.6, 2.15), (0.6, 1.3)], axles=(1.8, -1.7)),
}


def carro(tipo="sedan", cor="carro_branco"):
    p = PERFIS[tipo]
    mb = MB()
    hw = p["W"] / 2
    mb.xprism(p["body"], -hw, hw, cor,
              colfn=lambda i, dx, dz: ("g:vidro_veiculo" if (dx < -0.25 and dz > 0.45) else cor))
    for s in (-1, 1):
        y0, y1 = (hw, hw + 0.012) if s > 0 else (-hw - 0.012, -hw)
        mb.xprism(p["win"], y0, y1, "g:vidro_veiculo")
    xf = max(v[0] for v in p["body"])
    xr = min(v[0] for v in p["body"])
    mb.box((xr - 0.05, -hw + 0.05, 0.28), (xf + 0.06, hw - 0.05, 0.5), "preto_suave")
    for s in (-1, 1):
        mb.box((xf + 0.0, s * (hw - 0.3) - 0.17, 0.58), (xf + 0.04, s * (hw - 0.3) + 0.17, 0.68), "farol")
        mb.box((xr - 0.04, s * (hw - 0.25) - 0.15, 0.7), (xr, s * (hw - 0.25) + 0.15, 0.82), "lanterna")
    for ax in p["axles"]:
        for s in (-1, 1):
            roda(mb, ax, s * (hw - 0.12), p["r"], p["r"], 0.24, n=10)
    if tipo == "pickup":
        mb.box((-2.45, -hw, 1.05), (-0.45, -hw + 0.06, 1.2), cor)
        mb.box((-2.45, hw - 0.06, 1.05), (-0.45, hw, 1.2), cor)
        mb.box((-2.45, -hw, 1.05), (-2.39, hw, 1.2), cor)
    return mb


def onibus(cor="carro_azul", faixa="branco"):
    mb = MB()
    L2, hw = 6.0, 1.27
    mb.rbox((-L2, -hw, 0.35), (L2, hw, 3.1), cor, r=0.12, top="branco")
    for s in (-1, 1):
        y = s * (hw + 0.012)
        mb.box((-L2 + 0.6, min(y, y - s * 0.02), 1.3), (L2 - 1.5, max(y, y - s * 0.02), 2.55), "g:vidro_veiculo")
        mb.box((-L2 + 0.3, min(y, y - s * 0.03), 0.55), (L2 - 0.3, max(y, y - s * 0.03), 0.85), faixa)
    mb.box((L2, -hw + 0.1, 1.0), (L2 + 0.02, hw - 0.1, 2.8), "g:vidro_veiculo")
    mb.box((L2 - 1.3, -hw - 0.02, 0.45), (L2 - 0.5, -hw - 0.01, 2.6), "g:vidro_escuro")
    mb.box((L2 + 0.0, -0.9, 2.85), (L2 + 0.03, 0.9, 3.05), "e:sinal_amarelo")
    for ax in (4.2, -3.2):
        for s in (-1, 1):
            roda(mb, ax, s * (hw - 0.15), 0.5, 0.5, 0.3, n=10)
    return mb


def caminhao_prancha(cor="azul_escuro", carga="vergalhao"):
    mb = MB()
    mb.box((-4.4, -0.55, 0.75), (3.0, 0.55, 1.05), "grafite")
    for x in (2.8, -2.0, -3.4):
        for y in (-1.02, 1.02):
            roda(mb, x, y, 0.5, 0.5, 0.36)
    cabine_caminhao(mb, 2.3, 4.25, 1.2, 0.95, 3.0, cor)
    mb.box((-4.6, -1.25, 1.1), (2.0, 1.25, 1.3), "madeira_escura", sides="grafite")
    if carga == "vergalhao":
        for k in range(3):
            mb.box((-4.5, -0.9 + k * 0.62, 1.3), (1.9, -0.45 + k * 0.62, 1.55), "vergalhao")
        for x in (-3.5, -1.2, 1.0):
            mb.box((x - 0.03, -1.25, 1.3), (x + 0.03, 1.25, 1.6), "amarelo_linha_vida")
    return mb
