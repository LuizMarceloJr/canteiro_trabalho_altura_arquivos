/* ui.js — fala, roda de escolhas (sem tempo), avisos e telas do HUD. */
(function (raiz) {
  'use strict';

  var $ = function (id) { return document.getElementById(id); };
  var U = { nome: 'você' };

  var elFala, elQuem, elTexto, elEsc, elToasts, elTela, elEtapas, elHud, elModo, elModoTxt, elCong, elSom;

  U.iniciar = function () {
    elFala = $('fala'); elQuem = $('fala-quem'); elTexto = $('fala-texto');
    elEsc = $('escolhas'); elToasts = $('toasts'); elTela = $('tela-jogo');
    elEtapas = $('etapas'); elHud = $('hud'); elModo = $('marca-modo');
    elModoTxt = $('marca-txt'); elCong = $('marca-congelado'); elSom = $('hud-som');
  };

  U.nomear = function (n) { U.nome = (n || '').trim() || 'você'; };
  function trocaNome(t) { return String(t == null ? '' : t).replace(/\{\{NOME\}\}/g, U.nome); };
  U.txt = trocaNome;

  U.hud = function (v) { elHud.hidden = !v; };

  U.cena = function (id, nome) {
    $('hud-cena-id').textContent = id || '';
    $('hud-cena-nome').textContent = nome || '';
  };

  U.som = function (s) {
    if (!s) { elSom.hidden = true; return; }
    elSom.textContent = '♪ ' + s;
    elSom.hidden = false;
    setTimeout(function () { elSom.hidden = true; }, 2600);
  };

  /* ---- fala: clique (ou Espaço/Enter) para avançar ----------------------- */
  function esperarClique() {
    return new Promise(function (ok) {
      function fim(e) {
        if (e.type === 'keydown' && e.key !== ' ' && e.key !== 'Enter') return;
        if (e.type === 'click' && e.target.closest('.botao, .carta')) return;
        document.removeEventListener('click', fim);
        document.removeEventListener('keydown', fim);
        ok();
      }
      setTimeout(function () {
        document.addEventListener('click', fim);
        document.addEventListener('keydown', fim);
      }, 90);
    });
  }

  U.falar = function (quem, texto, classe) {
    elFala.hidden = false;
    elFala.className = 'fala' + (classe ? ' ' + classe : '');
    elQuem.textContent = quem;
    elTexto.textContent = trocaNome(texto);
    return esperarClique();
  };

  U.falas = async function (lista) {
    for (var i = 0; i < (lista || []).length; i++) {
      await U.falar(lista[i].quem, lista[i].texto, 'personagem');
    }
  };

  U.ia = async function (linhas, classe) {
    for (var i = 0; i < (linhas || []).length; i++) {
      await U.falar('Instrutor', linhas[i], classe);
    }
  };

  U.calar = function () { elFala.hidden = true; };

  /* ---- escolhas (sem contagem regressiva) -------------------------------- */
  U.escolher = function (opcoes) {
    elFala.hidden = true;
    elEsc.hidden = false;
    elEsc.innerHTML = '';
    return new Promise(function (ok) {
      opcoes.forEach(function (o) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'carta';
        b.innerHTML = '<span class="carta-letra">' + o.id + '</span><span class="carta-txt">' +
          trocaNome(o.texto).replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>';
        b.addEventListener('click', function () {
          elEsc.hidden = true; elEsc.innerHTML = '';
          ok(o);
        });
        elEsc.appendChild(b);
      });
    });
  };

  /* ---- aviso "isso ficou registrado" ------------------------------------- */
  U.registrado = function (texto) {
    var d = document.createElement('div');
    d.className = 'toast';
    d.innerHTML = '<span class="toast-marca"></span><span>' + (texto || 'Isso ficou registrado.') + '</span>';
    elToasts.appendChild(d);
    setTimeout(function () { d.classList.add('sai'); }, 3400);
    setTimeout(function () { if (d.parentNode) d.parentNode.removeChild(d); }, 4200);
  };

  /* ---- painel de tela (PT, missão, avisos) ------------------------------- */
  U.tela = function (t) {
    if (!t) { elTela.hidden = true; elTela.innerHTML = ''; return Promise.resolve(); }
    var h = '';
    if (t.titulo) h += '<div class="tj-titulo">' + trocaNome(t.titulo) + '</div>';
    (t.linhas || []).forEach(function (l) { h += '<div class="tj-linha">' + trocaNome(l) + '</div>'; });
    if (t.campos) {
      h += '<dl class="tj-campos">';
      t.campos.forEach(function (c) { h += '<dt>' + trocaNome(c[0]) + '</dt><dd>' + trocaNome(c[1]) + '</dd>'; });
      h += '</dl>';
    }
    h += '<button type="button" class="botao primario tj-ok">' +
      ((t.botoes && t.botoes[0]) ? trocaNome(t.botoes[0]) : 'Continuar') + '</button>';
    elTela.innerHTML = h;
    elTela.hidden = false;
    return new Promise(function (ok) {
      elTela.querySelector('.tj-ok').addEventListener('click', function () {
        elTela.hidden = true; elTela.innerHTML = ''; ok();
      });
    });
  };

  /* ---- marcas de 3ª pessoa e congelamento -------------------------------- */
  U.terceira = function (on, texto) {
    elModo.hidden = !on;
    if (on) elModoTxt.textContent = texto || 'consequência da sua escolha';
    document.body.classList.toggle('modo-3p', !!on);
  };
  U.congelado = function (on) {
    elCong.hidden = !on;
    document.body.classList.toggle('congelado', !!on);
  };
  /** nada congela: o momento crítico passa em câmera lenta e a tarja diz isso. */
  U.lenta = function (on) {
    if (!elCong) return;
    elCong.textContent = 'câmera lenta';
    elCong.hidden = !on;
    document.body.classList.toggle('camera-lenta', !!on);
    document.body.classList.remove('congelado');
  };

  /* ---- etapas da tarefa (C21) -------------------------------------------- */
  U.etapas = function (lista, feitas) {
    if (!lista) { elEtapas.hidden = true; return; }
    elEtapas.hidden = false;
    elEtapas.innerHTML = lista.map(function (e, i) {
      return '<span class="etapa-i' + (i < feitas ? ' ok' : (i === feitas ? ' agora' : '')) + '">' + e + '</span>';
    }).join('');
  };

  U.esperar = function (ms) { return new Promise(function (ok) { setTimeout(ok, ms); }); };

  raiz.UI = U;
})(window);
