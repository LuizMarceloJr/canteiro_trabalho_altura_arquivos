# gen_13_torreA_protecoes.py - protecoes coletivas da Torre A (NR-18 18.9)
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB


def gcr(mb, a, b, z0, inward, off=0.10, screen=True, spacing=1.9, cpost="laranja_escuro", crail="laranja_seguranca",
        ctoe="amarelo_linha_vida", clamp=True):
    """Guarda-corpo e rodape: travessao 1,20 m, intermediario 0,70 m, rodape 0,20 m, tela nos vaos."""
    ax, ay = a
    bx, by = b
    Ls = math.hypot(bx - ax, by - ay)
    if Ls < 0.2:
        return
    ux, uy = (bx - ax) / Ls, (by - ay) / Ls
    nx, ny = inward

    def P(s, o, z):
        return (ax + ux * s + nx * o, ay + uy * s + ny * o, z)
    npost = max(2, int(math.ceil((Ls - 0.12) / spacing)) + 1)
    for i in range(npost):
        s = 0.06 + (Ls - 0.12) * i / (npost - 1)
        mb.strut(P(s, off + 0.025, z0), P(s, off + 0.025, z0 + 1.22), 0.05, cpost)
        if clamp:
            mb.strut(P(s, -0.05, z0 + 0.02), P(s, off + 0.22, z0 + 0.02), 0.07, "grafite", h=0.04)
            mb.strut(P(s, -0.03, z0 - 0.16), P(s, -0.03, z0 + 0.04), 0.07, "grafite", h=0.04, up=(ux, uy, 0))
    mb.strut(P(0, off - 0.02, z0 + 1.15), P(Ls, off - 0.02, z0 + 1.15), 0.04, crail, h=0.10)
    mb.strut(P(0, off - 0.02, z0 + 0.70), P(Ls, off - 0.02, z0 + 0.70), 0.04, crail, h=0.08)
    mb.strut(P(0, off - 0.015, z0 + 0.10), P(Ls, off - 0.015, z0 + 0.10), 0.025, ctoe, h=0.20)
    if screen:
        o = off - 0.045
        mb.quad_uv([P(0, o, z0 + 0.2), P(Ls, o, z0 + 0.2), P(Ls, o, z0 + 1.1), P(0, o, z0 + 1.1)],
                   [(0, 0), (Ls / 0.2, 0), (Ls / 0.2, 4.5), (0, 4.5)], K.S_TELA_GCR)


def build():
    C = K.coll("13_TorreA_Protecoes")
    K.clear_coll(C)
    X0, Y0, X1, Y1 = L.TORRE_A
    XL, YL = L.TA_XL, L.TA_YL
    Z = L.TA_Z
    grp = K.empty("GRP_TorreA_Protecoes", C, (0, 0, 0), size=2.0, props={"categoria": "protecao_coletiva"})
    count = {"GcR": 0}

    def seg_obj(name, segs, z0, props, screen=True):
        mb = MB()
        for (a, b, inward) in segs:
            gcr(mb, a, b, z0, inward, screen=screen)
        o = K.finish(mb, name, C, parent=grp, props=props)
        count["GcR"] += 1
        return o

    # ---------------- periferia: GcR entre pilares
    def face_bays(face):
        out = []
        if face in ("S", "N"):
            y = Y0 if face == "S" else Y1
            inward = (0.0, 1.0) if face == "S" else (0.0, -1.0)
            for i, (a, b) in enumerate(zip(XL[:-1], XL[1:])):
                ra, rb = L.TA_PILAR(a, y), L.TA_PILAR(b, y)
                out.append((i, (ra[2] + 0.02, y), (rb[0] - 0.02, y), inward))
        else:
            x = X0 if face == "W" else X1
            inward = (1.0, 0.0) if face == "W" else (-1.0, 0.0)
            for i, (a, b) in enumerate(zip(YL[:-1], YL[1:])):
                ra, rb = L.TA_PILAR(x, a), L.TA_PILAR(x, b)
                out.append((i, (x, ra[3] + 0.02), (x, rb[1] - 0.02), inward))
        return out

    NOMES = {"S": "Sul", "N": "Norte", "W": "Oeste", "E": "Leste"}
    elev_y0, elev_y1 = 11.8, 14.2
    for n in range(5, 10):
        z0 = Z(n)
        for face in ("S", "N", "W", "E"):
            if n == 5 and face in ("N", "E"):
                continue
            if face == "E" and n >= 7:
                continue
            for (i, a, b, inward) in face_bays(face):
                if n == 5 and face == "S" and i in (1, 2):
                    continue
                props = {"categoria": "protecao_coletiva", "tipo": "GcR_guarda_corpo_rodape", "pavimento": n,
                         "face": NOMES[face], "nr_ref": "NR-18 18.9.4.2 (1,20 / 0,70 / rodape)"}
                if face == "W" and i == 1:
                    seg_obj("TorreA_Pav%02d_GcR_%s_%02da" % (n, NOMES[face], i + 1), [(a, (X0, elev_y0 - 0.05), inward)], z0, props)
                    seg_obj("TorreA_Pav%02d_GcR_%s_%02db" % (n, NOMES[face], i + 1), [((X0, elev_y1 + 0.05), b, inward)], z0, props)
                else:
                    seg_obj("TorreA_Pav%02d_GcR_%s_%02d" % (n, NOMES[face], i + 1), [(a, b, inward)], z0, props)

    # ---------------- pav 4: vaos sul 04 e 05 abertos (frente de trabalho do treinamento) - GcR em dois trechos cada
    for (i, split) in ((3, L.TR_GCR_SPLIT["Sul_04"]), (4, L.TR_GCR_SPLIT["Sul_05"])):
        _, a, b, inward = face_bays("S")[i]
        for (suf, p0, p1) in (("a", a, (split - 0.03, Y0)), ("b", (split + 0.03, Y0), b)):
            props = {"categoria": "protecao_coletiva", "tipo": "GcR_guarda_corpo_rodape", "pavimento": 4, "face": "Sul",
                     "nr_ref": "NR-18 18.9.4.2 (1,20 / 0,70 / rodape)", "treinamento": "frente_de_trabalho_pav04", "interativo": True}
            seg_obj("TorreA_Pav04_GcR_Sul_%02d%s" % (i + 1, suf), [(p0, p1, inward)], Z(4), props)

    # ---------------- vao da escada (pav 5 a 9)
    ex0, ey0, ex1, ey1 = L.TA_ESCADA_VAO
    for n in range(5, 10):
        z0 = Z(n)
        props = {"categoria": "protecao_coletiva", "tipo": "GcR_vao_escada", "pavimento": n, "nr_ref": "NR-18 18.9.2 / 18.9.4.2"}
        segs = [((ex0 + 0.05, ey0), (ex1 + 0.1, ey0), (0.0, -1.0)),
                ((ex1, ey0 + 0.05), (ex1, 15.66), (1.0, 0.0)),
                ((ex1, 16.34), (ex1, ey1 - 0.05), (1.0, 0.0)),
                ((ex1 + 0.1, ey1), (ex0 + 0.05, ey1), (0.0, 1.0))]
        seg_obj("TorreA_Pav%02d_GcR_Vao_Escada" % n, segs, z0, props)

    # ---------------- topo dos pocos de elevador no pav 9
    props = {"categoria": "protecao_coletiva", "tipo": "GcR_poco_elevador_topo", "pavimento": 9, "nr_ref": "NR-18 18.9.3"}
    segs = [((16.3, 19.6), (21.7, 19.6), (0.0, -1.0)), ((16.4, 19.6), (16.4, 21.35), (-1.0, 0.0)), ((21.6, 19.6), (21.6, 21.35), (1.0, 0.0))]
    seg_obj("TorreA_Pav09_GcR_Pocos_Elevador", segs, Z(9), props)

    # ---------------- borda da forma da laje 10 (trabalho a 2,9 m sobre a laje 9)
    fx0, fy0, fx1, fy1 = L.TA_FORMA_L10
    zd = Z(10) - L.TA_LAJE
    props = {"categoria": "protecao_coletiva", "tipo": "GcR_borda_forma", "pavimento": 10, "nr_ref": "NR-18 18.9.4.2"}
    segs = [((fx0 + 0.15, fy1), (fx1, fy1), (0.0, -1.0)), ((fx1, fy1), (fx1, fy0), (-1.0, 0.0)),
            ((fx1, fy0), (fx0 + 0.15, fy0), (0.0, 1.0)), ((fx0 + 0.15, fy0), (fx0 + 0.15, 12.0), (1.0, 0.0)),
            ((fx0 + 0.15, 13.1), (fx0 + 0.15, fy1), (1.0, 0.0))]
    seg_obj("TorreA_Pav10_GcR_Borda_Forma", segs, zd, props)

    # ---------------- SLQA tipo forca (redes) na fachada leste, pav 7 a 9
    mb = MB()
    zt = Z(9) + 2.2
    ys = [4.35, 10.0, 16.0, 21.65]
    for y in ys:
        mb.cyl((X1 + 0.08, y, Z(7) - 0.4), (X1 + 0.08, y, zt), 0.045, "amarelo_escuro", n=6)
        mb.cyl((X1 + 0.08, y, zt), (X1 + 1.05, y, zt), 0.04, "amarelo_escuro", n=6)
        mb.strut((X1 + 0.08, y, zt - 0.6), (X1 + 0.7, y, zt - 0.02), 0.04, "amarelo_escuro")
        for n in (7, 8, 9):
            mb.box((X1 - 0.25, y - 0.12, Z(n) - 0.02), (X1 + 0.14, y + 0.12, Z(n) + 0.06), "grafite")
    mb.cyl((X1 + 1.05, ys[0], zt), (X1 + 1.05, ys[-1], zt), 0.012, "rede_preta", n=4)
    for n in (7, 8, 9):
        mb.strut((X1 - 0.02, Y0 + 0.4, Z(n) + 0.10), (X1 - 0.02, Y1 - 0.4, Z(n) + 0.10), 0.025, "amarelo_linha_vida", h=0.20)
    mb.quad_uv([(X1 + 0.12, ys[0], Z(7)), (X1 + 0.12, ys[-1], Z(7)), (X1 + 1.02, ys[-1], zt - 0.05), (X1 + 1.02, ys[0], zt - 0.05)],
               [(0, 0), ((ys[-1] - ys[0]) / 0.4, 0), ((ys[-1] - ys[0]) / 0.4, (zt - Z(7)) / 0.4), (0, (zt - Z(7)) / 0.4)], K.S_REDE)
    K.finish(mb, "TorreA_Pav07a09_SLQA_Rede_Forca_Leste", C, parent=grp,
             props={"categoria": "protecao_coletiva", "tipo": "SLQA_rede_tipo_forca", "face": "Leste", "nr_ref": "NR-18 18.9.4.4 (EN 1263)"})

    # ---------------- fechamento provisorio das portas dos pocos de elevador (pav 0 a 9)
    for n in range(0, 10):
        for k, cx in enumerate((17.75, 20.3)):
            mb = MB()
            z0 = Z(n)
            mb.box((cx - 0.68, 19.52, z0), (cx + 0.68, 19.58, z0 + 2.25), "compensado", sides="madeira")
            for hz in (0.35, 1.2, 2.0):
                mb.box((cx - 0.72, 19.47, z0 + hz), (cx + 0.72, 19.52, z0 + hz + 0.1), "madeira_escura")
            mb.strut((cx - 0.6, 19.465, z0 + 0.45), (cx + 0.6, 19.465, z0 + 1.9), 0.004, "amarelo_linha_vida", h=0.08, up=(0, 1, 0))
            mb.strut((cx + 0.6, 19.465, z0 + 0.45), (cx - 0.6, 19.465, z0 + 1.9), 0.004, "amarelo_linha_vida", h=0.08, up=(0, 1, 0))
            K.finish(mb, "TorreA_Pav%02d_Fechamento_Poco_Elevador_%d" % (n, k + 1), C, parent=grp,
                     props={"categoria": "protecao_coletiva", "tipo": "fechamento_provisorio_poco", "pavimento": n, "nr_ref": "NR-18 18.9.3"})

    # ---------------- tampoes das aberturas de shaft (pav 1 a 9)
    sx0, sy0, sx1, sy1 = L.TA_SHAFT
    for n in range(1, 10):
        if n in (2, 3):
            continue    # pav 2 e 3: tampas do roteiro (C10 protegida / C11 deslocada) no modulo de treinamento
        mb = MB()
        z0 = Z(n)
        mb.box((sx0 - 0.15, sy0 - 0.15, z0), (sx1 + 0.15, sy1 + 0.15, z0 + 0.03), "compensado", sides="madeira_escura")
        mb.box((sx0 - 0.02, sy0 - 0.02, z0 - 0.12), (sx0 + 0.04, sy1 + 0.02, z0), "madeira_escura")
        mb.box((sx1 - 0.04, sy0 - 0.02, z0 - 0.12), (sx1 + 0.02, sy1 + 0.02, z0), "madeira_escura")
        mb.strut((sx0 - 0.08, sy0 - 0.08, z0 + 0.032), (sx1 + 0.08, sy1 + 0.08, z0 + 0.032), 0.08, "amarelo_linha_vida", h=0.004)
        mb.strut((sx1 + 0.08, sy0 - 0.08, z0 + 0.033), (sx0 - 0.08, sy1 + 0.08, z0 + 0.033), 0.08, "amarelo_linha_vida", h=0.004)
        K.finish(mb, "TorreA_Pav%02d_Tampao_Shaft" % n, C, parent=grp,
                 props={"categoria": "protecao_coletiva", "tipo": "fechamento_abertura_piso", "pavimento": n, "nr_ref": "NR-18 18.9.2"})

    # ---------------- pontos de ancoragem no pav 9 (pilares da periferia)
    z9 = Z(9)
    k = 0
    for x in XL:
        for y in YL:
            if not (x in (X0, X1) or y in (Y0, Y1)):
                continue
            r = L.TA_PILAR(x, y)
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            dx = 0.55 if x == X0 else (-0.55 if x == X1 else 0.0)
            dy = 0.55 if y == Y0 else (-0.55 if y == Y1 else 0.0)
            if dx and dy:
                dx, dy = dx * 0.8, dy * 0.8
            px, py = cx + dx, cy + dy
            mb = MB()
            mb.box((-0.1, -0.1, 0.0), (0.1, 0.1, 0.012), "grafite", nobottom=True)
            mb.box((-0.07, -0.012, 0.012), (-0.045, 0.012, 0.13), "amarelo_linha_vida")
            mb.box((0.045, -0.012, 0.012), (0.07, 0.012, 0.13), "amarelo_linha_vida")
            mb.box((-0.07, -0.012, 0.13), (0.07, 0.012, 0.155), "amarelo_linha_vida")
            k += 1
            rz = 90.0 if y in (Y0, Y1) and x not in (X0, X1) else 0.0
            K.finish(mb, "TorreA_Pav09_Ponto_Ancoragem_%02d" % k, C, parent=grp, loc=(px, py, z9), rz=rz,
                     props={"categoria": "epi_ancoragem", "tipo": "ponto_ancoragem", "pavimento": 9, "carga_minima_kgf": 1500,
                            "nr_ref": "NR-18 18.12.12 / NR-35", "interativo": True})

    # ---------------- linha de vida horizontal no pav 9 (faces sul e oeste)
    mb = MB()
    pts = [(30.7, 5.3), (24.3, 5.3), (19.0, 5.3), (13.8, 5.3), (7.3, 5.3), (7.3, 10.8), (7.3, 15.2), (7.3, 20.7)]
    zc = z9 + 1.12
    for (px, py) in pts:
        mb.box((px - 0.15, py - 0.15, z9), (px + 0.15, py + 0.15, z9 + 0.02), "grafite", nobottom=True)
        mb.cyl((px, py, z9 + 0.02), (px, py, z9 + 1.2), 0.035, "amarelo_linha_vida", n=8)
        mb.cyl((px, py, z9 + 1.2), (px, py, z9 + 1.25), 0.05, "vermelho_seguranca", n=8)
    for a, b in zip(pts[:-1], pts[1:]):
        mb.cyl((a[0], a[1], zc), (b[0], b[1], zc), 0.008, "cinza_escuro", n=4, caps=False, smooth=False)
    mb.box((29.4, 5.24, zc - 0.05), (29.9, 5.36, zc + 0.05), "amarelo_escuro")
    mb.cyl((8.6, 5.3, zc), (9.0, 5.3, zc), 0.035, "vermelho_seguranca", n=8)
    K.finish(mb, "TorreA_Pav09_Linha_Vida_Horizontal", C, parent=grp,
             props={"categoria": "epi_ancoragem", "tipo": "linha_de_vida", "pavimento": 9, "nr_ref": "NR-35 / NR-18 18.12.12", "interativo": True})
    return {"objetos": len(C.objects), "gcr": count["GcR"], "ancoragens": k}
