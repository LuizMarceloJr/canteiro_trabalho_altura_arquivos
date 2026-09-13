# -*- coding: utf-8 -*-
# personagens.py - figurantes low-poly posaveis (sem rig) para o roteiro de Trabalho em Altura
# Convencao local do personagem: X = direita, Y = frente, Z = cima; pes em z = 0.
# Cada personagem vira UMA malha (1 material M_Paleta) -> leve no Three.js.
# Poses = angulos por articulacao (graus). Use pose("nome", **ajustes) para combinar.
import bpy, sys, math
from mathutils import Matrix, Vector, Euler

K = sys.modules["sitekit"]
MB = K.MB

# ------------------------------------------------------------------ papeis (roupas)
PAPEIS = {
    "jogador": dict(capacete="capacete_azul", camisa="uniforme_azul", calca="jeans_escuro", colete="colete_limao",
                    pele="pele_morena", luva="luva_cinza", bota="bota_couro", cinturao="laranja_seguranca", talabarte=True),
    "encarregado": dict(capacete="capacete_branco", camisa="branco_fosco", calca="jeans", colete=None, pele="pele_clara",
                        luva=None, bota="bota_couro", radio_peito=True),
    "pedreiro": dict(capacete="capacete_amarelo", camisa="uniforme_laranja", calca="jeans", colete=None, pele="pele_escura",
                     luva="luva_amarela", bota="bota_couro"),
    "servente": dict(capacete="capacete_amarelo", camisa="uniforme_cinza", calca="jeans_escuro", colete="laranja_seguranca",
                     pele="pele_morena", luva="luva_amarela", bota="bota_couro"),
    "colega_altura": dict(capacete="capacete_amarelo", camisa="uniforme_azul", calca="jeans", colete="colete_limao", pele="pele_clara",
                          luva="luva_cinza", bota="bota_couro", cinturao="amarelo_linha_vida", talabarte=True),
    "almoxarife": dict(capacete="capacete_branco", camisa="uniforme_verde", calca="jeans", colete=None, pele="pele_escura",
                       luva=None, bota="bota_couro"),
    "tecnico_seguranca": dict(capacete="capacete_verde", camisa="branco_fosco", calca="jeans_escuro", colete="colete_limao",
                              pele="pele_morena", luva=None, bota="bota_couro", radio_peito=True),
    "resgate": dict(capacete="capacete_vermelho", camisa="vermelho_resgate", calca="uniforme_cinza", colete="laranja_neon",
                    pele="pele_clara", luva="preto_suave", bota="preto_suave", cinturao="preto_radio", talabarte=False, radio_peito=True),
    "motorista": dict(capacete="capacete_amarelo", camisa="uniforme_cinza", calca="jeans", colete="colete_limao", pele="pele_escura",
                      luva="luva_cinza", bota="bota_couro"),
    "sinaleiro": dict(capacete="capacete_amarelo", camisa="uniforme_azul", calca="jeans_escuro", colete="laranja_neon",
                      pele="pele_clara", luva="luva_amarela", bota="bota_couro", radio_peito=True),
    "porteiro": dict(capacete=None, camisa="azul_escuro", calca="preto_suave", colete=None, pele="pele_morena", luva=None,
                     bota="preto_suave", cabelo=True),
    "armador": dict(capacete="capacete_azul", camisa="uniforme_cinza", calca="jeans", colete="laranja_seguranca", pele="pele_clara",
                    luva="luva_amarela", bota="bota_couro", cinturao="laranja_seguranca", talabarte=True),
}

# ------------------------------------------------------------------ esqueleto (repouso)
# nome: (pai, deslocamento a partir do pai)
OSSOS = [
    ("pelvis", None, (0.0, 0.0, 0.93)),
    ("spine", "pelvis", (0.0, 0.0, 0.10)),
    ("chest", "spine", (0.0, 0.0, 0.24)),
    ("neck", "chest", (0.0, 0.0, 0.19)),
    ("head", "neck", (0.0, 0.0, 0.07)),
    ("shoulder_R", "chest", (0.185, 0.0, 0.13)),
    ("elbow_R", "shoulder_R", (0.0, 0.0, -0.29)),
    ("wrist_R", "elbow_R", (0.0, 0.0, -0.255)),
    ("shoulder_L", "chest", (-0.185, 0.0, 0.13)),
    ("elbow_L", "shoulder_L", (0.0, 0.0, -0.29)),
    ("wrist_L", "elbow_L", (0.0, 0.0, -0.255)),
    ("hip_R", "pelvis", (0.10, 0.0, -0.03)),
    ("knee_R", "hip_R", (0.0, 0.0, -0.43)),
    ("ankle_R", "knee_R", (0.0, 0.0, -0.42)),
    ("hip_L", "pelvis", (-0.10, 0.0, -0.03)),
    ("knee_L", "hip_L", (0.0, 0.0, -0.43)),
    ("ankle_L", "knee_L", (0.0, 0.0, -0.42)),
]


def _rot(rx=0.0, ry=0.0, rz=0.0):
    return Euler((math.radians(rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix().to_4x4()


# ------------------------------------------------------------------ poses
def _arm(side, flex=0.0, abd=0.0, twist=0.0):
    """flex + = braco para frente; abd + = para fora (lado do corpo); twist + = rotacao interna."""
    s = 1.0 if side == "R" else -1.0
    return (flex, -abd * s, twist * s)


def _leg(side, flex=0.0, abd=0.0, twist=0.0):
    s = 1.0 if side == "R" else -1.0
    return (flex, -abd * s, twist * s)


def P(pz=0.93, raiz=(0, 0, 0), pelvis=(0, 0, 0), spine=(0, 0, 0), chest=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0),
      ombroR=(0, 8, 0), ombroL=(0, 8, 0), cotR=10, cotL=10, pulsoR=(0, 0, 0), pulsoL=(0, 0, 0),
      quadR=(0, 0, 0), quadL=(0, 0, 0), joeR=0, joeL=0, tornR=0, tornL=0):
    """angulos amigaveis -> dicionario por articulacao.
    spine/chest/neck/head: (rx, ry, rz) com rx NEGATIVO = inclinar para frente / olhar para baixo.
    ombro/quad: (flex, abd, twist); cot/joe: flexao (graus); torn: + = ponta do pe para cima."""
    return {
        "pz": pz, "raiz": raiz,
        "pelvis": pelvis, "spine": spine, "chest": chest, "neck": neck, "head": head,
        "shoulder_R": _arm("R", *ombroR), "shoulder_L": _arm("L", *ombroL),
        "elbow_R": (cotR, 0, 0), "elbow_L": (cotL, 0, 0),
        "wrist_R": pulsoR, "wrist_L": pulsoL,
        "hip_R": _leg("R", *quadR), "hip_L": _leg("L", *quadL),
        "knee_R": (-joeR, 0, 0), "knee_L": (-joeL, 0, 0),
        "ankle_R": (tornR, 0, 0), "ankle_L": (tornL, 0, 0),
    }


POSES = {
    "em_pe": dict(),
    "em_pe_bracos_cruzados": dict(ombroR=(35, -25, 0), ombroL=(35, -25, 0), cotR=115, cotL=110),
    "andando": dict(pz=0.92, quadR=(24, 2, 0), quadL=(-16, 2, 0), joeR=8, joeL=30, tornR=-4, tornL=12,
                    ombroR=(-22, 8, 0), ombroL=(24, 8, 0), cotR=12, cotL=22, spine=(0, 0, 4)),
    "correndo": dict(pz=0.88, spine=(-14, 0, 0), quadR=(48, 2, 0), quadL=(-30, 2, 0), joeR=35, joeL=85, tornR=0, tornL=20,
                     ombroR=(-45, 10, 0), ombroL=(50, 10, 0), cotR=85, cotL=85),
    "apontando": dict(ombroR=(82, 14, 0), cotR=4, head=(0, 0, -8), ombroL=(5, 10, 0)),
    "conversando": dict(ombroR=(30, 14, 0), cotR=72, ombroL=(8, 10, 0), cotL=15, head=(-4, 0, 6)),
    "falando_radio": dict(ombroR=(38, 30, 0), cotR=135, pulsoR=(0, 0, 0), head=(-8, 0, -6), ombroL=(5, 10, 0)),
    "segurando_tablet": dict(ombroR=(34, -14, 0), ombroL=(34, -14, 0), cotR=84, cotL=84, head=(-28, 0, 0), neck=(-6, 0, 0)),
    "entregando_tablet": dict(ombroR=(58, 6, 0), cotR=28, ombroL=(10, 8, 0), cotL=18, head=(-6, 0, 0), spine=(-4, 0, 0)),
    "agachado_trabalhando": dict(pz=0.55, spine=(-24, 0, 0), chest=(-10, 0, 0), head=(-30, 0, 0),
                                 quadR=(84, 4, 0), joeR=88, tornR=4, quadL=(-4, 4, 0), joeL=86, tornL=58,
                                 ombroR=(58, 6, 0), cotR=48, ombroL=(42, 10, 0), cotL=62),
    "ajoelhado_olhando": dict(pz=0.55, spine=(-8, 0, 0), head=(-12, 0, 0), quadR=(84, 4, 0), joeR=88, tornR=4,
                              quadL=(-4, 4, 0), joeL=86, tornL=58, ombroR=(20, 10, 0), cotR=40, ombroL=(10, 10, 0), cotL=30),
    "abaixado_pegando": dict(pz=0.80, spine=(-52, 0, 0), chest=(-14, 0, 0), head=(-10, 0, 0), quadR=(40, 4, 0), quadL=(36, 4, 0),
                             joeR=48, joeL=44, tornR=-6, tornL=-6, ombroR=(72, 6, 0), ombroL=(68, 6, 0), cotR=10, cotL=12),
    "escorregando": dict(pz=0.70, raiz=(0, 0, 0), pelvis=(26, 0, 0), spine=(14, 0, 0), chest=(8, 0, 0), head=(-18, 0, 0),
                         quadR=(62, 6, 0), joeR=8, tornR=10, quadL=(10, 8, 0), joeL=52, tornL=-10,
                         ombroR=(105, 42, 0), ombroL=(95, 48, 0), cotR=22, cotL=30),
    "desequilibrio_frente": dict(pz=0.90, spine=(-26, 6, 0), chest=(-8, 0, 0), head=(-10, 0, 0), quadR=(34, 4, 0), joeR=22,
                                 quadL=(-22, 6, 0), joeL=14, tornL=18, ombroR=(62, 62, 0), ombroL=(28, 74, 0), cotR=20, cotL=34),
    "desequilibrio_tras": dict(pz=0.88, pelvis=(10, 0, 0), spine=(20, -6, 0), chest=(8, 0, 0), head=(-12, 0, 0),
                               quadR=(32, 6, 0), joeR=12, quadL=(-12, 6, 0), joeL=28, ombroR=(40, 78, 0), ombroL=(55, 70, 0),
                               cotR=26, cotL=18),
    "tropecando": dict(pz=0.84, spine=(-36, 0, 0), chest=(-8, 0, 0), head=(22, 0, 0), quadR=(55, 4, 0), joeR=72, tornR=10,
                       quadL=(-30, 4, 0), joeL=12, tornL=28, ombroR=(78, 22, 0), ombroL=(72, 26, 0), cotR=28, cotL=22),
    "tontura": dict(pz=0.91, spine=(-12, 8, 0), head=(-16, 6, 10), ombroR=(148, 22, 0), cotR=122, pulsoR=(0, 0, 0),
                    ombroL=(18, 30, 0), cotL=16, quadR=(6, 4, 0), quadL=(2, 6, 0), joeR=10, joeL=6),
    "removendo_gcr": dict(pz=0.88, spine=(-30, 0, 0), head=(12, 0, 0), quadR=(24, 6, 0), quadL=(20, 6, 0), joeR=26, joeL=22,
                          ombroR=(72, 8, 0), ombroL=(70, 8, 0), cotR=28, cotL=30),
    "empurrando": dict(pz=0.90, spine=(-22, 0, 0), head=(10, 0, 0), ombroR=(62, 8, 0), ombroL=(62, 8, 0), cotR=18, cotL=18,
                       quadR=(26, 4, 0), joeR=12, quadL=(-18, 4, 0), joeL=24, tornL=14),
    "movendo_barreira": dict(pz=0.91, spine=(-6, 0, 16), ombroR=(22, 46, 0), cotR=24, ombroL=(48, -6, 0), cotL=42,
                             quadR=(18, 4, 0), joeR=10, quadL=(-12, 4, 0), joeL=20, head=(0, 0, 20)),
    "suspenso": dict(pz=0.93, pelvis=(12, 0, 0), spine=(6, 0, 0), head=(22, 0, 0), quadR=(34, 8, 0), quadL=(22, 10, 0),
                     joeR=46, joeL=30, tornR=-30, tornL=-26, ombroR=(158, 14, 0), ombroL=(162, 12, 0), cotR=28, cotL=34),
    "olhando_cima": dict(head=(30, 0, 0), neck=(8, 0, 0), ombroR=(122, 32, 0), cotR=112, ombroL=(6, 10, 0)),
    "sinalizando_pare": dict(ombroR=(92, 28, 0), cotR=48, pulsoR=(-60, 0, 0), ombroL=(6, 10, 0), head=(-2, 0, 0)),
    "vestindo_conferencia": dict(ombroR=(6, 26, 0), ombroL=(6, 26, 0), cotR=12, cotL=12, head=(-10, 0, 0)),
    "carregando_ombro": dict(pz=0.92, ombroR=(150, 36, 0), cotR=150, ombroL=(-12, 10, 0), cotL=14, quadR=(18, 2, 0), quadL=(-12, 2, 0),
                             joeR=6, joeL=22, tornL=10, head=(0, 0, -6)),
    "carregando_frente": dict(pz=0.91, spine=(4, 0, 0), ombroR=(46, 4, 0), ombroL=(46, 4, 0), cotR=64, cotL=64,
                              quadR=(16, 2, 0), quadL=(-12, 2, 0), joeR=6, joeL=20, tornL=10),
    "subindo_escada": dict(pz=0.93, spine=(-10, 0, 0), head=(14, 0, 0), quadR=(72, 4, 0), joeR=92, tornR=6, quadL=(8, 4, 0), joeL=12,
                           ombroR=(140, 12, 0), cotR=30, ombroL=(104, 12, 0), cotL=62),
    "ferramenta_tranco": dict(pz=0.55, spine=(-18, 0, -24), chest=(-4, 0, -10), head=(-18, 0, 14),
                              quadR=(84, 4, 0), joeR=88, tornR=4, quadL=(-4, 4, 0), joeL=86, tornL=58,
                              ombroR=(30, 70, 40), cotR=22, ombroL=(120, 30, 0), cotL=40),
    "assustado": dict(pz=0.90, spine=(8, 0, 0), head=(18, 0, 12), ombroR=(70, 40, 0), cotR=110, ombroL=(66, 40, 0), cotL=108,
                      quadR=(8, 6, 0), joeR=16, quadL=(-4, 8, 0), joeL=10),
    "comunicando_radio_agachado": dict(pz=0.55, spine=(-6, 0, 0), head=(-4, 0, -10), quadR=(84, 4, 0), joeR=88, tornR=4,
                                       quadL=(-4, 4, 0), joeL=86, tornL=58, ombroR=(38, 30, 0), cotR=135, ombroL=(20, 10, 0), cotL=40),
}


def pose(nome="em_pe", **aj):
    base = dict(POSES[nome])
    base.update(aj)
    return P(**base)



# ------------------------------------------------------------------ partes articuladas
# Cada personagem animavel vira uma arvore de pecas rigidas (estilo Minecraft):
# girar a peca gira em torno da propria articulacao, entao da para animar em tempo real.
PARTES = ["Quadril", "Torso", "Cabeca", "Braco_R", "Antebraco_R", "Braco_L", "Antebraco_L",
          "Coxa_R", "Canela_R", "Coxa_L", "Canela_L"]
ANCORA = {"Quadril": "pelvis", "Torso": "spine", "Cabeca": "head",
          "Braco_R": "shoulder_R", "Antebraco_R": "elbow_R",
          "Braco_L": "shoulder_L", "Antebraco_L": "elbow_L",
          "Coxa_R": "hip_R", "Canela_R": "knee_R",
          "Coxa_L": "hip_L", "Canela_L": "knee_L"}
PAI_PARTE = {"Quadril": None, "Torso": "Quadril", "Cabeca": "Torso",
             "Braco_R": "Torso", "Antebraco_R": "Braco_R",
             "Braco_L": "Torso", "Antebraco_L": "Braco_L",
             "Coxa_R": "Quadril", "Canela_R": "Coxa_R",
             "Coxa_L": "Quadril", "Canela_L": "Coxa_L"}
PARTE_DE = {"pelvis": "Quadril", "spine": "Torso", "chest": "Torso", "neck": "Torso",
            "head": "Cabeca",
            "shoulder_R": "Braco_R", "elbow_R": "Antebraco_R", "wrist_R": "Antebraco_R",
            "shoulder_L": "Braco_L", "elbow_L": "Antebraco_L", "wrist_L": "Antebraco_L",
            "hip_R": "Coxa_R", "knee_R": "Canela_R", "ankle_R": "Canela_R",
            "hip_L": "Coxa_L", "knee_L": "Canela_L", "ankle_L": "Canela_L"}


class _Roteador(object):
    """finge ser um MB, mas escreve na peca da articulacao que esta sendo desenhada."""

    def __init__(self, mbs):
        object.__setattr__(self, "_mbs", mbs)
        object.__setattr__(self, "_atual", "Quadril")

    def _ir(self, parte):
        object.__setattr__(self, "_atual", parte)
        return self

    def __getattr__(self, nome):
        return getattr(object.__getattribute__(self, "_mbs")[object.__getattribute__(self, "_atual")], nome)


def repouso():
    """pose neutra: todos os angulos zerados (a base da hierarquia)."""
    return P(pz=0.93)


def offsets_repouso():
    """deslocamento local de cada peca em relacao a peca pai, no esqueleto em repouso."""
    Mw = frames(repouso())
    out = {}
    for parte in PARTES:
        pai = PAI_PARTE[parte]
        Mp = Mw[ANCORA[pai]] if pai else Matrix.Identity(4)
        out[parte] = (Mp.inverted() @ Mw[ANCORA[parte]]).to_translation()
    return out


# ------------------------------------------------------------------ cinematica direta
def frames(p):
    Mw = {}
    root = Matrix.Translation(Vector((0.0, 0.0, 0.0))) @ _rot(*p.get("raiz", (0, 0, 0)))
    for (nome, pai, off) in OSSOS:
        if pai is None:
            M = root @ Matrix.Translation(Vector((0.0, 0.0, p["pz"])))
        else:
            M = Mw[pai] @ Matrix.Translation(Vector(off))
        ang = p.get(nome, (0, 0, 0))
        Mw[nome] = M @ _rot(*ang)
    return Mw


def _pt(M, v):
    return tuple(M @ Vector(v))


# ------------------------------------------------------------------ partes do corpo
def _limb(mb, M, length, r0, r1, c, n=6):
    with mb.at(M=M):
        mb.cyl((0, 0, 0.012), (0, 0, -length - 0.012), r0, c, n=n, r1=r1, smooth=False)


def _hull_local(mb, M, pts, c, **kw):
    with mb.at(M=M):
        mb.hull(pts, c, **kw)


def _ring(pts_center_M, r, c, mb, w=0.045, n=7, rz=0.0, sx=1.0, sy=1.0):
    """anel (fita) horizontal em torno do eixo Z local do frame."""
    M = pts_center_M
    ring = []
    for i in range(n):
        a = 2 * math.pi * i / n
        ring.append(_pt(M, (math.cos(a) * r * sx, math.sin(a) * r * sy, 0.0)))
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        mid = Vector(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2))
        ctr = M @ Vector((0, 0, 0))
        up = mid - ctr
        mb.strut(a, b, w, c, h=0.008, up=tuple(up.normalized()) if up.length > 1e-6 else (0, 0, 1))


def _strap(mb, pts, c, w=0.042, t=0.008, normal=(0, 1, 0)):
    for a, b in zip(pts[:-1], pts[1:]):
        mb.strut(a, b, w, c, h=t, up=normal)


# ------------------------------------------------------------------ itens de mao / carga
def item(mb, nome, M):
    """desenha o item no frame do punho (mao aponta para -Z local)."""
    with mb.at(M=M):
        if nome == "tablet":
            with mb.at((0.0, 0.07, -0.10), rx=90):
                mb.box((-0.13, -0.09, -0.006), (0.13, 0.09, 0.006), "preto_radio")
                mb.box((-0.12, -0.08, 0.006), (0.12, 0.08, 0.009), "e:tela_tablet_brilho")
        elif nome == "radio":
            mb.box((-0.03, -0.02, -0.16), (0.03, 0.025, -0.02), "preto_radio")
            mb.cyl((0.018, 0.0, -0.02), (0.018, 0.0, 0.10), 0.008, "preto_suave", n=5)
            mb.box((-0.02, 0.026, -0.10), (0.02, 0.028, -0.07), "e:verde_led")
        elif nome == "chave":
            mb.box((-0.012, -0.004, -0.26), (0.012, 0.004, -0.02), "cromado")
            mb.box((-0.03, -0.006, -0.30), (0.03, 0.006, -0.25), "cromado")
        elif nome == "chave_amarrada":
            mb.box((-0.012, -0.004, -0.26), (0.012, 0.004, -0.02), "cromado")
            mb.box((-0.03, -0.006, -0.30), (0.03, 0.006, -0.25), "cromado")
            mb.cyl((0.0, 0.0, -0.02), (0.0, 0.03, 0.12), 0.006, "amarelo_linha_vida", n=4)
        elif nome == "furadeira":
            mb.box((-0.03, -0.03, -0.14), (0.03, 0.03, -0.02), "amarelo_maquina")
            mb.box((-0.035, -0.03, -0.14), (0.035, 0.20, -0.07), "amarelo_maquina", top="preto_suave")
            mb.cyl((0.0, 0.20, -0.105), (0.0, 0.30, -0.105), 0.008, "cromado", n=5)
            mb.cyl((0.0, -0.02, -0.02), (0.0, -0.05, 0.10), 0.009, "preto_suave", n=4)
        elif nome == "tabua":
            mb.box((-0.06, -0.012, -0.5), (0.06, 0.012, 1.2), "madeira")
        elif nome == "bloco":
            mb.box((-0.07, -0.1, -0.2), (0.07, 0.1, 0.0), "bloco_ceramico")
        elif nome == "conector":
            mb.cyl((0.0, 0.0, -0.02), (0.0, 0.0, -0.13), 0.012, "cromado", n=5)
            mb.cyl((0.0, 0.03, -0.02), (0.0, 0.03, -0.13), 0.009, "cromado", n=5)
        elif nome == "cone":
            mb.cyl((0.0, 0.0, -0.05), (0.0, 0.0, -0.55), 0.03, "laranja_seguranca", n=6, r1=0.14)
        elif nome == "kit_resgate":
            mb.box((-0.15, -0.1, -0.45), (0.15, 0.1, -0.05), "vermelho_resgate", top="preto_suave")
        elif nome == "martelo":
            mb.box((-0.014, -0.005, -0.30), (0.014, 0.005, -0.02), "madeira")
            mb.box((-0.030, -0.024, -0.35), (0.030, 0.024, -0.29), "cromado")
            mb.box((-0.055, -0.012, -0.35), (-0.028, 0.012, -0.30), "cromado")
        elif nome == "vassoura":
            mb.cyl((0.0, 0.0, 0.22), (0.0, 0.22, -1.10), 0.016, "madeira", n=5)
            mb.box((-0.25, 0.16, -1.20), (0.25, 0.28, -1.08), "madeira_escura")
            for k in range(9):
                bx = -0.22 + k * 0.055
                mb.box((bx - 0.018, 0.17, -1.42), (bx + 0.018, 0.27, -1.19), "areia")
        elif nome == "pa":
            mb.cyl((0.0, 0.0, 0.20), (0.0, 0.20, -0.95), 0.016, "madeira", n=5)
            mb.box((-0.13, 0.14, -1.16), (0.13, 0.26, -0.93), "aco")
            mb.box((-0.13, 0.13, -1.20), (0.13, 0.27, -1.14), "cromado")
        elif nome == "rolo":
            mb.cyl((0.0, 0.0, -0.02), (0.0, 0.0, -0.34), 0.012, "madeira", n=5)
            mb.cyl((0.0, 0.0, -0.34), (0.0, 0.16, -0.34), 0.010, "cromado", n=4)
            mb.cyl((-0.11, 0.16, -0.34), (0.11, 0.16, -0.34), 0.035, "branco_gelo", n=8)
        elif nome == "prancheta":
            with mb.at((0.0, 0.06, -0.11), rx=90):
                mb.box((-0.12, -0.16, -0.008), (0.12, 0.16, 0.0), "madeira_escura")
                mb.box((-0.11, -0.15, 0.0), (0.11, 0.13, 0.004), "branco")
                mb.box((-0.05, 0.12, 0.004), (0.05, 0.16, 0.012), "cromado")
        elif nome == "serrote":
            mb.box((-0.022, -0.010, -0.20), (0.022, 0.010, -0.02), "madeira_escura")
            mb.box((-0.012, -0.004, -0.62), (0.012, 0.004, -0.19), "cromado")
            mb.box((-0.075, -0.003, -0.60), (0.075, 0.003, -0.21), "cromado")
        elif nome == "alicate":
            mb.cyl((0.0, 0.0, -0.02), (0.0, 0.0, -0.13), 0.014, "vermelho_resgate", n=5)
            mb.box((-0.012, -0.010, -0.24), (0.012, 0.010, -0.12), "cromado")
        elif nome == "garrafa_agua":
            mb.cyl((0.0, 0.0, -0.02), (0.0, 0.0, -0.22), 0.035, "g:agua", n=6)


def carga_ombro(mb, M_chest, tipo="tubos"):
    with mb.at(M=M_chest):
        if tipo == "tubos":
            for (dx, dz) in ((0.0, 0.0), (0.05, 0.0), (0.025, 0.04)):
                mb.cyl((0.16 + dx, -1.6, 0.22 + dz), (0.16 + dx, 2.2, 0.22 + dz), 0.022, "aco", n=6)
        elif tipo == "tabuas":
            for k in range(3):
                mb.box((0.10, -1.4, 0.20 + k * 0.03), (0.26, 2.0, 0.225 + k * 0.03), "madeira", sides="madeira_escura")
        elif tipo == "perfil":
            mb.box((0.12, -1.8, 0.2), (0.2, 2.4, 0.32), "grafite")


def carga_frente(mb, Mw, tipo="caixa"):
    a = Mw["wrist_R"] @ Vector((0, 0, -0.06))
    b = Mw["wrist_L"] @ Vector((0, 0, -0.06))
    c = (a + b) / 2
    if tipo == "caixa":
        mb.box((c.x - 0.22, c.y - 0.15, c.z - 0.18), (c.x + 0.22, c.y + 0.15, c.z + 0.12), "papelao")
    elif tipo == "blocos":
        mb.box((c.x - 0.2, c.y - 0.12, c.z - 0.12), (c.x + 0.2, c.y + 0.12, c.z + 0.12), "bloco_ceramico", top="argamassa")
    elif tipo == "tablet":
        with mb.at(M=Matrix.Translation(c + Vector((0.0, 0.03, 0.03))) @ _rot(50, 0, 0)):
            mb.box((-0.14, -0.10, -0.006), (0.14, 0.10, 0.006), "preto_radio")
            mb.box((-0.13, -0.09, 0.006), (0.13, 0.09, 0.009), "e:tela_tablet_brilho")
    elif tipo == "balde":
        mb.cyl((c.x, c.y, c.z - 0.3), (c.x, c.y, c.z - 0.02), 0.14, "preto_suave", n=8, r1=0.16)


# ------------------------------------------------------------------ construtor
def construir(papel="servente", p=None, pele=None, capacete=True, mao_R=None, mao_L=None, ombro=None, frente=None,
              cinturao=None, talabarte=None, talabarte_alvo=None, talabarte_folga=0.25, erro_cinturao=None,
              colete=None, radio_peito=None, variante_cor=None, partes=False):
    """MB do personagem (origem entre os pes). talabarte_alvo em coordenadas LOCAIS do personagem.

    partes=True devolve {peca: MB} em vez de um MB unico: o corpo sai em pecas rigidas
    articuladas (ja em repouso), para o jogo animar as juntas em tempo real."""
    R = dict(PAPEIS[papel])
    if variante_cor:
        R.update(variante_cor)
    if pele:
        R["pele"] = pele
    if colete is not None:
        R["colete"] = colete
    if cinturao is not None:
        R["cinturao"] = cinturao
    if talabarte is not None:
        R["talabarte"] = talabarte
    if radio_peito is not None:
        R["radio_peito"] = radio_peito
    if partes:
        p = repouso()          # a pose vem depois, girando as pecas no Three.js
    p = p or pose("em_pe")
    Mw = frames(p)
    MBS = dict((n, MB()) for n in PARTES) if partes else None
    mb = _Roteador(MBS) if partes else MB()

    def B(junta):
        """aponta o desenho para a peca dona daquela articulacao."""
        return mb._ir(PARTE_DE[junta]) if partes else mb

    camisa, calca, pel = R["camisa"], R["calca"], R["pele"]
    luva = R.get("luva") or pel
    bota = R.get("bota") or "bota_couro"

    # pelve e tronco
    _hull_local(B("pelvis"), Mw["pelvis"], [(-0.165, -0.10, -0.10), (0.165, -0.10, -0.10), (0.165, 0.10, -0.10), (-0.165, 0.10, -0.10),
                                   (-0.16, -0.095, 0.10), (0.16, -0.095, 0.10), (0.16, 0.095, 0.10), (-0.16, 0.095, 0.10)], calca)
    with B("pelvis").at(M=Mw["pelvis"]):
        mb.box((-0.168, -0.103, 0.045), (0.168, 0.103, 0.085), "grafite")
        mb.box((-0.03, 0.103, 0.048), (0.03, 0.108, 0.082), "cromado")
    _hull_local(B("spine"), Mw["spine"], [(-0.15, -0.095, -0.03), (0.15, -0.095, -0.03), (0.15, 0.095, -0.03), (-0.15, 0.095, -0.03),
                                  (-0.16, -0.10, 0.25), (0.16, -0.10, 0.25), (0.16, 0.10, 0.25), (-0.16, 0.10, 0.25)], camisa)
    _hull_local(B("chest"), Mw["chest"], [(-0.16, -0.10, -0.03), (0.16, -0.10, -0.03), (0.16, 0.105, -0.03), (-0.16, 0.105, -0.03),
                                  (-0.20, -0.105, 0.13), (0.20, -0.105, 0.13), (0.20, 0.11, 0.13), (-0.20, 0.11, 0.13),
                                  (-0.15, -0.085, 0.20), (0.15, -0.085, 0.20), (0.15, 0.085, 0.20), (-0.15, 0.085, 0.20)], camisa)
    if R.get("colete"):
        cv = R["colete"]
        _hull_local(mb, Mw["spine"], [(-0.162, -0.108, 0.02), (0.162, -0.108, 0.02), (0.162, 0.108, 0.02), (-0.162, 0.108, 0.02),
                                      (-0.172, -0.112, 0.26), (0.172, -0.112, 0.26), (0.172, 0.112, 0.26), (-0.172, 0.112, 0.26)], cv)
        _hull_local(mb, Mw["chest"], [(-0.172, -0.112, -0.03), (0.172, -0.112, -0.03), (0.172, 0.118, -0.03), (-0.172, 0.118, -0.03),
                                      (-0.205, -0.114, 0.12), (0.205, -0.114, 0.12), (0.205, 0.12, 0.12), (-0.205, 0.12, 0.12),
                                      (-0.12, -0.09, 0.205), (0.12, -0.09, 0.205), (0.12, 0.09, 0.205), (-0.12, 0.09, 0.205)], cv)
        with B("spine").at(M=Mw["spine"]):
            mb.box((-0.176, -0.116, 0.13), (0.176, 0.116, 0.16), "refletivo")
        with B("chest").at(M=Mw["chest"]):
            mb.box((-0.19, -0.118, 0.04), (0.19, 0.122, 0.07), "refletivo")
    # pescoco e cabeca
    _limb(B("neck"), Mw["neck"] @ _rot(180, 0, 0), 0.07, 0.052, 0.048, pel)
    _hull_local(B("head"), Mw["head"], [(-0.085, -0.09, 0.0), (0.085, -0.09, 0.0), (0.085, 0.10, 0.0), (-0.085, 0.10, 0.0),
                                 (-0.095, -0.10, 0.12), (0.095, -0.10, 0.12), (0.095, 0.11, 0.12), (-0.095, 0.11, 0.12),
                                 (-0.08, -0.085, 0.23), (0.08, -0.085, 0.23), (0.08, 0.09, 0.23), (-0.08, 0.09, 0.23)], pel)
    with B("head").at(M=Mw["head"]):
        mb.box((-0.016, 0.105, 0.085), (0.016, 0.135, 0.13), pel)                  # nariz
        for sx in (-1, 1):
            mb.box((sx * 0.042 - 0.014, 0.108, 0.13), (sx * 0.042 + 0.014, 0.113, 0.145), "preto_suave")  # olhos
            mb.box((sx * 0.097 - 0.008, -0.02, 0.08), (sx * 0.097 + 0.008, 0.03, 0.14), pel)                # orelhas
        mb.box((-0.04, 0.109, 0.05), (0.04, 0.112, 0.06), "cabelo_escuro" if R.get("cabelo") else "corte_fita")  # boca
    if R.get("capacete") and capacete:
        with B("head").at(M=Mw["head"] @ Matrix.Translation(Vector((0, 0.005, 0.165)))):
            mb.lathe([(0.128, 0.0), (0.126, 0.05), (0.108, 0.10), (0.07, 0.135), (0.01, 0.15)], R["capacete"], n=10, cap0=True, cap1=False)
            mb.box((-0.10, 0.11, -0.005), (0.10, 0.19, 0.012), R["capacete"])      # aba
            mb.box((-0.01, -0.09, 0.118), (0.01, 0.10, 0.156), R["capacete"])      # nervura
            mb.box((-0.13, -0.02, -0.07), (-0.125, 0.01, 0.0), "preto_suave")      # jugular
            mb.box((0.125, -0.02, -0.07), (0.13, 0.01, 0.0), "preto_suave")
    elif R.get("cabelo") or not capacete:
        _hull_local(mb, Mw["head"], [(-0.09, -0.10, 0.16), (0.09, -0.10, 0.16), (0.09, 0.09, 0.19), (-0.09, 0.09, 0.19),
                                     (-0.07, -0.08, 0.25), (0.07, -0.08, 0.25), (0.07, 0.06, 0.25), (-0.07, 0.06, 0.25)], "cabelo_escuro")
    # bracos
    for s in ("R", "L"):
        _limb(B("shoulder_" + s), Mw["shoulder_" + s], 0.29, 0.058, 0.048, camisa)
        _limb(B("elbow_" + s), Mw["elbow_" + s], 0.255, 0.047, 0.038, camisa)
        with B("wrist_" + s).at(M=Mw["wrist_" + s]):
            mb.box((-0.034, -0.045, -0.11), (0.034, 0.045, 0.005), luva)
            sx = -1 if s == "R" else 1
            mb.box((sx * 0.034 - 0.012, 0.0, -0.08), (sx * 0.034 + 0.012, 0.05, -0.02), luva)
        with B("shoulder_" + s).at(M=Mw["shoulder_" + s]):
            r = 0.062
            mb.hull([(r, 0, 0), (-r, 0, 0), (0, r, 0), (0, -r, 0), (0, 0, r), (0, 0, -r)], camisa)
    # pernas
    for s in ("R", "L"):
        _limb(B("hip_" + s), Mw["hip_" + s], 0.43, 0.072, 0.056, calca)
        _limb(B("knee_" + s), Mw["knee_" + s], 0.40, 0.056, 0.046, calca)
        with B("ankle_" + s).at(M=Mw["ankle_" + s]):
            mb.box((-0.056, -0.075, -0.052), (0.056, 0.19, 0.09), bota, top=bota)
            mb.box((-0.058, -0.078, -0.06), (0.058, 0.195, -0.045), "preto_suave")
    # radio no peito
    if R.get("radio_peito"):
        with B("chest").at(M=Mw["chest"]):
            mb.box((0.07, 0.115, 0.02), (0.12, 0.14, 0.13), "preto_radio")
            mb.cyl((0.11, 0.128, 0.13), (0.11, 0.128, 0.22), 0.006, "preto_suave", n=4)

    # cinturao tipo paraquedista
    if R.get("cinturao"):
        cc = R["cinturao"]
        ch, sp, pv = Mw["chest"], Mw["spine"], Mw["pelvis"]
        frouxo = erro_cinturao == "ajuste_frouxo"
        invertido = erro_cinturao == "colocado_invertido"
        fy = -1.0 if invertido else 1.0      # frente do cinturao
        for sx in (-1, 1):
            front = [_pt(pv, (sx * 0.09, fy * 0.11, 0.02)), _pt(sp, (sx * 0.10, fy * 0.118, 0.15)), _pt(ch, (sx * 0.11, fy * 0.125, 0.10)),
                     _pt(ch, (sx * 0.12, fy * 0.10, 0.19)), _pt(ch, (sx * 0.10, 0.0, 0.215))]
            back = [_pt(ch, (sx * 0.10, 0.0, 0.215)), _pt(ch, (sx * 0.08, -fy * 0.10, 0.19)), _pt(ch, (sx * 0.04, -fy * 0.12, 0.10)),
                    _pt(sp, (sx * 0.02, -fy * 0.115, 0.05)), _pt(pv, (sx * 0.05, -fy * 0.11, -0.02))]
            if frouxo:
                front = [(a[0] * 1.06, a[1] * 1.06, a[2]) for a in front]
            _strap(B("chest"), front, cc, normal=(0, fy, 0))
            _strap(B("chest"), back, cc, normal=(0, -fy, 0))
        # peitoral (fivela)
        if erro_cinturao == "fivela_aberta":
            for sx in (-1, 1):
                a = _pt(ch, (sx * 0.11, fy * 0.13, 0.08))
                b = _pt(ch, (sx * 0.035, fy * 0.135, 0.07))
                c = _pt(ch, (sx * 0.03, fy * 0.14, -0.10))
                _strap(B("chest"), [a, b, c], cc, w=0.035, normal=(0, fy, 0))
                with B("chest").at(M=ch):
                    mb.box((sx * 0.03 - 0.02, fy * 0.13, -0.13), (sx * 0.03 + 0.02, fy * 0.15, -0.09), "cromado")
        else:
            _strap(B("chest"), [_pt(ch, (-0.11, fy * 0.13, 0.08)), _pt(ch, (0.11, fy * 0.13, 0.08))], cc, w=0.035)
            with B("chest").at(M=ch):
                mb.box((-0.03, fy * 0.13 - 0.01, 0.06), (0.03, fy * 0.13 + 0.012, 0.10), "cromado")
        # argola dorsal
        with B("chest").at(M=ch):
            yb = -fy * 0.125
            mb.box((-0.03, yb - 0.01 * fy, 0.10), (0.03, yb + 0.005 * fy, 0.16), "grafite")
            mb.box((-0.02, yb - 0.02 * fy, 0.145), (0.02, yb - 0.005 * fy, 0.17), "cromado")
        # cinto abdominal e perneiras
        _ring(pv @ Matrix.Translation(Vector((0, 0, 0.065))), 0.17, cc, B("pelvis"), w=0.05, n=8, sy=0.66)
        for s in ("R", "L"):
            hz = -0.16 if frouxo else -0.09
            rr = 0.105 if frouxo else 0.080
            Mh = Mw["hip_" + s] @ Matrix.Translation(Vector((0, 0.0, hz)))
            _ring(Mh, rr, cc, B("hip_" + s), w=0.042, n=7)
            if erro_cinturao == "fita_torcida" and s == "R":
                a = _pt(Mh, (rr + 0.012, -0.03, 0.03))
                b = _pt(Mh, (rr + 0.012, 0.03, -0.03))
                c2 = _pt(Mh, (rr + 0.012, -0.03, -0.03))
                d = _pt(Mh, (rr + 0.012, 0.03, 0.03))
                B("hip_R").strut(a, b, 0.03, "fita_cinturao_azul", h=0.01, up=(1, 0, 0))
                B("hip_R").strut(c2, d, 0.03, "preto_suave", h=0.01, up=(1, 0, 0))
        if erro_cinturao == "corte_rompendo":
            p0 = _pt(ch, (0.115, 0.118, 0.17))
            B("chest").strut(p0, _pt(ch, (0.12, 0.13, 0.08)), 0.056, "corte_fita", h=0.016, up=(0, 1, 0))
            B("chest").strut(_pt(ch, (0.08, 0.136, 0.125)), _pt(ch, (0.16, 0.136, 0.125)), 0.02, "vermelho_seguranca", h=0.01, up=(0, 1, 0))
            for k in range(8):
                B("chest").strut(_pt(ch, (0.09 + k * 0.009, 0.13, 0.13)), _pt(ch, (0.08 + k * 0.012, 0.19, 0.10 - k * 0.008)), 0.005, "fita_desgastada", h=0.005)

    # talabarte duplo em Y com absorvedor
    if R.get("talabarte") and talabarte is not False:
        ch = Mw["chest"]
        fy = -1.0 if erro_cinturao == "colocado_invertido" else 1.0
        d_ring = Vector(_pt(ch, (0.0, -fy * 0.15, 0.16)))
        absorb = Vector(_pt(ch, (0.0, -fy * 0.19, 0.02)))
        B("chest").strut(tuple(d_ring), tuple(absorb), 0.06, "preto_radio", h=0.045)
        B("chest").box((absorb.x - 0.035, absorb.y - 0.03, absorb.z - 0.12), (absorb.x + 0.035, absorb.y + 0.03, absorb.z + 0.01), "amarelo_escuro", top="preto_radio")
        base = absorb + Vector((0, 0, -0.12))
        if talabarte_alvo is not None:
            alvo = Vector(talabarte_alvo)
            for k, off in enumerate((-0.035, 0.035)):
                a = base
                b = alvo + Vector((off, 0, -0.02 * k))
                mid = (a + b) / 2 + Vector((0, 0, -talabarte_folga))
                cor = "fita_desgastada" if (erro_cinturao == "talabarte_desfiando" and k == 0) else "laranja_escuro"
                _strap(B("chest"), [tuple(a), tuple(mid), tuple(b)], cor, w=0.03, t=0.012, normal=(0, 0, 1))
                if erro_cinturao == "talabarte_desfiando" and k == 0:
                    for j in range(6):
                        q = (a + mid) / 2 + Vector((0.01 * j - 0.03, 0.0, 0.01 * j))
                        B("chest").strut(tuple(q), tuple(q + Vector((0.03, 0.05, -0.04))), 0.004, "fita_desgastada", h=0.004)
                B("chest").box((b.x - 0.02, b.y - 0.02, b.z - 0.07), (b.x + 0.02, b.y + 0.02, b.z + 0.01), "cromado")
        else:
            # ganchos estacionados no peitoral
            for sx in (-1, 1):
                hook = Vector(_pt(ch, (sx * 0.14, fy * 0.14, 0.0)))
                mid = Vector(_pt(Mw["spine"], (sx * 0.19, 0.0, 0.05)))
                _strap(B("chest"), [tuple(base), tuple(mid), tuple(hook)], "laranja_escuro", w=0.03, t=0.012, normal=(sx, 0, 0))
                B("chest").box((hook.x - 0.02, hook.y - 0.015, hook.z - 0.06), (hook.x + 0.02, hook.y + 0.015, hook.z + 0.01), "cromado")

    # itens
    if mao_R:
        item(B("wrist_R"), mao_R, Mw["wrist_R"])
    if mao_L:
        item(B("wrist_L"), mao_L, Mw["wrist_L"])
    if ombro:
        carga_ombro(B("chest"), Mw["chest"], ombro)
    if frente:
        carga_frente(B("chest"), Mw, frente)
    if not partes:
        return mb
    # leva os vertices de cada peca para o espaco local da sua articulacao
    for nome in PARTES:
        m = MBS[nome]
        if not m.F:
            continue
        inv = Mw[ANCORA[nome]].inverted()
        m.V[:] = [tuple(inv @ Vector(v)) for v in m.V]
    return MBS


def rz_para(origem, alvo):
    dx, dy = alvo[0] - origem[0], alvo[1] - origem[1]
    return math.degrees(math.atan2(-dx, dy))


def local_de(loc, rz, ponto):
    """converte ponto do mundo para o espaco local do personagem (origem loc, rotacao rz)."""
    a = math.radians(rz)
    dx, dy, dz = ponto[0] - loc[0], ponto[1] - loc[1], ponto[2] - loc[2]
    ca, sa = math.cos(-a), math.sin(-a)
    return (dx * ca - dy * sa, dx * sa + dy * ca, dz)


def criar(nome, C, loc, rz=0.0, papel="servente", pose_nome="em_pe", pose_aj=None, parent=None, props=None, **kw):
    p = pose(pose_nome, **(pose_aj or {}))
    if kw.get("talabarte_alvo_mundo") is not None:
        kw["talabarte_alvo"] = local_de(loc, rz, kw.pop("talabarte_alvo_mundo"))
    else:
        kw.pop("talabarte_alvo_mundo", None)
    mb = construir(papel, p, **kw)
    pr = {"categoria": "personagem", "papel": papel, "pose": pose_nome}
    if props:
        pr.update(props)
    return K.finish(mb, nome, C, parent=parent, loc=loc, rz=rz, props=pr)



def angulos_parte(p):
    """angulos (em radianos) de cada peca, a partir de uma pose do esqueleto."""
    def g(j):
        return p.get(j, (0.0, 0.0, 0.0))

    def soma(*js):
        return tuple(math.radians(sum(g(j)[k] for j in js)) for k in range(3))

    return {"Quadril": soma("pelvis"), "Torso": soma("spine", "chest"), "Cabeca": soma("neck", "head"),
            "Braco_R": soma("shoulder_R"), "Antebraco_R": soma("elbow_R"),
            "Braco_L": soma("shoulder_L"), "Antebraco_L": soma("elbow_L"),
            "Coxa_R": soma("hip_R"), "Canela_R": soma("knee_R"),
            "Coxa_L": soma("hip_L"), "Canela_L": soma("knee_L")}


def criar_partes(nome, C, loc, rz=0.0, papel="servente", pose_nome="em_pe", pose_aj=None,
                 parent=None, props=None, **kw):
    """cria o personagem como arvore de pecas rigidas, pronta para animar em tempo real.

    A pose inicial e aplicada girando cada peca, entao no Blender ele continua posado -
    e no Three.js basta continuar girando as mesmas pecas."""
    # o talabarte ancorado e feito no jogo (corda dinamica entre o peito e o ponto):
    # aqui so guardamos onde ele esta preso.
    alvo_mundo = kw.pop("talabarte_alvo_mundo", None)
    alvo_local = kw.pop("talabarte_alvo", None)
    MBS = construir(papel, partes=True, **kw)
    off = offsets_repouso()
    p = pose(pose_nome, **(pose_aj or {}))
    ang = angulos_parte(p)
    pr = {"categoria": "personagem", "papel": papel, "pose": pose_nome,
          "articulado": True, "pecas": PARTES}
    if alvo_mundo is not None:
        pr["conectado_em"] = [round(float(v), 4) for v in alvo_mundo]
    elif alvo_local is not None:
        a = math.radians(rz)
        ca, sa = math.cos(a), math.sin(a)
        pr["conectado_em"] = [round(loc[0] + alvo_local[0] * ca - alvo_local[1] * sa, 4),
                              round(loc[1] + alvo_local[0] * sa + alvo_local[1] * ca, 4),
                              round(loc[2] + alvo_local[2], 4)]
    if props:
        pr.update(props)
    raiz = K.empty(nome, C, loc, size=0.22, kind='PLAIN_AXES', props=pr)
    raiz.rotation_euler = (0.0, 0.0, math.radians(rz))
    if parent is not None:
        raiz.parent = parent
    objs = {}
    for parte in PARTES:
        m = MBS[parte]
        if not m.F:
            continue
        pai = PAI_PARTE[parte]
        alvo = objs.get(pai) if pai else None
        d = off[parte]
        if parte == "Quadril":
            d = Vector((d.x, d.y, p.get("pz", 0.93)))
        o = K.finish(m, nome + "_" + parte, C, parent=(alvo or raiz), loc=tuple(d),
                     props={"peca": parte, "personagem": nome})
        if o is None:
            continue
        o.rotation_euler = ang[parte]
        o.matrix_parent_inverse = Matrix.Identity(4)
        objs[parte] = o
    return raiz


# ------------------------------------------------------------------ maos em 1a pessoa (espaco da camera: -Z frente, +Y cima, +X direita)
# Geometria explicita cotovelo -> punho -> mao. Proporcoes de adulto:
# antebraco ~0.26 m, mao ~0.19 m, punho ~0.055 m de raio de manga.
_POSES_1P = {
    # (cotovelo, mao) por lado + direcao para onde o item segurado aponta.
    # A lente de 1a pessoa tem 20 mm (FOV horizontal ~84 graus => vertical ~54 graus):
    # a borda inferior do quadro fica em y = -0.507 * profundidade. As maos ficam
    # logo acima dessa borda (~80% da altura do quadro) e os cotovelos, bem abaixo,
    # entram pelos cantos inferiores.
    "baixo": dict(
        R=((0.340, -0.500, -0.240), (0.255, -0.250, -0.620)),
        L=((-0.340, -0.510, -0.240), (-0.255, -0.258, -0.625)),
        aim_R=(0.05, -0.45, -1.0), aim_L=(-0.05, -0.45, -1.0)),
    "tablet": dict(
        R=((0.360, -0.500, -0.200), (0.200, -0.178, -0.436)),
        L=((-0.360, -0.500, -0.200), (-0.200, -0.182, -0.440)),
        aim_R=(0.55, -0.25, -1.0), aim_L=(-0.55, -0.25, -1.0)),
    "radio": dict(
        R=((0.340, -0.460, -0.180), (0.160, -0.172, -0.380)),
        aim_R=(0.0, -0.35, -0.94)),
    "chave": dict(
        R=((0.310, -0.460, -0.270), (0.130, -0.262, -0.600)),
        L=((-0.320, -0.470, -0.270), (-0.175, -0.280, -0.615)),
        aim_R=(0.10, -0.30, -0.95), aim_L=(-0.10, -0.32, -0.94)),
    "conector": dict(
        R=((0.320, -0.460, -0.260), (0.150, -0.244, -0.580)),
        aim_R=(0.0, -0.20, -0.98)),
}


def _quadro_1p(origem, aim, roll=0.0):
    """matriz cujo -Z local aponta para aim (mao/item apontam para -Z)."""
    d = Vector(aim)
    if d.length < 1e-6:
        d = Vector((0.0, 0.0, -1.0))
    M = Matrix.Translation(Vector(origem)) @ d.normalized().to_track_quat('-Z', 'Y').to_matrix().to_4x4()
    if roll:
        M = M @ _rot(0, 0, roll)
    return M


def _braco_1p(mb, cotovelo, mao, luva, manga, lado="R"):
    """antebraco (manga) + mao fechada; devolve o quadro do punho (-Z = dedos)."""
    c, m = Vector(cotovelo), Vector(mao)
    d = m - c
    if d.length < 1e-5:
        return None
    u = d.normalized()
    punho = m - u * 0.075
    # antebraco: afunila do cotovelo (0.052) ate o punho (0.036)
    mb.cyl(tuple(c), tuple(punho), 0.052, manga, n=6, r1=0.036, smooth=False)
    # punho de couro da luva
    mb.cyl(tuple(punho - u * 0.015), tuple(punho + u * 0.035), 0.038, luva, n=6, smooth=False)
    M = Matrix.Translation(punho) @ u.to_track_quat('-Z', 'Y').to_matrix().to_4x4()
    s = 1.0 if lado == "R" else -1.0
    with mb.at(M=M):
        # palma + dedos fechados (mao ~0.175 m do punho a ponta)
        mb.box((-0.040, -0.028, -0.135), (0.040, 0.030, -0.005), luva)
        # polegar por dentro
        mb.box((0.030 * s - 0.020, -0.010, -0.095), (0.030 * s + 0.020, 0.034, -0.030), luva)
    return M


def maos_1p(item_R=None, item_L=None, luva="luva_cinza", manga="uniforme_azul", pose_1p="baixo"):
    """maos do jogador vistas em 1a pessoa, no espaco local da camera."""
    mb = MB()
    cfg = _POSES_1P[pose_1p]
    for lado in ("R", "L"):
        braco = cfg.get(lado)
        if not braco:
            continue
        cot, mao = braco
        M = _braco_1p(mb, cot, mao, luva, manga, lado)
        it = item_R if lado == "R" else item_L
        if it and M:
            aim = cfg.get("aim_" + lado) or (0.0, -0.3, -1.0)
            item(mb, it, _quadro_1p(mao, aim))
    return mb
