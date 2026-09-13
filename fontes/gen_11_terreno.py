# gen_11_terreno.py - terreno do canteiro com cava (geometria explicita, taludes facetados)
import bpy, bmesh, sys, math, random
from mathutils import Vector
K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB

OUTLINE = [(-10.0, -22.0), (10.0, -22.0), (10.0, -19.4375), (23.0, -17.0), (23.0, -12.0), (10.0, -9.5625), (10.0, -6.0), (-10.0, -6.0)]


def pip(x, y, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside


def facet_face(mb, pts, color, rng, step=1.0, amp=0.09):
    """subdivide um quad/triangulo planar e desloca vertices internos na normal (visual low-poly)."""
    P = [Vector(p) for p in pts]
    nrm = (P[1] - P[0]).cross(P[2] - P[0]).normalized()
    if len(P) == 4:
        n = max(1, int(round(max((P[1] - P[0]).length, (P[2] - P[3]).length) / step)))
        m = max(1, int(round(max((P[3] - P[0]).length, (P[2] - P[1]).length) / step)))
        verts = []
        for j in range(m + 1):
            v = j / m
            for i in range(n + 1):
                u = i / n
                p = (P[0] * (1 - u) + P[1] * u) * (1 - v) + (P[3] * (1 - u) + P[2] * u) * v
                if 0 < i < n and 0 < j < m:
                    p = p + nrm * rng.uniform(-amp, amp)
                verts.append(tuple(p))
        faces = []
        for j in range(m):
            for i in range(n):
                a = j * (n + 1) + i
                if (i + j) % 2 == 0:
                    faces += [(a, a + 1, a + n + 2), (a, a + n + 2, a + n + 1)]
                else:
                    faces += [(a, a + 1, a + n + 1), (a + 1, a + n + 2, a + n + 1)]
        mb.part(verts, faces, color)
    else:
        n = max(1, int(round(max((P[1] - P[0]).length, (P[2] - P[1]).length, (P[0] - P[2]).length) / step)))
        idx = {}
        verts = []
        for i in range(n + 1):
            for j in range(n + 1 - i):
                k = n - i - j
                p = (P[0] * i + P[1] * j + P[2] * k) / n
                if i > 0 and j > 0 and k > 0:
                    p = p + nrm * rng.uniform(-amp, amp)
                idx[(i, j)] = len(verts)
                verts.append(tuple(p))
        faces = []
        for i in range(n):
            for j in range(n - i):
                faces.append((idx[(i, j)], idx[(i + 1, j)], idx[(i, j + 1)]))
                if i + j < n - 1:
                    faces.append((idx[(i + 1, j)], idx[(i + 1, j + 1)], idx[(i, j + 1)]))
        # garante normal para cima
        a, b, c = Vector(verts[faces[0][0]]), Vector(verts[faces[0][1]]), Vector(verts[faces[0][2]])
        if (b - a).cross(c - a).z < 0:
            faces = [tuple(reversed(f)) for f in faces]
        mb.part(verts, faces, color)


def build():
    C = K.coll("11_Canteiro_Terraplenagem")
    for nm in ("Canteiro_Terreno_Cava", "Canteiro_Terreno", "Canteiro_Cava_Escavacao"):
        o = bpy.data.objects.get(nm)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    K.purge_meshes()
    rng = random.Random(21)
    LX0, LY0, LX1, LY1 = L.LOTE
    TRILHAS = [(29.0, -30.0, 37.0, -5.0), (21.0, -17.0, 37.0, -12.0), (-22.0, -5.0, 38.0, 1.0), (-22.0, 1.0, -16.0, 16.0)]
    PISOS = [((5.4, 3.4, 32.6, 22.6), "concreto"), ((-31.6, -14.6, -14.4, -1.4), "concreto"), (tuple(L.ELEVADOR), "concreto")]

    # ---- chao plano com recorte da cava
    bm = bmesh.new()
    step = 2.0
    nx, ny = int((LX1 - LX0) / step), int((LY1 - LY0) / step)
    vs = [[bm.verts.new((LX0 + i * step, LY0 + j * step, 0.0)) for i in range(nx + 1)] for j in range(ny + 1)]
    for j in range(ny):
        for i in range(nx):
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    lines = []
    for a, b in zip(OUTLINE, OUTLINE[1:] + OUTLINE[:1]):
        lines.append((a, b))
    for r in TRILHAS + [p[0] for p in PISOS]:
        x0, y0, x1, y1 = r
        lines += [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x0, y1), (x1, y1)), ((x0, y0), (x0, y1))]
    for (a, b) in lines:
        dx, dy = b[0] - a[0], b[1] - a[1]
        nrm = Vector((-dy, dx, 0.0)).normalized()
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-5, plane_co=(a[0], a[1], 0.0), plane_no=nrm, clear_outer=False, clear_inner=False)
    kill = []
    for f in bm.faces:
        c = f.calc_center_median()
        if pip(c.x, c.y, OUTLINE):
            kill.append(f)
    bmesh.ops.delete(bm, geom=kill, context='FACES_ONLY')
    loose = [v for v in bm.verts if not v.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bm.verts.index_update()
    verts = [tuple(v.co) for v in bm.verts]
    faces, cols = [], []
    for f in bm.faces:
        c = f.calc_center_median()
        col = "terra"
        for r in TRILHAS:
            if r[0] <= c.x <= r[2] and r[1] <= c.y <= r[3]:
                col = "terra_escura"
        for (r, cc) in PISOS:
            if r[0] <= c.x <= r[2] and r[1] <= c.y <= r[3]:
                col = cc
        faces.append([v.index for v in f.verts])
        cols.append(col)
    bm.free()
    mb = MB()
    mb.part(verts, faces, cols)
    K.finish(mb, "Canteiro_Terreno", C, props={"categoria": "terreno"})

    # ---- cava (fundo, taludes 1:1, rampa com inclinacao ~19%)
    D = L.CAVA_PROF
    mb = MB()
    zb = -D
    facet_face(mb, [(-7, -19, zb), (7, -19, zb), (7, -9, zb), (-7, -9, zb)], "terra_escura", rng, step=2.0, amp=0.05)
    facet_face(mb, [(-7, -9, zb), (7, -9, zb), (10, -6, 0), (-10, -6, 0)], "talude", rng)
    facet_face(mb, [(-10, -22, 0), (10, -22, 0), (7, -19, zb), (-7, -19, zb)], "talude", rng)
    facet_face(mb, [(-10, -22, 0), (-7, -19, zb), (-7, -9, zb), (-10, -6, 0)], "talude", rng)
    facet_face(mb, [(7, -19, zb), (10, -22, 0), (10, -19.4375, 0), (7, -17, zb)], "talude", rng)
    facet_face(mb, [(7, -12, zb), (10, -9.5625, 0), (10, -6, 0), (7, -9, zb)], "talude", rng)
    facet_face(mb, [(7, -17, zb), (23, -17, 0), (23, -12, 0), (7, -12, zb)], "terra_escura", rng, step=1.5, amp=0.03)
    facet_face(mb, [(7, -17, zb), (10, -19.4375, 0), (23, -17, 0)], "talude", rng)
    facet_face(mb, [(7, -12, zb), (23, -12, 0), (10, -9.5625, 0)], "talude", rng)
    o = K.finish(mb, "Canteiro_Cava_Escavacao", C, props={"categoria": "terreno", "profundidade_m": D, "talude": "1:1 (45 graus)",
                                                         "rampa_inclinacao_pct": round(100 * D / 16.0, 1), "nr_ref": "NR-18 18.6 escavacoes"})
    # normais: garantir que apontam para cima/dentro da cava
    me = o.data
    import numpy as np
    flip = []
    for p in me.polygons:
        if p.normal.z < 0:
            flip.append(p.index)
    if flip:
        bm2 = bmesh.new()
        bm2.from_mesh(me)
        bm2.faces.ensure_lookup_table()
        bmesh.ops.reverse_faces(bm2, faces=[bm2.faces[i] for i in flip])
        bm2.to_mesh(me)
        bm2.free()
    return {"invertidas": len(flip)}
