# gen_14_15_andaime_elevador.py - andaime fachadeiro (fachada sul) e elevador de cremalheira (fachada oeste)
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
gen13 = sys.modules.get("gen_13")


def tube(mb, a, b, r=0.024, c="azul_andaime", n=6):
    mb.cyl(a, b, r, c, n=n, caps=False)


def build_andaime():
    C = K.coll("14_TorreA_Andaime")
    K.clear_coll(C)
    grp = K.empty("GRP_TorreA_Andaime_Fachadeiro", C, (0, 0, 0), size=2.0,
                  props={"categoria": "andaime", "tipo": "andaime_fachadeiro", "nr_ref": "NR-18 18.12"})
    xa, xb = L.ANDAIME
    YO, YI = 2.70, 3.70
    nb = int(round((xb - xa) / 2.0))
    XS = [xa + 2.0 * i for i in range(nb + 1)]
    LIFTS = [2.0 * k for k in range(1, 8)]
    ZTOP = LIFTS[-1] + 2.0

    mb = MB()
    for y in (YO, YI):
        mb.box((xa - 0.3, y - 0.15, 0.0), (xb + 0.3, y + 0.15, 0.05), "madeira", nobottom=True)
        for x in XS:
            mb.box((x - 0.08, y - 0.08, 0.05), (x + 0.08, y + 0.08, 0.06), "grafite", nobottom=True)
            mb.cyl((x, y, 0.06), (x, y, 0.28), 0.018, "cromado", n=6, caps=False)
            mb.box((x - 0.05, y - 0.05, 0.22), (x + 0.05, y + 0.05, 0.26), "laranja_escuro")
            tube(mb, (x, y, 0.26), (x, y, ZTOP))
    for x in XS:
        tube(mb, (x, YO, 0.45), (x, YI, 0.45), r=0.02)
    tube(mb, (xa, YO, 0.45), (xb, YO, 0.45), r=0.02)
    tube(mb, (xa, YI, 0.45), (xb, YI, 0.45), r=0.02)
    K.finish(mb, "TorreA_Andaime_Base_Montantes", C, parent=grp, props={"categoria": "andaime", "parte": "base_e_montantes"})

    for k, z in enumerate(LIFTS, start=1):
        mb = MB()
        zl = z - 0.08
        tube(mb, (xa, YO, zl), (xb, YO, zl), r=0.022)
        tube(mb, (xa, YI, zl), (xb, YI, zl), r=0.022)
        for x in XS:
            tube(mb, (x, YO - 0.05, zl), (x, YI + 0.05, zl), r=0.022)
        for i in range(nb):
            x0, x1 = XS[i] + 0.03, XS[i + 1] - 0.03
            if i == 0:
                mb.box((x0 + 0.85, YO + 0.03, z - 0.05), (x1, YI - 0.03, z), "aco", sides="cinza_medio")
                mb.box((x0, YO + 0.03, z - 0.05), (x0 + 0.85, 3.10, z), "aco", sides="cinza_medio")
                mb.box((x0 + 0.02, 3.10, z), (x0 + 0.83, 3.13, z + 0.7), "amarelo_escuro")
            else:
                mb.box((x0, YO + 0.03, z - 0.05), (x1, YI - 0.03, z), "aco", sides="cinza_medio")
        # guarda-corpo externo + rodape (NR-18 18.12.1 d)
        yg = YO - 0.05
        tube(mb, (xa - 0.05, yg, z + 1.2), (xb + 0.05, yg, z + 1.2), r=0.024, c="amarelo_linha_vida")
        tube(mb, (xa - 0.05, yg, z + 0.7), (xb + 0.05, yg, z + 0.7), r=0.022, c="amarelo_linha_vida")
        mb.box((xa, yg - 0.03, z), (xb, yg, z + 0.15), "madeira")
        for xe in (xa - 0.05, xb + 0.05):
            tube(mb, (xe, YO - 0.05, z + 1.2), (xe, YI + 0.05, z + 1.2), r=0.022, c="amarelo_linha_vida")
            tube(mb, (xe, YO - 0.05, z + 0.7), (xe, YI + 0.05, z + 0.7), r=0.022, c="amarelo_linha_vida")
            mb.box((xe - 0.015, YO, z), (xe + 0.015, YI, z + 0.15), "madeira")
        # contraventamento diagonal na face externa
        z0 = z - 2.0 + (0.3 if k == 1 else 0.1)
        for i in range(nb):
            if (i + k) % 2 == 0:
                tube(mb, (XS[i], YO - 0.03, z0), (XS[i + 1], YO - 0.03, z - 0.12), r=0.02)
        K.finish(mb, "TorreA_Andaime_Nivel_%02d" % k, C, parent=grp,
                 props={"categoria": "andaime", "parte": "plataforma", "nivel": k, "cota_piso_m": z,
                        "nr_ref": "NR-18 18.12.5 forracao completa; 18.12.1 GcR"})

    mb = MB()
    zprev = 0.06
    for k, z in enumerate(LIFTS, start=1):
        bx, by = xa + 0.45, YI - 0.06
        tx, ty = xa + 0.45, 3.16
        zb, zt = zprev, z + 1.0
        for dx in (-0.22, 0.22):
            mb.strut((bx + dx, by, zb), (tx + dx, ty, zt), 0.04, "cinza_claro", h=0.07)
        nr = int((zt - zb) / 0.3)
        for j in range(1, nr):
            u = j / nr
            px = bx
            py = by + (ty - by) * u
            pz = zb + (zt - zb) * u
            mb.cyl((px - 0.22, py, pz), (px + 0.22, py, pz), 0.015, "cinza_claro", n=5, caps=False)
        zprev = z
    K.finish(mb, "TorreA_Andaime_Escadas_Acesso", C, parent=grp,
             props={"categoria": "andaime", "parte": "escada_interna_com_alcapao", "nr_ref": "NR-18 18.12.14"})

    mb = MB()
    for x in (11.2, 16.4, 21.6, 26.8):
        for z in (4.6, 8.6, 12.6):
            tube(mb, (x, YI - 0.02, z), (x, 4.05, z), r=0.024, c="cromado")
            tube(mb, (x - 0.9, YI - 0.02, z), (x + 0.9, YI - 0.02, z), r=0.022, c="cromado")
            mb.box((x - 0.06, 3.98, z - 0.08), (x + 0.06, 4.03, z + 0.08), "grafite")
    K.finish(mb, "TorreA_Andaime_Ancoragens_Estrutura", C, parent=grp,
             props={"categoria": "andaime", "parte": "ancoragem_na_estrutura", "nr_ref": "NR-18 18.12.13 b"})

    mb = MB()
    yt = YO - 0.12
    z0, z1 = LIFTS[0], ZTOP
    Lx = (xb + 0.12) - (xa - 0.12)
    mb.quad_uv([(xa - 0.12, yt, z0), (xb + 0.12, yt, z0), (xb + 0.12, yt, z1), (xa - 0.12, yt, z1)],
               [(0, 0), (Lx / 0.5, 0), (Lx / 0.5, (z1 - z0) / 0.5), (0, (z1 - z0) / 0.5)], K.S_TELA_FACHADA)
    for xe in (xa - 0.12, xb + 0.12):
        mb.quad_uv([(xe, yt, z0), (xe, 3.95, z0), (xe, 3.95, z1), (xe, yt, z1)],
                   [(0, 0), (1.35 / 0.5, 0), (1.35 / 0.5, (z1 - z0) / 0.5), (0, (z1 - z0) / 0.5)], K.S_TELA_FACHADA)
    K.finish(mb, "TorreA_Andaime_Tela_Fachadeira", C, parent=grp,
             props={"categoria": "protecao_coletiva", "tipo": "tela_fachadeira", "nr_ref": "NR-18 18.12.15 (ate 2 m acima da ultima plataforma)"})
    return len(C.objects)


def build_elevador():
    C = K.coll("15_TorreA_Elevador_Cremalheira")
    K.clear_coll(C)
    Z = L.TA_Z
    ex0, ey0, ex1, ey1 = L.ELEVADOR
    MX, MY = 2.0, L.ELEV_CABINE_Y
    grp = K.empty("GRP_Elevador_Cremalheira", C, (MX, MY, 0), size=2.0,
                  props={"categoria": "elevador_obra", "tipo": "elevador_passageiros_cremalheira", "nr_ref": "NR-18 18.11.21 (obra >= 24 m)"})
    HTOP = Z(9) + 6.0
    # ---- torre (mastro) + base
    mb = MB()
    mb.box((0.9 - MX, 10.4 - MY, 0.0), (4.6 - MX, 15.6 - MY, 0.15), "grafite", top="cinza_escuro", nobottom=True)
    for dy in (-0.9, 0.9):
        mb.cyl((3.4 - MX, dy, 0.15), (3.4 - MX, dy, 0.55), 0.12, "amarelo_maquina", n=8)
    h = 0.3
    for (dx, dy) in ((-h, -h), (h, -h), (h, h), (-h, h)):
        mb.cyl((dx, dy, 0.15), (dx, dy, HTOP), 0.036, "cinza_claro", n=6, caps=False)
    zz = 0.15
    while zz < HTOP - 0.1:
        for (a, b) in (((-h, -h), (h, -h)), ((h, -h), (h, h)), ((h, h), (-h, h)), ((-h, h), (-h, -h))):
            mb.cyl((a[0], a[1], zz), (b[0], b[1], zz), 0.016, "cinza_claro", n=5, caps=False)
        mb.cyl((-h, -h, zz), (-h, h, zz + 1.508), 0.014, "cinza_claro", n=5, caps=False)
        mb.cyl((-h, -h, zz), (h, -h, zz + 1.508), 0.014, "cinza_claro", n=5, caps=False)
        mb.cyl((h, h, zz), (-h, h, zz + 1.508), 0.014, "cinza_claro", n=5, caps=False)
        zz += 1.508
    mb.box((h + 0.02, -0.08, 0.15), (h + 0.07, 0.08, HTOP), "grafite")
    # amarracoes do mastro na estrutura (desviando da cabine)
    for n in (2, 4, 6, 8):
        zt = Z(n) - 0.9
        for s in (-1, 1):
            yend = s * 1.95
            mb.strut((0.0, s * h, zt), (0.0, yend, zt), 0.06, "amarelo_escuro")
            mb.strut((0.0, yend, zt), (6.0 - MX + 0.05, yend, zt), 0.06, "amarelo_escuro")
            mb.box((6.0 - MX, yend - 0.12, zt - 0.12), (6.12 - MX, yend + 0.12, zt + 0.12), "grafite")
    K.finish(mb, "TorreA_Elevador_Torre_Mastro", C, parent=grp, loc=(0, 0, 0),
             props={"categoria": "elevador_obra", "parte": "torre_mastro_cremalheira", "altura_m": round(HTOP, 2)})

    # ---- cercado da base (2 m) com portao ao sul
    mb = MB()
    fence = [((ex0, ey0), (ex0, ey1)), ((ex0, ey1), (ex1 - 0.05, ey1)), ((ex0, ey0), (3.8, ey0))]
    for (a, b) in fence:
        ax_, ay_ = a[0] - MX, a[1] - MY
        bx_, by_ = b[0] - MX, b[1] - MY
        Lf = math.hypot(bx_ - ax_, by_ - ay_)
        npst = max(2, int(math.ceil(Lf / 2.0)) + 1)
        for i in range(npst):
            u = i / (npst - 1)
            px, py = ax_ + (bx_ - ax_) * u, ay_ + (by_ - ay_) * u
            mb.box((px - 0.03, py - 0.03, 0.0), (px + 0.03, py + 0.03, 2.05), "grafite", nobottom=True)
        for zr in (0.1, 1.95):
            mb.strut((ax_, ay_, zr), (bx_, by_, zr), 0.04, "amarelo_maquina")
        ux, uy = (bx_ - ax_) / Lf, (by_ - ay_) / Lf
        mb.quad_uv([(ax_, ay_, 0.12), (bx_, by_, 0.12), (bx_, by_, 1.93), (ax_, ay_, 1.93)],
                   [(0, 0), (Lf / 0.3, 0), (Lf / 0.3, 6.0), (0, 6.0)], K.S_REDE)
    gx0, gx1 = 3.95 - MX, 5.9 - MX
    gy = ey0 - MY
    mb.box((gx0, gy - 0.03, 0.0), (gx0 + 0.06, gy + 0.03, 2.05), "grafite", nobottom=True)
    mb.box((gx1 - 0.06, gy - 0.03, 0.0), (gx1, gy + 0.03, 2.05), "grafite", nobottom=True)
    mb.strut((gx0 + 0.06, gy - 0.6, 1.95), (gx0 + 0.06, gy, 1.95), 0.04, "amarelo_maquina")
    mb.quad_uv([(gx0 + 0.06, gy - 0.02, 0.1), (gx0 + 0.06, gy - 0.9, 0.1), (gx0 + 0.06, gy - 0.9, 1.9), (gx0 + 0.06, gy - 0.02, 1.9)],
               [(0, 0), (3, 0), (3, 6), (0, 6)], K.S_REDE)
    mb.box((gx1 - 0.3, gy - 0.08, 1.1), (gx1 - 0.1, gy - 0.03, 1.4), "vermelho_seguranca")
    K.finish(mb, "TorreA_Elevador_Cercado_Base", C, parent=grp,
             props={"categoria": "elevador_obra", "parte": "cercamento_base_2m", "interativo": True})

    # ---- cobertura de protecao no acesso (queda de materiais)
    mb = MB()
    for (px, py) in ((3.6, 6.0), (5.9, 6.0), (3.6, 8.9)):
        mb.box((px - MX - 0.06, py - MY - 0.06, 0.0), (px - MX + 0.06, py - MY + 0.06, 2.6), "amarelo_escuro", nobottom=True)
    mb.box((3.5 - MX, 5.9 - MY, 2.6), (5.95 - MX, 9.0 - MY, 2.68), "compensado", sides="madeira_escura")
    mb.box((4.45 - MX, 9.0 - MY, 2.4), (5.95 - MX, 17.0 - MY, 2.46), "compensado", sides="madeira_escura")
    mb.box((4.45 - MX, 16.9 - MY, 0.0), (4.55 - MX, 17.0 - MY, 2.4), "amarelo_escuro", nobottom=True)
    K.finish(mb, "TorreA_Elevador_Cobertura_Protecao", C, parent=grp,
             props={"categoria": "protecao_coletiva", "tipo": "cobertura_contra_queda_de_materiais"})

    # ---- rampas de acesso + cancelas (pav 1 a 9)
    for n in range(1, 10):
        z = Z(n)
        mb = MB()
        y0, y1 = 11.8 - MY, 14.2 - MY
        x0, x1 = 4.45 - MX, 6.0 - MX
        mb.box((x0, y0, z - 0.07), (x1 + 0.05, y1, z), "madeira", sides="madeira_escura")
        for yy in (y0 + 0.2, y1 - 0.2):
            mb.strut((x0 + 0.05, yy, z - 0.07), (x1, yy, z - 0.85), 0.06, "grafite")
        for (ys, inward) in ((y0, (0.0, 1.0)), (y1, (0.0, -1.0))):
            if gen13:
                gen13.gcr(mb, (x0 + 0.05, ys), (x1, ys), z, inward, off=0.06, spacing=1.6, clamp=False)
        for yy in (y0 - 0.06, y1):
            mb.box((x0 - 0.06, yy, z), (x0, yy + 0.06, z + 1.85), "amarelo_maquina")
        mb.box((x0 - 0.06, y0 - 0.06, z + 1.8), (x0, y1 + 0.06, z + 1.86), "amarelo_maquina")
        mb.box((x0 - 0.05, y0 + 0.02, z + 0.05), (x0 - 0.01, y1 - 0.02, z + 0.1), "amarelo_maquina")
        mb.quad_uv([(x0 - 0.03, y0 + 0.02, z + 0.1), (x0 - 0.03, y1 - 0.02, z + 0.1), (x0 - 0.03, y1 - 0.02, z + 1.78), (x0 - 0.03, y0 + 0.02, z + 1.78)],
                   [(0, 0), (2.36 / 0.2, 0), (2.36 / 0.2, 1.68 / 0.2), (0, 1.68 / 0.2)], K.S_TELA_GCR)
        mb.box((x0 - 0.12, y1 + 0.07, z + 1.0), (x0 - 0.02, y1 + 0.22, z + 1.25), "vermelho_seguranca")
        K.finish(mb, "TorreA_Pav%02d_Elevador_Rampa_Cancela" % n, C, parent=grp,
                 props={"categoria": "protecao_coletiva", "tipo": "cancela_1_8m_intertravada_e_rampa", "pavimento": n,
                        "nr_ref": "NR-18 18.11.13 / 18.11.15", "interativo": True})

    # ---- cabine (origem no piso da cabine; animar location.z entre os pavimentos)
    mb = MB()
    cx0, cx1 = -0.85, 0.85
    cy0, cy1 = -1.6, 1.6
    mb.box((cx0, cy0, -0.15), (cx1, cy1, 0.0), "grafite", top="cinza_escuro")
    mb.box((cx0 - 0.03, cy0 - 0.03, 2.4), (cx1 + 0.03, cy1 + 0.03, 2.5), "amarelo_maquina")
    for (px, py) in ((cx0, cy0), (cx1, cy0), (cx1, cy1), (cx0, cy1), (cx0, 0.0), (cx1, 0.0)):
        mb.box((px - 0.04, py - 0.04, 0.0), (px + 0.04, py + 0.04, 2.4), "amarelo_maquina", nobottom=True)
    mb.box((cx0, cy0, 0.0), (cx1, cy0 + 0.04, 1.1), "cinza_claro")
    mb.box((cx0, cy1 - 0.04, 0.0), (cx1, cy1, 1.1), "cinza_claro")
    mb.box((cx0, cy0, 0.0), (cx0 + 0.04, cy1, 1.1), "cinza_claro")
    for zb in (1.1, 2.35):
        mb.box((cx0, cy0, zb), (cx1, cy0 + 0.05, zb + 0.05), "amarelo_maquina")
        mb.box((cx0, cy1 - 0.05, zb), (cx1, cy1, zb + 0.05), "amarelo_maquina")
        mb.box((cx0, cy0, zb), (cx0 + 0.05, cy1, zb + 0.05), "amarelo_maquina")
    for (a, b) in (((cx0 + 0.02, cy0 + 0.02), (cx1 - 0.02, cy0 + 0.02)), ((cx1 - 0.02, cy1 - 0.02), (cx0 + 0.02, cy1 - 0.02)), ((cx0 + 0.02, cy1 - 0.02), (cx0 + 0.02, cy0 + 0.02))):
        Lq = math.hypot(b[0] - a[0], b[1] - a[1])
        mb.quad_uv([(a[0], a[1], 1.15), (b[0], b[1], 1.15), (b[0], b[1], 2.35), (a[0], a[1], 2.35)],
                   [(0, 0), (Lq / 0.2, 0), (Lq / 0.2, 6), (0, 6)], K.S_TELA_GCR)
    mb.box((cx1 - 0.02, -1.2, 0.0), (cx1 + 0.03, 1.2, 0.08), "amarelo_maquina")
    mb.box((cx1 - 0.02, -1.2, 1.9), (cx1 + 0.03, 1.2, 1.98), "amarelo_maquina")
    mb.quad_uv([(cx1 + 0.005, -1.2, 0.08), (cx1 + 0.005, 1.2, 0.08), (cx1 + 0.005, 1.2, 1.9), (cx1 + 0.005, -1.2, 1.9)],
               [(0, 0), (12, 0), (12, 9.1), (0, 9.1)], K.S_TELA_GCR)
    for (px, py) in ((cx0, cy0), (cx1, cy0), (cx1, cy1), (cx0, cy1)):
        mb.box((px - 0.02, py - 0.02, 2.5), (px + 0.02, py + 0.02, 3.6), "amarelo_maquina", nobottom=True)
    for zr in (3.05, 3.58):
        mb.box((cx0, cy0 - 0.02, zr), (cx1, cy0 + 0.02, zr + 0.04), "amarelo_maquina")
        mb.box((cx0, cy1 - 0.02, zr), (cx1, cy1 + 0.02, zr + 0.04), "amarelo_maquina")
        mb.box((cx0 - 0.02, cy0, zr), (cx0 + 0.02, cy1, zr + 0.04), "amarelo_maquina")
    mb.box((-1.35, -0.55, 2.5), (-0.75, 0.55, 3.25), "cinza_escuro", top="grafite")
    for dy in (-0.3, 0.3):
        mb.cyl((-1.05, dy, 3.25), (-1.05, dy, 3.6), 0.14, "azul_escuro", n=8)
    mb.box((-0.75, -0.25, 1.0), (-0.68, 0.25, 1.6), "grafite")
    mb.box((-0.68, -0.18, 1.2), (-0.66, -0.05, 1.3), "sinal_verde")
    mb.box((-0.68, 0.05, 1.2), (-0.66, 0.18, 1.3), "sinal_vermelho")
    z_cab = Z(6)
    K.finish(mb, "TorreA_Elevador_Cabine", C, parent=grp, loc=(3.4 - MX, 0.0, z_cab),
             props={"categoria": "elevador_obra", "parte": "cabine_passageiros", "capacidade_kg": 1500, "pavimento_atual": 6,
                    "cotas_pavimentos": ",".join("%.2f" % L.TA_Z(n) for n in range(10)), "interativo": True})
    return len(C.objects)


def build():
    a = build_andaime()
    e = build_elevador()
    return {"andaime_objs": a, "elevador_objs": e}
