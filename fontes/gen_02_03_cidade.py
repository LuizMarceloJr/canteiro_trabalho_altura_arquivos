# gen_02_03_cidade_mobiliario_veiculos.py - postes, arvores, semaforos, ponto de onibus, orelhao, lixeiras, carros
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
V = sys.modules["veiculos"]
MB = K.MB


def proto_poste():
    mb = MB()
    mb.cyl((0, 0, 0), (0, 0, 0.35), 0.16, "poste_verde", n=8, smooth=False)
    mb.cyl((0, 0, 0.35), (0, 0, 5.2), 0.07, "poste_verde", n=8, r1=0.05)
    mb.cyl((0, 0, 2.4), (0, 0, 2.5), 0.09, "poste_verde", n=8)
    mb.strut((0, 0, 4.9), (0.9, 0, 5.15), 0.05, "poste_verde")
    mb.strut((0.9, 0, 5.15), (1.25, 0, 5.05), 0.05, "poste_verde")
    mb.box((1.1, -0.18, 4.72), (1.4, 0.18, 4.95), "poste_verde")
    mb.box((1.14, -0.14, 4.4), (1.36, 0.14, 4.72), "e:lampada")
    mb.hull([(1.05, -0.22, 4.95), (1.45, -0.22, 4.95), (1.45, 0.22, 4.95), (1.05, 0.22, 4.95), (1.25, 0.0, 5.2)], "poste_verde")
    mb.box((1.12, -0.16, 4.35), (1.38, 0.16, 4.4), "poste_verde")
    return K.mesh_only(mb, "PROTO_Poste_Iluminacao")


def proto_arvore(var, rng):
    mb = MB()
    mb.box((-0.6, -0.6, 0.0), (0.6, 0.6, 0.1), "meio_fio", top="terra_escura")
    if var == 2:
        mb.cyl((0, 0, 0.1), (0.2, 0.1, 5.5), 0.14, "tronco", n=6, r1=0.1)
        for k in range(7):
            a = 2 * math.pi * k / 7
            tip = (0.2 + 2.2 * math.cos(a), 0.1 + 2.2 * math.sin(a), 4.6)
            mb.hull([(0.2, 0.1, 5.55), (0.2 + 0.4 * math.cos(a + 0.4), 0.1 + 0.4 * math.sin(a + 0.4), 5.6), tip,
                     (0.2 + 1.2 * math.cos(a), 0.1 + 1.2 * math.sin(a), 5.45)], "folha_escura" if k % 2 else "folha")
        return K.mesh_only(mb, "PROTO_Arvore_Palmeira")
    h = 2.2 if var == 0 else 2.8
    mb.cyl((0, 0, 0.1), (0, 0, h + 0.6), 0.14, "tronco", n=6, r1=0.1)
    mb.strut((0, 0, h - 0.4), (0.6, 0.2, h + 0.3), 0.08, "tronco")
    if var == 0:
        mb.blob((0.0, 0.0, h + 1.2), 1.55, "folha", sub=2, noise=0.1, rng=rng, squash=(1.0, 1.0, 0.9),
                colfn=lambda i, Vv, F: "folha_clara" if sum(Vv[j][2] for j in F[i]) > 0.8 else "folha")
        mb.blob((0.8, 0.5, h + 0.7), 0.95, "folha", sub=1, noise=0.12, rng=rng)
        mb.blob((-0.7, -0.4, h + 0.8), 0.9, "folha_escura", sub=1, noise=0.12, rng=rng)
        nm = "PROTO_Arvore_Copa_Redonda"
    else:
        mb.blob((0.0, 0.0, h + 1.8), 1.3, "folha_escura", sub=2, noise=0.1, rng=rng, squash=(1.0, 1.0, 1.55),
                colfn=lambda i, Vv, F: "folha" if sum(Vv[j][2] for j in F[i]) > 0.6 else "folha_escura")
        nm = "PROTO_Arvore_Copa_Alta"
    return K.mesh_only(mb, nm)


def proto_semaforo():
    mb = MB()
    mb.cyl((0, 0, 0), (0, 0, 5.6), 0.09, "grafite", n=8)
    mb.strut((0, 0, 5.4), (3.2, 0, 5.4), 0.1, "grafite", h=0.12)
    for (x, z, lit) in ((2.9, 4.85, True), (0.0, 2.6, False)):
        mb.box((x - 0.17, -0.15, z - 0.55), (x + 0.17, 0.15, z + 0.55), "preto_suave")
        for k, c in enumerate(("sinal_vermelho", "sinal_amarelo", "sinal_verde")):
            zz = z + 0.33 - k * 0.33
            col = ("e:" + c) if (k == 0 and lit) or (k == 2 and not lit) else "grafite"
            mb.cyl((x + 0.17, 0, zz), (x + 0.2, 0, zz), 0.1, col, n=8)
    return K.mesh_only(mb, "PROTO_Semaforo")


def proto_balizador():
    mb = MB()
    mb.cyl((0, 0, 0), (0, 0, 0.85), 0.06, "preto_suave", n=8)
    mb.cyl((0, 0, 0.6), (0, 0, 0.68), 0.065, "branco_sinal", n=8)
    return K.mesh_only(mb, "PROTO_Balizador")


def build():
    CM = K.coll("02_Cidade_Mobiliario")
    CV = K.coll("03_Cidade_Veiculos")
    K.clear_coll(CM)
    K.clear_coll(CV)
    rng = random.Random(77)
    poste = proto_poste()
    arv = [proto_arvore(0, rng), proto_arvore(1, rng), proto_arvore(2, rng)]
    sem = proto_semaforo()
    bal = proto_balizador()
    zones_x = [(xc - w / 2 - 9, xc + w / 2 + 9) for (xc, w) in L.RUAS_NS]
    zones_y = [(yc - h / 2 - 9, yc + h / 2 + 9) for (yc, h) in L.RUAS_LO]

    def free(v, zones):
        return all(not (a <= v <= b) for (a, b) in zones)
    n_poste = n_arv = 0
    # postes e arvores ao longo das ruas L-O (incluindo a avenida)
    for (yc, h) in L.RUAS_LO:
        for side in (-1, 1):
            yy = yc + side * (h / 2 + 0.7)
            yt = yc + side * (h / 2 + 2.3)
            x = -150.0
            k = 0
            while x <= 150.0:
                if free(x, zones_x):
                    if k % 2 == 0:
                        K.inst("Cidade_Poste_%03d" % n_poste, poste, CM, (x, yy, 0.0), rz=-90.0 * side)
                        n_poste += 1
                    elif not (yc == -41.0 and side == 1 and -40 < x < 40) and not (yc == -41.0 and side == -1 and -14 < x < 12):
                        K.inst("Cidade_Arvore_%03d" % n_arv, arv[rng.randint(0, 1) if abs(yc) > 50 else rng.choice((0, 0, 1, 2))], CM,
                               (x + rng.uniform(-0.5, 0.5), yt, 0.0), rz=rng.uniform(0, 360), scale=rng.uniform(0.85, 1.15))
                        n_arv += 1
                x += 12.5
                k += 1
    # postes nas ruas N-S
    for (xc, w) in L.RUAS_NS:
        for side in (-1, 1):
            xx = xc + side * (w / 2 + 0.7)
            y = -125.0
            k = 0
            while y <= 175.0:
                if free(y, zones_y) and k % 2 == 0:
                    K.inst("Cidade_Poste_%03d" % n_poste, poste, CM, (xx, y, 0.0), rz=180.0 if side > 0 else 0.0)
                    n_poste += 1
                elif free(y, zones_y) and abs(xc) > 100 or (free(y, zones_y) and xc == -49.0 and side < 0):
                    K.inst("Cidade_Arvore_%03d" % n_arv, arv[rng.randint(0, 1)], CM, (xc + side * (w / 2 + 2.3), y + rng.uniform(-0.5, 0.5), 0.0),
                           rz=rng.uniform(0, 360), scale=rng.uniform(0.85, 1.15))
                    n_arv += 1
                y += 12.5
                k += 1
    # praca leste e estacionamento sudoeste
    for (x, y) in ((88.5, 23.0), (91.5, 36.5), (104.5, 24.0), (105.5, 37.0), (89.0, 30.0), (106.0, 30.5)):
        K.inst("Cidade_Arvore_%03d" % n_arv, arv[0], CM, (x, y, 0.12), rz=rng.uniform(0, 360), scale=1.1)
        n_arv += 1
    for y in (-110.0, -100.0, -74.0, -62.0):
        K.inst("Cidade_Arvore_%03d" % n_arv, arv[2], CM, (-105.5, y, 0.03), rz=rng.uniform(0, 360))
        n_arv += 1
    # semaforos nos cruzamentos do quarteirao da obra
    n_sem = 0
    for (xc, w) in ((-49.0, 10.0), (49.0, 10.0)):
        for (yc, h) in ((-41.0, 14.0), (83.0, 10.0)):
            for (sx, sy, rz) in ((1, 1, 180.0), (-1, -1, 0.0), (1, -1, 90.0), (-1, 1, -90.0)):
                K.inst("Cidade_Semaforo_%02d" % n_sem, sem, CM, (xc + sx * (w / 2 + 0.6), yc + sy * (h / 2 + 0.6), 0.0), rz=rz)
                n_sem += 1
    # balizadores junto as faixas de pedestre do quarteirao
    nb = 0
    for (xc, w) in ((-49.0, 10.0), (49.0, 10.0)):
        for (yc, h) in ((-41.0, 14.0),):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    for k in range(3):
                        K.inst("Cidade_Balizador_%02d" % nb, bal, CM, (xc + sx * (w / 2 + 1.4 + k * 1.4), yc + sy * (h / 2 + 0.45), 0.0))
                        nb += 1

    # ---------------- ponto de onibus, orelhao, lixeiras de reciclagem, banco (calcada sul da avenida)
    mb = MB()
    bx, by = -3.0, -50.2
    for (px, py) in ((bx - 2.6, by - 0.7), (bx + 2.6, by - 0.7), (bx - 2.6, by + 0.6), (bx + 2.6, by + 0.6)):
        mb.box((px - 0.05, py - 0.05, 0.0), (px + 0.05, py + 0.05, 2.6), "preto_suave", nobottom=True)
    mb.hull([(bx - 2.8, by - 1.0, 2.6), (bx + 2.8, by - 1.0, 2.6), (bx - 2.8, by + 1.2, 2.75), (bx + 2.8, by + 1.2, 2.75),
             (bx - 2.8, by - 1.0, 2.66), (bx + 2.8, by - 1.0, 2.66), (bx - 2.8, by + 1.2, 2.81), (bx + 2.8, by + 1.2, 2.81)], "t:vidro_claro")
    mb.box((bx - 2.8, by - 1.02, 2.5), (bx + 2.8, by - 0.92, 2.62), "preto_suave")
    mb.box((bx - 2.55, by - 0.72, 0.25), (bx + 2.55, by - 0.68, 2.4), "t:vidro_claro")
    mb.box((bx - 2.55, by - 0.76, 2.4), (bx + 2.55, by - 0.64, 2.5), "preto_suave")
    mb.box((bx - 1.8, by - 0.55, 0.45), (bx + 1.2, by - 0.15, 0.5), "madeira")
    for px in (bx - 1.6, bx + 1.0):
        mb.box((px - 0.03, by - 0.5, 0.0), (px + 0.03, by - 0.2, 0.45), "preto_suave")
    mb.box((bx + 2.62, by - 0.75, 0.3), (bx + 2.72, by + 0.6, 2.3), "preto_suave")
    mb.box((bx + 2.6, by - 0.65, 0.4), (bx + 2.62, by + 0.5, 2.2), "e:agua")
    mb.cyl((bx - 3.6, by + 0.8, 0.0), (bx - 3.6, by + 0.8, 3.0), 0.04, "grafite", n=6)
    mb.box((bx - 3.95, by + 0.77, 2.3), (bx - 3.25, by + 0.83, 2.95), "azul_escuro")
    mb.box((bx - 3.85, by + 0.83, 2.4), (bx - 3.35, by + 0.84, 2.85), "branco")
    K.finish(mb, "Cidade_Ponto_Onibus", CM, props={"categoria": "cidade_mobiliario"})
    mb = MB()
    ox, oy = 5.5, -50.8
    mb.cyl((ox, oy, 0.0), (ox, oy, 1.9), 0.045, "grafite", n=6)
    with mb.at((ox, oy + 0.05, 1.25)):
        mb.lathe([(0.02, 1.02), (0.22, 0.98), (0.42, 0.82), (0.52, 0.55), (0.55, 0.2), (0.5, 0.0)], "orelhao_laranja", n=12, cap0=False, cap1=False,
                 color_fn=lambda k, i: "orelhao_laranja" if (i < 9 and i > 2) or k < 1 else "branco")
    mb.box((ox - 0.12, oy + 0.3, 1.45), (ox + 0.12, oy + 0.4, 1.8), "grafite")
    mb.box((ox - 0.06, oy + 0.28, 1.55), (ox + 0.06, oy + 0.3, 1.75), "preto_suave")
    K.finish(mb, "Cidade_Orelhao_Telefone_Publico", CM, props={"categoria": "cidade_mobiliario"})
    mb = MB()
    for k, c in enumerate(("lixeira_azul", "lixeira_vermelha", "lixeira_verde", "lixeira_amarela")):
        x = 8.0 + k * 0.62
        mb.box((x - 0.28, -51.4, 0.0), (x + 0.28, -50.9, 0.95), c, top="grafite", nobottom=True)
        mb.box((x - 0.29, -51.42, 0.95), (x + 0.29, -50.88, 1.02), c)
        mb.box((x - 0.12, -50.89, 0.75), (x + 0.12, -50.87, 0.82), "preto_suave")
    mb.box((11.5, -51.3, 0.42), (13.3, -50.9, 0.47), "madeira")
    mb.box((11.5, -51.32, 0.47), (13.3, -51.28, 0.85), "madeira")
    for x in (11.7, 13.1):
        mb.box((x - 0.03, -51.3, 0.0), (x + 0.03, -50.95, 0.42), "preto_suave")
    mb.cyl((-10.0, -48.6, 0.0), (-10.0, -48.6, 1.0), 0.03, "grafite", n=6)
    mb.cyl((-10.0, -48.45, 0.6), (-10.0, -48.45, 1.05), 0.2, "laranja_seguranca", n=10)
    mb.cyl((14.8, -48.7, 0.0), (14.8, -48.7, 0.55), 0.12, "vermelho_seguranca", n=8, cap="amarelo_maquina")
    mb.cyl((14.6, -48.7, 0.35), (15.0, -48.7, 0.35), 0.05, "vermelho_seguranca", n=6)
    K.finish(mb, "Cidade_Lixeiras_Reciclagem_Banco_Hidrante", CM, props={"categoria": "cidade_mobiliario"})

    # ---------------- veiculos
    CORES = ["carro_laranja", "carro_teal", "carro_verde", "carro_branco", "carro_vermelho", "carro_azul", "carro_bege", "carro_prata", "carro_preto", "carro_amarelo"]
    TIPOS = ["sedan", "hatch", "suv", "pickup", "hatch", "sedan", "van"]
    protos = {}

    def proto(tipo, cor):
        key = (tipo, cor)
        if key not in protos:
            protos[key] = K.mesh_only(V.carro(tipo, cor), "PROTO_Carro_%s_%s" % (tipo, cor))
        return protos[key]
    n_car = 0

    def car(x, y, rz, tipo=None, cor=None):
        nonlocal n_car
        tipo = tipo or rng.choice(TIPOS)
        cor = cor or rng.choice(CORES)
        K.inst("Cidade_Carro_%03d_%s" % (n_car, tipo), proto(tipo, cor), CV, (x, y, L.ZR), rz=rz, props={"categoria": "cidade_veiculo", "tipo": tipo})
        n_car += 1
    # avenida: faixas leste (sul) e oeste (norte)
    for (x, lane_y, rz) in ((-95, -46.25, 0), (-72, -42.75, 0), (-30, -42.75, 0), (26, -46.25, 0), (62, -42.75, 0), (110, -46.25, 0),
                            (-120, -35.75, 180), (-78, -39.25, 180), (-20, -35.75, 180), (18, -39.25, 180), (75, -35.75, 180), (130, -39.25, 180)):
        car(float(x), lane_y, float(rz))
    # parados no semaforo (cruzamento oeste)
    car(-59.5, -46.25, 0.0, "suv", "carro_prata")
    car(-65.5, -46.25, 0.0, "hatch", "carro_vermelho")
    car(-38.5, -35.75, 180.0, "sedan", "carro_azul")
    # ruas N-S: estacionados junto ao meio-fio
    for (xc, w) in L.RUAS_NS:
        for side in (-1, 1):
            x = xc + side * (w / 2 - 1.1)
            y = -120.0
            while y < 170.0:
                if free(y, zones_y) and rng.random() < 0.28:
                    car(x, y, 90.0 if side > 0 else -90.0)
                y += rng.uniform(6.0, 9.0)
    # circulando nas ruas N-S e na rua norte
    for (x, y, rz) in ((-51.75, 20.0, -90), (-46.25, 55.0, 90), (51.75, -8.0, -90), (46.25, 40.0, 90), (-20.0, 80.5, 180), (30.0, 85.5, 0), (-146.0, -70.0, 90), (148.0, 120.0, -90)):
        car(float(x), float(y), float(rz))
    # estacionamento do supermercado
    for i in range(12):
        if rng.random() < 0.6:
            car(-136.0 + i * 2.6 + 1.3, -115.5, 90.0)
        if rng.random() < 0.5:
            car(-136.0 + i * 2.6 + 1.3, -68.5, -90.0)
    K.finish(V.onibus("carro_azul", "branco"), "Cidade_Onibus_Parado_no_Ponto", CV, loc=(-3.0, -46.4, L.ZR), props={"categoria": "cidade_veiculo", "tipo": "onibus"})
    K.finish(V.caminhao_prancha("azul_escuro"), "Veiculo_Caminhao_Entrega_Vergalhoes_Portao_Oeste", CV, loc=(-46.5, 26.0, L.ZR), rz=-90.0,
             props={"categoria": "veiculo_obra", "tipo": "entrega_de_material", "interativo": True})
    return {"postes": n_poste, "arvores": n_arv, "semaforos": n_sem, "carros": n_car, "prototipos_carros": len(protos)}
