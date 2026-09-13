# -*- coding: utf-8 -*-
# sitekit.py - biblioteca de modelagem low-poly do cenario
# "Canteiro de Obras - Trabalho em Altura" (TRAINING SIM)
# Convencoes: 1 unidade = 1 m | X = Leste, Y = Norte, Z = Cima.
# Cores: textura unica T_Paleta (16 x 16 celulas). Cada face aponta sua UV
# para o centro da celula da cor -> 1 material = 1 draw call no Three.js.
import bpy, bmesh, math, random
from mathutils import Vector, Matrix, Euler
from contextlib import contextmanager

GRID = 16
CELL = 8
ROOT = "CANTEIRO_OBRA"

PAL = [
    ("branco", "F4F4F1"), ("branco_gelo", "E4E5E1"), ("cinza_claro", "CBCDD0"), ("cinza", "A8AAAE"),
    ("cinza_medio", "8D9197"), ("cinza_escuro", "6D7076"), ("grafite", "4B4E53"), ("preto_suave", "2C2D30"),
    ("preto", "1B1B1D"), ("aco", "B5BBC2"), ("asfalto", "54575D"), ("asfalto_escuro", "45484D"),
    ("faixa_branca", "EFEFEA"), ("faixa_amarela", "F2C230"), ("calcada", "B1B3B6"), ("calcada_escura", "9C9FA3"),
    ("meio_fio", "CACCCE"), ("grama", "84C255"), ("terra", "E4B78E"), ("terra_escura", "D2A077"),
    ("areia", "EBCB98"), ("brita", "A19E99"), ("talude", "D9A67B"), ("concreto_claro", "DAD6D0"),
    ("concreto", "C4BFB7"), ("concreto_escuro", "A39E96"), ("concreto_fresco", "8E8B87"), ("reboco", "E6DACA"),
    ("bloco_ceramico", "C2653F"), ("tijolo", "B0502E"), ("argamassa", "CFC6B8"), ("pintura_fachada", "EFE9DF"),
    ("madeira_clara", "D6B07E"), ("madeira", "BF9262"), ("madeira_escura", "93693F"), ("compensado", "DDBE8E"),
    ("forma_resinada", "A65A2A"), ("pallet", "C29667"), ("papelao", "CBA376"), ("saco_cimento", "EEEAE0"),
    ("saco_faixa", "5B86C8"), ("big_bag", "F1EFE7"), ("filme_plastico", "D8DEE3"), ("vergalhao", "8A5A3C"),
    ("ferrugem", "A5552C"), ("tubo_pvc", "E9E6DD"), ("tubo_concreto", "C9C5BE"), ("lona_azul", "2F6FC8"),
    ("amarelo_maquina", "F3B61C"), ("amarelo_escuro", "D39A12"), ("laranja_seguranca", "F2791E"), ("laranja_escuro", "C95F17"),
    ("vermelho_seguranca", "D8322B"), ("vermelho_escuro", "A6261F"), ("azul_andaime", "2E56C8"), ("azul_container", "2F72DA"),
    ("azul_claro", "5E97E8"), ("azul_escuro", "234A9A"), ("verde_seguranca", "2E9E4F"), ("verde_escuro", "2F7A3C"),
    ("amarelo_linha_vida", "F6C51A"), ("zebrado_preto", "202020"), ("branco_sinal", "FAFAF7"), ("cromado", "D5D9DD"),
    ("verde_betoneira", "2E9E5B"), ("laranja_caminhao", "E96B34"), ("vermelho_caminhao", "D9443A"), ("verde_caminhao", "82B93C"),
    ("pneu", "27282A"), ("aro", "9AA0A6"), ("farol", "FFF3C4"), ("lanterna", "E0302A"),
    ("vidro_veiculo", "3D4B5D"), ("carro_laranja", "E8834A"), ("carro_teal", "3AA6A0"), ("carro_verde", "4F9E6E"),
    ("carro_branco", "EFEFEB"), ("carro_vermelho", "D24B4B"), ("carro_azul", "4A78C2"), ("carro_bege", "E3CFA6"),
    ("carro_prata", "BCC1C7"), ("carro_preto", "36383C"), ("carro_amarelo", "F0C43C"), ("predio_cinza", "ABADB1"),
    ("predio_cinza_claro", "D0D2D5"), ("predio_cinza_escuro", "7D8085"), ("predio_lavanda", "9E9ACE"), ("predio_rosa", "DAA9A2"),
    ("predio_creme", "E7DDC9"), ("predio_teal", "88ADAA"), ("predio_branco", "EDEDEB"), ("vidro_predio", "5F738B"),
    ("vidro_claro", "92A8BD"), ("vidro_escuro", "44526A"), ("telhado", "8F9296"), ("condensadora", "E2E3E4"),
    ("folha_clara", "7BC950"), ("folha", "5AAF40"), ("folha_escura", "408F36"), ("tronco", "7B5331"),
    ("poste_verde", "3E7C59"), ("lampada", "FFE7A8"), ("orelhao_azul", "2F80C2"), ("orelhao_laranja", "F08B25"),
    ("lixeira_azul", "2D70C1"), ("lixeira_amarela", "F2C31C"), ("lixeira_verde", "40A14B"), ("lixeira_vermelha", "D43B33"),
    ("tela_verde", "3F8F5B"), ("tela_azul", "3D70B9"), ("rede_preta", "2B2B2B"), ("cobre", "B87534"),
    ("agua", "70A9DD"), ("vidro_obra", "58677C"), ("aviso_luz", "FF3B24"), ("sinal_verde", "3BD16F"),
    ("sinal_amarelo", "FFC933"), ("sinal_vermelho", "FF4436"), ("pele", "E0B08A"), ("uniforme_azul", "2F5DA8"),
    ("uniforme_laranja", "F07F2A"), ("capacete_branco", "F4F4F0"), ("capacete_amarelo", "F6C21E"), ("capacete_azul", "2B6CD0"),
    ("borracha", "3A3B3E"), ("placa_obra", "1F4E8C"), ("ciclovia", "C8473D"), ("concreto_pilar", "CFCAC2"),
    # ---- cores do treinamento (personagens, EPI, estados) - acrescentadas no fim para nao mudar indices
    ("pele_clara", "EBC3A0"), ("pele_morena", "C68E64"), ("pele_escura", "8C5A3C"), ("cabelo_escuro", "2E2520"),
    ("uniforme_cinza", "7E8791"), ("uniforme_verde", "4E7D5B"), ("jeans", "4A6A96"), ("jeans_escuro", "2E4466"),
    ("colete_limao", "C8E03A"), ("refletivo", "E3E6E8"), ("luva_cinza", "8F9398"), ("luva_amarela", "E8C24A"),
    ("bota_couro", "4A3526"), ("capacete_vermelho", "D23A2E"), ("capacete_verde", "3FA35A"), ("vermelho_resgate", "C92A22"),
    ("fita_cinturao_azul", "2C58B8"), ("fita_desgastada", "CDBE9E"), ("corte_fita", "5A1A12"), ("tela_tablet", "1B3F6E"),
    ("tela_tablet_brilho", "4F8FD8"), ("preto_radio", "232427"), ("verde_led", "38E070"), ("amarelo_ancoragem", "FFD21A"),
    ("marca_rachadura", "34332F"), ("madeira_molhada", "8A6A48"), ("concreto_molhado", "8A867F"), ("sujeira", "7A6A55"),
    ("lona_verde", "3C7A4A"), ("laranja_neon", "FF6A1F"), ("cinza_chumbo", "5A5D62"), ("branco_fosco", "D9DAD6"),
]
PI = {n: i for i, (n, h) in enumerate(PAL)}

# slots de material (indice * 256 + cor)
SLOTS = ["M_Paleta", "M_Paleta_Vidro", "M_Paleta_Emissivo", "M_Placas",
         "M_Tela_GcR", "M_Tela_Fachada", "M_Rede_Seguranca", "M_Vidro_Transparente", "M_Treinamento"]
PREFIX = {"g": 1, "e": 2, "t": 7}
S_PLACAS, S_TELA_GCR, S_TELA_FACHADA, S_REDE = 3, 4, 5, 6
S_TREINO = 8   # atlas T_Treinamento (tablet, placas do roteiro)


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def cid(c):
    if isinstance(c, int):
        return c
    slot = 0
    if len(c) > 2 and c[1] == ':':
        slot = PREFIX[c[0]]
        c = c[2:]
    return slot * 256 + PI[c]


def T(loc=(0, 0, 0), rz=0.0, rx=0.0, ry=0.0):
    return Matrix.Translation(Vector(loc)) @ Euler(
        (math.radians(rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix().to_4x4()


# ------------------------------------------------------------------ materiais
def _inp(node, *names):
    for n in names:
        if n in node.inputs:
            return node.inputs[n]
    return None


def _reset_nodes(mat):
    try:
        mat.use_nodes = True
    except Exception:
        pass
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    out.location = (500, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (150, 0)
    nt.links.new(bsdf.outputs[0], out.inputs['Surface'])
    return nt, bsdf


def _new_image(name, w, h, alpha):
    old = bpy.data.images.get(name)
    if old is not None:
        bpy.data.images.remove(old)
    img = bpy.data.images.new(name, w, h, alpha=alpha)
    return img


def _fill_image(img, arr):
    img.pixels.foreach_set(arr.ravel().astype('float32'))
    img.update()
    try:
        img.pack()
    except Exception:
        pass
    img.use_fake_user = True


def build_palette_image():
    import numpy as np
    size = GRID * CELL
    img = _new_image("T_Paleta", size, size, False)
    arr = np.ones((size, size, 4), dtype=np.float32)
    arr[..., :3] = 1.0
    for i, (n, h) in enumerate(PAL):
        r, g, b = hex_rgb(h)
        cx, cy = i % GRID, i // GRID
        y0 = size - (cy + 1) * CELL
        x0 = cx * CELL
        arr[y0:y0 + CELL, x0:x0 + CELL, 0] = r
        arr[y0:y0 + CELL, x0:x0 + CELL, 1] = g
        arr[y0:y0 + CELL, x0:x0 + CELL, 2] = b
    _fill_image(img, arr)
    return img


def build_mesh_image(name, hexcol, size=32, step=8, line=2, diamond=False, bg_alpha=0.0, line_alpha=1.0, shade=1.0):
    import numpy as np
    img = _new_image(name, size, size, True)
    r, g, b = hex_rgb(hexcol)
    arr = np.zeros((size, size, 4), dtype=np.float32)
    arr[..., 0], arr[..., 1], arr[..., 2] = r * shade, g * shade, b * shade
    arr[..., 3] = bg_alpha
    yy, xx = np.mgrid[0:size, 0:size]
    if diamond:
        m = ((xx + yy) % step < line) | ((xx - yy) % step < line)
    else:
        m = (xx % step < line) | (yy % step < line)
    arr[..., 3][m] = line_alpha
    arr[..., 0][m], arr[..., 1][m], arr[..., 2][m] = r, g, b
    _fill_image(img, arr)
    return img


def _tex(nt, img, loc=(-350, 0), interp='Closest'):
    t = nt.nodes.new('ShaderNodeTexImage')
    t.image = img
    t.interpolation = interp
    t.location = loc
    return t


def ensure_materials(rebuild_images=True):
    pal = build_palette_image() if (rebuild_images or not bpy.data.images.get("T_Paleta")) else bpy.data.images["T_Paleta"]
    mats = {}

    def base(name, rough, spec, emit=None, alpha=None, viewport=(0.8, 0.8, 0.8, 1)):
        mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        nt, bsdf = _reset_nodes(mat)
        tx = _tex(nt, pal)
        nt.links.new(tx.outputs['Color'], _inp(bsdf, 'Base Color'))
        _inp(bsdf, 'Roughness').default_value = rough
        s = _inp(bsdf, 'Specular IOR Level', 'Specular')
        if s is not None:
            s.default_value = spec
        if emit:
            nt.links.new(tx.outputs['Color'], _inp(bsdf, 'Emission Color', 'Emission'))
            _inp(bsdf, 'Emission Strength').default_value = emit
        if alpha is not None:
            _inp(bsdf, 'Alpha').default_value = alpha
            mat.surface_render_method = 'BLENDED'
        else:
            mat.surface_render_method = 'DITHERED'
        mat.use_backface_culling = False
        mat.diffuse_color = viewport
        mat.use_fake_user = True
        mats[name] = mat
        return mat

    base("M_Paleta", 0.85, 0.25)
    base("M_Paleta_Vidro", 0.12, 0.7, viewport=(0.35, 0.42, 0.5, 1))
    base("M_Paleta_Emissivo", 0.5, 0.3, emit=6.0, viewport=(1, 0.9, 0.6, 1))
    base("M_Vidro_Transparente", 0.05, 0.8, alpha=0.3, viewport=(0.7, 0.8, 0.9, 0.3))

    # placas (atlas). Placeholder branco ate o atlas ser importado.
    mat = bpy.data.materials.get("M_Placas") or bpy.data.materials.new("M_Placas")
    atlas = bpy.data.images.get("T_Placas")
    if atlas is None:
        import numpy as np
        atlas = _new_image("T_Placas", 4, 4, True)
        _fill_image(atlas, np.ones((4, 4, 4), dtype=np.float32))
    nt, bsdf = _reset_nodes(mat)
    tx = _tex(nt, atlas, interp='Linear')
    nt.links.new(tx.outputs['Color'], _inp(bsdf, 'Base Color'))
    _inp(bsdf, 'Roughness').default_value = 0.55
    mat.use_backface_culling = False
    mat.use_fake_user = True
    mats["M_Placas"] = mat

    # atlas do treinamento (tablet, identificacao do ponto de ancoragem, placas do roteiro)
    mt = bpy.data.materials.get("M_Treinamento") or bpy.data.materials.new("M_Treinamento")
    at2 = bpy.data.images.get("T_Treinamento")
    if at2 is None:
        import numpy as np
        at2 = _new_image("T_Treinamento", 4, 4, True)
        _fill_image(at2, np.ones((4, 4, 4), dtype=np.float32))
    nt, bsdf = _reset_nodes(mt)
    tx = _tex(nt, at2, interp='Linear')
    nt.links.new(tx.outputs['Color'], _inp(bsdf, 'Base Color'))
    _inp(bsdf, 'Roughness').default_value = 0.6
    mt.use_backface_culling = False
    mt.use_fake_user = True
    mats["M_Treinamento"] = mt

    # telas e redes: alpha MASK (Math Round) -> glTF alphaMode MASK
    def masked(name, img, rough=0.8):
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        nt, bsdf = _reset_nodes(m)
        tx = _tex(nt, img, loc=(-500, 0), interp='Linear')
        nt.links.new(tx.outputs['Color'], _inp(bsdf, 'Base Color'))
        rnd = nt.nodes.new('ShaderNodeMath')
        rnd.operation = 'ROUND'
        rnd.location = (-150, -250)
        nt.links.new(tx.outputs['Alpha'], rnd.inputs[0])
        nt.links.new(rnd.outputs[0], _inp(bsdf, 'Alpha'))
        _inp(bsdf, 'Roughness').default_value = rough
        m.surface_render_method = 'DITHERED'
        m.use_backface_culling = False
        m.use_fake_user = True
        mats[name] = m
        return m

    masked("M_Tela_GcR", build_mesh_image("T_Tela_GcR", PAL[PI["laranja_seguranca"]][1], size=32, step=8, line=2))
    masked("M_Rede_Seguranca", build_mesh_image("T_Rede_Seguranca", PAL[PI["rede_preta"]][1], size=32, step=16, line=2, diamond=True))

    # tela fachadeira: semitransparente (BLEND)
    m = bpy.data.materials.get("M_Tela_Fachada") or bpy.data.materials.new("M_Tela_Fachada")
    img = build_mesh_image("T_Tela_Fachada", PAL[PI["tela_azul"]][1], size=32, step=4, line=1, bg_alpha=1.0, shade=0.82)
    nt, bsdf = _reset_nodes(m)
    tx = _tex(nt, img, interp='Linear')
    nt.links.new(tx.outputs['Color'], _inp(bsdf, 'Base Color'))
    _inp(bsdf, 'Alpha').default_value = 0.62
    _inp(bsdf, 'Roughness').default_value = 0.9
    m.surface_render_method = 'BLENDED'
    m.use_backface_culling = False
    m.use_fake_user = True
    mats["M_Tela_Fachada"] = m
    return mats


def get_mat(slot):
    m = bpy.data.materials.get(SLOTS[slot])
    if m is None:
        ensure_materials(False)
        m = bpy.data.materials.get(SLOTS[slot])
    return m


# ---------------------------------------------------------------- colecoes
def root():
    c = bpy.data.collections.get(ROOT)
    if c is None:
        c = bpy.data.collections.new(ROOT)
        bpy.context.scene.collection.children.link(c)
    return c


def coll(name, parent=None):
    if parent is None:
        par = root()
    elif isinstance(parent, str):
        par = coll(parent)
    else:
        par = parent
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        par.children.link(c)
    return c


def purge_meshes():
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)
    for cu in list(bpy.data.curves):
        if cu.users == 0:
            bpy.data.curves.remove(cu)


def clear_coll(c):
    if isinstance(c, str):
        c = bpy.data.collections.get(c)
        if c is None:
            return
    for o in list(c.all_objects):
        bpy.data.objects.remove(o, do_unlink=True)
    purge_meshes()


def unique_name(base):
    if bpy.data.objects.get(base) is None:
        return base
    k = 2
    while bpy.data.objects.get("%s_%02d" % (base, k)) is not None:
        k += 1
    return "%s_%02d" % (base, k)


def tag(o, **kw):
    for k, v in kw.items():
        o[k] = v
    return o


def empty(name, c, loc=(0, 0, 0), rz=0.0, parent=None, size=1.0, kind='PLAIN_AXES', props=None):
    o = bpy.data.objects.new(unique_name(name), None)
    o.empty_display_type = kind
    o.empty_display_size = size
    o.location = loc
    o.rotation_euler = (0.0, 0.0, math.radians(rz))
    c.objects.link(o)
    if parent is not None:
        o.parent = parent
    if props:
        tag(o, **props)
    return o


def inst(name, mesh, c, loc=(0, 0, 0), rz=0.0, parent=None, rx=0.0, ry=0.0, scale=None, props=None):
    if isinstance(mesh, bpy.types.Object):
        mesh = mesh.data
    o = bpy.data.objects.new(unique_name(name), mesh)
    o.location = loc
    o.rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
    if scale is not None:
        o.scale = scale if hasattr(scale, '__len__') else (scale, scale, scale)
    c.objects.link(o)
    if parent is not None:
        o.parent = parent
    if props:
        tag(o, **props)
    return o


# -------------------------------------------------------------- construtor
_ICO = {}


def ico_data(sub=2):
    if sub not in _ICO:
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0)
        bm.verts.index_update()
        V = [tuple(v.co) for v in bm.verts]
        F = [[v.index for v in f.verts] for f in bm.faces]
        bm.free()
        _ICO[sub] = (V, F)
    return _ICO[sub]


BOX_F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


class MB:
    """Acumula geometria (vertices, faces, cor por face) em coordenadas locais."""

    def __init__(self):
        self.V = []
        self.F = []
        self.C = []
        self.S = []
        self.UV = {}
        self.stack = [Matrix.Identity(4)]

    # transformacoes -------------------------------------------------------
    @property
    def M(self):
        return self.stack[-1]

    @contextmanager
    def at(self, loc=(0, 0, 0), rz=0.0, rx=0.0, ry=0.0, M=None):
        self.stack.append(self.stack[-1] @ (M if M is not None else T(loc, rz, rx, ry)))
        try:
            yield self
        finally:
            self.stack.pop()

    def _tr(self, verts):
        M = self.M
        if M == Matrix.Identity(4):
            return [tuple(v) for v in verts]
        return [tuple(M @ Vector(v)) for v in verts]

    def part(self, verts, faces, cols, smooth=False):
        b = len(self.V)
        self.V.extend(self._tr(verts))
        multi = isinstance(cols, list)
        sm_multi = isinstance(smooth, list)
        for i, f in enumerate(faces):
            self.F.append(tuple(b + k for k in f))
            self.C.append(cid(cols[i] if multi else cols))
            self.S.append(smooth[i] if sm_multi else smooth)

    def merge(self, other):
        b = len(self.V)
        f0 = len(self.F)
        self.V.extend(self._tr(other.V))
        for f in other.F:
            self.F.append(tuple(b + k for k in f))
        self.C.extend(other.C)
        self.S.extend(other.S)
        for fi, uv in other.UV.items():
            self.UV[f0 + fi] = uv

    @property
    def nfaces(self):
        return len(self.F)

    # primitivas -----------------------------------------------------------
    def poly(self, pts, c, smooth=False):
        self.part(pts, [tuple(range(len(pts)))], [c], smooth)

    def quad_uv(self, pts, uvs, slot):
        b = len(self.V)
        self.V.extend(self._tr(pts))
        self.UV[len(self.F)] = list(uvs)
        self.F.append(tuple(range(b, b + len(pts))))
        self.C.append(slot * 256)
        self.S.append(False)

    def box(self, lo, hi, c, top=None, bottom=None, sides=None, nobottom=False, notop=False, fc=None):
        x0, x1 = sorted((lo[0], hi[0]))
        y0, y1 = sorted((lo[1], hi[1]))
        z0, z1 = sorted((lo[2], hi[2]))
        v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        faces, cols = [], []
        for i, f in enumerate(BOX_F):
            if (i == 0 and nobottom) or (i == 1 and notop):
                continue
            col = c
            if fc is not None:
                col = fc[i]
            elif i == 0 and bottom is not None:
                col = bottom
            elif i == 1 and top is not None:
                col = top
            elif i >= 2 and sides is not None:
                col = sides
            faces.append(f)
            cols.append(col)
        self.part(v, faces, cols)

    def boxc(self, center, size, c, **kw):
        cx, cy, cz = center
        sx, sy, sz = size
        self.box((cx - sx / 2, cy - sy / 2, cz - sz / 2), (cx + sx / 2, cy + sy / 2, cz + sz / 2), c, **kw)

    def hull(self, pts, c, top=None, bottom=None, side=None, smooth=False, thr=0.7):
        bm = bmesh.new()
        vs = [bm.verts.new(p) for p in pts]
        res = bmesh.ops.convex_hull(bm, input=vs, use_existing_faces=False)
        junk = [g for g in list(res.get('geom_interior', [])) + list(res.get('geom_unused', []))
                if isinstance(g, bmesh.types.BMVert)]
        if junk:
            bmesh.ops.delete(bm, geom=junk, context='VERTS')
        bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), use_dissolve_boundaries=False,
                                 verts=list(bm.verts), edges=list(bm.edges))
        bm.normal_update()
        bm.verts.index_update()
        verts = [tuple(v.co) for v in bm.verts]
        faces, cols = [], []
        for f in bm.faces:
            faces.append([v.index for v in f.verts])
            n = f.normal
            col = c
            if top is not None and n.z > thr:
                col = top
            elif bottom is not None and n.z < -thr:
                col = bottom
            elif side is not None and abs(n.z) <= thr:
                col = side
            cols.append(col)
        bm.free()
        self.part(verts, faces, cols, smooth)

    def rbox(self, lo, hi, c, r=0.05, top=None, bottom=None, side=None):
        x0, x1 = sorted((lo[0], hi[0]))
        y0, y1 = sorted((lo[1], hi[1]))
        z0, z1 = sorted((lo[2], hi[2]))
        d = max(0.0, min(r, (x1 - x0) * 0.45, (y1 - y0) * 0.45, (z1 - z0) * 0.45))
        if d < 1e-4:
            return self.box((x0, y0, z0), (x1, y1, z1), c, top=top, bottom=bottom, sides=side)
        pts = []
        for x, sx in ((x0, 1), (x1, -1)):
            for y, sy in ((y0, 1), (y1, -1)):
                for z, sz in ((z0, 1), (z1, -1)):
                    pts += [(x + sx * d, y + sy * d, z), (x + sx * d, y, z + sz * d), (x, y + sy * d, z + sz * d)]
        self.hull(pts, c, top=top, bottom=bottom, side=side)

    def taper(self, lo, hi, inset_top=(0.0, 0.0, 0.0, 0.0), c='branco', top=None, side=None, bottom=None):
        """caixa com topo recuado: inset_top = (x0, x1, y0, y1) recuos no topo."""
        x0, y0, z0 = lo
        x1, y1, z1 = hi
        a, b, cc, d = inset_top
        pts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
               (x0 + a, y0 + cc, z1), (x1 - b, y0 + cc, z1), (x1 - b, y1 - d, z1), (x0 + a, y1 - d, z1)]
        self.hull(pts, c, top=top, side=side, bottom=bottom)

    def cyl(self, p0, p1, r, c, n=8, r1=None, caps=True, cap=None, smooth=True, phase=None):
        p0 = Vector(p0)
        p1 = Vector(p1)
        ax = p1 - p0
        L = ax.length
        if L < 1e-7:
            return
        z = ax / L
        a = Vector((0, 0, 1)) if abs(z.z) < 0.95 else Vector((1, 0, 0))
        x = a.cross(z).normalized()
        y = z.cross(x)
        r1 = r if r1 is None else r1
        ph = (math.pi / n) if phase is None else phase
        ring0, ring1 = [], []
        for i in range(n):
            ang = ph + 2 * math.pi * i / n
            d = x * math.cos(ang) + y * math.sin(ang)
            ring0.append(tuple(p0 + d * r))
            ring1.append(tuple(p1 + d * r1))
        capc = cap if cap is not None else c
        if r1 <= 1e-6:
            verts = ring0 + [tuple(p1)]
            faces = [(i, (i + 1) % n, n) for i in range(n)]
            cols = [c] * n
            sm = [smooth] * n
            if caps:
                faces.append(tuple(reversed(range(n))))
                cols.append(capc)
                sm.append(False)
        else:
            verts = ring0 + ring1
            faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
            cols = [c] * n
            sm = [smooth] * n
            if caps:
                faces.append(tuple(reversed(range(n))))
                faces.append(tuple(range(n, 2 * n)))
                cols += [capc, capc]
                sm += [False, False]
        self.part(verts, faces, cols, sm)

    def strut(self, p0, p1, w, c, h=None, up=(0, 0, 1), caps=True):
        p0 = Vector(p0)
        p1 = Vector(p1)
        d = p1 - p0
        L = d.length
        if L < 1e-7:
            return
        z = d / L
        upv = Vector(up)
        if abs(z.dot(upv)) > 0.99:
            upv = Vector((1, 0, 0)) if abs(z.x) < 0.9 else Vector((0, 1, 0))
        x = upv.cross(z).normalized()
        y = z.cross(x)
        hw = w / 2.0
        hh = (h if h is not None else w) / 2.0
        cs = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        verts = [tuple(p0 + x * a + y * b) for a, b in cs] + [tuple(p1 + x * a + y * b) for a, b in cs]
        faces = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        if caps:
            faces += [(3, 2, 1, 0), (4, 5, 6, 7)]
        self.part(verts, faces, c)

    def lathe(self, prof, c, n=12, smooth=True, cap0=True, cap1=True, color_fn=None, phase=None):
        ph = math.pi / n if phase is None else phase
        rings = len(prof)
        verts = []
        for (r, z) in prof:
            for i in range(n):
                a = ph + 2 * math.pi * i / n
                verts.append((r * math.cos(a), r * math.sin(a), z))
        faces, cols, sm = [], [], []
        for k in range(rings - 1):
            for i in range(n):
                j = (i + 1) % n
                faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
                cols.append(color_fn(k, i) if color_fn else c)
                sm.append(smooth)
        if cap0:
            faces.append(tuple(reversed(range(n))))
            cols.append(cap0 if isinstance(cap0, str) else c)
            sm.append(False)
        if cap1:
            faces.append(tuple(range((rings - 1) * n, rings * n)))
            cols.append(cap1 if isinstance(cap1, str) else c)
            sm.append(False)
        self.part(verts, faces, cols, sm)

    def prism(self, poly, z0, z1, c, top=None, bottom=None, nobottom=False, notop=False, side=None):
        n = len(poly)
        area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
        if area < 0:
            poly = list(reversed(poly))
        verts = [(p[0], p[1], z0) for p in poly] + [(p[0], p[1], z1) for p in poly]
        faces, cols = [], []
        for i in range(n):
            j = (i + 1) % n
            faces.append((i, j, n + j, n + i))
            cols.append(side if side is not None else c)
        if not nobottom:
            faces.append(tuple(reversed(range(n))))
            cols.append(bottom if bottom is not None else c)
        if not notop:
            faces.append(tuple(range(n, 2 * n)))
            cols.append(top if top is not None else c)
        self.part(verts, faces, cols)

    def xprism(self, poly, y0, y1, c, front=None, back=None, top=None, side=None, thr=0.6, colfn=None):
        """poligono no plano XZ [(x, z)], extrudado de y0 a y1."""
        n = len(poly)
        area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
        if area < 0:
            poly = list(reversed(poly))
        verts = [(p[0], y0, p[1]) for p in poly] + [(p[0], y1, p[1]) for p in poly]
        faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
        cols = [front if front is not None else c, back if back is not None else c]
        for i in range(n):
            j = (i + 1) % n
            faces.append((i, n + i, n + j, j))
            dx = poly[j][0] - poly[i][0]
            dz = poly[j][1] - poly[i][1]
            L = math.hypot(dx, dz) or 1.0
            nz = -dx / L
            col = c
            if colfn is not None:
                col = colfn(i, dx / L, dz / L)
            elif top is not None and nz > thr:
                col = top
            elif side is not None:
                col = side
            cols.append(col)
        self.part(verts, faces, cols)

    def blob(self, center, radius, c, sub=2, noise=0.12, rng=None, squash=(1.0, 1.0, 1.0), smooth=False, colfn=None):
        V, F = ico_data(sub)
        rng = rng or random
        cx, cy, cz = center
        verts = []
        for (x, y, z) in V:
            k = 1.0 + (rng.uniform(-noise, noise) if noise else 0.0)
            verts.append((cx + x * radius * squash[0] * k, cy + y * radius * squash[1] * k, cz + z * radius * squash[2] * k))
        cols = [colfn(i, V, F) for i in range(len(F))] if colfn else c
        self.part(verts, F, cols, smooth)

    def wall(self, x0, x1, y0, y1, z0, z1, c, openings=()):
        """parede ao longo de X (espessura em Y) com vaos [(ox0, ox1, oz0, oz1)]."""
        xs = sorted(set([x0, x1] + [v for o in openings for v in (o[0], o[1]) if x0 < v < x1]))
        zs = sorted(set([z0, z1] + [v for o in openings for v in (o[2], o[3]) if z0 < v < z1]))
        for zi in range(len(zs) - 1):
            za, zb = zs[zi], zs[zi + 1]
            run = None
            for xi in range(len(xs) - 1):
                xa, xb = xs[xi], xs[xi + 1]
                xm, zm = (xa + xb) / 2, (za + zb) / 2
                hole = any(o[0] <= xm <= o[1] and o[2] <= zm <= o[3] for o in openings)
                if not hole:
                    run = (run[0], xb) if run else (xa, xb)
                elif run:
                    self.box((run[0], y0, za), (run[1], y1, zb), c)
                    run = None
            if run:
                self.box((run[0], y0, za), (run[1], y1, zb), c)

    def ywall(self, y0, y1, x0, x1, z0, z1, c, openings=()):
        """parede ao longo de Y (espessura em X); vaos [(oy0, oy1, oz0, oz1)]."""
        sub = MB()
        sub.wall(y0, y1, -x1, -x0, z0, z1, c, openings)
        with self.at(M=Matrix(((0, -1, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))):
            self.merge(sub)

    def ring_box(self, x0, y0, x1, y1, z0, z1, w, c, **kw):
        """moldura retangular (4 caixas) de largura w para dentro."""
        self.box((x0, y0, z0), (x1, y0 + w, z1), c, **kw)
        self.box((x0, y1 - w, z0), (x1, y1, z1), c, **kw)
        self.box((x0, y0 + w, z0), (x0 + w, y1 - w, z1), c, **kw)
        self.box((x1 - w, y0 + w, z0), (x1, y1 - w, z1), c, **kw)

    def polyline_tube(self, pts, r, c, n=6, smooth=True):
        for a, b in zip(pts[:-1], pts[1:]):
            self.cyl(a, b, r, c, n=n, caps=False, smooth=smooth)


def finish(mb, name, c, parent=None, loc=None, rz=0.0, props=None):
    nm = unique_name(name)
    me = finish_mesh(mb, nm)
    if me is None:
        return None
    o = bpy.data.objects.new(nm, me)
    if loc is not None:
        o.location = loc
    if rz:
        o.rotation_euler = (0.0, 0.0, math.radians(rz))
    c.objects.link(o)
    if parent is not None:
        o.parent = parent
    if props:
        tag(o, **props)
    return o


def mesh_only(mb, name):
    """cria so o datablock de malha (prototipo para instancias)."""
    return finish_mesh(mb, name)


def finish_mesh(mb, nm):
    import numpy as np
    if not mb.F:
        return None
    me = bpy.data.meshes.new(nm)
    me.from_pydata(mb.V, [], mb.F)
    npoly = len(me.polygons)
    if npoly != len(mb.F):
        raise RuntimeError("from_pydata perdeu faces em %s (%d/%d)" % (nm, npoly, len(mb.F)))
    C = np.asarray(mb.C, dtype=np.int64)
    slots = C // 256
    colors = C % 256
    used = sorted(set(int(s) for s in slots))
    remap = np.zeros(max(used) + 1, dtype=np.int64)
    for k, s in enumerate(used):
        me.materials.append(get_mat(s))
        remap[s] = k
    me.polygons.foreach_set('material_index', remap[slots].astype(np.int32))
    me.polygons.foreach_set('use_smooth', np.asarray(mb.S, dtype=bool))
    ltot = np.zeros(npoly, dtype=np.int32)
    me.polygons.foreach_get('loop_total', ltot)
    lc = np.repeat(colors, ltot)
    uv = np.empty((len(lc), 2), dtype=np.float32)
    uv[:, 0] = (lc % GRID + 0.5) / GRID
    uv[:, 1] = 1.0 - ((lc // GRID) + 0.5) / GRID
    if mb.UV:
        lst = np.zeros(npoly, dtype=np.int32)
        me.polygons.foreach_get('loop_start', lst)
        for fi, uvs in mb.UV.items():
            s = int(lst[fi])
            for k, (u, v) in enumerate(uvs):
                uv[s + k, 0] = u
                uv[s + k, 1] = v
    uvl = me.uv_layers.new(name="UVMap")
    uvl.data.foreach_set('uv', uv.ravel())
    me.update()
    return me


# ------------------------------------------------------------- utilidades
def desktop():
    import os
    try:
        import ctypes, uuid
        from ctypes import wintypes

        class GUID(ctypes.Structure):
            _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD), ("Data3", wintypes.WORD),
                        ("Data4", ctypes.c_ubyte * 8)]
        u = uuid.UUID('{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}')
        g = GUID(u.fields[0], u.fields[1], u.fields[2], (ctypes.c_ubyte * 8).from_buffer_copy(u.bytes[8:]))
        ptr = ctypes.c_wchar_p()
        f = ctypes.windll.shell32.SHGetKnownFolderPath
        f.argtypes = [ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]
        if f(ctypes.byref(g), 0, None, ctypes.byref(ptr)) == 0:
            p = ptr.value
            ctypes.windll.ole32.CoTaskMemFree(ptr)
            return p
    except Exception:
        pass
    return os.path.join(os.path.expanduser('~'), 'Desktop')


def save():
    import os
    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile(compress=True)
    else:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(desktop(), "canteiro_trabalho_altura.blend"), compress=True)
    return bpy.data.filepath


def tri_count(objs):
    t = 0
    for o in objs:
        if o.type == 'MESH':
            for p in o.data.polygons:
                t += p.loop_total - 2
    return t


def stats():
    out = {}
    for c in root().children:
        objs = list(c.all_objects)
        out[c.name] = (len(objs), tri_count(objs))
    return out


def set_view(loc, rot_deg, dist, shading='MATERIAL', lens=35):
    from mathutils import Vector, Euler
    for w in bpy.data.window_managers[0].windows:
        for a in w.screen.areas:
            if a.type == 'VIEW_3D':
                sp = a.spaces.active
                sp.shading.type = shading
                sp.overlay.show_floor = False
                sp.overlay.show_axis_x = False
                sp.overlay.show_axis_y = False
                sp.overlay.show_relationship_lines = False
                r3 = sp.region_3d
                r3.view_perspective = 'PERSP'
                r3.view_location = Vector(loc)
                r3.view_rotation = Euler([math.radians(v) for v in rot_deg], 'XYZ').to_quaternion()
                r3.view_distance = dist
                sp.lens = lens
    return True


def loadmod(name):
    import sys, types
    m = sys.modules.get(name)
    if m is None:
        m = types.ModuleType(name)
        exec(compile(bpy.data.texts[name + ".py"].as_string(), name + ".py", "exec"), m.__dict__)
        sys.modules[name] = m
    return m


def look(cam, target, lens=35, shading='MATERIAL'):
    from mathutils import Vector
    cam = Vector(cam)
    target = Vector(target)
    d = target - cam
    for w in bpy.data.window_managers[0].windows:
        for a in w.screen.areas:
            if a.type == 'VIEW_3D':
                sp = a.spaces.active
                sp.shading.type = shading
                r3 = sp.region_3d
                r3.view_perspective = 'PERSP'
                r3.view_location = target
                r3.view_rotation = d.to_track_quat('-Z', 'Y')
                r3.view_distance = d.length
                sp.lens = lens
    return True


def render_cam(cam_name, filename, pct=50):
    import os
    scn = bpy.context.scene
    scn.camera = bpy.data.objects[cam_name]
    scn.render.resolution_percentage = pct
    pasta = os.path.join(desktop(), "canteiro_trabalho_altura_arquivos", "renders")
    os.makedirs(pasta, exist_ok=True)
    scn.render.filepath = os.path.join(pasta, filename)
    bpy.ops.render.render(write_still=True)
    return scn.render.filepath
