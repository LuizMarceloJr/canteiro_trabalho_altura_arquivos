/* dados.js — carrega o roteiro e prepara os índices que o motor usa. */
(function (raiz) {
  'use strict';

  var D = {
    roteiro: null,
    cenas: [],          // C01..C21 em ordem
    porId: {},
    eventos: [],
    consequencias: [],
    fechamento: [],
    principal: null,
    lidaPor: {},        // VARIAVEL -> [ids de consequência que a leem]
    categorias: []
  };

  D.carregar = function (url) {
    return fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error('não consegui ler ' + url + ' (' + r.status + ')');
      return r.json();
    }).then(function (R) {
      D.roteiro = R;
      D.cenas = R.cenas;
      D.eventos = R.eventos_inesperados;
      D.consequencias = R.consequencias;
      D.fechamento = R.fechamento;
      D.principal = R.cena_principal;
      D.categorias = R.relatorio.categorias;
      D.sorteio = R.sorteio_de_eventos;

      [].concat(R.cenas, R.eventos_inesperados, R.fechamento, [R.cena_principal]).forEach(function (c) {
        D.porId[c.id] = c;
        (c.subcenas || []).forEach(function (s) { D.porId[s.id] = s; });
      });

      // quais variáveis são cobradas depois (para o aviso "isso ficou registrado")
      function marcar(cond, id) {
        Object.keys(cond || {}).forEach(function (v) {
          (D.lidaPor[v] = D.lidaPor[v] || []).push(id);
        });
      }
      R.consequencias.forEach(function (c) {
        marcar(c.se, c.id);
        (c.se_qualquer || []).forEach(function (d) { marcar(d, c.id); });
      });
      R.cena_principal.resultados.forEach(function (r) { marcar(r.se, 'PRINC'); });
      R.eventos_inesperados.forEach(function (e) { marcar(e.requer, e.id); });
      return D;
    });
  };

  /* ---- sorteio de eventos ------------------------------------------------ */
  function condOk(req, vars) {
    if (!req) return true;
    return Object.keys(req).every(function (k) { return vars[k] === req[k]; });
  }

  D.sortearEventos = function (vars) {
    var s = D.sorteio;
    var min = s.quantidade_por_sessao[0], max = s.quantidade_por_sessao[1];
    var alvo = min + Math.floor(Math.random() * (max - min + 1));
    var proibido = {};
    s.nao_sortear_juntos.forEach(function (par) {
      par.forEach(function (a) {
        proibido[a] = (proibido[a] || []).concat(par.filter(function (b) { return b !== a; }));
      });
    });

    var pool = D.eventos.filter(function (e) { return condOk(e.requer, vars); });
    // roleta por peso
    var escolhidos = [], vetados = {}, criticos = 0;
    var maxCrit = s.maximo_eventos_criticos_por_sessao || 2;
    while (escolhidos.length < alvo && pool.length) {
      var cand = pool.filter(function (e) {
        if (vetados[e.variavel_evento]) return false;
        if (escolhidos.indexOf(e) >= 0) return false;
        if (e.peso >= 3 && criticos >= maxCrit) return false;
        return true;
      });
      if (!cand.length) break;
      var total = cand.reduce(function (a, e) { return a + (e.peso || 1); }, 0);
      var r = Math.random() * total, ev = cand[0];
      for (var i = 0; i < cand.length; i++) { r -= (cand[i].peso || 1); if (r <= 0) { ev = cand[i]; break; } }
      escolhidos.push(ev);
      if (ev.peso >= 3) criticos++;
      (proibido[ev.variavel_evento] || []).forEach(function (x) { vetados[x] = true; });
    }
    // ordem estável pela numeração do evento, para a obra "andar" de forma coerente
    escolhidos.sort(function (a, b) { return a.id.localeCompare(b.id); });
    return escolhidos;
  };

  D.condOk = condOk;

  /* quadro de storyboard de cada cena (pasta ../renders/storyboard/) */
  raiz.QUADROS = {
    C01: 'C01_1P', C02: 'C02_1P', C03: 'C03_1P', C04: 'C04_1P', C05: 'C05_1P',
    C06: 'C06_1P', C06a: 'C06_1P_capacete', C06b: 'C06_1P_cinturao', C06c: 'C06_1P_talabarte',
    C07: 'C07_3P_erro', C08: 'C08_1P', C09: 'C09_1P', C10: 'C10_1P', C11: 'C11_1P',
    C12: 'C12_1P', C13: 'C13_1P', C14: 'C14_1P', C15: 'C15_1P', C16: 'C16_1P',
    C17: 'C17_1P', C18: 'C18_1P', C19: 'C19_1P', C20: 'C20_1P', C21: 'C21_1P',
    PRINC: 'PRINC_1P', CONC: 'CONC_1P', ORG: 'ORG_1P', RET: 'RET_1P', EMERG: 'EMERG_1P',
    EV01: 'EV01_1P', EV02: 'EV02_1P', EV03: 'EV03_1P', EV04: 'EV04_1P', EV05: 'EV05_1P',
    EV06: 'EV06_1P', EV07: 'EV07_1P', EV08: 'EV08_1P', EV09: 'EV09_1P', EV10: 'EV10_1P',
    EV11: 'EV11_1P', EV12: 'EV12_1P', EV13: 'EV13_1P', EV14: 'EV14_1P', EV15: 'EV15_1P',
    EV16: 'EV16_1P', EV17: 'EV17_1P',
    CONSEQ_MATERIAL_SOLTO: 'CONSEQ_3P_material_solto',
    CONSEQ_MATERIAL_RETIRADO: 'CONSEQ_3P_material_retirado',
    CONSEQ_ABERTURA_IGNORADA: 'C11_3P_conseq',
    CONSEQ_CONEXAO_INCORRETA: 'CONSEQ_3P_conexao',
    CONSEQ_EQUIPAMENTO_DANIFICADO: 'CONSEQ_3P_equipamento',
    CONSEQ_GUARDA_CORPO_PROBLEMA: 'CONSEQ_3P_guarda_corpo',
    CONSEQ_ISOLAMENTO_FUNCIONOU: 'PRINC_3P_isolada',
    CONSEQ_COMUNICACAO_RESTABELECIDA: 'EV05_1P'
  };
  raiz.PASTA_QUADROS = '../renders/storyboard/';

  raiz.Dados = D;
})(window);
