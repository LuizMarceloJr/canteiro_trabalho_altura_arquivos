/* motor.js — a prova: percorre o roteiro, guarda as variáveis, sorteia os
   eventos, dispara as consequências e monta o relatório. */
(function (raiz) {
  'use strict';

  var M = {};
  var D, C3, U;
  var est = null;
  var camAnterior = null;

  M.iniciar = function (dados, cena3d, ui) { D = dados; C3 = cena3d; U = ui; };

  function zerar(nome) {
    est = {
      nome: nome, vars: {}, registro: [], relatorio: {}, criticos: [],
      eventos: [], feitos: {}, comecou: Date.now()
    };
    C3.estadoInicial();
    U.terceira(false); U.congelado(false); U.etapas(null);
    return est;
  }
  M.estado = function () { return est; };

  /* ---- relatório ---------------------------------------------------------- */
  function anotar(reg) {
    if (!reg) return;
    var atual = est.relatorio[reg.categoria];
    if (atual !== 'PRECISA_MELHORAR') est.relatorio[reg.categoria] = reg.resultado;
  }

  /* ---- aplicar um passo (cena, escolha ou consequência) ------------------- */
  function aplicarPasso(p) { C3.aplicar(p); }

  function defineVars(op) {
    var avisou = false;
    Object.keys(op.define || {}).forEach(function (v) {
      est.vars[v] = op.define[v];
      if (!avisou && D.lidaPor[v]) { U.registrado('Isso ficou registrado.'); avisou = true; }
    });
  }

  /* ---- consequência em 3ª pessoa ----------------------------------------- */
  /* objetos que, na consequência, precisam cair de verdade em vez de aparecer parados */
  var QUEDAS = {
    PRINC_Chave_Caida_Dentro_Area_Isolada: { altura: 12.0, seguir: true },
    PRINC_Chave_Caindo_Congelada_Sobre_Pessoa: { altura: 6.5, seguir: true, congelaNoFim: true },
    CONSEQ_Material_Solto_Caindo_Congelado: { altura: 5.0, seguir: true, congelaNoFim: true },
    CONSEQ_Material_Solto_No_Chao: { altura: 11.0, seguir: true },
    EV03_Objeto_02_Congelado_Mais_Proximo: { altura: 4.5, seguir: true, congelaNoFim: true },
    EV02_Peca_Escapa_Congelada: { altura: 5.5, seguir: true, congelaNoFim: true },
    EV12_Fragmento_Retido_Pelo_Rodape: { altura: 3.0, seguir: false }
  };

  /* peças do cenário que se mexem na consequência: nada de quadro parado */
  var MOVIMENTOS = {
    EV06_Lona_Batendo_Poeira: { tipo: 'tremor', dur: 3.4, amp: 0.17, freq: 1.5, eixo: 'z' },
    PRINC_Chave_Retida_Pelo_Cordao: { tipo: 'balanco', dur: 3.2, amp: 0.50, freq: 0.8, eixo: 'x' },
    CONSEQ_GcR_Sul05a_Cedendo: { tipo: 'inclinar', dur: 2.4, alvo: 0.22, amp: 0.04, eixo: 'x' },
    C13_GcR_Sul05a_Levemente_Solto: { tipo: 'tremor', dur: 2.0, amp: 0.045, freq: 2.4, eixo: 'x' },
    EV15_GcR_Sul04b_Deslocado_Depois: { tipo: 'ir', dur: 1.9, d: { x: 0.28, y: 0, z: 0.12 } },
    EV10_GcR_Sul05b_Travessao_Intermediario_Removido: { tipo: 'tremor', dur: 1.8, amp: 0.05, freq: 2.2, eixo: 'x' },
    EV04_Paleteira_Palete_Aproximando: { tipo: 'ir', dur: 3.0, d: { x: 1.5, y: 0, z: 2.8 } },
    EV01_Pecas_GcR_Retiradas_no_Piso: { tipo: 'tremor', dur: 1.4, amp: 0.06, freq: 3.0, eixo: 'y' },
    C11_Pav03_Abertura_Protecao_Deslocada: { tipo: 'ir', dur: 1.6, d: { x: 0.22, y: 0, z: 0.18 } },
    EV01_GcR_Sul04a_Removido_Vao_Aberto: { tipo: 'tremor', dur: 1.6, amp: 0.05, freq: 2.0, eixo: 'x' }
  };

  /** deixa a cena viva: quem está por perto olha para o jogador. */
  function encenar(nomes, forca) {
    var cam = C3.camera().position;
    (nomes || []).forEach(function (n) {
      var a = C3.ator(n);
      if (a && a.raiz.visible) a.olhar(cam, forca === undefined ? 0.85 : forca);
    });
  }

  /** faz o objeto cair de verdade, com a câmera acompanhando. */
  async function quedaReal(nome) {
    var cfg = QUEDAS[nome];
    var o = C3.porNome[nome];
    if (!cfg || !o) return false;
    var fim = o.position.y;
    o.visible = true;
    if (cfg.seguir) C3.seguir(o, { suav: 5 });
    if (cfg.congelaNoFim) { C3.camaraLenta(0.35, 3.2); U.lenta(true); }   // o instante crítico em câmera lenta
    await C3.cair(o, {
      de: { x: o.position.x, y: fim + cfg.altura, z: o.position.z },
      vy: 0.3, parar_em: fim
    });
    await U.esperar(600);
    C3.pararSeguir();
    C3.velocidadeNormal(); U.lenta(false);
    return true;
  }

  /* corpos que precisam encenar a queda / o desequilíbrio em vez de aparecer parados */
  var ENCENACAO = {
    AVATAR_C19_Desconectado_Escorrega: { clipes: ['andando', 'escorregando', 'queda_corpo'],
                                         tempos: [1.1, 1.3, 0], queda: { frente: 0.9, chao: -0.35 } },
    AVATAR_EV06_Desequilibrio_Sistema_Atua: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.4, 0],
                                              queda: { frente: 0.7, retido: -0.95 } },
    AVATAR_CONSEQ_Conexao_Incorreta_Tubulacao: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.2, 0],
                                                 queda: { frente: 0.6, chao: -1.6 } },
    AVATAR_CONSEQ_Conexao_Incorreta_Vergalhao: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.2, 0],
                                                 queda: { frente: 0.6, chao: -1.6 } },
    AVATAR_CONSEQ_Conexao_Incorreta_EstruturaMetalica: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.2, 0],
                                                        queda: { frente: 0.6, chao: -1.6 } },
    AVATAR_CONSEQ_Conexao_Incorreta_GuardaCorpo: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.2, 0],
                                                  queda: { frente: 0.6, chao: -1.6 } },
    AVATAR_CONSEQ_Cinturao_Danificado: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.3, 0],
                                         queda: { frente: 0.5, chao: -1.4 } },
    AVATAR_CONSEQ_Talabarte_Danificado: { clipes: ['desequilibrio', 'queda_corpo'], tempos: [1.3, 0],
                                          queda: { frente: 0.5, chao: -1.4 } },
    AVATAR_C08_Tropeco: { clipes: ['andando', 'tropecando', 'parado'], tempos: [1.0, 1.2, 0.8] },
    AVATAR_EV08_Quase_Tropeco: { clipes: ['andando', 'tropecando', 'parado'], tempos: [1.0, 1.1, 0.8] },
    AVATAR_EV11_Susto: { clipes: ['trabalhando', 'assustado', 'parado'], tempos: [0.9, 1.6, 0.6] },
    AVATAR_EV14_Ferramenta_Tranco: { clipes: ['trabalhando', 'desequilibrio', 'trabalhando'], tempos: [0.8, 1.3, 0.6] },
    AVATAR_EV05_Radio_Sem_Resposta: { clipes: ['radio'], tempos: [0] },
    AVATAR_EMERG_B_Subindo_Escada: { clipes: ['subindo'], tempos: [0] },
    NPC_EMERG_Trabalhador_Suspenso: { clipes: ['suspenso'], tempos: [0] },
    NPC_EV09_Colega_Desequilibrio: { clipes: ['tonto', 'desequilibrio'], tempos: [1.0, 0] },
    NPC_EV02_Dentro_Area_Isolada: { clipes: ['andando'], tempos: [0], passeio: { dx: 2.2, dz: 0.6, vel: 1.1 } },
    NPC_EV02_Afasta_Barreira_Entra: { clipes: ['empurrando', 'andando'], tempos: [1.4, 1.0], passeio: { dx: 1.6, dz: 1.0, vel: 0.9 } },
    AVATAR_C07_Cinturao_Correto: { clipes: ['vestindo', 'conferindo', 'vestindo'], tempos: [1.6, 1.3, 1.1] },
    AVATAR_C07_Erro_Fita_Torcida: { clipes: ['vestindo', 'conferindo', 'vestindo'], tempos: [1.6, 1.3, 1.1] },
    AVATAR_C07_Erro_Fivela_Aberta: { clipes: ['vestindo', 'conferindo', 'vestindo'], tempos: [1.6, 1.3, 1.1] },
    AVATAR_C07_Erro_Ajuste_Frouxo: { clipes: ['vestindo', 'conferindo', 'vestindo'], tempos: [1.6, 1.3, 1.1] },
    AVATAR_C07_Erro_Colocado_Invertido: { clipes: ['vestindo', 'conferindo', 'vestindo'], tempos: [1.6, 1.3, 1.1] },
    AVATAR_TAREFA_Ajoelhado_Conectado: { clipes: ['trabalhando', 'assustado', 'trabalhando'], tempos: [1.2, 1.4, 1.0] },
    AVATAR_PRINC_Chave_Escapou: { clipes: ['trabalhando', 'assustado', 'parado'], tempos: [0.9, 1.7, 0.8] },
    AVATAR_EV06_A_Parado_Area_Segura: { clipes: ['parado', 'assustado', 'parado'], tempos: [0.9, 1.5, 0.8] },
    AVATAR_ORG_Recolhendo_Ferramentas: { clipes: ['trabalhando', 'carregando'], tempos: [1.7, 1.1] },
    AVATAR_EMERG_A_Radio: { clipes: ['radio'], tempos: [0] },
    NPC_CONSEQ_Pav03_Trabalhador_Carregando: { clipes: ['andando_carregando', 'tropecando', 'assustado'],
                                               tempos: [1.7, 1.2, 1.0], passeio: { dx: 2.6, dz: 0.4, vel: 1.15 } },
    NPC_EV04_Operador_Paleteira_Aproximando: { clipes: ['andando_empurrando'], tempos: [0], passeio: { dx: 1.5, dz: 2.8, vel: 0.85 } },
    NPC_EV04_Auxiliar_Entra_Na_Area: { clipes: ['andando', 'conferindo'], tempos: [1.5, 0.9], passeio: { dx: -1.1, dz: 1.6, vel: 1.0 } },
    NPC_EV01_Colega_Retira_GcR: { clipes: ['trabalhando', 'carregando'], tempos: [1.7, 1.1] },
    NPC_EV12_Pedreiro_Cortando_Bloco: { clipes: ['serrando'], tempos: [0] }
  };

  /** encena o corpo: a sequência de clipes e, quando é o caso, a queda com gravidade. */
  async function encenarCorpo(nome) {
    var cfg = ENCENACAO[nome];
    var a = C3.ator(nome);
    if (!cfg || !a) return false;
    var o = C3.porNome[nome];
    if (o) o.visible = true;
    C3.seguirAtor(a);
    a.semRotina();
    if (cfg.passeio) {                        // o corpo caminha de verdade enquanto encena
      var p0 = a.raiz.position;
      a.andar([{ x: p0.x + (cfg.passeio.dx || 0), y: p0.y, z: p0.z + (cfg.passeio.dz || 0) }],
              cfg.passeio.vel || 1.0);
    }
    for (var i = 0; i < cfg.clipes.length; i++) {
      a.tocar(cfg.clipes[i]);
      a.t = 0;
      var dur = cfg.tempos[i];
      if (dur > 0) { await U.esperar(dur * 1000); continue; }
      if (cfg.queda) {
        C3.camaraLenta(0.3, 2.6); U.lenta(true);
        await a.cair(cfg.queda);
        C3.velocidadeNormal(); U.lenta(false);
      } else {
        await U.esperar(900);
      }
    }
    C3.pararSeguir();
    a.voltarRotina();
    return true;
  }

  /** ninguém fica de estátua: quem está perto reage e o instante vem em câmera lenta. */
  async function reacaoAoVivo() {
    var cam = C3.camera().position, perto = [];
    Object.keys(C3.atores).forEach(function (n) {
      var a = C3.atores[n];
      if (!a.raiz.visible) return;
      var d = a.raiz.position.distanceTo(cam);
      if (d < 18) perto.push({ a: a, d: d });
    });
    perto.sort(function (x, y) { return x.d - y.d; });
    var elenco = perto.slice(0, 6);
    elenco.forEach(function (p, i) {
      p.antes = p.a.clip;
      p.a.olhar(cam, 0.9);
      if (p.a.ehFigurante) return;            // o figurante segue no serviço dele, só olha
      p.a.tocar(i === 0 ? 'assustado' : 'conferindo');
      p.a.t = 0;
    });
    C3.camaraLenta(0.5, 2.6); U.lenta(true);
    await U.esperar(1700);
    C3.velocidadeNormal(); U.lenta(false);
    elenco.forEach(function (p) { if (!p.a.ehFigurante && p.antes) p.a.tocar(p.antes); });
    return elenco.length > 0;
  }

  /** ninguém fica encarando a câmera depois que a consequência termina. */
  function soltarOlhares() {
    Object.keys(C3.atores).forEach(function (n) { C3.atores[n].olhar(null); });
  }

  async function consequencia(cq, etiqueta) {
    if (!cq) return;
    U.calar();
    U.terceira(true, etiqueta || 'consequência da sua escolha');
    await U.esperar(200);
    await C3.irPara(cq.camera, { trilho: true, dur: 1.4 });
    aplicarPasso(cq);
    C3.olharLivre(false);
    encenar(cq.mostrar, 0.5);

    // tudo o que pode acontecer ao vivo, acontece ao vivo
    var mostrados = (cq.mostrar || []).slice();
    // o corpo do jogador entra por fora da lista do roteiro (é a variante da escolha)
    Object.keys(C3.atores).forEach(function (n) {
      if (n.indexOf('AVATAR_') !== 0 || mostrados.indexOf(n) >= 0) return;
      if (!ENCENACAO[n]) return;
      var o = C3.porNome[n];
      if (o && o.visible) mostrados.push(n);
    });
    var movidos = 0;
    mostrados.forEach(function (n) {           // as peças se mexem todas juntas
      if (MOVIMENTOS[n]) { C3.movimentar(n, MOVIMENTOS[n]); movidos++; }
    });
    var houve = false;
    for (var i = 0; i < mostrados.length && !houve; i++) {
      if (QUEDAS[mostrados[i]]) houve = await quedaReal(mostrados[i]);
    }
    for (var j = 0; j < mostrados.length && !houve; j++) {
      if (ENCENACAO[mostrados[j]]) houve = await encenarCorpo(mostrados[j]);
    }
    if (!houve && movidos) { await U.esperar(1900); houve = true; }
    if (!houve) await reacaoAoVivo();          // nunca uma imagem parada

    await U.ia(cq.ia, 'conseq');
    if (cq.tela) await U.tela(cq.tela);
    if (cq.nota) await U.falar('Nota', cq.nota, 'conseq nota');
    C3.velocidadeNormal(); U.lenta(false);
    U.terceira(false);
    soltarOlhares();
    if (camAnterior) {
      C3.semAvatar();
      await C3.irPara(camAnterior, { trilho: true, dur: 1.1 });
      C3.olharLivre(true);
    }
  }

  /* ---- registro de decisões (uma linha por cena, sempre a última tentativa) */
  function registrar(c, op) {
    var linha = {
      cena: c.id, titulo: c.titulo, quadro: quadroDe(c),
      opcao: op.id, texto: op.texto, correta: !!op.correta, critico: !!op.erro_critico,
      define: op.define || null, conseq: op.consequencia ? op.consequencia.camera : null
    };
    for (var i = est.registro.length - 1; i >= 0; i--) {
      if (est.registro[i].cena === c.id) { est.registro[i] = linha; return; }
    }
    est.registro.push(linha);
  }

  function marcarCritico(c, op) {
    if (est.criticos.some(function (x) { return x.cena === c.id; })) return;
    est.criticos.push({ cena: c.id, titulo: c.titulo, opcao: op.id, texto: op.texto });
  }

  /* ---- bloco de escolhas -------------------------------------------------- */
  var MAX_TENTATIVAS = 3;

  async function escolhas(c, lista) {
    var op, guarda = 0, vistas = {};
    do {
      guarda++;
      op = await U.escolher(lista);
      var repetida = !!vistas[op.id];
      vistas[op.id] = true;
      defineVars(op);
      aplicarPasso(op);
      if (op.falas && !repetida) await U.falas(op.falas);
      if (op.ia) await U.ia(op.ia, op.correta ? 'boa' : (op.erro_critico ? 'ruim' : ''));
      if (op.tela && !repetida) await U.tela(op.tela);
      anotar(op.registro);
      if (op.erro_critico) marcarCritico(c, op);
      registrar(c, op);
      if (op.consequencia && !repetida) await consequencia(op.consequencia);

      if (op.retornar) {
        if (guarda >= MAX_TENTATIVAS) {
          var certa = lista.filter(function (x) { return x.correta; })[0];
          if (certa) {
            await U.falar('Instrutor', 'Vamos seguir pelo caminho previsto, e eu explico por quê.', '');
            defineVars(certa);
            aplicarPasso(certa);
            if (certa.ia) await U.ia(certa.ia, 'boa');
            anotar(op.registro);          // o relatório guarda a tentativa do trabalhador
            registrar(c, certa);
            op = certa;
          }
          break;
        }
        await U.falar('Instrutor', 'Olhe de novo antes de decidir.', '');
      }
    } while (op.retornar);
    return op;
  }

  /* ---- nome do quadro de storyboard de uma cena (para a revisão) ---------- */
  function Q(id) { return (raiz.QUADROS || {})[id] || null; }
  function quadroDe(c) { return Q(c.id); }

  async function rodarEtapas(c) {
    var trab = C3.ator('AVATAR_TAREFA_Ajoelhado_Conectado');
    if (trab) trab.tocar('trabalhando');
    for (var i = 0; i < c.etapas.length; i++) {
      U.etapas(c.etapas, i);
      await U.falar('Tarefa', c.etapas[i].charAt(0).toUpperCase() + c.etapas[i].slice(1) + '.', 'tarefa');
    }
    U.etapas(c.etapas, c.etapas.length);
    await U.esperar(400);
    U.etapas(null);
  }

  async function subcenas(c) {
    for (var i = 0; i < (c.subcenas || []).length; i++) {
      var sc = c.subcenas[i];
      U.cena(c.id, U.txt(sc.titulo));
      await C3.caminharAte(sc.camera, { vel: 1.1, maxDist: 8 });
      camAnterior = sc.camera;
      if (sc.ia) await U.ia(sc.ia);
      if (sc.escolhas) await escolhas(sc, sc.escolhas);
    }
    camAnterior = c.camera;
  }

  /* ---- uma cena ----------------------------------------------------------- */
  async function cena(c, num, total) {
    U.cena(c.id, U.txt(c.titulo));
    aplicarPasso(c);
    camAnterior = c.camera;
    if (c.modo === '3P') {
      await C3.irPara(c.camera, { trilho: true });
      C3.olharLivre(false);
    } else {
      C3.semAvatar();                       // em 1ª pessoa o corpo do jogador não aparece
      C3.olharLivre(true);
      // vai andando até o ponto, sem parar a ação: a conversa corre junto
      var indo = C3.caminharAte(c.camera, { vel: 1.5 });
      encenar(c.mostrar);
      if (c.som) U.som(c.som);
      if (c.ia_silenciosa) U.registrado('O instrutor não vai interferir aqui.');
      if (c.falas) await U.falas(c.falas);
      if (c.ia) await U.ia(c.ia);
      await indo;                           // só segue quando chegou E terminou de falar
      encenar(c.mostrar);
      if (c.tela) await U.tela(c.tela);
      if (c.etapas) await rodarEtapas(c);
      await subcenas(c);
      if (c.escolhas) await escolhas(c, c.escolhas);
      if (c.consequencia_didatica) await consequencia(c.consequencia_didatica, 'o que as proteções evitaram');
      if (c.registro_automatico) anotar(c.registro_automatico);
      est.feitos[c.id] = true;
      return;
    }
    if (c.som) U.som(c.som);
    if (c.ia_silenciosa) U.registrado('O instrutor não vai interferir aqui.');
    if (c.falas) await U.falas(c.falas);
    if (c.ia) await U.ia(c.ia);
    if (c.tela) await U.tela(c.tela);

    if (c.etapas) await rodarEtapas(c);
    await subcenas(c);
    if (c.escolhas) await escolhas(c, c.escolhas);

    if (c.consequencia_didatica) await consequencia(c.consequencia_didatica, 'o que as proteções evitaram');
    if (c.registro_automatico) anotar(c.registro_automatico);
    est.feitos[c.id] = true;
  }

  /* ---- cena principal: a chave escapa ------------------------------------- */
  async function principal() {
    var p = D.principal;
    U.cena('★', U.txt(p.titulo));
    aplicarPasso(p);
    camAnterior = p.camera;
    await C3.irPara(p.camera, { trilho: true });
    C3.olharLivre(true);
    U.som('CLANG!');
    await U.ia(p.ia);
    var r = p.resultados.filter(function (x) { return D.condOk(x.se, est.vars); })[0] || p.resultados[p.resultados.length - 1];
    anotar(r.registro);
    if (r.erro_critico) marcarCritico({ id: 'PRINC', titulo: p.titulo }, { id: '—', texto: 'queda de ferramenta sem proteção e sem isolamento' });
    est.registro.push({
      cena: 'PRINC', titulo: p.titulo, quadro: Q('PRINC'),
      opcao: '—', texto: 'desfecho: ' + Object.keys(r.se).map(function (k) { return k + '=' + r.se[k]; }).join(' e '),
      correta: !r.erro_critico, critico: !!r.erro_critico, define: null,
      conseq: r.consequencia ? r.consequencia.camera : null
    });
    await consequencia(r.consequencia, 'a ferramenta escapou');
    est.feitos.PRINC = true;
  }

  /* ---- consequências adiadas ---------------------------------------------- */
  function disparam(c) {
    if (c.requer_evento && !est.feitos[c.requer_evento]) return false;
    if (c.se_qualquer) return c.se_qualquer.some(function (d) { return D.condOk(d, est.vars); });
    return D.condOk(c.se, est.vars);
  }

  async function adiadas(ids) {
    for (var i = 0; i < ids.length; i++) {
      var c = D.consequencias.filter(function (x) { return x.id === ids[i]; })[0];
      if (!c || est.feitos[c.id] || !disparam(c)) continue;
      est.feitos[c.id] = true;
      if (c.consequencia) {
        var cq = JSON.parse(JSON.stringify(c.consequencia));
        // variante por condição / por ponto escolhido
        (c.variantes || []).forEach(function (v) {
          if (D.condOk(v.se, est.vars)) {
            cq.mostrar = (cq.mostrar || []).concat(v.mostrar || []);
            cq.ocultar = (cq.ocultar || []).concat(v.ocultar || []);
            if (v.ia) cq.ia = (cq.ia || []).concat(v.ia);
          }
        });
        var vp = c.variantes_por_ponto && c.variantes_por_ponto[est.vars.PONTO_ESCOLHIDO];
        if (vp) {
          cq.mostrar = (cq.mostrar || []).concat(vp.mostrar || []);
          if (vp.camera) cq.camera = vp.camera;
        }
        await consequencia(cq, c.positiva ? 'a sua boa decisão' : 'consequência do que ficou registrado');
      } else if (c.ia) {
        await U.ia(c.ia, c.positiva ? 'boa' : '');
      }
      anotar(c.registro);
      if (c.erro_critico) marcarCritico(c, { id: '—', texto: c.titulo });
      est.registro.push({
        cena: c.id, titulo: c.titulo, quadro: Q(c.id), opcao: '—',
        texto: c.positiva ? 'consequência positiva' : 'consequência de uma escolha anterior',
        correta: !!c.positiva, critico: !!c.erro_critico, define: null,
        conseq: c.consequencia ? c.consequencia.camera : null
      });
    }
  }

  /* ---- a prova inteira ----------------------------------------------------- */
  M.jogar = async function (nome, aoFim) {
    zerar(nome);
    U.nomear(nome);
    U.hud(true);

    for (var i = 0; i < D.cenas.length; i++) await cena(D.cenas[i], i + 1, D.cenas.length);

    est.eventos = D.sortearEventos(est.vars);
    for (var e = 0; e < est.eventos.length; e++) {
      var ev = est.eventos[e];
      U.registrado('A obra continua andando…');
      await U.esperar(500);
      await cena(ev);
      // respiro entre eventos: o roteiro pede que a situação volte ao normal
      if (e < est.eventos.length - 1) {
        await C3.irPara('CAM_1P_C21_Inicio_Tarefa', { trilho: true, dur: 1.4 });
        await U.esperar(700);
      }
    }

    await principal();
    await adiadas(['CONSEQ_MATERIAL_SOLTO', 'CONSEQ_MATERIAL_RETIRADO', 'CONSEQ_ISOLAMENTO_FUNCIONOU',
      'CONSEQ_CONEXAO_INCORRETA', 'CONSEQ_EQUIPAMENTO_DANIFICADO', 'CONSEQ_GUARDA_CORPO_PROBLEMA',
      'CONSEQ_COMUNICACAO_RESTABELECIDA']);

    for (var f = 0; f < D.fechamento.length; f++) {
      var fc = D.fechamento[f];
      await cena(fc);
      if (fc.consequencias_pendentes) await adiadas(fc.consequencias_pendentes);
    }

    U.hud(false);
    U.calar();
    if (aoFim) aoFim(M.resultado());
  };

  /* ---- resultado ----------------------------------------------------------- */
  M.resultado = function () {
    var cats = D.categorias.map(function (c) {
      return { categoria: c, resultado: est.relatorio[c] || 'NAO_AVALIADO' };
    });
    var melhorar = cats.filter(function (c) { return c.resultado === 'PRECISA_MELHORAR'; }).length;
    var id = est.criticos.length ? 'ERROS_CRITICOS' : (melhorar >= 3 ? 'PONTOS_A_MELHORAR' : 'BOM_DESEMPENHO');
    var desf = D.roteiro.resultados.filter(function (r) { return r.id === id; })[0];
    return {
      id: id, desfecho: desf, categorias: cats, melhorar: melhorar,
      criticos: est.criticos, registro: est.registro, vars: est.vars,
      eventos: est.eventos.map(function (e) { return e.id + ' · ' + e.titulo; }),
      minutos: Math.round((Date.now() - est.comecou) / 60000)
    };
  };

  raiz.Motor = M;
})(window);
