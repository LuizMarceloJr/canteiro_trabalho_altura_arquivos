# Cenário 3D — Canteiro de Obras | Trabalho em Altura (TRAINING SIM)

Cenário low-poly (estilo das imagens de referência) montado no Blender 5.2 para o treinamento interativo de **Trabalho em Altura**. Serve para exportar `.glb` para o Three.js (r128) e para renderizar cinemáticas no próprio Blender.

> Estado atual: canteiro **em conformidade** (proteções instaladas) + o roteiro do treinamento montado sobre ele. Cada proteção é um objeto separado e nomeado, e cada variante do roteiro (proteção removida, equipamento danificado, consequência congelada) é um objeto próprio que nasce desligado — ver §11.
>
> **Câmera: o treinamento inteiro é em 1ª pessoa.** A câmera só vai para 3ª pessoa para mostrar a **consequência** de uma escolha (e na Cena 07, onde o próprio roteiro pede que o jogador se veja vestindo o cinturão).

---

## 1. Arquivos

| Arquivo | Conteúdo |
|---|---|
| `Área de Trabalho/canteiro_trabalho_altura.blend` | Cena completa (texturas embutidas, scripts geradores dentro do arquivo) |
| `canteiro_trabalho_altura_arquivos/canteiro_trabalho_altura.glb` | Exportação glTF binária sem compressão (~23,9 MB) |
| `canteiro_trabalho_altura_arquivos/canteiro_trabalho_altura_draco.glb` | Mesma cena com compressão Draco (~2,7 MB) — recomendada para web |
| **`canteiro_trabalho_altura_arquivos/roteiro_treinamento.json`** | **O roteiro inteiro em dados**: cenas, escolhas, falas da IA, variáveis, 17 eventos + regras de sorteio, consequências, relatório e telas finais — cada item já apontando para a câmera e os objetos do `.glb` |
| `canteiro_trabalho_altura_arquivos/texturas/T_Placas.png` + `T_Placas_uv.json` | Atlas das placas de sinalização (editável) e mapa de UV de cada placa |
| `canteiro_trabalho_altura_arquivos/texturas/T_Treinamento.png` + `treino_uv.json` | Atlas das telas/placas do treinamento (tablet, PT, etiquetas, rotas de fuga) |
| `canteiro_trabalho_altura_arquivos/renders/` | 8 renders 1920×1080 do canteiro |
| `canteiro_trabalho_altura_arquivos/renders/storyboard/` | 77 quadros 1280×720 — um por cena/evento/consequência do roteiro |
| `canteiro_trabalho_altura_arquivos/fontes/` | Cópia em disco de todos os scripts geradores (os mesmos que estão dentro do `.blend`) + `roteiro_json.py` e `acentos.py`, que rodam fora do Blender |

## 2. Convenções

- **Escala:** 1 unidade = 1 metro. **Eixos no Blender:** X = leste, Y = norte, Z = cima (o glTF sai com Y para cima).
- **Origem:** centro do lote do canteiro (80 × 60 m). Canteiro e calçadas no nível 0; asfalto a −0,15 m.
- **Nomes:** sem acentos, espaços ou pontos → funcionam direto com `scene.getObjectByName()`.
- **Propriedades personalizadas** (viram `object.userData` no Three.js): `categoria`, `tipo`, `pavimento`, `face`, `nr_ref`, `interativo`, `descricao` etc. 545 nós têm `userData`.
- **Grupos:** objetos agrupados por empties `GRP_*` (ex.: `GRP_Grua_Amarela_Giro`).

## 3. Materiais e cores (baixo custo no Three.js)

Todas as cores vêm de **uma textura de paleta** (`T_Paleta`, 128×128, 16×16 células): cada face aponta a UV para a célula da sua cor. Resultado: só 8 materiais na cena inteira.

| Material | Uso | Modo glTF |
|---|---|---|
| `M_Paleta` | Quase toda a geometria | OPAQUE |
| `M_Paleta_Vidro` | Vidros de prédios, cabines e veículos (mais brilhante) | OPAQUE |
| `M_Paleta_Emissivo` | Lâmpadas, balizamento das gruas, semáforos | OPAQUE + emissive |
| `M_Placas` | Atlas das placas (`T_Placas`) | OPAQUE |
| `M_Tela_GcR` | Tela laranja dos guarda-corpos e cancelas | MASK (alphaTest 0,5) |
| `M_Rede_Seguranca` | Redes (SLQA), cercados de grua/elevador, portões | MASK |
| `M_Tela_Fachada` | Tela azul do andaime fachadeiro | BLEND |
| `M_Vidro_Transparente` | Vidro do ponto de ônibus | BLEND |

Para recolorir algo: pinte a célula correspondente em `T_Paleta` (afeta tudo que usa a cor) ou mova as UVs da face para outra célula.

## 4. Planta do canteiro (coordenadas em metros)

| Elemento | Posição / dimensões |
|---|---|
| Lote do canteiro | X −40…40, Y −30…30 (tapume h = 2,2 m) |
| Avenida (4 faixas) | ao sul, eixo Y = −41 |
| Portão de veículos + lava-rodas | fachada sul, X 28…38 |
| Acesso de pedestres (catraca) e portaria | X 26,5…28 / portaria em X ≈ 23,6 |
| **Torre A** (10 pavimentos, pé-direito 3 m) | X 6…32, Y 4…22; laje do pav. n em Z = 0,15 + 3n (pav. 9 = 27,15 m) |
| Andaime fachadeiro (fachada sul) | X 8…30, 7 plataformas a cada 2 m, tela até 16 m |
| Elevador de cremalheira (fachada oeste) | mastro em X 2, Y 13; cabine no pav. 6 |
| **Bloco B** (2 lajes executadas) | X −31…−15, Y −14…−2 |
| Cava (3 m, taludes 1:1) + rampa | fundo X −7…7, Y −19…−9; rampa X 7…23 |
| Grua amarela (47 m, lança 45 m) | base X 36, Y 13 |
| Grua vermelha/branca (36 m, lança 40 m) | base X −8, Y 18 |
| Guindaste móvel (patolas estendidas) | X −12, Y 5, içando palete para a laje 2 do Bloco B |
| Áreas de vivência | faixa sul: vestiário, sanitários, refeitório, banheiros químicos, DDS, almoxarifado/EPI, portaria |
| Escritório de obra (2 níveis) | fachada leste, X 38,5, Y −10…2 |
| Centrais de armação e carpintaria, estoque | quadrante noroeste |

## 5. Coleções

| Coleção | Conteúdo |
|---|---|
| `00_Terreno_Vias` | Asfalto, calçadas, meio-fio, faixas, faixas de pedestre, bueiros |
| `01_Cidade_Predios` | 32 prédios detalhados do entorno, estacionamento, praça |
| `01b_Cidade_Distante` | Quadras distantes simplificadas (pode ser excluída na exportação) |
| `02_Cidade_Mobiliario` | Postes, árvores, semáforos, balizadores, ponto de ônibus, orelhão, lixeiras de reciclagem |
| `03_Cidade_Veiculos` | 93 carros, ônibus, caminhão de entrega no portão oeste |
| `10_Canteiro_Perimetro` | Tapume, portões, catraca, saída de emergência, placa de obra, torres de iluminação |
| `11_Canteiro_Terraplenagem` | Terreno do canteiro, cava com taludes facetados, montes de terra |
| `12_TorreA_Estrutura` | Lajes, vigas, pilares, poços, escadas, alvenaria (pav. 0–5), escoramentos, fôrmas e armaduras do topo |
| `13_TorreA_Protecoes` | GcR por vão, vão da escada, topo dos poços, borda da fôrma, redes SLQA, fechamentos, tampões, ancoragens, linha de vida |
| `14_TorreA_Andaime` | Andaime fachadeiro por nível, escadas internas, ancoragens, tela |
| `15_TorreA_Elevador_Cremalheira` | Mastro, cercado, cobertura, rampas + cancelas (pav. 1–9), cabine |
| `16_BlocoB_Estrutura` / `17_BlocoB_Protecoes` | Estrutura, materiais e betoneira / GcR, torre de acesso, escada de mão |
| `20_Gruas` | Duas gruas completas com cargas (caçamba de concreto e feixe de vigas) |
| `21_Maquinas_Veiculos_Obra` | Betoneiras, basculantes, escavadeira, mini-carregadeira, pá carregadeira, rolo, empilhadeira, PTA tesoura, gerador, carrinhos, guindaste móvel |
| `22_Areas_Vivencia` | Contêineres, DDS, banheiros químicos, caixa d'água, caçambas, tubo coletor de entulho |
| `23_Centrais_Estoque_Materiais` | Galpões, vergalhões, paletes, cimento, big bags, escoras, tubos de concreto, contêineres marítimos, baias, QGD |
| `24_Sinalizacao_Seguranca` | 45 placas + placas dos poços/pavimentos, extintores, proteção da cava, cones, estação de EPI |
| `30_Pontos_Treinamento` | 15 marcadores `PT_*` (setas) para ancorar o roteiro |
| `90_Cameras` / `91_Iluminacao` | 15 câmeras / sol |

## 6. Itens de segurança modelados (referências NR-18 / NR-35)

- **Guarda-corpo e rodapé (GcR):** travessão superior a 1,20 m, intermediário a 0,70 m, rodapé de 0,20 m e tela nos vãos (NR-18 18.9.4.2). Na Torre A: pav. 5 (faces sem alvenaria) e pav. 6–9, vão da escada (pav. 5–9), topo dos poços (pav. 9) e bordas da fôrma da laje 10. No Bloco B: pav. 1–2 e abertura da laje 2. Também na borda da cava e nas rampas do elevador.
- **Rede de segurança tipo forca (SLQA):** fachada leste, pav. 7–9, com rodapés (NR-18 18.9.4.4).
- **Aberturas:** fechamento provisório das portas dos poços de elevador (pav. 0–9) e tampões travados nos shafts (NR-18 18.9.2 / 18.9.3).
- **Ancoragem:** 16 pontos de ancoragem no pav. 9 (1.500 kgf) e linha de vida horizontal nas faces sul e oeste (NR-18 18.12.12 / NR-35).
- **Andaime fachadeiro:** forração completa, GcR externo com rodapé, escada interna com alçapão, ancoragem na estrutura e tela desde a 1ª plataforma até 2 m acima da última (NR-18 18.12).
- **Elevador de passageiros (obra ≥ 24 m):** cancelas de 1,80 m com intertravamento, rampas com proteção, cercado da base e cobertura contra queda de materiais (NR-18 18.11).
- **Gruas:** cercado da base, escada interna com linha de vida vertical e trava-quedas, plataformas de descanso, luzes de balizamento, cargas com cabo-guia.
- **Escavação:** taludes 1:1, rampa ~19%, GcR nas bordas, barreiras plásticas, escada de acesso, pilhas afastadas da borda.
- **Escada de mão (Bloco B):** 75°, ultrapassa 1 m o piso e amarrada no topo (NR-18 18.8.6.13).
- **Outros:** PTA tesoura com guarda-corpo, isolamento da área de içamento (cones + fita), estação de EPI com cintos paraquedista + talabarte duplo e capacetes, área de DDS com quadro, ponto de encontro, extintores (inclusive em todos os pavimentos da Torre A), saída de emergência, placa de obra e sinalização em PT-BR.

## 7. Câmeras

| Câmera | Uso |
|---|---|
| `CAM_00_Cinematica_Abertura` | Travelling animado (frames 1–300, 30 fps) com alvo `ALVO_CAM_00_Abertura` |
| `CAM_01` … `CAM_04` | Vistas equivalentes às 4 imagens de referência |
| `CAM_05` … `CAM_13` | Pontos de vista do trabalhador: portaria, DDS, EPI, elevador, andaime, borda do pav. 9, fôrma/carga suspensa, cava, escada de mão |
| `CAM_14_Operador_Grua_Amarela` | Visão do operador (filha do giro da grua) |
| **`CAM_1P_*` (46)** | **Câmeras do treinamento em 1ª pessoa** — uma por cena/evento. Lente 20 mm (FOV horizontal 84°), olhos a 1,62 m em pé e 1,00 m ajoelhado |
| **`CAM_3P_*` (30)** | **Somente consequências** — a câmera sai da 1ª pessoa para mostrar o resultado de uma escolha, e volta. Lente de 18 a 35 mm conforme o enquadramento |
| **`MAOS_1P_*` (6)** | Mãos/antebraços do jogador, *parentados* na câmera 1P correspondente (tablet, chave, rádio, mão que soltou a chave). Ficam desligados até a cena pedir |

## 8. Partes animáveis

- Gruas: `GRP_Grua_*_Giro` (rotação Z), `Grua_*_Carro_Trole` (location.x), `Grua_*_Cabos_Aco` (scale.z = comprimento do cabo), `Grua_*_Moitao_Gancho` (location.z).
- Guindaste móvel: `Guindaste_Movel_Superestrutura_Lanca` (rotação Z).
- Elevador: `TorreA_Elevador_Cabine` (location.z; as cotas dos pavimentos estão em `userData.cotas_pavimentos`).

## 9. Integração no Three.js (r128)

```js
const loader = new THREE.GLTFLoader();
const draco = new THREE.DRACOLoader();
draco.setDecoderPath('js/libs/draco/');          // pasta examples/js/libs/draco do r128
loader.setDRACOLoader(draco);

const interativos = [];
loader.load('canteiro_trabalho_altura_draco.glb', (gltf) => {
  gltf.scene.traverse((o) => {
    if (o.isMesh) {
      o.castShadow = true;
      o.receiveShadow = true;
      if (o.material.map) o.material.map.anisotropy = 4;
    }
    if (o.userData && o.userData.interativo) interativos.push(o);
  });
  scene.add(gltf.scene);
  const pav9 = gltf.scene.getObjectByName('TorreA_Pav09_Linha_Vida_Horizontal');
});

renderer.outputEncoding = THREE.sRGBEncoding;   // a paleta foi pensada em sRGB
renderer.shadowMap.enabled = true;

// Luz equivalente ao sol do Blender (vindo do sudeste)
const sol = new THREE.DirectionalLight(0xfff4e6, 1.0);
sol.position.set(41, 72, 56);                    // direção do sol convertida para Y-up
sol.castShadow = true;
sol.shadow.mapSize.set(4096, 4096);
Object.assign(sol.shadow.camera, { left: -90, right: 90, top: 90, bottom: -90, near: 1, far: 300 });
scene.add(sol, new THREE.HemisphereLight(0xbcd8ff, 0xd9b48a, 0.65));
```

- Câmera em primeira pessoa: `near = 0.1`; vistas aéreas: `near = 1`. `far = 2000` cobre a cidade.
- Números da cena completa: ~346 mil triângulos, 834 nós, ~1.300 draw calls. Para aparelhos mais fracos: exporte sem `01b_Cidade_Distante` e `03_Cidade_Veiculos` (opções no script `gen_99_exportar_glb.py`) e/ou junte malhas estáticas não interativas por material.

## 10. Como editar ou regenerar

Os scripts ficam dentro do `.blend` (aba *Text Editor*): `sitekit.py` (biblioteca de modelagem), `layout.py` (coordenadas mestre), `veiculos.py` e um gerador por coleção (`gen_*.py`). Cada gerador **apaga e recria só a sua coleção**.

1. Abra `_carregar_geradores.py` no Text Editor e rode (Alt+P) — registra todos os módulos (inclusive `personagens`, `gen_40`…`gen_43` e `treino_estados`).
2. No console Python do Blender, rode o `build()` do gerador desejado, por exemplo:
   `import sys; sys.modules['gen_13'].build()`  (refaz as proteções da Torre A)
3. Para exportar de novo: rode `gen_99_exportar_glb.py` (ele revela temporariamente as variantes ocultas do treinamento, senão elas ficariam de fora do `.glb`).
4. Para refazer o `roteiro_treinamento.json`: `fontes/roteiro_json.py` (roda fora do Blender, junto com `fontes/acentos.py`) — `python roteiro_json.py roteiro_treinamento.json`.
5. Para refazer o storyboard: `import sys; sys.modules['treino_estados'].render_shots(0, 77)`.

> Edições feitas à mão numa coleção se perdem se o gerador dela for rodado de novo. Câmeras, sol, céu e ajustes de render foram configurados direto na cena (não têm gerador).
>
> Visual do render: EEVEE, transformação de cor **Standard** (as cores da paleta saem iguais às do Three.js com sRGB), sol com força 2,6 e céu em gradiente com nuvens procedurais.


---

## 11. Organização do treinamento (1ª pessoa / 3ª pessoa)

### 11.1 A regra da câmera

| Momento | Câmera | Exemplo |
|---|---|---|
| Todo o percurso, decisões, eventos | **1ª pessoa** `CAM_1P_*` | `CAM_1P_C18_Ponto_Conexao` |
| **Consequência** de uma escolha | **3ª pessoa** `CAM_3P_*`, e volta para a 1ª | `CAM_3P_C19_Desconectado_Escorrega` |
| Cena 07 (conferência do cinturão vestido) | 3ª pessoa — **exceção pedida pelo roteiro** | `CAM_3P_C07_Conferencia_Cinturao` |

No JSON, todo bloco de 3ª pessoa vem como `"consequencia": {"modo": "3P", "camera": …, "voltar_para": "1P"}`. Se `congelar: true`, a cena deve parar no quadro (é o “congelar antes do impacto” do roteiro).

### 11.2 Coleções do treinamento

| Coleção | O que tem |
|---|---|
| `40_Treino_Cenario` | Cenário do roteiro: rota de entrada e caminhão (40a), área de equipamentos e EPI com defeito (40b), aberturas dos pav. 2 e 3 (40c), frente de trabalho do pav. 4 (40d), isolamento do térreo (40e), sinalização de emergência (40f) |
| `41_Treino_Personagens` | 64 figurantes posados: ambiente (41a), pav. 4 (41b), pav. 3 (41c), térreo (41d), **avatar do jogador nas cenas de 3ª pessoa** (41e), emergência (41f) |
| `42_Treino_Eventos_Consequencias` | Objetos dos 17 eventos (42a), a chave que escapa nos 3 desfechos (42b), consequências das variáveis (42c), sobras da organização final (42d), emergência final (42e) |
| `43_Treino_Cameras_Gatilhos` | Câmeras 1P (43a) e 3P (43b), mãos em 1ª pessoa (43c), gatilhos `TRG_*` (43d), rota de navegação `NAV_*` (43e) |

### 11.3 Ligar e desligar as variantes

Todo objeto do treinamento tem `userData.visivel_inicial`. **101 objetos nascem desligados** (proteção removida, EPI danificado em uso, consequências congeladas, avatares). Eles **estão no `.glb`** — só chegam invisíveis.

```js
// 1) estado inicial, logo depois do load
gltf.scene.traverse(o => {
  if (o.userData && 'visivel_inicial' in o.userData) o.visible = !!o.userData.visivel_inicial;
});

// 2) a cada cena / escolha / consequência do JSON
function aplicar(passo) {
  (passo.ocultar || []).forEach(n => { const o = raiz.getObjectByName(n); if (o) o.visible = false; });
  (passo.mostrar || []).forEach(n => { const o = raiz.getObjectByName(n); if (o) o.visible = true; });
  if (passo.camera) trocarCamera(passo.camera);   // 1P ou 3P, conforme passo.modo
}
```

### 11.4 Percurso e gatilhos

- `TRG_*` são caixas (empties com `scale` = meia-dimensão em metros) que marcam onde cada cena começa: portaria, encarregado, área de equipamentos, obstáculo, acesso, patamares dos pav. 2 e 3, chegada ao pav. 4, frente de trabalho, posição do suporte, zona de risco de queda, saída e observação da emergência.
- `NAV_*` são as rotas sugeridas (R01…R09) em waypoints, para caminhada guiada ou para validar o caminho livre.

### 11.5 O que o `roteiro_treinamento.json` traz

- `cenas` (21) — C01 a C21, cada uma com câmera 1P, falas da IA, falas dos personagens, telas, escolhas, variáveis que cada escolha define e a categoria do relatório que ela alimenta.
- `eventos_inesperados` (17) — EV01 a EV17, com `peso`, pré-condições (`requer`) e a consequência em 3ª pessoa de cada escolha.
- `sorteio_de_eventos` — 3 a 5 por sessão, intervalo mínimo entre eventos, pares que não podem sair juntos, no máximo 2 eventos críticos, e três exemplos de execução (para a 2ª e a 3ª vez ficarem diferentes).
- `cena_principal` — a queda da chave, **obrigatória em toda sessão**, com os três desfechos conforme `FERRAMENTAS_PROTEGIDAS` e `AREA_INFERIOR_ISOLADA`.
- `consequencias` (8) — inclusive as **positivas** (material retirado da borda, isolamento que funcionou, comunicação restabelecida).
- `relatorio`, `resultados`, `final` — as 13 categorias do relatório, os três desfechos (bom desempenho / pontos a melhorar / erros críticos) e a tela final.
- `regras_tecnicas` (17) e `linguagem` — as regras de validação e o jeito de falar (frase curta, nome do trabalhador em `{{NOME}}`, nada de regra inventada como “choveu = proibido”).

Todo nome de câmera e de objeto citado no JSON foi conferido contra o `.blend`: **nenhuma referência quebrada**.

### 11.6 Onde cada cena acontece

| Cenas | Lugar no canteiro |
|---|---|
| C01 | Portão de pedestres (27, −26) olhando para o 4º pavimento |
| C02–C05 | Frente ao DDS, com o encarregado (25, −22) |
| C06–C07 | Área de equipamentos, em frente ao almoxarifado (14…20, −26…−22) |
| C08–C09 | Caminho até o acesso e escolha do acesso (25, −10 → 25, 2) |
| C10–C11 | Aberturas protegida (2º pav.) e deslocada (3º pav.), junto ao núcleo da escada |
| C12–C21, EV01–EV17 | Canto **sudeste do 4º pavimento** (z = 12,15), suporte em (30,3 / 4,5), ancoragem PA-04-01 no pilar de canto |
| Consequências da queda | Térreo abaixo da frente de trabalho, área a isolar (26…33, −1…4) |
| Emergência final | Fachada leste do Bloco B (−14,5 / −10,2) |
