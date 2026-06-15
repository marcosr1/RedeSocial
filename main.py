import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from datetime import datetime
import shutil
import json
import os
import random

# Configurações Globais de Aparência (Ultra Minimalista)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PASTA_MIDIAS = "midias"
ARQ_USUARIOS = "usuarios.json"
ARQ_POSTS = "posts.json"
ARQ_MENSAGENS = "mensagens.json"

if not os.path.exists(PASTA_MIDIAS):
    os.makedirs(PASTA_MIDIAS)


# =========================================================
# MOTOR DE INTELIGÊNCIA ARTIFICIAL AVANÇADO (DINÂMICO)
# =========================================================
def responder_como_ia(mensagem_usuario):
    msg = mensagem_usuario.lower().strip()
    
    # 1. Contexto: Erros, bugs e problemas de programação
    if any(p in msg for p in ["erro", "bug", "syntaxerror", "quebrou", "falha", "consertar", "codigo", "código"]):
        respostas_erro = [
            "Bugs são apenas oportunidades de melhoria! 💻 Verifique se não há parênteses abertos, erros de indentação (tabulação) ou variáveis escritas de forma errada. Qual erro apareceu no seu console?",
            "Analisando... Geralmente erros de SyntaxError acontecem por caracteres inválidos ou falta de dois pontos ':' no final de condicionais/funções. Se quiser, me mande o pedaço do código!",
            "Eita! O código parou? Dica de ouro: use a função print() antes da linha do erro para rastrear o que suas variáveis estão guardando antes de quebrar."
        ]
        return random.choice(respostas_erro)
        
    # 2. Contexto: Ideias, o que fazer, sugestões de projetos
    elif any(p in msg for p in ["ideia", "sugestao", "sugestão", "criar", "fazer", "projeto"]):
        ideias = [
            "Que tal criar um sistema de automação que envia mensagens automáticas para o seu WhatsApp usando a biblioteca pywhatkit?",
            "Uma ótima ideia seria adicionar um sistema de 'Notificações' real aqui no FacePit para quando alguém curtir ou comentar um post!",
            "Você pode tentar desenvolver um bot para o Discord que puxa dados de APIs de jogos, usando a biblioteca discord.py. É muito divertido!"
        ]
        return f"💡 Aqui vai uma sugestão de projeto em Python: {random.choice(ideias)}"

    # 3. Contexto: Cumprimentos e saudações
    elif any(p in msg for p in ["olá", "ola", "oi", "eae", "salve", "bom dia", "boa tarde", "boa noite"]):
        cumprimentos = [
            "Olá! Eu sou o Bot_Python, sua Inteligência Artificial integrada. Como posso te ajudar com programação ou suporte hoje? 🤖",
            "Opa, tudo beleza? Pronto para escrever algumas linhas de código ou resolver algum problema?",
            "Oi! Bot_Python online e pronto para o serviço. O que vamos programar hoje?"
        ]
        return random.choice(cumprimentos)
        
    # 4. Contexto: Identidade da IA
    elif any(p in msg for p in ["quem é você", "quem e voce", "o que voce faz", "o que você faz", "sua função", "quem criou"]):
        return "Eu sou o Bot_Python! Um assistente de IA embutido diretamente no núcleo do FacePit. Minha missão é ajudar você a debater lógica de programação, resolver bugs e automatizar tarefas."
        
    # 5. Contexto: Piadas e entretenimento
    elif any(p in msg for p in ["piada", "engraçado", "rir", "descontrair", "conta uma"]):
        piadas = [
            "Por que o programador foi ao médico? Porque ele estava com falta de 'ponto e vírgula'! 🤭",
            "O que o código Python disse para o desenvolvedor? 'Não me indente que eu fico maluco!' 🐍",
            "Existem 10 tipos de pessoas no mundo: as que entendem binário e as que não entendem. De qual grupo você é?"
        ]
        return random.choice(piadas)
        
    # 6. Contexto: Jogos (Como o GTA mencionado no seu banco de dados)
    elif any(p in msg for p in ["gta", "jogo", "game", "jogar"]):
        return "GTA é clássico demais! Vi pelas postagens que a comunidade curte dar um rolê em Los Santos. Nada melhor do que jogar um pouco para esfriar a cabeça depois de debugar códigos."

    # 7. Contexto: Agradecimentos
    elif any(p in msg for p in ["obrigado", "valeu", "agradecido", "obrigada", "top", "perfeito"]):
        return "Tamo junto! Se surgir qualquer outro erro de sintaxe ou se precisar de uma ideia de algoritmo, é só me chamar aqui. 🚀"

    # 8. Respostas de fallback dinâmicas (para evitar repetição caso o tema seja genérico)
    respostas_sistema = [
        "Compreendi! Pensando em termos de código, como poderíamos transformar isso que você disse em uma função ou automação?",
        "Interessante! Me dá mais detalhes sobre isso para que eu possa te dar uma resposta ou código mais preciso.",
        "Processando dados... Essa é uma boa linha de raciocínio. Quer que eu te ajude a estruturar isso usando Python?",
        "Interessante! Como uma IA integrada no FacePit, fico feliz em trocar essa ideia com você."
    ]
    return random.choice(respostas_sistema)


# BANCO JSON
def carregar_mensagens():
    if os.path.exists(ARQ_MENSAGENS):
        with open(ARQ_MENSAGENS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_mensagens():
    with open(ARQ_MENSAGENS, "w", encoding="utf-8") as f:
        json.dump(historico_mensagens, f, indent=4)

def carregar_usuarios():
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for u in dados:
                if "amigos" not in u:
                    u["amigos"] = []
            
            # Registra a IA no banco caso não exista
            if not any(u["usuario"] == "Bot_Python" for u in dados):
                dados.append({
                    "usuario": "Bot_Python",
                    "senha": "root_system_ia_secured_password",
                    "foto_perfil": None,
                    "bio": "🤖 Inteligência Artificial oficial integrada ao FacePit. Pergunte-me sobre erros de código ou ideias!",
                    "tema": "Dark",
                    "amigos": []
                })
            return dados
    return []

def salvar_usuarios():
    with open(ARQ_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)

def carregar_posts():
    if os.path.exists(ARQ_POSTS):
        with open(ARQ_POSTS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_posts():
    with open(ARQ_POSTS, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)

usuarios = carregar_usuarios()
posts = carregar_posts()
historico_mensagens = carregar_mensagens()

usuario_logado = None

# INSTÂNCIA PRINCIPAL
class FacePit(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FacePit")
        self.geometry("1150x800")
        self.minsize(1100, 750)
        
        self.configure(fg_color=("#F4F5F6", "#0F0F10"))
        
        self.menu_expandido = False 
        self.aba_atual = "inicio"  

        self.tela_login()

    def limpar(self):
        for w in self.winfo_children():
            w.destroy()

    def alternar_menu(self):
        self.menu_expandido = not self.menu_expandido
        if self.aba_atual == "inicio":
            self.tela_feed()
        elif self.aba_atual == "perfil":
            self.tela_perfil()
        elif self.aba_atual == "amigos":
            self.tela_amigos()
        elif self.aba_atual == "mensagens":
            self.tela_mensagens()

    def alternar_tema_sistema(self):
        if self.switch_tema.get() == "on":
            ctk.set_appearance_mode("dark")
            self.switch_tema.configure(text="Modo Escuro")
        else:
            ctk.set_appearance_mode("light")
            self.switch_tema.configure(text="Modo Claro")

    # PESQUISA DE USUÁRIO
    def ejecutar_pesquisa(self, event=None):
        termo = self.campo_pesquisa.get().strip()
        if not termo:
            return
        
        usuario_encontrado = next((u for u in usuarios if u["usuario"].lower() == termo.lower()), None)
        
        if usuario_encontrado:
            self.campo_pesquisa.delete(0, "end")
            self.tela_perfil(usuario_alvo=usuario_encontrado["usuario"])
        else:
            self.campo_pesquisa.delete(0, "end")
            self.campo_pesquisa.configure(placeholder_text="Usuário não encontrado! ✕")
            self.after(2000, lambda: self.campo_pesquisa.configure(placeholder_text="Pesquisar usuário..."))

    # LOGIN
    def tela_login(self):
        self.limpar()

        frame_central = ctk.CTkFrame(self, width=420, height=500, corner_radius=16, fg_color=("#FFFFFF", "#161618"), border_width=0)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        frame_central.pack_propagate(False)

        ctk.CTkLabel(frame_central, text="FacePit", font=("Segoe UI", 32, "bold"), text_color=("#1A1A1A", "#FFFFFF")).pack(pady=(60, 5))
        ctk.CTkLabel(frame_central, text="Insira as suas credenciais para aceder.", font=("Segoe UI", 13), text_color="gray").pack(pady=(0, 40))

        self.login_usuario = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Utilizador", corner_radius=8, border_width=1, fg_color=("#F5F5F7", "#1E1E21"), border_color=("#E5E5E5", "#2D2D31"))
        self.login_usuario.pack(pady=8)

        self.login_senha = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Palavra-passe", show="*", corner_radius=8, border_width=1, fg_color=("#F5F5F7", "#1E1E21"), border_color=("#E5E5E5", "#2D2D31"))
        self.login_senha.pack(pady=8)
        
        self.lbl_erro = ctk.CTkLabel(frame_central, text="", font=("Segoe UI", 12), text_color="#FF4D4D")
        self.lbl_erro.pack(pady=5)

        btn_entrar = ctk.CTkButton(frame_central, text="Entrar", width=300, height=42, font=("Segoe UI", 13, "bold"), corner_radius=8, fg_color=("#007AFF", "#007AFF"), hover_color=("#0063CC", "#0063CC"), command=self.fazer_login)
        btn_entrar.pack(pady=(15, 10))

        btn_cadastrar = ctk.CTkButton(frame_central, text="Criar conta", width=300, height=35, fg_color="transparent", text_color=("#007AFF", "#4AA3DF"), font=("Segoe UI", 13), hover_color=("#F0F0F2", "#222225"), command=self.tela_cadastro)
        btn_cadastrar.pack()

    def fazer_login(self):
        usuario = self.login_usuario.get().strip()
        senha = self.login_senha.get().strip()

        if not usuario or not senha:
            self.lbl_erro.configure(text="Preencha todos os campos.")
            return

        if usuario == "Bot_Python":
            self.lbl_erro.configure(text="Acesso restrito ao núcleo da IA.")
            return

        usuario_encontrado = next((u for u in usuarios if u["usuario"] == usuario), None)

        if usuario_encontrado and usuario_encontrado["senha"] == senha:
            global usuario_logado
            usuario_logado = usuario
            self.lbl_erro.configure(text="") 
            self.tela_feed() 
        else:
            self.lbl_erro.configure(text="Utilizador ou palavra-passe incorretos.")
            self.login_senha.delete(0, "end")

    # CADASTRO
    def tela_cadastro(self):
        self.limpar()

        frame_central = ctk.CTkFrame(self, width=420, height=500, corner_radius=16, fg_color=("#FFFFFF", "#161618"), border_width=0)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        frame_central.pack_propagate(False)

        ctk.CTkLabel(frame_central, text="Criar Conta", font=("Segoe UI", 28, "bold"), text_color=("#1A1A1A", "#FFFFFF")).pack(pady=(60, 5))
        ctk.CTkLabel(frame_central, text="Seja bem-vindo ao FacePit.", font=("Segoe UI", 13), text_color="gray").pack(pady=(0, 40))

        self.cad_usuario = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Nome de Utilizador", corner_radius=8, border_width=1, fg_color=("#F5F5F7", "#1E1E21"), border_color=("#E5E5E5", "#2D2D31"))
        self.cad_usuario.pack(pady=8)

        self.cad_senha = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Defina uma Palavra-passe", show="*", corner_radius=8, border_width=1, fg_color=("#F5F5F7", "#1E1E21"), border_color=("#E5E5E5", "#2D2D31"))
        self.cad_senha.pack(pady=8)

        btn_salvar = ctk.CTkButton(frame_central, text="Registar", width=300, height=42, font=("Segoe UI", 13, "bold"), corner_radius=8, fg_color=("#007AFF", "#007AFF"), command=self.salvar_usuario)
        btn_salvar.pack(pady=(20, 10))

        btn_voltar = ctk.CTkButton(frame_central, text="Voltar ao Login", width=300, height=35, fg_color="transparent", text_color="gray", font=("Segoe UI", 13), hover_color=("#F0F0F2", "#222225"), command=self.tela_login)
        btn_voltar.pack()

    def salvar_usuario(self):
        usuario = self.cad_usuario.get().strip()
        senha = self.cad_senha.get().strip()

        if not usuario or not senha:
            return

        if any(u["usuario"] == usuario for u in usuarios) or usuario in ["Suporte_Hub", "Bot_Python"]:
            return

        usuarios.append({
            "usuario": usuario,
            "senha": senha,
            "foto_perfil": None,
            "bio": "",
            "tema": "Dark",
            "amigos": []
        })
        salvar_usuarios()
        self.tela_login()

    # SISTEMA DE AMIGOS
    def adicionar_amigo(self, nome_amigo):
        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
        perfil_amigo = next((u for u in usuarios if u["usuario"] == nome_amigo), None)

        if meu_perfil and perfil_amigo:
            if nome_amigo not in meu_perfil["amigos"]:
                meu_perfil["amigos"].append(nome_amigo)
            if usuario_logado not in perfil_amigo["amigos"]:
                perfil_amigo["amigos"].append(usuario_logado)
            
            salvar_usuarios()
            self.tela_amigos()

    def remover_amigo(self, nome_amigo):
        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
        perfil_amigo = next((u for u in usuarios if u["usuario"] == nome_amigo), None)

        if meu_perfil and perfil_amigo:
            if nome_amigo in meu_perfil["amigos"]:
                meu_perfil["amigos"].remove(nome_amigo)
            if usuario_logado in perfil_amigo["amigos"]:
                perfil_amigo["amigos"].remove(usuario_logado)
            
            salvar_usuarios()
            self.tela_amigos()

    def deletar_post(self, post_alvo, de_perfil):
        caminho_foto = post_alvo.get("imagem")
        if caminho_foto and os.path.exists(caminho_foto):
            try:
                os.remove(caminho_foto)
            except Exception as e:
                print(f"Erro físico: {e}")

        if post_alvo in posts:
            posts.remove(post_alvo)

        salvar_posts() 
        if de_perfil:
            self.tela_perfil()
        else:
            self.tela_feed()

    def deletar_usuario(self):
        global usuario_logado, usuarios
        usuario_alvo = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
        if usuario_alvo:
            for u in usuarios:
                if usuario_logado in u.get("amigos", []):
                    u["amigos"].remove(usuario_logado)

            usuarios.remove(usuario_alvo)
            salvar_usuarios()
            
            global posts
            posts = [p for p in posts if p["autor"] != usuario_logado]
            salvar_posts()
            
            usuario_logado = None
            self.tela_login()

    def adicionar_comentario(self, post_alvo, campo_texto, de_perfil):
        texto = campo_texto.get().strip()
        if not texto:
            return
        
        if "comentarios" not in post_alvo:
            post_alvo["comentarios"] = []
            
        post_alvo["comentarios"].append({
            "autor": usuario_logado,
            "texto": texto
        })
        
        salvar_posts()
        if de_perfil:
            self.tela_perfil()
        else:
            self.tela_feed()

    def escolher_foto_perfil(self, label_status):
        arquivo_origem = filedialog.askopenfilename(title="Foto de perfil", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
        if arquivo_origem:
            try:
                _, extensao = os.path.splitext(arquivo_origem)
                nome_novo_arquivo = f"perfil_{usuario_logado}{extensao}"
                caminho_destino = os.path.join(PASTA_MIDIAS, nome_novo_arquivo)
                shutil.copy(arquivo_origem, caminho_destino)
                self.nova_foto_perfil = caminho_destino
                label_status.configure(text="✓ Imagem importada com sucesso", text_color="#28A745")
            except Exception as e:
                label_status.configure(text="✕ Erro ao processar arquivo", text_color="#FF4D4D")

    def salvar_dados_perfil(self, campo_bio):
        nova_bio = campo_bio.get("1.0", "end").strip()
        for u in usuarios:
            if u["usuario"] == usuario_logado:
                u["bio"] = nova_bio
                if hasattr(self, 'nova_foto_perfil') and self.nova_foto_perfil:
                    u["foto_perfil"] = self.nova_foto_perfil
                break
        salvar_usuarios()
        self.tela_perfil()

    # LAYOUT BASE
    def construir_layout_base(self, aba_ativa):
        self.limpar()
        self.aba_atual = aba_ativa 

        topo = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkLabel(topo, text="FacePit", font=("Segoe UI", 20, "bold"), text_color=("#007AFF", "#FFFFFF")).pack(side="left", padx=25)
        
        self.campo_pesquisa = ctk.CTkEntry(topo, width=280, height=32, placeholder_text="Pesquisar usuário...", corner_radius=6, border_width=0, fg_color=("#F1F2F4", "#1E1E21"))
        self.campo_pesquisa.pack(side="left", padx=30)
        self.campo_pesquisa.bind("<Return>", self.ejecutar_pesquisa)

        btn_sair = ctk.CTkButton(topo, text="Sair", width=60, height=28, fg_color=("#FF3B30", "#FF453A"), hover_color=("#D62218", "#D62218"), font=("Segoe UI", 12), corner_radius=6, command=self.tela_login)
        btn_sair.pack(side="right", padx=25)
        
        ctk.CTkLabel(topo, text=usuario_logado, font=("Segoe UI", 13, "bold"), text_color="gray").pack(side="right", padx=5)

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=25, pady=20)

        largura_menu = 180 if self.menu_expandido else 55
        menu = ctk.CTkFrame(corpo, width=largura_menu, fg_color=("#FFFFFF", "#141416"), corner_radius=12, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        menu.pack(side="left", fill="y", padx=(0, 20))
        menu.pack_propagate(False)

        texto_hamburguer = "   Menu ☰" if self.menu_expandido else "☰"
        btn_toggle = ctk.CTkButton(menu, text=texto_hamburguer, height=35, width=40, font=("Segoe UI", 13), fg_color="transparent", text_color="gray", hover_color=("#F5F5F7", "#1E1E21"), command=self.alternar_menu)
        if self.menu_expandido:
            btn_toggle.pack(pady=(12, 10), anchor="w", padx=12)
        else:
            btn_toggle.pack(pady=(12, 10), anchor="center")

        botoes_menu = [
            ("  Início", "🏠", self.tela_feed, "inicio"),
            ("  Perfil", "👤", self.tela_perfil, "perfil"),
            ("  Amigos", "👥", self.tela_amigos, "amigos"),
            ("  Mensagens", "💬", self.tela_mensagens, "mensagens")
        ]

        for texto_cheio, icone, comando, chave in botoes_menu:
            ativo = (chave == aba_ativa)
            texto_exibir = f"{icone} {texto_cheio}" if self.menu_expandido else icone
            alinhamento = "w" if self.menu_expandido else "center"
            pad_x = 8 if self.menu_expandido else 4

            btn = ctk.CTkButton(
                menu, text=texto_exibir, anchor=alinhamento, height=38,
                font=("Segoe UI", 13, "bold" if ativo else "normal"),
                fg_color=("#E6F0FA", "#1A2530") if ativo else "transparent",
                text_color=("#007AFF", "#4AA3DF") if ativo else ("#333333", "#A0A0A5"),
                hover_color=("#F2F4F7", "#1E1E21"), corner_radius=8, command=comando
            )
            btn.pack(fill="x", padx=pad_x, pady=3)

        centro = ctk.CTkFrame(corpo, fg_color="transparent")
        centro.pack(side="left", fill="both", expand=True)
        return centro

    # FEED
    def tela_feed(self):
        centro = self.construir_layout_base(aba_ativa="inicio")

        caixa_post = ctk.CTkFrame(centro, fg_color=("#FFFFFF", "#141416"), corner_radius=12, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        caixa_post.pack(fill="x", pady=(0, 15))

        self.post_texto = ctk.CTkTextbox(caixa_post, height=65, corner_radius=8, border_width=1, fg_color=("#F9F9FB", "#1A1A1C"), border_color=("#EAEAEA", "#252528"), font=("Segoe UI", 13))
        self.post_texto.pack(fill="x", padx=15, pady=(15, 10))

        sub_barra = ctk.CTkFrame(caixa_post, fg_color="transparent")
        sub_barra.pack(fill="x", padx=15, pady=(0, 15))

        self.btn_foto = ctk.CTkButton(sub_barra, text="Anexar Imagem", width=120, height=30, fg_color=("#F1F2F4", "#222225"), text_color=("#333333", "#CCCCCC"), hover_color=("#E4E5E8", "#2C2C30"), font=("Segoe UI", 12), corner_radius=6, command=self.escolher_foto)
        self.btn_foto.pack(side="left")

        btn_publicar = ctk.CTkButton(sub_barra, text="Publicar", width=80, height=30, fg_color="#007AFF", font=("Segoe UI", 12, "bold"), corner_radius=6, command=self.publicar_post)
        btn_publicar.pack(side="right")

        self.feed_frame = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        self.feed_frame.pack(fill="both", expand=True)
        
        self.caminho_imagem = None
        self.renderizar_lista_posts(posts)
    
    # CHAT INTEGRADO COM A INTELIGÊNCIA ARTIFICIAL
    def disparar_mensagem(self, destinatario, campo_texto):
        texto = campo_texto.get().strip()
        if not texto:
            return

        historico_mensagens.append({
            "enviado_por": usuario_logado,
            "recebido_por": destinatario,
            "texto": texto
        })

        # Dispara resposta se o chat ativo for a IA (Bot_Python)
        if destinatario == "Bot_Python":
            resposta_ia = responder_como_ia(texto)
            historico_mensagens.append({
                "enviado_por": "Bot_Python",
                "recebido_por": usuario_logado,
                "texto": resposta_ia
            })

        elif destinatario == "Suporte_Hub":
            resposta_automatica = "Olá! Caso precise de suporte avançado para recuperação de conta ou bugs na interface, chame nossa equipe oficial via Whatsapp no número: (86) 98183-5751"
            historico_mensagens.append({
                "enviado_por": "Suporte_Hub",
                "recebido_por": usuario_logado,
                "texto": resposta_automatica
            })

        salvar_mensagens()     
        campo_texto.delete(0, 'end')  
        self.tela_mensagens(destinatario)  

    def tela_mensagens(self, contato_selecionado=None):
        centro = self.construir_layout_base(aba_ativa="mensagens")

        container_chat = ctk.CTkFrame(centro, fg_color="transparent")
        container_chat.pack(fill="both", expand=True)

        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), {"amigos": []})
        meus_amigos = meu_perfil.get("amigos", [])

        # Garante a exibição correta dos canais e amigos na aba de chat
        contatos = ["Bot_Python", "Suporte_Hub"] + meus_amigos

        if contato_selecionado is None or contato_selecionado not in contatos:
            contato_selecionado = contatos[0]

        coluna_esquerda = ctk.CTkFrame(container_chat, width=220, fg_color=("#FFFFFF", "#141416"), corner_radius=12, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        coluna_esquerda.pack(side="left", fill="y", padx=(0, 15))
        coluna_esquerda.pack_propagate(False)

        ctk.CTkLabel(coluna_esquerda, text="Conversas", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=15, pady=12)

        for contato in contatos:
            esta_ativo = (contato == contato_selecionado)
            
            if contato == "Bot_Python":
                prefixo = "🤖"
            elif contato == "Suporte_Hub":
                prefixo = "🛠️"
            else:
                prefixo = "💬"
                
            btn_contato = ctk.CTkButton(
                coluna_esquerda, text=f"{prefixo} {contato}", anchor="w", height=38,
                fg_color=("#F0F4F8", "#1A242F") if esta_ativo else "transparent",
                text_color=("#007AFF", "#4AA3DF") if esta_ativo else ("#1A1A1A", "#BBBBBC"),
                hover_color=("#F5F5F7", "#1E1E21"),
                font=("Segoe UI", 12, "bold" if esta_ativo else "normal"),
                command=lambda c=contato: self.tela_mensagens(contato_selecionado=c)
            )
            btn_contato.pack(fill="x", padx=6, pady=2)

        coluna_direita = ctk.CTkFrame(container_chat, fg_color=("#FFFFFF", "#141416"), corner_radius=12, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        coluna_direita.pack(side="left", fill="both", expand=True)

        topo_chat = ctk.CTkFrame(coluna_direita, height=45, fg_color="transparent")
        topo_chat.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(topo_chat, text=contato_selecionado, font=("Segoe UI", 13, "bold")).pack(side="left")

        area_baloes = ctk.CTkScrollableFrame(coluna_direita, fg_color="transparent")
        area_baloes.pack(fill="both", expand=True, padx=15, pady=5)

        mensagens_filtradas = []
        for msg in historico_mensagens:
            if (msg["enviado_por"] == usuario_logado and msg["recebido_por"] == contato_selecionado) or \
               (msg["enviado_por"] == contato_selecionado and msg["recebido_por"] == usuario_logado):
                mensagens_filtradas.append(msg)

        if not mensagens_filtradas:
            ctk.CTkLabel(area_baloes, text="Sem mensagens.", font=("Segoe UI", 12, "italic"), text_color="gray").pack(pady=20)
        else:
            for msg in mensagens_filtradas:
                eh_meu = (msg["enviado_por"] == usuario_logado)
                frame_balao = ctk.CTkFrame(area_baloes, fg_color="transparent")
                frame_balao.pack(fill="x", pady=3)

                balao = ctk.CTkFrame(frame_balao, fg_color=("#007AFF", "#007AFF") if eh_meu else ("#E9E9EB", "#262629"), corner_radius=12)
                balao.pack(side="right" if eh_meu else "left", padx=5)

                ctk.CTkLabel(balao, text=msg["texto"], text_color="white" if eh_meu else ("#000000", "#FFFFFF"), font=("Segoe UI", 13), wraplength=400, justify="left").pack(padx=12, pady=6)

        barra_envio = ctk.CTkFrame(coluna_direita, height=50, fg_color="transparent")
        barra_envio.pack(fill="x", padx=15, pady=(0, 15))
        barra_envio.pack_propagate(False)

        campo_msg = ctk.CTkEntry(barra_envio, placeholder_text="Mensagem...", corner_radius=8, border_width=0, fg_color=("#F1F2F4", "#1E1E21"), font=("Segoe UI", 13))
        campo_msg.pack(side="left", fill="both", expand=True, padx=(0, 10))
        campo_msg.bind("<Return>", lambda event: self.disparar_mensagem(contato_selecionado, campo_msg))

        btn_enviar = ctk.CTkButton(barra_envio, text="Enviar", width=70, fg_color="#007AFF", font=("Segoe UI", 12, "bold"), corner_radius=8, command=lambda: self.disparar_mensagem(contato_selecionado, campo_msg))
        btn_enviar.pack(side="right", fill="y")

    # AMIGOS & UTILIZADORES
    def tela_amigos(self):
        centro = self.construir_layout_base(aba_ativa="amigos")

        scroll_amigos = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        scroll_amigos.pack(fill="both", expand=True)

        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), {"amigos": []})
        meus_amigos = meu_perfil.get("amigos", [])

        ctk.CTkLabel(scroll_amigos, text="Os meus amigos", font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=5, pady=(5, 10))

        if not meus_amigos:
            ctk.CTkLabel(scroll_amigos, text="Lista vazia.", font=("Segoe UI", 12, "italic"), text_color="gray").pack(anchor="w", padx=15, pady=5)
        else:
            for amigo in meus_amigos:
                card = ctk.CTkFrame(scroll_amigos, fg_color=("#FFFFFF", "#141416"), corner_radius=8, height=50, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
                card.pack(fill="x", pady=3)
                card.pack_propagate(False)

                ctk.CTkButton(card, text=amigo, font=("Segoe UI", 13, "bold"), text_color=("#1A1A1A", "#FFFFFF"), fg_color="transparent", hover_color=("#F5F5F7", "#1E1E21"), command=lambda n=amigo: self.tela_perfil(usuario_alvo=n)).pack(side="left", padx=10)
                ctk.CTkButton(card, text="Remover", width=75, height=26, fg_color="transparent", text_color="#FF3B30", font=("Segoe UI", 12), hover_color=("#FFEBEA", "#2A1414"), corner_radius=6, command=lambda a=amigo: self.remover_amigo(a)).pack(side="right", padx=15)

        ctk.CTkFrame(scroll_amigos, height=1, fg_color=("#EAEAEA", "#1F1F22")).pack(fill="x", pady=20)

        ctk.CTkLabel(scroll_amigos, text="Lista de utilizadores", font=("Segoe UI", 14, "bold"), text_color="gray").pack(anchor="w", padx=5, pady=(0, 10))

        usuarios_restantes = [u["usuario"] for u in usuarios if u["usuario"] != usuario_logado and u["usuario"] not in meus_amigos and u["usuario"] not in ["Bot_Python", "Suporte_Hub"]]

        if not usuarios_restantes:
            ctk.CTkLabel(scroll_amigos, text="Nenhum utilizador registado pendente.", font=("Segoe UI", 12, "italic"), text_color="gray").pack(anchor="w", padx=15)
        else:
            for sug in usuarios_restantes:
                card_sug = ctk.CTkFrame(scroll_amigos, fg_color=("#FFFFFF", "#141416"), corner_radius=8, height=50, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
                card_sug.pack(fill="x", pady=3)
                card_sug.pack_propagate(False)

                ctk.CTkButton(card_sug, text=sug, font=("Segoe UI", 13), text_color=("#1A1A1A", "#FFFFFF"), fg_color="transparent", hover_color=("#F5F5F7", "#1E1E21"), command=lambda n=sug: self.tela_perfil(usuario_alvo=n)).pack(side="left", padx=10)
                ctk.CTkButton(card_sug, text="Adicionar", width=75, height=26, fg_color="#007AFF", font=("Segoe UI", 12), corner_radius=6, command=lambda s=sug: self.adicionar_amigo(s)).pack(side="right", padx=15)

    # PERFIL
    def tela_perfil(self, usuario_alvo=None):
        centro = self.construir_layout_base(aba_ativa="perfil" if usuario_alvo is None else "inicio")
        self.nova_foto_perfil = None 

        eh_meu_perfil = (usuario_alvo is None or usuario_alvo == usuario_logado)
        dono_da_pagina = usuario_logado if eh_meu_perfil else usuario_alvo

        dados_usuario = next((u for u in usuarios if u["usuario"] == dono_da_pagina), {"bio": "", "foto_perfil": None})
        posts_do_usuario = [p for p in posts if p["autor"] == dono_da_pagina]

        card_perfil = ctk.CTkFrame(centro, fg_color=("#FFFFFF", "#141416"), corner_radius=12, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        card_perfil.pack(fill="x", pady=(0, 15))

        frame_foto_nome = ctk.CTkFrame(card_perfil, fg_color="transparent")
        frame_foto_nome.pack(fill="x", padx=20, pady=(15, 5))

        if dados_usuario.get("foto_perfil") and os.path.exists(dados_usuario["foto_perfil"]):
            try:
                img_p = Image.open(dados_usuario["foto_perfil"])
                img_p.thumbnail((50, 50))
                foto_p = ctk.CTkImage(light_image=img_p, dark_image=img_p, size=(50, 50))
                lbl_foto = ctk.CTkLabel(frame_foto_nome, image=foto_p, text="")
                lbl_foto.image = foto_p
                lbl_foto.pack(side="left", padx=(0, 12))
            except:
                pass

        ctk.CTkLabel(frame_foto_nome, text=dono_da_pagina, font=("Segoe UI", 20, "bold")).pack(side="left", anchor="center")

        if not eh_meu_perfil:
            btn_voltar_feed = ctk.CTkButton(frame_foto_nome, text="Voltar ao Feed", width=100, height=28, fg_color=("#F1F2F4", "#222225"), text_color=("#1A1A1A", "#FFFFFF"), hover_color=("#E4E5E8", "#2C2C30"), font=("Segoe UI", 12), command=self.tela_feed)
            btn_voltar_feed.pack(side="right")

        bio_atual = dados_usuario.get("bio") if dados_usuario.get("bio") else "Sem biografia."
        ctk.CTkLabel(card_perfil, text=bio_atual, font=("Segoe UI", 13, "italic"), text_color="gray", justify="left").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(card_perfil, text=f"{len(posts_do_usuario)} publicações", font=("Segoe UI", 12, "bold"), text_color="#007AFF").pack(anchor="w", padx=20, pady=(0, 15))

        if eh_meu_perfil:
            frame_edicao = ctk.CTkFrame(card_perfil, fg_color=("#FAFAFC", "#19191B"), corner_radius=8)
            frame_edicao.pack(fill="x", padx=15, pady=(0, 15))

            frame_linha = ctk.CTkFrame(frame_edicao, fg_color="transparent")
            frame_linha.pack(fill="x", padx=10, pady=10)

            ctk.CTkButton(frame_linha, text="Alterar Foto", width=95, height=28, fg_color=("#F1F2F4", "#2A2A2D"), text_color=("#1A1A1A", "#FFFFFF"), hover_color=("#E4E5E8", "#333338"), font=("Segoe UI", 11), command=lambda: self.escolher_foto_perfil(lbl_status_foto)).pack(side="left")
            lbl_status_foto = ctk.CTkLabel(frame_linha, text="Padrão", font=("Segoe UI", 11), text_color="gray")
            lbl_status_foto.pack(side="left", padx=8)

            txt_bio = ctk.CTkTextbox(frame_linha, height=32, font=("Segoe UI", 12), border_width=1, fg_color=("#FFFFFF", "#1E1E21"), border_color=("#EAEAEA", "#252528"))
            txt_bio.pack(side="left", fill="x", expand=True, padx=10)
            txt_bio.insert("1.0", dados_usuario.get("bio", ""))

            ctk.CTkButton(frame_linha, text="Salvar", width=60, height=28, fg_color="#007AFF", font=("Segoe UI", 11, "bold"), command=lambda: self.salvar_dados_perfil(txt_bio)).pack(side="right")

            frame_tema = ctk.CTkFrame(frame_edicao, fg_color="transparent")
            frame_tema.pack(fill="x", padx=10, pady=(0, 10))

            modo_atual = ctk.get_appearance_mode()
            switch_var = ctk.StringVar(value="on" if modo_atual == "Dark" else "off")
            self.switch_tema = ctk.CTkSwitch(frame_tema, text="Modo Escuro", font=("Segoe UI", 11), variable=switch_var, onvalue="on", offvalue="off", command=self.alternar_tema_sistema)
            self.switch_tema.pack(side="left")

            ctk.CTkButton(frame_tema, text="Excluir Conta", height=26, fg_color="#FF3B30", font=("Segoe UI", 11), corner_radius=6, command=self.deletar_usuario).pack(side="right")

        scroll_publicacoes = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        scroll_publicacoes.pack(fill="both", expand=True)

        self.feed_frame = scroll_publicacoes
        self.renderizar_lista_posts(posts_do_usuario, de_perfil=eh_meu_perfil)

    # AUXILIARES DE FOTO E PUBLICAÇÃO
    def escolher_foto(self):
        arquivo_origem = filedialog.askopenfilename(title="Anexar imagem", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
        if arquivo_origem:
            try:
                _, extensao = os.path.splitext(arquivo_origem)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_novo_arquivo = f"post_{usuario_logado}_{timestamp}{extensao}"
                caminho_destino = os.path.join(PASTA_MIDIAS, nome_novo_arquivo)
                
                shutil.copy(arquivo_origem, caminho_destino)
                self.caminho_imagem = caminho_destino 
                self.btn_foto.configure(text="✓ Imagem Pronta", fg_color="#34C759", text_color="#FFFFFF")
            except Exception as e:
                self.caminho_imagem = None
                self.btn_foto.configure(text="Falhou", fg_color="#FF3B30", text_color="#FFFFFF")

    def publicar_post(self):
        if not hasattr(self, 'caminho_imagem'):
            self.caminho_imagem = None

        texto = self.post_texto.get("1.0", "end").strip()
        if not texto and not self.caminho_imagem:
            return

        posts.insert(0, {
            "autor": usuario_logado,
            "texto": texto,
            "imagem": self.caminho_imagem, 
            "curtidas": 0
        })

        salvar_posts()
        self.post_texto.delete("1.0", "end")
        self.caminho_imagem = None 
        self.btn_foto.configure(text="Anexar Imagem", fg_color=("#F1F2F4", "#222225"), text_color=("#333333", "#CCCCCC"))
        self.tela_feed()

    def curtir(self, post_alvo, de_perfil):
        for p in posts:
            if p == post_alvo:
                p["curtidas"] += 1
                break
        salvar_posts()
        if de_perfil:
            self.tela_perfil()
        else:
            self.tela_feed()

    def renderizar_lista_posts(self, lista_filtrada, de_perfil=False):
        for w in self.feed_frame.winfo_children():
            w.destroy()

        if not lista_filtrada:
            ctk.CTkLabel(self.feed_frame, text="Nenhuma publicação disponível.", font=("Segoe UI", 12, "italic"), text_color="gray").pack(pady=30)
            return

        for post in lista_filtrada:
            card = ctk.CTkFrame(self.feed_frame, fg_color=("#FFFFFF", "#141416"), corner_radius=12, border_width=1, border_color=("#EAEAEA", "#1F1F22"))
            card.pack(fill="x", pady=6)

            cabecalho = ctk.CTkFrame(card, fg_color="transparent")
            cabecalho.pack(fill="x", padx=15, pady=(10, 5))

            autor_dados = next((u for u in usuarios if u["usuario"] == post["autor"]), None)
            if autor_dados and autor_dados.get("foto_perfil") and os.path.exists(autor_dados["foto_perfil"]):
                try:
                    img_mini = Image.open(autor_dados["foto_perfil"])
                    img_mini.thumbnail((26, 26))
                    foto_mini = ctk.CTkImage(light_image=img_mini, dark_image=img_mini, size=(26, 26))
                    lbl_mini = ctk.CTkLabel(cabecalho, image=foto_mini, text="")
                    lbl_mini.image = foto_mini
                    lbl_mini.pack(side="left", padx=(0, 8))
                except:
                    pass

            ctk.CTkButton(
                cabecalho, text=post['autor'], font=("Segoe UI", 13, "bold"), text_color=("#007AFF", "#4AA3DF"),
                fg_color="transparent", hover_color=("#F5F5F7", "#1E1E21"), width=0, height=20,
                command=lambda a=post['autor']: self.tela_perfil(usuario_alvo=a)
            ).pack(side="left")

            if post["autor"] == usuario_logado:
                ctk.CTkButton(cabecalho, text="✕", width=20, height=20, fg_color="transparent", text_color="gray", hover_color=("#FFEBEA", "#2A1414"), command=lambda p=post: self.deletar_post(p, de_perfil)).pack(side="right")

            if post["texto"]:
                ctk.CTkLabel(card, text=post["texto"], font=("Segoe UI", 13), wraplength=700, justify="left").pack(anchor="w", padx=15, pady=5)

            if post.get("imagem") and os.path.exists(post["imagem"]):
                try:
                    img = Image.open(post["imagem"])
                    img.thumbnail((450, 350))
                    foto = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                    lbl_post_img = ctk.CTkLabel(card, image=foto, text="")
                    lbl_post_img.image = foto
                    lbl_post_img.pack(pady=8, padx=15, anchor="w")
                except:
                    pass

            rodape = ctk.CTkFrame(card, fg_color="transparent")
            rodape.pack(fill="x", padx=15, pady=5)

            ctk.CTkButton(rodape, text=f"♥  {post['curtidas']}", width=50, height=24, fg_color="transparent", text_color="#FF3B30", font=("Segoe UI", 12, "bold"), hover_color=("#FFEBEA", "#2A1414"), corner_radius=6, command=lambda p=post: self.curtir(p, de_perfil)).pack(side="left")

            frame_comentarios = ctk.CTkFrame(card, fg_color=("#F9F9FB", "#18181A"), corner_radius=6)
            frame_comentarios.pack(fill="x", padx=15, pady=(5, 10))

            if "comentarios" in post and post["comentarios"]:
                for cmt in post["comentarios"]:
                    ctk.CTkLabel(frame_comentarios, text=f"{cmt['autor']}: {cmt['texto']}", font=("Segoe UI", 12), text_color=("#333333", "#CCCCCC"), wraplength=650, justify="left").pack(anchor="w", padx=10, pady=1)

            barra_digitar_cmt = ctk.CTkFrame(frame_comentarios, fg_color="transparent")
            barra_digitar_cmt.pack(fill="x", padx=5, pady=5)

            entry_cmt = ctk.CTkEntry(barra_digitar_cmt, placeholder_text="Comentar...", height=24, fg_color=("#FFFFFF", "#1E1E21"), border_width=0, font=("Segoe UI", 12), corner_radius=4)
            entry_cmt.pack(side="left", fill="x", expand=True, padx=(0, 5))

            ctk.CTkButton(barra_digitar_cmt, text="OK", width=40, height=24, fg_color=("#F1F2F4", "#222225"), text_color=("#1A1A1A", "#FFFFFF"), font=("Segoe UI", 11, "bold"), corner_radius=4, command=lambda p=post, e=entry_cmt: self.adicionar_comentario(p, e, de_perfil)).pack(side="right")

if __name__ == "__main__":
    app = FacePit()
    app.mainloop()