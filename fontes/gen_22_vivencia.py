# gen_22_vivencia.py - areas de vivencia (NR-18 18.5), escritorio, portaria, almoxarifado/EPI, DDS, cacambas
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
g13 = sys.modules["gen_13"]


def container(mb, Lc=6.0, W=2.4, H=2.6, cor="azul_container", trim="branco", windows=(), doors=(), ac=None, z0=0.0, ribs=True, marit=False):
    """contêiner com eixo longo em X centrado na origem. windows/doors: (lado, centro, largura[, z0, z1]); lados 'N'(+Y) 'S'(-Y) 'E'(+X) 'W'(-X)."""
    hx, hy = Lc / 2, W / 2
    z1 = z0 + H
    mb.box((-hx, -hy, z0), (hx, hy, z0 + 0.15), "grafite")
    mb.box((-hx + 0.03, -hy + 0.03, z0 + 0.15), (hx - 0.03, hy - 0.03, z1 - 0.14), cor)
    mb.box((-hx, -hy, z1 - 0.14), (hx, hy, z1), trim if not marit else cor)
    for (x, y) in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)):
        mb.box((x - 0.07 * (1 if x > 0 else -1) * 0 - 0.07, y - 0.07, z0), (x + 0.07, y + 0.07, z1), trim if not marit else "grafite")
    if not marit:
        mb.box((-hx + 0.1, -hy + 0.1, z1), (hx - 0.1, hy - 0.1, z1 + 0.06), "cinza_claro")

    def occupied(side, s):
        for it in list(windows) + list(doors):
            if it[0] == side and abs(s - it[1]) < it[2] / 2 + 0.12:
                return True
        return False
    if ribs:
        step = 0.5 if not marit else 0.3
        for side in ("N", "S"):
            y = hy if side == "N" else -hy
            s = -hx + 0.35
            while s < hx - 0.3:
                if not occupied(side, s):
                    yy = (y, y + 0.025) if side == "N" else (y - 0.025, y)
                    mb.box((s - 0.05, yy[0], z0 + 0.18), (s + 0.05, yy[1], z1 - 0.17), cor)
                s += step
        if marit:
            for side in ("E", "W"):
                x = hx if side == "E" else -hx
                s = -hy + 0.3
                while s < hy - 0.2:
                    xx = (x, x + 0.025) if side == "E" else (x - 0.025, x)
                    mb.box((xx[0], s - 0.05, z0 + 0.18), (xx[1], s + 0.05, z1 - 0.17), cor)
                    s += 0.3
    for it in windows:
        side, c, w = it[0], it[1], it[2]
        wz0, wz1 = (it[3], it[4]) if len(it) > 3 else (1.0, 2.0)
        if side in ("N", "S"):
            y = hy if side == "N" else -hy
            sg = 1 if side == "N" else -1
            mb.box((c - w / 2, min(y, y + sg * 0.03), z0 + wz0), (c + w / 2, max(y, y + sg * 0.03), z0 + wz1), "g:vidro_escuro")
            mb.ring_box(c - w / 2 - 0.06, min(y, y + sg * 0.05), c + w / 2 + 0.06, max(y, y + sg * 0.05), z0 + wz0 - 0.06, z0 + wz0, 0.0, trim)
            mb.box((c - w / 2 - 0.06, min(y, y + sg * 0.05), z0 + wz0 - 0.06), (c + w / 2 + 0.06, max(y, y + sg * 0.05), z0 + wz0), trim)
            mb.box((c - w / 2 - 0.06, min(y, y + sg * 0.05), z0 + wz1), (c + w / 2 + 0.06, max(y, y + sg * 0.05), z0 + wz1 + 0.06), trim)
            mb.box((c - w / 2 - 0.06, min(y, y + sg * 0.05), z0 + wz0), (c - w / 2, max(y, y + sg * 0.05), z0 + wz1), trim)
            mb.box((c + w / 2, min(y, y + sg * 0.05), z0 + wz0), (c + w / 2 + 0.06, max(y, y + sg * 0.05), z0 + wz1), trim)
            for k in range(1, 4):
                xx = c - w / 2 + k * w / 4
                mb.box((xx - 0.012, min(y, y + sg * 0.06), z0 + wz0), (xx + 0.012, max(y, y + sg * 0.06), z0 + wz1), "cinza_escuro")
        else:
            x = hx if side == "E" else -hx
            sg = 1 if side == "E" else -1
            mb.box((min(x, x + sg * 0.03), c - w / 2, z0 + wz0), (max(x, x + sg * 0.03), c + w / 2, z0 + wz1), "g:vidro_escuro")
            mb.box((min(x, x + sg * 0.05), c - w / 2 - 0.06, z0 + wz0 - 0.06), (max(x, x + sg * 0.05), c + w / 2 + 0.06, z0 + wz0), trim)
            mb.box((min(x, x + sg * 0.05), c - w / 2 - 0.06, z0 + wz1), (max(x, x + sg * 0.05), c + w / 2 + 0.06, z0 + wz1 + 0.06), trim)
    for it in doors:
        side, c, w = it[0], it[1], it[2]
        if side in ("N", "S"):
            y = hy if side == "N" else -hy
            sg = 1 if side == "N" else -1
            mb.box((c - w / 2, min(y, y + sg * 0.04), z0 + 0.15), (c + w / 2, max(y, y + sg * 0.04), z0 + 2.2), "cinza_claro")
            mb.box((c - w / 2 - 0.07, min(y, y + sg * 0.05), z0 + 2.2), (c + w / 2 + 0.07, max(y, y + sg * 0.05), z0 + 2.28), trim)
            mb.box((c + w / 2 - 0.2, min(y, y + sg * 0.07), z0 + 1.0), (c + w / 2 - 0.1, max(y, y + sg * 0.07), z0 + 1.08), "grafite")
            mb.box((c - w / 2 - 0.1, min(y + sg * 0.05, y + sg * 0.7), 0.0), (c + w / 2 + 0.1, max(y + sg * 0.05, y + sg * 0.7), z0 + 0.15), "concreto")
        else:
            x = hx if side == "E" else -hx
            sg = 1 if side == "E" else -1
            mb.box((min(x, x + sg * 0.04), c - w / 2, z0 + 0.15), (max(x, x + sg * 0.04), c + w / 2, z0 + 2.2), "cinza_claro")
            if marit:
                for k in range(4):
                    yy = c - w / 2 + (k + 0.5) * w / 4
                    mb.box((min(x, x + sg * 0.08), yy - 0.02, z0 + 0.3), (max(x, x + sg * 0.08), yy + 0.02, z0 + 2.4), "cinza_escuro")
    if ac:
        side, c = ac
        y = hy if side == "N" else -hy
        sg = 1 if side == "N" else -1
        mb.box((c - 0.4, min(y, y + sg * 0.32), z0 + 1.5), (c + 0.4, max(y, y + sg * 0.32), z0 + 2.05), "condensadora")
        mb.cyl((c - 0.1, y + sg * 0.32, z0 + 1.77), (c - 0.1, y + sg * 0.33, z0 + 1.77), 0.2, "cinza_escuro", n=10)


def build():
    C = K.coll("22_Areas_Vivencia")
    K.clear_coll(C)
    yc = -28.4
    P = lambda tipo, **kw: dict({"categoria": "area_de_vivencia", "tipo": tipo, "nr_ref": "NR-18 18.5 areas de vivencia"}, **kw)

    def place(mb, name, loc, rz=0.0, props=None):
        return K.finish(mb, name, C, loc=loc, rz=rz, props=props)

    for (nm, cx, tipo, wins) in (("Vestiario", -25.0, "vestiario", [("N", -1.5, 0.8, 1.7, 2.2), ("N", 1.5, 0.8, 1.7, 2.2)]),
                                 ("Instalacao_Sanitaria", -18.6, "instalacao_sanitaria", [("N", -1.8, 0.6, 1.8, 2.2), ("N", 0.2, 0.6, 1.8, 2.2), ("N", 2.2, 0.6, 1.8, 2.2)])):
        mb = MB()
        container(mb, windows=wins, doors=[("N", -0.3 if tipo == "vestiario" else -1.0, 0.9)], ac=("S", 1.5) if tipo == "vestiario" else None, z0=0.2)
        place(mb, "Vivencia_Container_" + nm, (cx, yc, 0.0), 0.0, P(tipo, interativo=True))
    mb = MB()
    container(mb, Lc=12.0, windows=[("N", -4.0, 1.4), ("N", -1.2, 1.4), ("N", 3.6, 1.4), ("W", 0.0, 1.0)], doors=[("N", 1.2, 1.1)], ac=("S", -2.0), z0=0.2)
    mb.box((-5.9, 1.2, 0.0), (5.9, 3.2, 0.12), "concreto", nobottom=True)
    for k in range(3):
        x = -4.5 + k * 3.2
        mb.box((x, 2.1, 0.12), (x + 1.8, 2.9, 0.85), "madeira_clara", notop=False)
    mb.box((5.2, 1.3, 0.12), (5.8, 1.8, 1.0), "cromado", top="cinza_escuro")
    place(mb, "Vivencia_Container_Refeitorio", (-9.2, yc, 0.0), 0.0, P("refeitorio_com_bebedouro", interativo=True))

    # banheiros quimicos
    for k in range(3):
        mb = MB()
        mb.box((-0.55, -0.55, 0.0), (0.55, 0.55, 0.12), "azul_escuro")
        mb.rbox((-0.52, -0.52, 0.12), (0.52, 0.52, 2.2), "azul_container", r=0.04)
        mb.hull([(-0.56, -0.56, 2.2), (0.56, -0.56, 2.2), (0.56, 0.56, 2.2), (-0.56, 0.56, 2.2), (-0.3, -0.3, 2.42), (0.3, -0.3, 2.42), (0.3, 0.3, 2.42), (-0.3, 0.3, 2.42)], "branco")
        mb.box((-0.4, 0.52, 0.2), (0.4, 0.56, 2.05), "azul_claro")
        mb.box((0.25, 0.56, 1.1), (0.35, 0.6, 1.2), "vermelho_seguranca")
        mb.box((-0.2, 0.56, 1.9), (0.2, 0.58, 2.0), "branco")
        place(mb, "Vivencia_Banheiro_Quimico_%02d" % (k + 1), (-0.8 + k * 1.25, -29.1, 0.0), 0.0, P("banheiro_quimico"))

    # area de DDS coberta
    mb = MB()
    x0, x1, y0, y1 = 5.0, 12.0, -29.4, -25.4
    for (px, py, h) in ((x0, y0, 2.9), (x1, y0, 2.9), ((x0 + x1) / 2, y0, 2.9), (x0, y1, 2.6), (x1, y1, 2.6), ((x0 + x1) / 2, y1, 2.6)):
        mb.box((px - 0.06, py - 0.06, 0.0), (px + 0.06, py + 0.06, h), "cinza_escuro", nobottom=True)
    mb.hull([(x0 - 0.3, y0 - 0.3, 2.9), (x1 + 0.3, y0 - 0.3, 2.9), (x0 - 0.3, y1 + 0.3, 2.55), (x1 + 0.3, y1 + 0.3, 2.55),
             (x0 - 0.3, y0 - 0.3, 3.0), (x1 + 0.3, y0 - 0.3, 3.0), (x0 - 0.3, y1 + 0.3, 2.65), (x1 + 0.3, y1 + 0.3, 2.65)], "lona_azul")
    mb.box((x0 - 0.3, y0, 0.0), (x1 + 0.3, y1, 0.08), "concreto", nobottom=True)
    for k in range(3):
        by = -28.7 + k * 1.0
        mb.box((6.8, by, 0.42), (10.8, by + 0.35, 0.47), "madeira")
        for bx in (7.0, 10.6):
            mb.box((bx - 0.04, by + 0.05, 0.08), (bx + 0.04, by + 0.3, 0.42), "grafite")
    mb.box((x1 - 0.35, -28.9, 0.08), (x1 - 0.3, -26.1, 2.3), "grafite")
    mb.box((x1 - 0.42, -28.8, 0.9), (x1 - 0.35, -26.2, 2.2), "branco_sinal")
    place(mb, "Vivencia_Area_DDS_Coberta", (0.0, 0.0, 0.0), 0.0, P("area_DDS_dialogo_diario_seguranca", interativo=True, ponto_de_partida_treinamento=True))

    # almoxarifado com balcao de EPI
    mb = MB()
    container(mb, windows=[("N", 1.6, 1.4, 1.0, 1.9)], doors=[("N", -1.4, 1.0)], ac=("S", 0.0), z0=0.2)
    mb.box((0.8, 1.2, 1.1), (2.4, 1.6, 1.16), "madeira_clara")
    for k in range(4):
        mb.rbox((0.9 + k * 0.38, 1.3, 1.16), (1.2 + k * 0.38, 1.5, 1.32), ("capacete_branco", "capacete_amarelo", "capacete_azul", "capacete_branco")[k], r=0.06)
    place(mb, "Vivencia_Container_Almoxarifado_EPI", (17.0, yc, 0.0), 0.0, P("almoxarifado_entrega_EPI", interativo=True, nr_ref="NR-6 EPI / NR-35 cinturao"))

    # portaria
    mb = MB()
    container(mb, Lc=4.8, windows=[("N", 0.8, 1.6, 1.0, 2.0), ("E", 0.0, 1.4, 1.0, 2.0), ("W", 0.0, 1.0, 1.0, 2.0)], doors=[("N", -1.3, 0.9)], z0=0.2, cor="branco", trim="azul_escuro")
    place(mb, "Vivencia_Container_Portaria", (23.6, yc, 0.0), 0.0, P("portaria_controle_acesso", interativo=True))

    # escritorio de obra: 2 pavimentos (4 conteineres) + escada e passarela com GcR
    ox = 38.5
    for lvl, z in ((0, 0.2), (1, 2.8)):
        for k, cy in enumerate((-7.0, -1.0)):
            mb = MB()
            container(mb, windows=[("N", -1.5, 1.3), ("N", 1.5, 1.3)], doors=[("N", 0.0, 0.9)], ac=("S", 1.0), z0=z)
            place(mb, "Vivencia_Container_Escritorio_Nivel%d_%02d" % (lvl, k + 1), (ox, cy, 0.0), 90.0, P("escritorio_de_obra", nivel=lvl))
    mb = MB()
    wx0, wx1 = 36.05, 37.3
    zw = 2.8 + 0.15
    mb.box((wx0, -10.0, zw - 0.08), (wx1, 2.0, zw), "grafite", top="aco")
    for y in (-10.0, -4.0, 2.0):
        mb.box((wx0 - 0.05, y - 0.05, 0.0), (wx0 + 0.05, y + 0.05, zw - 0.08), "grafite", nobottom=True)
    g13.gcr(mb, (wx0, -9.9), (wx0, 1.95), zw, (1.0, 0.0), off=0.08, spacing=1.8, clamp=False, cpost="grafite", crail="amarelo_linha_vida", ctoe="grafite", screen=False)
    g13.gcr(mb, (wx0 + 0.05, 1.95), (wx1, 1.95), zw, (0.0, -1.0), off=0.05, clamp=False, cpost="grafite", crail="amarelo_linha_vida", ctoe="grafite", screen=False)
    steps = 15
    sy0, sy1 = -10.0, -14.2
    for s in range(steps):
        u0, u1 = s / steps, (s + 1) / steps
        yy = sy1 + (sy0 - sy1) * u1
        mb.box((wx0 + 0.05, yy - 0.28, zw * u0), (wx1 - 0.05, yy, zw * u1), "aco", sides="grafite")
    for xr in (wx0, wx1):
        mb.strut((xr, sy1, 1.0), (xr, sy0, zw + 1.0), 0.045, "amarelo_linha_vida")
        mb.strut((xr, sy1, 0.0), (xr, sy1, 1.05), 0.05, "grafite")
    place(mb, "Vivencia_Escritorio_Escada_Passarela_GcR", (0.0, 0.0, 0.0), 0.0,
          P("escada_e_passarela_com_guarda_corpo", nr_ref="NR-18 18.8 escadas / 18.9.4.2", interativo=True))

    # caixa d'agua em torre
    mb = MB()
    tx, ty = -15.8, -25.6
    for (dx, dy) in ((-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8)):
        mb.box((tx + dx - 0.06, ty + dy - 0.06, 0.0), (tx + dx + 0.06, ty + dy + 0.06, 4.0), "grafite", nobottom=True)
    for z in (1.5, 3.0):
        mb.ring_box(tx - 0.86, ty - 0.86, tx + 0.86, ty + 0.86, z, z + 0.06, 0.06, "grafite")
    mb.box((tx - 1.0, ty - 1.0, 4.0), (tx + 1.0, ty + 1.0, 4.1), "grafite")
    mb.cyl((tx, ty, 4.1), (tx, ty, 5.6), 0.95, "lona_azul", n=14, cap="azul_escuro")
    mb.cyl((tx + 0.5, ty + 0.5, 0.0), (tx + 0.5, ty + 0.5, 4.1), 0.04, "tubo_pvc", n=6)
    place(mb, "Vivencia_Caixa_Agua_Torre", (0.0, 0.0, 0.0), 0.0, P("caixa_dagua_5000L"))

    # cacambas de entulho + tubo coletor na fachada leste da Torre A
    for (nm, loc, rz, cor) in (("01_Torre_A", (34.1, 6.6, 0.0), 90.0, "verde_escuro"), ("02_Oeste", (-37.2, -15.5, 0.0), 0.0, "laranja_caminhao")):
        mb = MB()
        mb.hull([(-1.4, -0.85, 0.1), (1.4, -0.85, 0.1), (1.4, 0.85, 0.1), (-1.4, 0.85, 0.1),
                 (-1.9, -1.0, 1.2), (1.9, -1.0, 1.2), (1.9, 1.0, 1.2), (-1.9, 1.0, 1.2)], cor)
        mb.box((-1.7, -0.9, 1.05), (1.7, 0.9, 1.21), "concreto_escuro")
        for sx in (-1.2, 1.2):
            mb.box((sx - 0.1, -1.05, 0.0), (sx + 0.1, 1.05, 0.12), "grafite")
        place(mb, "Vivencia_Cacamba_Entulho_" + nm, loc, rz, P("cacamba_entulho", nr_ref="NR-18 18.14 residuos"))
    mb = MB()
    cx, cy = 32.9, 6.6
    ztop = L.TA_Z(6) + 1.0
    z = 1.35
    while z < ztop:
        z1 = min(ztop, z + 1.0)
        with mb.at((cx, cy, z)):
            mb.lathe([(0.3, 0.0), (0.3, 0.75), (0.36, 1.0)], "amarelo_maquina", n=8, cap0=False, cap1=False)
        z = z1
    for n in range(1, 7):
        zz = L.TA_Z(n)
        mb.box((32.0, cy - 0.45, zz + 0.05), (cx + 0.3, cy + 0.45, zz + 0.12), "grafite")
        mb.hull([(32.1, cy - 0.45, zz + 0.12), (32.1, cy + 0.45, zz + 0.12), (32.1, cy - 0.45, zz + 1.0), (32.1, cy + 0.45, zz + 1.0),
                 (32.5, cy - 0.35, zz + 0.5), (32.5, cy + 0.35, zz + 0.5)], "laranja_seguranca")
        mb.strut((32.0, cy, zz - 0.3), (cx, cy, zz - 0.3), 0.06, "grafite")
    place(mb, "TorreA_Tubo_Coletor_Entulho", (0.0, 0.0, 0.0), 0.0, P("tubo_coletor_entulho", categoria="residuos", nr_ref="NR-18 residuos por calha fechada"))
    return {"objetos": len(C.objects)}
