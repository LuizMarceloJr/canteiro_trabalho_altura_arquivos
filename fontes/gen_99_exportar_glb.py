# gen_99_exportar_glb.py - exporta o cenario para glTF binario (Three.js r128)
# Uso: rode este texto no Text Editor (Alt+P). Ajuste as opcoes abaixo.
import bpy, os, sys, time

INCLUIR_CIDADE_DISTANTE = True      # coleção 01b_Cidade_Distante
INCLUIR_VEICULOS_CIDADE = True      # coleção 03_Cidade_Veiculos
INCLUIR_CAMERAS = True
INCLUIR_VARIANTES_TREINO = True   # exporta tambem os objetos com visivel_inicial=False (variantes do roteiro)
NOME_ARQUIVO = "canteiro_trabalho_altura.glb"


def desktop():
    K = sys.modules.get("sitekit")
    if K:
        return K.desktop()
    return os.path.join(os.path.expanduser("~"), "Desktop")


def exportar(draco=False, nome=None):
    """draco=True gera a versao comprimida que o jogo carrega (canteiro_trabalho_altura_draco.glb)."""
    vl = bpy.context.view_layer
    if nome is None:
        nome = NOME_ARQUIVO.replace(".glb", "_draco.glb") if draco else NOME_ARQUIVO
    alvo = os.path.join(desktop(), "canteiro_trabalho_altura_arquivos", nome)
    os.makedirs(os.path.dirname(alvo), exist_ok=True)
    ocultar = []
    if not INCLUIR_CIDADE_DISTANTE:
        ocultar.append("01b_Cidade_Distante")
    if not INCLUIR_VEICULOS_CIDADE:
        ocultar.append("03_Cidade_Veiculos")

    def find_lc(lc, name):
        if lc.collection.name == name:
            return lc
        for ch in lc.children:
            r = find_lc(ch, name)
            if r:
                return r
        return None
    estados = []
    for nm in ocultar:
        lc = find_lc(vl.layer_collection, nm)
        if lc:
            estados.append((lc, lc.exclude))
            lc.exclude = True
    # variantes do treinamento: estao ocultas no viewport (estado inicial da cena),
    # mas precisam ir para o .glb - o Three.js liga/desliga por userData.visivel_inicial
    ocultos = []
    if INCLUIR_VARIANTES_TREINO:
        fila, vistos = [], set()
        for ob in bpy.data.objects:
            if "visivel_inicial" not in ob:
                continue
            for q in [ob] + list(ob.children_recursive):   # as pecas dos personagens tambem
                if q.name not in vistos:
                    vistos.add(q.name); fila.append(q)
        for ob in fila:
            try:
                oculto_vl = ob.hide_get()
            except RuntimeError:
                oculto_vl = None
            if oculto_vl or ob.hide_viewport:
                ocultos.append((ob, oculto_vl, ob.hide_viewport))
                ob.hide_viewport = False
                if oculto_vl:
                    ob.hide_set(False)
    t0 = time.time()
    try:
        bpy.ops.export_scene.gltf(
            filepath=alvo, export_format='GLB', use_selection=False, use_visible=True, use_renderable=False,
            use_active_collection=False, export_extras=True, export_cameras=INCLUIR_CAMERAS, export_lights=False,
            export_apply=True, export_yup=True, export_normals=True, export_tangents=False,
            export_materials='EXPORT', export_image_format='AUTO', export_animations=True,
            export_force_sampling=True, export_frame_range=True,
            export_draco_mesh_compression_enable=bool(draco), export_draco_mesh_compression_level=6,
            export_draco_position_quantization=13, export_draco_normal_quantization=9,
            export_draco_texcoord_quantization=11,
            export_gpu_instances=False, export_unused_images=False, export_unused_textures=False,
            export_hierarchy_flatten_objs=False, will_save_settings=False)
    finally:
        for ob, oculto_vl, hv in ocultos:
            ob.hide_viewport = hv
            if oculto_vl:
                try:
                    ob.hide_set(True)
                except RuntimeError:
                    pass
        for lc, ex in estados:
            lc.exclude = ex
    return alvo, round(time.time() - t0, 1), os.path.getsize(alvo), len(ocultos)


if __name__ == "__main__":
    print(exportar())
    print(exportar(draco=True))
