# gen_20_gruas.py - gruas de torre (amarela e vermelha/branca) com cargas icadas
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB


def lattice_mast(mb, H, a, c, sec=3.0, rc=0.07, rb=0.035, z0=0.3):
    corners = [(-a, -a), (a, -a), (a, a), (-a, a)]
    for (x, y) in corners:
        mb.cyl((x, y, z0), (x, y, H), rc, c, n=6, caps=False)
    z = z0
    k = 0
    while z < H - 0.05:
        z1 = min(H, z + sec)
        for f in range(4):
            p, q = corners[f], corners[(f + 1) % 4]
            mb.cyl((p[0], p[1], z1), (q[0], q[1], z1), rb, c, n=5, caps=False)
            if (k + f) % 2 == 0:
                mb.cyl((p[0], p[1], z), (q[0], q[1], z1), rb, c, n=5, caps=False)
            else:
                mb.cyl((q[0], q[1], z), (p[0], p[1], z1), rb, c, n=5, caps=False)
        k += 1
        z = z1


def grua(nome, base, H, Lj, Lc, theta, trolley_r, rope_len, cm, cj, ch, ccab, carga):
    C = K.coll("20_Gruas")
    bx, by = base
    root = K.empty("GRP_Grua_" + nome, C, (bx, by, 0.0), size=3.0,
                   props={"categoria": "grua", "altura_gancho_m": H, "lanca_m": Lj, "contralanca_m": Lc,
                          "nr_ref": "NR-18 18.10 / NR-12 - gruas"})
    # ---------------- fundacao + cercado
    mb = MB()
    mb.box((-3.0, -3.0, -1.2), (3.0, 3.0, 0.3), "concreto", top="concreto_claro", nobottom=True)
    for (x, y) in ((-0.8, -0.8), (0.8, -0.8), (0.8, 0.8), (-0.8, 0.8)):
        mb.box((x - 0.25, y - 0.25, 0.3), (x + 0.25, y + 0.25, 0.55), "grafite")
    E = 3.8
    pts = [(-E, -E), (E, -E), (E, E), (-E, E)]
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        Lf = math.dist(a, b)
        seg = [(a, b)]
        if i == 0:
            seg = [(a, (-0.6, -E)), ((0.6, -E), b)]
        for (p, q) in seg:
            Ls = math.dist(p, q)
            npst = max(2, int(math.ceil(Ls / 2.0)) + 1)
            for j in range(npst):
                u = j / (npst - 1)
                px, py = p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u
                mb.box((px - 0.03, py - 0.03, 0.0), (px + 0.03, py + 0.03, 2.0), "amarelo_escuro", nobottom=True)
            for zr in (0.1, 1.95):
                mb.strut((p[0], p[1], zr), (q[0], q[1], zr), 0.04, "amarelo_escuro")
            mb.quad_uv([(p[0], p[1], 0.12), (q[0], q[1], 0.12), (q[0], q[1], 1.93), (p[0], p[1], 1.93)],
                       [(0, 0), (Ls / 0.3, 0), (Ls / 0.3, 6), (0, 6)], K.S_REDE)
    mb.strut((-0.6, -E, 1.0), (0.6, -E - 0.9, 1.0), 0.04, "amarelo_escuro")
    K.finish(mb, "Grua_%s_Fundacao_Cercado" % nome, C, parent=root, props={"categoria": "grua", "parte": "fundacao_e_cercado", "interativo": True})

    # ---------------- torre (mastro), escada, plataformas de descanso, linha de vida vertical
    a = 0.8
    mb = MB()
    lattice_mast(mb, H, a, cm)
    ly = -a + 0.28
    for dx in (-0.22, 0.22):
        mb.strut((dx, ly, 0.3), (dx, ly, H), 0.035, "cinza_escuro", h=0.06)
    z = 0.6
    while z < H - 0.2:
        mb.strut((-0.22, ly, z), (0.22, ly, z), 0.022, "cinza_escuro", caps=False)
        z += 0.3
    z = 9.3
    while z < H - 3:
        mb.box((-a + 0.05, -a + 0.05, z), (a - 0.05, -a + 0.05 + 0.1, z + 0.05), "grafite")
        mb.box((-a + 0.05, -a + 0.75, z), (a - 0.05, a - 0.05, z + 0.05), "grafite")
        mb.box((0.28, -a + 0.1, z), (a - 0.05, -a + 0.75, z + 0.05), "grafite")
        z += 9.0
    mb.cyl((0.0, ly + 0.1, 0.4), (0.0, ly + 0.1, H), 0.007, "amarelo_linha_vida", n=4, caps=False, smooth=False)
    mb.box((-0.05, ly + 0.04, 1.5), (0.05, ly + 0.16, 1.72), "amarelo_linha_vida")
    K.finish(mb, "Grua_%s_Torre_Escada" % nome, C, parent=root,
             props={"categoria": "grua", "parte": "torre_com_escada_e_linha_de_vida_vertical", "altura_m": H, "interativo": True})

    # ---------------- parte giratoria
    giro = K.empty("GRP_Grua_%s_Giro" % nome, C, (0.0, 0.0, H), rz=theta, parent=root, size=2.0,
                   props={"categoria": "grua", "parte": "giro", "animavel": "rotation_euler.z"})
    mb = MB()
    mb.cyl((0, 0, -0.5), (0, 0, 0.0), 1.05, "grafite", n=12, smooth=False)
    mb.box((-1.2, -1.2, 0.0), (1.2, 1.2, 1.0), ch, top="grafite")
    mb.box((-1.9, -1.9, -0.12), (1.9, 1.9, 0.0), "grafite")
    for (p, q) in (((-1.9, -1.9), (1.9, -1.9)), ((1.9, -1.9), (1.9, 1.9)), ((1.9, 1.9), (-1.9, 1.9)), ((-1.9, 1.9), (-1.9, -1.9))):
        mb.strut((p[0], p[1], 1.05), (q[0], q[1], 1.05), 0.04, "amarelo_linha_vida")
        mb.strut((p[0], p[1], 0.55), (q[0], q[1], 0.55), 0.03, "amarelo_linha_vida")
    for (x, y) in ((-1.9, -1.9), (1.9, -1.9), (1.9, 1.9), (-1.9, 1.9)):
        mb.box((x - 0.03, y - 0.03, 0.0), (x + 0.03, y + 0.03, 1.08), "amarelo_linha_vida")
    # cabine do operador
    mb.box((0.3, -2.45, 0.1), (1.9, -1.25, 2.35), ccab, top="branco")
    mb.box((1.9, -2.35, 0.9), (1.93, -1.35, 2.2), "g:vidro_veiculo")
    mb.box((0.4, -2.48, 0.9), (1.8, -2.45, 2.2), "g:vidro_veiculo")
    mb.box((0.4, -1.25, 1.2), (1.2, -1.22, 2.1), "g:vidro_veiculo")
    mb.cyl((1.6, -2.1, 2.35), (1.6, -2.1, 2.55), 0.08, "e:aviso_luz", n=6)
    # torre de cabeca (A) - ponto de fixacao dos tirantes
    Ht = 7.5
    top = (0.0, 0.0, Ht)
    for (x, y) in ((-0.9, -0.9), (0.9, -0.9), (0.9, 0.9), (-0.9, 0.9)):
        mb.cyl((x, y, 1.0), top, 0.06, ch, n=6, caps=False)
    for hz in (3.2, 5.4):
        s = 0.9 * (1 - (hz - 1.0) / (Ht - 1.0))
        for (p, q) in (((-s, -s), (s, -s)), ((s, -s), (s, s)), ((s, s), (-s, s)), ((-s, s), (-s, -s))):
            mb.cyl((p[0], p[1], hz), (q[0], q[1], hz), 0.03, ch, n=5, caps=False)
    mb.box((-0.25, -0.25, Ht - 0.1), (0.25, 0.25, Ht + 0.3), ch)
    mb.cyl((0, 0, Ht + 0.3), (0, 0, Ht + 0.55), 0.1, "e:aviso_luz", n=8)
    mb.cyl((0.2, 0.0, Ht + 0.3), (0.2, 0.0, Ht + 1.2), 0.015, "grafite", n=4)
    for k in range(3):
        ang = 2 * math.pi * k / 3
        mb.box((0.2 + 0.25 * math.cos(ang) - 0.05, 0.25 * math.sin(ang) - 0.05, Ht + 1.15), (0.2 + 0.25 * math.cos(ang) + 0.05, 0.25 * math.sin(ang) + 0.05, Ht + 1.25), "branco")
    # lanca (secao triangular)
    x0 = 1.2
    w, hj = 0.7, 1.35
    mb.box((x0, -w - 0.06, 0.0), (Lj, -w + 0.06, 0.12), cj)
    mb.box((x0, w - 0.06, 0.0), (Lj, w + 0.06, 0.12), cj)
    mb.cyl((x0, 0, hj), (Lj, 0, hj), 0.06, cj, n=6, caps=True)
    x = x0
    i = 0
    while x < Lj - 0.01:
        x1 = min(Lj, x + 2.0)
        mb.strut((x, -w, 0.06), (x, w, 0.06), 0.05, cj)
        if i % 2 == 0:
            mb.cyl((x, -w, 0.1), (x1, 0, hj), 0.03, cj, n=5, caps=False)
            mb.cyl((x, w, 0.1), (x1, 0, hj), 0.03, cj, n=5, caps=False)
        else:
            mb.cyl((x, 0, hj), (x1, -w, 0.1), 0.03, cj, n=5, caps=False)
            mb.cyl((x, 0, hj), (x1, w, 0.1), 0.03, cj, n=5, caps=False)
        mb.cyl((x, -w, 0.06), (x1, w, 0.06), 0.025, cj, n=4, caps=False)
        x = x1
        i += 1
    mb.strut((Lj, -w, 0.06), (Lj, w, 0.06), 0.08, cj)
    mb.cyl((Lj, 0, 0.1), (Lj, 0, hj), 0.05, cj, n=5)
    mb.cyl((Lj, 0, hj), (Lj, 0, hj + 0.2), 0.08, "e:aviso_luz", n=6)
    for f in (0.35, 0.72):
        mb.cyl(top, (Lj * f, 0, hj), 0.04, "grafite", n=5, caps=False)
    # contralanca com contrapesos, guincho e passarela
    mb.box((-Lc, -1.0, 0.0), (-1.0, -0.8, 0.45), ch)
    mb.box((-Lc, 0.8, 0.0), (-1.0, 1.0, 0.45), ch)
    xx = -1.0
    while xx > -Lc:
        mb.strut((xx, -0.8, 0.2), (xx, 0.8, 0.2), 0.08, ch)
        xx -= 2.0
    mb.box((-Lc + 0.1, -0.8, 0.42), (-1.0, 0.8, 0.47), "grafite")
    for s in (-1, 1):
        for xp in [(-1.2 - 2.0 * k) for k in range(int((Lc - 1.5) / 2.0) + 1)]:
            mb.box((xp - 0.025, s * 1.0 - 0.025, 0.45), (xp + 0.025, s * 1.0 + 0.025, 1.55), "amarelo_linha_vida", nobottom=True)
        mb.strut((-Lc + 0.2, s * 1.0, 1.5), (-1.0, s * 1.0, 1.5), 0.04, "amarelo_linha_vida")
        mb.strut((-Lc + 0.2, s * 1.0, 1.0), (-1.0, s * 1.0, 1.0), 0.03, "amarelo_linha_vida")
    for k in range(4):
        xa = -Lc + 0.2 + k * 0.82
        mb.box((xa, -1.1, -1.7), (xa + 0.78, 1.1, 0.35), "concreto", top="concreto_claro")
    mb.cyl((-Lc + 5.2, -0.6, 1.0), (-Lc + 5.2, 0.6, 1.0), 0.45, "grafite", n=10)
    mb.box((-Lc + 5.8, -0.7, 0.47), (-Lc + 6.9, 0.7, 1.4), "azul_escuro", top="grafite")
    mb.box((-Lc + 7.3, -0.5, 0.47), (-Lc + 8.1, 0.5, 2.0), "cinza_claro", top="grafite")
    mb.cyl(top, (-Lc + 0.8, 0, 0.45), 0.045, "grafite", n=5, caps=False)
    K.finish(mb, "Grua_%s_Lanca_Contralanca_Cabine" % nome, C, parent=giro,
             props={"categoria": "grua", "parte": "parte_giratoria", "interativo": True})

    # ---------------- carro, cabos, moitao e carga
    carro = MB()
    carro.box((-0.6, -0.8, -0.55), (0.6, 0.8, -0.05), "grafite", top=cj)
    for sx in (-0.45, 0.45):
        for sy in (-0.7, 0.7):
            carro.cyl((sx, sy - 0.06, 0.0), (sx, sy + 0.06, 0.0), 0.12, "cinza_escuro", n=8)
    for sy in (-0.25, 0.25):
        carro.cyl((0.0, sy - 0.05, -0.55), (0.0, sy + 0.05, -0.55), 0.25, "cinza_claro", n=10)
    oc = K.finish(carro, "Grua_%s_Carro_Trole" % nome, C, parent=giro, loc=(trolley_r, 0.0, 0.0),
                  props={"categoria": "grua", "parte": "carro", "raio_m": trolley_r, "animavel": "location.x"})
    cab = MB()
    for (dx, dy) in ((-0.12, -0.18), (0.12, -0.18), (-0.12, 0.18), (0.12, 0.18)):
        cab.cyl((dx, dy, 0.0), (dx, dy, -1.0), 0.011, "cinza_escuro", n=4, caps=False, smooth=False)
    ocab = K.finish(cab, "Grua_%s_Cabos_Aco" % nome, C, parent=oc, loc=(0.0, 0.0, -0.8),
                    props={"categoria": "grua", "parte": "cabos", "animavel": "scale.z = comprimento"})
    ocab.scale = (1.0, 1.0, rope_len)
    hk = MB()
    hk.box((-0.28, -0.22, -0.75), (0.28, 0.22, 0.0), "amarelo_maquina")
    for dy in (-0.23, 0.23):
        hk.cyl((0.0, dy - 0.03, -0.2), (0.0, dy + 0.03, -0.2), 0.2, "zebrado_preto", n=10)
    hk.box((-0.06, -0.06, -1.05), (0.06, 0.06, -0.75), "grafite")
    hk.strut((0.0, 0.0, -1.05), (0.0, 0.0, -1.35), 0.09, "grafite")
    hk.strut((0.0, 0.0, -1.35), (0.22, 0.0, -1.3), 0.08, "grafite")
    hk.strut((0.22, 0.0, -1.3), (0.24, 0.0, -1.12), 0.06, "grafite")
    ohk = K.finish(hk, "Grua_%s_Moitao_Gancho" % nome, C, parent=oc, loc=(0.0, 0.0, -0.8 - rope_len),
                   props={"categoria": "grua", "parte": "moitao_gancho"})
    ld = MB()
    if carga == "vigas":
        for i in range(5):
            y = -0.45 + i * 0.22
            zb = -3.2
            for (zz0, zz1, hw) in ((zb, zb + 0.02, 0.1), (zb + 0.28, zb + 0.3, 0.1)):
                ld.box((-3.0, y - hw, zz0), (3.0, y + hw, zz1), "ferrugem")
            ld.box((-3.0, y - 0.01, zb + 0.02), (3.0, y + 0.01, zb + 0.28), "vermelho_escuro")
        for sx in (-2.2, 2.2):
            ld.strut((0.0, 0.0, -1.35), (sx, -0.55, -2.9), 0.05, "laranja_seguranca", h=0.012)
            ld.strut((0.0, 0.0, -1.35), (sx, 0.55, -2.9), 0.05, "laranja_seguranca", h=0.012)
            ld.box((sx - 0.04, -0.58, -3.25), (sx + 0.04, 0.58, -2.88), "laranja_seguranca")
        ld.cyl((2.9, 0.0, -3.2), (2.7, 0.15, -6.2), 0.01, "amarelo_linha_vida", n=4, caps=False)
        nomec = "Feixe_Vigas_Aco"
    else:
        ld.lathe([(0.32, -3.6), (0.7, -2.5), (0.72, -1.95), (0.65, -1.85)], "cinza_medio", n=12, cap0="grafite", cap1="concreto_fresco")
        ld.box((-0.08, -0.8, -2.1), (0.08, 0.8, -1.95), "amarelo_escuro")
        for sy in (-0.75, 0.75):
            ld.strut((0.0, 0.0, -1.35), (0.0, sy, -2.0), 0.03, "cinza_escuro")
        ld.strut((0.3, -0.1, -3.55), (0.9, -0.1, -3.2), 0.05, "vermelho_seguranca")
        ld.cyl((0.0, 0.0, -3.65), (0.0, 0.0, -3.6), 0.2, "grafite", n=8)
        nomec = "Cacamba_Concreto"
    K.finish(ld, "Grua_%s_Carga_%s" % (nome, nomec), C, parent=ohk,
             props={"categoria": "carga_icada", "tipo": nomec, "nr_ref": "NR-18 18.10 - nao permanecer sob carga suspensa", "interativo": True})
    return root


def build():
    C = K.coll("20_Gruas")
    K.clear_coll(C)
    ga = L.GRUA_AMARELA
    gv = L.GRUA_VERMELHA
    grua("Amarela", ga, 47.0, 45.0, 14.0, 162.0, 10.5, 11.2, "amarelo_maquina", "amarelo_maquina", "amarelo_maquina", "branco", "cacamba")
    grua("Vermelha", gv, 36.0, 40.0, 12.0, -5.0, 22.0, 0.6, "branco", "branco", "vermelho_seguranca", "vermelho_seguranca", "vigas")
    return {"objetos": len(C.objects)}
