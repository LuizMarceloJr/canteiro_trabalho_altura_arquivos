# -*- coding: utf-8 -*-
"""Repoe os acentos nos textos que o trabalhador le/ouve.
Nomes de objeto, camera e variavel (com _ colado) nunca sao tocados."""
import re

MAPA = {
 "acoes": "ações", "alguem": "alguém", "animacao": "animação", "ate": "até", "autorizacao": "autorização",
 "avaliacao": "avaliação", "area": "área", "caida": "caída", "cenario": "cenário", "cinturao": "cinturão",
 "cinturoes": "cinturões", "circulacao": "circulação", "comeco": "começo", "comecam": "começam",
 "comecar": "começar", "comecou": "começou", "comunicacao": "comunicação", "condicao": "condição",
 "condicoes": "condições", "conexao": "conexão", "confirmacao": "confirmação", "consequencia": "consequência",
 "consequencias": "consequências", "construcao": "construção", "criterio": "critério", "critico": "crítico",
 "criticos": "críticos", "decisao": "decisão", "decisoes": "decisões", "desequilibrio": "desequilíbrio",
 "devera": "deverá", "diferenca": "diferença", "emergencia": "emergência", "espaco": "espaço",
 "especificas": "específicas", "estao": "estão", "exposicao": "exposição", "fixacao": "fixação",
 "funcao": "função", "ha": "há", "identificacao": "identificação", "improvisacao": "improvisação",
 "informacao": "informação", "informacoes": "informações", "inspecao": "inspeção",
 "interrupcao": "interrupção", "ja": "já", "la": "lá", "lesao": "lesão", "licenca": "licença",
 "licoes": "lições", "maximo": "máximo", "medico": "médico", "metalica": "metálica",
 "movimentacao": "movimentação", "nao": "não", "necessaria": "necessária", "necessario": "necessário",
 "ninguem": "ninguém", "obstaculos": "obstáculos", "ola": "olá", "organizacao": "organização",
 "padrao": "padrão", "pe": "pé", "peca": "peça", "pedaco": "pedaço", "permaneca": "permaneça",
 "posicao": "posição", "possivel": "possível", "preocupacao": "preocupação", "producao": "produção",
 "propria": "própria", "proprio": "próprio", "protecao": "proteção", "protecoes": "proteções",
 "proxima": "próxima", "proximo": "próximo", "qualificacao": "qualificação", "radio": "rádio",
 "rapido": "rápido", "reflexao": "reflexão", "regiao": "região", "responsaveis": "responsáveis",
 "rodape": "rodapé", "sao": "são", "seguranca": "segurança", "sequencia": "sequência", "sera": "será",
 "servico": "serviço", "servicos": "serviços", "silencio": "silêncio", "simultaneos": "simultâneos",
 "situacao": "situação", "situacoes": "situações", "so": "só", "tambem": "também", "tecnica": "técnica",
 "tecnicas": "técnicas", "tecnico": "técnico", "terao": "terão", "terreo": "térreo",
 "tubulacao": "tubulação", "ultima": "última", "ultimo": "último", "utilizacao": "utilização",
 "vao": "vão", "varios": "vários", "vergalhao": "vergalhão", "vibracao": "vibração",
 "visivel": "visível", "vitima": "vítima", "voce": "você", "voces": "vocês", "atencao": "atenção",
 "aptidao": "aptidão", "permissao": "permissão", "analise": "análise", "gratis": "grátis",
 "trafego": "tráfego", "veiculo": "veículo", "veiculos": "veículos", "pratica": "prática",
 "obrigatoria": "obrigatória", "didatica": "didática", "aleatorios": "aleatórios", "basico": "básico",
 "unico": "único", "unica": "única", "minimo": "mínimo", "intervalo": "intervalo",
}

FRASES = [
 ("Esse e o ponto previsto", "Esse é o ponto previsto"),
 ("E a avaliação feita antes", "É a avaliação feita antes"),
 ("E a liberação utilizada", "É a liberação utilizada"),
 ("E um ponto previsto", "É um ponto previsto"),
 ("E rapidinho.", "É rapidinho."),
 ("E só um serviço rápido.", "É só um serviço rápido."),
 ("'E só o último.'", "'É só o último.'"),
 ("E só passar por baixo.", "É só passar por baixo."),
 ("E exatamente por isso", "É exatamente por isso"),
 ("E essa e justamente", "E essa é justamente"),
 ("E trabalhar sabendo quando", "É trabalhar sabendo quando"),
 ("Segurança não e trabalhar devagar", "Segurança não é trabalhar devagar"),
 ("E SÓ PEDIR PARA TOMAREM CUIDADO", "É SÓ PEDIR PARA TOMAREM CUIDADO"),
 ("E SÓ UMA GARUA", "É SÓ UMA GARUA"),
 ("Da para vocês dois trabalharem", "Dá para vocês dois trabalharem"),
 ("Da para terminar com ela", "Dá para terminar com ela"),
 ("e preciso se aproximar", "é preciso se aproximar"),
 ("Aproxime-se e observe", "Aproxime-se e observe"),
 ("nao e ponto previsto", "não é ponto previsto"),
 ("O caminho mais rápido nem sempre e", "O caminho mais rápido nem sempre é"),
 ("A obra mudou enquanto voce", "A obra mudou enquanto você"),
 ("Essa e uma das frases", "Essa é uma das frases"),
 ("Uma proteção deixa de cumprir sua função quando alguém passa por ela",
  "Uma proteção deixa de cumprir sua função quando alguém passa por ela"),
 ("Esse documento pertence a outro serviço", "Esse documento pertence a outro serviço"),
 ("o servico atual", "o serviço atual"),
 ("Este evento e importante", "Este evento é importante"),
 ("A autorização do seu colega nao vale", "A autorização do seu colega não vale"),
 ("nao e autorização", "não é autorização"),
 ("A falta de informação não e autorização", "A falta de informação não é autorização"),
 ("o meio de comunicação previsto nao esta", "o meio de comunicação previsto não está"),
 ("nao esta funcionando", "não está funcionando"),
 ("Ele esta suspenso", "Ele está suspenso"),
 ("ELE DISSE QUE ESTA BEM", "ELE DISSE QUE ESTÁ BEM"),
 ("Ele avisou que nao estava", "Ele avisou que não estava"),
 ("esse caminho estava assim quando voce chegou", "esse caminho estava assim quando você chegou"),
 ("Voce esta autorizado", "Você está autorizado"),
 ("ESTA DE PÉ. PODE SER USADO", "ESTÁ DE PÉ. PODE SER USADO"),
 ("Uma parte do guarda-corpo esta levemente solta", "Uma parte do guarda-corpo está levemente solta"),
 ("A identificação do ponto previsto esta suja", "A identificação do ponto previsto está suja"),
 ("O serviço esta praticamente concluído", "O serviço está praticamente concluído"),
 ("Agora voce esta precisando", "Agora você está precisando"),
 ("Agora voce esta vendo", "Agora você está vendo"),
 ("O equipamento esta sendo exigido", "O equipamento está sendo exigido"),
 ("Tudo esta dentro do previsto", "Tudo está dentro do previsto"),
 ("ESTA BOM ASSIM", "ESTÁ BOM ASSIM"),
 ("nao esta certa", "não está certa"),
 ("alguma coisa nao esta certa", "alguma coisa não está certa"),
 ("Estou meio tonto", "Estou meio tonto"),
 ("esta me ouvindo", "está me ouvindo"),
 ("Ele esta próximo de uma área", "Ele está próximo de uma área"),
 ("nao esta em condições", "não está em condições"),
 ("Uma pessoa que nao esta em condições", "Uma pessoa que não está em condições"),
 ("Cada trabalhador precisa estar liberado", "Cada trabalhador precisa estar liberado"),
]

_RX = {p: re.compile(r"(?<![\wÀ-ÿ])" + p + r"(?![\wÀ-ÿ])", re.IGNORECASE) for p in MAPA}



MAPA.update({
 "ambulancia": "ambulância", "ausencia": "ausência", "botao": "botão", "caminhao": "caminhão",
 "compativel": "compatível", "conclusao": "conclusão", "correcao": "correção", "documentacao": "documentação",
 "entao": "então", "execucao": "execução", "experiencia": "experiência", "legivel": "legível",
 "liberacao": "liberação", "missao": "missão", "poderao": "poderão", "portao": "portão",
 "preferencia": "preferência", "preparacao": "preparação", "substituicao": "substituição",
 "temporaria": "temporária", "temporario": "temporário", "verificacao": "verificação",
 "realizara": "realizará", "continuara": "continuará", "podera": "poderá", "deverao": "deverão",
 "inicio": "início", "atencao": "atenção", "aptidao": "aptidão", "sotaques": "sotaques",
 "tres": "três", "apos": "após", "alem": "além", "porem": "porém", "ideia": "ideia",
 "estatico": "estático", "automatico": "automático", "obvio": "óbvio", "serie": "série",
 "saida": "saída", "saidas": "saídas", "ai": "aí", "sai": "sai", "traz": "traz",
 "consciencia": "consciência", "urgencia": "urgência", "referencia": "referência",
 "distancia": "distância", "instancia": "instância", "tolerancia": "tolerância",
})
_RX = {p: re.compile(r"(?<![\w\u00c0-\u00ff])" + p + r"(?![\w\u00c0-\u00ff])", re.IGNORECASE) for p in MAPA}

FRASES = FRASES + [
 ("confirme se você esta liberado", "confirme se você está liberado"),
 ("A MOVIMENTAÇÃO E COMPATÍVEL", "A MOVIMENTAÇÃO É COMPATÍVEL"),
 ("Ponto de identificação não esta legível", "Ponto de identificação não está legível"),
 ("EM ALTURA ESTA PROIBIDO", "EM ALTURA ESTÁ PROIBIDO"),
 ("Esta tela pode ser reaberta", "Esta tela pode ser reaberta"),
 ("A INSPEÇÃO", "A INSPEÇÃO"),
 ("O CORTE E PEQUENO", "O CORTE É PEQUENO"),
 ("A ATIVIDADE E COMUNICAR", "A ATIVIDADE E COMUNICAR"),
 ("Mas isso não significa", "Mas isso não significa"),
 ("proximo a borda da laje", "próximo à borda da laje"),
 ("próximo a borda da laje", "próximo à borda da laje"),
 ("proximo a borda", "próximo à borda"),
 ("próximo a borda", "próximo à borda"),
 ("junto a borda", "junto à borda"),
 ("nada ficou próximo a borda", "nada ficou próximo à borda"),
 ("não pertence a sua tarefa", "não pertence à sua tarefa"),
 ("Um risco não deixa de existir porque não pertence a sua tarefa",
  "Um risco não deixa de existir porque não pertence à sua tarefa"),
 ("volta a uma condição segura", "volta a uma condição segura"),
 ("A equipe responsável verifica", "A equipe responsável verifica"),
 ("Nao improvise", "Não improvise"),
]


def _caso(orig, novo):
    if orig.isupper():
        return novo.upper()
    if orig[:1].isupper():
        return novo[:1].upper() + novo[1:]
    return novo



# "esta" é demonstrativo só antes destes substantivos; no resto é o verbo "está".
_DEMONSTRATIVO = ("atividade", "tela", "consequencia", "consequência", "situacao", "situação",
                  "cena", "obra", "versao", "versão", "semana", "altura", "area", "área",
                  "etapa", "parte", "lista", "ordem", "opcao", "opção", "pasta", "vez", "hora")
_RX_ESTA = re.compile(r"(?<![\w\u00c0-\u00ff])(esta)(\s+)([A-Za-z\u00c0-\u00ff]+)", re.IGNORECASE)


def _esta(m):
    if m.group(3).lower() in _DEMONSTRATIVO:
        return m.group(0)
    return _caso(m.group(1), "está") + m.group(2) + m.group(3)


_DEPOIS = [
    (re.compile(r"(?<![\w\u00c0-\u00ff])(n[ãa]o)(\s+)e(?![\w\u00c0-\u00ff])", re.IGNORECASE),
     lambda m: m.group(1) + m.group(2) + ("É" if m.group(1).isupper() else "é")),
    (re.compile(r"ALTURA E PROIBIDO"), lambda m: "ALTURA É PROIBIDO"),
    (re.compile(r"O que vale e a"), lambda m: "O que vale é a"),
    (re.compile(r"(?<![\w\u00c0-\u00ff])que e (um|uma|o|a)(?![\w\u00c0-\u00ff])", re.IGNORECASE),
     lambda m: "que é " + m.group(1)),
]


def texto(s):
    if not isinstance(s, str) or not s:
        return s
    for p, rx in _RX.items():
        s = rx.sub(lambda m: _caso(m.group(0), MAPA[p]), s)
    for a, b in FRASES:
        if a in s:
            s = s.replace(a, b)
    s = _RX_ESTA.sub(_esta, s)
    for rx, fn in _DEPOIS:
        s = rx.sub(fn, s)
    return s


# campos que o trabalhador le ou ouve (os demais ficam em ASCII, como os nomes de objeto)
CAMPOS = {"ia", "texto", "titulo", "linhas", "nota", "regra", "condicao", "quando", "ambiente", "descricao",
          "principio", "botoes", "regra_tecnica", "proibido_ensinar", "excecao_3p", "motivo", "etapas",
          "lista_verificacao", "sintomas", "condicao_mudou", "falas_naturais", "a_ia_nunca_deve",
          "pensamentos_a_combater", "regras_tecnicas", "principios", "nota_dev", "observacao",
          "estado_inicial", "durante_o_roteiro", "padrao", "terceira_pessoa", "maos_1p", "retorno",
          "usar_em", "evitar", "proporcao", "cabecalho", "glossario", "campos", "falas", "tela",
          "unidades", "origem", "cenario_principal"}
# NUNCA acentuar: valores, categorias, escala, definida_em, nomes de objeto/camera/variavel


def aplicar(x, chave=None):
    if isinstance(x, str):
        return texto(x) if (chave in CAMPOS) else x
    if isinstance(x, dict):
        return {k: aplicar(v, k) for k, v in x.items()}
    if isinstance(x, list):
        return [aplicar(v, chave) for v in x]
    return x
