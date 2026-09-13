/* animacao.js — anima os personagens em tempo real girando as peças rígidas
   (Quadril, Torso, Cabeca, Braco/Antebraco, Coxa/Canela), no espírito do
   Minecraft: bonecos de partes, sem esqueleto com pele.

   Convenção dos ângulos (já no espaço do Three.js, em radianos):
     x = flexão (para frente / para trás)
     y = giro em torno do próprio eixo
     z = abertura lateral
*/
(function (raiz) {
  'use strict';

  var PARTES = ['Quadril', 'Torso', 'Cabeca', 'Braco_R', 'Antebraco_R', 'Braco_L',
                'Antebraco_L', 'Coxa_R', 'Canela_R', 'Coxa_L', 'Canela_L'];

  function P(o) { return o || {}; }

  /* ---------------------------------------------------------------- poses
     Todos os ângulos abaixo estão na CONVENÇÃO DO BONECO (não no eixo cru da
     peça, que muda de junta para junta porque cada peça foi assada no seu
     próprio encaixe). O conversor lá embaixo traduz para a peça.

       x  + flexiona para a FRENTE  (braço e coxa vão à frente; tronco e cabeça
                                     inclinam para baixo; antebraço fecha o cotovelo)
          - canela: + é esticar, - é dobrar o joelho (o pé vai para trás)
       y  + torce para a ESQUERDA do boneco
       z  + ABRE para fora do corpo

     Braço e coxa em x = 0 apontam para baixo; x = 1.57 deixa na horizontal à
     frente; x = 3.14 aponta para cima. Peças da esquerda são espelhadas
     sozinhas, então os dois lados usam o mesmo número. */
  var POSES = {
    em_pe: {
      Braco_R: [-0.04, 0, 0.10], Antebraco_R: [0.12, 0, 0],
      Braco_L: [-0.04, 0, 0.10], Antebraco_L: [0.12, 0, 0]
    },
    maos_na_cintura: {
      Braco_R: [-0.10, 0, 0.52], Antebraco_R: [1.25, 0, -0.45],
      Braco_L: [-0.10, 0, 0.52], Antebraco_L: [1.25, 0, -0.45]
    },
    agachado: {
      _y: -0.36,
      Quadril: [0.16, 0, 0], Torso: [0.26, 0, 0], Cabeca: [-0.36, 0, 0],
      // canela dobra o mesmo tanto que a coxa: o pé fica embaixo do corpo,
      // e não à frente (senão o boneco parece sentado no ar)
      Coxa_R: [0.95, 0, 0.14], Canela_R: [-1.90, 0, 0],
      Coxa_L: [0.85, 0, 0.14], Canela_L: [-1.70, 0, 0],
      Braco_R: [0.80, 0, 0.16], Antebraco_R: [0.70, 0, 0],
      Braco_L: [0.70, 0, 0.16], Antebraco_L: [0.80, 0, 0]
    },
    ajoelhado: {
      _y: -0.34,
      Quadril: [0.10, 0, 0], Torso: [0.30, 0, 0], Cabeca: [-0.42, 0, 0],
      Coxa_R: [0.25, 0, 0.10], Canela_R: [-1.85, 0, 0],     // joelho direito no chão
      Coxa_L: [1.00, 0, 0.14], Canela_L: [-1.90, 0, 0],     // pé esquerdo plantado embaixo
      Braco_R: [0.95, 0, 0.18], Antebraco_R: [0.78, 0, 0],
      Braco_L: [0.85, 0, 0.20], Antebraco_L: [0.90, 0, 0]
    },
    assustado: {
      Quadril: [-0.10, 0, 0], Torso: [-0.20, 0, 0], Cabeca: [-0.28, 0, 0],
      Braco_R: [1.05, 0, 0.60], Antebraco_R: [1.45, 0, 0],
      Braco_L: [1.05, 0, 0.60], Antebraco_L: [1.45, 0, 0],
      Coxa_R: [0.14, 0, 0.12], Coxa_L: [-0.10, 0, 0.12]
    },
    escorregando: {
      Quadril: [-0.42, 0, 0], Torso: [-0.30, 0, 0], Cabeca: [-0.24, 0, 0],
      Braco_R: [2.10, 0, 0.45], Antebraco_R: [0.35, 0, 0],
      Braco_L: [2.25, 0, 0.42], Antebraco_L: [0.30, 0, 0],
      Coxa_R: [1.15, 0, 0.16], Canela_R: [-0.35, 0, 0],
      Coxa_L: [-0.50, 0, 0.14], Canela_L: [-0.85, 0, 0]
    },
    suspenso: {
      Quadril: [0.28, 0, 0], Torso: [-0.16, 0, 0], Cabeca: [-0.10, 0, 0],
      Braco_R: [1.00, 0, 0.38], Antebraco_R: [1.10, 0, 0],
      Braco_L: [0.95, 0, 0.38], Antebraco_L: [1.05, 0, 0],
      Coxa_R: [0.72, 0, 0.14], Canela_R: [-0.95, 0, 0],
      Coxa_L: [0.58, 0, 0.14], Canela_L: [-0.80, 0, 0]
    },
    tonto: {
      Torso: [0.10, 0, 0], Cabeca: [0.10, 0, 0],
      Braco_R: [1.70, 0, 0.32], Antebraco_R: [2.05, 0, 0],
      Braco_L: [-0.08, 0, 0.16], Antebraco_L: [0.25, 0, 0],
      Coxa_R: [0.05, 0, 0.16], Coxa_L: [-0.05, 0, 0.16]
    },
    apontando: {
      Torso: [0, -0.10, 0],
      Braco_R: [1.38, 0, 0.22], Antebraco_R: [0.12, 0, 0],
      Braco_L: [-0.06, 0, 0.12], Antebraco_L: [0.18, 0, 0]
    },
    radio: {
      Braco_R: [1.05, 0, 0.32], Antebraco_R: [1.95, 0, 0],
      Braco_L: [-0.06, 0, 0.12], Antebraco_L: [0.20, 0, 0]
    },
    empurrando: {
      Quadril: [0.12, 0, 0], Torso: [0.18, 0, 0], Cabeca: [-0.26, 0, 0],
      Braco_R: [1.18, 0, 0.20], Antebraco_R: [0.25, 0, 0],
      Braco_L: [1.18, 0, 0.20], Antebraco_L: [0.25, 0, 0]
    },
    subindo: {
      Torso: [0.10, 0, 0], Cabeca: [-0.22, 0, 0],
      Braco_R: [2.35, 0, 0.25], Antebraco_R: [0.45, 0, 0],
      Braco_L: [1.20, 0, 0.25], Antebraco_L: [1.35, 0, 0],
      Coxa_R: [1.25, 0, 0.14], Canela_R: [-1.30, 0, 0],
      Coxa_L: [0.35, 0, 0.14], Canela_L: [-0.45, 0, 0]
    },
    carregando: {
      Torso: [-0.08, 0, 0],
      Braco_R: [1.05, 0, 0.26], Antebraco_R: [1.25, 0, 0],
      Braco_L: [1.05, 0, 0.26], Antebraco_L: [1.25, 0, 0]
    }
  };

  /* --------------------------------------------------------------- clipes
     Cada clipe devolve uma pose (peça -> [x, y, z]) para o tempo t. */
  var CLIPES = {
    escorregando: function (t) {
      var d = Math.min(1, t * 2.2), g = Math.sin(t * 7.0) * Math.max(0, 1 - t * 0.8);
      var alvo = mescla(POSES.em_pe, POSES.escorregando), r = {}, k;
      for (k in alvo) {
        var b = POSES.em_pe[k] || [0, 0, 0];
        r[k] = [b[0] + (alvo[k][0] - b[0]) * d, b[1] + (alvo[k][1] - b[1]) * d,
                b[2] + (alvo[k][2] - b[2]) * d];
      }
      if (r.Quadril) r.Quadril[1] = 0.06 * g;
      if (r.Cabeca) r.Cabeca[1] = 0.12 * g;
      return r;
    },
    desequilibrio: function (t) {
      var s = Math.sin(t * 3.4), c = Math.cos(t * 2.6);
      return mescla(POSES.em_pe, {
        Quadril: [-0.16 + 0.08 * s, 0.10 * c, 0], Torso: [-0.18, 0.10 * s, 0],
        Cabeca: [-0.20, 0.14 * s, 0],
        Braco_R: [1.85 + 0.25 * s, 0, 0.62], Antebraco_R: [0.55, 0, 0],
        Braco_L: [1.90 - 0.25 * s, 0, 0.58], Antebraco_L: [0.50, 0, 0],
        Coxa_R: [0.26 * s, 0, 0.18], Coxa_L: [-0.26 * s, 0, 0.18]
      });
    },
    tropecando: function (t) {
      var d = Math.min(1, t * 3.0);
      return mescla(POSES.em_pe, {
        Quadril: [0.28 * d, 0, 0], Torso: [0.32 * d, 0, 0], Cabeca: [-0.30 * d, 0, 0],
        Braco_R: [1.60 * d, 0, 0.42], Antebraco_R: [0.60 * d, 0, 0],
        Braco_L: [1.70 * d, 0, 0.38], Antebraco_L: [0.55 * d, 0, 0],
        Coxa_R: [0.95 * d, 0, 0.10], Canela_R: [-0.30 * d, 0, 0],
        Coxa_L: [-0.50 * d, 0, 0.10], Canela_L: [-1.05 * d, 0, 0]
      });
    },
    parado: function (t) {
      var r = 0.02 * Math.sin(t * 1.6);
      return mescla(POSES.em_pe, {
        Torso: [r, 0.02 * Math.sin(t * 0.9), 0],
        Cabeca: [r * 0.6, 0.06 * Math.sin(t * 0.35), 0],
        Braco_R: [-0.04 + r, 0, 0.10], Braco_L: [-0.04 - r, 0, 0.10]
      });
    },
    falando: function (t) {
      var g = Math.sin(t * 3.1), h = Math.sin(t * 2.2 + 1.0);
      return mescla(POSES.em_pe, {
        Torso: [0.02 * g, 0.05 * h, 0],
        Cabeca: [0.05 + 0.08 * Math.sin(t * 2.7), 0.12 * h, 0],
        Braco_R: [0.34 + 0.22 * g, 0, 0.24 + 0.08 * h], Antebraco_R: [0.85 + 0.30 * g, 0, 0],
        Braco_L: [-0.04, 0, 0.13], Antebraco_L: [0.25, 0, 0]
      });
    },
    andando: function (t, vel) {
      var m = marcha(t, vel);
      var c = Math.cos(6.2832 * m.fase), s = Math.sin(6.2832 * m.fase);
      return {
        _y: m._y,
        Quadril: [0.03, 0.05 * s, 0],
        Torso: [0.06, -0.07 * s, 0],
        Cabeca: [-0.05, 0.03 * s, 0],
        Coxa_R: m.Coxa_R, Canela_R: m.Canela_R,
        Coxa_L: m.Coxa_L, Canela_L: m.Canela_L,
        // o braço vai ao contrário da perna do mesmo lado
        Braco_R: [-0.34 * c, 0, 0.11], Antebraco_R: [0.24 + 0.16 * Math.max(0, -c), 0, 0],
        Braco_L: [0.34 * c, 0, 0.11], Antebraco_L: [0.24 + 0.16 * Math.max(0, c), 0, 0]
      };
    },
    andando_carregando: function (t, vel) {
      var base = CLIPES.andando(t, vel), sN = Math.sin(6.2832 * marcha(t, vel).fase);
      return mescla(base, {
        Torso: [-0.05, -0.04 * sN, 0], Cabeca: [0.04, 0, 0],
        Braco_R: [1.05, 0, 0.26], Antebraco_R: [1.25 + 0.06 * sN, 0, 0],
        Braco_L: [1.05, 0, 0.26], Antebraco_L: [1.25 - 0.06 * sN, 0, 0]
      });
    },
    andando_empurrando: function (t, vel) {
      var base = CLIPES.andando(t, vel), sN = Math.sin(6.2832 * marcha(t, vel).fase);
      return mescla(base, {
        Quadril: [0.10, 0.03 * sN, 0], Torso: [0.15, -0.04 * sN, 0], Cabeca: [0.20, 0, 0],
        Braco_R: [1.18, 0, 0.20], Antebraco_R: [0.25, 0, 0],
        Braco_L: [1.18, 0, 0.20], Antebraco_L: [0.25, 0, 0]
      });
    },
    queda_corpo: function (t) {
      var d = Math.min(1, t * 1.6), g = Math.sin(t * 9.0) * Math.max(0, 1 - t);
      return {
        Quadril: [-0.85 * d, 0.30 * g, 0], Torso: [-0.50 * d, 0.40 * g, 0],
        Cabeca: [-0.45 * d, 0.30 * g, 0],
        Braco_R: [2.55 * d, 0, 0.85 * d], Antebraco_R: [1.10 * d, 0, 0],
        Braco_L: [2.65 * d, 0, 0.80 * d], Antebraco_L: [1.00 * d, 0, 0],
        Coxa_R: [1.35 * d + 0.35 * g, 0, 0.24 * d], Canela_R: [-1.20 * d, 0, 0],
        Coxa_L: [0.90 * d - 0.35 * g, 0, 0.24 * d], Canela_L: [-1.45 * d, 0, 0]
      };
    },
    caido: function (t) {
      var g = 0.03 * Math.sin(t * 2.0);
      return {
        Quadril: [1.42, 0, 0], Torso: [-0.28 + g, 0.14, 0], Cabeca: [-0.38, 0.18, 0],
        Braco_R: [0.95, 0, 0.95], Antebraco_R: [1.35, 0, 0],
        Braco_L: [0.80, 0, 0.90], Antebraco_L: [1.20 + g, 0, 0],
        Coxa_R: [-1.30, 0, 0.28], Canela_R: [-0.95, 0, 0],
        Coxa_L: [-1.10, 0, 0.22], Canela_L: [-1.25, 0, 0]
      };
    },
    trabalhando: function (t) {
      var g = Math.sin(t * 4.4);
      return mescla(POSES.ajoelhado, {
        _y: -0.34,
        Braco_R: [0.95 + 0.22 * g, -0.10 * g, 0.18], Antebraco_R: [0.78 + 0.30 * g, 0, 0],
        Cabeca: [-0.42 + 0.04 * g, 0, 0]
      });
    },
    radio: function (t) {
      return mescla(POSES.radio, { Cabeca: [0.04 + 0.05 * Math.sin(t * 2.4), 0.06, 0] });
    },
    tonto: function (t) {
      var s = Math.sin(t * 1.5), c = Math.cos(t * 1.1);
      return mescla(POSES.tonto, {
        Quadril: [0.04 * s, 0.09 * c, 0], Torso: [0.10 + 0.05 * s, 0.10 * c, 0],
        Cabeca: [0.12, 0.10 * s, 0]
      });
    },
    suspenso: function (t) {
      var s = Math.sin(t * 0.9), c = Math.cos(t * 0.7);
      return mescla(POSES.suspenso, {
        Quadril: [0.28 + 0.05 * s, 0.08 * c, 0],
        Coxa_R: [0.72 + 0.10 * s, 0, 0.14], Coxa_L: [0.58 - 0.10 * s, 0, 0.14]
      });
    },
    empurrando: function (t) {
      var s = Math.sin(t * 4.0);
      return mescla(POSES.empurrando, {
        Coxa_R: [0.40 * s, 0, 0.06], Canela_R: [-Math.max(0, -0.5 * s) - 0.10, 0, 0],
        Coxa_L: [-0.40 * s, 0, 0.06], Canela_L: [-Math.max(0, 0.5 * s) - 0.10, 0, 0]
      });
    },
    subindo: function (t) {
      var a = t * 3.0, s = Math.sin(a), c = -s;
      return mescla(POSES.subindo, {
        Braco_R: [2.35 - 0.45 * s, 0, 0.25], Braco_L: [2.35 - 0.45 * c, 0, 0.25],
        Antebraco_R: [0.45 + 0.55 * (0.5 + 0.5 * s), 0, 0],
        Antebraco_L: [0.45 + 0.55 * (0.5 + 0.5 * c), 0, 0],
        Coxa_R: [1.25 - 0.50 * c, 0, 0.14], Coxa_L: [1.25 - 0.50 * s, 0, 0.14]
      });
    },
    assustado: function (t) {
      var d = Math.exp(-t * 2.2);
      return mescla(POSES.em_pe, escalar(POSES.assustado, 0.35 + 0.65 * d));
    },
    carregando: function (t) {
      return mescla(POSES.carregando, { Torso: [-0.08 + 0.015 * Math.sin(t * 1.7), 0, 0] });
    },
    caindo: function (t) {
      var g = Math.sin(t * 6.0);
      return {
        Quadril: [-0.32, 0.12 * g, 0], Torso: [-0.28, 0.25 * g, 0], Cabeca: [-0.32, 0, 0],
        Braco_R: [2.45 + 0.30 * g, 0, 0.75], Antebraco_R: [0.80, 0, 0],
        Braco_L: [2.45 - 0.30 * g, 0, 0.75], Antebraco_L: [0.80, 0, 0],
        Coxa_R: [1.05 - 0.40 * g, 0, 0.20], Canela_R: [-0.90, 0, 0],
        Coxa_L: [0.70 + 0.40 * g, 0, 0.20], Canela_L: [-1.20, 0, 0]
      };
    },

    /* ---- tarefas de canteiro (ciclos curtos, para os figurantes) --------- */
    martelando: function (t) {
      var g = Math.sin(t * 6.0);
      return mescla(POSES.em_pe, {
        Quadril: [0.05, 0, 0], Torso: [0.14 + 0.05 * g, 0.10, 0], Cabeca: [0.24, -0.10, 0],
        Braco_R: [0.95, 0, 0.22], Antebraco_R: [0.95 + 0.80 * g, 0, 0],
        Braco_L: [0.85, 0, 0.26], Antebraco_L: [1.30, 0, 0],
        Coxa_R: [0.06, 0, 0.12], Coxa_L: [-0.06, 0, 0.12]
      });
    },
    serrando: function (t) {
      var s = Math.sin(t * 4.6);
      return mescla(POSES.em_pe, {
        Quadril: [0.14, 0, 0], Torso: [0.24, 0.12, 0], Cabeca: [0.30, -0.10, 0],
        Braco_R: [0.60 + 0.30 * s, 0, 0.30], Antebraco_R: [1.00 - 0.65 * s, 0, 0],
        Braco_L: [0.70, 0, 0.32], Antebraco_L: [1.10, 0, 0],
        Coxa_R: [0.20, 0, 0.14], Canela_R: [-0.14, 0, 0],
        Coxa_L: [-0.22, 0, 0.14], Canela_L: [-0.30, 0, 0]
      });
    },
    varrendo: function (t) {
      var s = Math.sin(t * 2.4);
      return mescla(POSES.em_pe, {
        Quadril: [0.12, 0.10 * s, 0], Torso: [0.26, 0.18 * s, 0], Cabeca: [0.30, -0.12 * s, 0],
        // braço baixo e quase reto: é o que põe a vassoura no chão, à frente
        Braco_R: [0.58 + 0.14 * s, 0, 0.14 + 0.06 * s], Antebraco_R: [0.18 - 0.08 * s, 0, 0],
        Braco_L: [0.45 + 0.12 * s, 0, 0.20], Antebraco_L: [0.45 - 0.14 * s, 0, 0],
        Coxa_R: [0.06, 0, 0.12], Coxa_L: [-0.06, 0, 0.12]
      });
    },
    prancheta: function (t) {
      var olha = Math.max(0, Math.sin(t * 0.5));
      return mescla(POSES.em_pe, {
        Torso: [0.05, 0.05 * Math.sin(t * 0.7), 0],
        Cabeca: [0.38 - 0.50 * olha, 0.10 * Math.sin(t * 0.9), 0],
        Braco_R: [0.80, 0, 0.30], Antebraco_R: [1.45 + 0.12 * Math.sin(t * 2.3), 0, -0.30],
        Braco_L: [0.90, 0, 0.26], Antebraco_L: [1.55, 0, -0.30]
      });
    },
    cavando: function (t) {
      var a = (t * 0.62) % 1, d = a < 0.5 ? a * 2 : (1 - a) * 2, f = d * d;
      return mescla(POSES.em_pe, {                 // f = 0 enfia a pá, f = 1 levanta a carga
        _y: -0.10 * (1 - f),
        Quadril: [0.22 - 0.14 * f, 0, 0], Torso: [0.34 - 0.20 * f, 0.12, 0],
        Cabeca: [0.34 - 0.12 * f, -0.08, 0],
        Braco_R: [0.40 + 0.30 * f, 0, 0.14], Antebraco_R: [0.25 + 0.20 * f, 0, 0],
        Braco_L: [0.42 + 0.30 * f, 0, 0.18], Antebraco_L: [0.40 + 0.25 * f, 0, 0],
        Coxa_R: [0.26 - 0.12 * f, 0, 0.14], Canela_R: [-0.24, 0, 0],
        Coxa_L: [-0.18, 0, 0.14], Canela_L: [-0.30, 0, 0]
      });
    },
    pintando: function (t) {
      var s = Math.sin(t * 2.1);
      return mescla(POSES.em_pe, {
        Torso: [0.04, 0.10, 0], Cabeca: [-0.14 - 0.20 * s, -0.10, 0],
        Braco_R: [1.35 + 0.70 * s, 0, 0.24], Antebraco_R: [0.55 - 0.20 * s, 0, 0],
        Braco_L: [-0.04, 0, 0.13], Antebraco_L: [0.25, 0, 0],
        Coxa_R: [0.04, 0, 0.12], Coxa_L: [-0.04, 0, 0.12]
      });
    },
    misturando: function (t) {
      var s = Math.sin(t * 3.0), c = Math.cos(t * 3.0);
      return mescla(POSES.em_pe, {
        Quadril: [0.16, 0.08 * s, 0], Torso: [0.30, 0.12 * s, 0], Cabeca: [0.38, -0.08 * s, 0],
        Braco_R: [0.70 + 0.26 * s, 0, 0.28], Antebraco_R: [0.95 + 0.32 * c, 0, 0],
        Braco_L: [0.55 + 0.20 * s, 0, 0.26], Antebraco_L: [1.15 + 0.28 * c, 0, 0],
        Coxa_R: [0.16, 0, 0.14], Canela_R: [-0.14, 0, 0],
        Coxa_L: [-0.20, 0, 0.14], Canela_L: [-0.28, 0, 0]
      });
    },
    assentando: function (t) {
      var a = (t * 0.42) % 1;
      var f = a < 0.45 ? (a / 0.45) : 1 - ((a - 0.45) / 0.55);
      f = f * f * (3 - 2 * f);
      var bate = a > 0.80 ? Math.abs(Math.sin((a - 0.80) * 36)) : 0;
      return mescla(POSES.em_pe, {
        _y: -0.24 * f,
        Quadril: [0.10 + 0.20 * f, 0, 0], Torso: [0.18 + 0.28 * f, 0.08, 0],
        Cabeca: [0.28 + 0.14 * f, 0, 0],
        Braco_R: [0.85 + 0.30 * f - 0.40 * bate, 0, 0.22], Antebraco_R: [1.05 - 0.40 * f, 0, 0],
        Braco_L: [0.80 + 0.30 * f, 0, 0.22], Antebraco_L: [1.00 - 0.35 * f, 0, 0],
        Coxa_R: [0.10 + 0.85 * f, 0, 0.14], Canela_R: [-0.12 - 1.70 * f, 0, 0],
        Coxa_L: [-0.06 + 0.75 * f, 0, 0.14], Canela_L: [-0.18 - 1.50 * f, 0, 0]
      });
    },
    olhando_cima: function (t) {
      var g = Math.sin(t * 0.75);
      return mescla(POSES.em_pe, {
        Torso: [-0.10, 0.08 * g, 0], Cabeca: [-0.44, 0.16 * g, 0],
        Braco_R: [1.95, 0, 0.32], Antebraco_R: [1.85, 0, 0],
        Braco_L: [-0.06, 0, 0.46], Antebraco_L: [0.35, 0, 0]
      });
    },
    descanso: function (t) {
      var s = Math.sin(t * 0.85), limpa = Math.max(0, Math.sin(t * 0.4 - 1.3));
      return mescla(POSES.maos_na_cintura, {
        Quadril: [0, 0.05 * s, 0], Torso: [0.03, 0.08 * s, 0], Cabeca: [-0.06, 0.14 * s, 0],
        Braco_R: [-0.10 + 1.75 * limpa, 0, 0.52 - 0.22 * limpa],
        Antebraco_R: [1.25 + 0.80 * limpa, 0, -0.45]
      });
    },
    amarrando: function (t) {
      var s = Math.sin(t * 7.2);
      return mescla(POSES.agachado, {
        _y: -0.23,
        Torso: [0.34, 0.08 * s, 0], Cabeca: [0.40, 0, 0],
        Braco_R: [0.92, -0.16 * s, 0.16], Antebraco_R: [0.95 + 0.22 * s, 0, 0],
        Braco_L: [0.88, 0.16 * s, 0.16], Antebraco_L: [1.00 - 0.22 * s, 0, 0]
      });
    },
    puxando: function (t) {
      var a = t * 2.4, s = 0.5 + 0.5 * Math.sin(a), c = 1 - s;
      return mescla(POSES.em_pe, {
        Quadril: [-0.06, 0, 0], Torso: [-0.12, 0.08 * (s - 0.5), 0], Cabeca: [-0.22, 0, 0],
        Braco_R: [2.25 - 0.90 * s, 0, 0.20], Antebraco_R: [0.35 + 0.95 * s, 0, 0],
        Braco_L: [2.25 - 0.90 * c, 0, 0.20], Antebraco_L: [0.35 + 0.95 * c, 0, 0],
        Coxa_R: [0.08, 0, 0.13], Coxa_L: [-0.08, 0, 0.13]
      });
    },
    conferindo: function (t) {
      var g = Math.sin(t * 1.5), h = Math.sin(t * 0.6);
      return mescla(POSES.em_pe, {
        Torso: [0.02, 0.10 * h, 0], Cabeca: [-0.12 - 0.12 * g, 0.20 * h, 0],
        Braco_R: [1.45 + 0.25 * h, 0, 0.22 + 0.18 * h], Antebraco_R: [0.20, 0, 0],
        Braco_L: [-0.04, 0, 0.14], Antebraco_L: [0.30, 0, 0]
      });
    },
    vestindo: function (t) {
      var a = (t * 0.5) % 1, s = Math.sin(t * 2.6), alto = a < 0.5;
      return mescla(POSES.em_pe, {
        Torso: [0.06, 0.06 * s, 0], Cabeca: [0.28 + (alto ? -0.10 : 0.10), 0.10 * s, 0],
        Braco_R: [(alto ? 0.55 : 0.20) + 0.10 * s, 0, 0.46], Antebraco_R: [(alto ? 1.60 : 1.25) + 0.18 * s, 0, -0.35],
        Braco_L: [(alto ? 0.55 : 0.20) - 0.10 * s, 0, 0.46], Antebraco_L: [(alto ? 1.60 : 1.25) - 0.18 * s, 0, -0.35]
      });
    }
  };

  /* clipes que rodam em ciclo: podem começar em qualquer ponto do ciclo, o que
     serve para dessincronizar os figurantes uns dos outros. */
  var CICLICO = {
    parado: 1, falando: 1, andando: 1, andando_carregando: 1, andando_empurrando: 1,
    trabalhando: 1, radio: 1, carregando: 1, empurrando: 1, subindo: 1, tonto: 1,
    suspenso: 1, caido: 1, desequilibrio: 1, martelando: 1, serrando: 1, varrendo: 1,
    prancheta: 1, cavando: 1, pintando: 1, misturando: 1, assentando: 1,
    olhando_cima: 1, descanso: 1, amarrando: 1, puxando: 1, conferindo: 1, vestindo: 1
  };

  /* ------------------------------------------------------------- caminhada
     A perna é resolvida ao contrário: primeiro decide-se onde o PÉ tem de
     estar (plantado no chão enquanto apoia, no ar enquanto avança) e só
     depois se calcula o ângulo da coxa e do joelho que põem o pé ali. É isso
     que tira o deslizamento e faz a passada parecer de gente. */
  var PASSO_POR_VEL = 0.82;    // metros por segundo quando vel = 1
  var L_PERNA = 0.43;          // coxa e canela têm o mesmo comprimento
  var QUADRIL_Y = 0.90;        // altura da junta do quadril em repouso
  var SOLA_Y = 0.045;          // altura do tornozelo com a perna esticada
  var PASSO_M = 0.42;          // comprimento de um passo
  var APOIO = 0.60;            // fração do ciclo com o pé no chão
  var ALTURA_PE = 0.07;        // o quanto o pé sobe ao avançar (é pouco, no andar de verdade)
  /* A descida do quadril não é enfeite: com a perna aberta o pé só alcança o chão
     se o quadril baixar. sqrt((2L)^2 - meioPasso^2) dá exatamente o quanto. */
  var QUEDA_QUADRIL = QUADRIL_Y - SOLA_Y -
      Math.sqrt(Math.max(0.01, 4 * L_PERNA * L_PERNA - Math.pow(0.6 * PASSO_M, 2)));

  /** ângulos da coxa e do joelho que levam o tornozelo até (frente, altura). */
  function pernaIK(frente, yPe, yQuadril) {
    var dy = yPe - yQuadril;                 // negativo: o pé está abaixo do quadril
    var d = Math.sqrt(dy * dy + frente * frente);
    var dmax = 2 * L_PERNA - 0.015;
    if (d > dmax) { var k = dmax / d; frente *= k; dy *= k; d = dmax; }
    var meio = Math.acos(clamp(d / (2 * L_PERNA), -1, 1));
    var psi = Math.atan2(frente, -dy);
    return [psi + meio, -2 * meio];          // coxa (+ = à frente), joelho (- = dobra)
  }

  /** um ciclo de caminhada a uma velocidade dada. */
  function marcha(t, vel) {
    var v = Math.max(0.25, (vel || 1) * PASSO_POR_VEL);      // metros por segundo
    var T = 2 * PASSO_M / v;                                 // segundos por ciclo
    var fase = (t / T) % 1;
    var exc = v * APOIO * T;                                 // recuo do pé apoiado
    function pe(ph) {
      if (ph < APOIO) {                                      // apoiado: recua junto com o corpo
        return [exc * (0.5 - ph / APOIO), 0];
      }
      var u = (ph - APOIO) / (1 - APOIO);                    // no ar: volta para a frente
      var e = u * u * (3 - 2 * u);
      return [exc * (-0.5 + e), ALTURA_PE * Math.sin(Math.PI * u)];
    }
    // o quadril desce no apoio duplo e sobe no meio do apoio, como no andar de verdade
    var yq = QUADRIL_Y - QUEDA_QUADRIL * (0.5 + 0.5 * Math.cos(12.5664 * fase));
    var pR = pe(fase), pL = pe((fase + 0.5) % 1);
    var iR = pernaIK(pR[0], SOLA_Y + pR[1], yq);
    var iL = pernaIK(pL[0], SOLA_Y + pL[1], yq);
    return { fase: fase, _y: yq - QUADRIL_Y,
             Coxa_R: [iR[0], 0, 0.05], Canela_R: [iR[1], 0, 0],
             Coxa_L: [iL[0], 0, 0.05], Canela_L: [iL[1], 0, 0] };
  }

  function mescla(a, b) {
    var r = {}, k;
    for (k in a) r[k] = a[k];
    for (k in b) r[k] = b[k];
    return r;
  }
  function escalar(p, f) {
    var r = {}, k;
    for (k in p) r[k] = [p[k][0] * f, p[k][1] * f, p[k][2] * f];
    return r;
  }

  /* ----------------------------------------------------------------- ator */
  function Ator(objRaiz) {
    this.raiz = objRaiz;
    this.pecas = {};
    this.base = {};
    var self = this;
    objRaiz.traverse(function (o) {
      var p = o.userData && o.userData.peca;
      if (p && PARTES.indexOf(p) >= 0 && !self.pecas[p]) {
        self.pecas[p] = o;
        self.base[p] = [o.rotation.x, o.rotation.y, o.rotation.z];
      }
    });
    this.ok = Object.keys(this.pecas).length >= 6;
    // tamanho da geometria própria de cada peça: um antebraço "grande" é alguém
    // com ferramenta comprida na mão (vassoura, pá, serrote) - esse braço não
    // pode balançar ao andar, senão a ferramenta varre as pernas
    this.tam = {};
    for (var tn in this.pecas) {
      var tg = this.pecas[tn].geometry;
      if (!tg) continue;
      if (!tg.boundingBox) tg.computeBoundingBox();
      var tsz = tg.boundingBox.getSize(new THREE.Vector3());
      this.tam[tn] = Math.max(tsz.x, tsz.y, tsz.z);
    }
    this.ferramentaLonga = (this.tam.Antebraco_R || 0) > 0.55;
    // repouso de cada peça, medido no referencial da raiz: é isso que permite
    // escrever as poses na convenção do boneco em vez do eixo cru de cada junta
    objRaiz.updateWorldMatrix(true, true);
    var qr = objRaiz.getWorldQuaternion(new THREE.Quaternion()).invert();
    this.frame = {};
    for (var nm in this.pecas) {
      var pc = this.pecas[nm];
      var qp = pc.parent.getWorldQuaternion(new THREE.Quaternion()).premultiply(qr);
      // tronco e cabeça apontam para CIMA, braço e coxa para BAIXO: o mesmo giro
      // no eixo X joga um para a frente e o outro para trás. O sinal abaixo faz
      // com que, em todas as peças, x positivo signifique "inclina para a frente".
      this.frame[nm] = { pai: qp, paiInv: qp.clone().invert(),
                         l0: pc.quaternion.clone(),
                         esp: nm.slice(-2) === '_L' ? -1 : 1,
                         sx: (nm === 'Quadril' || nm === 'Torso' || nm === 'Cabeca') ? -1 : 1 };
    }
    this.t = 0;
    this.fase = Math.random() * 9.7;   // cada um entra no ciclo num ponto diferente
    this.clip = 'parado';
    this.vel = 1;
    this.peso = 1;
    this.atual = {};
    this.alvoOlhar = null;
    this.forcaOlhar = 1;
    this.caminho = null;
    this.aoChegar = null;
    this.alturaBase = objRaiz.position.y;
    this.posBase = objRaiz.position.clone();
    this.rotBase = objRaiz.rotation.y;
    this._v = new THREE.Vector3();
    this._q = new THREE.Vector3();
    for (var k in this.base) this.atual[k] = [0, 0, 0];   // 0,0,0 = peça em repouso
  }

  /** devolve o personagem ao lugar e à pose de origem. */
  Ator.prototype.reiniciar = function () {
    this.raiz.position.copy(this.posBase);
    this.raiz.rotation.y = this.rotBase;
    if (this.queda) {
      if (this.queda.relogio) clearTimeout(this.queda.relogio);
      if (this.queda.aoFim) { this.queda.aoFim('cancelado'); this.queda.aoFim = null; }
    }
    this.queda = null;
    this.caminho = null;
    this.t = 0;
    this.rotOff = false;
    if (this.rot) { this.rot.fase = 'parado'; this.rot.rel = 0; this.rot.ate = Math.random() * this.rot.espera * 1.2; }
    return this;
  };

  Ator.prototype.tocar = function (clip, opc) {
    opc = P(opc);
    if (!CLIPES[clip]) clip = 'parado';
    if (this.clip !== clip) { this.clip = clip; this.t = 0; }
    if (opc.vel) this.vel = opc.vel;
    return this;
  };

  Ator.prototype.pose = function (nome) {
    this.clip = null;
    this.poseFixa = POSES[nome] || {};
    return this;
  };

  Ator.prototype.olhar = function (ponto, forca) {
    this.alvoOlhar = ponto ? new THREE.Vector3(ponto.x, ponto.y, ponto.z) : null;
    this.forcaOlhar = (forca === undefined) ? 1 : forca;
    return this;
  };

  /** anda por uma lista de pontos {x,y,z} em metros/segundo. devolve promessa. */
  Ator.prototype.andar = function (pontos, vel) {
    var self = this;
    this.caminho = pontos.map(function (p) { return new THREE.Vector3(p.x, p.y, p.z); });
    this.velAndar = vel || 0.85;
    this.tocar('andando', { vel: this.velAndar / PASSO_POR_VEL });
    return new Promise(function (ok) { self.aoChegar = ok; });
  };

  /** rotina de canteiro: caminha entre os pontos e executa uma tarefa em cada um.
      pts = [x,z, x,z, ...] já no espaço do Three.js. */
  Ator.prototype.rotina = function (pts, atividades, opc) {
    opc = P(opc);
    var lista = [];
    for (var i = 0; i + 1 < pts.length; i += 2) lista.push(new THREE.Vector3(pts[i], this.raiz.position.y, pts[i + 1]));
    if (lista.length < 2) return this;
    var esp = opc.espera || 12;
    this.rot = {
      pts: lista, i: 0,
      ativ: atividades && atividades.length ? atividades : ['parado'],
      esperas: (opc.esperas && opc.esperas.length) ? opc.esperas : null,
      vel: opc.vel || 0.85, espera: esp, fase: 'parado',
      rel: 0, ate: 1.0 + Math.random() * esp, tarefa: null
    };
    this.tocar(this.rot.ativ[0]);          // começa fazendo o serviço do primeiro ponto
    return this;
  };

  /** suspende a rotina de canteiro (a encenação assume o corpo); reversível. */
  Ator.prototype.semRotina = function () { this.rotOff = true; this.caminho = null; return this; };
  Ator.prototype.voltarRotina = function () {
    this.rotOff = false;
    if (this.rot) { this.rot.fase = 'parado'; this.rot.rel = 0; this.rot.ate = 0.4 + Math.random(); }
    return this;
  };

  /** o corpo cai de verdade: clipe de queda + gravidade no tronco. */
  Ator.prototype.cair = function (opc) {
    opc = P(opc);
    this.semRotina();
    // chao e retido vem em metros RELATIVOS ao piso onde o personagem está.
    // Quando o talabarte segura (retido), o piso fica fora do caminho: senão a
    // queda terminaria no chão antes de a corda esticar.
    var temRet = (opc.retido !== undefined && opc.retido !== null);
    var baixo = (opc.chao !== undefined) ? opc.chao : (temRet ? opc.retido - 12 : -0.6);
    this.queda = {
      v: opc.v0 || 0,
      chao: this.alturaBase + baixo,
      frente: opc.frente || 0, aoFim: null, t: 0,
      retido: temRet ? this.alturaBase + opc.retido : null
    };
    this.tocar('queda_corpo');
    var self = this;
    // prazo de relógio: se o navegador parar de desenhar (aba em segundo plano),
    // a queda termina mesmo assim e a prova não trava
    var alvoY = (this.queda.retido !== null) ? this.queda.retido : this.queda.chao;
    var alturaQueda = Math.max(0.2, this.raiz.position.y - alvoY);
    var prazo = Math.sqrt(2 * alturaQueda / 9.81) + 2.5;
    return new Promise(function (ok) {
      self.queda.aoFim = ok;
      self.queda.relogio = setTimeout(function () {
        var q = self.queda;
        if (!q) return;
        self.raiz.position.y = alvoY;
        self.queda = null;
        self.tocar(q.retido !== null ? 'suspenso' : 'caido');
        if (q.aoFim) { q.aoFim(q.retido !== null ? 'retido' : 'chao'); q.aoFim = null; }
      }, prazo * 1000);
    });
  };

  Ator.prototype.parar = function () {
    this.caminho = null;
    if (this.aoChegar) { var f = this.aoChegar; this.aoChegar = null; f(); }
    this.tocar('parado');
    return this;
  };

  Ator.prototype.virarPara = function (ponto) {
    var d = new THREE.Vector3(ponto.x - this.raiz.position.x, 0, ponto.z - this.raiz.position.z);
    if (d.lengthSq() > 1e-6) this.raiz.rotation.y = Math.atan2(-d.x, -d.z);
    return this;
  };

  var TMP = new THREE.Vector3(), TMP2 = new THREE.Vector3();

  Ator.prototype.atualizar = function (dt) {
    if (!this.ok) return;
    this.t += dt;

    // queda do corpo (consequência animada)
    if (this.queda) {
      var q = this.queda;
      q.t += dt;
      q.v -= 9.81 * dt;
      this.raiz.position.y += q.v * dt;
      this.raiz.position.x -= Math.sin(this.raiz.rotation.y) * q.frente * dt;
      this.raiz.position.z -= Math.cos(this.raiz.rotation.y) * q.frente * dt;
      if (q.retido !== null && this.raiz.position.y <= q.retido) {
        this.raiz.position.y = q.retido;                 // o talabarte segurou
        this.queda = null;
        if (q.relogio) clearTimeout(q.relogio);
        this.tocar('suspenso');
        if (q.aoFim) { q.aoFim('retido'); q.aoFim = null; }
      } else if (this.raiz.position.y <= q.chao) {
        this.raiz.position.y = q.chao;
        this.queda = null;
        if (q.relogio) clearTimeout(q.relogio);
        this.tocar('caido');
        if (q.aoFim) { q.aoFim('chao'); q.aoFim = null; }
      }
      var alvoQ = CLIPES[this.clip] ? CLIPES[this.clip](this.t, this.vel) : {};
      aplicarPose(this, alvoQ, Math.min(1, dt * 12));
      return;
    }

    // rotina de canteiro (relógio próprio: o clipe reinicia o this.t)
    if (this.rot && !this.rotOff && !this.caminho) {
      var R = this.rot;
      R.rel += dt;
      if (R.fase === 'parado') {
        if (R.rel >= R.ate) {
          var de = R.i;                          // de onde estou saindo
          R.i = (R.i + 1) % R.pts.length;
          R.fase = 'indo'; R.rel = 0;
          this.andar([R.pts[R.i]], R.vel);
          // quem sai de um ponto de material volta carregado
          var levando = R.ativ[de % R.ativ.length];
          this.tocar(levando === 'carregando' ? 'andando_carregando'
                   : (levando === 'empurrando' ? 'andando_empurrando' : 'andando'),
                   { vel: this.velAndar / PASSO_POR_VEL });
        }
      } else {
        R.fase = 'parado'; R.rel = 0;
        R.tarefa = R.ativ[R.i % R.ativ.length];  // a tarefa é a DAQUELE ponto
        var base = R.esperas ? R.esperas[R.i % R.esperas.length] : R.espera;
        R.ate = base * (0.85 + Math.random() * 0.3);
        this.tocar(R.tarefa);
      }
    }

    // deslocamento pelo caminho
    if (this.caminho && this.caminho.length) {
      var destino = this.caminho[0];
      TMP.set(destino.x - this.raiz.position.x, 0, destino.z - this.raiz.position.z);
      var d = TMP.length();
      if (d < 0.12) {
        this.caminho.shift();
        if (!this.caminho.length) {
          this.caminho = null;
          this.tocar('parado');
          if (this.aoChegar) { var f = this.aoChegar; this.aoChegar = null; f(); }
        }
      } else {
        TMP.divideScalar(d);
        var passo = Math.min(d, this.velAndar * dt);
        this.raiz.position.x += TMP.x * passo;
        this.raiz.position.z += TMP.z * passo;
        var alvoY = Math.atan2(-TMP.x, -TMP.z);   // o boneco olha para o -Z dele
        this.raiz.rotation.y += anguloCurto(alvoY - this.raiz.rotation.y) * Math.min(1, dt * 5);
      }
    }

    // pose alvo, misturada na convenção do boneco
    var fn = this.clip && CLIPES[this.clip];
    var tc = this.t + (CICLICO[this.clip] ? this.fase : 0);
    var alvo = fn ? fn(tc, this.vel) : (this.poseFixa || POSES.em_pe);
    // clipes agachados abaixam o corpo, e a caminhada traz o balanço do quadril
    var yAlvo = this.alturaBase + (alvo._y || 0);
    this.raiz.position.y += (yAlvo - this.raiz.position.y) * Math.min(1, dt * 12);

    var k, mist = Math.min(1, dt * 9);
    var travar = this.bracosPresos ? BRACOS : null;
    var segura = (!travar && this.ferramentaLonga && !USA_FERRAMENTA[this.clip]) ? SEGURA_FERRAMENTA : null;
    for (k in this.pecas) {
      var a = (travar && travar[k]) ? ZERO : ((segura && segura[k]) || alvo[k] || ZERO);
      var c = this.atual[k];
      c[0] += (a[0] - c[0]) * mist;
      c[1] += (a[1] - c[1]) * mist;
      c[2] += (a[2] - c[2]) * mist;
    }

    // olhar para um ponto: entra somado à pose, não por cima dela
    var olhoX = 0, olhoY = 0, troncoY = 0;
    if (this.alvoOlhar && this.pecas.Cabeca) {
      this.raiz.updateWorldMatrix(true, false);
      TMP2.copy(this.alvoOlhar);
      this.raiz.worldToLocal(TMP2);
      var dist = Math.sqrt(TMP2.x * TMP2.x + TMP2.z * TMP2.z);
      var yaw = clamp(Math.atan2(-TMP2.x, -TMP2.z), -1.1, 1.1) * this.forcaOlhar;
      var pitch = clamp(-Math.atan2(TMP2.y - 1.55, Math.max(0.2, dist)), -0.6, 0.7) * this.forcaOlhar;
      olhoY = clamp(yaw * 0.70, -0.8, 0.8);
      olhoX = clamp(pitch * 0.80, -0.5, 0.6);
      troncoY = clamp(yaw * 0.30, -0.4, 0.4);
    }

    for (k in this.pecas) {
      if (k === 'Cabeca') escrever(this, k, this.atual[k], olhoX, olhoY);
      else if (k === 'Torso') escrever(this, k, this.atual[k], 0, troncoY);
      else escrever(this, k, this.atual[k]);
    }
  };

  var _eq = new THREE.Euler(0, 0, 0, 'XYZ'), _qq = new THREE.Quaternion();
  var ZERO = [0, 0, 0];
  // quem carrega caixa ou tábua tem a carga colada no tronco, na posição em que
  // as mãos estavam quando o modelo foi feito: esses braços ficam no repouso
  var BRACOS = { Braco_R: 1, Antebraco_R: 1, Braco_L: 1, Antebraco_L: 1 };
  var ANDANDO = { andando: 1, andando_carregando: 1, andando_empurrando: 1 };
  // clipes que já seguram a ferramenta do jeito certo; fora deles, quem tem
  // ferramenta comprida na mão a carrega inclinada, para não varrer o chão
  var USA_FERRAMENTA = {
    varrendo: 1, cavando: 1, serrando: 1, martelando: 1, amarrando: 1, pintando: 1,
    misturando: 1, assentando: 1, trabalhando: 1, puxando: 1, prancheta: 1, radio: 1
  };
  var SEGURA_FERRAMENTA = { Braco_R: [0.52, 0, 0.16], Antebraco_R: [0.24, 0, 0] };

  /** escreve na peça um giro dado na convenção do boneco.
      local = (repouso do pai)^-1 * giro * (repouso do pai) * (repouso da peça) */
  function escrever(ator, nome, e, maisX, maisY) {
    var f = ator.frame[nome];
    if (!f) return;
    _eq.set((e[0] + (maisX || 0)) * f.sx, (e[1] + (maisY || 0)) * f.esp, e[2] * f.esp);
    _qq.setFromEuler(_eq);
    ator.pecas[nome].quaternion.copy(f.paiInv).multiply(_qq).multiply(f.pai).multiply(f.l0);
  }

  function aplicarPose(ator, alvo, mist) {
    for (var k in ator.pecas) {
      var a = alvo[k] || ZERO;
      var c = ator.atual[k];
      c[0] += (a[0] - c[0]) * mist;
      c[1] += (a[1] - c[1]) * mist;
      c[2] += (a[2] - c[2]) * mist;
      escrever(ator, k, c);
    }
  }

  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function anguloCurto(a) {
    while (a > Math.PI) a -= Math.PI * 2;
    while (a < -Math.PI) a += Math.PI * 2;
    return a;
  }

  /* ------------------------------------------------------------- diretor */
  var A = { atores: {}, lista: [], POSES: POSES, CLIPES: CLIPES };

  /** cria (ou devolve) o ator de um personagem pelo nome do objeto raiz. */
  A.ator = function (nome, obj) {
    if (A.atores[nome]) return A.atores[nome];
    if (!obj) return null;
    var a = new Ator(obj);
    if (!a.ok) return null;
    A.atores[nome] = a;
    A.lista.push(a);
    return a;
  };

  A.atualizar = function (dt) {
    for (var i = 0; i < A.lista.length; i++) {
      var a = A.lista[i];
      if (a.raiz.visible) a.atualizar(dt);
    }
    separar();
  };

  /** ninguém ocupa o lugar de ninguém. Quem está no posto não sai do lugar (a cena
      foi enquadrada com ele ali); quem está de passagem é que contorna. */
  var RAIO = 0.80, RAIO2 = RAIO * RAIO;
  function separar() {
    var L = A.lista, i, j;
    for (i = 0; i < L.length; i++) {
      var a = L[i];
      if (!a.rot || a.queda || !a.raiz.visible) continue;   // só quem anda desvia
      for (j = 0; j < L.length; j++) {
        if (j === i) continue;
        var b = L[j];
        if (b.queda || !b.raiz.visible) continue;
        var dy = b.raiz.position.y - a.raiz.position.y;
        if (dy > 1.2 || dy < -1.2) continue;                // pavimentos diferentes
        var dx = b.raiz.position.x - a.raiz.position.x;
        var dz = b.raiz.position.z - a.raiz.position.z;
        var d2 = dx * dx + dz * dz;
        if (d2 > RAIO2) continue;
        if (d2 < 1e-6) { a.raiz.position.x += RAIO; continue; }
        var d = Math.sqrt(d2);
        var passo = (RAIO - d) * (b.rot ? 0.5 : 1.0) / d;   // se o outro também anda, dividem
        a.raiz.position.x -= dx * passo;
        a.raiz.position.z -= dz * passo;
      }
    }
  }

  /** pose inicial sugerida pelo nome da pose que veio do Blender */
  A.CLIP_DA_POSE = {
    em_pe: 'parado', andando: 'andando', correndo: 'andando', conversando: 'falando',
    falando_radio: 'radio', comunicando_radio_agachado: 'radio', apontando: 'falando',
    agachado_trabalhando: 'trabalhando', ajoelhado_olhando: 'trabalhando',
    abaixado_pegando: 'trabalhando', escorregando: 'escorregando', tontura: 'tonto',
    suspenso: 'suspenso', empurrando: 'empurrando', movendo_barreira: 'empurrando',
    subindo_escada: 'subindo', assustado: 'assustado', carregando_frente: 'carregando',
    carregando_ombro: 'carregando', desequilibrio_frente: 'desequilibrio',
    desequilibrio_tras: 'desequilibrio', tropecando: 'tropecando',
    vestindo_conferencia: 'vestindo', entregando_tablet: 'falando', segurando_tablet: 'prancheta',
    martelando: 'martelando', serrando: 'serrando', varrendo: 'varrendo',
    conferindo_prancheta: 'prancheta', cavando: 'cavando', pintando: 'pintando',
    misturando_argamassa: 'misturando', assentando_bloco: 'assentando',
    amarrando_ferragem: 'amarrando', puxando_corda: 'puxando', descansando: 'descanso',
    removendo_gcr: 'trabalhando', empurrando_gcr: 'empurrando', ferramenta_tranco: 'desequilibrio',
    sinalizando_pare: 'conferindo', olhando_cima: 'olhando_cima'
  };

  raiz.Anim = A;
  raiz.Ator = Ator;
})(window);
