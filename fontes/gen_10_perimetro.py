# gen_10_perimetro.py - tapume, portoes, catraca, saida de emergencia, placa de obra, torres de iluminacao
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB

HT = 2.2


def tapume(mb, a, b, openings=()):
    """segmento reto de a->b (2D) com vaos [(s0, s1)] em metros ao longo do segmento."""
    ax, ay = a
    bx, by = b
    Ls = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / Ls, (by - ay) / Ls
    cuts = sorted(openings)
    runs, cur = [], 0.0
    for s0, s1 in cuts:
        if s0 > cur:
            runs.append((cur, s0))
        cur = s1
    if cur < Ls:
        runs.append((cur, Ls))
    for (s0, s1) in runs:
        p0 = (ax + ux * s0, ay + uy * s0)
        p1 = (ax + ux * s1, ay + uy * s1)
        mb.strut((p0[0], p0[1], 0.1), (p1[0], p1[1], 0.1), 0.12, "concreto", h=0.2)
        mb.strut((p0[0], p0[1], 1.05), (p1[0], p1[1], 1.05), 0.05, "pintura_fachada", h=1.7)
        mb.strut((p0[0], p0[1], 2.05), (p1[0], p1[1], 2.05), 0.06, "placa_obra", h=0.3)
        n = max(1, int(round((s1 - s0) / 2.5)))
        for i in range(n + 1):
            s = s0 + (s1 - s0) * i / n
            px, py = ax + ux * s, ay + uy * s
            mb.box((px - 0.06, py - 0.06, 0.0), (px + 0.06, py + 0.06, HT + 0.05), "cinza_medio", nobottom=True)


def build():
    C = K.coll("10_Canteiro_Perimetro")
    K.clear_coll(C)
    X0, Y0, X1, Y1 = L.LOTE
    g0, g1 = L.PORTAO
    mb = MB()
    tapume(mb, (X0, Y0), (X1, Y0), openings=[(g0 - 1.5 - X0, g1 - X0)])
    tapume(mb, (X1, Y0), (X1, Y1), openings=[(20.0 - Y0, 21.2 - Y0)])
    tapume(mb, (X1, Y1), (X0, Y1))
    tapume(mb, (X0, Y1), (X0, Y0), openings=[(Y1 - 22.0, Y1 - 14.0)])
    K.finish(mb, "Canteiro_Tapume_Perimetro", C, props={"categoria": "perimetro", "tipo": "tapume_h2.2m", "nr_ref": "NR-18 18.4 / codigo de obras"})

    # ---------------- portao de veiculos (sul) aberto para dentro + portico
    mb = MB()
    for x in (g0, g1):
        mb.box((x - 0.15, Y0 - 0.15, 0.0), (x + 0.15, Y0 + 0.15, 5.2), "grafite", nobottom=True)
    mb.box((g0 - 0.2, Y0 - 0.2, 5.0), (g1 + 0.2, Y0 + 0.2, 5.35), "grafite")
    for (hx, s) in ((g0 + 0.2, 1), (g1 - 0.2, -1)):
        yA, yB = Y0 + 0.1, Y0 + 5.0
        mb.box((hx - 0.05, yA, 0.05), (hx + 0.05, yA + 0.08, 2.1), "azul_escuro")
        mb.box((hx - 0.05, yB - 0.08, 0.05), (hx + 0.05, yB, 2.1), "azul_escuro")
        for z in (0.05, 2.02):
            mb.box((hx - 0.05, yA, z), (hx + 0.05, yB, z + 0.08), "azul_escuro")
        mb.strut((hx, yA + 0.05, 0.12), (hx, yB - 0.05, 2.0), 0.05, "azul_escuro", h=0.05)
        mb.quad_uv([(hx, yA, 0.13), (hx, yB, 0.13), (hx, yB, 2.02), (hx, yA, 2.02)],
                   [(0, 0), (4.9 / 0.3, 0), (4.9 / 0.3, 6.3), (0, 6.3)], K.S_REDE)
        mb.box((hx - 0.2, yB - 0.25, 0.0), (hx + 0.2, yB + 0.05, 0.12), "borracha")
    # lava-rodas na saida
    mb.box((g0 + 1.0, Y0 + 1.0, 0.0), (g1 - 1.0, Y0 + 5.0, 0.08), "concreto", nobottom=True)
    for k in range(9):
        y = Y0 + 1.3 + k * 0.42
        mb.box((g0 + 1.2, y, 0.08), (g1 - 1.2, y + 0.12, 0.1), "grafite", nobottom=True)
    mb.box((g1 - 0.9, Y0 + 5.3, 0.0), (g1 - 0.7, Y0 + 5.5, 1.3), "azul_escuro", nobottom=True)
    mb.cyl((g1 - 0.8, Y0 + 5.4, 1.2), (g1 - 0.2, Y0 + 5.0, 0.9), 0.03, "amarelo_escuro", n=5)
    K.finish(mb, "Canteiro_Portao_Veiculos_Sul", C, props={"categoria": "perimetro", "tipo": "portao_veiculos_aberto", "largura_m": g1 - g0, "interativo": True})

    # ---------------- portao de pedestres + catraca
    mb = MB()
    px0, px1 = g0 - 1.5, g0 - 0.15
    mb.box((px0 - 0.08, Y0 - 0.08, 0.0), (px0 + 0.08, Y0 + 0.08, 2.5), "grafite", nobottom=True)
    mb.box((px0, Y0 - 0.05, 2.35), (g0, Y0 + 0.05, 2.5), "grafite")
    mb.box((px0 + 0.05, Y0 + 0.05, 0.05), (px0 + 0.1, Y0 + 1.25, 2.1), "verde_escuro")
    mb.box((px0 + 0.35, Y0 + 1.6, 0.0), (px0 + 0.75, Y0 + 2.1, 1.0), "cromado", top="grafite")
    for k in range(3):
        a = math.radians(90 + k * 120)
        mb.cyl((px0 + 0.55, Y0 + 1.85, 0.95), (px0 + 0.55 + 0.55 * math.cos(a), Y0 + 1.85 + 0.55 * math.sin(a), 0.95 - 0.2 * (k != 0)), 0.025, "cromado", n=6)
    mb.box((px0 + 0.45, Y0 + 1.7, 1.0), (px0 + 0.65, Y0 + 1.75, 1.2), "g:vidro_escuro")
    K.finish(mb, "Canteiro_Portao_Pedestres_Catraca", C, props={"categoria": "perimetro", "tipo": "acesso_pedestres_controle", "interativo": True})

    # ---------------- portao lateral oeste (fechado) e saida de emergencia leste
    mb = MB()
    for y in (14.0, 22.0):
        mb.box((X0 - 0.12, y - 0.12, 0.0), (X0 + 0.12, y + 0.12, 2.6), "grafite", nobottom=True)
    for (ya, yb) in ((14.1, 17.98), (18.02, 21.9)):
        for z in (0.05, 2.1):
            mb.box((X0 - 0.04, ya, z), (X0 + 0.04, yb, z + 0.08), "azul_escuro")
        mb.box((X0 - 0.04, ya, 0.05), (X0 + 0.04, ya + 0.08, 2.18), "azul_escuro")
        mb.box((X0 - 0.04, yb - 0.08, 0.05), (X0 + 0.04, yb, 2.18), "azul_escuro")
        mb.box((X0 - 0.02, ya + 0.08, 0.13), (X0 + 0.02, yb - 0.08, 2.1), "pintura_fachada")
        mb.box((X0 - 0.035, ya + 0.08, 1.75), (X0 + 0.035, yb - 0.08, 2.05), "placa_obra")
    K.finish(mb, "Canteiro_Portao_Veiculos_Oeste_Fechado", C, props={"categoria": "perimetro", "tipo": "portao_entrega_materiais"})
    mb = MB()
    mb.box((X1 - 0.1, 19.9, 0.0), (X1 + 0.1, 20.0, 2.3), "grafite", nobottom=True)
    mb.box((X1 - 0.1, 21.2, 0.0), (X1 + 0.1, 21.3, 2.3), "grafite", nobottom=True)
    mb.box((X1 - 0.1, 19.9, 2.2), (X1 + 0.1, 21.3, 2.3), "grafite")
    mb.box((X1 - 0.03, 20.0, 0.02), (X1 + 0.03, 21.2, 2.2), "verde_seguranca")
    mb.box((X1 - 0.08, 20.1, 1.0), (X1 - 0.03, 21.1, 1.06), "cromado")
    K.finish(mb, "Canteiro_Saida_Emergencia_Leste", C, props={"categoria": "emergencia", "tipo": "saida_de_emergencia", "interativo": True})

    # ---------------- placa de obra (estrutura; arte aplicada no modulo de sinalizacao)
    mb = MB()
    bx0, bx1, by = -37.0, -31.0, Y0 + 0.35
    for x in (bx0 + 0.6, bx1 - 0.6):
        mb.box((x - 0.08, by - 0.08, 0.0), (x + 0.08, by + 0.08, 5.6), "grafite", nobottom=True)
    mb.box((bx0 - 0.08, by, 2.45), (bx1 + 0.08, by + 0.12, 5.55), "cinza_escuro")
    for z in (3.0, 4.2, 5.2):
        mb.box((bx0 + 0.2, by + 0.12, z), (bx1 - 0.2, by + 0.2, z + 0.08), "grafite")
    K.finish(mb, "Canteiro_Placa_Obra_Estrutura", C, props={"categoria": "sinalizacao", "tipo": "placa_de_obra"})

    # ---------------- torres de iluminacao
    for i, (x, y, rz) in enumerate(((-38.6, -28.6, 45.0), (39.2, -28.2, 135.0), (-38.6, 28.6, -45.0), (38.6, 28.6, -135.0), (-11.8, -4.2, -60.0))):
        mb = MB()
        mb.box((-0.3, -0.3, 0.0), (0.3, 0.3, 0.25), "concreto", nobottom=True)
        mb.cyl((0, 0, 0.25), (0, 0, 8.0), 0.09, "cinza_medio", n=8, r1=0.06)
        mb.box((-0.9, -0.05, 7.8), (0.9, 0.05, 7.9), "grafite")
        for sx in (-0.65, 0.0, 0.65):
            mb.box((sx - 0.22, 0.05, 7.4), (sx + 0.22, 0.35, 7.75), "grafite")
            mb.box((sx - 0.18, 0.35, 7.45), (sx + 0.18, 0.37, 7.7), "e:lampada")
        mb.box((-0.15, -0.1, 1.2), (0.15, 0.1, 1.6), "cinza_claro")
        K.finish(mb, "Canteiro_Torre_Iluminacao_%02d" % (i + 1), C, loc=(x, y, 0.0), rz=rz,
                 props={"categoria": "iluminacao", "tipo": "refletores_8m"})
    return {"objetos": len(C.objects)}
