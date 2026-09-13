# -*- coding: utf-8 -*-
# gen_41_treino_personagens.py - figurantes (NPC_) e personagem do jogador (AVATAR_) do roteiro
# AVATAR_* so aparece nos momentos de 3a pessoa (consequencias e conferencia do cinturao).
import bpy, sys, math

K = sys.modules["sitekit"]
L = sys.modules["layout"]
PG = sys.modules["personagens"]
G40 = sys.modules["gen_40"]

Z3, Z4 = L.TA_Z(3), L.TA_Z(4)
BB2 = 6.15          # laje do pav 2 do Bloco B
PAI = "41_Treino_Personagens"

# posicoes-chave
POS_TRABALHO = (30.3, 5.15, Z4)                  # jogador ajoelhado no suporte
ANC = (L.TR_ANCORAGEM[0] - 0.10, L.TR_ANCORAGEM[1], Z4 + L.TR_ANCORAGEM[2] - 0.02)   # argola do PA-04-01


def rz_dir(dx, dy):
    return math.degrees(math.atan2(-dx, dy))


def olhar(de, para):
    return rz_dir(para[0] - de[0], para[1] - de[1])


# (nome, colecao, papel, pose, loc, rz ou ponto-alvo, visivel, cena, extras_construcao, pose_ajustes, props)
def lista():
    N = []

    def add(nome, sub, papel, pose, loc, rumo, vis=True, cena=None, kw=None, aj=None, props=None):
        N.append(dict(nome=nome, sub=sub, papel=papel, pose=pose, loc=loc, rumo=rumo, vis=vis, cena=cena, kw=kw or {}, aj=aj or {}, props=props or {}))

    # ------------------------------------------------ ambiente geral (visiveis)
    add("NPC_AMB_Porteiro", "41a_Ambiente", "porteiro", "conversando", (26.85, -27.95, 0.0), (27.1, -28.2), cena="C01")
    add("NPC_AMB_Trabalhador_Caminhando_01", "41a_Ambiente", "pedreiro", "andando", (22.6, -18.6, 0.0), (18.0, -18.2), cena="C01")
    add("NPC_AMB_Trabalhador_Carregando_Caixa", "41a_Ambiente", "servente", "carregando_frente", (29.6, -17.2, 0.0), (29.4, -12.0), cena="C01",
        kw=dict(frente="caixa"), aj=dict())
    add("NPC_AMB_Munck_Operador", "41a_Ambiente", "motorista", "falando_radio", (10.55, -0.55, 0.0), (11.3, 1.8), cena="C01", kw=dict(mao_R="radio"))
    add("NPC_AMB_Munck_Auxiliar_Cabo_Guia", "41a_Ambiente", "sinaleiro", "apontando", (13.2, 0.35, 0.0), (11.3, 1.75), cena="C01",
        aj=dict(ombroR=(45, 30, 0), cotR=20))
    add("NPC_AMB_Andaime_Reboco", "41a_Ambiente", "pedreiro", "apontando", (12.6, 3.25, 6.0), (12.6, 4.2), cena="C01",
        aj=dict(ombroR=(75, 10, 0), cotR=30))
    add("NPC_AMB_Almoxarife", "41a_Ambiente", "almoxarife", "conversando", (16.85, -23.9, 0.0), (19.3, -23.85), cena="C06")
    add("NPC_C02_Encarregado_Conversando", "41a_Ambiente", "encarregado", "conversando", (25.05, -22.6, 0.0), (26.35, -21.9), cena="C02",
        props={"interativo": True, "fala": "Bom dia, {{NOME}}. Precisamos terminar aquele suporte."})
    add("NPC_C04_Encarregado_Entrega_Tablet", "41a_Ambiente", "encarregado", "entregando_tablet", (25.05, -22.6, 0.0), (26.35, -21.9), vis=False, cena="C04",
        kw=dict(mao_R="tablet"), props={"interativo": True, "fala": "Fizeram praticamente o mesmo servico no terceiro andar na semana passada."})

    # ------------------------------------------------ 4o pavimento: outras equipes (visiveis)
    add("NPC_C16_Pedreiro_Assentando", "41b_Pav04", "pedreiro", "abaixado_pegando", (24.9, 9.42, Z4), (24.9, 10.3), cena="C16", kw=dict(mao_R="bloco"))
    add("NPC_C16_Servente_Carrinho_Blocos", "41b_Pav04", "servente", "empurrando", (26.9, 10.6, Z4), (26.6, 6.4), cena="C16",
        props={"interativo": True, "rotulo": "Equipe movimentando material no mesmo pavimento"})
    add("NPC_Pav04_Encarregado", "41b_Pav04", "encarregado", "falando_radio", (28.9, 9.45, Z4), (29.8, 5.4), vis=False, cena="EV",
        kw=dict(mao_R="radio"), props={"usado_em": "EV01-A, EV04, EV05-A, EV06, EV11"})
    add("NPC_EV05_Encarregado_Radio_Substituto", "41b_Pav04", "encarregado", "entregando_tablet", (29.2, 6.3, Z4), POS_TRABALHO, vis=False, cena="EV05",
        kw=dict(mao_R="radio"))
    add("NPC_EV01_Colega_Retira_GcR", "41b_Pav04", "servente", "removendo_gcr", (23.05, 4.78, Z4), (23.05, 3.5), vis=False, cena="EV01",
        props={"fala": "Parceiro, vou tirar isso aqui so um minutinho para passar o material. E rapidinho."})
    add("NPC_EV01_Andaime_Recebe_Material", "41b_Pav04", "armador", "apontando", (21.05, 3.2, 12.0), (23.0, 4.5), vis=False, cena="EV01",
        aj=dict(ombroR=(60, 20, 0), cotR=40), kw=dict(talabarte=False))
    add("NPC_EV03_Colega_Assustado", "41b_Pav04", "servente", "assustado", (27.95, 6.55, Z4), (29.4, 4.6), vis=False, cena="EV03",
        props={"fala": "Caramba!"})
    add("NPC_EV04_Operador_Paleteira_Inicio", "41b_Pav04", "servente", "empurrando", (19.9, 12.75, Z4), (26.0, 12.75), vis=False, cena="EV04")
    add("NPC_EV04_Operador_Paleteira_Aproximando", "41b_Pav04", "servente", "empurrando", (27.95, 8.75, Z4), (28.2, 5.5), vis=False, cena="EV04")
    add("NPC_EV04_Auxiliar_Entra_Na_Area", "41b_Pav04", "sinaleiro", "sinalizando_pare", (29.35, 6.2, Z4), (28.0, 8.5), vis=False, cena="EV04")
    add("NPC_EV07_Colega_Pede_Mesmo_Ponto", "41b_Pav04", "colega_altura", "conversando", (31.0, 5.55, Z4), POS_TRABALHO, vis=False, cena="EV07",
        kw=dict(mao_R="conector"), props={"fala": "{{NOME}}, prende o meu aqui junto com o seu. E so um servico rapido."})
    add("NPC_EV09_Colega_Tontura", "41b_Pav04", "colega_altura", "tontura", (25.25, 4.85, Z4), (25.3, 3.5), vis=False, cena="EV09",
        props={"fala": "Estou meio tonto. Ja passa."})
    add("NPC_EV09_Colega_Desequilibrio", "41b_Pav04", "colega_altura", "desequilibrio_frente", (25.25, 4.72, Z4), (25.3, 3.5), vis=False, cena="EV09")
    add("NPC_EV12_Pedreiro_Cortando_Bloco", "41b_Pav04", "pedreiro", "agachado_trabalhando", (24.35, 5.45, Z4), (24.6, 4.2), vis=False, cena="EV12",
        kw=dict(mao_R="chave"))
    add("NPC_EV14_Colega_Da_Para_Terminar", "41b_Pav04", "colega_altura", "conversando", (29.05, 6.15, Z4), POS_TRABALHO, vis=False, cena="EV14",
        props={"fala": "Da para terminar com ela."})
    add("NPC_C11_Equipe_Corrige_Ajoelhado", "41c_Pav03", "servente", "agachado_trabalhando", (14.0, 14.1, Z3), (14.0, 15.0), vis=False, cena="C11")
    add("NPC_C11_Equipe_Corrige_Em_Pe", "41c_Pav03", "pedreiro", "apontando", (12.8, 15.2, Z3), (14.0, 15.0), vis=False, cena="C11",
        aj=dict(ombroR=(40, 10, 0)))
    add("NPC_CONSEQ_Pav03_Trabalhador_Carregando", "41c_Pav03", "servente", "carregando_ombro", (12.45, 14.9, Z3), (16.0, 14.9), vis=False, cena="CONSEQ",
        kw=dict(ombro="tabuas"), props={"consequencia": "ABERTURA_IGNORADA=SIM"})

    # ------------------------------------------------ terreo abaixo da frente de trabalho
    add("NPC_C14_Terreo_Carrinho_Circulando", "41d_Terreo", "servente", "empurrando", (25.3, -2.6, 0.0), (23.9, 0.4), cena="C14")
    add("NPC_C14_Terreo_Passando_Sob_Borda", "41d_Terreo", "pedreiro", "andando", (31.2, 1.9, 0.0), (24.0, 1.8), cena="C14",
        props={"estado": "AREA_INFERIOR_ISOLADA=NAO (inicial)"})
    add("NPC_PRINC_Trabalhador_Abaixo", "41d_Terreo", "pedreiro", "andando", (30.35, 2.5, 0.0), (24.0, 2.3), vis=False, cena="PRINC",
        props={"usado_em": "PRINC (ferramenta sem protecao e area nao isolada), CONSEQ material solto, EV11"})
    add("NPC_EV02_Afasta_Barreira_Entra", "41d_Terreo", "servente", "movendo_barreira", (26.0, 0.75, 0.0), (29.5, 1.6), vis=False, cena="EV02")
    add("NPC_EV02_Dentro_Area_Isolada", "41d_Terreo", "servente", "andando", (28.9, 1.4, 0.0), (32.0, 1.9), vis=False, cena="EV02")

    # ------------------------------------------------ avatar do jogador (3a pessoa)
    ava_c07 = (20.35, -22.35, 0.0)
    rum_c07 = (22.2, -24.7)
    for (suf, erro) in (("Cinturao_Correto", None), ("Erro_Fita_Torcida", "fita_torcida"), ("Erro_Fivela_Aberta", "fivela_aberta"),
                        ("Erro_Ajuste_Frouxo", "ajuste_frouxo"), ("Erro_Colocado_Invertido", "colocado_invertido")):
        add("AVATAR_C07_" + suf, "41e_Avatar", "jogador", "vestindo_conferencia", ava_c07, rum_c07, vis=False, cena="C07",
            kw=dict(erro_cinturao=erro), props={"variavel": "CINTURAO_AJUSTADO", "erro": erro or "nenhum"})
    add("AVATAR_C08_Tropeco", "41e_Avatar", "jogador", "tropecando", (25.45, -7.45, 0.0), (25.2, -4.0), vis=False, cena="C08")
    add("AVATAR_C19_Desconectado_Escorrega", "41e_Avatar", "jogador", "escorregando", (30.05, 5.05, Z4), (30.05, 3.0), vis=False, cena="C19")
    add("AVATAR_TAREFA_Ajoelhado_Conectado", "41e_Avatar", "jogador", "agachado_trabalhando", POS_TRABALHO, (30.3, 3.5), vis=False, cena="C21",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.35, mao_R="chave_amarrada"))
    add("AVATAR_PRINC_Chave_Escapou", "41e_Avatar", "jogador", "assustado", (30.3, 5.3, Z4), (30.3, 3.5), vis=False, cena="PRINC",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.3), aj=dict(pz=0.6, quadR=(84, 4, 0), joeR=88, quadL=(-4, 4, 0), joeL=86, tornL=58,
                                                                        ombroR=(80, 20, 0), cotR=30, ombroL=(40, 30, 0), cotL=60, head=(-35, 0, 0)))
    add("AVATAR_EV05_Radio_Sem_Resposta", "41e_Avatar", "jogador", "comunicando_radio_agachado", POS_TRABALHO, (30.3, 3.5), vis=False, cena="EV05",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.35, mao_R="radio"))
    add("AVATAR_EV06_Desequilibrio_Sistema_Atua", "41e_Avatar", "jogador", "desequilibrio_frente", (30.25, 4.85, Z4), (30.25, 3.0), vis=False, cena="EV06",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.0))
    add("AVATAR_EV06_A_Parado_Area_Segura", "41e_Avatar", "jogador", "em_pe_bracos_cruzados", (28.2, 8.6, Z4), (30.0, 5.0), vis=False, cena="EV06",
        props={"estado": "escolha_A (parou antes da rajada forte)"})
    add("AVATAR_EV08_Quase_Tropeco", "41e_Avatar", "jogador", "tropecando", (24.95, 12.85, Z4), (22.0, 12.85), vis=False, cena="EV08")
    add("AVATAR_EV11_Susto", "41e_Avatar", "jogador", "assustado", (30.25, 5.4, Z4), (30.3, 3.5), vis=False, cena="EV11",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.2))
    add("AVATAR_EV14_Ferramenta_Tranco", "41e_Avatar", "jogador", "ferramenta_tranco", POS_TRABALHO, (30.3, 3.5), vis=False, cena="EV14",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.35, mao_R="furadeira"))
    conexoes = (("Tubulacao", (31.66, 4.75, Z4 + 1.4)), ("Vergalhao", (28.5, 4.45, Z4 + 0.36)),
                ("GuardaCorpo", (29.9, 4.08, Z4 + 1.15)), ("EstruturaMetalica", (29.9, 7.0, Z4 + 1.05)))
    for (nm, alvo) in conexoes:
        pos = (29.55, 4.85, Z4) if nm != "Vergalhao" else (28.75, 4.9, Z4)
        add("AVATAR_CONSEQ_Conexao_Incorreta_" + nm, "41e_Avatar", "jogador", "desequilibrio_frente", pos, (pos[0] + 0.2, 3.0), vis=False, cena="CONSEQ",
            kw=dict(talabarte_alvo_mundo=alvo, talabarte_folga=0.0), props={"consequencia": "CONEXAO_INCORRETA=SIM", "ponto_escolhido": nm})
    add("AVATAR_CONSEQ_Cinturao_Danificado", "41e_Avatar", "jogador", "desequilibrio_frente", (30.25, 4.85, Z4), (30.25, 3.0), vis=False, cena="CONSEQ",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.0, erro_cinturao="corte_rompendo"), props={"consequencia": "CINTURAO_DANIFICADO=SIM"})
    add("AVATAR_CONSEQ_Talabarte_Danificado", "41e_Avatar", "jogador", "desequilibrio_frente", (30.25, 4.85, Z4), (30.25, 3.0), vis=False, cena="CONSEQ",
        kw=dict(talabarte_alvo_mundo=ANC, talabarte_folga=0.0, erro_cinturao="talabarte_desfiando"), props={"consequencia": "TALABARTE_DANIFICADO=SIM"})
    add("AVATAR_ORG_Recolhendo_Ferramentas", "41e_Avatar", "jogador", "abaixado_pegando", (28.3, 6.45, Z4), (28.1, 5.6), vis=False, cena="ORG")
    add("AVATAR_EMERG_A_Radio", "41e_Avatar", "jogador", "falando_radio", (11.6, -2.9, 0.0), (-14.5, -10.0), vis=False, cena="EMERG", kw=dict(mao_R="radio"))
    add("AVATAR_EMERG_B_Subindo_Escada", "41e_Avatar", "jogador", "subindo_escada", (-14.38, -5.5, 1.35), (-16.0, -5.5), vis=False, cena="EMERG",
        kw=dict(talabarte=False))

    # ------------------------------------------------ eventos gerais e emergencia final (Bloco B)
    for k, (loc, alvo) in enumerate((((24.8, -12.0, 0.0), (23.5, -21.0)), ((25.5, -14.9, 0.0), (24.5, -21.5)), ((22.9, -19.2, 0.0), (22.6, -22.5)))):
        add("NPC_EV17_Evacuacao_%02d" % (k + 1), "41f_Emergencia", ("pedreiro", "servente", "armador")[k], "andando", loc, alvo, vis=False, cena="EV17")
    vit = (L.TR_BLOCOB_VITIMA[0], L.TR_BLOCOB_VITIMA[1], 2.25)
    anc_b = (-15.32, L.TR_BLOCOB_VITIMA[1], BB2 + 0.2)
    add("NPC_EMERG_Trabalhador_Suspenso", "41f_Emergencia", "colega_altura", "suspenso", vit, (-10.0, L.TR_BLOCOB_VITIMA[1]), vis=False, cena="EMERG",
        kw=dict(talabarte_alvo_mundo=anc_b, talabarte_folga=0.0), props={"situacao": "queda contida pelo sistema de protecao - trabalhador suspenso"})
    add("NPC_EMERG_Resgate_01_Borda", "41f_Emergencia", "resgate", "agachado_trabalhando", (-15.85, -10.0, BB2), (-14.0, -10.2), vis=False, cena="EMERG",
        kw=dict(mao_R="kit_resgate"))
    add("NPC_EMERG_Resgate_02_Radio", "41f_Emergencia", "resgate", "falando_radio", (-16.6, -11.4, BB2), (-14.5, -10.2), vis=False, cena="EMERG", kw=dict(mao_R="radio"))
    add("NPC_EMERG_Resgate_03_Chegando", "41f_Emergencia", "resgate", "correndo", (-9.2, -6.4, 0.0), (-13.5, -9.5), vis=False, cena="EMERG", kw=dict(mao_R="kit_resgate"))
    add("NPC_EMERG_C_Pessoa_Nao_Preparada", "41f_Emergencia", "servente", "subindo_escada", (-14.38, -5.5, 1.35), (-16.0, -5.5), vis=False, cena="EMERG")
    return N



# ------------------------------------------------------------------ vida no canteiro
# Regra: ninguem anda a esmo. Quem sai do lugar tem um circuito curto e com
# motivo - do posto de trabalho ate o material e de volta, ou uma ronda entre
# dois pontos fazendo a mesma coisa. Todo o resto trabalha parado no seu posto.

# tarefa de quem fica no lugar, por oficio
TAREFA_PADRAO = {
    "pedreiro": "assentando", "servente": "carregando", "armador": "amarrando",
    "almoxarife": "prancheta", "motorista": "radio", "sinaleiro": "conferindo",
    "porteiro": "prancheta", "tecnico_seguranca": "prancheta", "encarregado": "falando",
    "colega_altura": "trabalhando", "resgate": "parado", "jogador": "parado",
}

# quem participa do roteiro e trabalha parado: o enquadramento das cenas conta com
# eles naquele ponto exato
TAREFA_FIXA = {
    "NPC_EV01_Andaime_Recebe_Material": "puxando", "NPC_Pav04_Encarregado": "falando",
    "NPC_EV12_Pedreiro_Cortando_Bloco": "serrando", "NPC_C11_Equipe_Corrige_Ajoelhado": "amarrando",
    "NPC_C11_Equipe_Corrige_Em_Pe": "conferindo", "NPC_EV05_Encarregado_Radio_Substituto": "radio",
    "NPC_EMERG_Resgate_02_Radio": "radio", "NPC_EMERG_Resgate_01_Borda": "trabalhando",
    "NPC_EMERG_Resgate_03_Chegando": "carregando", "NPC_EV09_Colega_Tontura": "tonto",
    "NPC_EV07_Colega_Pede_Mesmo_Ponto": "falando", "NPC_EV14_Colega_Da_Para_Terminar": "falando",
    "NPC_EV03_Colega_Assustado": "assustado", "NPC_C04_Encarregado_Entrega_Tablet": "falando",
    "NPC_C02_Encarregado_Conversando": "falando", "NPC_EV01_Colega_Retira_GcR": "trabalhando",
    "NPC_EV04_Auxiliar_Entra_Na_Area": "conferindo", "NPC_C16_Pedreiro_Assentando": "assentando",
    "NPC_EMERG_C_Pessoa_Nao_Preparada": "subindo", "NPC_AMB_Munck_Operador": "radio",
    "NPC_AMB_Munck_Auxiliar_Cabo_Guia": "conferindo", "NPC_AMB_Andaime_Reboco": "martelando",
    "NPC_AMB_Almoxarife": "prancheta", "NPC_AMB_Porteiro": "prancheta",
    "NPC_AMB_Trabalhador_Carregando_Caixa": "carregando", "NPC_C16_Servente_Carrinho_Blocos": "empurrando",
    "NPC_C14_Terreo_Passando_Sob_Borda": "conferindo", "NPC_EV04_Operador_Paleteira_Inicio": "empurrando",
    "NPC_EV04_Operador_Paleteira_Aproximando": "empurrando", "NPC_EV17_Evacuacao_01": "conferindo",
    "NPC_EV17_Evacuacao_02": "falando", "NPC_EV17_Evacuacao_03": "conferindo",
    "NPC_EV02_Afasta_Barreira_Entra": "empurrando", "NPC_EV02_Dentro_Area_Isolada": "conferindo",
    "NPC_PRINC_Trabalhador_Abaixo": "carregando", "NPC_EV09_Colega_Desequilibrio": "desequilibrio",
    "NPC_EMERG_Trabalhador_Suspenso": "suspenso",
    "NPC_CONSEQ_Pav03_Trabalhador_Carregando": "carregando",
}

# os unicos do roteiro que continuam se deslocando - e com destino certo
CIRCUITOS_ROTEIRO = {
    # nome: (tipo, tarefa no posto, espera no posto, espera no apoio, alcance)
    "NPC_AMB_Trabalhador_Caminhando_01": ("ronda", "conferindo", 6.0, 6.0, (7.0, 11.0)),
    "NPC_C14_Terreo_Carrinho_Circulando": ("material", "empurrando", 9.0, 5.0, (4.0, 7.0)),
}

Z3_, Z4_ = L.TA_Z(3), L.TA_Z(4)

# ------------------------------------------------------- figurantes de ambiente
# Cada um é uma frente de serviço de verdade. "anda":
#   None       - trabalha parado no posto
#   "material" - vai buscar material a poucos metros e volta para o posto
#   "ronda"    - faz a mesma coisa entre dois pontos (limpeza, inspeção)
POSTOS = [
    dict(id="Central_Argamassa", loc=(-2.5, -24.0, 0.0), papel="pedreiro", item=None,
         tarefa="misturando", anda="material", espera=(16.0, 5.0), alcance=(3.5, 6.0)),
    dict(id="Alvenaria_Fundos", loc=(6.2, -25.5, 0.0), papel="pedreiro", item=None,
         tarefa="assentando", anda="material", espera=(18.0, 5.0), alcance=(3.5, 6.0)),
    dict(id="Almoxarifado", loc=(12.2, -22.0, 0.0), papel="almoxarife", item="prancheta",
         tarefa="prancheta", anda=None),
    dict(id="Vala_Drenagem", loc=(20.0, -8.4, 0.0), papel="servente", item="pa",
         tarefa="cavando", anda=None),
    dict(id="Carpintaria", loc=(29.5, -25.0, 0.0), papel="pedreiro", item="martelo",
         tarefa="martelando", anda=None),
    dict(id="Patio_Armacao", loc=(-20.4, -21.0, 0.0), papel="armador", item="alicate",
         tarefa="amarrando", anda=None),
    dict(id="Inspecao_Seguranca", loc=(-24.5, -16.0, 0.0), papel="tecnico_seguranca", item="prancheta",
         tarefa="conferindo", anda="ronda", espera=(9.0, 9.0), alcance=(6.0, 10.0)),
    dict(id="Limpeza_Via", loc=(34.7, -7.3, 0.0), papel="servente", item="vassoura",
         tarefa="varrendo", anda="ronda", espera=(7.0, 7.0), alcance=(5.0, 8.0)),
    dict(id="Descarga_Sul", loc=(20.8, -3.3, 0.0), papel="servente", item=None,
         tarefa="carregando", anda="material", espera=(8.0, 6.0), alcance=(3.5, 6.5)),
    dict(id="Pintura_BlocoB", loc=(-25.0, -7.0, 0.0), papel="pedreiro", item="rolo",
         tarefa="pintando", anda=None),
    dict(id="Serra_Bancada", loc=(-19.0, 2.5, 0.0), papel="armador", item="serrote",
         tarefa="serrando", anda=None),
    dict(id="Pav03_Ferragem", loc=(15.1, 20.4, Z3_), papel="colega_altura", item="alicate",
         tarefa="amarrando", anda=None),
    dict(id="Pav04_Forma", loc=(11.5, 8.5, Z4_), papel="colega_altura", item="martelo",
         tarefa="martelando", anda=None),
    dict(id="Pav04_Instalacao", loc=(28.2, 16.5, Z4_), papel="colega_altura", item=None,
         tarefa="trabalhando", anda=None),
]


# ---------------------------------------------------------------- raio-casting
def _cena():
    return bpy.context.scene, bpy.context.evaluated_depsgraph_get()


def _bate(orig, dirv, dist):
    sc, dep = _cena()
    r = sc.ray_cast(dep, orig, dirv, distance=dist)
    return r[0], r[1], r[2]


def _piso(x, y, z, tol=0.30):
    ok, loc, nor = _bate((x, y, z + 1.30), (0, 0, -1), 2.4)
    return bool(ok) and abs(loc.z - z) <= tol and nor.z > 0.55


def _folga(x, y, z, dir_xy, dist, alturas=(0.35, 0.95, 1.62)):
    d = min(dist, 60.0)
    for h in alturas:
        ok, loc, _n = _bate((x, y, z + h), (dir_xy[0], dir_xy[1], 0.0), d)
        if ok:
            d = min(d, math.dist((x, y, z + h), (loc.x, loc.y, loc.z)))
    return d


def _cabe(x, y, z, raio=0.70):
    if not _piso(x, y, z):
        return False
    for k in range(8):
        a = k * math.pi / 4.0
        dx, dy = math.cos(a), math.sin(a)
        if _folga(x, y, z, (dx, dy), raio) < raio - 0.01:
            return False
        if not _piso(x + dx * raio, y + dy * raio, z, tol=0.45):
            return False
    return True


def destino(x, y, z, minimo=3.5, maximo=6.0, evitar=None):
    """acha UM ponto alcançavel a partir de (x, y): é para onde a pessoa vai."""
    melhor = None
    for k in range(24):
        a = k * math.pi / 12.0
        dx, dy = math.cos(a), math.sin(a)
        livre = _folga(x, y, z, (dx, dy), maximo + 1.4)
        alc = min(livre - 1.0, maximo)
        while alc >= minimo:
            px, py = x + dx * alc, y + dy * alc
            if _cabe(px, py, z) and (evitar is None or math.dist((px, py), evitar) > 2.5):
                if melhor is None or alc > melhor[0]:
                    melhor = (alc, round(px, 2), round(py, 2))
                break
            alc -= 0.7
    return None if melhor is None else (melhor[1], melhor[2])


def lugar_livre(x, y, z, usados, raio=0.75, afast=5.0):
    for r in (0.0, 1.2, 2.4, 3.6, 5.0):
        passos = 1 if r == 0 else 8
        for k in range(passos):
            a = k * 2 * math.pi / passos
            px, py = x + math.cos(a) * r, y + math.sin(a) * r
            if not _cabe(px, py, z, raio):
                continue
            if any(math.dist((px, py), (ux, uy)) < afast for (ux, uy, uz) in usados if abs(uz - z) < 1.0):
                continue
            return (round(px, 2), round(py, 2))
    return None


def ambientes(usados):
    """cria os figurantes de fundo que sobrevivem à validação do terreno."""
    N = []
    for d in POSTOS:
        x, y, z = d["loc"]
        pt = lugar_livre(x, y, z, usados)
        if not pt:
            continue
        usados.append((pt[0], pt[1], z))
        kw = {}
        if d["item"]:
            kw["mao_R"] = d["item"]
        if d["papel"] in ("colega_altura", "armador"):
            kw["talabarte"] = False
        N.append(dict(nome="NPC_VIDA_" + d["id"], sub="41g_Vida", papel=d["papel"],
                      pose="em_pe", loc=(pt[0], pt[1], z),
                      rumo=(pt[0], pt[1] - 3.0), vis=True, cena="AMB",
                      kw=kw, aj={}, props={"figurante": True},
                      posto=d))
    return N


def circuito(d):
    """monta o trajeto com sentido: para onde vai e o que faz ao chegar."""
    x, y, z = d["loc"]
    posto = d.get("posto")
    if posto:
        tipo, tarefa = posto.get("anda"), posto["tarefa"]
        esp = posto.get("espera", (14.0, 5.0))
        alc = posto.get("alcance", (3.5, 6.0))
    else:
        c = CIRCUITOS_ROTEIRO.get(d["nome"])
        if not c:
            return None
        tipo, tarefa, e0, e1, alc = c
        esp = (e0, e1)
    if not tipo:
        return None
    alvo = destino(x, y, z, alc[0], alc[1])
    if not alvo:
        return None
    if tipo == "material":                       # trabalha no posto, busca material e volta
        ativ = [tarefa, "carregando"]
    else:                                        # ronda: faz a mesma coisa nos dois pontos
        ativ = [tarefa, tarefa]
    return {"patrulha": [round(x, 2), round(y, 2), alvo[0], alvo[1]],
            "atividades": ativ,
            "esperas": [float(esp[0]), float(esp[1])],
            "vel_andar": round(0.78 + (abs(hash(d["nome"])) % 4) * 0.04, 2)}


def planejar(d):
    """decide a rotina ANTES de existir qualquer boneco (senão o raio bate nele mesmo)."""
    nome, papel = d["nome"], d["papel"]
    if nome.startswith("AVATAR_"):
        return {}
    c = circuito(d)
    if c:
        return c
    posto = d.get("posto")
    if posto:
        return {"tarefa_fixa": posto["tarefa"]}
    return {"tarefa_fixa": TAREFA_FIXA.get(nome) or TAREFA_PADRAO.get(papel, "parado")}


def build():
    K.coll(PAI)
    subs = {}
    K.clear_coll(PAI)
    bpy.context.view_layer.update()            # o cenario precisa estar sem bonecos para medir

    roteiro = lista()
    usados = [(d["loc"][0], d["loc"][1], d["loc"][2]) for d in roteiro]
    todos = roteiro + ambientes(usados)
    planos = dict((d["nome"], planejar(d)) for d in todos)

    feitos = []
    andando = parados = 0
    for d in todos:
        if d["sub"] not in subs:
            subs[d["sub"]] = K.coll(d["sub"], PAI)
        C = subs[d["sub"]]
        rumo = d["rumo"]
        rz = rumo if isinstance(rumo, (int, float)) else olhar(d["loc"], rumo)
        kw = dict(d["kw"])
        if not d["nome"].startswith("AVATAR_") and "pele" not in kw:
            kw["pele"] = ("pele_clara", "pele_morena", "pele_escura")[sum(ord(ch) for ch in d["nome"]) % 3]
        props = {"treinamento": True, "visivel_inicial": bool(d["vis"])}
        if d["cena"]:
            props["cena"] = d["cena"]
        props["modo_camera"] = "3P_consequencia" if d["nome"].startswith("AVATAR_") else "cenario"
        props.update(d["props"])
        o = PG.criar_partes(d["nome"], C, d["loc"], rz=rz, papel=d["papel"], pose_nome=d["pose"],
                            pose_aj=d["aj"], props=props, **kw)
        plano = planos.get(d["nome"], {})
        for (k, v) in plano.items():
            o[k] = v
        if "patrulha" in plano:
            andando += 1
        elif "tarefa_fixa" in plano:
            parados += 1
        G40.mostrar(o, d["vis"])
        for f in o.children_recursive:
            G40.mostrar(f, d["vis"])
        feitos.append(o)
    pecas = [x for x in bpy.data.objects if x.type == 'MESH' and x.get("personagem")]
    return {"personagens": len(feitos), "figurantes_novos": len(todos) - len(roteiro),
            "com_circuito": andando, "trabalhando_parados": parados,
            "pecas": len(pecas), "tris": K.tri_count(pecas)}
