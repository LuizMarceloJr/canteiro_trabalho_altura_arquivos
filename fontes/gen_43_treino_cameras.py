# -*- coding: utf-8 -*-
# gen_43_treino_cameras.py - cameras de 1a pessoa (CAM_1P_*), cameras de 3a pessoa so para consequencias (CAM_3P_*),
# gatilhos (TRG_*), rota de navegacao (NAV_*) e maos em 1a pessoa (MAOS_1P_*).
import bpy, sys, math
from mathutils import Vector, Matrix, Euler

K = sys.modules["sitekit"]
L = sys.modules["layout"]
MB = K.MB
PG = sys.modules["personagens"]
G40 = sys.modules["gen_40"]

Z = L.TA_Z
Z3, Z4 = Z(3), Z(4)
E = 1.62            # altura dos olhos em pe
EA = 1.0            # ajoelhado
LENTE_1P = 20.0     # ~84 graus na horizontal (16:9)
PAI = "43_Treino_Cameras_Gatilhos"
TRAB = (30.3, 5.25, Z4 + EA)      # olhos do trabalhador ajoelhado no suporte


def cams_1p():
    return [
        ("CAM_1P_C01_Entrada_Canteiro", (27.1, -26.4, E), (26.6, 4.2, 12.4), "C01", "Entrada: pessoas circulando, caminhao descarregando ao fundo, predio a frente; olhar para o 4o pavimento"),
        ("CAM_1P_C02_Encarregado", (26.35, -21.9, E), (25.05, -22.6, 1.58), "C02", "O encarregado encontra o trabalhador"),
        ("CAM_1P_C03_Observar_Predio", (26.35, -21.9, E), (29.6, 4.2, 12.6), "C03", "Observar o predio: precisa mesmo existir exposicao a altura?"),
        ("CAM_1P_C04_Encarregado_Tablet", (26.35, -21.9, E), (25.25, -22.45, 1.3), "C04", "O encarregado entrega o tablet"),
        ("CAM_1P_C05_Tablet_Informacoes", (26.35, -21.9, E), (26.15, -23.25, 0.92), "C05", "Tablet: permissao de trabalho e analise de risco do servico de hoje"),
        ("CAM_1P_C06_Area_Equipamentos", (19.35, -23.85, E), (17.9, -23.8, 0.82), "C06", "Area de equipamentos: bancada de inspecao"),
        ("CAM_1P_C06_Inspecao_Capacete", (18.48, -24.69, 1.36), (17.9, -24.69, 0.95), "C06", "Aproximacao: capacete com rachadura"),
        ("CAM_1P_C06_Inspecao_Cinturao", (18.42, -23.6, 1.42), (17.86, -23.66, 0.9), "C06", "Aproximacao: cinturao com pequeno corte na fita"),
        ("CAM_1P_C06_Inspecao_Talabarte", (18.55, -22.85, 1.42), (18.0, -22.9, 0.9), "C06", "Aproximacao: talabarte com desgaste"),
        ("CAM_1P_C08_Caminho_Obstaculo", (26.15, -10.2, E), (25.4, -6.2, 0.3), "C08", "Materiais bloqueando parcialmente a circulacao"),
        ("CAM_1P_C09_Escolha_Acesso", (24.85, -2.3, E), (24.35, 3.4, 2.1), "C09", "Acesso previsto (coberto) x escada portatil ao lado"),
        ("CAM_1P_C10_Pav02_Abertura_Protegida", (17.1, 14.95, Z(2) + E), (14.0, 15.0, Z(2)), "C10", "2o pavimento: abertura corretamente protegida"),
        ("CAM_1P_C11_Pav03_Abertura_Deslocada", (17.1, 14.95, Z3 + E), (14.0, 15.0, Z3), "C11", "3o pavimento: protecao da abertura deslocada"),
        ("CAM_1P_C12_Chegada_Pav04", (28.3, 9.6, Z4 + E), (29.3, 4.2, Z4 + 0.8), "C12", "Chegada ao 4o pavimento: comparar o encontrado com o planejado"),
        ("CAM_1P_C13_Guarda_Corpo_Solto", (28.35, 5.35, Z4 + E), (28.2, 4.12, Z4 + 0.7), "C13", "Parte do guarda-corpo levemente solta (e preciso se aproximar)"),
        ("CAM_1P_C14_Area_Abaixo", (29.6, 4.02, Z4 + 1.34), (29.35, 0.6, 0.0), "C14", "Olhar para baixo (debrucado sobre o guarda-corpo): circulacao no terreo"),
        ("CAM_1P_C15_Material_Solto", (27.55, 5.35, Z4 + E), (27.98, 4.3, Z4 + 0.4), "C15", "Pequeno pedaco de madeira junto a borda"),
        ("CAM_1P_C16_Outras_Equipes", (28.4, 7.1, Z4 + E), (25.1, 9.9, Z4 + 0.95), "C16", "Outras equipes movimentando material no mesmo pavimento"),
        ("CAM_1P_C17_Condicoes_Ambiente", (29.4, 5.2, Z4 + E), (34.0, -7.0, 9.5), "C17", "Vento leve: fita no guarda-corpo e biruta ao fundo"),
        ("CAM_1P_C18_Ponto_Conexao", (29.9, 8.6, Z4 + E), (30.6, 4.6, Z4 + 0.9), "C18", "Ponto identificado x guarda-corpo, vergalhao, tubulacao e estrutura metalica"),
        ("CAM_1P_C19_Regiao_Exposicao", (29.8, 6.0, Z4 + E), (30.3, 4.3, Z4 + 0.45), "C19", "A partir daqui existe risco de queda"),
        ("CAM_1P_C20_Ferramentas", (28.9, 6.6, Z4 + E), (28.15, 5.7, Z4), "C20", "Chave, parafusos, ferramenta eletrica e pequenas pecas"),
        ("CAM_1P_C21_Inicio_Tarefa", TRAB, (30.3, 4.45, Z4 + 0.05), "C21", "Posicionar, fixar e apertar o suporte (ajoelhado)"),
        ("CAM_1P_PRINC_Chave_Escapa", TRAB, (30.32, 4.02, Z4 + 0.30), "PRINC", "A chave escapa durante o aperto"),
        ("CAM_1P_EV01_Colega_Retira_GcR", (27.6, 6.3, Z4 + E), (23.4, 4.6, Z4 + 0.9), "EV01", "Colega comeca a retirar parte do guarda-corpo"),
        ("CAM_1P_EV02_Invasao_Area_Isolada", (29.35, 4.02, Z4 + 1.34), (27.2, 0.9, 0.0), "EV02", "Olhar para baixo: alguem afasta a barreira e entra"),
        ("CAM_1P_EV03_Objeto_Cai_Superior", TRAB, (29.35, 4.55, Z4 + 0.15), "EV03", "CLANG! pedaco de material cai perto"),
        ("CAM_1P_EV04_Movimentacao_Carga", (30.1, 5.6, Z4 + E), (25.5, 10.6, Z4 + 0.8), "EV04", "Movimentacao de palete no mesmo pavimento, vindo na direcao da area"),
        ("CAM_1P_EV05_Radio_Sem_Resposta", TRAB, (30.3, 4.3, Z4 + 0.95), "EV05", "O radio nao responde (chiado)"),
        ("CAM_1P_EV06_Rajada_Vento", (29.9, 5.5, Z4 + E), (26.2, 8.4, Z4 + 0.9), "EV06", "Rajada: lona batendo, poeira e materiais leves"),
        ("CAM_1P_EV07_Colega_Mesmo_Ponto", TRAB, (31.0, 5.55, Z4 + 1.45), "EV07", "Colega pede para prender no mesmo ponto"),
        ("CAM_1P_EV08_Material_Na_Rota", (26.2, 11.6, Z4 + E), (24.4, 12.8, Z4), "EV08", "Cabo e mangueira deixados na rota de saida"),
        ("CAM_1P_EV09_Colega_Tontura", (28.4, 5.9, Z4 + E), (25.3, 4.9, Z4 + 1.2), "EV09", "Colega com tontura perto da borda"),
        ("CAM_1P_EV10_Protecao_Alterada", (30.4, 6.4, Z4 + E), (30.5, 4.1, Z4 + 0.55), "EV10", "Depois do intervalo: protecao alterada"),
        ("CAM_1P_EV11_Faz_So_Esse_Ultimo", (30.3, 4.08, Z4 + 1.22), (30.3, 1.6, 0.0), "EV11", "A condicao mudou (ex.: trabalhador abaixo)"),
        ("CAM_1P_EV12_Quase_Acidente_Retido", (26.6, 6.0, Z4 + E), (25.05, 4.2, Z4), "EV12", "Fragmento retido pelo rodape"),
        ("CAM_1P_EV13_Identificacao_Ilegivel", (30.6, 4.9, Z4 + E), (31.64, 4.18, Z4 + 1.15), "EV13", "Identificacao do ponto suja/ilegivel"),
        ("CAM_1P_EV14_Ferramenta_Defeituosa", TRAB, (29.55, 5.75, Z4 + 0.1), "EV14", "Ferramenta eletrica com cabo danificado"),
        ("CAM_1P_EV15_Impacto_Protecao", (27.2, 6.2, Z4 + E), (25.3, 4.1, Z4 + 0.9), "EV15", "CLANG! algo atinge a protecao proxima"),
        ("CAM_1P_EV16_Chuva", (29.4, 6.2, Z4 + E), (29.5, 3.0, Z4 - 0.6), "EV16", "Gotas leves: piso molhado"),
        ("CAM_1P_EV17_Alarme", (24.0, 12.0, Z4 + E), (20.4, 13.9, Z4 + 2.0), "EV17", "Alarme geral da obra"),
        ("CAM_1P_CONC_Suporte_Instalado", TRAB, (30.3, 4.45, Z4 + 0.05), "CONC", "Servico concluido: suporte instalado"),
        ("CAM_1P_ORG_Organizacao_Final", (28.9, 7.2, Z4 + E), (29.9, 5.0, Z4), "ORG", "Organizacao final antes de sair"),
        ("CAM_1P_RET_Descendo_Escada", (17.6, 16.5, Z(1) + E), (20.3, 16.4, 2.2), "RET", "Retorno pelo acesso previsto"),
        ("CAM_1P_RET_Chegada_Terreo", (23.6, 2.2, E), (23.3, -6.0, 1.3), "RET", "Chegada ao terreo"),
        ("CAM_1P_EMERG_Trabalhador_Suspenso", (19.5, -3.8, E), (-14.5, -10.2, 3.9), "EMERG", "Alarme: trabalhador suspenso em outra regiao da obra (Bloco B)"),
    ]


def cams_3p():
    return [
        ("CAM_3P_C07_Conferencia_Cinturao", (22.15, -24.55, 1.45), (20.35, -22.35, 1.0), 28, "C07", "Conferencia do cinturao vestido (roteiro pede 3a pessoa)"),
        ("CAM_3P_C08_Tropeco_Obstaculo", (27.8, -9.2, 1.9), (25.45, -7.2, 0.7), 28, "C08", "Escolha B: passou por cima e tropecou levemente"),
        ("CAM_3P_C11_Conseq_Abertura_Ignorada", (15.6, 12.5, Z3 + 1.9), (13.3, 14.8, Z3 + 0.6), 24, "CONSEQ", "ABERTURA_IGNORADA=SIM: outro trabalhador se aproxima da abertura (congelar)"),
        ("CAM_3P_C19_Desconectado_Escorrega", (27.9, 6.9, Z4 + 2.05), (30.0, 4.6, Z4 + 0.6), 28, "C19", "Escolha B: desconectou, deu alguns passos e escorregou (congelar antes da queda)"),
        ("CAM_3P_PRINC_Ferramenta_Retida", (31.6, 0.4, Z4 + 1.9), (30.3, 4.2, Z4 + 0.6), 30, "PRINC", "FERRAMENTAS_PROTEGIDAS=SIM: a chave fica retida"),
        ("CAM_3P_PRINC_Ferramenta_Area_Isolada", (26.9, -2.6, 1.8), (29.8, 2.1, 0.6), 28, "PRINC", "Ferramenta caiu dentro da area isolada - ninguem atingido"),
        ("CAM_3P_PRINC_Ferramenta_Pessoa_Abaixo", (25.5, -4.0, 0.6), (30.2, 3.0, 6.0), 18, "PRINC", "Ferramenta cai e um trabalhador passa abaixo (congelar antes do impacto, silencio)"),
        ("CAM_3P_CONSEQ_Material_Solto", (25.8, -3.0, 0.8), (28.1, 3.0, 6.5), 20, "CONSEQ", "MATERIAL_SOLTO=SIM: o objeto se desloca e cai"),
        ("CAM_3P_CONSEQ_Material_Retirado_Positivo", (27.0, 6.6, Z4 + 1.9), (28.0, 4.2, Z4 + 0.4), 28, "CONSEQ", "Consequencia positiva: o vento aumenta e o local esta livre"),
        ("CAM_3P_CONSEQ_Conexao_Incorreta", (27.2, 7.4, Z4 + 2.25), (30.0, 4.7, Z4 + 0.75), 24, "CONSEQ", "CONEXAO_INCORRETA=SIM: o ponto escolhido nao funciona como previsto (congelar)"),
        ("CAM_3P_CONSEQ_Equipamento_Danificado", (29.0, 6.4, Z4 + 1.45), (30.2, 4.75, Z4 + 1.05), 35, "CONSEQ", "CINTURAO/TALABARTE_DANIFICADO=SIM: o dano se torna critico (congelar)"),
        ("CAM_3P_CONSEQ_Guarda_Corpo_Problema", (27.0, 6.8, Z4 + 1.85), (28.2, 4.1, Z4 + 0.65), 28, "CONSEQ", "GUARDA_CORPO_PROBLEMA=SIM (sugestao a validar)"),
        ("CAM_3P_EV01_Vao_Aberto", (26.3, 7.4, Z4 + 1.85), (23.0, 4.1, Z4 + 0.65), 24, "EV01", "B/C: o guarda-corpo ficou aberto - a camera mostra o vao"),
        ("CAM_3P_EV02_Peca_Escapa", (24.5, -3.5, 2.2), (28.5, 1.5, 3.2), 24, "EV02", "B/C: pequena peca escapa com alguem na area (congelar)"),
        ("CAM_3P_EV03_Segundo_Objeto", (32.8, 1.8, Z4 + 2.45), (30.4, 4.3, Z4 + 1.15), 28, "EV03", "B/C: segundo objeto cai mais proximo (congelar)"),
        ("CAM_3P_EV04_Carga_Aproxima", (31.3, 8.9, Z4 + 2.45), (28.6, 6.3, Z4 + 0.55), 24, "EV04", "B/C: a carga se aproxima e um auxiliar entra na regiao (congelar)"),
        ("CAM_3P_EV05_Radio_Sem_Resposta", (31.3, 6.5, Z4 + 1.75), (30.3, 5.1, Z4 + 0.85), 28, "EV05", "B/C: mais tarde precisa de ajuda e o radio continua sem funcionar"),
        ("CAM_3P_EV06_Rajada_Desequilibrio", (32.6, 1.5, Z4 + 2.15), (30.3, 4.7, Z4 + 0.85), 28, "EV06", "B/C: perda de equilibrio, o sistema de protecao entra em acao (congelar)"),
        ("CAM_3P_EV06_A_Rajada_Forte", (27.0, 10.6, Z4 + 2.05), (28.6, 6.6, Z4 + 0.65), 24, "EV06", "A: parou antes; rajada ainda mais forte"),
        ("CAM_3P_EV08_Quase_Tropeco", (22.8, 11.2, Z4 + 1.85), (24.9, 12.85, Z4 + 0.55), 28, "EV08", "B/C: quase tropeca no cabo/mangueira"),
        ("CAM_3P_EV09_Colega_Desequilibrio", (27.0, 6.8, Z4 + 2.05), (25.25, 4.7, Z4 + 0.85), 28, "EV09", "B/C: o colega tenta continuar e fica desequilibrado (congelar)"),
        ("CAM_3P_EV10_Protecao_Alterada", (31.2, 6.8, Z4 + 1.85), (30.5, 4.1, Z4 + 0.65), 28, "EV10", "B: encontra a protecao alterada durante a atividade"),
        ("CAM_3P_EV11_Susto", (25.5, -4.0, 0.6), (30.2, 3.0, 6.0), 18, "EV11", "B: a situacao evolui - susto e congelar"),
        ("CAM_3P_EV12_Fragmento_Retido", (26.3, 5.6, Z4 + 0.85), (25.05, 4.2, Z4 + 0.05), 35, "EV12", "Fragmento retido pelas protecoes existentes"),
        ("CAM_3P_EV14_Ferramenta_Movimento", (31.2, 6.3, Z4 + 1.65), (30.3, 5.1, Z4 + 0.75), 28, "EV14", "B/C: a ferramenta para ou provoca movimento inesperado (congelar, sem lesao)"),
        ("CAM_3P_EV15_Protecao_Deslocada", (26.8, 6.6, Z4 + 1.85), (25.3, 4.1, Z4 + 0.65), 28, "EV15", "B: mais tarde a protecao apresenta movimento"),
        ("CAM_3P_EMERG_A_Equipe_Resgate", (-10.5, -13.5, 4.5), (-15.2, -10.2, 4.6), 24, "EMERG", "A: procedimento acionado, equipe preparada executa o resgate"),
        ("CAM_3P_EMERG_B_Subir_Sozinho", (-11.0, -7.2, 2.6), (-14.8, -7.4, 3.2), 24, "EMERG", "B: subir sozinho para puxa-lo - pare"),
        ("CAM_3P_EMERG_C_Qualquer_Pessoa", (-11.0, -7.2, 2.6), (-14.8, -7.4, 3.2), 24, "EMERG", "C: pedir para qualquer pessoa ajudar"),
        ("CAM_3P_EMERG_D_Aguardando", (-9.0, -10.0, 1.8), (-14.55, -10.2, 3.3), 28, "EMERG", "D: apenas chamar ambulancia - o trabalhador continua suspenso"),
    ]


# maos em 1a pessoa (parentadas nas cameras)
MAOS = [
    ("MAOS_1P_C05_Tablet_Permissao", "CAM_1P_C05_Tablet_Informacoes", "tablet_pt", True),
    ("MAOS_1P_C04_Tablet_Semana_Passada", "CAM_1P_C05_Tablet_Informacoes", "tablet_pt_semana_passada", False),
    ("MAOS_1P_C21_Chave", "CAM_1P_C21_Inicio_Tarefa", "chave", True),
    ("MAOS_1P_PRINC_Mao_Solta_Chave", "CAM_1P_PRINC_Chave_Escapa", "vazio", True),
    ("MAOS_1P_EV05_Radio", "CAM_1P_EV05_Radio_Sem_Resposta", "radio", True),
    ("MAOS_1P_EMERG_Radio", "CAM_1P_EMERG_Trabalhador_Suspenso", "radio", False),
]

# gatilhos: (nome, centro, meia-dimensao (x, y, z), cena)
def gatilhos():
    return [
        ("TRG_C01_Portaria", (27.1, -26.8, 1.0), (1.2, 1.2, 1.1), "C01"),
        ("TRG_C02_C05_Encarregado", (26.2, -22.0, 1.0), (1.4, 1.4, 1.1), "C02"),
        ("TRG_C06_C07_Area_Equipamentos", (19.4, -23.6, 1.0), (1.3, 2.0, 1.1), "C06"),
        ("TRG_C08_Obstaculo", (26.1, -9.2, 1.0), (1.2, 1.5, 1.1), "C08"),
        ("TRG_C09_Acesso", (24.8, -1.9, 1.0), (1.3, 1.1, 1.1), "C09"),
        ("TRG_C10_Pav02_Patamar", (17.05, 15.0, Z(2) + 1.0), (0.7, 0.9, 1.1), "C10"),
        ("TRG_C11_Pav03_Patamar", (17.05, 15.0, Z3 + 1.0), (0.7, 0.9, 1.1), "C11"),
        ("TRG_C12_Chegada_Pav04", (28.3, 9.4, Z4 + 1.0), (1.2, 1.2, 1.1), "C12"),
        ("TRG_C13_C19_Frente_Trabalho", (29.6, 5.6, Z4 + 1.0), (2.1, 1.6, 1.1), "C13"),
        ("TRG_C21_Posicao_Suporte", (30.3, 5.2, Z4 + 0.6), (0.6, 0.5, 0.7), "C21"),
        ("TRG_EXPOSICAO_Zona_Risco_Queda", (29.4, 5.0, Z4 + 1.0), (2.3, 1.0, 1.1), "C19"),
        ("TRG_ORG_Saida_Frente", (28.45, 8.2, Z4 + 1.0), (0.8, 1.0, 1.1), "ORG"),
        ("TRG_RET_Terreo_Saida", (23.6, 2.3, 1.0), (1.0, 1.4, 1.1), "RET"),
        ("TRG_EMERG_Observacao", (19.5, -3.8, 1.0), (1.2, 1.2, 1.1), "EMERG"),
    ]


def rota():
    R = {}
    R["R01_Portaria_Encarregado"] = [(27.15, -29.0, 0), (27.1, -26.8, 0), (26.6, -23.2, 0), (26.35, -21.9, 0)]
    R["R02_Encarregado_Equipamentos"] = [(26.35, -21.9, 0), (22.3, -21.2, 0), (20.4, -22.4, 0), (19.35, -23.85, 0)]
    R["R03_Equipamentos_Acesso"] = [(19.35, -23.85, 0), (21.0, -21.0, 0), (26.45, -20.2, 0), (26.25, -10.5, 0), (25.7, -3.2, 0), (24.85, -1.9, 0)]
    R["R04_Acesso_Escada_Terreo"] = [(24.85, -1.9, 0), (23.6, 0.9, 0), (23.6, 5.0, 0.15), (23.6, 12.8, 0.15), (15.6, 12.8, 0.15), (15.6, 14.95, 0.15), (17.05, 14.95, 0.15)]
    esc = []
    for n in range(0, 4):
        z0 = Z(n)
        esc += [(17.05, 14.95, z0), (19.55, 14.9, z0 + 1.5), (20.6, 15.7, z0 + 1.5), (19.55, 16.5, z0 + 1.5), (17.05, 16.5, z0 + 3.0)]
    R["R05_Escada_Terreo_Pav04"] = esc + [(17.05, 14.95, Z4)]
    R["R06_Pav04_Nucleo_Frente"] = [(17.05, 14.95, Z4), (15.6, 14.95, Z4), (15.6, 12.8, Z4), (28.45, 12.8, Z4), (28.45, 7.8, Z4), (28.9, 6.6, Z4), (30.3, 5.2, Z4)]
    R["R07_Retorno_Frente_Terreo"] = list(reversed(R["R06_Pav04_Nucleo_Frente"])) + list(reversed(esc)) + list(reversed(R["R04_Acesso_Escada_Terreo"]))[:-1]
    R["R08_Terreo_Observacao_Emergencia"] = [(23.6, 0.9, 0), (22.0, -2.4, 0), (19.5, -3.8, 0)]
    R["R09_Emergencia_Ponto_Encontro"] = [(19.5, -3.8, 0), (25.7, -3.2, 0), (26.25, -10.5, 0), (26.45, -20.2, 0), (23.0, -22.5, 0)]
    return R


def _camera(nome, C, loc, alvo, lens, props, parent=None):
    cd = bpy.data.cameras.new(nome)
    cd.lens = lens
    cd.sensor_width = 36.0
    cd.sensor_fit = 'HORIZONTAL'
    cd.clip_start = 0.03
    cd.clip_end = 900.0
    o = bpy.data.objects.new(nome, cd)
    C.objects.link(o)
    o.location = loc
    d = Vector(alvo) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    for k, v in props.items():
        o[k] = v
    if parent:
        o.parent = parent
    return o


def _limpar_antigos():
    removidos = []
    for o in list(bpy.data.objects):
        n = o.name
        if n.startswith("PT_") or any(n.startswith("CAM_%02d_" % i) for i in range(5, 14)) or n in ("TMP_TOP", "TMP_CAM_TESTE"):
            removidos.append(n)
            bpy.data.objects.remove(o, do_unlink=True)
    c = bpy.data.collections.get("30_Pontos_Treinamento")
    if c and len(c.all_objects) == 0:
        bpy.data.collections.remove(c)
    for cd in list(bpy.data.cameras):
        if cd.users == 0:
            bpy.data.cameras.remove(cd)
    return removidos


def maos(nome, cam, item, uvt):
    mb = MB()
    if item.startswith("tablet"):
        base = PG.maos_1p(None, None, pose_1p="tablet")
        mb.merge(base)
        with mb.at(M=Matrix.Translation(Vector((0.0, -0.165, -0.43))) @ Euler((math.radians(-21), 0, 0), 'XYZ').to_matrix().to_4x4()):
            mb.box((-0.17, -0.112, -0.01), (0.17, 0.112, 0.0), "preto_radio")
            G40.decal(mb, uvt, item, (0.0, 0.0, 0.0), (0, 0, 1), 0.316, up=(0.0, 1.0, 0.0), off=0.0015)
    elif item == "chave":
        mb.merge(PG.maos_1p("chave_amarrada", None, pose_1p="chave"))
    elif item == "radio":
        mb.merge(PG.maos_1p("radio", None, pose_1p="radio"))
    elif item == "vazio":
        mb.merge(PG.maos_1p(None, None, pose_1p="chave"))
    else:
        mb.merge(PG.maos_1p(None, None, pose_1p="baixo"))
    return mb


def build():
    removidos = _limpar_antigos()
    K.coll(PAI)
    subs = {n: K.coll(n, PAI) for n in ("43a_Cameras_1a_Pessoa", "43b_Cameras_3a_Pessoa_Consequencias", "43c_Maos_1a_Pessoa", "43d_Gatilhos", "43e_Rota_Navegacao")}
    K.clear_coll(PAI)
    for cd in list(bpy.data.cameras):
        if cd.users == 0:
            bpy.data.cameras.remove(cd)
    uvt = G40.UVT()
    raiz = K.empty("TREINAMENTO_TRABALHO_ALTURA", subs["43d_Gatilhos"], (0, 0, 0), size=1.0, props={
        "treinamento": True, "roteiro": "Treinamento Interativo de Trabalho em Altura - Cenario principal: Canteiro de Obras",
        "modo_padrao": "1a pessoa", "terceira_pessoa": "somente consequencias (CAM_3P_*) e conferencia do cinturao (C07)",
        "dados": "roteiro_treinamento.json", "altura_olhos_m": E, "lente_1p_mm": LENTE_1P,
        "visibilidade": "use userData.visivel_inicial para montar o estado inicial"})
    ncam = {"1P": 0, "3P": 0}
    cams = {}
    for (nome, loc, alvo, cena, desc) in cams_1p():
        o = _camera(nome, subs["43a_Cameras_1a_Pessoa"], loc, alvo, LENTE_1P,
                    {"treinamento": True, "modo_camera": "1P", "cena": cena, "descricao": desc, "alvo": [round(v, 3) for v in alvo],
                     "altura_olhos_m": round(loc[2] - (Z4 if loc[2] > Z4 else (Z3 if loc[2] > Z3 else (Z(2) if loc[2] > Z(2) else (Z(1) if loc[2] > Z(1) else 0.0)))), 2)})
        cams[nome] = o
        ncam["1P"] += 1
    for (nome, loc, alvo, lens, cena, desc) in cams_3p():
        o = _camera(nome, subs["43b_Cameras_3a_Pessoa_Consequencias"], loc, alvo, lens,
                    {"treinamento": True, "modo_camera": "3P", "cena": cena, "descricao": desc, "uso": "consequencia", "alvo": [round(v, 3) for v in alvo]})
        cams[nome] = o
        ncam["3P"] += 1
    for (nome, cam, item, vis) in MAOS:
        mb = maos(nome, cam, item, uvt)
        o = K.finish(mb, nome, subs["43c_Maos_1a_Pessoa"], parent=cams[cam],
                     props={"treinamento": True, "visivel_inicial": False, "modo_camera": "1P", "camera": cam, "item": item,
                            "variante": "principal" if vis else "alternativa"})
        o.matrix_parent_inverse = Matrix.Identity(4)
        o.location = (0, 0, 0)
        o.rotation_euler = (0, 0, 0)
        G40.mostrar(o, True)
    for (nome, c, h, cena) in gatilhos():
        e = K.empty(nome, subs["43d_Gatilhos"], c, size=1.0, kind='CUBE', props={"treinamento": True, "tipo": "gatilho", "cena": cena,
                                                                            "meia_dimensao_m": list(h)})
        e.scale = h
        e.parent = raiz
    for rn, pts in rota().items():
        g = K.empty("NAV_" + rn, subs["43e_Rota_Navegacao"], (0, 0, 0), size=0.4, kind='SPHERE',
                    props={"treinamento": True, "tipo": "rota", "pontos": len(pts), "inicio": list(pts[0]), "fim": list(pts[-1])})
        g.parent = raiz
        for i, p in enumerate(pts):
            w = K.empty("NAV_%s_%02d" % (rn[:3], i), subs["43e_Rota_Navegacao"], p, size=0.25, kind='SINGLE_ARROW',
                        props={"treinamento": True, "tipo": "waypoint", "rota": rn, "ordem": i, "altura_olhos_m": E})
            w.parent = g
    return {"cameras": ncam, "removidos_antigos": len(removidos)}
