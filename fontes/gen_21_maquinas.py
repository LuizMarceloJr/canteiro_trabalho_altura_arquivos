# gen_21_maquinas.py - maquinas e veiculos posicionados no canteiro
import bpy, sys, math, random
K = sys.modules["sitekit"]
L = sys.modules["layout"]
V = sys.modules["veiculos"]
MB = K.MB


def place(mb, name, C, loc, rz=0.0, ry=0.0, props=None, parent=None):
    o = K.finish(mb, name, C, loc=loc, props=props, parent=parent)
    o.rotation_euler = (0.0, math.radians(ry), math.radians(rz))
    return o


def build():
    C = K.coll("21_Maquinas_Veiculos_Obra")
    K.clear_coll(C)
    P = lambda tipo, **kw: dict({"categoria": "maquina_veiculo", "tipo": tipo, "nr_ref": "NR-12 / NR-18"}, **kw)
    place(V.betoneira("branco"), "Veiculo_Caminhao_Betoneira_01", C, (-1.5, -2.0, 0.0), 0.0, props=P("caminhao_betoneira"))
    place(V.betoneira("laranja_caminhao"), "Veiculo_Caminhao_Betoneira_02", C, (34.8, -22.0, 0.0), 90.0, props=P("caminhao_betoneira"))
    x = 15.5
    zr = -L.CAVA_PROF + L.CAVA_PROF * (x - 7.0) / 16.0
    place(V.basculante("vermelho_caminhao", carregado=False), "Veiculo_Caminhao_Basculante_01", C, (x, -14.5, zr), 0.0,
          ry=-math.degrees(math.atan(L.CAVA_PROF / 16.0)), props=P("caminhao_basculante", situacao="aguardando_carga_na_rampa"))
    place(V.basculante("verde_caminhao", carregado=True), "Veiculo_Caminhao_Basculante_02", C, (35.8, -16.4, 0.0), -115.0,
          props=P("caminhao_basculante", situacao="saindo_carregado"))
    place(V.escavadeira(), "Maquina_Escavadeira_Hidraulica", C, (-2.0, -13.5, -L.CAVA_PROF), 180.0, props=P("escavadeira", situacao="escavando_fundo_da_cava"))
    place(V.mini_carregadeira(), "Maquina_Mini_Carregadeira", C, (4.0, -17.2, -L.CAVA_PROF), 30.0, props=P("mini_carregadeira"))
    place(V.rolo_compactador(), "Maquina_Rolo_Compactador", C, (-26.0, -20.5, 0.0), 0.0, props=P("rolo_compactador"))
    place(V.pa_carregadeira(), "Maquina_Pa_Carregadeira", C, (-19.0, 11.0, 0.0), -20.0, props=P("pa_carregadeira"))
    place(V.empilhadeira(True), "Maquina_Empilhadeira", C, (-31.0, 11.5, 0.0), 0.0, props=P("empilhadeira"))
    place(V.gerador(), "Equipamento_Gerador", C, (34.2, 3.6, 0.0), 0.0, props=P("gerador"))
    mb, ptop = V.pta_tesoura(2.6)
    place(mb, "Maquina_PTA_Plataforma_Tesoura", C, (-23.0, 0.9, 0.0), 0.0,
          props=P("PTA_plataforma_trabalho_aereo_tesoura", altura_plataforma_m=round(ptop, 2), nr_ref="NR-18 18.13 PTA / NR-35", interativo=True))
    for (nm, loc, rz, carga) in (("01", (-17.5, -0.3, 0.0), 40.0, "areia"), ("02", (5.0, -4.2, 0.0), -15.0, None),
                                 ("03", (22.5, 2.0, 0.0), 90.0, "concreto_fresco"), ("04_TorreA_Pav09", (12.0, 9.5, L.TA_Z(9)), 10.0, None),
                                 ("05_BlocoB_Pav02", (-27.5, -6.0, 6.15), 200.0, "argamassa")):
        place(V.carrinho_mao(carga), "Equipamento_Carrinho_Mao_" + nm, C, loc, rz, props=P("carrinho_de_mao"))

    # ---------------- guindaste movel (patolas estendidas) icando palete para a laje 2 do Bloco B
    grp = K.empty("GRP_Guindaste_Movel", C, (-12.0, 5.0, 0.0), rz=90.0, size=2.0,
                  props={"categoria": "maquina_veiculo", "tipo": "guindaste_telescopico_sobre_caminhao", "patolas": "totalmente estendidas sobre pranchoes",
                         "nr_ref": "NR-18 18.10 / NR-12", "interativo": True})
    ch, sup, tip = V.guindaste_movel(boom_ang=58.0, boom_len=21.0)
    K.finish(ch, "Guindaste_Movel_Chassi_Patolas", C, parent=grp)
    target = (-23.0, -8.0)
    piv_world = (-12.0, 5.0 - 3.5)
    ang = math.degrees(math.atan2(target[1] - piv_world[1], target[0] - piv_world[0]))
    rz_local = ang - 90.0
    osup = K.finish(sup, "Guindaste_Movel_Superestrutura_Lanca", C, parent=grp, loc=(-3.5, 0.0, 1.55), rz=rz_local,
                    props={"categoria": "maquina_veiculo", "parte": "superestrutura", "animavel": "rotation_euler.z"})
    tip_z = 1.55 + tip[2]
    hook_z = 10.2
    mb = MB()
    tx, tz = tip[0], tip[2]
    for dy in (-0.1, 0.1):
        mb.cyl((tx, dy, tz), (tx, dy, hook_z - 1.55 + 0.7), 0.012, "cinza_escuro", n=4, caps=False, smooth=False)
    hz = hook_z - 1.55
    mb.box((tx - 0.25, -0.2, hz), (tx + 0.25, 0.2, hz + 0.7), "amarelo_maquina")
    mb.strut((tx, 0.0, hz), (tx, 0.0, hz - 0.3), 0.08, "grafite")
    base_z = 7.6 - 1.55
    for (sx, sy) in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
        mb.strut((tx, 0.0, hz - 0.3), (tx + sx, sy, base_z + 1.0), 0.03, "laranja_seguranca", h=0.01)
    mb.box((tx - 0.55, -0.55, base_z), (tx + 0.55, 0.55, base_z + 0.13), "pallet")
    mb.box((tx - 0.5, -0.5, base_z + 0.13), (tx + 0.5, 0.5, base_z + 1.0), "filme_plastico", top="bloco_ceramico")
    mb.cyl((tx + 0.5, 0.5, base_z + 0.1), (tx + 0.9, 0.8, base_z - 0.95), 0.01, "amarelo_linha_vida", n=4, caps=False)
    K.finish(mb, "Guindaste_Movel_Cabo_Gancho_Carga", C, parent=osup,
             props={"categoria": "carga_icada", "tipo": "palete_blocos", "nr_ref": "NR-18 - isolamento da area de icamento", "interativo": True})
    return {"objetos": len(C.objects), "ponta_lanca_z": round(tip_z, 2)}
