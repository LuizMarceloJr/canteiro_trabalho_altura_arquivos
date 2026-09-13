/* main.js — amarra tudo: carrega, aula, prova, resultado, revisão. */
(function () {
  'use strict';

  var $ = function (id) { return document.getElementById(id); };
  var GLB = '../canteiro_trabalho_altura_draco.glb';
  var ROTEIRO = '../roteiro_treinamento.json';
  var DRACO = 'vendor/draco/';
  var ultimo = null, nome = '';

  function mostrar(id) {
    ['carregando', 'tela-abertura', 'tela-aula', 'tela-resultado', 'tela-revisao'].forEach(function (t) {
      $(t).hidden = t !== id;
    });
  }

  function progresso(p, txt) {
    $('barra-int').style.width = Math.round(p * 100) + '%';
    if (txt) $('carga-txt').textContent = txt;
  }

  /* ---------------------------------------------------------------- arranque */
  UI.iniciar();
  Cena3D.iniciar($('cena'));
  Motor.iniciar(Dados, Cena3D, UI);

  progresso(0.05, 'lendo o roteiro…');
  Dados.carregar(ROTEIRO).then(function () {
    progresso(0.15, 'carregando o canteiro (2,7 MB)…');
    return Cena3D.carregar(GLB, DRACO, function (p) {
      progresso(0.15 + p * 0.8, 'carregando o canteiro… ' + Math.round(p * 100) + '%');
    });
  }).then(function () {
    progresso(1, 'pronto');
    Cena3D.irPara('CAM_1P_C01_Entrada_Canteiro', { trilho: false });
    setTimeout(function () { mostrar('tela-abertura'); }, 350);
  }).catch(function (e) {
    console.error(e);
    $('carga-txt').innerHTML = 'Não consegui carregar: ' + e.message +
      '<br><br>Abra pelo <b>abrir_jogo.bat</b> (ou por um servidor local). Arquivo aberto direto com dois cliques não carrega o modelo 3D.';
  });

  /* ---------------------------------------------------------------- abertura */
  $('form-nome').addEventListener('submit', function (e) {
    e.preventDefault();
    nome = $('campo-nome').value.trim() || 'colega';
    UI.nomear(nome);
    mostrar('tela-aula');
    Aula.iniciar(comecarProva);
  });

  /* ------------------------------------------------------------------ prova */
  function comecarProva() {
    mostrar(null);
    ['carregando', 'tela-abertura', 'tela-aula', 'tela-resultado', 'tela-revisao']
      .forEach(function (t) { $(t).hidden = true; });
    Motor.jogar(nome, function (r) { ultimo = r; verResultado(r); });
  }

  /* -------------------------------------------------------------- resultado */
  var ROTULO = {
    AUTORIZACAO: 'Autorização', PLANEJAMENTO: 'Planejamento',
    INSPECAO_DOS_EQUIPAMENTOS: 'Inspeção dos equipamentos', ACESSO: 'Acesso',
    OBSERVACAO_DO_CANTEIRO: 'Observação do canteiro', ABERTURAS_E_PROTECOES: 'Aberturas e proteções',
    PROTECAO_CONTRA_QUEDA: 'Proteção contra queda',
    QUEDA_DE_FERRAMENTAS_E_MATERIAIS: 'Queda de ferramentas e materiais',
    PROTECAO_DAS_PESSOAS_ABAIXO: 'Proteção das pessoas abaixo',
    REACAO_A_SITUACOES_INESPERADAS: 'Reação a situações inesperadas',
    MUDANCA_NAS_CONDICOES: 'Mudança nas condições', COMUNICACAO: 'Comunicação', EMERGENCIA: 'Emergência'
  };
  var TITULO = {
    BOM_DESEMPENHO: 'Bom desempenho',
    PONTOS_A_MELHORAR: 'Existem pontos a melhorar',
    ERROS_CRITICOS: 'Decisões que precisam ser refeitas'
  };

  function verResultado(r) {
    $('res-titulo').textContent = TITULO[r.id];
    $('res-titulo').className = 'res-' + r.id.toLowerCase();
    $('res-nome').textContent = nome + ' · ' + r.registro.length + ' decisões · ' +
      (r.eventos.length ? r.eventos.length + ' eventos inesperados nesta execução' : 'sem eventos sorteados');
    $('res-ia').innerHTML = (r.desfecho.ia || []).map(function (l) {
      return '<p>' + UI.txt(l) + '</p>';
    }).join('');
    $('res-cats').innerHTML = r.categorias.map(function (c) {
      var cls = c.resultado === 'CORRETO' ? 'ok' : (c.resultado === 'PRECISA_MELHORAR' ? 'mel' : 'na');
      var txt = c.resultado === 'CORRETO' ? 'correto' :
        (c.resultado === 'PRECISA_MELHORAR' ? 'precisa melhorar' : 'não avaliado nesta execução');
      return '<div class="cat ' + cls + '"><span class="cat-n">' + (ROTULO[c.categoria] || c.categoria) +
        '</span><span class="cat-v">' + txt + '</span></div>';
    }).join('');
    $('res-criticas').hidden = !r.criticos.length;
    mostrar('tela-resultado');
  }

  $('res-revisar').addEventListener('click', function () { verRevisao(ultimo); });
  $('rev-voltar').addEventListener('click', function () { mostrar('tela-resultado'); });
  $('res-refazer').addEventListener('click', function () { comecarProva(); });
  $('res-criticas').addEventListener('click', function () { verRevisao(ultimo, true); });

  /* ---------------------------------------------------------------- revisão */
  function verRevisao(r, soCriticas) {
    var lista = r.registro.filter(function (d) { return soCriticas ? d.critico : true; });
    $('rev-lista').innerHTML = lista.map(function (d) {
      var cls = d.critico ? 'crit' : (d.correta ? 'boa' : 'meh');
      var img = d.quadro ? '<img src="' + (window.PASTA_QUADROS || '../renders/storyboard/') + d.quadro +
        '.jpg" alt="" loading="lazy">' : '';
      var vars = d.define ? Object.keys(d.define).map(function (v) {
        return '<span class="rev-var">' + v + ' = ' + d.define[v] + '</span>';
      }).join('') : '';
      return '<article class="rev-i ' + cls + '">' + img +
        '<div class="rev-t"><span class="rev-cena">' + d.cena + '</span><h4>' + UI.txt(d.titulo) + '</h4>' +
        '<p class="rev-esc"><b>' + d.opcao + '</b> ' + UI.txt(d.texto) + '</p>' +
        (vars ? '<div class="rev-vars">' + vars + '</div>' : '') +
        (d.conseq ? '<p class="rev-conseq">consequência mostrada em 3ª pessoa</p>' : '') +
        '</div></article>';
    }).join('') || '<p class="rev-vazio">Nenhuma decisão crítica nesta execução.</p>';
    mostrar('tela-revisao');
  }
})();
