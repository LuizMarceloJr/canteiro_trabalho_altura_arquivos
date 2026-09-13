# _carregar_geradores.py - registra a biblioteca e os geradores do cenario (rode com Alt+P)
# Depois, no console Python:  import sys; sys.modules["gen_13"].build()
import bpy, sys, types

ORDEM = [
    ("sitekit", "sitekit.py"), ("layout", "layout.py"), ("gen_12", "gen_12_torreA_estrutura.py"),
    ("gen_13", "gen_13_torreA_protecoes.py"), ("veiculos", "veiculos.py"), ("gen_22", "gen_22_vivencia.py"),
    ("gen_00", "gen_00_vias.py"), ("gen_01_predios", "gen_01_predios.py"), ("gen_02_03", "gen_02_03_cidade.py"),
    ("gen_10", "gen_10_perimetro.py"), ("gen_11", "gen_11_terreno.py"), ("gen_14_15", "gen_14_15_andaime_elevador.py"),
    ("gen_16_17", "gen_16_17_blocoB.py"), ("gen_20", "gen_20_gruas.py"), ("gen_21", "gen_21_maquinas.py"),
    ("gen_23", "gen_23_centrais_estoque.py"), ("gen_24", "gen_24_sinalizacao.py"),
    ("personagens", "personagens.py"), ("gen_40", "gen_40_treino_cenario.py"),
    ("gen_41", "gen_41_treino_personagens.py"), ("gen_42", "gen_42_treino_eventos.py"),
    ("gen_43", "gen_43_treino_cameras.py"), ("treino_estados", "treino_estados.py"),
    ("gen_99", "gen_99_exportar_glb.py"),
]
for nome, texto in ORDEM:
    src = bpy.data.texts[texto].as_string()
    if nome == "gen_99":
        src = src.replace('if __name__ == "__main__":', 'if False:')
    m = types.ModuleType(nome)
    exec(compile(src, texto, "exec"), m.__dict__)
    sys.modules[nome] = m
print("Geradores carregados:", ", ".join(n for n, _ in ORDEM))
