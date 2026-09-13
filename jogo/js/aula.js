/* aula.js — a instrução que vem antes da prova.
   Se existir um vídeo em aula/aula.mp4, ele é a aula. Senão, entra a aula em
   slides montada com os quadros do storyboard. */
(function (raiz) {
  'use strict';

  var A = {};
  var $ = function (id) { return document.getElementById(id); };
  var i = 0, S = [], aoFim = null, viuTudo = false;

  /* Cada slide cobre um ponto que a prova depois cobra. */
  A.slides = [
    { q: 'C01_1P', t: 'Como este treinamento funciona',
      p: ['Você vai entrar no canteiro em primeira pessoa e realizar um serviço de verdade.',
          'O caminho é sempre o mesmo: observar → pensar → decidir → executar → perceber a consequência.',
          'Algumas escolhas cobram na hora. Outras só aparecem alguns minutos depois.',
          'Nada aqui é pegadinha: tudo o que você precisa saber está no ambiente.'] },
    { q: 'C02_1P', t: 'Antes de subir: você está liberado?',
      p: ['Trabalho em altura exige treinamento, aptidão e autorização para aquela atividade.',
          'Tempo de obra e experiência ajudam, mas não substituem a liberação.',
          'A autorização de um colega não vale para você.'] },
    { q: 'C03_1P', t: 'Dá para evitar a exposição?',
      p: ['A primeira pergunta não é "qual cinturão eu uso", e sim "dá para fazer sem expor alguém à queda?".',
          'Só quando não é possível evitar é que se trabalha com o sistema de proteção definido.'] },
    { q: 'C04_1P', t: 'O planejamento é o de hoje',
      p: ['ANÁLISE DE RISCO é a avaliação feita antes do serviço: o que pode dar errado e como trabalhar com segurança.',
          'PERMISSÃO DE TRABALHO é a liberação usada para determinadas atividades antes de começar.',
          'Um serviço parecido na semana passada não significa que as condições continuam iguais.'] },
    { q: 'C05_1P', t: 'O que a permissão define',
      p: ['Local, atividade, acesso previsto, proteção da periferia e sistema de proteção da área de execução.',
          'Área abaixo isolada, ferramentas protegidas contra queda, meio de comunicação e procedimento de emergência.',
          'Você não precisa decorar: precisa conferir se o que foi planejado existe mesmo no local.'] },
    { q: 'C06_1P', t: 'Inspecionar antes de usar',
      p: ['Capacete: trincas e rachaduras tiram o equipamento de uso.',
          'Cinturão: olhe fitas, costuras e fivelas. Corte pequeno também é dano.',
          'Talabarte: desgaste tira de uso. Não se conserta equipamento de proteção — solicite outro.'] },
    { q: 'C07_3P_correto', t: 'Vestir e conferir',
      p: ['Fita torcida, fivela aberta, ajuste frouxo ou equipamento colocado ao contrário anulam a proteção.',
          'Confira antes de entrar na área com risco de queda — e peça para alguém conferir junto.'] },
    { q: 'C09_1P', t: 'O acesso é o que foi previsto',
      p: ['Use o acesso definido para a atividade, mesmo quando existe um caminho mais curto ao lado.',
          'Nem toda escada encontrada na obra é meio adequado de acesso.',
          'Obstáculo no caminho não se normaliza: peça para liberar.'] },
    { q: 'C11_1P', t: 'Aberturas e proteções coletivas',
      p: ['Abertura no piso deve estar protegida — e proteção não se retira nem se altera sem autorização.',
          'Encontrou proteção deslocada? Impeça a passagem e comunique.',
          'Improvisar uma madeira solta por cima cria um risco novo.',
          'Um risco não deixa de existir porque pertence ao serviço de outra pessoa.'] },
    { q: 'C13_1P', t: 'Guarda-corpo: olhe de perto',
      p: ['Uma proteção não precisa estar caída para apresentar problema.',
          'Encontrou um trecho solto? Comunique e aguarde a correção.',
          'Não tente empurrar de volta: você não sabe se está corretamente fixada.'] },
    { q: 'C14_1P', t: 'Quem está embaixo',
      p: ['A área abaixo da frente de trabalho precisa ficar isolada.',
          '"Todo mundo vê que estamos trabalhando" não é isolamento.',
          'Se alguém passa pela barreira, o isolamento deixou de cumprir a função: pare e restabeleça.'] },
    { q: 'C18_1P', t: 'Ponto de ancoragem é o previsto',
      p: ['Conecte-se ao ponto definido e identificado para a atividade.',
          'Tubulação, vergalhão e guarda-corpo não são ponto de ancoragem por padrão — mesmo parecendo fortes.',
          'Identificação ilegível? Pare e confirme. Falta de informação não autoriza escolher por conta própria.',
          'Ninguém prende o equipamento de outra pessoa no seu ponto sem confirmação.'] },
    { q: 'C20_1P', t: 'Ferramenta que cai vira risco lá embaixo',
      p: ['Ferramentas e pequenas peças precisam de proteção contra queda: cordão, bolsa fechada, amarração.',
          '"Eu seguro bem" e "ninguém vai ficar embaixo" não são medidas de proteção.',
          'Isolar a área abaixo e proteger a ferramenta são duas coisas diferentes — e as duas são necessárias.'] },
    { q: 'EV10_1P', t: 'A obra muda enquanto você trabalha',
      p: ['Material aparece na rota, outra equipe movimenta carga, o vento muda, uma proteção é alterada no intervalo.',
          'Verificar uma vez não significa que o local vai continuar igual.',
          'Não existe regra inventada do tipo "choveu = proibido": o critério é o que foi definido para a atividade.',
          'Quando a condição muda e não está prevista: pare, comunique e reavalie. Nunca improvise.'] },
    { q: 'EV05_1P', t: 'Comunicação faz parte do sistema',
      p: ['Se o rádio foi definido como meio de comunicação, trabalhar sem ele é trabalhar fora do planejado.',
          'Problema pequeno agora costuma ser exatamente o que falta na hora de pedir ajuda.'] },
    { q: 'EMERG_3P_A', t: 'Emergência: acionar, não improvisar',
      p: ['Resgate em altura tem procedimento e equipe preparada — isso existe antes da atividade começar.',
          'Subir sozinho para puxar a vítima transforma você na segunda vítima.',
          'Chamar ambulância pode ser necessário, mas não substitui a resposta prevista para trabalhador suspenso.'] },
    { q: 'C12_1P', t: 'Agora é com você',
      p: ['A prova é a sua jornada de trabalho: ajustar e fixar um suporte junto à borda do 4º pavimento.',
          'Arraste o mouse para olhar em volta. As decisões aparecem na parte de baixo da tela.',
          'Quando uma escolha ficar guardada para cobrar depois, você vê o aviso "Isso ficou registrado".',
          'No fim você recebe um relatório por categoria — não uma nota solta.'] }
  ];

  A.iniciar = function (cb) {
    aoFim = cb;
    S = A.slides;
    $('aula-total').textContent = S.length;
    montarPassos();
    $('aula-avancar').addEventListener('click', function () { ir(i + 1); });
    $('aula-voltar').addEventListener('click', function () { ir(i - 1); });
    $('aula-sair').addEventListener('click', terminar);
    document.addEventListener('keydown', function (e) {
      if ($('tela-aula').hidden) return;
      if (e.key === 'ArrowRight') ir(i + 1);
      if (e.key === 'ArrowLeft') ir(i - 1);
    });
    verVideo();
  };

  /* ---- vídeo, quando existir --------------------------------------------- */
  function verVideo() {
    var v = $('aula-video');
    fetch('aula/aula.mp4', { method: 'HEAD' }).then(function (r) {
      if (!r.ok) throw 0;
      v.hidden = false;
      v.src = 'aula/aula.mp4';
      $('aula-img').hidden = true;
      $('aula-titulo').textContent = 'Aula em vídeo';
      $('aula-pontos').innerHTML = '<li>Assista à instrução completa. O botão para a prova libera no fim do vídeo.</li>';
      $('aula-passos').hidden = true;
      $('aula-avancar').hidden = true;
      $('aula-voltar').hidden = true;
      $('aula-sair').hidden = false;
      $('aula-sair').disabled = true;
      $('aula-sair').textContent = 'Assista até o fim';
      v.addEventListener('ended', function () {
        $('aula-sair').disabled = false;
        $('aula-sair').textContent = 'Iniciar a prova';
      });
    }).catch(function () { ir(0); });
  }

  function montarPassos() {
    $('aula-passos').innerHTML = S.map(function (_, k) {
      return '<button type="button" class="passo" data-k="' + k + '" aria-label="slide ' + (k + 1) + '"></button>';
    }).join('');
    $('aula-passos').addEventListener('click', function (e) {
      var b = e.target.closest('.passo');
      if (b) ir(+b.dataset.k);
    });
  }

  function ir(k) {
    if (k < 0) return;
    if (k >= S.length) { if (viuTudo) terminar(); return; }
    i = k;
    if (i === S.length - 1) viuTudo = true;
    var s = S[i];
    $('aula-n').textContent = i + 1;
    $('aula-titulo').textContent = s.t;
    var img = $('aula-img');
    img.hidden = false;
    img.src = (raiz.PASTA_QUADROS || '../renders/storyboard/') + s.q + '.jpg';
    img.alt = s.t;
    $('aula-pontos').innerHTML = s.p.map(function (x) { return '<li>' + x + '</li>'; }).join('');
    $('aula-voltar').disabled = i === 0;
    $('aula-avancar').textContent = (i === S.length - 1) ? 'Iniciar a prova' : 'Avançar';
    $('aula-sair').hidden = !viuTudo || i === S.length - 1;
    Array.prototype.forEach.call(document.querySelectorAll('.passo'), function (b, k2) {
      b.classList.toggle('ativo', k2 === i);
      b.classList.toggle('visto', k2 < i);
    });
  }

  function terminar() { if (aoFim) aoFim(); }

  raiz.Aula = A;
})(window);
