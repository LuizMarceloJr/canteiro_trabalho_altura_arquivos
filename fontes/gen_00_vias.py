# gen_00_vias.py - asfalto, calcadas, meio-fio, sinalizacao horizontal e bueiros
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB


def intervals(lo, hi, roads):
    out, cur = [], lo
    for c, w in sorted(roads):
        a, b = c - w / 2, c + w / 2
        if a > cur:
            out.append((cur, a))
        cur = b
    if hi > cur:
        out.append((cur, hi))
    return out


def free_runs(a0, a1, zones):
    runs, cur = [], a0
    for za, zb in sorted(zones):
        if zb <= cur or za >= a1:
            continue
        if za > cur:
            runs.append((cur, za))
        cur = max(cur, zb)
    if cur < a1:
        runs.append((cur, a1))
    return runs


def dashed(a0, a1, on=3.0, off=5.0):
    out, s = [], a0 + off / 2
    while s + on <= a1:
        out.append((s, s + on))
        s += on + off
    return out


def build():
    C = K.coll("00_Terreno_Vias")
    K.clear_coll(C)
    CX0, CY0, CX1, CY1 = L.CITY
    LX0, LY0, LX1, LY1 = L.LOTE
    ZR = L.ZR
    ZM = ZR + 0.02
    mb = MB()
    E = 1500.0
    for (a, b, c, d) in ((-E, -E, E, CY0), (-E, CY1, E, E), (-E, CY0, CX0, CY1), (CX1, CY0, E, CY1)):
        mb.poly([(a, b, -0.16), (c, b, -0.16), (c, d, -0.16), (a, d, -0.16)], "calcada_escura")
    K.finish(mb, "Chao_Distante", C)
    mb = MB()
    for (a, b, c, d) in ((CX0, CY0, CX1, LY0), (CX0, LY1, CX1, CY1), (CX0, LY0, LX0, LY1), (LX1, LY0, CX1, LY1)):
        mb.poly([(a, b, ZR), (c, b, ZR), (c, d, ZR), (a, d, ZR)], "asfalto")
    K.finish(mb, "Vias_Asfalto", C)
    XS = intervals(CX0, CX1, L.RUAS_NS)
    YS = intervals(CY0, CY1, L.RUAS_LO)
    mb, mbc = MB(), MB()
    for (xa, xb) in XS:
        for (ya, yb) in YS:
            if (xa, ya, xb, yb) == L.QUADRA_OBRA:
                mb.box((xa, ya, ZR), (xb, ya + 4, 0), "calcada", sides="meio_fio", nobottom=True)
                mb.box((xa, yb - 4, ZR), (xb, yb, 0), "calcada", sides="meio_fio", nobottom=True)
                mb.box((xa, ya + 4, ZR), (xa + 4, yb - 4, 0), "calcada", sides="meio_fio", nobottom=True)
                mb.box((xb - 4, ya + 4, ZR), (xb, yb - 4, 0), "calcada", sides="meio_fio", nobottom=True)
                mb.box((-40, 30, ZR), (40, 74, 0), "calcada_escura", nobottom=True)
            else:
                mb.box((xa, ya, ZR), (xb, yb, 0), "calcada", sides="meio_fio", nobottom=True)
            mbc.ring_box(xa, ya, xb, yb, 0.0, 0.02, 0.25, "meio_fio", nobottom=True)
    K.finish(mb, "Calcadas_Quadras", C)
    K.finish(mbc, "Calcadas_Meio_Fio", C)

    def mark(m, x0, y0, x1, y1, c="faixa_branca"):
        m.poly([(x0, y0, ZM), (x1, y0, ZM), (x1, y1, ZM), (x0, y1, ZM)], c)
    mk = MB()
    LW = 0.12
    for (yc, h) in L.RUAS_LO:
        zones = [(xc - w / 2 - 7.0, xc + w / 2 + 7.0) for (xc, w) in L.RUAS_NS]
        for (ra, rb) in free_runs(CX0, CX1, zones):
            if h >= 14:
                mark(mk, ra, yc + 0.06, rb, yc + 0.06 + LW, "faixa_amarela")
                mark(mk, ra, yc - 0.06 - LW, rb, yc - 0.06, "faixa_amarela")
                for off in (-3.5, 3.5):
                    for (da, db) in dashed(ra, rb):
                        mark(mk, da, yc + off - LW / 2, db, yc + off + LW / 2)
                mark(mk, ra, yc - h / 2 + 0.35, rb, yc - h / 2 + 0.35 + LW)
                mark(mk, ra, yc + h / 2 - 0.35 - LW, rb, yc + h / 2 - 0.35)
            else:
                for (da, db) in dashed(ra, rb, 3.0, 4.0):
                    mark(mk, da, yc - LW / 2, db, yc + LW / 2, "faixa_amarela")
    for (xc, w) in L.RUAS_NS:
        zones = [(yc - h / 2 - 7.0, yc + h / 2 + 7.0) for (yc, h) in L.RUAS_LO]
        for (ra, rb) in free_runs(CY0, CY1, zones):
            for (da, db) in dashed(ra, rb, 3.0, 4.0):
                mark(mk, xc - LW / 2, da, xc + LW / 2, db, "faixa_amarela")
    SW, SP, CW = 0.45, 0.45, 4.0
    for (xc, w) in L.RUAS_NS:
        for (yc, h) in L.RUAS_LO:
            for sgn in (1, -1):
                ya = yc + sgn * (h / 2 + 1.0)
                yb = ya + sgn * CW
                x = xc - w / 2 + 0.4
                while x + SW <= xc + w / 2 - 0.4:
                    mark(mk, x, min(ya, yb), x + SW, max(ya, yb))
                    x += SW + SP
                ys = yb + sgn * 1.2
                if sgn > 0:
                    mark(mk, xc - w / 2 + 0.4, ys, xc - 0.2, ys + 0.4)
                else:
                    mark(mk, xc + 0.2, ys - 0.4, xc + w / 2 - 0.4, ys)
            for sgn in (1, -1):
                xa = xc + sgn * (w / 2 + 1.0)
                xb = xa + sgn * CW
                y = yc - h / 2 + 0.4
                while y + SW <= yc + h / 2 - 0.4:
                    mark(mk, min(xa, xb), y, max(xa, xb), y + SW)
                    y += SW + SP
                xs = xb + sgn * 1.2
                if sgn > 0:
                    mark(mk, xs, yc + 0.2, xs + 0.4, yc + h / 2 - 0.4)
                else:
                    mark(mk, xs - 0.4, yc - h / 2 + 0.4, xs, yc - 0.2)
    K.finish(mk, "Vias_Sinalizacao_Horizontal", C)
    mh = MB()
    for (x, y) in [(-49, -20), (-49, 20), (49, -10), (49, 35), (-20, -41), (15, -44.5), (35, -37.5), (-30, -44.5), (0, 83), (90, -41), (-95, -41)]:
        mh.cyl((x, y, ZR), (x, y, ZR + 0.025), 0.35, "grafite", n=10, smooth=False)
    for x in range(-40, 41, 16):
        mh.box((x - 0.5, -34.3, ZR), (x + 0.5, -34.0, ZR + 0.03), "preto_suave")
        mh.box((x - 0.5, -48.0, ZR), (x + 0.5, -47.7, ZR + 0.03), "preto_suave")
    K.finish(mh, "Vias_Bueiros", C)
    return {"objetos": len(C.objects)}
