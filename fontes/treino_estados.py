# -*- coding: utf-8 -*-
# treino_estados.py - estados de visibilidade do roteiro (para cinematicas/renders no Blender) e lista do storyboard.
# No Three.js a mesma logica e feita com userData.visivel_inicial + listas "mostrar/ocultar" do roteiro_treinamento.json.
import bpy, os, sys

K = sys.modules["sitekit"]


def _vis(o, v):
    o.hide_viewport = not v
    o.hide_render = not v
    for f in o.children_recursive:          # personagens articulados: as pecas acompanham a raiz
        f.hide_viewport = not v
        f.hide_render = not v


def estado_inicial():
    n = 0
    for o in bpy.data.objects:
        if "visivel_inicial" in o.keys():
            _vis(o, bool(o["visivel_inicial"]))
            n += 1
    return n


def aplicar(mostrar=(), ocultar=()):
    estado_inicial()
    falt = []
    for nome in mostrar:
        o = bpy.data.objects.get(nome)
        if o is None:
            falt.append(nome)
            continue
        _vis(o, True)
    for nome in ocultar:
        o = bpy.data.objects.get(nome)
        if o is None:
            falt.append(nome)
            continue
        _vis(o, False)
    return falt


SUP = ["C21_Suporte_Posicionado"]
SUP_H = ["C21_Suporte_Aguardando"]

# (arquivo, camera, mostrar, ocultar, legenda)
SHOTS = [
    ("C01_1P", "CAM_1P_C01_Entrada_Canteiro", [], [], "Cena 01 - Entrada no canteiro"),
    ("C02_1P", "CAM_1P_C02_Encarregado", [], [], "Cena 02 - Estou liberado?"),
    ("C03_1P", "CAM_1P_C03_Observar_Predio", [], [], "Cena 03 - Precisa mesmo existir exposicao?"),
    ("C04_1P", "CAM_1P_C04_Encarregado_Tablet", ["NPC_C04_Encarregado_Entrega_Tablet"], ["NPC_C02_Encarregado_Conversando"], "Cena 04 - Planejamento"),
    ("C05_1P", "CAM_1P_C05_Tablet_Informacoes", ["MAOS_1P_C05_Tablet_Permissao"], [], "Cena 05 - Informacoes do servico"),
    ("C06_1P", "CAM_1P_C06_Area_Equipamentos", [], [], "Cena 06 - Area de equipamentos"),
    ("C06_1P_capacete", "CAM_1P_C06_Inspecao_Capacete", [], [], "Cena 06 - Capacete com rachadura"),
    ("C06_1P_cinturao", "CAM_1P_C06_Inspecao_Cinturao", [], [], "Cena 06 - Cinturao com pequeno corte"),
    ("C06_1P_talabarte", "CAM_1P_C06_Inspecao_Talabarte", [], [], "Cena 06 - Talabarte com desgaste"),
    ("C07_3P_erro", "CAM_3P_C07_Conferencia_Cinturao", ["AVATAR_C07_Erro_Fivela_Aberta"], [], "Cena 07 - Conferencia (erro: fivela aberta)"),
    ("C07_3P_correto", "CAM_3P_C07_Conferencia_Cinturao", ["AVATAR_C07_Cinturao_Correto"], [], "Cena 07 - Agora sim"),
    ("C08_1P", "CAM_1P_C08_Caminho_Obstaculo", [], [], "Cena 08 - Caminho ate o acesso"),
    ("C08_3P_tropeco", "CAM_3P_C08_Tropeco_Obstaculo", ["AVATAR_C08_Tropeco"], [], "Cena 08 - B: tropeca levemente"),
    ("C09_1P", "CAM_1P_C09_Escolha_Acesso", [], [], "Cena 09 - Escada de acesso"),
    ("C10_1P", "CAM_1P_C10_Pav02_Abertura_Protegida", [], [], "Cena 10 - Abertura protegida (2o pav.)"),
    ("C11_1P", "CAM_1P_C11_Pav03_Abertura_Deslocada", [], [], "Cena 11 - Protecao deslocada (3o pav.)"),
    ("C11_3P_conseq", "CAM_3P_C11_Conseq_Abertura_Ignorada", ["NPC_CONSEQ_Pav03_Trabalhador_Carregando"], [], "Consequencia - abertura ignorada"),
    ("C12_1P", "CAM_1P_C12_Chegada_Pav04", [], [], "Cena 12 - Chegada ao 4o pavimento"),
    ("C13_1P", "CAM_1P_C13_Guarda_Corpo_Solto", [], [], "Cena 13 - Guarda-corpo levemente solto"),
    ("C14_1P", "CAM_1P_C14_Area_Abaixo", [], [], "Cena 14 - Area abaixo"),
    ("C15_1P", "CAM_1P_C15_Material_Solto", [], [], "Cena 15 - Material solto"),
    ("C16_1P", "CAM_1P_C16_Outras_Equipes", [], [], "Cena 16 - Outras equipes"),
    ("C17_1P", "CAM_1P_C17_Condicoes_Ambiente", [], [], "Cena 17 - Condicoes do ambiente"),
    ("C18_1P", "CAM_1P_C18_Ponto_Conexao", [], [], "Cena 18 - Ponto de conexao"),
    ("C19_1P", "CAM_1P_C19_Regiao_Exposicao", [], [], "Cena 19 - Entrando na regiao de exposicao"),
    ("C19_3P_escorrega", "CAM_3P_C19_Desconectado_Escorrega", ["AVATAR_C19_Desconectado_Escorrega"], [], "Cena 19 - B: desconectou e escorregou"),
    ("C20_1P", "CAM_1P_C20_Ferramentas", [], [], "Cena 20 - Preparacao das ferramentas"),
    ("C21_1P", "CAM_1P_C21_Inicio_Tarefa", ["MAOS_1P_C21_Chave"] + SUP, SUP_H, "Cena 21 - Inicio da tarefa"),
    ("PRINC_1P", "CAM_1P_PRINC_Chave_Escapa", ["PRINC_Chave_Escapando_1P", "MAOS_1P_PRINC_Mao_Solta_Chave"] + SUP, SUP_H, "Cena principal - a chave escapa"),
    ("PRINC_3P_retida", "CAM_3P_PRINC_Ferramenta_Retida", ["AVATAR_PRINC_Chave_Escapou", "PRINC_Chave_Retida_Pelo_Cordao", "C20_Ferramentas_Protegidas"] + SUP,
     SUP_H + ["C20_Ferramentas_Soltas"], "Ferramentas protegidas: chave retida"),
    ("PRINC_3P_isolada", "CAM_3P_PRINC_Ferramenta_Area_Isolada", ["C14_Area_Inferior_Isolada", "C14_Barreira_Oeste_Movel", "PRINC_Chave_Caida_Dentro_Area_Isolada"],
     ["C14_Area_Inferior_Nao_Isolada", "NPC_C14_Terreo_Passando_Sob_Borda"], "Sem protecao, area isolada: ninguem atingido"),
    ("PRINC_3P_pessoa", "CAM_3P_PRINC_Ferramenta_Pessoa_Abaixo", ["PRINC_Chave_Caindo_Congelada_Sobre_Pessoa", "NPC_PRINC_Trabalhador_Abaixo", "AVATAR_PRINC_Chave_Escapou"],
     ["NPC_C14_Terreo_Passando_Sob_Borda"], "Sem protecao e sem isolamento: pessoa exposta (congelar)"),
    ("CONSEQ_3P_material_solto", "CAM_3P_CONSEQ_Material_Solto", ["CONSEQ_Material_Solto_Caindo_Congelado", "NPC_PRINC_Trabalhador_Abaixo"],
     ["C15_Madeira_Solta_Junto_Borda", "NPC_C14_Terreo_Passando_Sob_Borda"], "Consequencia - material solto"),
    ("CONSEQ_3P_material_retirado", "CAM_3P_CONSEQ_Material_Retirado_Positivo", ["EV06_Lona_Batendo_Poeira", "C15_Madeira_Retirada_Guardada"],
     ["C15_Madeira_Solta_Junto_Borda", "C17_Lona_Cobrindo_Material"], "Consequencia positiva - material retirado"),
    ("CONSEQ_3P_conexao", "CAM_3P_CONSEQ_Conexao_Incorreta", ["AVATAR_CONSEQ_Conexao_Incorreta_Tubulacao", "CONSEQ_Conexao_Tubulacao_Cedendo"],
     ["C18_Distrator_Tubulacao"], "Consequencia - conexao incorreta (tubulacao)"),
    ("CONSEQ_3P_equipamento", "CAM_3P_CONSEQ_Equipamento_Danificado", ["AVATAR_CONSEQ_Cinturao_Danificado"], [], "Consequencia - equipamento danificado"),
    ("EV01_1P", "CAM_1P_EV01_Colega_Retira_GcR", ["NPC_EV01_Colega_Retira_GcR", "EV01_Material_Longo_Tubos", "NPC_EV01_Andaime_Recebe_Material"], [], "EV01 - alguem remove o guarda-corpo"),
    ("EV01_3P_vao", "CAM_3P_EV01_Vao_Aberto", ["EV01_GcR_Sul04a_Removido_Vao_Aberto", "EV01_Pecas_GcR_Retiradas_no_Piso"], ["TorreA_Pav04_GcR_Sul_04a"], "EV01 - B/C: o vao ficou aberto"),
    ("EV02_1P", "CAM_1P_EV02_Invasao_Area_Isolada", ["C14_Area_Inferior_Isolada", "EV02_Barreira_Afastada", "NPC_EV02_Afasta_Barreira_Entra"],
     ["C14_Area_Inferior_Nao_Isolada", "NPC_C14_Terreo_Passando_Sob_Borda"], "EV02 - trabalhador entra na area isolada"),
    ("EV02_3P", "CAM_3P_EV02_Peca_Escapa", ["C14_Area_Inferior_Isolada", "EV02_Barreira_Afastada", "NPC_EV02_Dentro_Area_Isolada", "EV02_Peca_Escapa_Congelada"],
     ["C14_Area_Inferior_Nao_Isolada", "NPC_C14_Terreo_Passando_Sob_Borda"], "EV02 - B/C: peca escapa (congelar)"),
    ("EV03_1P", "CAM_1P_EV03_Objeto_Cai_Superior", ["EV03_Objeto_01_Impacto_Proximo", "NPC_EV03_Colega_Assustado"] + SUP, SUP_H, "EV03 - objeto cai de pavimento superior"),
    ("EV03_3P", "CAM_3P_EV03_Segundo_Objeto", ["EV03_Objeto_02_Congelado_Mais_Proximo", "EV03_Objeto_01_Impacto_Proximo", "AVATAR_TAREFA_Ajoelhado_Conectado"] + SUP, SUP_H,
     "EV03 - B/C: segundo objeto mais proximo (congelar)"),
    ("EV04_1P", "CAM_1P_EV04_Movimentacao_Carga", ["EV04_Paleteira_Palete_Inicio", "NPC_EV04_Operador_Paleteira_Inicio", "NPC_Pav04_Encarregado"], [], "EV04 - movimentacao de carga proxima"),
    ("EV04_3P", "CAM_3P_EV04_Carga_Aproxima", ["EV04_Paleteira_Palete_Aproximando", "NPC_EV04_Operador_Paleteira_Aproximando", "NPC_EV04_Auxiliar_Entra_Na_Area",
                                              "AVATAR_TAREFA_Ajoelhado_Conectado"] + SUP, SUP_H + ["NPC_C16_Servente_Carrinho_Blocos"], "EV04 - B/C: a situacao fica confusa (congelar)"),
    ("EV05_1P", "CAM_1P_EV05_Radio_Sem_Resposta", ["MAOS_1P_EV05_Radio"] + SUP, SUP_H, "EV05 - o radio para de funcionar"),
    ("EV05_3P", "CAM_3P_EV05_Radio_Sem_Resposta", ["AVATAR_EV05_Radio_Sem_Resposta"] + SUP, SUP_H, "EV05 - B/C: precisa de ajuda e o radio falha"),
    ("EV06_1P", "CAM_1P_EV06_Rajada_Vento", ["EV06_Lona_Batendo_Poeira"], ["C17_Lona_Cobrindo_Material"], "EV06 - rajada de vento"),
    ("EV06_3P_BC", "CAM_3P_EV06_Rajada_Desequilibrio", ["AVATAR_EV06_Desequilibrio_Sistema_Atua", "EV06_Lona_Batendo_Poeira"] + SUP, SUP_H + ["C17_Lona_Cobrindo_Material"],
     "EV06 - B/C: perda de equilibrio, sistema atua (congelar)"),
    ("EV06_3P_A", "CAM_3P_EV06_A_Rajada_Forte", ["AVATAR_EV06_A_Parado_Area_Segura", "EV06_Lona_Batendo_Poeira"], ["C17_Lona_Cobrindo_Material"], "EV06 - A: parou antes da rajada forte"),
    ("EV07_1P", "CAM_1P_EV07_Colega_Mesmo_Ponto", ["NPC_EV07_Colega_Pede_Mesmo_Ponto"] + SUP, SUP_H, "EV07 - colega pede o mesmo ponto"),
    ("EV08_1P", "CAM_1P_EV08_Material_Na_Rota", ["EV08_Cabo_Mangueira_Na_Rota_Saida"], [], "EV08 - material aparece no caminho"),
    ("EV08_3P", "CAM_3P_EV08_Quase_Tropeco", ["EV08_Cabo_Mangueira_Na_Rota_Saida", "AVATAR_EV08_Quase_Tropeco"], [], "EV08 - B/C: quase tropeca"),
    ("EV09_1P", "CAM_1P_EV09_Colega_Tontura", ["NPC_EV09_Colega_Tontura"], [], "EV09 - colega se sente mal"),
    ("EV09_3P", "CAM_3P_EV09_Colega_Desequilibrio", ["NPC_EV09_Colega_Desequilibrio"], [], "EV09 - B/C: desequilibrado (congelar)"),
    ("EV10_1P", "CAM_1P_EV10_Protecao_Alterada", ["EV10_GcR_Sul05b_Travessao_Intermediario_Removido"], ["TorreA_Pav04_GcR_Sul_05b"], "EV10 - protecao alterada no intervalo"),
    ("EV10_3P", "CAM_3P_EV10_Protecao_Alterada", ["EV10_GcR_Sul05b_Travessao_Intermediario_Removido", "AVATAR_TAREFA_Ajoelhado_Conectado"] + SUP,
     ["TorreA_Pav04_GcR_Sul_05b"] + SUP_H, "EV10 - B: descobre a alteracao durante a atividade"),
    ("EV11_1P", "CAM_1P_EV11_Faz_So_Esse_Ultimo", ["NPC_PRINC_Trabalhador_Abaixo"] + SUP, ["NPC_C14_Terreo_Passando_Sob_Borda"] + SUP_H, "EV11 - 'faz so esse ultimo'"),
    ("EV11_3P", "CAM_3P_EV11_Susto", ["AVATAR_EV11_Susto", "NPC_PRINC_Trabalhador_Abaixo"] + SUP, ["NPC_C14_Terreo_Passando_Sob_Borda"] + SUP_H, "EV11 - B: susto (congelar)"),
    ("EV12_1P", "CAM_1P_EV12_Quase_Acidente_Retido", ["EV12_Fragmento_Retido_Pelo_Rodape", "NPC_EV12_Pedreiro_Cortando_Bloco"], [], "EV12 - quase acidente sem culpa do jogador"),
    ("EV12_3P", "CAM_3P_EV12_Fragmento_Retido", ["EV12_Fragmento_Retido_Pelo_Rodape", "NPC_EV12_Pedreiro_Cortando_Bloco"], [], "EV12 - protecoes retiveram o fragmento"),
    ("EV13_1P", "CAM_1P_EV13_Identificacao_Ilegivel", ["EV13_Identificacao_PA0401_Ilegivel"], ["C18_Identificacao_PA0401_Legivel"], "EV13 - identificacao ilegivel"),
    ("EV14_1P", "CAM_1P_EV14_Ferramenta_Defeituosa", ["EV14_Ferramenta_Eletrica_Cabo_Danificado", "NPC_EV14_Colega_Da_Para_Terminar"] + SUP, SUP_H, "EV14 - ferramenta defeituosa"),
    ("EV14_3P", "CAM_3P_EV14_Ferramenta_Movimento", ["AVATAR_EV14_Ferramenta_Tranco"] + SUP, SUP_H, "EV14 - B/C: movimento inesperado (congelar)"),
    ("EV15_1P", "CAM_1P_EV15_Impacto_Protecao", ["EV15_GcR_Sul04b_Impacto_Sem_Dano_Aparente", "EV15_Tubo_Que_Atingiu_Protecao"], ["TorreA_Pav04_GcR_Sul_04b"], "EV15 - impacto na protecao"),
    ("EV15_3P", "CAM_3P_EV15_Protecao_Deslocada", ["EV15_GcR_Sul04b_Deslocado_Depois"], ["TorreA_Pav04_GcR_Sul_04b"], "EV15 - B: a protecao se move depois"),
    ("EV16_1P", "CAM_1P_EV16_Chuva", ["EV16_Piso_Molhado_Chuva"], [], "EV16 - chuva inesperada"),
    ("EV17_1P", "CAM_1P_EV17_Alarme", [], [], "EV17 - alarme de emergencia"),
    ("CONC_1P", "CAM_1P_CONC_Suporte_Instalado", ["CONC_Suporte_Instalado", "MAOS_1P_C21_Chave"], SUP_H, "Conclusao - suporte instalado"),
    ("ORG_1P", "CAM_1P_ORG_Organizacao_Final", ["ORG_Sobras_Ferramentas_Apos_Servico", "CONC_Suporte_Instalado"], SUP_H, "Organizacao final"),
    ("RET_1P", "CAM_1P_RET_Descendo_Escada", [], [], "Retorno pelo acesso previsto"),
    ("EMERG_1P", "CAM_1P_EMERG_Trabalhador_Suspenso", ["NPC_EMERG_Trabalhador_Suspenso"], [], "Ultima situacao - trabalhador suspenso"),
    ("EMERG_3P_A", "CAM_3P_EMERG_A_Equipe_Resgate", ["NPC_EMERG_Trabalhador_Suspenso", "NPC_EMERG_Resgate_01_Borda", "NPC_EMERG_Resgate_02_Radio",
                                                  "NPC_EMERG_Resgate_03_Chegando", "EMERG_Ancoragem_Kit_Isolamento_Resgate"], [], "Emergencia - A: equipe preparada"),
    ("EMERG_3P_B", "CAM_3P_EMERG_B_Subir_Sozinho", ["NPC_EMERG_Trabalhador_Suspenso", "AVATAR_EMERG_B_Subindo_Escada"], [], "Emergencia - B: subir sozinho (pare)"),
    ("EMERG_3P_D", "CAM_3P_EMERG_D_Aguardando", ["NPC_EMERG_Trabalhador_Suspenso"], [], "Emergencia - D: continua suspenso"),
    ("EMERG_3P_C", "CAM_3P_EMERG_C_Qualquer_Pessoa", ["NPC_EMERG_Trabalhador_Suspenso", "NPC_EMERG_C_Pessoa_Nao_Preparada"], [],
     "Emergencia - C: pedir para qualquer pessoa ajudar"),
    ("CONSEQ_3P_guarda_corpo", "CAM_3P_CONSEQ_Guarda_Corpo_Problema", ["CONSEQ_GcR_Sul05a_Cedendo", "C13_GcR_Sul05a_Levemente_Solto"],
     ["TorreA_Pav04_GcR_Sul_05a"], "Consequencia - guarda-corpo com problema nao comunicado"),
    ("RET_1P_terreo", "CAM_1P_RET_Chegada_Terreo", [], [], "Retorno - chegada ao terreo"),
]


def pasta_storyboard():
    p = os.path.join(K.desktop(), "canteiro_trabalho_altura_arquivos", "renders", "storyboard")
    os.makedirs(p, exist_ok=True)
    return p


def render_shots(i0, i1, res=(1280, 720), qualidade=86, pct=100):
    scn = bpy.context.scene
    old = (scn.camera, scn.render.resolution_x, scn.render.resolution_y, scn.render.resolution_percentage, scn.render.filepath,
           scn.render.image_settings.file_format)
    feitos, faltas = [], {}
    try:
        scn.render.resolution_x, scn.render.resolution_y, scn.render.resolution_percentage = res[0], res[1], pct
        scn.render.image_settings.file_format = 'JPEG'
        scn.render.image_settings.quality = qualidade
        for (arq, cam, most, ocul, leg) in SHOTS[i0:i1]:
            f = aplicar(most, ocul)
            if f:
                faltas[arq] = f
            scn.camera = bpy.data.objects[cam]
            scn.render.filepath = os.path.join(pasta_storyboard(), arq + ".jpg")
            bpy.ops.render.render(write_still=True)
            feitos.append(arq)
    finally:
        estado_inicial()
        (scn.camera, scn.render.resolution_x, scn.render.resolution_y, scn.render.resolution_percentage, scn.render.filepath,
         scn.render.image_settings.file_format) = old
    return {"feitos": feitos, "faltas": faltas}
