# gen_01_predios.py - predios do entorno (quarteirao detalhado + anel distante simplificado)
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB

STYLES = {
    "grade": dict(bay=2.2, pw=0.45, sh=1.0, d=0.30, fh=3.3, gh=4.4, glass="g:vidro_predio"),
    "grade_fina": dict(bay=1.6, pw=0.16, sh=0.45, d=0.22, fh=3.4, gh=5.0, glass="g:vidro_claro"),
    "janelas": dict(bay=2.8, pw=1.35, sh=1.45, d=0.28, fh=3.0, gh=3.8, glass="g:vidro_escuro"),
    "faixas": dict(bay=40.0, pw=0.9, sh=1.25, d=0.35, fh=3.3, gh=4.2, glass="g:vidro_predio"),
}


def predio(mb, x0, y0, x1, y1, floors, style, wall, rng, front=(), storefront=False, balconies=False,
           roof="telhado", crown=None, tanks=True, ac=True, simple=False, base=None):
    st = STYLES[style]
    fh, gh, d, bay, pw, sh = st["fh"], st["gh"], st["d"], st["bay"], st["pw"], st["sh"]
    glass = st["glass"]
    W, Dp = x1 - x0, y1 - y0
    H = gh + floors * fh
    base = base or wall
    mb.box((x0 + d, y0 + d, gh), (x1 - d, y1 - d, H), glass, nobottom=True, notop=True)
    if storefront:
        mb.box((x0 + 0.9, y0 + 0.9, 0.0), (x1 - 0.9, y1 - 0.9, gh), "g:vidro_escuro", nobottom=True, notop=True)
    else:
        mb.box((x0 + 0.15, y0 + 0.15, 0.0), (x1 - 0.15, y1 - 0.15, gh), base, nobottom=True, notop=True)
    mb.ring_box(x0 - 0.05, y0 - 0.05, x1 + 0.05, y1 + 0.05, gh - 0.6, gh + (sh if not simple else 0.5), d + 0.25, wall, nobottom=False)
    for k in range(1, floors):
        zb = gh + k * fh - sh * 0.5
        mb.ring_box(x0, y0, x1, y1, zb, zb + sh, d + 0.05, wall)

    def facade_pilasters(ax0, ax1, fixed, horizontal, inward):
        span = ax1 - ax0
        n = max(1, int(round(span / bay)))
        for i in range(n + 1):
            c = ax0 + i * span / n
            a = max(ax0, c - pw / 2)
            b = min(ax1, c + pw / 2)
            if i not in (0, n) and (style == "faixas" or simple):
                continue
            wpil = pw if i not in (0, n) else max(pw, 0.7)
            if i == 0:
                a, b = ax0, ax0 + wpil
            elif i == n:
                a, b = ax1 - wpil, ax1
            if horizontal:
                y_a, y_b = (fixed, fixed + inward * (d + 0.05))
                mb.box((a, min(y_a, y_b), gh), (b, max(y_a, y_b), H), wall, nobottom=True)
            else:
                x_a, x_b = (fixed, fixed + inward * (d + 0.05))
                mb.box((min(x_a, x_b), a, gh), (max(x_a, x_b), b, H), wall, nobottom=True)
    facade_pilasters(x0, x1, y0, True, 1)
    facade_pilasters(x0, x1, y1, True, -1)
    facade_pilasters(y0, y1, x0, False, 1)
    facade_pilasters(y0, y1, x1, False, -1)
    if storefront:
        for f in front:
            if f in ("S", "N"):
                yy = y0 if f == "S" else y1 - 0.5
                n = max(1, int(round(W / 5.0)))
                for i in range(n + 1):
                    cx = x0 + i * W / n
                    mb.box((max(x0, cx - 0.25), yy, 0), (min(x1, cx + 0.25), yy + 0.5, gh - 0.6), wall, nobottom=True)
                for i in range(n):
                    if rng.random() < 0.55:
                        cx0 = x0 + i * W / n + 0.5
                        cx1 = x0 + (i + 1) * W / n - 0.5
                        col = rng.choice(["vermelho_seguranca", "verde_escuro", "laranja_seguranca", "azul_escuro", "branco"])
                        s = -1 if f == "S" else 1
                        yb = y0 if f == "S" else y1
                        mb.hull([(cx0, yb, gh - 0.8), (cx1, yb, gh - 0.8), (cx0, yb, gh - 0.95), (cx1, yb, gh - 0.95),
                                 (cx0, yb + s * 1.3, gh - 1.55), (cx1, yb + s * 1.3, gh - 1.55)], col)
            else:
                xx = x0 if f == "W" else x1 - 0.5
                n = max(1, int(round(Dp / 5.0)))
                for i in range(n + 1):
                    cy = y0 + i * Dp / n
                    mb.box((xx, max(y0, cy - 0.25), 0), (xx + 0.5, min(y1, cy + 0.25), gh - 0.6), wall, nobottom=True)
                for i in range(n):
                    if rng.random() < 0.55:
                        cy0 = y0 + i * Dp / n + 0.5
                        cy1 = y0 + (i + 1) * Dp / n - 0.5
                        col = rng.choice(["vermelho_seguranca", "verde_escuro", "laranja_seguranca", "azul_escuro", "branco"])
                        s = -1 if f == "W" else 1
                        xb = x0 if f == "W" else x1
                        mb.hull([(xb, cy0, gh - 0.8), (xb, cy1, gh - 0.8), (xb, cy0, gh - 0.95), (xb, cy1, gh - 0.95),
                                 (xb + s * 1.3, cy0, gh - 1.55), (xb + s * 1.3, cy1, gh - 1.55)], col)
    else:
        for f in front or ("S",):
            if f in ("S", "N"):
                yb = y0 - 0.02 if f == "S" else y1 - 0.12
                cx = (x0 + x1) / 2
                mb.box((cx - 1.2, yb, 0), (cx + 1.2, yb + 0.14, 2.6), "g:vidro_escuro", nobottom=True)
            else:
                xb = x0 - 0.02 if f == "W" else x1 - 0.12
                cy = (y0 + y1) / 2
                mb.box((xb, cy - 1.2, 0), (xb + 0.14, cy + 1.2, 2.6), "g:vidro_escuro", nobottom=True)
    if balconies:
        for f in front:
            for k in range(1, floors):
                zf = gh + k * fh - sh * 0.5
                if f in ("S", "N"):
                    n = max(1, int(round(W / (bay * 2))))
                    for i in range(n):
                        ca = x0 + (i + 0.5) * W / n
                        s = -1 if f == "S" else 1
                        yb = y0 if f == "S" else y1
                        mb.box((ca - 1.3, yb, zf), (ca + 1.3, yb + s * 1.1, zf + 0.14), wall)
                        mb.box((ca - 1.3, yb + s * 1.0, zf + 0.14), (ca + 1.3, yb + s * 1.1, zf + 1.05), wall, nobottom=True)
                else:
                    n = max(1, int(round(Dp / (bay * 2))))
                    for i in range(n):
                        ca = y0 + (i + 0.5) * Dp / n
                        s = -1 if f == "W" else 1
                        xb = x0 if f == "W" else x1
                        mb.box((xb, ca - 1.3, zf), (xb + s * 1.1, ca + 1.3, zf + 0.14), wall)
                        mb.box((xb + s * 1.0, ca - 1.3, zf + 0.14), (xb + s * 1.1, ca + 1.3, zf + 1.05), wall, nobottom=True)
    mb.box((x0 + 0.25, y0 + 0.25, H - 0.1), (x1 - 0.25, y1 - 0.25, H + 0.12), roof, nobottom=True)
    mb.ring_box(x0, y0, x1, y1, H - sh * 0.5, H + 0.9, 0.3, wall)
    if crown:
        mb.ring_box(x0 + 0.8, y0 + 0.8, x1 - 0.8, y1 - 0.8, H + 0.9, H + 3.2, 0.25, crown)
    if simple:
        return H
    pw_, pd_ = min(6.0, W * 0.3), min(5.0, Dp * 0.3)
    cx, cy = x0 + W * rng.uniform(0.3, 0.6), y0 + Dp * rng.uniform(0.3, 0.6)
    mb.box((cx - pw_ / 2, cy - pd_ / 2, H + 0.12), (cx + pw_ / 2, cy + pd_ / 2, H + 3.2), wall, top=roof, nobottom=True)
    if tanks:
        tx, ty = cx + pw_ / 2 + 1.6, cy
        if tx + 1.2 < x1 - 0.5:
            for k in range(2):
                ox = tx + k * 2.3
                if ox + 1.0 < x1 - 0.4:
                    mb.cyl((ox, ty, H + 0.12), (ox, ty, H + 1.5), 0.9, "lona_azul", n=10, cap="azul_escuro")
    if ac:
        nx_ = max(1, int((W - 3.0) / 2.6))
        rows = [y0 + 1.5, y1 - 2.3]
        for ry in rows:
            for i in range(nx_):
                if rng.random() < 0.6:
                    ax = x0 + 1.6 + i * 2.6
                    if abs(ax - cx) < pw_ / 2 + 1.2 and abs(ry - cy) < pd_ / 2 + 1.2:
                        continue
                    mb.box((ax, ry, H + 0.12), (ax + 1.1, ry + 0.8, H + 0.95), "condensadora", top="cinza", nobottom=True)
                    mb.cyl((ax + 0.55, ry + 0.4, H + 0.95), (ax + 0.55, ry + 0.4, H + 0.99), 0.3, "cinza_escuro", n=8, smooth=False)
    return H


def build():
    C_P = K.coll("01_Cidade_Predios")
    C_D = K.coll("01b_Cidade_Distante")
    K.clear_coll(C_P)
    K.clear_coll(C_D)
    rng = random.Random(2026)
    DET = [
        ("Vizinho_N1_Escritorio", -39, 33, -13, 58, 7, "grade", "predio_cinza", ("S",), False, False, None),
        ("Vizinho_N2_Torre_Vidro", -8, 36, 22, 73, 11, "grade_fina", "predio_cinza_claro", ("S",), False, False, "predio_cinza_claro"),
        ("Vizinho_N3_Residencial_Rosa", 26, 33, 39.5, 72, 5, "janelas", "predio_rosa", ("S", "E"), False, True, None),
        ("Vizinho_N4_Comercial", -39, 62, -13, 73, 3, "faixas", "predio_creme", ("N",), True, False, None),
        ("Leste_E1_Residencial_Lavanda", 58, -30, 88, -6, 6, "janelas", "predio_lavanda", ("W", "S"), False, True, None),
        ("Leste_E2_Comercial_Creme", 58, 0, 82, 36, 4, "faixas", "predio_creme", ("W",), True, False, None),
        ("Leste_E3_Escritorio", 92, -30, 138, 16, 9, "grade", "predio_cinza", ("S",), False, False, None),
        ("Leste_E4_Torre_Vidro", 62, 44, 106, 74, 12, "grade_fina", "predio_branco", ("W",), False, False, "predio_branco"),
        ("Leste_E5_Residencial_Teal", 112, 24, 138, 74, 7, "janelas", "predio_teal", ("W",), False, True, None),
        ("Oeste_W1_Escritorio_Grade", -92, -30, -58, 2, 8, "grade", "predio_cinza_claro", ("E", "S"), True, False, None),
        ("Oeste_W2_Residencial_Rosa", -88, 8, -58, 40, 5, "janelas", "predio_rosa", ("E",), False, True, None),
        ("Oeste_W3_Escritorio_Escuro", -138, -30, -98, 16, 12, "grade", "predio_cinza_escuro", ("S",), False, False, None),
        ("Oeste_W4_Residencial_Creme", -138, 22, -96, 74, 6, "janelas", "predio_creme", ("E",), False, True, None),
        ("Oeste_W5_Torre_Vidro", -90, 46, -58, 74, 14, "grade_fina", "predio_cinza_claro", ("E",), False, False, "predio_cinza"),
        ("Sul_S1_Lojas", -40, -76, -8, -52, 3, "faixas", "predio_branco", ("N",), True, False, None),
        ("Sul_S2_Residencial", -2, -74, 40, -52, 4, "janelas", "predio_creme", ("N",), True, True, None),
        ("Sul_S3_Escritorio", -40, -122, 40, -84, 6, "grade", "predio_cinza", ("N",), False, False, None),
        ("SO_Supermercado", -100, -84, -70, -56, 2, "faixas", "predio_branco", ("N", "W"), True, False, None),
        ("SO_Residencial", -96, -122, -58, -94, 4, "janelas", "predio_rosa", ("N",), False, True, None),
        ("SE_Escritorio", 58, -80, 100, -52, 5, "grade", "predio_cinza_claro", ("N", "W"), True, False, None),
        ("SE_Residencial_Lavanda", 106, -122, 138, -52, 8, "janelas", "predio_lavanda", ("W",), False, True, None),
        ("SE_Comercial_Teal", 58, -122, 100, -88, 3, "faixas", "predio_teal", ("N",), True, False, None),
        ("NO_Torre_Vidro", -138, 92, -100, 132, 18, "grade_fina", "predio_cinza_claro", ("S",), False, False, "predio_cinza"),
        ("NO_Escritorio", -92, 92, -58, 122, 10, "grade", "predio_cinza", ("S",), False, False, None),
        ("NO_Residencial", -138, 140, -58, 172, 8, "janelas", "predio_creme", ("S",), False, True, None),
        ("Norte_Torre_Vidro_Alta", -40, 92, 0, 130, 20, "grade_fina", "predio_branco", ("S",), False, False, "predio_cinza_claro"),
        ("Norte_Escritorio", 8, 92, 40, 126, 14, "grade", "predio_cinza_escuro", ("S",), False, False, None),
        ("Norte_Residencial", -40, 138, 40, 172, 9, "janelas", "predio_rosa", ("S",), False, True, None),
        ("NE_Torre_Mais_Alta", 58, 92, 96, 140, 22, "grade_fina", "predio_cinza_claro", ("S", "W"), False, False, "predio_cinza"),
        ("NE_Escritorio", 104, 92, 138, 130, 12, "grade", "predio_cinza", ("S",), False, False, None),
        ("NE_Residencial", 104, 138, 138, 172, 8, "janelas", "predio_teal", ("S",), False, True, None),
        ("NE_Comercial", 58, 146, 96, 172, 6, "faixas", "predio_creme", ("S",), True, False, None),
    ]
    alturas = {}
    for (nome, x0, y0, x1, y1, fl, stl, cor, fr, loja, var, crown) in DET:
        mb = MB()
        H = predio(mb, float(x0), float(y0), float(x1), float(y1), fl, stl, cor, rng, front=fr, storefront=loja,
                   balconies=var, crown=crown)
        K.finish(mb, "Predio_" + nome, C_P, props={"categoria": "cidade_predio", "andares": fl, "altura_m": round(H, 1)})
        alturas[nome] = round(H, 1)
    pk = MB()
    pk.box((-138, -122, 0.0), (-104, -52, 0.03), "asfalto", nobottom=True)
    for row_y, s in ((-118.0, 1), (-66.0, -1)):
        for i in range(12):
            x = -136.0 + i * 2.6
            pk.box((x, row_y, 0.03), (x + 0.1, row_y + s * 5.0, 0.04), "faixa_branca", nobottom=True)
    for i in range(12):
        x = -136.0 + i * 2.6
        pk.box((x, -96.0, 0.03), (x + 0.1, -91.0, 0.04), "faixa_branca", nobottom=True)
        pk.box((x, -84.0, 0.03), (x + 0.1, -79.0, 0.04), "faixa_branca", nobottom=True)
    K.finish(pk, "Estacionamento_SO", C_P, props={"categoria": "cidade_piso"})
    pr = MB()
    pr.box((86, 20, 0.0), (108, 40, 0.12), "grama", sides="meio_fio", nobottom=True)
    pr.box((94, 20, 0.0), (100, 40, 0.14), "calcada", nobottom=True)
    K.finish(pr, "Praca_Leste", C_P, props={"categoria": "cidade_piso"})
    xs = [(-240.0, -152.0), (-142.0, -54.0), (-44.0, 44.0), (54.0, 142.0), (152.0, 240.0)]
    ys = [(-220.0, -136.0), (-126.0, -48.0), (-34.0, 78.0), (88.0, 176.0), (186.0, 270.0)]
    cores = ["predio_cinza", "predio_cinza_claro", "predio_creme", "predio_rosa", "predio_lavanda", "predio_teal", "predio_branco", "predio_cinza_escuro"]
    n_far = 0
    for ix, (xa, xb) in enumerate(xs):
        for iy, (ya, yb) in enumerate(ys):
            if 1 <= ix <= 3 and 1 <= iy <= 3:
                continue
            mb = MB()
            ax0, ay0, ax1, ay1 = xa + 4, ya + 4, xb - 4, yb - 4
            mx, my = (ax0 + ax1) / 2, (ay0 + ay1) / 2
            lots = [(ax0, ay0, mx - 3, my - 3), (mx + 3, ay0, ax1, my - 3), (ax0, my + 3, mx - 3, ay1), (mx + 3, my + 3, ax1, ay1)]
            for (lx0, ly0, lx1, ly1) in lots:
                if rng.random() < 0.12:
                    continue
                far = max(abs(mx), abs(my))
                fl = rng.randint(4, 10) + (rng.randint(0, 10) if far > 150 else 0)
                stl = rng.choice(["grade", "faixas", "janelas", "grade_fina"])
                predio(mb, lx0, ly0, lx1, ly1, fl, stl, rng.choice(cores), rng, simple=True)
                n_far += 1
            K.finish(mb, "Cidade_Distante_Quadra_%d_%d" % (ix, iy), C_D, props={"categoria": "cidade_distante"})
    return {"detalhados": len(DET), "distantes": n_far, "alturas": alturas}
