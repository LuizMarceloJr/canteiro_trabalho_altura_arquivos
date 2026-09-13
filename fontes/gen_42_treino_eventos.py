# -*- coding: utf-8 -*-
# gen_42_treino_eventos.py - props dos eventos inesperados (EV01-EV17), cena principal (queda da chave),
# consequencias (CONSEQ_), organizacao final (ORG_) e emergencia final (EMERG_). Tudo oculto no estado inicial,
# exceto o que ja existe no ambiente antes do evento (ex.: origem do EV03).
import bpy, sys, math, random
from mathutils import Vector

K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
G40 = sys.modules["gen_40"]

Z4, Z5 = L.TA_Z(4), L.TA_Z(5)
PAI = "42_Treino_Eventos_Consequencias"


def build():
    K.coll(PAI)
    subs = {n: K.coll(n, PAI) for n in ("42a_Eventos_Pav04", "42b_Cena_Principal_Queda_Chave", "42c_Consequencias", "42d_Organizacao_Final",
                                        "42e_Emergencia_Final")}
    K.clear_coll(PAI)
    obj = G40.obj
    C = subs["42a_Eventos_Pav04"]

    # EV01 - material longo que o colega quer passar para o andaime
    mb = MB()
    for k in range(5):
        y = 5.55 + (k % 3) * 0.06
        mb.cyl((21.9, y + k * 0.05, Z4 + 0.03 + (k // 3) * 0.05), (25.9, y + k * 0.05, Z4 + 0.03 + (k // 3) * 0.05), 0.024, "aco", n=6)
    obj(mb, "EV01_Material_Longo_Tubos", C, visivel=False, cena="EV01", props={"evento": "EVENTO_GUARDA_CORPO_REMOVIDO"})

    # EV02 - pequena peca escapa e congela antes de atingir o nivel inferior
    mb = MB()
    with mb.at((29.8, 3.55, 5.2), rx=35, rz=20):
        mb.cyl((0, 0, -0.03), (0, 0, 0.03), 0.012, "cromado", n=6, smooth=False)
        mb.cyl((0, 0, 0.03), (0, 0, 0.045), 0.02, "cromado", n=6, smooth=False)
    for k in range(6):
        mb.box((29.78 - 0.003, 3.55 - 0.003, 5.35 + k * 0.35), (29.78 + 0.003, 3.55 + 0.003, 5.5 + k * 0.35), "branco_sinal")
    obj(mb, "EV02_Peca_Escapa_Congelada", C, visivel=False, cena="EV02", props={"evento": "EVENTO_INVASAO_AREA_ISOLADA", "congelar": True})

    # EV03 - origem (blocos junto a borda do pav 5, acima do rodape) e objetos
    mb = MB()
    for k in range(3):
        for j in range(2):
            mb.box((29.6 + j * 0.42, 4.2, Z5 + k * 0.2), (29.99 + j * 0.42, 4.39, Z5 + k * 0.2 + 0.19), "bloco_ceramico", top="argamassa")
    mb.box((30.7, 4.22, Z5 + 0.6), (30.9, 4.37, Z5 + 0.72), "bloco_ceramico")
    obj(mb, "EV03_Origem_Blocos_Junto_Borda_Pav05", C, visivel=True, cena="EV03", props={"evento": "EVENTO_OBJETO_SUPERIOR",
        "nota": "condicao existente no pav 5 que explica a queda (visivel ao olhar para cima)"})
    mb = MB()
    mb.hull([(29.05, 4.35, Z4), (29.22, 4.38, Z4), (29.2, 4.52, Z4), (29.02, 4.5, Z4), (29.1, 4.44, Z4 + 0.09), (29.18, 4.46, Z4 + 0.08)], "bloco_ceramico")
    for k in range(7):
        a = random.Random(k).uniform(0, 6.28)
        r = 0.12 + 0.05 * k
        mb.box((29.1 + r * math.cos(a), 4.6 + abs(r * math.sin(a)), Z4), (29.13 + r * math.cos(a), 4.63 + abs(r * math.sin(a)), Z4 + 0.02), "bloco_ceramico")
    obj(mb, "EV03_Objeto_01_Impacto_Proximo", C, visivel=False, cena="EV03", props={"evento": "EVENTO_OBJETO_SUPERIOR", "som": "CLANG"})
    mb = MB()
    with mb.at((30.55, 3.9, Z4 + 1.75), rx=25, ry=40):
        mb.hull([(-0.08, -0.05, -0.05), (0.08, -0.05, -0.05), (0.08, 0.05, -0.04), (-0.07, 0.06, -0.05),
                 (-0.05, -0.03, 0.06), (0.06, -0.02, 0.05), (0.05, 0.04, 0.06)], "bloco_ceramico")
    for k in range(5):
        mb.box((30.55 - 0.003, 3.9 - 0.003, Z4 + 1.9 + k * 0.3), (30.55 + 0.003, 3.9 + 0.003, Z4 + 2.05 + k * 0.3), "branco_sinal")
    obj(mb, "EV03_Objeto_02_Congelado_Mais_Proximo", C, visivel=False, cena="EV03", props={"evento": "EVENTO_OBJETO_SUPERIOR", "congelar": True})

    # EV04 - paleteira com palete de blocos (inicio distante e aproximando da area)
    def paleteira(mb, x, y, rz):
        with mb.at((x, y, Z4), rz=rz):
            mb.box((-0.55, -0.55, 0.0), (0.55, 0.55, 0.14), "pallet")
            mb.box((-0.5, -0.5, 0.14), (0.5, 0.5, 1.0), "filme_plastico", top="bloco_ceramico")
            for sx in (-0.2, 0.2):
                mb.box((sx - 0.08, -0.55, 0.04), (sx + 0.08, 0.7, 0.09), "vermelho_escuro")
            mb.box((-0.25, 0.62, 0.0), (0.25, 0.78, 0.35), "vermelho_escuro")
            mb.cyl((0.0, 0.7, 0.35), (0.0, 1.05, 1.15), 0.025, "grafite", n=6)
            mb.box((-0.18, 1.02, 1.12), (0.18, 1.1, 1.18), "preto_suave")
            for sx in (-0.2, 0.2):
                mb.cyl((sx - 0.03, -0.45, 0.04), (sx + 0.03, -0.45, 0.04), 0.04, "borracha", n=6)
    mb = MB()
    paleteira(mb, 21.2, 12.75, 90.0)
    obj(mb, "EV04_Paleteira_Palete_Inicio", C, visivel=False, cena="EV04", props={"evento": "EVENTO_MOVIMENTACAO_CARGA", "radio": "Vamos fazer uma movimentacao aqui do lado."})
    mb = MB()
    paleteira(mb, 28.0, 7.35, 180.0)
    obj(mb, "EV04_Paleteira_Palete_Aproximando", C, visivel=False, cena="EV04", props={"evento": "EVENTO_MOVIMENTACAO_CARGA", "congelar": True})

    # EV08 - cabo e mangueira deixados na rota de saida
    mb = MB()
    pts = [(24.2, 11.6, Z4 + 0.02), (24.5, 12.3, Z4 + 0.02), (24.35, 13.1, Z4 + 0.02), (24.7, 13.9, Z4 + 0.02), (24.4, 14.6, Z4 + 0.02)]
    for a, b in zip(pts[:-1], pts[1:]):
        mb.cyl(a, b, 0.012, "laranja_seguranca", n=5, caps=False, smooth=False)
    pts = [(25.2, 11.4, Z4 + 0.025), (24.9, 12.2, Z4 + 0.025), (25.4, 12.9, Z4 + 0.025), (25.0, 13.8, Z4 + 0.025)]
    for a, b in zip(pts[:-1], pts[1:]):
        mb.cyl(a, b, 0.022, "verde_seguranca", n=6, caps=False, smooth=False)
    mb.box((23.6, 12.2, Z4), (24.0, 13.4, Z4 + 0.04), "madeira")
    obj(mb, "EV08_Cabo_Mangueira_Na_Rota_Saida", C, visivel=False, cena="EV08", props={"evento": "EVENTO_OBSTACULO_NOVO"})

    # EV12 - fragmento retido pelo rodape/tela (quase acidente sem culpa do jogador)
    mb = MB()
    mb.hull([(25.0, 4.12, Z4 + 0.0), (25.14, 4.12, Z4 + 0.0), (25.12, 4.24, Z4 + 0.0), (24.98, 4.22, Z4 + 0.0), (25.05, 4.14, Z4 + 0.09), (25.1, 4.18, Z4 + 0.07)], "bloco_ceramico")
    for k in range(5):
        mb.box((24.7 + k * 0.1, 4.2 + (k % 2) * 0.08, Z4), (24.72 + k * 0.1, 4.22 + (k % 2) * 0.08, Z4 + 0.015), "argamassa")
    obj(mb, "EV12_Fragmento_Retido_Pelo_Rodape", C, visivel=False, cena="EV12", props={"evento": "EVENTO_QUASE_ACIDENTE_EXTERNO"})

    # EV14 - ferramenta eletrica com cabo danificado
    mb = MB()
    G40.furadeira(mb, (29.55, 5.75, Z4 + 0.02), rz=-40.0, cabo_danificado=True)
    obj(mb, "EV14_Ferramenta_Eletrica_Cabo_Danificado", C, visivel=False, cena="EV14", props={"evento": "EVENTO_FERRAMENTA_DEFEITUOSA",
        "defeitos_possiveis": "vibracao anormal, cabo danificado, funcionamento intermitente, peca solta"})

    # EV15 - objeto que atinge a protecao
    mb = MB()
    mb.cyl((24.4, 4.75, Z4 + 0.03), (26.3, 5.6, Z4 + 0.03), 0.024, "aco", n=6)
    obj(mb, "EV15_Tubo_Que_Atingiu_Protecao", C, visivel=False, cena="EV15", props={"evento": "EVENTO_IMPACTO_PROTECAO", "som": "CLANG"})

    # EV16 - chuva: piso molhado
    mb = MB()
    rnd = random.Random(16)
    for k in range(18):
        cx, cy = rnd.uniform(24.0, 31.3), rnd.uniform(4.3, 8.5)
        r = rnd.uniform(0.15, 0.55)
        pts = [(cx + r * math.cos(a) * rnd.uniform(0.7, 1.2), cy + r * 0.7 * math.sin(a) * rnd.uniform(0.7, 1.2), Z4 + 0.004) for a in [2 * math.pi * j / 8 for j in range(8)]]
        mb.poly(pts, "concreto_molhado")
    obj(mb, "EV16_Piso_Molhado_Chuva", C, visivel=False, cena="EV16", props={"evento": "EVENTO_CHUVA",
        "nota": "nao ensinar 'choveu = proibido': verificar o que foi definido; se nao for seguro/previsto, parar e comunicar"})

    # ============================================ cena principal: a chave escapa
    C = subs["42b_Cena_Principal_Queda_Chave"]
    mb = MB()
    G40.chave_boca(mb, (30.32, 4.26, Z4 + 0.46), rz=-18.0, rx=42.0)
    for k in range(4):
        mb.box((30.24 + k * 0.012, 4.44 + k * 0.10, Z4 + 0.60 + k * 0.055),
               (30.30 + k * 0.012, 4.46 + k * 0.10, Z4 + 0.615 + k * 0.055), "branco_sinal")
    obj(mb, "PRINC_Chave_Escapando_1P", C, visivel=False, cena="PRINC", props={
        "momento": "a chave escapa da mao (visao em 1a pessoa)", "camera": "CAM_1P_PRINC_Chave_Escapa",
        "nota": "rastro branco = movimento; substituir por animacao no Three.js"})
    mb = MB()
    G40.chave_boca(mb, (30.3, 3.86, Z4 + 0.55), rz=0.0, rx=80.0)
    mb.cyl((30.34, 3.9, Z4 + 0.72), (30.35, 4.35, Z4 + 0.95), 0.005, "amarelo_linha_vida", n=4)
    mb.cyl((30.35, 4.35, Z4 + 0.95), (30.45, 4.9, Z4 + 0.72), 0.005, "amarelo_linha_vida", n=4)
    obj(mb, "PRINC_Chave_Retida_Pelo_Cordao", C, visivel=False, cena="PRINC", props={"condicao": "FERRAMENTAS_PROTEGIDAS=SIM"})
    mb = MB()
    G40.chave_boca(mb, (29.95, 2.1, 0.01), rz=-35.0)
    obj(mb, "PRINC_Chave_Caida_Dentro_Area_Isolada", C, visivel=False, cena="PRINC", props={"condicao": "FERRAMENTAS_PROTEGIDAS=NAO e AREA_INFERIOR_ISOLADA=SIM"})
    mb = MB()
    G40.chave_boca(mb, (30.35, 2.55, 2.55), rz=25.0, rx=60.0)
    for k in range(7):
        mb.box((30.35 - 0.003, 2.55 - 0.003, 2.8 + k * 0.35), (30.35 + 0.003, 2.55 + 0.003, 2.95 + k * 0.35), "branco_sinal")
    obj(mb, "PRINC_Chave_Caindo_Congelada_Sobre_Pessoa", C, visivel=False, cena="PRINC", props={"condicao": "FERRAMENTAS_PROTEGIDAS=NAO e AREA_INFERIOR_ISOLADA=NAO",
        "congelar": True, "tela": "AREA ABAIXO NAO ISOLADA + FERRAMENTA SEM PROTECAO = PESSOA EXPOSTA"})

    # ============================================ consequencias
    C = subs["42c_Consequencias"]
    mb = MB()
    with mb.at((28.05, 3.6, 7.2), rx=65, rz=15):
        mb.box((-0.03, -0.0125, -0.45), (0.03, 0.0125, 0.45), "madeira")
    for k in range(6):
        mb.box((28.05 - 0.003, 3.6 - 0.003, 7.8 + k * 0.4), (28.05 + 0.003, 3.6 + 0.003, 7.95 + k * 0.4), "branco_sinal")
    obj(mb, "CONSEQ_Material_Solto_Caindo_Congelado", C, visivel=False, cena="CONSEQ", props={"consequencia": "MATERIAL_SOLTO=SIM", "congelar": True,
        "oculta": "C15_Madeira_Solta_Junto_Borda"})
    mb = MB()
    mb.box((28.2, 1.3, 0.0), (28.26, 2.2, 0.025), "madeira")
    obj(mb, "CONSEQ_Material_Solto_No_Chao", C, visivel=False, cena="CONSEQ", props={"consequencia": "MATERIAL_SOLTO=SIM e AREA_INFERIOR_ISOLADA=SIM"})

    # ponto escolhido cedendo (CONEXAO_INCORRETA)
    mb = MB()
    px_, py_ = 31.72, 4.75
    mb.cyl((px_, py_, Z4), (px_ - 0.02, py_, Z4 + 1.1), 0.038, "aco", n=8)
    mb.cyl((px_ - 0.02, py_, Z4 + 1.1), (px_ - 0.35, py_ - 0.05, Z4 + 1.62), 0.038, "aco", n=8)
    mb.cyl((px_ - 0.35, py_ - 0.05, Z4 + 1.62), (px_, py_, L.TA_Z(5) - 0.5), 0.038, "aco", n=8)
    mb.box((px_ - 0.12, py_ - 0.06, Z4 + 1.8), (px_ + 0.02, py_ + 0.06, Z4 + 1.84), "grafite")
    mb.box((px_ - 0.25, py_ + 0.1, Z4 + 0.02), (px_ - 0.1, py_ + 0.2, Z4 + 0.05), "grafite")
    obj(mb, "CONSEQ_Conexao_Tubulacao_Cedendo", C, visivel=False, cena="CONSEQ", props={"consequencia": "CONEXAO_INCORRETA=SIM", "oculta": "C18_Distrator_Tubulacao"})
    mb = MB()
    for dx in (0.0, 0.22):
        base = Vector((28.35 + dx, 4.45, Z4))
        tip = base + Vector((0.0, -0.22, 0.24))
        mb.cyl(tuple(base), tuple(tip), 0.0063, "vergalhao", n=5, smooth=False)
        mb.cyl(tuple(base + Vector((0.11, 0, 0))), tuple(tip + Vector((0.11, 0, 0))), 0.0063, "vergalhao", n=5, smooth=False)
        mb.cyl(tuple(tip), tuple(tip + Vector((0.11, -0.05, 0.02))), 0.0063, "vergalhao", n=5, smooth=False)
        mb.box((base.x - 0.05, base.y - 0.05, Z4), (base.x + 0.16, base.y + 0.05, Z4 + 0.015), "concreto_escuro")
    obj(mb, "CONSEQ_Conexao_Vergalhao_Dobrando", C, visivel=False, cena="CONSEQ", props={"consequencia": "CONEXAO_INCORRETA=SIM", "oculta": "C18_Distrator_Vergalhao"})
    mb = MB()
    for x in (29.25, 30.55):
        with mb.at((x, 7.0, Z4), ry=(18 if x > 30 else 0)):
            for (a, b) in (((-0.35, -0.3, 0.0), (-0.05, 0.0, 0.85)), ((0.35, -0.3, 0.0), (0.05, 0.0, 0.85)),
                           ((-0.35, 0.3, 0.0), (-0.05, 0.0, 0.85)), ((0.35, 0.3, 0.0), (0.05, 0.0, 0.85))):
                mb.strut(a, b, 0.04, "vermelho_escuro")
            mb.box((-0.3, -0.05, 0.85), (0.3, 0.05, 0.9), "vermelho_escuro")
    with mb.at((29.9, 6.8, Z4 + 0.85), rx=-14, rz=-18):
        mb.box((-1.0, -0.08, 0.05), (1.0, 0.08, 0.062), "grafite")
        mb.box((-1.0, -0.08, 0.24), (1.0, 0.08, 0.252), "grafite")
        mb.box((-1.0, -0.01, 0.062), (1.0, 0.01, 0.24), "grafite")
    obj(mb, "CONSEQ_Conexao_Estrutura_Metalica_Deslizando", C, visivel=False, cena="CONSEQ", props={"consequencia": "CONEXAO_INCORRETA=SIM",
        "oculta": "C18_Distrator_Estrutura_Metalica"})

    # ============================================ organizacao final
    C = subs["42d_Organizacao_Final"]
    mb = MB()
    rnd = random.Random(21)
    for k in range(6):
        px, py = rnd.uniform(28.9, 31.2), rnd.uniform(4.4, 5.9)
        mb.box((px, py, Z4), (px + rnd.uniform(0.05, 0.2), py + rnd.uniform(0.03, 0.08), Z4 + 0.01), ("papelao", "filme_plastico", "madeira")[k % 3])
    mb.box((30.9, 5.5, Z4), (31.3, 5.8, Z4 + 0.12), "preto_suave")
    G40.chave_boca(mb, (29.1, 4.55, Z4), rz=15.0)
    obj(mb, "ORG_Sobras_Ferramentas_Apos_Servico", C, visivel=False, cena="ORG", props={"interativo": True,
        "checklist": "recolher ferramentas; retirar materiais; conferir borda; verificar caminho de saida; observar protecoes; comunicar conclusao",
        "se_sair_com_material": "Observe novamente. Seu servico terminou. O risco que voce deixar aqui continuara para outra pessoa."})

    # ============================================ emergencia final (Bloco B)
    C = subs["42e_Emergencia_Final"]
    vx, vy = L.TR_BLOCOB_VITIMA
    mb = MB()
    mb.box((-15.45, vy - 0.12, 6.15), (-15.2, vy + 0.12, 6.17), "grafite")
    mb.box((-15.38, vy - 0.02, 6.17), (-15.26, vy + 0.02, 6.3), "amarelo_ancoragem")
    G40.decal(mb, G40.UVT(), "kit_resgate", (-16.0, vy + 0.72, 6.45), (0, -1, 0), 0.42)
    mb.box((-16.2, vy + 0.72, 6.15), (-15.8, vy + 1.0, 6.4), "vermelho_resgate", top="preto_suave")
    for (x, y) in ((-14.6, -12.9), (-12.0, -12.9), (-12.0, -7.6), (-14.6, -7.6)):
        G40.cone(mb, x, y)
    G40.fita_zebrada(mb, [(-14.6, -12.9), (-12.0, -12.9), (-12.0, -7.6), (-14.6, -7.6)], 0.62)
    obj(mb, "EMERG_Ancoragem_Kit_Isolamento_Resgate", C, visivel=False, cena="EMERG", props={"situacao": "ultima situacao - emergencia",
        "nota": "resgate executado apenas pela equipe preparada (regras 15-17 do roteiro tecnico)"})
    allo = list(bpy.data.collections[PAI].all_objects)
    return {"objetos": len(allo), "tris": K.tri_count(allo)}
