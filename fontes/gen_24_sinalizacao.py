# gen_24_sinalizacao.py - placas (atlas T_Placas), extintores, barreiras, cones, protecao da cava, estacao de EPI
import bpy, sys, math, random, json
from mathutils import Vector
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
g13 = sys.modules["gen_13"]
UV = json.loads(bpy.data.texts["placas_uv.json"].as_string())


def placa(mb, key, center, facing, w, board=True, depth=0.02, back="cinza_escuro", post_to_ground=False, post_c="cinza_medio"):
    u0, v0, u1, v1, pw, ph = UV[key]
    h = w * ph / pw
    fx, fy = facing
    rx, ry = -fy, fx
    cx, cy, cz = center
    if board:
        b = MB()
        mb.strut((cx - fx * depth * 0.5 - rx * (w / 2 + 0.02), cy - fy * depth * 0.5 - ry * (w / 2 + 0.02), cz),
                 (cx - fx * depth * 0.5 + rx * (w / 2 + 0.02), cy - fy * depth * 0.5 + ry * (w / 2 + 0.02), cz),
                 depth, back, h=h + 0.04)
    o = 0.004
    px, py = cx + fx * o, cy + fy * o
    pts = [(px - rx * w / 2, py - ry * w / 2, cz - h / 2), (px + rx * w / 2, py + ry * w / 2, cz - h / 2),
           (px + rx * w / 2, py + ry * w / 2, cz + h / 2), (px - rx * w / 2, py - ry * w / 2, cz + h / 2)]
    mb.quad_uv(pts, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], K.S_PLACAS)
    if post_to_ground:
        bx, by = cx - fx * (depth + 0.03), cy - fy * (depth + 0.03)
        mb.cyl((bx, by, 0.0), (bx, by, cz + h / 2), 0.035, post_c, n=6)
        mb.box((bx - 0.15, by - 0.15, 0.0), (bx + 0.15, by + 0.15, 0.06), "concreto", nobottom=True)
    return h


def extintor(mb, x, y, z, facing):
    fx, fy = facing
    bx, by = x + fx * 0.11, y + fy * 0.11
    mb.cyl((bx, by, z), (bx, by, z + 0.5), 0.09, "vermelho_seguranca", n=10, cap="vermelho_escuro")
    mb.cyl((bx, by, z + 0.5), (bx, by, z + 0.6), 0.03, "preto_suave", n=6)
    mb.box((bx - 0.05 * abs(fy) - 0.05 * abs(fx) * 0.2, by - 0.05 * abs(fx) - 0.05 * abs(fy) * 0.2, z + 0.58), (bx + 0.08 * fx + 0.02, by + 0.08 * fy + 0.02, z + 0.62), "preto_suave")
    mb.box((x - 0.06 + fx * 0.0, y - 0.06, z + 0.1), (x + 0.06 + fx * 0.02, y + 0.06 + fy * 0.02, z + 0.45), "grafite")


def cone(mb, x, y, h=0.7):
    mb.box((x - 0.19, y - 0.19, 0.0), (x + 0.19, y + 0.19, 0.04), "preto_suave", nobottom=True)
    with mb.at((x, y, 0.04)):
        mb.lathe([(0.15, 0.0), (0.12, h * 0.3), (0.095, h * 0.45), (0.07, h * 0.62), (0.045, h * 0.8), (0.02, h - 0.04)], "laranja_seguranca", n=8,
                 cap0=False, cap1=True, color_fn=lambda k, i: "branco_sinal" if k in (2, 3) else "laranja_seguranca")


def new_jersey(mb, x, y, rz, cor):
    with mb.at((x, y, 0.0), rz=rz):
        mb.xprism([(-0.25, 0.0), (0.25, 0.0), (0.22, 0.18), (0.1, 0.35), (0.09, 0.8), (-0.09, 0.8), (-0.1, 0.35), (-0.22, 0.18)], -0.5, 0.5, cor)
    return


def build():
    C = K.coll("24_Sinalizacao_Seguranca")
    K.clear_coll(C)
    Z = L.TA_Z
    cnt = {"placas": 0}
    P = lambda tipo, **kw: dict({"categoria": "sinalizacao", "tipo": tipo, "nr_ref": "NR-26 sinalizacao de seguranca"}, **kw)

    def obj(mb, name, props):
        return K.finish(mb, name, C, props=props)

    def P1(key, center, facing, w, name, **kw):
        mb = MB()
        placa(mb, key, center, facing, w, **kw)
        cnt["placas"] += 1
        return obj(mb, "Placa_" + name, P("placa", placa=key, interativo=True))

    S, N, E, W = (0.0, -1.0), (0.0, 1.0), (1.0, 0.0), (-1.0, 0.0)
    # ---------------- perimetro e acessos
    P1("epi_obrigatorio", (21.8, -30.04, 1.25), S, 1.8, "Acesso_Uso_Obrigatorio_EPI")
    P1("proibida_entrada", (12.0, -30.04, 1.25), S, 1.4, "Acesso_Proibida_Entrada")
    P1("nr35_acesso", (24.5, -30.04, 1.25), S, 1.1, "Acesso_NR35")
    P1("acesso_veiculos", (33.0, -30.22, 4.55), S, 3.6, "Portao_Acesso_Veiculos", board=False)
    P1("trafego_maquinas", (40.04, -26.0, 1.25), E, 1.4, "Tapume_Trafego_Maquinas")
    P1("saida_emergencia", (39.86, 20.6, 2.62), W, 1.2, "Saida_Emergencia_Interna")
    P1("saida_emergencia", (40.14, 20.6, 2.62), E, 1.2, "Saida_Emergencia_Externa")
    P1("placa_obra", (-34.0, -29.662, 4.0), S, 5.9, "Placa_de_Obra", board=False)
    P1("ponto_encontro", (23.0, -24.25, 1.75), N, 0.7, "Ponto_de_Encontro", post_to_ground=True)
    mb = MB()
    mb.box((21.0, -24.5, 0.0), (25.0, -20.5, 0.025), "verde_seguranca", nobottom=True)
    mb.ring_box(21.0, -24.5, 25.0, -20.5, 0.025, 0.03, 0.15, "branco_sinal", nobottom=True)
    obj(mb, "Piso_Ponto_de_Encontro", P("ponto_de_encontro", categoria="emergencia", interativo=True))
    P1("velocidade_10", (29.7, -24.7, 2.0), S, 0.55, "Velocidade_Maxima_10", post_to_ground=True)
    # ---------------- vivencia
    P1("dds_quadro", (11.572, -27.5, 1.55), W, 2.0, "Quadro_DDS", board=False)
    for (key, x) in (("sala_vestiario", -25.3), ("sala_sanitarios", -19.6), ("sala_refeitorio", -8.0), ("sala_almoxarifado", 15.6), ("sala_portaria", 22.3)):
        P1(key, (x, -27.14, 2.57), N, 0.9, key.replace("sala_", "Porta_").title())
    P1("sala_epi", (18.6, -27.14, 2.3), N, 1.0, "Janela_Entrega_EPI")
    P1("sala_escritorio", (37.25, -7.0, 2.57), W, 1.1, "Porta_Escritorio_Obra")
    P1("sala_sesmt", (37.25, -1.0, 5.17), W, 1.1, "Porta_Seguranca_Trabalho")
    # ---------------- torre A
    P1("elevador_capacidade", (1.35, 8.965, 1.3), S, 1.1, "Elevador_Capacidade")
    P1("nr35_acesso", (2.75, 8.965, 1.3), S, 1.1, "Elevador_NR35")
    P1("obrigatorio_cinto", (9.0, 2.6, 1.2), S, 0.55, "Andaime_Uso_Obrigatorio_Cinto")
    P1("andaime_liberado", (9.8, 2.6, 1.1), S, 0.35, "Andaime_Etiqueta_Liberado", back="verde_seguranca")
    for (n, pos, fac) in ((9, (19.0, 4.17, Z(9) + 0.95), N), (5, (13.8, 4.17, Z(5) + 0.95), N), (7, (6.17, 19.0, Z(7) + 0.95), E), (8, (31.83, 13.0, Z(8) + 0.95), W)):
        P1("perigo_queda", pos, fac, 0.9, "TorreA_Pav%02d_Perigo_Risco_Queda" % n)
    for x in (16.4, 21.6, 26.8):
        P1("ponto_ancoragem", (x, 4.302, Z(9) + 1.25), N, 0.5, "TorreA_Pav09_Placa_Ancoragem_X%02d" % int(x))
    P1("linha_de_vida", (30.7, 5.347, Z(9) + 0.85), N, 0.36, "TorreA_Pav09_Placa_Linha_Vida")
    mbp = MB()
    for n in range(10):
        for cx in (17.75, 20.3):
            placa(mbp, "perigo_poco_elevador", (cx, 19.455, Z(n) + 1.6), S, 0.8)
        placa(mbp, "pav_%02d" % n, (19.02, 19.585, Z(n) + 1.75), S, 0.6, board=False)
    obj(mbp, "Placas_TorreA_Pocos_e_Pavimentos", P("placas_poco_elevador_e_identificacao_pavimento"))
    # ---------------- gruas, icamento, cava, eletrica
    for (nm, bx, by) in (("Amarela",) + tuple(L.GRUA_AMARELA), ("Vermelha",) + tuple(L.GRUA_VERMELHA)):
        P1("icamento_grua", (bx + 1.8, by - 3.82, 1.3), S, 1.1, "Grua_%s_Proibido_Raio_Acao" % nm)
        P1("usar_trava_quedas", (bx - 1.6, by - 3.82, 1.3), S, 0.5, "Grua_%s_Usar_Trava_Quedas" % nm)
    P1("area_icamento", (-17.9, 11.2, 1.3), N, 1.0, "Guindaste_Area_Icamento_Norte", post_to_ground=True)
    P1("area_icamento", (-6.6, 0.6, 1.3), E, 1.0, "Guindaste_Area_Icamento_Leste", post_to_ground=True)
    P1("proibido_sob_carga", (-5.5, 2.4, 1.6), S, 0.5, "Proibido_Sob_Carga_Suspensa", post_to_ground=True)
    P1("perigo_eletricidade", (27.55, -26.165, 1.45), N, 0.3, "QGD_Perigo_Eletricidade", board=False)
    P1("atencao_escavacao", (-2.0, -4.83, 0.95), N, 1.0, "Cava_Atencao_Norte")
    P1("atencao_escavacao", (-11.17, -14.0, 0.95), W, 1.0, "Cava_Atencao_Oeste")
    P1("atencao_escavacao", (0.0, -23.75, 1.1), S, 1.0, "Cava_Atencao_Sul", post_to_ground=True)
    P1("perigo_queda", (-23.0, -2.17, 6.15 + 0.95), S, 0.8, "BlocoB_Pav02_Perigo_Risco_Queda")
    P1("andaime_liberado", (-21.0, -17.2, 1.2), S, 0.35, "BlocoB_Torre_Acesso_Liberada", back="verde_seguranca")
    P1("obrigatorio_capacete", (-40.04, 18.0, 1.25), W, 0.55, "Portao_Oeste_Uso_Capacete")

    # ---------------- extintores
    ext = [((14.6, -27.2 + 0.0, 0.7), N, "Almoxarifado"), ((-6.8, -27.2, 0.7), N, "Refeitorio"), ((21.2, -27.2, 0.7), N, "Portaria"),
           ((-24.0, 20.42, 0.7), S, "Central_Carpintaria"), ((-38.0, 20.42, 0.7), S, "Central_Armacao"), ((26.5, -26.25, 0.7), N, "QGD"),
           ((-21.0, -17.2, 0.0 + 0.7), S, "BlocoB_Torre_Acesso"), ((36.0, -4.0, 0.7), W, "Escritorio")]
    for n in range(10):
        ext.append(((21.3, 19.6, Z(n) + 0.55), S, "TorreA_Pav%02d" % n))
    for (pos, fac, nm) in ext:
        mb = MB()
        x, y, z = pos
        extintor(mb, x, y, z, fac)
        placa(mb, "extintor", (x + fac[0] * 0.02, y + fac[1] * 0.02, z + 1.0), fac, 0.28)
        obj(mb, "Extintor_" + nm, P("extintor_com_placa", categoria="emergencia", nr_ref="NR-23 protecao contra incendios", interativo=True))

    # ---------------- protecao da cava: GcR (norte, oeste, leste) + barreiras (sul) + escada de acesso
    gc = dict(cpost="madeira_escura", crail="amarelo_linha_vida", ctoe="madeira", clamp=False, spacing=2.0)
    segs = [("Norte_01", (-11.0, -5.0), (-5.6, -5.0), (0.0, 1.0)), ("Norte_02", (-4.4, -5.0), (11.0, -5.0), (0.0, 1.0)),
            ("Oeste", (-11.0, -23.0), (-11.0, -5.0), (-1.0, 0.0)), ("Leste_01", (11.0, -5.0), (11.0, -8.6), (1.0, 0.0)),
            ("Rampa_Norte", (11.0, -8.6), (23.6, -11.0), None), ("Rampa_Sul", (23.6, -18.0), (11.0, -20.4), None), ("Leste_02", (11.0, -20.4), (11.0, -23.0), (1.0, 0.0))]
    for (nm, a, b, inw) in segs:
        if inw is None:
            dx, dy = b[0] - a[0], b[1] - a[1]
            Ls = math.hypot(dx, dy)
            nx, ny = -dy / Ls, dx / Ls
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if (mx + nx - 16.0) ** 2 + (my + ny + 14.5) ** 2 < (mx - 16.0) ** 2 + (my + 14.5) ** 2:
                nx, ny = -nx, -ny
            inw = (nx, ny)
        mb = MB()
        g13.gcr(mb, a, b, 0.0, inw, off=0.0, **gc)
        obj(mb, "Cava_GcR_" + nm, P("GcR_borda_escavacao", categoria="protecao_coletiva", nr_ref="NR-18 18.6 escavacoes / 18.9.4.2", interativo=True))
    mb = MB()
    k = 0
    x = -10.5
    while x < 10.8:
        new_jersey(mb, x, -23.0, 0.0, "vermelho_seguranca" if k % 2 == 0 else "branco_sinal")
        x += 1.02
        k += 1
    obj(mb, "Cava_Barreiras_New_Jersey_Sul", P("barreira_plastica", categoria="protecao_coletiva", interativo=True))
    mb = MB()
    x0, x1 = -5.5, -4.5
    steps = 15
    for s in range(steps):
        y0 = -9.0 + s * 0.2
        z0 = -3.0 + s * 0.2
        mb.box((x0, y0, z0 + 0.14), (x1, y0 + 0.24, z0 + 0.2), "madeira")
    for xs in (x0 - 0.05, x1 + 0.05):
        mb.strut((xs, -9.0, -2.9), (xs, -6.0, 0.1), 0.06, "madeira_escura", h=0.2)
    mb.box((x0 - 0.1, -6.0, -0.06), (x1 + 0.1, -5.0, 0.04), "madeira", sides="madeira_escura")
    for xs in (x0 - 0.12, x1 + 0.12):
        for s in range(0, steps + 1, 5):
            yy = -9.0 + s * 0.2
            zz = -3.0 + s * 0.2
            mb.box((xs - 0.03, yy - 0.03, zz), (xs + 0.03, yy + 0.03, zz + 1.05), "madeira_escura", nobottom=True)
        mb.strut((xs, -9.0, -1.95), (xs, -6.0, 1.05), 0.05, "amarelo_linha_vida")
    obj(mb, "Cava_Escada_Acesso_Madeira", P("escada_de_acesso_escavacao", categoria="acesso", nr_ref="NR-18 18.6 escavacoes com acesso seguro", interativo=True))

    # ---------------- isolamento da area do guindaste: cones + fita zebrada
    mb = MB()
    rect = [(-17.8, -1.3), (-7.0, -1.3), (-7.0, 10.8), (-17.8, 10.8)]
    pts = []
    for i in range(4):
        a, b = rect[i], rect[(i + 1) % 4]
        Ls = math.dist(a, b)
        n = max(1, int(round(Ls / 2.2)))
        for j in range(n):
            u = j / n
            pts.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
    for (x, y) in pts:
        cone(mb, x, y)
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        mb.strut((a[0], a[1], 0.62), (b[0], b[1], 0.62), 0.004, "amarelo_linha_vida", h=0.07)
        mb.strut((a[0], a[1], 0.55), (b[0], b[1], 0.55), 0.004, "zebrado_preto", h=0.04)
    obj(mb, "Guindaste_Isolamento_Cones_Fita", P("isolamento_area_icamento", categoria="protecao_coletiva", interativo=True))
    mb = MB()
    for (x, y) in ((3.3, 8.4), (6.4, 8.4), (-2.3, -4.6), (0.8, -4.6), (26.2, -14.0), (26.2, -15.8)):
        cone(mb, x, y)
    obj(mb, "Cones_Diversos", P("cones"))

    # ---------------- estacao de EPI (cintos paraquedista + capacetes) junto ao almoxarifado
    mb = MB()
    x0, x1, y = 19.6, 21.2, -26.7
    for x in (x0, x1):
        mb.box((x - 0.04, y - 0.04, 0.0), (x + 0.04, y + 0.04, 2.0), "madeira_escura", nobottom=True)
    mb.box((x0, y - 0.05, 1.85), (x1, y + 0.05, 1.95), "madeira_escura")
    mb.box((x0, y - 0.18, 0.9), (x1, y + 0.18, 0.95), "madeira")
    for k in range(3):
        hx = x0 + 0.3 + k * 0.5
        mb.box((hx - 0.01, y + 0.02, 1.72), (hx + 0.01, y + 0.1, 1.86), "cromado")
        with mb.at((hx, y + 0.1, 0.0)):
            cs = ("laranja_seguranca", "amarelo_linha_vida", "laranja_seguranca")[k]
            mb.ring_box(-0.035, -0.012, 0.035, 0.012, 1.63, 1.7, 0.012, "cromado")
            for sx in (-1, 1):
                mb.strut((sx * 0.06, 0.0, 1.68), (sx * 0.14, 0.0, 1.25), 0.04, cs, h=0.01, up=(0, 1, 0))
                mb.strut((sx * 0.14, 0.0, 1.25), (sx * 0.1, 0.0, 1.0), 0.04, cs, h=0.01, up=(0, 1, 0))
                mb.strut((sx * 0.1, 0.0, 1.0), (sx * 0.02, 0.0, 1.08), 0.035, cs, h=0.01, up=(0, 1, 0))
            mb.strut((-0.13, 0.0, 1.45), (0.13, 0.0, 1.45), 0.035, cs, h=0.01)
            mb.strut((-0.16, 0.0, 1.22), (0.16, 0.0, 1.22), 0.045, cs, h=0.012)
            mb.strut((0.0, 0.01, 1.63), (-0.12, 0.03, 0.95), 0.03, "azul_escuro", h=0.008)
            mb.strut((0.0, 0.01, 1.63), (0.12, 0.03, 0.95), 0.03, "azul_escuro", h=0.008)
            mb.box((-0.03, 0.0, 1.35), (0.03, 0.05, 1.5), "preto_suave")
            for sx in (-0.12, 0.12):
                mb.strut((sx, 0.03, 0.95), (sx, 0.03, 0.83), 0.03, "cromado", h=0.012)
    for k in range(4):
        hx = x0 + 0.25 + k * 0.37
        with mb.at((hx, y, 0.95)):
            mb.lathe([(0.15, 0.0), (0.15, 0.02), (0.12, 0.03), (0.12, 0.09), (0.09, 0.15), (0.04, 0.18), (0.005, 0.19)],
                     ("capacete_branco", "capacete_amarelo", "capacete_azul", "capacete_branco")[k], n=10, cap0=True, cap1=False)
    placa(mb, "obrigatorio_cinto", (20.4, y - 0.06, 2.35), S, 0.42, post_to_ground=False)
    mb.box((20.38, y - 0.04, 1.95), (20.42, y, 2.05), "madeira_escura")
    obj(mb, "Estacao_EPI_Cintos_Capacetes", P("estacao_EPI_cinto_paraquedista_talabarte_duplo_capacetes", categoria="epi",
                                               nr_ref="NR-6 / NR-35 (cinturao tipo paraquedista com talabarte duplo)", interativo=True))
    return {"objetos": len(C.objects), "placas_individuais": cnt["placas"]}
