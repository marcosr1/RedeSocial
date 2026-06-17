import random

# Dicionário global na memória do script para manter o estado da conversa com cada usuário
# Isso permite que a IA tenha "memória de curto prazo" enquanto o FacePit estiver aberto.
ESTADO_CONVERSA = {}

def obter_contexto_usuario(usuario):
    """Inicializa ou retorna o estado de memória do usuário."""
    if usuario not in ESTADO_CONVERSA:
        ESTADO_CONVERSA[usuario] = {
            "ultimo_topico": None,
            "historico_humor": [],
            "contador_mensagens": 0,
            "sugestao_oferecida": None
        }
    return ESTADO_CONVERSA[usuario]

def responder_como_ia(mensagem_usuario, nome_usuario="Dev"):
    """
    Motor de IA Racional e Dinâmico para o FacePit.
    Analisa o humor, mantém o contexto do assunto anterior e engaja o usuário com perguntas.
    """
    msg = mensagem_usuario.lower().strip()
    ctx = obter_contexto_usuario(nome_usuario)
    ctx["contador_mensagens"] += 1
    
    # -------------------------------------------------------------------------
    # 1. ANÁLISE DE HUMOR / SENTIMENTO (Deixa a IA mais empática e funcional)
    # -------------------------------------------------------------------------
    humor_atual = "neutro"
    if any(p in msg for p in ["porra", "caralho", "merda", "droga", "inferno", "odio", "ódio", "raiva", "difícil", "dificil"]):
        humor_atual = "frustrado"
    elif any(p in msg for p in ["kkk", "rsrs", "haha", "engraçado", "amei", "legal", "top", "perfeito", "obrigado", "valeu"]):
        humor_atual = "positivo"
    elif any(p in msg for p in ["triste", "cansado", "desistir", "desisto", "ruim"]):
        humor_atual = "desanimado"
        
    ctx["historico_humor"].append(humor_atual)

    # -------------------------------------------------------------------------
    # 2. SISTEMA DE MEMÓRIA E SEGUIMENTO DE CONTEXTO (Conversa Contínua)
    # -------------------------------------------------------------------------
    # Se o usuário respondeu sim/curtiu após uma sugestão de projeto
    if ctx["ultimo_topico"] == "ideia_projeto" and any(p in msg for p in ["sim", "quero", "manda", "como", "explica", "pode ser", "gostei"]):
        ctx["ultimo_topico"] = "detalhes_projeto"
        projeto = ctx["sugestao_oferecida"]
        
        detalhes = {
            "pywhatkit": "Para começar com o pywhatkit, use `pip install pywhatkit`. Com a função `kit.sendwhatmsg()`, você agenda o envio passando o número com +55 e o horário. Quer que eu escreva o esqueleto desse código para você?",
            "notificacoes": "Para as notificações no FacePit, você pode criar uma nova tabela ou arquivo `notificacoes.json`. Sempre que a função `curtir()` rodar, você injeta um registro lá. Quer pensar em como estruturar essa função?",
            "discord": "Para o bot do Discord, você vai precisar criar um aplicativo no Discord Developer Portal e pegar um Token. Depois, usamos o `commands.Bot`. Quer ajuda para configurar os primeiros comandos?"
        }
        return detalhes.get(projeto, "Excelente escolha! Quer que eu te ajude a dar o primeiro passo com o código ou prefere arquitetar a lógica primeiro?")

    # Se o usuário estiver frustrado lidando com um bug
    if ctx["ultimo_topico"] == "erro_codigo" and humor_atual == "frustrado":
        return "Calma! Respire fundo. O estresse bloqueia nossa mente na hora de debugar. Copie o erro exato que o console do Python exibiu e cole aqui. Vamos quebrar esse problema em partes juntos."

    # -------------------------------------------------------------------------
    # 3. FILTROS DE INTENÇÃO DINÂMICOS (Racionalização por tópicos)
    # -------------------------------------------------------------------------
    
    # CONTEXTO: Erros e Bugs
    if any(p in msg for p in ["erro", "bug", "syntaxerror", "quebrou", "falha", "consertar", "codigo", "código", "indenta", "traceback"]):
        ctx["ultimo_topico"] = "erro_codigo"
        
        if humor_atual == "frustrado":
            return f"Ei {nome_usuario}, eu percebi que você está estressado com isso. Bugs acontecem até nos sistemas da NASA! 🚀 Me mostra a linha onde o Python apontou o erro para eu te dar um norte lógico."
            
        respostas = [
            f"Analisando o cenário... {nome_usuario}, a maioria dos erros em Python são causados por 3 coisas: falta de dois pontos (`:`), variáveis escritas com letras maiúsculas/minúsculas invertidas, ou tabs misturados com espaços. Qual é a mensagem de erro que aparece?",
            "Entendido. Quando um código quebra, o segredo é isolar o problema. Se você colocar um `print()` logo antes da linha suspeita, o que ele te joga na tela? Se quiser, me mande o trecho!",
            "Opa, hora de debugar! Se for um 'NameError', a variável não foi criada. Se for 'TypeError', você está tentando misturar texto com número. O que o seu console está dizendo agora?"
        ]
        return random.choice(respostas)

    # CONTEXTO: Ideias de Projetos
    elif any(p in msg for p in ["ideia", "sugestao", "sugestão", "criar", "fazer", "projeto", "desafio", "estudar"]):
        ctx["ultimo_topico"] = "ideia_projeto"
        
        opcoes_projeto = ["pywhatkit", "notificacoes", "discord"]
        projeto_escolhido = random.choice(opcoes_projeto)
        ctx["sugestao_oferecida"] = projeto_escolhido
        
        sugestoes = {
            "pywhatkit": f"Que tal criarmos um script de automação que envia mensagens agendadas para o seu WhatsApp usando a biblioteca `pywhatkit`? É super útil para o dia a dia. Quer saber como implementar?",
            "notificacoes": f"Estava olhando a estrutura do FacePit... Seria genial se implementássemos um sistema de notificações em tempo real para quando alguém interagir com um post. O que acha dessa ideia?",
            "discord": f"Uma boa pedida seria desenvolver um Bot para o Discord que consome uma API externa de previsão do tempo ou de jogos (usando `discord.py`). Topa encarar esse desafio?"
        }
        return sugestoes[projeto_escolhido]

    # CONTEXTO: Cumprimentos / Small Talk
    elif any(p in msg for p in ["olá", "ola", "oi", "eae", "salve", "bom dia", "boa tarde", "boa noite"]):
        # Reação dinâmica baseada no número de interações
        if ctx["contador_mensagens"] > 5:
            return f"Opa, de novo! Haha. Estamos conversando bastante hoje, {nome_usuario}. No que mais posso ser útil na sua jornada de desenvolvimento?"
            
        cumprimentos = [
            f"Olá, {nome_usuario}! Sou o Bot_Python. Estou monitorando o servidor do FacePit e pronto para clarear suas ideias de programação. O que está desenvolvendo hoje?",
            f"Salve, {nome_usuario}! Tudo tranquilo por aí? Se tiver algum bug te tirando o sono ou quiser bater um papo sobre arquitetura de software, manda bala.",
            "Oi! Bot_Python operacional. Pronto para transformar café em linhas de código válidas. Qual a missão de hoje?"
        ]
        return random.choice(cumprimentos)

    # CONTEXTO: Quem é você / Identidade
    elif any(p in msg for p in ["quem é você", "quem e voce", "o que voce faz", "o que você faz", "sua função", "quem criou", "seu nome"]):
        return f"Eu sou o Bot_Python, um agente cognitivo integrado nativamente ao ecossistema FacePit. Minha lógica foi construída para atuar como um copiloto de desenvolvimento: posso estruturar algoritmos, ajudar a rastrear erros de sintaxe ou sugerir melhorias no seu código. Inclusive, já limpou o seu terminal hoje?"

    # CONTEXTO: Piadas / Entretenimento
    elif any(p in msg for p in ["piada", "engraçado", "rir", "descontrair", "conta uma", "humor"]):
        piadas = [
            "Por que os programadores preferem o modo escuro? ...Porque a luz atrai bugs! 🕶️ E convenhamos, o tema dark do FacePit tá bonito demais.",
            "O que o ponteiro do C disse para o programador Python? 'Você não tem a menor noção de onde eu estou apontando!' 🤣 (Cuidado com a alocação de memória!)",
            "Sabe qual é o animal favorito de um desenvolvedor? É a sucuri... vulgo Anaconda Python! 🐍"
        ]
        return f"{random.choice(piadas)} Quer falar sério agora ou quer outra piada para quebrar o gelo?"

    # CONTEXTO: Games / GTA
    elif any(p in msg for p in ["gta", "jogo", "game", "jogar", "los santos"]):
        return "Vi umas capturas de GTA V rodando aqui na linha do tempo do FacePit! Rodar jogos pesados e codar ao mesmo tempo exige um bom hardware, hein? Falando nisso, sabia que a lógica de inteligência dos NPCs de jogos usa máquinas de estado bem parecidas com o que estrutura nosso chat aqui?"

    # CONTEXTO: Agradecimentos
    elif any(p in msg for p in ["obrigado", "valeu", "agradecido", "obrigada", "top", "perfeito", "obg"]):
        ctx["ultimo_topico"] = None
        return f"Tamo junto, {nome_usuario}! A comunidade do FacePit cresce quando nos ajudamos. Qualquer coisa que quebrar no seu console, já sabe onde me encontrar. Bons códigos! 🚀"

    # -------------------------------------------------------------------------
    # 4. RESPOSTAS DE FALLBACK CONVERSATIVAS (Evita parecer um robô travado)
    # -------------------------------------------------------------------------
    if ctx["ultimo_topico"] == "detalhes_projeto":
        return "Eu posso te passar a sintaxe exata ou te explicar a teoria lógica de como isso funciona por trás dos panos. O que faz mais sentido para você agora?"
        
    fallbacks = [
        f"Entendi seu ponto, {nome_usuario}. Pensando de forma racional, como nós poderíamos traduzir essa sua ideia em uma função ou script automatizado?",
        "Interessante! Isso me pegou de surpresa. Pode me dar mais contexto ou explicar de outra forma? Quero entender sua linha de raciocínio.",
        "Processando dados aqui... Isso parece correlacionado a desenvolvimento ou experiência no FacePit. Quer que eu te ajude a estruturar um algoritmo baseado nisso?",
        "Entendi! Como uma inteligência artificial em constante evolução aqui na rede, eu adoro esse tipo de troca de ideias. O que te levou a pensar nisso?"
    ]
    return random.choice(fallbacks)