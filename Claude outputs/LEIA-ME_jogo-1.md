# Aula e Prova — Trabalho em Altura (protótipo jogável)

Jogo de escolha e consequência no canteiro 3D, no estilo *Minecraft: Story Mode*: você não
controla um personagem correndo pelo mapa — você **para em cada ponto, olha em volta, ouve e
decide**. A câmera viaja sozinha de uma cena para a outra e só sai da primeira pessoa para
mostrar **a consequência** de uma escolha.

O fluxo é **aula → prova → resultado**: primeiro a instrução, depois a jornada de trabalho
valendo avaliação.

---

## 1. Como abrir

Dê dois cliques em **`abrir_jogo.bat`**. Ele sobe um servidor local, espera a porta responder e
só então abre `http://localhost:8765/jogo/` no navegador. Fica uma janela minimizada chamada
**“servidor do treinamento”** — fechar essa janela encerra o jogo.

O `.bat` tenta, nesta ordem: `py -3` → `python` → **PowerShell**. Como o PowerShell já vem no
Windows, **não é preciso instalar nada**: o `servidor.ps1` desta pasta é um servidor de arquivos
mínimo que roda direto.

> Abrir o `index.html` com dois cliques **não funciona**: o navegador bloqueia a leitura do
> modelo 3D em `file://`. Tem que ser pelo `.bat` (ou por qualquer outro servidor web).

**Se aparecer “Não é possível acessar esse site / ERR_CONNECTION_REFUSED”:** o servidor não
subiu. Rode o `.bat` de novo e leia a janela preta — ela agora diz qual motor usou e, quando
falha, explica o motivo. Os dois casos comuns:

- **Porta 8765 ocupada** por outro programa → abra o `abrir_jogo.bat` no Bloco de Notas e troque
  `set PORTA=8765` por `set PORTA=8766`.
- **PowerShell bloqueado** pela política da empresa ou pelo antivírus → instale o Python em
  python.org (marque *Add python.exe to PATH*) e rode o `.bat` de novo.

Para colocar na intranet da empresa depois, é só publicar a pasta
`canteiro_trabalho_altura_arquivos` em qualquer servidor web e apontar o pessoal para `/jogo/`.

Requisitos: navegador com WebGL2 (Chrome, Edge, Opera ou Firefox atuais). Nada é instalado e nada
sai da máquina — o three.js e o decodificador Draco estão em `jogo/vendor/`, então o jogo roda
**sem internet**.

## 2. As três partes

### Aula
Dezessete telas com os quadros renderizados do próprio canteiro, cobrindo exatamente o que a
prova depois cobra: liberação, planejamento, inspeção de EPI, acesso, aberturas e proteções
coletivas, guarda-corpo, área abaixo, ponto de ancoragem, ferramentas, mudança de condições,
comunicação e emergência.

**Para usar um vídeo no lugar dos slides:** salve o arquivo como `jogo/aula/aula.mp4`. O jogo
detecta sozinho, toca o vídeo e só libera o botão *Iniciar a prova* quando ele terminar. A aula
em slides serve como roteiro pronto para gravar esse vídeo.

### Prova
- **Primeira pessoa o tempo todo.** Arraste o mouse (ou o dedo) para olhar em volta — o giro é
  limitado, você está parado no ponto de trabalho, não voando pelo canteiro.
- **A câmera anda no trilho.** Entre uma cena e outra ela viaja suave até a próxima posição;
  a duração é proporcional à distância.
- **Roda de diálogo sem tempo.** As opções aparecem embaixo e esperam. Não existe contagem
  regressiva: a pressa do canteiro vem das falas dos personagens, não de um cronômetro.
- **“Isso ficou registrado.”** Quando a escolha grava uma variável que vai ser cobrada depois,
  aparece o aviso no canto — é o “fulano vai lembrar disso”.
- **Terceira pessoa só na consequência.** Entram as tarjas pretas, a faixa laranja *3ª pessoa*,
  e quando o roteiro pede “congelar” a imagem trava com a palavra CONGELADO. Terminado o
  trecho, a câmera volta para a primeira pessoa.
- **Eventos sorteados.** De 3 a 5 dos 17 eventos entram em cada partida, respeitando os pares
  que não podem sair juntos, o limite de 2 eventos pesados e as pré-condições (a invasão da
  área isolada, por exemplo, só acontece se você tiver isolado a área). Jogar de novo dá uma
  partida diferente.
- **A queda da ferramenta acontece sempre**, com um dos três desfechos, conforme o que você
  decidiu lá atrás sobre proteger as ferramentas e isolar a área abaixo.
- Se você insistir numa opção que o roteiro manda repensar, na terceira tentativa o instrutor
  segue pelo caminho previsto explicando o porquê — e o relatório continua marcando a sua
  tentativa.

### Resultado
Relatório por **13 categorias** (correto / precisa melhorar / não avaliado nesta execução),
um dos três desfechos do roteiro, e **Ver minhas decisões**: a lista do que você escolheu, com
o quadro da cena, as variáveis gravadas e onde a câmera foi para a terceira pessoa. Havendo
erro crítico, aparece também *Refazer situações críticas*.

## 3. Arquivos

```
jogo/
  index.html            telas (carga, abertura, aula, HUD, resultado, revisão)
  abrir_jogo.bat        sobe o servidor local e abre o navegador
  servidor.ps1          servidor de arquivos em PowerShell (usado quando não há Python)
  css/jogo.css          identidade visual (concreto, fita zebrada, guarda-corpo)
  js/dados.js           carrega o roteiro, indexa e sorteia os eventos
  js/cena3d.js          three.js: .glb + Draco, visibilidade, trilho da câmera, olhar livre
  js/ui.js              fala, roda de escolhas, avisos, telas, marcas de 3ª pessoa
  js/aula.js            aula em vídeo ou em slides
  js/motor.js           a prova: estados, variáveis, consequências, relatório
  js/main.js            amarra tudo
  vendor/               three.js r128 + GLTFLoader + DRACOLoader + decodificador Draco
  aula/                 coloque aqui o aula.mp4 (veja LEIA-ME_video.txt)
```

O jogo consome, da pasta acima: `canteiro_trabalho_altura_draco.glb` (o canteiro),
`roteiro_treinamento.json` (todo o roteiro) e `renders/storyboard/` (os quadros da aula e da
revisão). **Nada do roteiro está escrito dentro do código** — mexer no JSON muda o jogo.

## 4. Mexer no conteúdo

| Quero mudar | Onde |
|---|---|
| Uma fala, uma opção, uma consequência | `../roteiro_treinamento.json` (gerado por `../fontes/roteiro_json.py`) |
| Quantos eventos por partida, pares proibidos | `sorteio_de_eventos` no mesmo JSON |
| O texto da aula | `A.slides` em `js/aula.js` |
| O vídeo da aula | `jogo/aula/aula.mp4` |
| Posição de câmera, objeto, variante | Blender → `gen_40`…`gen_43` → exportar o `.glb` de novo |
| Quantas tentativas antes do instrutor seguir | `MAX_TENTATIVAS` em `js/motor.js` |

## 5. O que ainda não tem

- **Som.** Os momentos sonoros do roteiro (CLANG!, chiado do rádio, alarme) aparecem como
  aviso na tela. Para colocar áudio de verdade: um `<audio>` por nome de som e um `U.som()`
  que toque o arquivo em vez de só mostrar o texto.
- **Animação.** As consequências são quadros congelados, que é exatamente o que o roteiro pede
  (“congelar antes do impacto”). Para animar a queda da chave ou o desequilíbrio, o caminho é
  animar no Blender e exportar a ação junto do `.glb`.
- **Registro do resultado.** O relatório fica na tela. Para guardar por trabalhador, a saída de
  `Motor.resultado()` já vem pronta em JSON — é só enviar para onde a empresa quiser.
