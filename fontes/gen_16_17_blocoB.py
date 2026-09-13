# gen_16_17_blocoB.py - Bloco B (2 lajes executadas, pilares do 3o pavimento em execucao)
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
g12 = sys.modules["gen_12"]
g13 = sys.modules["gen_13"]


def build():
    CS = K.coll("16_BlocoB_Estrutura")
    CP = K.coll("17_BlocoB_Protecoes")
    K.clear_coll(CS)
    K.clear_coll(CP)
    R = random.Random(5)
    X0, Y0, X1, Y1 = L.BLOCO_B
    XL = [X0, X0 + (X1 - X0) / 3, X0 + 2 * (X1 - X0) / 3, X1]
    YL = [Y0, (Y0 + Y1) / 2, Y1]
    PD = 3.0
    LT, VB, VH = 0.12, 0.2, 0.45

    def Z(n):
        return 0.15 + PD * n

    def pilar(x, y):
        w, d = 0.3, 0.3
        cx = min(max(x, X0 + w / 2), X1 - w / 2)
        cy = min(max(y, Y0 + d / 2), Y1 - d / 2)
        return (cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2)

    grp = K.empty("GRP_BlocoB", CS, (0, 0, 0), size=2.0, props={"categoria": "edificio", "nome": "Bloco B", "pavimentos_executados": 2})
    mb = MB()
    mb.box((X0 - 0.3, Y0 - 0.3, -0.05), (X1 + 0.3, Y1 + 0.3, Z(0)), "concreto_claro", sides="concreto", nobottom=True)
    K.finish(mb, "BlocoB_Pav00_Radier", CS, parent=grp, props={"categoria": "estrutura", "pavimento": 0})
    HOLE = (-19.0, -6.2, -16.6, -3.2)
    for n in (1, 2):
        zt, zb = Z(n), Z(n - 1)
        mb = MB()
        g12.slab_holes(mb, X0, Y0, X1, Y1, zt - LT, zt, [HOLE] if n == 2 else [], "concreto", top="concreto_claro")
        for y in YL:
            ya = y if y == Y0 else (y - VB if y == Y1 else y - VB / 2)
            mb.box((X0, ya, zt - VH), (X1, ya + VB, zt - LT), "concreto", notop=True)
        for x in XL:
            xa = x if x == X0 else (x - VB if x == X1 else x - VB / 2)
            mb.box((xa, Y0, zt - VH), (xa + VB, Y1, zt - LT), "concreto", notop=True)
        for x in XL:
            for y in YL:
                r = pilar(x, y)
                mb.box((r[0], r[1], zb), (r[2], r[3], zt - VH), "concreto_pilar", nobottom=True, notop=True)
        K.finish(mb, "BlocoB_Pav%02d_Estrutura" % n, CS, parent=grp, props={"categoria": "estrutura", "pavimento": n, "cota_laje_m": round(zt, 2)})
    # escoramento sob a laje 2
    mb = MB()
    x = X0 + 0.8
    while x < X1 - 0.4:
        y = Y0 + 0.8
        while y < Y1 - 0.4:
            if not any(abs(x - cx) < 0.45 and abs(y - cy) < 0.45 for cx in XL for cy in YL):
                mb.box((x - 0.07, y - 0.07, Z(1)), (x + 0.07, y + 0.07, Z(1) + 0.01), "grafite", nobottom=True)
                mb.strut((x, y, Z(1)), (x, y, Z(2) - LT - 0.1), 0.05, "aco")
                mb.box((x - 0.1, y - 0.04, Z(2) - LT - 0.1), (x + 0.1, y + 0.04, Z(2) - LT), "amarelo_escuro")
            y += 1.3
        x += 1.3
    K.finish(mb, "BlocoB_Pav01_Escoramento", CS, parent=grp, props={"categoria": "escoramento", "pavimento": 1})
    # pilares do pav 3: armaduras envoltas e formas (como na referencia)
    z2 = Z(2)
    mf, ma = MB(), MB()
    for i, x in enumerate(XL):
        for j, y in enumerate(YL):
            r = pilar(x, y)
            if (i + j) % 3 == 0:
                e = 0.04
                mf.box((r[0] - e, r[1] - e, z2), (r[2] + e, r[3] + e, z2 + 2.5), "forma_resinada", top="madeira_escura", nobottom=True)
                for hz in (0.3, 1.0, 1.7, 2.35):
                    mf.ring_box(r[0] - e - 0.05, r[1] - e - 0.05, r[2] + e + 0.05, r[3] + e + 0.05, z2 + hz, z2 + hz + 0.08, 0.07, "madeira_escura")
                for (bx, by) in ((r[0] + 0.05, r[1] + 0.05), (r[2] - 0.05, r[1] + 0.05), (r[2] - 0.05, r[3] - 0.05), (r[0] + 0.05, r[3] - 0.05)):
                    mf.box((bx - 0.0125, by - 0.0125, z2 + 2.5), (bx + 0.0125, by + 0.0125, z2 + 3.3), "vergalhao", nobottom=True)
            else:
                x0, y0, x1, y1 = r[0] + 0.03, r[1] + 0.03, r[2] - 0.03, r[3] - 0.03
                for (bx, by) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
                    ma.box((bx - 0.0125, by - 0.0125, z2), (bx + 0.0125, by + 0.0125, z2 + 3.3), "vergalhao", nobottom=True)
                zz = z2 + 0.15
                while zz < z2 + 3.1:
                    ma.ring_box(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zz, zz + 0.012, 0.012, "vergalhao")
                    zz += 0.25
                ma.box((r[0] - 0.02, r[1] - 0.02, z2), (r[2] + 0.02, r[3] + 0.02, z2 + 0.4), "laranja_escuro", nobottom=True)
    K.finish(mf, "BlocoB_Pav02_Formas_Pilares", CS, parent=grp, props={"categoria": "forma", "pavimento": 2})
    K.finish(ma, "BlocoB_Pav02_Armaduras_Pilares", CS, parent=grp, props={"categoria": "armadura", "pavimento": 2})
    # materiais sobre a laje 2
    mb = MB()
    for (px, py) in ((-29.5, -12.8), (-28.2, -12.8), (-29.5, -11.5)):
        mb.box((px, py, z2), (px + 1.1, py + 1.1, z2 + 0.12), "pallet")
        mb.box((px + 0.04, py + 0.04, z2 + 0.12), (px + 1.06, py + 1.06, z2 + 1.0), "filme_plastico", top="bloco_ceramico")
    for k in range(4):
        for i in range(3):
            mb.rbox((-24.6 + i * 0.52, -12.9, z2 + 0.12 + k * 0.14), (-24.1 + i * 0.52, -12.2, z2 + 0.25 + k * 0.14), "saco_cimento", r=0.03)
    mb.box((-24.7, -13.0, z2), (-23.0, -12.0, z2 + 0.12), "pallet")
    for i in range(8):
        mb.box((-21.5, -12.8 + i * 0.09, z2), (-17.5, -12.8 + i * 0.09 + 0.06, z2 + 0.06), "vergalhao")
    for k in range(5):
        mb.box((-27.0, -5.0, z2 + k * 0.05), (-24.56, -3.78, z2 + (k + 1) * 0.05 - 0.004), "compensado", sides="forma_resinada")
    # betoneira pequena
    bx, by = -22.5, -4.2
    mb.box((bx - 0.5, by - 0.35, z2), (bx + 0.5, by + 0.35, z2 + 0.08), "amarelo_escuro")
    for sx in (-0.45, 0.45):
        mb.cyl((bx + sx, by - 0.38, z2 + 0.18), (bx + sx, by - 0.30, z2 + 0.18), 0.18, "pneu", n=8)
    mb.box((bx - 0.1, by - 0.1, z2 + 0.08), (bx + 0.1, by + 0.1, z2 + 0.75), "amarelo_maquina")
    with mb.at((bx + 0.15, by, z2 + 1.0), ry=-35.0):
        mb.lathe([(0.18, -0.45), (0.42, -0.25), (0.45, 0.05), (0.32, 0.35), (0.2, 0.45)], "amarelo_maquina", n=10, cap0=True, cap1="grafite")
    K.finish(mb, "BlocoB_Pav02_Materiais_Betoneira", CS, parent=grp, props={"categoria": "material", "pavimento": 2})

    # ---------------- protecoes
    gp = K.empty("GRP_BlocoB_Protecoes", CP, (0, 0, 0), size=2.0, props={"categoria": "protecao_coletiva"})
    NOMES = {"S": "Sul", "N": "Norte", "W": "Oeste", "E": "Leste"}
    n_obj = 0
    tower_x = (-22.5, -19.5)
    for n in (1, 2):
        z0 = Z(n)
        for face in ("S", "N", "W", "E"):
            if face in ("S", "N"):
                y = Y0 if face == "S" else Y1
                inward = (0.0, 1.0) if face == "S" else (0.0, -1.0)
                for i, (a, b) in enumerate(zip(XL[:-1], XL[1:])):
                    ra, rb = pilar(a, y), pilar(b, y)
                    s0, s1 = ra[2] + 0.02, rb[0] - 0.02
                    pieces = [(s0, s1)]
                    if face == "S" and s0 < tower_x[0] + 1.0 < s1:
                        pieces = [(s0, tower_x[0] + 0.3), (tower_x[1] - 0.3, s1)]
                    for pi, (p0, p1) in enumerate(pieces):
                        mb = MB()
                        g13.gcr(mb, (p0, y), (p1, y), z0, inward)
                        K.finish(mb, "BlocoB_Pav%02d_GcR_%s_%02d%s" % (n, NOMES[face], i + 1, "ab"[pi] if len(pieces) > 1 else ""), CP, parent=gp,
                                 props={"categoria": "protecao_coletiva", "tipo": "GcR_guarda_corpo_rodape", "pavimento": n, "face": NOMES[face],
                                        "nr_ref": "NR-18 18.9.4.2"})
                        n_obj += 1
            else:
                x = X0 if face == "W" else X1
                inward = (1.0, 0.0) if face == "W" else (-1.0, 0.0)
                for i, (a, b) in enumerate(zip(YL[:-1], YL[1:])):
                    ra, rb = pilar(x, a), pilar(x, b)
                    s0, s1 = ra[3] + 0.02, rb[1] - 0.02
                    pieces = [(s0, s1)]
                    if face == "E" and n == 1 and s0 < -5.5 < s1:
                        pieces = [(s0, -6.1), (-4.9, s1)]
                    for pi, (p0, p1) in enumerate(pieces):
                        mb = MB()
                        g13.gcr(mb, (x, p0), (x, p1), z0, inward)
                        K.finish(mb, "BlocoB_Pav%02d_GcR_%s_%02d%s" % (n, NOMES[face], i + 1, "ab"[pi] if len(pieces) > 1 else ""), CP, parent=gp,
                                 props={"categoria": "protecao_coletiva", "tipo": "GcR_guarda_corpo_rodape", "pavimento": n, "face": NOMES[face],
                                        "nr_ref": "NR-18 18.9.4.2"})
                        n_obj += 1
    # abertura na laje 2 (passagem de material) com GcR
    mb = MB()
    hx0, hy0, hx1, hy1 = HOLE
    for (a, b, inw) in (((hx0 - 0.1, hy0), (hx1 + 0.1, hy0), (0, -1)), ((hx1, hy0 - 0.1), (hx1, hy1 + 0.1), (1, 0)),
                        ((hx1 + 0.1, hy1), (hx0 - 0.1, hy1), (0, 1)), ((hx0, hy1 + 0.1), (hx0, hy0 - 0.1), (-1, 0))):
        g13.gcr(mb, a, b, Z(2), inw, clamp=False)
    K.finish(mb, "BlocoB_Pav02_GcR_Abertura_Laje", CP, parent=gp,
             props={"categoria": "protecao_coletiva", "tipo": "GcR_abertura_piso", "pavimento": 2, "nr_ref": "NR-18 18.9.2"})

    # torre de acesso (andaime-escada) na fachada sul
    tx0, tx1 = tower_x
    ty0, ty1 = Y0 - 2.9, Y0 - 0.25
    mb = MB()
    HT = 8.0
    for (px, py) in ((tx0, ty0), (tx1, ty0), (tx1, ty1), (tx0, ty1)):
        mb.box((px - 0.1, py - 0.1, 0.0), (px + 0.1, py + 0.1, 0.02), "grafite", nobottom=True)
        mb.cyl((px, py, 0.02), (px, py, HT + 1.2), 0.03, "laranja_seguranca", n=6, caps=False)
    for k in range(1, 5):
        z = 2.0 * k
        for (a, b) in (((tx0, ty0), (tx1, ty0)), ((tx1, ty0), (tx1, ty1)), ((tx1, ty1), (tx0, ty1)), ((tx0, ty1), (tx0, ty0))):
            mb.cyl((a[0], a[1], z - 0.05), (b[0], b[1], z - 0.05), 0.025, "laranja_seguranca", n=6, caps=False)
        mb.box((tx0 + 0.03, ty0 + 0.03, z - 0.05), (tx1 - 0.03, ty0 + 0.8, z), "aco", sides="cinza_medio")
        mb.box((tx0 + 0.03, ty1 - 0.8, z - 0.05), (tx1 - 0.03, ty1 - 0.03, z), "aco", sides="cinza_medio")
        for (a, b) in (((tx0, ty0), (tx1, ty0)), ((tx0, ty0), (tx0, ty1)), ((tx1, ty0), (tx1, ty1))):
            for hz in (0.7, 1.2):
                mb.cyl((a[0], a[1], z + hz), (b[0], b[1], z + hz), 0.022, "laranja_seguranca", n=6, caps=False)
    zprev = 0.0
    for k in range(1, 5):
        z = 2.0 * k
        if k % 2:
            mb.box((tx0 + 0.15, ty0 + 0.8, zprev), (tx1 - 0.15, ty1 - 0.8, zprev + 0.05), "cinza_medio")
        steps = 10
        for s in range(steps):
            u = s / steps
            yy = (ty0 + 0.8) + (ty1 - 0.8 - (ty0 + 0.8)) * (u if k % 2 else 1 - u)
            mb.box((tx0 + 0.2, yy - 0.12, zprev + (z - zprev) * u), (tx0 + 1.4, yy + 0.12, zprev + (z - zprev) * (u + 1 / steps)), "aco")
        zprev = z
    for (xs, ys) in ((tx0 - 0.02, (ty0, ty1)), (tx1 + 0.02, (ty0, ty1))):
        mb.box((xs - 0.015, ys[0], 0.3), (xs + 0.015, ys[1], 1.8), "lona_azul")
        mb.box((xs - 0.015, ys[0], 4.3), (xs + 0.015, ys[1], 5.8), "lona_azul")
    mb.box((tx0, ty0 - 0.02, 2.3), (tx1, ty0 + 0.01, 3.8), "lona_azul")
    for n in (1, 2):
        zb = Z(n)
        mb.box((tx0 + 0.3, ty1, zb - 0.06), (tx1 - 0.3, Y0 + 0.3, zb), "madeira", sides="madeira_escura")
    K.finish(mb, "BlocoB_Torre_Acesso_Escada", CP, parent=gp, props={"categoria": "andaime", "tipo": "torre_de_acesso_com_escada",
                                                                    "nr_ref": "NR-18 18.8 / 18.12", "interativo": True})
    # escada de mao (face leste, pav 1): ultrapassa 1 m, amarrada no topo, ~75 graus
    mb = MB()
    top = (X1 - 0.05, -5.5, Z(1) + 1.05)
    ang = math.radians(75.0)
    run = (Z(1) + 1.05) / math.tan(ang)
    bot = (X1 + run, -5.5, 0.0)
    for dy in (-0.22, 0.22):
        mb.strut((bot[0], bot[1] + dy, bot[2]), (top[0], top[1] + dy, top[2]), 0.05, "amarelo_maquina", h=0.08, up=(1, 0, 0))
    Lh = math.dist(bot, top)
    nr = int(Lh / 0.3)
    for j in range(1, nr):
        u = j / nr
        p = (bot[0] + (top[0] - bot[0]) * u, -5.5, bot[2] + (top[2] - bot[2]) * u)
        mb.cyl((p[0], -5.72, p[2]), (p[0], -5.28, p[2]), 0.018, "cinza_escuro", n=5, caps=False)
    for dy in (-0.22, 0.22):
        mb.box((bot[0] - 0.08, -5.5 + dy - 0.05, 0.0), (bot[0] + 0.08, -5.5 + dy + 0.05, 0.05), "borracha")
    mb.cyl((X1 + 0.05, -5.8, Z(1) + 0.15), (X1 + 0.05, -5.2, Z(1) + 0.15), 0.015, "amarelo_linha_vida", n=5)
    K.finish(mb, "BlocoB_Escada_Mao_Acesso_Pav01", CP, parent=gp,
             props={"categoria": "acesso", "tipo": "escada_de_mao", "comprimento_m": round(Lh, 2), "angulo_graus": 75,
                    "ultrapassa_piso_m": 1.05, "nr_ref": "NR-18 18.8.6.13 (<= 7 m, ultrapassar 1 m)", "interativo": True})
    return {"estrutura": len(CS.objects), "protecoes": len(CP.objects)}
