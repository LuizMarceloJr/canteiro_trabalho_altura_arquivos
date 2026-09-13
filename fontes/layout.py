
CITY = (-240.0, -220.0, 240.0, 270.0)
RUAS_NS = [(-147.0, 10.0), (-49.0, 10.0), (49.0, 10.0), (147.0, 10.0)]   # (x do eixo, largura)
RUAS_LO = [(-131.0, 10.0), (-41.0, 14.0), (83.0, 10.0), (181.0, 10.0)]   # (y do eixo, largura)
ZR = -0.15                       # cota do asfalto (calcadas e canteiro em z = 0)
LOTE = (-40.0, -30.0, 40.0, 30.0)
QUADRA_OBRA = (-44.0, -34.0, 44.0, 78.0)
CAVA_FUNDO = (-7.0, -19.0, 7.0, -9.0)
CAVA_PROF = 3.0
RAMPA = (7.0, 23.0, -17.0, -12.0)          # x fundo, x topo, y0, y1
TORRE_A = (6.0, 4.0, 32.0, 22.0)
TORRE_A_PAV = 10
PE_DIREITO = 3.0
BLOCO_B = (-31.0, -14.0, -15.0, -2.0)
GRUA_AMARELA = (36.0, 13.0)
GRUA_VERMELHA = (-8.0, 18.0)
PORTAO = (28.0, 38.0)

# ---- detalhes da Torre A (adicionado no modulo da estrutura)
ELEVADOR = (0.5, 9.0, 6.0, 17.0)            # cercamento do elevador cremalheira (fachada oeste)
ELEV_CABINE_Y = 13.0
TA_XL = [6.0, 11.2, 16.4, 21.6, 26.8, 32.0]
TA_YL = [4.0, 10.0, 16.0, 22.0]
TA_LAJE = 0.12
TA_VIGA = (0.20, 0.50)
TA_ESCADA_VAO = (17.75, 14.15, 21.45, 17.25)
TA_ELEV1 = (16.55, 19.75, 18.95, 21.85)
TA_ELEV2 = (19.15, 19.75, 21.45, 21.85)
TA_SHAFT = (13.4, 14.4, 14.6, 15.6)          # shaft junto a porta oeste do nucleo (treinamento: C10/C11)
TA_FORMA_L10 = (21.6, 10.0, 32.0, 22.0)
ANDAIME = (8.0, 22.0)                        # extensao X do andaime fachadeiro (fachada sul) - vaos sul 04/05 livres

def TA_Z(n):
    return 0.15 + PE_DIREITO * n

def TA_PILAR(x, y):
    X0, Y0, X1, Y1 = TORRE_A
    w, d = 0.30, 0.60
    if y in (Y0, Y1):
        w, d = 0.60, 0.25
    if x in (X0, X1):
        w, d = 0.25, 0.60
    if x in (X0, X1) and y in (Y0, Y1):
        w, d = 0.35, 0.35
    cx = min(max(x, X0 + w / 2), X1 - w / 2)
    cy = min(max(y, Y0 + d / 2), Y1 - d / 2)
    return (cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2)


# ---- TREINAMENTO "Trabalho em Altura" (roteiro): frente de trabalho no 4o pavimento, canto sudeste
TR_PAV = 4
TR_PORTA_OESTE_NUCLEO = (14.35, 15.55)      # vao (y0, y1) na parede oeste do nucleo da escada, pav 0 a 4
TR_GCR_SPLIT = {"Sul_04": 24.2, "Sul_05": 29.35}   # GcR dos vaos sul 04 e 05 do pav 4 em dois trechos (a/b)
TR_SUPORTE = (30.3, 4.52)                    # suporte a ser fixado junto a borda (laje do pav 4)
TR_ANCORAGEM = (31.64, 4.18, 1.45)           # ponto de ancoragem PA-04-01: face oeste do pilar de canto (x, y, altura)
TR_ISOLAMENTO = (26.3, -0.9, 32.6, 3.95)     # area a isolar no terreo, abaixo da frente de trabalho
TR_COBERTURA_ACESSO = (22.6, 1.2, 24.6, 3.98)  # acesso previsto de pedestres (coberto) - vao sul 04 do terreo
TR_ESCADA_PORTATIL_X = 25.26                 # escada portatil (atalho) apoiada na janela do pav 1
TR_AREA_EQUIP = (13.8, -25.9, 19.8, -21.6)   # area de equipamentos (frente ao almoxarifado)
TR_ENCARREGADO = (25.0, -22.2)               # encontro com o encarregado (C02-C05)
TR_MUNCK = (33.8, -9.6)                      # caminhao munck descarregando (C01, a direita; livre da rota de pedestres e da visada do Bloco B)
TR_BLOCOB_VITIMA = (-14.55, -10.2)           # emergencia final: trabalhador suspenso (fachada leste do Bloco B)
