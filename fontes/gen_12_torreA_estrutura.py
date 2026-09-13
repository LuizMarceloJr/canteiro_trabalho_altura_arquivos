# gen_12_torreA_estrutura.py - estrutura da Torre A (10 pavimentos, pe-direito 3 m)
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB


def slab_holes(mb, x0, y0, x1, y1, z0, z1, holes, c, top=None):
    xs = sorted(set([x0, x1] + [v for h in holes for v in (h[0], h[2]) if x0 < v < x1]))
    ys = sorted(set([y0, y1] + [v for h in holes for v in (h[1], h[3]) if y0 < v < y1]))
    for j in range(len(ys) - 1):
        ya, yb = ys[j], ys[j + 1]
        run = None
        for i in range(len(xs) - 1):
            xa, xb = xs[i], xs[i + 1]
            xm, ym = (xa + xb) / 2, (ya + yb) / 2
            hole = any(h[0] <= xm <= h[2] and h[1] <= ym <= h[3] for h in holes)
            if not hole:
                run = (run[0], xb) if run else (xa, xb)
            elif run:
                mb.box((run[0], ya, z0), (run[1], yb, z1), c, top=top)
                run = None
        if run:
            mb.box((run[0], ya, z0), (run[1], yb, z1), c, top=top)


def build():
    C = K.coll("12_TorreA_Estrutura")
    K.clear_coll(C)
    R = random.Random(11)
    X0, Y0, X1, Y1 = L.TORRE_A
    XL, YL = L.TA_XL, L.TA_YL
    Z = L.TA_Z
    LT = L.TA_LAJE
    VB, VH = L.TA_VIGA
    HOLES = [L.TA_ESCADA_VAO, L.TA_ELEV1, L.TA_ELEV2, L.TA_SHAFT]
    objs = 0
    grp = K.empty("GRP_TorreA", C, (0, 0, 0), size=3.0, props={"categoria": "edificio", "nome": "Torre A", "pavimentos": 10})

    # ---------------- terreo (radier)
    mb = MB()
    mb.box((X0 - 0.3, Y0 - 0.3, -0.05), (X1 + 0.3, Y1 + 0.3, Z(0)), "concreto_claro", sides="concreto", nobottom=True)
    K.finish(mb, "TorreA_Pav00_Radier", C, parent=grp, props={"categoria": "estrutura", "pavimento": 0})

    for n in range(1, 10):
        zt = Z(n)
        zb = Z(n - 1)
        mb = MB()
        # laje com aberturas
        slab_holes(mb, X0, Y0, X1, Y1, zt - LT, zt, HOLES, "concreto", top="concreto_claro")
        # vigas
        for y in YL:
            ya = y if y == Y0 else (y - VB if y == Y1 else y - VB / 2)
            mb.box((X0, ya, zt - VH), (X1, ya + VB, zt - LT), "concreto", nobottom=False, notop=True)
        for x in XL:
            xa = x if x == X0 else (x - VB if x == X1 else x - VB / 2)
            mb.box((xa, Y0, zt - VH), (xa + VB, Y1, zt - LT), "concreto", notop=True)
        # pilares do pavimento de baixo
        for x in XL:
            for y in YL:
                r = L.TA_PILAR(x, y)
                mb.box((r[0], r[1], zb), (r[2], r[3], zt - VH), "concreto_pilar", nobottom=True, notop=True)
        # nucleo: paredes dos pocos de elevador (concreto)
        z0, z1 = zb, zt - LT
        mb.wall(16.4, 21.6, 19.6, 19.75, z0, z1, "concreto", openings=[(17.2, 18.3, z0, z0 + 2.1), (19.75, 20.85, z0, z0 + 2.1)])
        mb.ywall(19.75, 21.85, 16.4, 16.55, z0, z1, "concreto")
        mb.ywall(19.75, 21.85, 18.95, 19.15, z0, z1, "concreto")
        mb.ywall(19.75, 21.85, 21.45, 21.6, z0, z1, "concreto")
        mb.box((16.4, 21.85, z0), (21.6, 22.0, z1), "concreto", nobottom=True, notop=True)
        # escada (dois lances + patamar) entre n-1 e n
        r = PD = L.PE_DIREITO
        rise = PD / 16.0
        xa, xb = 17.75, 19.71
        run = (xb - xa) / 8.0
        for k in range(8):
            mb.box((xa + k * run, 14.15, zb + k * rise), (xb, 15.65, zb + (k + 1) * rise), "concreto_claro", nobottom=(k > 0))
        mb.box((xb, 14.15, zb + 1.5 - 0.14), (21.45, 17.25, zb + 1.5), "concreto_claro")
        for k in range(8):
            mb.box((xa, 15.75, zb + 1.5 + k * rise), (xb - k * run, 17.25, zb + 1.5 + (k + 1) * rise), "concreto_claro", nobottom=(k > 0))
        K.finish(mb, "TorreA_Pav%02d_Estrutura" % n, C, parent=grp, props={"categoria": "estrutura", "pavimento": n, "cota_laje_m": round(zt, 2)})
        objs += 1

    # ---------------- alvenaria de vedacao (pavimentos 0 a 4 completos, 5 parcial)
    def bays(lines):
        return list(zip(lines[:-1], lines[1:]))
    for n in range(0, 6):
        z0 = Z(n)
        z1 = Z(n + 1) - VH
        col = "reboco" if n <= 2 else "bloco_ceramico"
        mb = MB()
        for face in ("S", "N", "W", "E"):
            if n == 5 and face == "W":
                continue
            horizontal = face in ("S", "N")
            lines = XL if horizontal else YL
            for bi, (a, b) in enumerate(bays(lines)):
                if horizontal:
                    ra = L.TA_PILAR(a, Y0 if face == "S" else Y1)
                    rb = L.TA_PILAR(b, Y0 if face == "S" else Y1)
                    wa, wb = ra[2], rb[0]
                else:
                    ra = L.TA_PILAR(X0 if face == "W" else X1, a)
                    rb = L.TA_PILAR(X0 if face == "W" else X1, b)
                    wa, wb = ra[3], rb[1]
                if face == "N" and a >= 16.4 and b <= 21.6:
                    continue
                span = wb - wa
                ops = []
                zt_wall = z1
                if n == 4 and face == "S" and bi in (3, 4):
                    continue    # treinamento: vaos sul 04/05 do pav 4 abertos (GcR)
                if n == 0 and face == "S":
                    ops = [(wa + 0.6, wb - 0.6, z0, z0 + 2.4)]
                elif n == 5 and face == "S":
                    if bi not in (1, 2):
                        continue
                    zt_wall = z0 + 1.2
                elif face == "W" and a == 10.0:
                    ops = [(11.8, 14.2, z0, z0 + 2.1)]
                else:
                    ww = 1.2 if horizontal else 1.4
                    for f in (0.27, 0.73):
                        c = wa + span * f
                        ops.append((c - ww / 2, c + ww / 2, z0 + 1.0, z0 + 2.2))
                if horizontal:
                    yy = Y0 + 0.04 if face == "S" else Y1 - 0.18
                    mb.wall(wa, wb, yy, yy + 0.14, z0, zt_wall, col, openings=ops)
                else:
                    xx = X0 + 0.04 if face == "W" else X1 - 0.18
                    mb.ywall(wa, wb, xx, xx + 0.14, z0, zt_wall, col, openings=ops)
        # paredes da escada (fechamento da caixa) nos pavimentos com alvenaria
        if n <= 4:
            mb.wall(16.4, 21.6, 13.95, 14.1, z0, z1, col)
            mb.ywall(14.1, 17.4, 16.25, 16.4, z0, z1, col, openings=[(L.TR_PORTA_OESTE_NUCLEO[0], L.TR_PORTA_OESTE_NUCLEO[1], z0, z0 + 2.1)])
            mb.ywall(14.1, 17.4, 21.6, 21.75, z0, z1, col)
            mb.wall(16.4, 21.6, 17.4, 17.55, z0, z1, col, openings=[(16.6, 17.6, z0, z0 + 2.1)])
        K.finish(mb, "TorreA_Pav%02d_Alvenaria" % n, C, parent=grp, props={"categoria": "alvenaria", "pavimento": n})

    # paletes de blocos no pavimento 5 (alvenaria em andamento)
    mb = MB()
    for (px, py) in ((12.0, 6.0), (13.4, 6.0), (24.0, 6.2), (27.5, 12.5)):
        z = Z(5)
        mb.box((px, py, z), (px + 1.1, py + 1.1, z + 0.12), "pallet")
        mb.box((px + 0.05, py + 0.05, z + 0.12), (px + 1.05, py + 1.05, z + 0.95), "bloco_ceramico", top="argamassa")
    mb.box((15.0, 8.0, Z(5)), (15.6, 8.6, Z(5) + 0.35), "cinza_escuro")
    K.finish(mb, "TorreA_Pav05_Paletes_Blocos", C, parent=grp, props={"categoria": "material"})

    # ---------------- escoramento remanescente (pav 8 sob a laje 9; reescoramento no pav 7)
    for n, step in ((8, 1.5), (7, 3.0)):
        mb = MB()
        z0 = Z(n)
        z1 = Z(n + 1) - LT
        x = X0 + 0.9
        while x < X1 - 0.5:
            y = Y0 + 0.9
            while y < Y1 - 0.5:
                inside = any(h[0] - 0.3 <= x <= h[2] + 0.3 and h[1] - 0.3 <= y <= h[3] + 0.3 for h in [(16.3, 13.9, 21.7, 22.1), L.TA_SHAFT])
                near_col = any(abs(x - cx) < 0.5 and abs(y - cy) < 0.6 for cx in XL for cy in YL)
                if not inside and not near_col:
                    mb.box((x - 0.07, y - 0.07, z0), (x + 0.07, y + 0.07, z0 + 0.01), "grafite", nobottom=True)
                    mb.strut((x, y, z0), (x, y, z1 - 0.12), 0.05, "aco")
                    mb.box((x - 0.1, y - 0.04, z1 - 0.12), (x + 0.1, y + 0.04, z1), "amarelo_escuro")
                y += step
            x += step
        K.finish(mb, "TorreA_Pav%02d_Escoramento" % n, C, parent=grp, props={"categoria": "escoramento", "pavimento": n})

    # ---------------- frente de trabalho no pavimento 9 (topo)
    z9 = Z(9)
    formados, armaduras = MB(), MB()
    for x in XL:
        for y in YL:
            r = L.TA_PILAR(x, y)
            if x == X0 or (x == 11.2 and y in (Y0, Y1)):
                m = armaduras
                x0, y0, x1, y1 = r[0] + 0.03, r[1] + 0.03, r[2] - 0.03, r[3] - 0.03
                bars = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), ((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)] if (x1 - x0) > (y1 - y0) else [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)]
                for (bx, by) in bars:
                    m.box((bx - 0.0125, by - 0.0125, z9), (bx + 0.0125, by + 0.0125, z9 + 3.4), "vergalhao", nobottom=True)
                zz = z9 + 0.15
                while zz < z9 + 3.2:
                    m.ring_box(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zz, zz + 0.012, 0.012, "vergalhao")
                    zz += 0.3
            else:
                m = formados
                e = 0.04
                m.box((r[0] - e, r[1] - e, z9), (r[2] + e, r[3] + e, z9 + 2.5), "forma_resinada", top="madeira_escura", nobottom=True)
                for hz in (0.25, 0.9, 1.55, 2.2):
                    m.ring_box(r[0] - e - 0.05, r[1] - e - 0.05, r[2] + e + 0.05, r[3] + e + 0.05, z9 + hz, z9 + hz + 0.09, 0.07, "madeira_escura")
                cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
                for (dx, dy) in ((1.0, 0.0), (0.0, 1.0)):
                    sx = -1 if x == X1 else 1
                    sy = -1 if y == Y1 else 1
                    m.strut((cx + dx * 0.1 * sx, cy + dy * 0.1 * sy, z9 + 1.9), (cx + dx * 1.6 * sx, cy + dy * 1.6 * sy, z9 + 0.02), 0.04, "aco")
                ix0, iy0, ix1, iy1 = r[0] + 0.05, r[1] + 0.05, r[2] - 0.05, r[3] - 0.05
                for (bx, by) in ((ix0, iy0), (ix1, iy0), (ix1, iy1), (ix0, iy1)):
                    m.box((bx - 0.0125, by - 0.0125, z9 + 2.5), (bx + 0.0125, by + 0.0125, z9 + 3.35), "vergalhao", nobottom=True)
    K.finish(formados, "TorreA_Pav09_Formas_Pilares", C, parent=grp, props={"categoria": "forma", "pavimento": 9})
    K.finish(armaduras, "TorreA_Pav09_Armaduras_Pilares", C, parent=grp, props={"categoria": "armadura", "pavimento": 9})

    # forma parcial da laje do pavimento 10 (assoalho, barroteamento, escoras)
    fx0, fy0, fx1, fy1 = L.TA_FORMA_L10
    zd = L.TA_Z(10) - LT
    mb = MB()
    colholes = []
    for x in XL:
        for y in YL:
            r = L.TA_PILAR(x, y)
            if fx0 - 0.5 <= x <= fx1 + 0.5 and fy0 - 0.5 <= y <= fy1 + 0.5:
                colholes.append((r[0] - 0.05, r[1] - 0.05, r[2] + 0.05, r[3] + 0.05))
    slab_holes(mb, fx0 + 0.1, fy0, fx1, fy1, zd - 0.02, zd, colholes, "compensado")
    for y in (fy1 - 0.14, fy0 + 0.0):
        mb.box((fx0 + 0.1, y, zd - 0.40), (fx1, y + 0.28, zd), "forma_resinada")
    mb.box((fx1 - 0.28, fy0, zd - 0.40), (fx1, fy1, zd), "forma_resinada")
    mb.box((26.8 - 0.14, fy0, zd - 0.40), (26.8 + 0.14, fy1, zd), "forma_resinada")
    mb.box((fx0 + 0.1, 16.0 - 0.14, zd - 0.40), (fx1, 16.0 + 0.14, zd), "forma_resinada")
    yy = fy0 + 0.3
    while yy < fy1 - 0.2:
        mb.box((fx0 + 0.15, yy - 0.035, zd - 0.14), (fx1 - 0.05, yy + 0.035, zd - 0.02), "madeira")
        yy += 0.6
    xx = fx0 + 0.7
    props_pts = []
    while xx < fx1 - 0.3:
        mb.box((xx - 0.05, fy0 + 0.1, zd - 0.30), (xx + 0.05, fy1 - 0.1, zd - 0.14), "amarelo_escuro")
        yy = fy0 + 0.7
        while yy < fy1 - 0.3:
            near_col = any(abs(xx - cx) < 0.45 and abs(yy - cy) < 0.55 for cx in XL for cy in YL)
            if not near_col:
                props_pts.append((xx, yy))
            yy += 1.2
        xx += 1.2
    for (px, py) in props_pts:
        mb.box((px - 0.07, py - 0.07, z9), (px + 0.07, py + 0.07, z9 + 0.01), "grafite", nobottom=True)
        mb.strut((px, py, z9), (px, py, zd - 0.30), 0.05, "aco")
        mb.box((px - 0.02, py - 0.02, z9 + 1.6), (px + 0.02, py + 0.02, z9 + 1.75), "vermelho_seguranca")
    K.finish(mb, "TorreA_Pav10_Forma_Laje_Parcial", C, parent=grp, props={"categoria": "forma", "pavimento": 10, "escoras": len(props_pts)})

    # armadura (malha) sobre parte do assoalho
    mb = MB()
    zr = zd + 0.04
    x = 26.95
    while x < fx1 - 0.1:
        mb.box((x - 0.005, 16.2, zr), (x + 0.005, fy1 - 0.2, zr + 0.01), "vergalhao", nobottom=True)
        x += 0.15
    y = 16.2
    while y < fy1 - 0.2:
        mb.box((26.95, y - 0.005, zr + 0.01), (fx1 - 0.1, y + 0.005, zr + 0.02), "vergalhao", nobottom=True)
        y += 0.15
    K.finish(mb, "TorreA_Pav10_Armadura_Laje", C, parent=grp, props={"categoria": "armadura", "pavimento": 10})

    # materiais na laje 9
    mb = MB()
    for k in range(10):
        mb.box((9.0, 6.0, z9 + k * 0.05), (11.44, 7.22, z9 + (k + 1) * 0.05 - 0.004), "compensado", sides="forma_resinada")
    for k in range(4):
        for i in range(6):
            mb.box((12.5, 5.0 + i * 0.13, z9 + k * 0.13), (16.5, 5.0 + i * 0.13 + 0.07, z9 + k * 0.13 + 0.12), "madeira")
    for i in range(12):
        mb.strut((8.5, 12.0 + i * 0.07, z9 + 0.04), (11.5, 12.0 + i * 0.07, z9 + 0.04), 0.06, "aco")
    for i in range(3):
        mb.box((23.0 - 0.2, 5.0, z9 + i * 0.1), (23.0 + 5.8, 5.0 + 0.1, z9 + i * 0.1 + 0.08), "vergalhao")
        mb.box((23.0 - 0.2, 5.3, z9 + i * 0.1), (23.0 + 5.8, 5.3 + 0.1, z9 + i * 0.1 + 0.08), "vergalhao")
    for bx in (23.5, 28.0):
        mb.box((bx, 4.9, z9), (bx + 0.1, 5.6, z9 + 0.08), "madeira_escura")
    mb.box((13.0, 12.0, z9), (15.0, 12.8, z9 + 0.85), "madeira", top="madeira_clara")
    mb.cyl((14.5, 9.0, z9), (14.5, 9.0, z9 + 0.5), 0.35, "preto_suave", n=10, cap="grafite")
    K.finish(mb, "TorreA_Pav09_Materiais", C, parent=grp, props={"categoria": "material", "pavimento": 9})
    return {"objetos": len(C.objects)}
