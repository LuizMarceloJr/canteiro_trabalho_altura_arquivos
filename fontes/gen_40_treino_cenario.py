# -*- coding: utf-8 -*-
# gen_40_treino_cenario.py - cenario do roteiro "Trabalho em Altura" (props, interativos e variantes de estado)
# Convencao de nomes (viram node.name no glTF / Three.js):
#   C01..C21  = cenas do roteiro | CONC/ORG/RET = conclusao, organizacao final, retorno
#   Objetos ocultos no estado inicial levam userData.visivel_inicial = false (o export inclui todos).
import bpy, sys, math, json, random
from mathutils import Vector, Matrix, Euler

K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
g13 = sys.modules["gen_13"]
V = sys.modules["veiculos"]

Z4 = L.TA_Z(4)
PAI = "40_Treino_Cenario"


def UVT():
    return json.loads(bpy.data.texts["treino_uv.json"].as_string())


def UVP():
    return json.loads(bpy.data.texts["placas_uv.json"].as_string())


# ------------------------------------------------------------------ utilidades
def colecoes():
    K.coll(PAI)
    nomes = ["40a_Rota_Acesso_Caminhao", "40b_Area_Equipamentos", "40c_Aberturas_Pav02_Pav03", "40d_Frente_Trabalho_Pav04",
             "40e_Isolamento_Terreo", "40f_Sinalizacao_Emergencia"]
    return {n: K.coll(n, PAI) for n in nomes}


def mostrar(o, v):
    o.hide_viewport = not v
    o.hide_render = not v


def obj(mb, nome, C, visivel=True, cena=None, props=None, loc=None, rz=0.0, parent=None):
    pr = {"treinamento": True, "visivel_inicial": bool(visivel)}
    if cena:
        pr["cena"] = cena
    if props:
        pr.update(props)
    o = K.finish(mb, nome, C, parent=parent, loc=loc, rz=rz, props=pr)
    if o is not None:
        mostrar(o, visivel)
    return o


def decal(mb, uv, key, center, normal, w, up=(0.0, 0.0, 1.0), slot=None, off=0.003):
    u0, v0, u1, v1, pw, ph = uv[key]
    h = w * ph / pw
    n = Vector((normal[0], normal[1], normal[2] if len(normal) > 2 else 0.0)).normalized()
    upv = Vector(up)
    right = upv.cross(n)
    if right.length < 1e-6:
        right = Vector((1.0, 0.0, 0.0))
    right.normalize()
    upr = n.cross(right).normalized()
    c = Vector(center) + n * off
    pts = [c - right * w / 2 - upr * h / 2, c + right * w / 2 - upr * h / 2, c + right * w / 2 + upr * h / 2, c - right * w / 2 + upr * h / 2]
    mb.quad_uv([tuple(p) for p in pts], [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], K.S_TREINO if slot is None else slot)
    return h


def cone(mb, x, y, z=0.0, h=0.7, deitado=False, rz=0.0):
    with mb.at((x, y, z), rz=rz, rx=(90 if deitado else 0)):
        mb.box((-0.19, -0.19, 0.0), (0.19, 0.19, 0.04), "preto_suave", nobottom=True)
        with mb.at((0, 0, 0.04)):
            mb.lathe([(0.15, 0.0), (0.12, h * 0.3), (0.095, h * 0.45), (0.07, h * 0.62), (0.045, h * 0.8), (0.02, h - 0.04)], "laranja_seguranca", n=8,
                     cap0=False, cap1=True, color_fn=lambda k, i: "branco_sinal" if k in (2, 3) else "laranja_seguranca")


def fita_zebrada(mb, pts, z):
    for a, b in zip(pts[:-1], pts[1:]):
        mb.strut((a[0], a[1], z), (b[0], b[1], z), 0.004, "amarelo_linha_vida", h=0.07)
        mb.strut((a[0], a[1], z - 0.07), (b[0], b[1], z - 0.07), 0.004, "zebrado_preto", h=0.04)


# ------------------------------------------------------------------ guarda-corpo com variacoes (espelha gen_13.gcr)
def gcr_var(mb, a, b, z0, inward, off=0.10, spacing=1.9, cpost="laranja_escuro", crail="laranja_seguranca", ctoe="amarelo_linha_vida",
            sem_travessao=False, sem_intermediario=False, sem_rodape=False, sem_tela=False,
            incl=None, clamp_solto=(), flecha=0.0, folga_travessao=None, amassado=None, marca=None):
    """incl = {indice_poste: graus_para_fora}; flecha = deslocamento para fora do travessao no meio (m);
    folga_travessao = indice do poste onde o travessao fica solto (gap); amassado = s (m) de um vinco no travessao."""
    ax, ay = a
    bx, by = b
    Ls = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / Ls, (by - ay) / Ls
    nx, ny = inward
    ox, oy = -nx, -ny
    incl = incl or {}
    npost = max(2, int(math.ceil((Ls - 0.12) / spacing)) + 1)
    ss = [0.06 + (Ls - 0.12) * i / (npost - 1) for i in range(npost)]

    def P(s, o, z):
        return Vector((ax + ux * s + nx * o, ay + uy * s + ny * o, z))

    def post_dir(i):
        t = math.radians(incl.get(i, 0.0))
        return Vector((ox * math.sin(t), oy * math.sin(t), math.cos(t)))

    def on_post(i, h, o=None):
        o = (off + 0.025) if o is None else o
        base = P(ss[i], o, z0)
        return base + post_dir(i) * h

    for i, s in enumerate(ss):
        p0 = P(s, off + 0.025, z0)
        mb.strut(tuple(p0), tuple(p0 + post_dir(i) * 1.22), 0.05, cpost)
        if i in clamp_solto:
            mb.strut(tuple(P(s, -0.05, z0 - 0.05)), tuple(P(s, off + 0.18, z0 - 0.02)), 0.07, "grafite", h=0.04)
            mb.strut(tuple(P(s, -0.10, z0 - 0.22)), tuple(P(s, -0.06, z0 - 0.02)), 0.07, "grafite", h=0.04, up=(ux, uy, 0))
        else:
            mb.strut(tuple(P(s, -0.05, z0 + 0.02)), tuple(P(s, off + 0.22, z0 + 0.02)), 0.07, "grafite", h=0.04)
            mb.strut(tuple(P(s, -0.03, z0 - 0.16)), tuple(P(s, -0.03, z0 + 0.04)), 0.07, "grafite", h=0.04, up=(ux, uy, 0))

    def rail(h, w, hh, c, o_abs):
        pts = []
        first = on_post(0, h, o_abs) - Vector((ux, uy, 0)) * 0.06
        pts.append(first)
        for i in range(npost):
            pts.append(on_post(i, h, o_abs))
        pts.append(on_post(npost - 1, h, o_abs) + Vector((ux, uy, 0)) * 0.06)
        if flecha and h > 1.0:
            mid = len(pts) // 2
            for k in range(1, len(pts) - 1):
                t = 1.0 - abs(k - mid) / max(1, mid)
                pts[k] = pts[k] + Vector((ox, oy, -0.25 * abs(flecha))) * (flecha * t)
        for k in range(len(pts) - 1):
            pa, pb = pts[k], pts[k + 1]
            if folga_travessao is not None and h > 1.0 and k == folga_travessao + 1:
                pa = pa + (pb - pa).normalized() * 0.05
            if amassado is not None and h > 1.0:
                sa = (pa - P(0, 0, 0)).dot(Vector((ux, uy, 0)))
                sb = (pb - P(0, 0, 0)).dot(Vector((ux, uy, 0)))
                if sa < amassado < sb:
                    pm = pa + (pb - pa) * ((amassado - sa) / (sb - sa)) + Vector((nx, ny, -0.02)) * 0.035
                    mb.strut(tuple(pa), tuple(pm), w, c, h=hh)
                    mb.strut(tuple(pm), tuple(pb), w, c, h=hh)
                    continue
            mb.strut(tuple(pa), tuple(pb), w, c, h=hh)
        return pts

    if not sem_travessao:
        rail(1.15, 0.04, 0.10, crail, off - 0.02)
    if not sem_intermediario:
        rail(0.70, 0.04, 0.08, crail, off - 0.02)
    if not sem_rodape:
        rail(0.10, 0.025, 0.20, ctoe, off - 0.015)
    if not sem_tela:
        for i in range(npost - 1):
            o = off - 0.045
            q = [on_post(i, 0.2, o), on_post(i + 1, 0.2, o), on_post(i + 1, 1.1, o), on_post(i, 1.1, o)]
            if i == 0:
                q[0] = q[0] - Vector((ux, uy, 0)) * 0.06
                q[3] = q[3] - Vector((ux, uy, 0)) * 0.06
            if i == npost - 2:
                q[1] = q[1] + Vector((ux, uy, 0)) * 0.06
                q[2] = q[2] + Vector((ux, uy, 0)) * 0.06
            L0 = ss[i] - (0.06 if i == 0 else 0.0)
            L1 = ss[i + 1] + (0.06 if i == npost - 2 else 0.0)
            mb.quad_uv([tuple(p) for p in q], [(L0 / 0.2, 0), (L1 / 0.2, 0), (L1 / 0.2, 4.5), (L0 / 0.2, 4.5)], K.S_TELA_GCR)
    if marca is not None:
        p = P(marca, off - 0.07, z0 + 1.15)
        mb.box((p.x - 0.06, p.y - 0.004, p.z - 0.05), (p.x + 0.06, p.y + 0.004, p.z + 0.05), "sujeira")
    return ss


def gcr_trecho(nome_base):
    """extremidades dos trechos a/b do GcR sul 04/05 do pav 4 (mesma regra do gen_13)."""
    X0, Y0, X1, Y1 = L.TORRE_A
    XL = L.TA_XL
    bays = []
    for i, (xa, xb) in enumerate(zip(XL[:-1], XL[1:])):
        ra, rb = L.TA_PILAR(xa, Y0), L.TA_PILAR(xb, Y0)
        bays.append(((ra[2] + 0.02, Y0), (rb[0] - 0.02, Y0)))
    tr = {}
    for (i, key) in ((3, "Sul_04"), (4, "Sul_05")):
        a, b = bays[i]
        split = L.TR_GCR_SPLIT[key]
        tr[key + "a"] = (a, (split - 0.03, Y0))
        tr[key + "b"] = ((split + 0.03, Y0), b)
    return tr[nome_base]


# ------------------------------------------------------------------ equipamentos (modelos para inspecao)
def capacete(mb, cor, rachado=False):
    """capacete com aba frontal; origem na borda inferior, frente = +Y."""
    mb.lathe([(0.135, 0.0), (0.138, 0.02), (0.132, 0.06), (0.115, 0.10), (0.085, 0.135), (0.045, 0.155), (0.0, 0.162)], cor, n=16,
             cap0=False, cap1=False, smooth=True)
    mb.lathe([(0.125, 0.0), (0.126, 0.05), (0.0, 0.05)], "preto_suave", n=12, cap0=False, cap1=False, smooth=False)
    mb.hull([(-0.11, 0.10, 0.0), (0.11, 0.10, 0.0), (-0.09, 0.20, 0.01), (0.09, 0.20, 0.01),
             (-0.11, 0.10, 0.015), (0.11, 0.10, 0.015), (-0.09, 0.20, 0.022), (0.09, 0.20, 0.022)], cor)
    mb.hull([(-0.012, -0.13, 0.08), (0.012, -0.13, 0.08), (-0.012, 0.12, 0.10), (0.012, 0.12, 0.10),
             (-0.008, -0.05, 0.168), (0.008, -0.05, 0.168), (-0.008, 0.05, 0.168), (0.008, 0.05, 0.168)], cor)
    for sx in (-1, 1):
        mb.box((sx * 0.128 - 0.004, -0.02, -0.06), (sx * 0.128 + 0.004, 0.02, 0.01), "preto_suave")
    mb.box((-0.02, 0.125, 0.07), (0.02, 0.13, 0.09), "branco_sinal")
    if rachado:
        # rachadura: zigue-zague escuro sobre a casca (lado direito/frente)
        pts = []
        for k in range(9):
            t = k / 8.0
            th = math.radians(20 + 55 * t)
            ph = math.radians(35 + 28 * t + (7 if k % 2 else -7))
            r, hh = 0.1385, 0.163
            pts.append((r * math.sin(th) * math.cos(ph), r * math.sin(th) * math.sin(ph), hh * math.cos(th) * 0.98 + 0.004))
        for a, b in zip(pts[:-1], pts[1:]):
            mb.strut(a, b, 0.005, "marca_rachadura", h=0.004)


def webbing(mb, pts, cor, w=0.045, t=0.004, normal=(0, 0, 1)):
    for a, b in zip(pts[:-1], pts[1:]):
        mb.strut(a, b, w, cor, h=t, up=normal)


def cinturao_mesa(mb, cor="laranja_seguranca", corte=False):
    """cinturao paraquedista aberto sobre a mesa (origem no centro, deitado no plano XY, cabeca = +Y)."""
    z = 0.004
    L_ = [(-0.10, 0.34, z), (-0.13, 0.12, z), (-0.10, -0.08, z), (-0.13, -0.32, z)]
    R_ = [(0.10, 0.34, z), (0.13, 0.12, z), (0.10, -0.08, z), (0.13, -0.32, z)]
    webbing(mb, L_, cor)
    webbing(mb, R_, cor)
    webbing(mb, [(-0.13, 0.12, z + 0.002), (0.13, 0.12, z + 0.002)], cor, w=0.04)
    mb.box((-0.03, 0.10, z), (0.03, 0.14, z + 0.012), "cromado")
    mb.box((-0.035, 0.30, z), (0.035, 0.40, z + 0.015), "grafite")               # argola dorsal
    mb.box((-0.02, 0.38, z + 0.015), (0.02, 0.43, z + 0.022), "cromado")
    for sx in (-1, 1):
        cx, cy = sx * 0.17, -0.40
        ring = [(cx + 0.09 * math.cos(a), cy + 0.12 * math.sin(a), z) for a in [2 * math.pi * k / 8 for k in range(9)]]
        webbing(mb, ring, cor, w=0.04)
        mb.box((cx - 0.03, cy + 0.10, z), (cx + 0.03, cy + 0.15, z + 0.012), "cromado")
    webbing(mb, [(-0.13, -0.32, z), (0.13, -0.32, z)], cor, w=0.05)
    mb.box((-0.06, -0.06, z), (0.06, -0.02, z + 0.006), "branco_fosco")          # etiqueta CA
    if corte:
        # pequeno corte na fita do ombro esquerdo + fibras
        cx, cy = -0.118, 0.07
        mb.hull([(cx - 0.03, cy + 0.016, z + 0.003), (cx + 0.006, cy - 0.002, z + 0.003), (cx - 0.03, cy - 0.024, z + 0.003),
                 (cx - 0.03, cy + 0.016, z + 0.008), (cx + 0.006, cy - 0.002, z + 0.008), (cx - 0.03, cy - 0.024, z + 0.008)], "corte_fita")
        for k in range(7):
            a = (cx - 0.026 + k * 0.005, cy - 0.016 + k * 0.005, z + 0.008)
            b = (a[0] - 0.02, a[1] + 0.02, z + 0.014)
            mb.strut(a, b, 0.003, "fita_desgastada", h=0.003)


def talabarte_mesa(mb, desgastado=False):
    z = 0.004
    mb.box((-0.045, 0.28, z), (0.045, 0.50, z + 0.045), "preto_radio", top="amarelo_escuro")   # absorvedor
    mb.box((-0.02, 0.50, z), (0.02, 0.56, z + 0.02), "cromado")
    for k, sx in enumerate((-1, 1)):
        pts = [(sx * 0.02, 0.28, z)]
        for j in range(1, 6):
            pts.append((sx * (0.06 + 0.07 * (j % 2)), 0.28 - j * 0.09, z))
        pts.append((sx * 0.10, -0.26, z))
        cor = "laranja_escuro"
        webbing(mb, pts, cor, w=0.032)
        if desgastado and sx == 1:
            for j in (2, 3):
                a, b = Vector(pts[j]), Vector(pts[j + 1])
                mb.strut(tuple(a + Vector((0, 0, 0.003))), tuple(b + Vector((0, 0, 0.003))), 0.036, "fita_desgastada", h=0.005)
                for q in range(6):
                    p = a + (b - a) * (q / 6.0)
                    mb.strut(tuple(p + Vector((0, 0, 0.006))), tuple(p + Vector((0.03, 0.01, 0.009))), 0.0025, "fita_desgastada", h=0.002)
        hx, hy = sx * 0.10, -0.34
        mb.hull([(hx - 0.03, hy + 0.08, z), (hx + 0.03, hy + 0.08, z), (hx - 0.045, hy - 0.10, z), (hx + 0.045, hy - 0.10, z),
                 (hx - 0.03, hy + 0.08, z + 0.02), (hx + 0.03, hy + 0.08, z + 0.02), (hx - 0.045, hy - 0.10, z + 0.02), (hx + 0.045, hy - 0.10, z + 0.02)], "cromado")
        mb.box((hx - 0.03, hy - 0.06, z + 0.02), (hx + 0.03, hy - 0.01, z + 0.026), "grafite")


def conector(mb, x, y, z, rz=0.0):
    with mb.at((x, y, z), rz=rz):
        ring = [(0.035 * math.cos(a), 0.06 * math.sin(a), 0.008) for a in [2 * math.pi * k / 10 for k in range(11)]]
        for a, b in zip(ring[:-1], ring[1:]):
            mb.cyl(a, b, 0.006, "cromado", n=5, caps=False, smooth=False)
        mb.box((0.025, -0.02, 0.0), (0.045, 0.02, 0.016), "grafite")


def bolsa_ferramentas(mb, x, y, z, fechada=True):
    with mb.at((x, y, z)):
        mb.rbox((-0.17, -0.10, 0.0), (0.17, 0.10, 0.24), "azul_escuro", r=0.02, top="preto_suave")
        mb.box((-0.12, 0.10, 0.06), (0.12, 0.115, 0.18), "azul_claro")
        mb.cyl((0.0, 0.0, 0.24), (0.0, 0.0, 0.30), 0.02, "cromado", n=5)
        if not fechada:
            mb.box((-0.15, -0.08, 0.24), (0.15, 0.08, 0.26), "grafite")
    for k in range(2):
        pts = [(x + 0.2 + 0.04 * math.cos(j * 0.9), y - 0.05 + k * 0.1 + 0.04 * math.sin(j * 0.9), z + 0.005 + j * 0.001) for j in range(14)]
        for a, b in zip(pts[:-1], pts[1:]):
            mb.cyl(a, b, 0.004, "amarelo_linha_vida", n=4, caps=False, smooth=False)


def radio(mb, x, y, z, rz=0.0, deitado=True):
    with mb.at((x, y, z), rz=rz, rx=(90 if deitado else 0)):
        mb.box((-0.03, 0.0, -0.02), (0.03, 0.14, 0.02), "preto_radio")
        mb.cyl((0.018, 0.14, 0.0), (0.018, 0.24, 0.0), 0.007, "preto_suave", n=5)
        mb.box((-0.02, 0.08, 0.02), (0.02, 0.11, 0.023), "e:verde_led")


def chave_boca(mb, p, rz=0.0, rx=0.0):
    with mb.at(p, rz=rz, rx=rx):
        mb.box((-0.012, -0.12, 0.0), (0.012, 0.12, 0.008), "cromado")
        for sy in (-1, 1):
            mb.hull([(-0.028, sy * 0.12, 0.0), (0.028, sy * 0.12, 0.0), (-0.02, sy * 0.155, 0.0), (0.02, sy * 0.155, 0.0),
                     (-0.028, sy * 0.12, 0.008), (0.028, sy * 0.12, 0.008), (-0.02, sy * 0.155, 0.008), (0.02, sy * 0.155, 0.008)], "cromado")


def furadeira(mb, p, rz=0.0, cabo_danificado=False):
    with mb.at(p, rz=rz):
        mb.box((-0.04, -0.10, 0.0), (0.04, 0.05, 0.08), "amarelo_maquina", top="preto_suave")
        mb.box((-0.035, 0.02, 0.0), (0.035, 0.08, 0.22), "amarelo_maquina")
        mb.box((-0.04, 0.05, 0.16), (0.04, 0.30, 0.23), "amarelo_maquina", top="preto_suave")
        mb.cyl((0.0, 0.30, 0.195), (0.0, 0.42, 0.195), 0.009, "cromado", n=6)
        pts = [(0.0, -0.10, 0.04), (0.06, -0.30, 0.01), (0.20, -0.45, 0.01), (0.34, -0.62, 0.01), (0.30, -0.90, 0.01)]
        for k, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
            cor = "preto_suave"
            if cabo_danificado and k == 2:
                mid = tuple((Vector(a) + Vector(b)) / 2)
                mb.cyl(a, mid, 0.007, cor, n=5, caps=False, smooth=False)
                mb.cyl(mid, b, 0.007, cor, n=5, caps=False, smooth=False)
                mb.box((mid[0] - 0.03, mid[1] - 0.02, mid[2] - 0.005), (mid[0] + 0.03, mid[1] + 0.02, mid[2] + 0.012), "cinza_chumbo")
                for (dx, c2) in ((-0.02, "cobre"), (0.0, "vermelho_seguranca"), (0.02, "azul_claro")):
                    mb.strut((mid[0] + dx, mid[1], mid[2] + 0.012), (mid[0] + dx * 1.8, mid[1] + 0.04, mid[2] + 0.02), 0.003, c2, h=0.003)
                continue
            mb.cyl(a, b, 0.007, cor, n=5, caps=False, smooth=False)


def suporte(mb, estado="aguardando"):
    """suporte metalico em L com mao-francesa (origem no centro da chapa de base; aba vertical no lado -Y = borda)."""
    mb.box((-0.20, -0.14, 0.0), (0.20, 0.14, 0.012), "aco", sides="cinza_medio")
    mb.box((-0.20, -0.14, 0.012), (0.20, -0.126, 0.40), "aco", sides="cinza_medio")
    for sx in (-0.14, 0.14):
        mb.hull([(sx - 0.006, -0.126, 0.012), (sx + 0.006, -0.126, 0.012), (sx - 0.006, 0.12, 0.012), (sx + 0.006, 0.12, 0.012),
                 (sx - 0.006, -0.126, 0.34), (sx + 0.006, -0.126, 0.34)], "aco")
    for (x, zz) in ((-0.07, 0.30), (0.07, 0.30)):
        mb.box((x - 0.02, -0.142, zz - 0.008), (x + 0.02, -0.14, zz + 0.008), "grafite")
    for (x, y) in ((-0.17, 0.0), (0.17, 0.0), (-0.07, 0.09), (0.07, 0.09)):
        if estado == "aguardando":
            mb.box((x - 0.009, y - 0.009, 0.012), (x + 0.009, y + 0.009, 0.013), "grafite")
            continue
        alto = 0.06 if estado == "posicionado" else 0.012
        mb.cyl((x, y, 0.012), (x, y, 0.012 + alto), 0.006, "cromado", n=6)
        mb.cyl((x, y, 0.012 + (alto - 0.012 if estado == "posicionado" else 0.0)), (x, y, 0.024 + (alto - 0.012 if estado == "posicionado" else 0.0)),
               0.012, "cromado", n=6, smooth=False)
        mb.cyl((x, y, 0.012), (x, y, 0.016), 0.016, "aco", n=8, smooth=False)


# ------------------------------------------------------------------ construcao
def build():
    random.seed(40)
    Cs = colecoes()
    K.clear_coll(PAI)
    uvt, uvp = UVT(), UVP()
    X0, Y0, X1, Y1 = L.TORRE_A
    out = {}

    # ================================================================ 40a rota, acesso previsto, escada portatil, caminhao
    C = Cs["40a_Rota_Acesso_Caminhao"]
    # faixa de pedestres pintada (portaria -> acesso previsto da Torre A)
    rota = [(27.15, -27.3), (26.45, -20.2), (26.25, -10.5), (25.7, -3.2), (23.6, 0.9)]
    mb = MB()
    zf = 0.012
    for (a, b) in zip(rota[:-1], rota[1:]):
        d = Vector((b[0] - a[0], b[1] - a[1], 0))
        n = Vector((-d.y, d.x, 0)).normalized()
        A, B = Vector((a[0], a[1], zf)), Vector((b[0], b[1], zf))
        A, B = A - d.normalized() * 0.4, B + d.normalized() * 0.4
        mb.poly([tuple(A - n * 0.75), tuple(B - n * 0.75), tuple(B + n * 0.75), tuple(A + n * 0.75)], "verde_seguranca")
        for s in (-0.78, 0.78):
            mb.poly([tuple(A + n * (s - 0.04) + Vector((0, 0, 0.001))), tuple(B + n * (s - 0.04) + Vector((0, 0, 0.001))),
                     tuple(B + n * (s + 0.04) + Vector((0, 0, 0.001))), tuple(A + n * (s + 0.04) + Vector((0, 0, 0.001)))], "branco_sinal")
    for (x, y) in ((26.8, -24.0), (26.35, -16.0), (26.0, -7.8)):
        decal(mb, uvt, "pedestres_piso", (x, y, zf + 0.002), (0, 0, 1), 1.2, up=(0.0, 1.0, 0.0))
    # travessia (zebra) sobre a pista de caminhoes
    for k in range(6):
        y = -15.3 + k * 0.45
        mb.poly([(25.5, y, 0.014), (27.1, y, 0.014), (27.1, y + 0.22, 0.014), (25.5, y + 0.22, 0.014)], "branco_sinal")
    obj(mb, "C08_Rota_Pedestres_Sinalizada", C, cena="C01", props={"tipo": "rota_de_pedestres", "descricao": "caminho da portaria ate o acesso previsto da Torre A"})

    # materiais bloqueando parcialmente a circulacao (C08)
    def pilha_materiais(mb, x, y, rz, organizada=False):
        with mb.at((x, y, 0.0), rz=rz):
            for k in range(6):
                mb.box((-0.61, -1.22, 0.02 + k * 0.018), (0.61, 1.22, 0.02 + k * 0.018 + 0.017), "compensado", sides="forma_resinada")
            mb.box((-0.5, -1.0, 0.0), (-0.42, 1.0, 0.02), "madeira_escura")
            mb.box((0.42, -1.0, 0.0), (0.5, 1.0, 0.02), "madeira_escura")
            if not organizada:
                for k in range(4):
                    mb.box((0.7 + k * 0.13, -1.6, 0.0), (0.8 + k * 0.13, 1.4, 0.05), "madeira")
                with mb.at((1.2, 1.9, 0.0)):
                    for j in range(3):
                        ring = [(0.32 * math.cos(a) * (1 - j * 0.12), 0.32 * math.sin(a) * (1 - j * 0.12), 0.03 + j * 0.03) for a in [2 * math.pi * q / 12 for q in range(13)]]
                        for p0, p1 in zip(ring[:-1], ring[1:]):
                            mb.cyl(p0, p1, 0.025, "preto_suave", n=5, caps=False, smooth=False)
            else:
                for k in range(4):
                    mb.box((-0.55, -1.3, 0.13 + k * 0.05), (-0.45 + k * 0.01, 1.3, 0.18 + k * 0.05), "madeira")
    mb = MB()
    pilha_materiais(mb, 25.35, -6.6, 28.0)
    obj(mb, "C08_Materiais_Bloqueando_Caminho", C, cena="C08", props={"interativo": True, "estado": "inicial",
        "rotulo": "Materiais bloqueando parcialmente a circulacao", "escolhas": "A pedir para liberar / B passar por cima"})
    mb = MB()
    pilha_materiais(mb, 23.95, -5.6, 90.0, organizada=True)
    obj(mb, "C08_Materiais_Liberados_Organizados", C, visivel=False, cena="C08", props={"estado": "apos_escolha_A"})

    # acesso previsto: cobertura de protecao sobre a entrada (vao sul 04 do terreo)
    cx0, cy0, cx1, cy1 = L.TR_COBERTURA_ACESSO
    mb = MB()
    for (x, y) in ((cx0 + 0.06, cy0 + 0.06), (cx1 - 0.06, cy0 + 0.06)):
        mb.box((x - 0.06, y - 0.06, 0.0), (x + 0.06, y + 0.06, 2.62), "grafite", nobottom=True)
        mb.box((x - 0.15, y - 0.15, 0.0), (x + 0.15, y + 0.15, 0.03), "concreto_escuro", nobottom=True)
    for x in (cx0 + 0.06, cx1 - 0.06):
        mb.box((x - 0.05, cy0, 2.55), (x + 0.05, cy1, 2.7), "grafite")
    mb.box((cx0 - 0.1, cy0 - 0.1, 2.7), (cx1 + 0.1, cy1, 2.74), "madeira", top="compensado", sides="madeira_escura")
    mb.box((cx0 - 0.12, cy0 - 0.12, 2.74), (cx1 + 0.12, cy0 + 0.02, 3.0), "amarelo_linha_vida")
    for k in range(7):
        x = cx0 - 0.1 + k * 0.33
        mb.poly([(x, cy0 - 0.125, 2.745), (x + 0.16, cy0 - 0.125, 2.745), (x + 0.30, cy0 - 0.125, 2.995), (x + 0.14, cy0 - 0.125, 2.995)], "zebrado_preto")
    decal(mb, uvt, "acesso_previsto", ((cx0 + cx1) / 2, cy0 - 0.13, 2.2), (0, -1, 0), 1.7)
    obj(mb, "C09_Acesso_Previsto_Coberto", C, cena="C09", props={"interativo": True, "rotulo": "Acesso previsto (escada interna)",
        "correto": True, "nr_ref": "NR-18 18.9 protecao contra queda de materiais no acesso"})

    # escada portatil (atalho NAO previsto) apoiada na janela do pav 1
    xl = L.TR_ESCADA_PORTATIL_X
    top = (xl, 4.02, L.TA_Z(1) + 1.0 + 0.05)
    bot = (xl, 4.02 - (top[2] / math.tan(math.radians(74))), 0.0)
    mb = MB()
    for dx in (-0.21, 0.21):
        mb.strut((bot[0] + dx, bot[1], bot[2]), (top[0] + dx, top[1] + 0.05, top[2] + 0.55), 0.045, "madeira", h=0.07, up=(0, 1, 0))
    Lh = math.dist(bot, top)
    for j in range(1, int(Lh / 0.3) + 1):
        u = j / (Lh / 0.3 + 1)
        p = (bot[0], bot[1] + (top[1] - bot[1]) * u, bot[2] + (top[2] - bot[2]) * u)
        mb.box((p[0] - 0.21, p[1] - 0.02, p[2] - 0.02), (p[0] + 0.21, p[1] + 0.02, p[2] + 0.02), "madeira_escura")
    obj(mb, "C09_Escada_Portatil_Atalho", C, cena="C09", props={"interativo": True, "rotulo": "Escada portatil (mais rapida?)", "correto": False,
        "nota": "nao definida como acesso para a atividade (regra 7 do roteiro tecnico)"})

    # caminhao munck descarregando paletes (ao fundo da Cena 01)
    tx, ty = L.TR_MUNCK
    mbt = V.caminhao_prancha("verde_caminhao", carga=None)
    obj(mbt, "C01_Caminhao_Munck_Descarregando", C, cena="C01", loc=(tx, ty, 0.0), rz=180.0,
        props={"tipo": "caminhao_munck", "ambiente": "caminhao descarregando material ao fundo"})
    mb = MB()
    colx = tx - 2.05
    mb.box((colx - 0.3, ty - 0.3, 1.1), (colx + 0.3, ty + 0.3, 1.45), "amarelo_maquina")
    mb.cyl((colx, ty, 1.45), (colx, ty, 2.9), 0.18, "amarelo_maquina", n=8)
    for s in (-1, 1):
        mb.box((colx - 0.12, ty + s * 1.2, 0.55), (colx + 0.12, ty + s * 2.45, 0.75), "amarelo_escuro")
        mb.box((colx - 0.08, ty + s * 2.35, 0.0), (colx + 0.08, ty + s * 2.5, 0.6), "grafite")
        mb.box((colx - 0.25, ty + s * 2.2 - 0.25, 0.0), (colx + 0.25, ty + s * 2.2 + 0.25, 0.08), "madeira")
    j1 = (colx, ty, 2.9)
    j2 = (colx + 0.5, ty + 2.4, 5.4)
    j3 = (colx + 0.9, ty + 4.0, 4.3)
    mb.strut(j1, j2, 0.26, "amarelo_maquina", h=0.3)
    mb.strut(j2, j3, 0.2, "amarelo_maquina", h=0.24)
    mb.cyl(j1, ((j1[0] + j2[0]) / 2, (j1[1] + j2[1]) / 2 - 0.2, (j1[2] + j2[2]) / 2 - 0.3), 0.06, "cromado", n=6)
    hz = 1.75
    mb.cyl(j3, (j3[0], j3[1], hz + 0.35), 0.01, "cinza_escuro", n=4, caps=False)
    mb.box((j3[0] - 0.08, j3[1] - 0.08, hz + 0.2), (j3[0] + 0.08, j3[1] + 0.08, hz + 0.38), "amarelo_maquina")
    for (sx, sy) in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
        mb.strut((j3[0], j3[1], hz + 0.2), (j3[0] + sx, j3[1] + sy, hz - 0.1), 0.03, "laranja_seguranca", h=0.01)
    px, py = j3[0], j3[1]
    mb.box((px - 0.55, py - 0.55, hz - 1.1), (px + 0.55, py + 0.55, hz - 0.97), "pallet")
    mb.box((px - 0.5, py - 0.5, hz - 0.97), (px + 0.5, py + 0.5, hz - 0.1), "filme_plastico", top="bloco_ceramico")
    mb.cyl((px + 0.5, py - 0.5, hz - 0.5), (px + 1.6, py - 1.3, 1.0), 0.008, "amarelo_linha_vida", n=4, caps=False)
    for (qx, qy) in ((tx + 1.6, ty + 3.35), (tx + 2.95, ty + 3.35)):
        mb.box((qx - 0.55, qy - 0.55, 0.0), (qx + 0.55, qy + 0.55, 0.13), "pallet")
        mb.box((qx - 0.5, qy - 0.5, 0.13), (qx + 0.5, qy + 0.5, 1.0), "filme_plastico", top="bloco_ceramico")
    for k in range(3):
        qx = tx - 1.6 + k * 1.2
        mb.box((qx, ty - 0.5, 1.3), (qx + 1.1, ty + 0.6, 1.43), "pallet")
        mb.box((qx + 0.05, ty - 0.45, 1.43), (qx + 1.05, ty + 0.55, 2.3), "filme_plastico", top="bloco_ceramico")
    pts = [(tx - 4.9, ty + 1.6), (tx + 4.9, ty + 1.6), (tx + 4.9, ty + 4.5), (tx - 4.9, ty + 4.5)]
    for (x, y) in pts:
        cone(mb, x, y)
    fita_zebrada(mb, pts + [pts[0]], 0.62)
    obj(mb, "C01_Munck_Lanca_Carga_Isolamento", C, cena="C01", props={"tipo": "icamento_munck", "animavel": "carga desce do caminhao"})

    # ================================================================ 40b area de equipamentos (C06)
    C = Cs["40b_Area_Equipamentos"]
    ex0, ey0, ex1, ey1 = L.TR_AREA_EQUIP
    mb = MB()
    tx0, tx1, ty0, ty1 = 14.6, 19.6, -25.9, -21.9
    for (x, y) in ((tx0, ty0), (tx1, ty0), (tx0, ty1), (tx1, ty1)):
        mb.box((x - 0.04, y - 0.04, 0.0), (x + 0.04, y + 0.04, 2.7), "cinza_claro", nobottom=True)
        mb.box((x - 0.12, y - 0.12, 0.0), (x + 0.12, y + 0.12, 0.03), "grafite", nobottom=True)
    mb.poly([(tx0 - 0.1, ty0 - 0.1, 2.75), (tx1 + 0.1, ty0 - 0.1, 2.75), (tx1 + 0.1, ty1 + 0.1, 2.52), (tx0 - 0.1, ty1 + 0.1, 2.52)], "lona_azul")
    mb.poly([(tx0 - 0.1, ty1 + 0.1, 2.52), (tx1 + 0.1, ty1 + 0.1, 2.52), (tx1 + 0.1, ty1 + 0.1, 2.3), (tx0 - 0.1, ty1 + 0.1, 2.3)], "branco_sinal")
    # bancada de inspecao (ao longo de Y), lado leste = trabalhador
    bx0, bx1, by0, by1 = 17.5, 18.3, -25.65, -21.95
    mb.box((bx0, by0, 0.86), (bx1, by1, 0.9), "compensado", sides="madeira_escura")
    for (x, y) in ((bx0 + 0.05, by0 + 0.05), (bx1 - 0.05, by0 + 0.05), (bx0 + 0.05, by1 - 0.05), (bx1 - 0.05, by1 - 0.05)):
        mb.box((x - 0.03, y - 0.03, 0.0), (x + 0.03, y + 0.03, 0.86), "grafite", nobottom=True)
    mb.box((bx0 + 0.05, by0 + 0.1, 0.25), (bx1 - 0.05, by1 - 0.1, 0.28), "compensado")
    # arara com cinturoes e talabartes pendurados (fundo)
    rx_ = 15.3
    for y in (-25.4, -22.4):
        mb.box((rx_ - 0.03, y - 0.03, 0.0), (rx_ + 0.03, y + 0.03, 1.9), "cromado", nobottom=True)
    mb.cyl((rx_, -25.4, 1.85), (rx_, -22.4, 1.85), 0.02, "cromado", n=6)
    for k in range(6):
        y = -25.1 + k * 0.5
        cor = ("laranja_seguranca", "amarelo_linha_vida")[k % 2]
        mb.box((rx_ - 0.01, y - 0.01, 1.62), (rx_ + 0.01, y + 0.01, 1.85), "cromado")
        for s in (-1, 1):
            mb.strut((rx_ + 0.02, y + s * 0.05, 1.62), (rx_ + 0.02, y + s * 0.14, 1.2), 0.04, cor, h=0.008, up=(1, 0, 0))
            mb.strut((rx_ + 0.02, y + s * 0.14, 1.2), (rx_ + 0.02, y + s * 0.09, 0.95), 0.04, cor, h=0.008, up=(1, 0, 0))
        mb.strut((rx_ + 0.03, y - 0.15, 1.18), (rx_ + 0.03, y + 0.15, 1.18), 0.045, cor, h=0.01, up=(1, 0, 0))
        mb.box((rx_ + 0.03, y - 0.04, 1.38), (rx_ + 0.07, y + 0.04, 1.55), "preto_radio")
    # placa da area e caixa de retirados de uso
    decal(mb, uvt, "area_equipamentos", (tx1 + 0.05, (ty0 + ty1) / 2, 2.05), (1, 0, 0), 2.6)
    mb.box((tx1 + 0.02, ty0 + 0.4, 1.7), (tx1 + 0.05, ty1 - 0.4, 2.4), "branco_sinal")
    mb.box((18.85, -25.55, 0.0), (19.45, -25.05, 0.42), "vermelho_seguranca", top="vermelho_escuro")
    decal(mb, uvt, "caixa_retirados", (19.452, -25.3, 0.26), (1, 0, 0), 0.46)
    obj(mb, "C06_Area_Equipamentos_Estrutura", C, cena="C06", props={"tipo": "area_de_equipamentos",
        "descricao": "tenda com bancada de inspecao, arara, caixa 'retirado de uso' e placa de orientacao"})

    zt = 0.9
    itens = [
        ("C06_Capacete_01_OK", "capacete", -25.35, dict(cor="capacete_branco"), {"defeito": None}),
        ("C06_Capacete_02_OK", "capacete", -25.02, dict(cor="capacete_azul"), {"defeito": None}),
        ("C06_Capacete_03_Rachado", "capacete", -24.69, dict(cor="capacete_amarelo", rachado=True),
         {"defeito": "rachadura", "opcoes": "RETIRAR DE USO | USAR MESMO ASSIM", "variavel_se_usar": "CAPACETE_DANIFICADO"}),
        ("C06_Cinturao_01_OK", "cinturao", -24.2, dict(cor="laranja_seguranca"), {"defeito": None}),
        ("C06_Cinturao_02_Corte_Fita", "cinturao", -23.62, dict(cor="laranja_seguranca", corte=True),
         {"defeito": "pequeno corte na fita", "opcoes": "RETIRAR DE USO | O CORTE E PEQUENO. VOU USAR.", "variavel_se_usar": "CINTURAO_DANIFICADO"}),
        ("C06_Talabarte_01_OK", "talabarte", -22.85, dict(x=17.72), {"defeito": None}),
    ]
    for (nome, tipo, y, kw, extra) in itens:
        mb = MB()
        if tipo == "capacete":
            with mb.at((17.9, y, zt), rz=-90):
                capacete(mb, kw["cor"], kw.get("rachado", False))
        elif tipo == "cinturao":
            with mb.at((17.9, y, zt), rz=90):
                cinturao_mesa(mb, kw["cor"], kw.get("corte", False))
        elif tipo == "talabarte":
            with mb.at((kw.get("x", 17.9), y, zt), rz=180):
                talabarte_mesa(mb, False)
        pr = {"interativo": True, "item": tipo, "acao": "inspecionar"}
        pr.update({k: v for k, v in extra.items() if v is not None})
        obj(mb, nome, C, cena="C06", props=pr)
    # segundo talabarte (desgastado) sobre o tampo inferior da bancada (item separado para clique)
    mb = MB()
    with mb.at((18.08, -22.85, zt), rz=180):
        talabarte_mesa(mb, True)
    obj(mb, "C06_Talabarte_02_Desgastado", C, cena="C06", props={"interativo": True, "item": "talabarte", "acao": "inspecionar",
        "defeito": "desgaste na fita", "opcoes": "RETIRAR DE USO | USAR COM CUIDADO | TENTAR CONSERTAR", "variavel_se_usar": "TALABARTE_DANIFICADO"})
    mb = MB()
    for k in range(3):
        conector(mb, 18.0 + k * 0.09, -22.15, zt, rz=90)
    obj(mb, "C06_Conectores_OK", C, cena="C06", props={"interativo": True, "item": "conectores", "acao": "inspecionar"})
    mb = MB()
    bolsa_ferramentas(mb, 17.95, -25.25, zt - 0.62, fechada=True)
    obj(mb, "C06_Bolsa_Ferramentas_e_Cordoes", C, cena="C06", props={"interativo": True, "item": "bolsa_de_ferramentas",
        "nota": "usada depois para FERRAMENTAS_PROTEGIDAS"})
    mb = MB()
    radio(mb, 17.6, -22.2, 0.9, rz=90.0, deitado=True)
    radio(mb, 17.6, -22.1, 0.9, rz=90.0, deitado=True)
    obj(mb, "C06_Radios_Carregador", C, cena="C06", props={"interativo": True, "item": "radio", "canal": 3})

    # ================================================================ 40c aberturas no piso (C10 protegida / C11 deslocada)
    C = Cs["40c_Aberturas_Pav02_Pav03"]
    sx0, sy0, sx1, sy1 = L.TA_SHAFT
    cxs, cys = (sx0 + sx1) / 2, (sy0 + sy1) / 2

    def tampa(mb, cx, cy, z, rz=0.0, travas=True, placa=True):
        with mb.at((cx, cy, z), rz=rz):
            mb.box((-0.75, -0.75, 0.0), (0.75, 0.75, 0.03), "compensado", sides="madeira_escura")
            if placa:
                decal(mb, uvt, "tampao_abertura", (0.0, 0.0, 0.03), (0, 0, 1), 1.42, up=(0.0, 1.0, 0.0), off=0.002)
            for (x, y) in ((-0.68, -0.68), (0.68, -0.68), (0.68, 0.68), (-0.68, 0.68)):
                mb.cyl((x, y, 0.03), (x, y, 0.036), 0.012, "cromado", n=6, smooth=False)
            if travas:
                for s in (-1, 1):
                    mb.box((s * 0.6 - 0.02, -0.58, -0.10), (s * 0.6 + 0.02, 0.58, 0.0), "madeira_escura")
                    mb.box((-0.58, s * 0.6 - 0.02, -0.10), (0.58, s * 0.6 + 0.02, 0.0), "madeira_escura")

    mb = MB()
    tampa(mb, cxs, cys, L.TA_Z(2))
    obj(mb, "C10_Pav02_Abertura_Protegida", C, cena="C10", props={"interativo": True, "tipo": "tampa_fixada_abertura_piso",
        "rotulo": "Abertura no piso protegida", "nr_ref": "NR-18 18.9.2 (fechamento resistente e fixado)"})
    mb = MB()
    with mb.at((cxs + 0.62, cys + 0.18, L.TA_Z(3))):
        with mb.at((0, 0, 0.0), rz=14.0):
            mb.box((-0.75, -0.75, 0.0), (0.75, 0.75, 0.03), "compensado", sides="madeira_escura")
            decal(mb, uvt, "tampao_abertura", (0.0, 0.0, 0.03), (0, 0, 1), 1.42, up=(0.0, 1.0, 0.0), off=0.002)
            for s in (-1, 1):
                mb.box((s * 0.6 - 0.02, -0.58, 0.03), (s * 0.6 + 0.02, 0.58, 0.07), "madeira_escura")
    obj(mb, "C11_Pav03_Abertura_Protecao_Deslocada", C, cena="C11", props={"interativo": True, "estado": "inicial",
        "rotulo": "Abertura com protecao deslocada", "escolhas": "A impedir passagem e comunicar / B nao e minha area / C madeira solta por cima"})
    mb = MB()
    tampa(mb, cxs, cys, L.TA_Z(3))
    obj(mb, "C11_Pav03_Abertura_Corrigida", C, visivel=False, cena="C11", props={"estado": "apos_escolha_A (equipe corrige)"})
    mb = MB()
    zc = L.TA_Z(3)
    pts = [(sx0 - 0.6, sy0 - 0.6), (sx1 + 0.6, sy0 - 0.6), (sx1 + 0.6, sy1 + 0.6), (sx0 - 0.6, sy1 + 0.6)]
    for (x, y) in pts:
        cone(mb, x, y, z=zc)
    fita_zebrada(mb, [(p[0], p[1]) for p in pts] + [pts[0]], zc + 0.62)
    obj(mb, "C11_Pav03_Passagem_Impedida_Cones", C, visivel=False, cena="C11", props={"estado": "escolha_A (jogador impede a passagem)"})
    mb = MB()
    mb.box((sx0 - 0.35, cys - 0.14, zc), (sx1 + 0.25, cys + 0.12, zc + 0.03), "madeira", sides="madeira_escura")
    obj(mb, "C11_Pav03_Madeira_Solta_Improvisada", C, visivel=False, cena="C11", props={"estado": "escolha_C (improviso - feedback)"})

    # ================================================================ 40d frente de trabalho no 4o pavimento
    C = Cs["40d_Frente_Trabalho_Pav04"]
    z = Z4
    sx, sy = L.TR_SUPORTE
    # suporte (3 estados)
    for (nome, est, loc, rz, vis, cena) in (("C21_Suporte_Aguardando", "aguardando", (28.4, 5.85, z + 0.02), 8.0, True, "C21"),
                                            ("C21_Suporte_Posicionado", "posicionado", (sx, sy, z), 0.0, False, "C21"),
                                            ("CONC_Suporte_Instalado", "instalado", (sx, sy, z), 0.0, False, "CONC")):
        mb = MB()
        suporte(mb, est)
        obj(mb, nome, C, visivel=vis, cena=cena, loc=loc, rz=rz, props={"interativo": True, "tipo": "suporte_metalico", "estado": est,
            "missao": "posicionamento, fixacao, aperto, conferencia"})
    # tabua de apoio das ferramentas
    mb = MB()
    mb.box((27.55, 5.25, z), (28.75, 6.15, z + 0.02), "compensado", sides="madeira_escura")
    obj(mb, "C20_Base_Apoio_Ferramentas", C, cena="C20", props={"tipo": "apoio_ferramentas"})

    # ferramentas soltas (estado inicial) x protegidas contra queda
    mb = MB()
    chave_boca(mb, (28.5, 5.42, z + 0.02), rz=35.0)
    furadeira(mb, (27.85, 5.6, z + 0.02), rz=-70.0)
    mb.box((27.95, 5.92, z + 0.02), (28.15, 6.07, z + 0.08), "cinza_claro", top="cinza_escuro")
    rnd = random.Random(4)
    for k in range(9):
        px, py = 28.1 + rnd.uniform(-0.2, 0.3), 5.35 + rnd.uniform(0.0, 0.15)
        mb.cyl((px, py, z + 0.02), (px, py, z + 0.035), 0.009, "cromado", n=6, smooth=False)
    chave_boca(mb, (29.6, 4.62, z), rz=80.0)
    obj(mb, "C20_Ferramentas_Soltas", C, cena="C20", props={"interativo": True, "estado": "inicial",
        "itens": "chave, parafusos, ferramenta eletrica, pequenas pecas", "variavel": "FERRAMENTAS_PROTEGIDAS", "valor_se_mantido": "NAO"})
    mb = MB()
    bolsa_ferramentas(mb, 28.15, 5.75, z + 0.02, fechada=True)
    furadeira(mb, (27.75, 5.5, z + 0.02), rz=-80.0)
    mb.cyl((27.8, 5.4, z + 0.12), (28.15, 5.72, z + 0.25), 0.005, "amarelo_linha_vida", n=4)
    obj(mb, "C20_Ferramentas_Protegidas", C, visivel=False, cena="C20", props={"estado": "apos_escolha_A",
        "descricao": "ferramentas amarradas (cordao) e pecas em bolsa fechada", "variavel": "FERRAMENTAS_PROTEGIDAS", "valor": "SIM"})

    # ponto de ancoragem identificado PA-04-01 (face oeste do pilar de canto)
    ax, ay, ah = L.TR_ANCORAGEM
    mb = MB()
    zz = z + ah
    mb.box((ax - 0.018, ay - 0.06, zz - 0.11), (ax, ay + 0.06, zz + 0.11), "amarelo_ancoragem")
    for dz in (-0.08, 0.08):
        mb.cyl((ax - 0.018, ay, zz + dz), (ax - 0.032, ay, zz + dz), 0.013, "cromado", n=6, smooth=False)
    ring = [(ax - 0.05 - 0.055 * (1 + math.cos(a)) * 0.5, ay + 0.045 * math.sin(a), zz - 0.02 * math.cos(a)) for a in [2 * math.pi * k / 10 for k in range(11)]]
    for p0, p1 in zip(ring[:-1], ring[1:]):
        mb.cyl(p0, p1, 0.009, "cromado", n=5, caps=False, smooth=False)
    g24 = sys.modules["gen_24"]
    g24.placa(mb, "ponto_ancoragem", (ax - 0.002, ay, z + 1.95), (-1.0, 0.0), 0.3, board=True)
    obj(mb, "C18_Ponto_Ancoragem_PA0401", C, cena="C18", props={"interativo": True, "correto": True, "id": "PA-04-01",
        "rotulo": "Ponto identificado (sistema previsto para a atividade)", "nr_ref": "NR-35 / NR-18 18.12 (ponto previsto e identificado)"})
    mb = MB()
    decal(mb, uvt, "placa_pa0401", (ax - 0.004, ay, z + 1.05), (-1, 0, 0), 0.30)
    mb.box((ax - 0.006, ay - 0.16, z + 0.94), (ax - 0.002, ay + 0.16, z + 1.16), "grafite")
    obj(mb, "C18_Identificacao_PA0401_Legivel", C, cena="C18", props={"estado": "inicial", "evento_relacionado": "EV13"})
    mb = MB()
    decal(mb, uvt, "placa_pa0401_ilegivel", (ax - 0.007, ay, z + 1.05), (-1, 0, 0), 0.30)
    obj(mb, "EV13_Identificacao_PA0401_Ilegivel", C, visivel=False, cena="EV13", props={"evento": "EVENTO_IDENTIFICACAO_INDISPONIVEL"})

    # distratores (parecem fortes, NAO sao pontos previstos)
    mb = MB()
    for dx in (0.0, 0.22):
        base = Vector((29.28 + dx, 4.58, z))
        mb.cyl(tuple(base), tuple(base + Vector((0, 0, 0.55))), 0.0063, "vergalhao", n=5, smooth=False)
        mb.cyl(tuple(base + Vector((0.11, 0, 0))), tuple(base + Vector((0.11, 0, 0.55))), 0.0063, "vergalhao", n=5, smooth=False)
        arc = [tuple(base + Vector((0.055 - 0.055 * math.cos(a), 0, 0.55 + 0.05 * math.sin(a)))) for a in [math.pi * k / 6 for k in range(7)]]
        for p0, p1 in zip(arc[:-1], arc[1:]):
            mb.cyl(p0, p1, 0.0063, "vergalhao", n=5, caps=False, smooth=False)
    obj(mb, "C18_Distrator_Vergalhao", C, cena="C18", props={"interativo": True, "correto": False, "variavel_se_escolhido": "CONEXAO_INCORRETA",
        "rotulo": "Vergalhao (esperas) - nao e ponto previsto"})
    mb = MB()
    px_, py_ = 31.72, 5.60
    mb.cyl((px_, py_, z), (px_, py_, L.TA_Z(5) - 0.5), 0.038, "aco", n=8)
    for hz in (0.4, 1.8):
        mb.box((px_ - 0.05, py_ - 0.05, z + hz), (px_ + 0.1, py_ + 0.05, z + hz + 0.05), "grafite")
    mb.cyl((px_, py_, z + 1.25), (px_, py_ + 0.55, z + 1.25), 0.03, "aco", n=8)
    mb.cyl((px_, py_ + 0.45, z + 1.25), (px_ - 0.11, py_ + 0.45, z + 1.25), 0.012, "cromado", n=6)
    mb.cyl((px_ - 0.12, py_ + 0.36, z + 1.25), (px_ - 0.12, py_ + 0.54, z + 1.25), 0.01, "vermelho_seguranca", n=6)
    obj(mb, "C18_Distrator_Tubulacao", C, cena="C18", props={"interativo": True, "correto": False, "variavel_se_escolhido": "CONEXAO_INCORRETA",
        "rotulo": "Tubulacao - nao e ponto previsto"})
    mb = MB()
    for x in (27.95, 28.85):
        with mb.at((x, 5.50, z)):
            for (a, b) in (((-0.35, -0.3, 0.0), (-0.05, 0.0, 0.85)), ((0.35, -0.3, 0.0), (0.05, 0.0, 0.85)),
                           ((-0.35, 0.3, 0.0), (-0.05, 0.0, 0.85)), ((0.35, 0.3, 0.0), (0.05, 0.0, 0.85))):
                mb.strut(a, b, 0.04, "vermelho_escuro")
            mb.box((-0.3, -0.05, 0.85), (0.3, 0.05, 0.9), "vermelho_escuro")
    mb.box((27.60, 5.42, z + 0.9), (29.20, 5.58, z + 0.912), "grafite")
    mb.box((27.60, 5.42, z + 1.09), (29.20, 5.58, z + 1.102), "grafite")
    mb.box((27.60, 5.49, z + 0.912), (29.20, 5.51, z + 1.09), "grafite")
    obj(mb, "C18_Distrator_Estrutura_Metalica", C, cena="C18", props={"interativo": True, "correto": False, "variavel_se_escolhido": "CONEXAO_INCORRETA",
        "rotulo": "Estrutura metalica (perfil sobre cavaletes) - nao e ponto previsto"})

    # guarda-corpo: variantes dos trechos do vao sul 05 e 04 (base = gen_13)
    sul = (0.0, 1.0)
    def v(nome, trecho, vis, cena, props, **kw):
        a, b = gcr_trecho(trecho)
        mb = MB()
        gcr_var(mb, a, b, z, sul, **kw)
        pr = {"variante_de": "TorreA_Pav04_GcR_" + trecho, "tipo": "GcR_variante"}
        pr.update(props)
        return obj(mb, nome, C, visivel=vis, cena=cena, props=pr)

    v("C13_GcR_Sul05a_Levemente_Solto", "Sul_05a", True, "C13", {"interativo": True, "estado": "inicial",
      "rotulo": "Parte do guarda-corpo levemente solta (aproximar para perceber)", "variavel_se_B": "GUARDA_CORPO_PROBLEMA",
      "oculta_base": "TorreA_Pav04_GcR_Sul_05a"}, incl={1: 4.0}, clamp_solto=(1,), folga_travessao=1)
    v("CONSEQ_GcR_Sul05a_Cedendo", "Sul_05a", False, "CONSEQ", {"consequencia": "GUARDA_CORPO_PROBLEMA=SIM (sugestao: rajada/apoio)"},
      incl={0: 8.0, 1: 22.0, 2: 10.0}, clamp_solto=(1,), folga_travessao=1)
    v("EV10_GcR_Sul05b_Travessao_Intermediario_Removido", "Sul_05b", False, "EV10", {"evento": "EVENTO_PROTECAO_ALTERADA",
      "rotulo": "Protecao alterada durante o intervalo (sem travessao intermediario)"}, sem_intermediario=True)
    v("CONSEQ_Conexao_GuardaCorpo_Cedendo", "Sul_05b", False, "CONSEQ", {"consequencia": "CONEXAO_INCORRETA=SIM (escolheu guarda-corpo)"},
      incl={1: 9.0}, flecha=0.16)
    v("EV01_GcR_Sul04a_Removido_Vao_Aberto", "Sul_04a", False, "EV01", {"evento": "EVENTO_GUARDA_CORPO_REMOVIDO",
      "rotulo": "Guarda-corpo retirado 'so um minutinho' e nao recolocado"}, sem_travessao=True, sem_intermediario=True, sem_tela=True, sem_rodape=True)
    mb = MB()
    a, b = gcr_trecho("Sul_04a")
    for k, (hz, cc, hh) in enumerate(((0.05, "laranja_seguranca", 0.10), (0.16, "laranja_seguranca", 0.08), (0.27, "amarelo_linha_vida", 0.2))):
        mb.box((a[0] + 0.1, 5.1 + k * 0.28, z), (b[0] - 0.1, 5.1 + k * 0.28 + hh, z + 0.04), cc)
    mb.poly([(a[0] + 0.1, 6.0, z + 0.01), (b[0] - 0.1, 6.0, z + 0.01), (b[0] - 0.1, 6.9, z + 0.012), (a[0] + 0.1, 6.9, z + 0.012)], "laranja_seguranca")
    obj(mb, "EV01_Pecas_GcR_Retiradas_no_Piso", C, visivel=False, cena="EV01", props={"evento": "EVENTO_GUARDA_CORPO_REMOVIDO"})
    v("EV15_GcR_Sul04b_Impacto_Sem_Dano_Aparente", "Sul_04b", False, "EV15", {"evento": "EVENTO_IMPACTO_PROTECAO"}, amassado=1.2, marca=1.2)
    v("EV15_GcR_Sul04b_Deslocado_Depois", "Sul_04b", False, "EV15", {"evento": "EVENTO_IMPACTO_PROTECAO", "estado": "escolha_B (mais tarde)"},
      incl={1: 12.0, 2: 5.0}, clamp_solto=(1,), amassado=1.2, marca=1.2)
    # etiquetas 'nao remover' nos trechos
    mb = MB()
    for trecho in ("Sul_04a", "Sul_04b", "Sul_05a", "Sul_05b"):
        a, b = gcr_trecho(trecho)
        decal(mb, uvt, "nao_remover_gcr", ((a[0] + b[0]) / 2, 4.105, z + 1.07), (0, 1, 0), 0.30, off=0.0)
    obj(mb, "C12_Etiquetas_Protecao_Nao_Remover", C, cena="C12", props={"tipo": "sinalizacao"})

    # material solto junto a borda (C15) e retirado
    mb = MB()
    mb.strut((28.05, 4.42, z + 0.01), (27.92, 4.13, z + 0.86), 0.06, "madeira", h=0.025, up=(0, 1, 0))
    obj(mb, "C15_Madeira_Solta_Junto_Borda", C, cena="C15", props={"interativo": True, "estado": "inicial", "escolhas": "RETIRAR | DEIXAR",
        "variavel_se_deixar": "MATERIAL_SOLTO"})
    mb = MB()
    mb.box((26.1, 8.2, z + 0.25), (26.16, 9.1, z + 0.275), "madeira")
    obj(mb, "C15_Madeira_Retirada_Guardada", C, visivel=False, cena="C15", props={"estado": "apos_RETIRAR"})

    # outras equipes: alvenaria interna em execucao (C16)
    mb = MB()
    wy = L.TA_YL[1]
    for k in range(5):
        zk = z + k * 0.2
        off = 0.0 if k % 2 == 0 else 0.2
        x = 21.95 + off
        while x < 26.4:
            xe = min(x + 0.39, 26.45)
            mb.box((x, wy - 0.07, zk), (xe, wy + 0.07, zk + 0.19), "bloco_ceramico", top="argamassa")
            x += 0.4
    for (px, py) in ((23.0, 11.55), (24.3, 11.55)):
        mb.box((px - 0.55, py - 0.55, z), (px + 0.55, py + 0.55, z + 0.13), "pallet")
        mb.box((px - 0.5, py - 0.5, z + 0.13), (px + 0.5, py + 0.5, z + 0.95), "bloco_ceramico", top="argamassa")
    mb.box((25.2, 11.0, z), (26.3, 11.8, z + 0.3), "cinza_escuro")
    mb.box((25.28, 11.08, z + 0.2), (26.22, 11.72, z + 0.29), "argamassa")
    mb.box((22.6, 10.12, z + 1.0), (23.2, 10.2, z + 1.04), "amarelo_maquina")
    obj(mb, "C16_Alvenaria_Interna_Em_Execucao", C, cena="C16", props={"tipo": "paredes_parcialmente_construidas_e_materiais"})
    # lona cobrindo sacos de cimento (normal) e batendo (EV06)
    mb = MB()
    mb.box((25.6, 8.1, z), (26.7, 9.2, z + 0.13), "pallet")
    for k in range(4):
        mb.box((25.65, 8.15, z + 0.13 + k * 0.12), (26.65, 9.15, z + 0.25 + k * 0.12), "saco_cimento")
    mb.hull([(25.5, 8.0, z + 0.12), (26.8, 8.0, z + 0.12), (26.8, 9.3, z + 0.12), (25.5, 9.3, z + 0.12),
             (25.62, 8.12, z + 0.64), (26.68, 8.12, z + 0.64), (26.68, 9.18, z + 0.64), (25.62, 9.18, z + 0.64)], "lona_azul")
    obj(mb, "C17_Lona_Cobrindo_Material", C, cena="C17", props={"evento_relacionado": "EV06"})
    mb = MB()
    mb.box((25.6, 8.1, z), (26.7, 9.2, z + 0.13), "pallet")
    for k in range(4):
        mb.box((25.65, 8.15, z + 0.13 + k * 0.12), (26.65, 9.15, z + 0.25 + k * 0.12), "saco_cimento")
    # a lona levanta e dobra sobre a propria pilha: nao varre o piso onde a equipe trabalha
    mb.poly([(25.45, 7.95, z + 0.60), (26.85, 7.95, z + 0.60), (26.95, 9.05, z + 1.25), (25.35, 9.10, z + 1.35)], "lona_azul")
    mb.poly([(25.35, 9.10, z + 1.35), (26.95, 9.05, z + 1.25), (26.60, 8.55, z + 1.88), (25.55, 8.60, z + 1.95)], "lona_azul")
    rnd = random.Random(11)
    for k in range(14):                       # poeira solta: so no ar, em volta da lona
        px, py, pz = 25.2 + rnd.uniform(0, 2.4), 7.4 + rnd.uniform(0, 2.2), z + 0.9 + rnd.uniform(0, 1.3)
        mb.box((px, py, pz), (px + 0.04, py + 0.03, pz + 0.01), ("papelao", "saco_cimento", "madeira")[k % 3])
    obj(mb, "EV06_Lona_Batendo_Poeira", C, visivel=False, cena="EV06", props={"evento": "EVENTO_VENTO", "oculta_base": "C17_Lona_Cobrindo_Material"})
    # fita no guarda-corpo indicando vento (C17)
    mb = MB()
    a, b = gcr_trecho("Sul_05b")
    p = Vector((b[0] - 0.06, 4.10, z + 1.2))
    pts = [p, p + Vector((-0.12, -0.08, -0.03)), p + Vector((-0.26, -0.13, 0.02)), p + Vector((-0.42, -0.2, -0.02))]
    for p0, p1 in zip(pts[:-1], pts[1:]):
        mb.strut(tuple(p0), tuple(p1), 0.04, "vermelho_seguranca", h=0.003, up=(0, 0, 1))
    obj(mb, "C17_Fita_Indicadora_Vento", C, cena="C17", props={"tipo": "indicador_visual_de_vento"})

    # permissao de trabalho afixada no pilar + rota de fuga
    mb = MB()
    pc = L.TA_PILAR(26.8, 10.0)
    decal(mb, uvt, "pt_quadro", (pc[2] + 0.004, 10.0, z + 1.45), (1, 0, 0), 0.32)
    decal(mb, uvt, "rota_fuga_dir", (pc[2] + 0.004, 10.0, z + 2.05), (1, 0, 0), 0.42)
    decal(mb, uvt, "rota_fuga_esq", (19.0, 13.94, z + 2.1), (0, -1, 0), 0.52)
    obj(mb, "C12_Permissao_Trabalho_e_Rota_Fuga", C, cena="C12", props={"tipo": "documento_no_local_e_rota_de_fuga"})
    # sirene / alarme de emergencia no nucleo (EV17)
    mb = MB()
    sxp, syp, szp = 20.4, 13.93, z + 2.25
    mb.box((sxp - 0.14, syp - 0.12, szp - 0.14), (sxp + 0.14, syp, szp + 0.14), "vermelho_seguranca")
    mb.cyl((sxp, syp - 0.12, szp), (sxp, syp - 0.22, szp), 0.1, "vermelho_escuro", n=10)
    mb.cyl((sxp, syp - 0.12, szp + 0.2), (sxp, syp - 0.12, szp + 0.3), 0.05, "e:aviso_luz", n=8)
    decal(mb, uvt, "alarme", (sxp, syp - 0.002, szp - 0.33), (0, -1, 0), 0.4)
    obj(mb, "EV17_Sirene_Alarme_Pav04", C, cena="EV17", props={"evento": "EVENTO_ALARME", "tipo": "sirene_emergencia"})

    # protecao das janelas dos pav 1 a 4 (travessao a 1,20 m nos vaos de janela)
    mb = MB()
    XL, YL = L.TA_XL, L.TA_YL
    for n in range(1, 5):
        z0 = L.TA_Z(n)
        for face in ("S", "N", "W", "E"):
            horizontal = face in ("S", "N")
            lines = XL if horizontal else YL
            for bi, (a_, b_) in enumerate(zip(lines[:-1], lines[1:])):
                if horizontal:
                    ra = L.TA_PILAR(a_, Y0 if face == "S" else Y1)
                    rb = L.TA_PILAR(b_, Y0 if face == "S" else Y1)
                    wa, wb = ra[2], rb[0]
                else:
                    ra = L.TA_PILAR(X0 if face == "W" else X1, a_)
                    rb = L.TA_PILAR(X0 if face == "W" else X1, b_)
                    wa, wb = ra[3], rb[1]
                if face == "N" and a_ >= 16.4 and b_ <= 21.6:
                    continue
                if face == "W" and a_ == 10.0:
                    continue
                if n == 4 and face == "S" and bi in (3, 4):
                    continue
                span = wb - wa
                ww = 1.2 if horizontal else 1.4
                for f in (0.27, 0.73):
                    c_ = wa + span * f
                    if horizontal:
                        yy = Y0 - 0.02 if face == "S" else Y1 + 0.02
                        mb.cyl((c_ - ww / 2 - 0.05, yy, z0 + 1.2), (c_ + ww / 2 + 0.05, yy, z0 + 1.2), 0.022, "amarelo_linha_vida", n=6)
                    else:
                        xx = X0 - 0.02 if face == "W" else X1 + 0.02
                        mb.cyl((xx, c_ - ww / 2 - 0.05, z0 + 1.2), (xx, c_ + ww / 2 + 0.05, z0 + 1.2), 0.022, "amarelo_linha_vida", n=6)
    obj(mb, "TorreA_Pav01a04_Protecao_Vaos_Janela", C, cena="C12", props={"categoria": "protecao_coletiva", "tipo": "travessao_1,20m_vaos_de_janela",
        "nr_ref": "NR-18 18.9.4.2"})

    # ================================================================ 40e isolamento no terreo abaixo da frente de trabalho (C14 / EV02)
    C = Cs["40e_Isolamento_Terreo"]
    ix0, iy0, ix1, iy1 = L.TR_ISOLAMENTO

    def gradil(mb, a, b, placa_uv=None, placa_normal=None):
        a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
        d = b - a
        Ls = d.length
        u = d / Ls
        n = Vector((-u.y, u.x, 0))
        for s in (0.05, Ls - 0.05):
            p = a + u * s
            mb.box((p.x - 0.03, p.y - 0.03, 0.0), (p.x + 0.03, p.y + 0.03, 1.1), "cinza_claro", nobottom=True)
            mb.strut(tuple(p - n * 0.3), tuple(p + n * 0.3), 0.06, "concreto_escuro", h=0.08)
        for hz in (0.12, 1.07):
            mb.strut(tuple(a + u * 0.05 + Vector((0, 0, hz))), tuple(b - u * 0.05 + Vector((0, 0, hz))), 0.03, "cinza_claro")
        mb.quad_uv([tuple(a + u * 0.05 + Vector((0, 0, 0.12))), tuple(b - u * 0.05 + Vector((0, 0, 0.12))),
                    tuple(b - u * 0.05 + Vector((0, 0, 1.07))), tuple(a + u * 0.05 + Vector((0, 0, 1.07)))],
                   [(0, 0), (Ls / 0.15, 0), (Ls / 0.15, 6.3), (0, 6.3)], K.S_REDE)
        mb.strut(tuple(a + u * 0.05 + Vector((0, 0, 0.9))), tuple(b - u * 0.05 + Vector((0, 0, 0.9))), 0.002, "vermelho_seguranca", h=0.12, up=tuple(n))
        if placa_uv:
            m = (a + b) / 2
            decal(mb, uvt, placa_uv, (m.x + placa_normal[0] * 0.03, m.y + placa_normal[1] * 0.03, 0.62), placa_normal, 0.62)

    def perimetro_isolamento(excluir_oeste_movel=True):
        segs = []
        xs = [ix0 + k * (ix1 - ix0) / 3 for k in range(4)]
        for k in range(3):
            segs.append(((xs[k], iy0), (xs[k + 1], iy0), "S", k))
        ys = [iy0, (iy0 + iy1) / 2, iy1]
        for k in range(2):
            segs.append(((ix0, ys[k]), (ix0, ys[k + 1]), "W", k))
            segs.append(((ix1, ys[k]), (ix1, ys[k + 1]), "E", k))
        return segs

    mb = MB()
    for (a, b, face, k) in perimetro_isolamento():
        if face == "W" and k == 0:
            continue
        pl = None
        nrm = None
        if face == "S" and k == 1:
            pl, nrm = "area_isolada", (0.0, -1.0)
        if face == "W" and k == 1:
            pl, nrm = "area_isolada", (-1.0, 0.0)
        gradil(mb, a, b, pl, nrm)
    gradil(mb, (27.45, 4.4), (31.25, 4.4))
    for (x, y) in ((ix0, iy0), (ix1, iy0)):
        cone(mb, x - 0.35 if x == ix0 else x + 0.35, y - 0.35)
    obj(mb, "C14_Area_Inferior_Isolada", C, visivel=False, cena="C14", props={"estado": "AREA_INFERIOR_ISOLADA=SIM",
        "variavel": "AREA_INFERIOR_ISOLADA", "valor": "SIM", "inclui_tambem": "C14_Barreira_Oeste_Movel"})
    mb = MB()
    a, b = (ix0, iy0), (ix0, (iy0 + iy1) / 2)
    gradil(mb, a, b)
    obj(mb, "C14_Barreira_Oeste_Movel", C, visivel=False, cena="C14", props={"estado": "AREA_INFERIOR_ISOLADA=SIM", "evento_relacionado": "EV02"})
    mb = MB()
    a2 = (ix0 - 1.6, iy0 + 0.2)
    b2 = (ix0 - 1.0, iy0 + 2.2)
    gradil(mb, a2, b2)
    obj(mb, "EV02_Barreira_Afastada", C, visivel=False, cena="EV02", props={"evento": "EVENTO_INVASAO_AREA_ISOLADA", "oculta": "C14_Barreira_Oeste_Movel"})
    # estado inicial: isolamento incompleto (paineis encostados, cones soltos) e passagem livre
    mb = MB()
    with mb.at((ix1 - 0.4, iy1 - 0.25, 0.0), rz=90):
        for k in range(3):
            mb.box((-1.0, -0.06 + k * 0.07, 0.0), (1.0, 0.0 + k * 0.07, 1.1), "cinza_claro")
    cone(mb, ix0 + 0.4, iy1 - 0.4)
    cone(mb, ix0 + 1.9, iy0 + 0.8, deitado=True, rz=30)
    mb.strut((ix0 + 0.4, iy1 - 0.4, 0.02), (ix0 + 3.0, iy1 - 1.3, 0.02), 0.004, "amarelo_linha_vida", h=0.07)
    obj(mb, "C14_Area_Inferior_Nao_Isolada", C, cena="C14", props={"estado": "inicial (isolamento nao montado)", "variavel": "AREA_INFERIOR_ISOLADA",
        "valor": "NAO", "interativo": True, "rotulo": "Area abaixo da frente de trabalho"})

    # ================================================================ 40f sinalizacao e emergencia no canteiro
    C = Cs["40f_Sinalizacao_Emergencia"]
    mb = MB()
    bx_, by_ = 38.6, 1.6
    mb.cyl((bx_, by_, 5.5), (bx_, by_, 8.6), 0.03, "cinza_claro", n=6)
    mb.cyl((bx_, by_, 8.5), (bx_ - 1.1, by_ + 0.35, 8.35), 0.22, "laranja_seguranca", n=8, r1=0.08,
           caps=False)
    for k in (1, 2):
        u = k / 3
        p = (bx_ - 1.1 * u, by_ + 0.35 * u, 8.5 - 0.15 * u)
        mb.cyl((p[0] + 0.02, p[1], p[2]), (p[0] - 0.08, p[1] + 0.03, p[2]), 0.23 - 0.14 * u, "branco_sinal", n=8, caps=False)
    obj(mb, "C17_Biruta_Canteiro", C, cena="C17", props={"tipo": "biruta_indicador_de_vento"})
    mb = MB()
    mb.box((21.86, -26.5, 2.21), (22.14, -26.38, 2.49), "vermelho_seguranca")
    mb.cyl((22.0, -26.44, 2.49), (22.0, -26.44, 2.61), 0.05, "e:aviso_luz", n=8)
    mb.cyl((24.6, -24.3, 0.0), (24.6, -24.3, 3.0), 0.04, "cinza_claro", n=6)
    mb.box((24.46, -24.44, 3.0), (24.74, -24.16, 3.28), "vermelho_seguranca")
    mb.cyl((24.6, -24.3, 3.28), (24.6, -24.3, 3.4), 0.05, "e:aviso_luz", n=8)
    obj(mb, "EV17_Sirenes_Canteiro", C, cena="EMERG", props={"evento": "EVENTO_ALARME", "tipo": "sirene_emergencia_canteiro"})

    # esconde as bases substituidas no estado inicial
    for nome in ("TorreA_Pav04_GcR_Sul_05a",):
        o = bpy.data.objects.get(nome)
        if o:
            o["visivel_inicial"] = False
            o["variantes"] = "C13_GcR_Sul05a_Levemente_Solto (inicial) | CONSEQ_GcR_Sul05a_Cedendo"
            mostrar(o, False)
    for nome, var in (("TorreA_Pav04_GcR_Sul_05b", "EV10_GcR_Sul05b_Travessao_Intermediario_Removido | CONSEQ_Conexao_GuardaCorpo_Cedendo"),
                      ("TorreA_Pav04_GcR_Sul_04a", "EV01_GcR_Sul04a_Removido_Vao_Aberto"),
                      ("TorreA_Pav04_GcR_Sul_04b", "EV15_GcR_Sul04b_Impacto_Sem_Dano_Aparente | EV15_GcR_Sul04b_Deslocado_Depois")):
        o = bpy.data.objects.get(nome)
        if o:
            o["visivel_inicial"] = True
            o["variantes"] = var
    for nome in ("TorreA_Pav04_GcR_Sul_05b", "TorreA_Pav04_GcR_Sul_04a", "TorreA_Pav04_GcR_Sul_04b"):
        o = bpy.data.objects.get(nome)
        if o:
            mostrar(o, True)
    allo = list(bpy.data.collections[PAI].all_objects)
    return {"objetos": len(allo), "tris": K.tri_count(allo)}
