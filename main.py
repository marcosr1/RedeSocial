import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from datetime import datetime
import shutil
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PASTA_MIDIAS = "midias"
ARQ_USUARIOS = "usuarios.json"
ARQ_POSTS = "posts.json"
ARQ_MENSAGENS = "mensagens.json"

if not os.path.exists(PASTA_MIDIAS):
    os.makedirs(PASTA_MIDIAS)

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
            return json.load(f)
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

# APP
class RedeSocial(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rede Social")
        self.geometry("1100x750")
        self.minsize(1200, 800)
        
        # Variável para controlar se o menu começa aberto (True) ou fechado (False)
        self.menu_expandido = False 
        self.aba_atual = "inicio"  # Guarda qual aba o usuário está para recarregar ao alternar o menu

        self.tela_login()

    def limpar(self):
        for w in self.winfo_children():
            w.destroy()

    def alternar_menu(self):
        # Inverte o estado do menu
        self.menu_expandido = not self.menu_expandido
        
        # Recarrega a tela em que o usuário já estava, mas agora com a nova largura de menu
        if self.aba_atual == "inicio":
            self.tela_feed()
        elif self.aba_atual == "perfil":
            self.tela_perfil()
        elif self.aba_atual == "amigos":
            self.tela_amigos()
        elif self.aba_atual == "mensagens":
            self.tela_mensagens()

    def alternar_tema_sistema(self):
            # Se o switch estiver como "on", ativa o Dark Mode, senão ativa o Light Mode
            if self.switch_tema.get() == "on":
                ctk.set_appearance_mode("dark")
                self.switch_tema.configure(text="Modo Escuro Ativo")
            else:
                ctk.set_appearance_mode("light")
                self.switch_tema.configure(text="Modo Claro Ativo")

    # LOGIN
    def tela_login(self):
        self.limpar()

        # Frame central do login
        frame_central = ctk.CTkFrame(self, width=600, height=860, corner_radius=20)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        frame_central.pack_propagate(False)

        titulo = ctk.CTkLabel(
            frame_central,
            text="Bem-vindo de volta",
            font=("Segoe UI", 26, "bold")
        )
        titulo.pack(pady=(50, 5))

        subtitulo = ctk.CTkLabel(
            frame_central,
            text="Conecte-se à sua conta",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 30))

        # Inputs salvos na instância (self)
        self.login_usuario = ctk.CTkEntry(
            frame_central,
            width=300,
            height=45,
            placeholder_text="Usuário",
            corner_radius=10
        )
        self.login_usuario.pack(pady=10)

        self.login_senha = ctk.CTkEntry(
            frame_central,
            width=300,
            height=45,
            placeholder_text="Senha",
            show="*",
            corner_radius=10
        )
        self.login_senha.pack(pady=10)
        
        # Label invisível para exibir erros de senha
        self.lbl_erro = ctk.CTkLabel(
            frame_central, 
            text="", 
            font=("Segoe UI", 12, "bold"), 
            text_color=("#FF3333", "#FF4D4D")
        )
        self.lbl_erro.pack(pady=(5, 5))

        # Botão Entrar chama a lógica de verificação (fazer_login)
        btn_entrar = ctk.CTkButton(
            frame_central,
            text="Entrar",
            width=300,
            height=45,
            font=("Segoe UI", 14, "bold"),
            corner_radius=10,
            command=self.fazer_login
        )
        btn_entrar.pack(pady=(25, 10))

        btn_cadastrar = ctk.CTkButton(
            frame_central,
            text="Criar nova conta",
            width=300,
            height=45,
            fg_color="transparent",
            hover_color=("#EAEAEA", "#2B2B2B"),
            text_color=("#1F6AA5", "#4AA3DF"),
            font=("Segoe UI", 14, "bold"),
            corner_radius=10,
            command=self.tela_cadastro
        )
        btn_cadastrar.pack()

    # =========================================================
    # LÓGICA DE VALIDAÇÃO (Apenas uma função unificada)
    # =========================================================
    def fazer_login(self):
        usuario = self.login_usuario.get().strip()
        senha = self.login_senha.get().strip()

        # Valida campos em branco
        if not usuario or not senha:
            self.lbl_erro.configure(text="❌ Preencha todos os campos!")
            return

        # Procura usuário na sua lista global 'usuarios'
        usuario_encontrado = next((u for u in usuarios if u["usuario"] == usuario), None)

        if usuario_encontrado and usuario_encontrado["senha"] == senha:
            global usuario_logado
            usuario_logado = usuario
            
            self.lbl_erro.configure(text="") # Limpa erro anterior
            self.tela_feed() # Login feito com sucesso!
        else:
            # Dados errados: exibe mensagem vermelha na tela antes de mexer no campo
            self.lbl_erro.configure(text="❌ Usuário ou senha incorretos!")
            
            # Limpa o campo de senha de forma segura usando "end" em string normal
            self.login_senha.delete(0, "end")

    def verificar_login(self):
        usuario = self.campo_usuario.get().strip()
        senha = self.campo_senha.get().strip()

        # Procura o usuário na sua lista global de usuários cadastrados
        usuario_encontrado = next((u for u in usuarios if u["usuario"] == usuario), None)

        if usuario_encontrado and usuario_encontrado["senha"] == senha:
            # --- LOGIN COM SUCESSO ---
            global usuario_logado
            usuario_logado = usuario
            
            # Limpa o aviso de erro caso estivesse lá de uma tentativa anterior
            self.lbl_erro.configure(text="") 
            
            # Redireciona para o feed
            self.tela_feed()
        else:
            # --- FALHA NO LOGIN (Usuário ou Senha incorretos) ---
            self.lbl_erro.configure(text="❌ Usuário ou senha incorretos!")
            
            # Opcional: Limpa apenas o campo de senha para o usuário tentar de novo
            self.campo_senha.delete(0, 'end')
    # CADASTRO
    def tela_cadastro(self):
        self.limpar()

        frame_central = ctk.CTkFrame(self, width=600, height=860, corner_radius=20)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        frame_central.pack_propagate(False)

        ctk.CTkLabel(
            frame_central,
            text="Criar Conta",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(50, 5))

        ctk.CTkLabel(
            frame_central,
            text="Junte-se à nossa comunidade hoje",
            font=("Segoe UI", 14),
            text_color="gray"
        ).pack(pady=(0, 30))

        self.cad_usuario = ctk.CTkEntry(
            frame_central,
            width=300,
            height=45,
            placeholder_text="Adicione o nome de Usuário",
            corner_radius=10
        )
        self.cad_usuario.pack(pady=10)

        self.cad_senha = ctk.CTkEntry(
            frame_central,
            width=300,
            height=45,
            placeholder_text="Registre sua Senha",
            show="*",
            corner_radius=10
        )
        self.cad_senha.pack(pady=10)

        btn_salvar = ctk.CTkButton(
            frame_central,
            text="Cadastrar",
            width=300,
            height=45,
            font=("Segoe UI", 14, "bold"),
            corner_radius=10,
            command=self.salvar_usuario
        )
        btn_salvar.pack(pady=(25, 10))

        btn_voltar = ctk.CTkButton(
            frame_central,
            text="Voltar para o Login",
            width=300,
            height=40,
            fg_color="transparent",
            text_color="gray",
            hover_color=("#EAEAEA", "#2B2B2B"),
            command=self.tela_login
        )
        btn_voltar.pack()

    def deletar_post(self, post_alvo, de_perfil):
        # 1. APAGAR A FOTO DO COMPUTADOR (Se ela existir)
        caminho_foto = post_alvo.get("imagem")
        
        if caminho_foto and os.path.exists(caminho_foto):
            try:
                os.remove(caminho_foto)
                print(f"🗑️ Arquivo de imagem deletado com sucesso: {caminho_foto}")
            except Exception as e:
                print(f"⚠️ Não foi possível apagar o arquivo físico da foto: {e}")

        # 2. APAGAR O POST DA LISTA GLOBAL
        if post_alvo in posts:
            posts.remove(post_alvo)

        # 3. SALVAR AS ALTERAÇÕES NO JSON E ATUALIZAR A TELA
        salvar_posts() 
         
        if de_perfil:
            self.tela_perfil()
        else:
            self.tela_feed()

    def adicionar_comentario(self, post_alvo, campo_texto, de_perfil):
        texto = campo_texto.get().strip()
        if not texto:
            return
        
        # Se o post ainda não tiver a lista de comentários (posts antigos), cria uma
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
        arquivo_origem = filedialog.askopenfilename(
            title="Escolher foto de perfil",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")]
        )
        
        if arquivo_origem:
            try:
                # Pega a extensão do arquivo original (ex: .png ou .jpg)
                _, extensao = os.path.splitext(arquivo_origem)
                
                # Cria um nome único para o arquivo usando o nome do usuário para evitar duplicados
                nome_novo_arquivo = f"perfil_{usuario_logado}{extensao}"
                caminho_destino = os.path.join(PASTA_MIDIAS, nome_novo_arquivo)
                
                # Copia a imagem fisicamente do computador para a pasta do seu projeto
                shutil.copy(arquivo_origem, caminho_destino)
                
                # Guarda o caminho interno e relativo na variável temporária
                self.nova_foto_perfil = caminho_destino
                label_status.configure(text="✅ Foto salva no projeto!", text_color="#28A745")
            except Exception as e:
                label_status.configure(text="❌ Erro ao copiar arquivo", text_color="#FF4D4D")
                print(f"Erro: {e}")

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

    def salvar_usuario(self):
        usuario = self.cad_usuario.get()
        senha = self.cad_senha.get()

        if not usuario or not senha:
            return

        usuarios.append({
            "usuario": usuario,
            "senha": senha,
            "foto_perfil": None,
            "bio": "",
            "tema": "Dark"  
        })
        salvar_usuarios()
        self.tela_login()

    def fazer_login(self):
        global usuario_logado
        usuario = self.login_usuario.get()
        senha = self.login_senha.get()

        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                usuario_logado = usuario
                self.tela_feed()
                return

    # LAYOUT BASE (TOPO E MENU)
    def construir_layout_base(self, aba_ativa):
        """Método auxiliar para criar a base das telas com menu retrátil"""
        self.limpar()
        self.aba_atual = aba_ativa # Atualiza a aba onde o usuário está navegando

        # TOPO BARRA DE NAVEGAÇÃO
        topo = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=("#FFFFFF", "#1E1E1E"), border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkLabel(
            topo,
            text="🌐 ConnectHub",
            font=("Segoe UI", 24, "bold"),
            text_color=("#1F6AA5", "#4AA3DF")
        ).pack(side="left", padx=30)

        # Barra de Pesquisa
        ctk.CTkEntry(
            topo, width=350, height=38,
            placeholder_text="🔍 Pesquisar na rede...",
            corner_radius=20, border_width=1
        ).pack(side="left", padx=50)

        btn_sair = ctk.CTkButton(
            topo, text="Sair", width=70, height=35,
            fg_color=("#FF4D4D", "#CC3333"), hover_color=("#FF3333", "#992222"),
            font=("Segoe UI", 12, "bold"), corner_radius=10,
            command=self.tela_login
        )
        btn_sair.pack(side="right", padx=30)

        ctk.CTkLabel(topo, text=f"Olá, {usuario_logado} ✨", font=("Segoe UI", 15, "bold")).pack(side="right", padx=10)

        # CORPO PRINCIPAL
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=20, pady=20)

        # MENU LATERAL DINÂMICO (Muda de tamanho baseado no estado)
        largura_menu = 220 if self.menu_expandido else 60
        menu = ctk.CTkFrame(corpo, width=largura_menu, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=15)
        menu.pack(side="left", fill="y", padx=(0, 15))
        menu.pack_propagate(False)

        # BOTÃO HAMBÚRGUER / ALTERNAR MENU
        texto_hamburguer = " menu ☰" if self.menu_expandido else "☰"
        btn_toggle = ctk.CTkButton(
            menu, text=texto_hamburguer, height=35, width=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="transparent", text_color="gray",
            hover_color=("#F0F2F5", "#2A2A2A"),
            command=self.alternar_menu
        )
        if self.menu_expandido:
            btn_toggle.pack(pady=(15, 5), anchor="w", padx=15)
        else:
            btn_toggle.pack(pady=(15, 5), anchor="center")

        # Dados dos botões: (Texto Expandido, Texto Recolhido, Comando, Chave)
        botoes_menu = [
            ("🏠  Início", "🏠", self.tela_feed, "inicio"),
            ("👤  Perfil", "👤", self.tela_perfil, "perfil"),
            ("👥  Amigos", "👥", self.tela_amigos, "amigos"),
            ("💬  Mensagens", "💬", self.tela_mensagens, "mensagens")
        ]

        for texto_cheio, icone, comando, chave in botoes_menu:
            ativo = (chave == aba_ativa)
            
            # Define o texto que vai aparecer baseado no estado atual do menu
            texto_exibir = texto_cheio if self.menu_expandido else icone
            alinhamento = "w" if self.menu_expandido else "center"
            pad_x = 10 if self.menu_expandido else 5

            btn = ctk.CTkButton(
                menu, 
                text=texto_exibir, 
                anchor=alinhamento, 
                height=40,
                font=("Segoe UI", 14, "bold" if ativo else "normal"),
                fg_color=("#E5F1FA", "#1F3547") if ativo else "transparent",
                text_color=("#1F6AA5", "#4AA3DF") if ativo else ("#000000", "#FFFFFF"),
                hover_color=("#D0E6F7", "#28445C"),
                corner_radius=10,
                command=comando if comando else lambda: None
            )
            btn.pack(fill="x", padx=pad_x, pady=4)

        # ÁREA CENTRAL (Ganha mais espaço se o menu estiver em 60px)
        centro = ctk.CTkFrame(corpo, fg_color="transparent")
        centro.pack(side="left", fill="both", expand=True)
        return centro

    # FEED PRINCIPAL
    def tela_feed(self):
        centro = self.construir_layout_base(aba_ativa="inicio")

        # CAIXA DE CRIAÇÃO DE POST
        caixa_post = ctk.CTkFrame(centro, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=15, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
        caixa_post.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            caixa_post,
            text="No que você está pensando?",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.post_texto = ctk.CTkTextbox(
            caixa_post, height=80, corner_radius=10, border_width=1,
            border_color=("#D0D0D0", "#333333"), font=("Segoe UI", 13)
        )
        self.post_texto.pack(fill="x", padx=20, pady=5)

        sub_barra = ctk.CTkFrame(caixa_post, fg_color="transparent")
        sub_barra.pack(fill="x", padx=20, pady=(5, 15))

        self.btn_foto = ctk.CTkButton(
            sub_barra, text="Adicionar Foto", width=140, height=35,
            fg_color=("#F0F2F5", "#2A2A2A"), text_color=("#000000", "#FFFFFF"),
            hover_color=("#E4E6EB", "#3A3A3A"), font=("Segoe UI", 12, "bold"),
            corner_radius=8, 
            command=self.escolher_foto
        )
        self.btn_foto.pack(side="left")

        btn_publicar = ctk.CTkButton(
            sub_barra, text="Publicar", width=100, height=35,
            font=("Segoe UI", 12, "bold"), corner_radius=8, command=self.publicar_post
        )
        btn_publicar.pack(side="right")

        # SCROLL DOS POSTS (Geral)
        self.feed_frame = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        self.feed_frame.pack(fill="both", expand=True)
        
        self.caminho_imagem = None
        self.renderizar_lista_posts(posts)
    
    # TELA DE MENSAGENS 
    def disparar_mensagem(self, destinatario, campo_texto):
        texto = campo_texto.get().strip()
        if not texto:
            return

        # Guarda a mensagem com quem enviou (autor), quem recebe e o conteúdo
        historico_mensagens.append({
            "enviado_por": usuario_logado,
            "recebido_por": destinatario,
            "texto": texto
        })

        salvar_mensagens()     # Grava no arquivo JSON
        campo_texto.delete(0, 'end')  # Limpa o campo de digitação
        self.tela_mensagens(destinatario)  # Atualiza a tela para mostrar a nova mensagem

    def tela_mensagens(self, contato_selecionado=None):
        centro = self.construir_layout_base(aba_ativa="mensagens")

        container_chat = ctk.CTkFrame(centro, fg_color="transparent")
        container_chat.pack(fill="both", expand=True)

        contatos = [u["usuario"] for u in usuarios if u["usuario"] != usuario_logado]
        if not contatos:
            contatos = ["Suporte_Hub", "Bot_Python"]

        if contato_selecionado is None:
            contato_selecionado = contatos[0]

        # COLUNA ESQUERDA: LISTA DE CONVERSAS
        coluna_esquerda = ctk.CTkFrame(container_chat, width=250, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=12, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
        coluna_esquerda.pack(side="left", fill="y", padx=(0, 10))
        coluna_esquerda.pack_propagate(False)

        ctk.CTkLabel(coluna_esquerda, text="Conversas", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=15, pady=15)

        for contato in contatos:
            esta_ativo = (contato == contato_selecionado)
            btn_contato = ctk.CTkButton(
                coluna_esquerda,
                text=f"💬  {contato}",
                anchor="w", height=45,
                fg_color=("#E5F1FA", "#1F3547") if esta_ativo else "transparent",
                text_color=("#1F6AA5", "#4AA3DF") if esta_ativo else ("#000000", "#FFFFFF"),
                hover_color=("#F0F2F5", "#2A2A2A"),
                font=("Segoe UI", 13, "bold" if esta_ativo else "normal"),
                command=lambda c=contato: self.tela_mensagens(contato_selecionado=c)
            )
            btn_contato.pack(fill="x", padx=5, pady=2)

        # COLUNA DIREITA: JANELA DO CHAT ATIVO
        coluna_direita = ctk.CTkFrame(container_chat, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=12, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
        coluna_direita.pack(side="left", fill="both", expand=True)

        topo_chat = ctk.CTkFrame(coluna_direita, height=50, fg_color="transparent")
        topo_chat.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(topo_chat, text=f"🟢 {contato_selecionado}", font=("Segoe UI", 14, "bold")).pack(side="left")
        ctk.CTkFrame(coluna_direita, height=1, fg_color=("#E0E0E0", "#2D2D2D")).pack(fill="x", padx=15)

        # Área de Balões com Rolagem
        area_baloes = ctk.CTkScrollableFrame(coluna_direita, fg_color="transparent")
        area_baloes.pack(fill="both", expand=True, padx=15, pady=10)

        # FILTRAR MENSAGENS REAIS ENTRE OS DOIS USUÁRIOS
        mensagens_filtradas = []
        for msg in historico_mensagens:
            # Verifica se a mensagem pertence a essa conversa (enviada por você para ele, ou dele para você)
            if (msg["enviado_por"] == usuario_logado and msg["recebido_por"] == contato_selecionado) or \
               (msg["enviado_por"] == contato_selecionado and msg["recebido_por"] == usuario_logado):
                mensagens_filtradas.append(msg)

        if not mensagens_filtradas:
            ctk.CTkLabel(area_baloes, text="Nenhuma mensagem por aqui ainda. Diga oi! 👋", font=("Segoe UI", 13, "italic"), text_color="gray").pack(pady=30)
        else:
            for msg in mensagens_filtradas:
                eh_meu = (msg["enviado_por"] == usuario_logado)
                
                frame_balao = ctk.CTkFrame(area_baloes, fg_color="transparent")
                frame_balao.pack(fill="x", pady=4)

                balao = ctk.CTkFrame(
                    frame_balao,
                    fg_color=("#1F6AA5", "#4AA3DF") if eh_meu else ("#F0F2F5", "#2A2A2A"),
                    corner_radius=10
                )
                balao.pack(side="right" if eh_meu else "left", padx=5)

                ctk.CTkLabel(
                    balao, 
                    text=msg["texto"], 
                    text_color="white" if eh_meu else ("#000000", "#FFFFFF"),
                    font=("Segoe UI", 13),
                    wraplength=350, justify="left"
                ).pack(padx=12, pady=8)

        # Barra de envio inferior
        barra_envio = ctk.CTkFrame(coluna_direita, height=60, fg_color="transparent")
        barra_envio.pack(fill="x", padx=15, pady=(0, 15))
        barra_envio.pack_propagate(False)

        campo_msg = ctk.CTkEntry(barra_envio, placeholder_text=f"Enviar mensagem para {contato_selecionado}...", corner_radius=10, font=("Segoe UI", 13))
        campo_msg.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Vincula a tecla 'Enter' do teclado para também enviar a mensagem de forma prática
        campo_msg.bind("<Return>", lambda event: self.disparar_mensagem(contato_selecionado, campo_msg))

        btn_enviar = ctk.CTkButton(
            barra_envio, 
            text="Enviar 🚀", 
            width=90, font=("Segoe UI", 13, "bold"), corner_radius=10,
            command=lambda: self.disparar_mensagem(contato_selecionado, campo_msg)
        )
        btn_enviar.pack(side="right", fill="y")

    # TELA DE AMIGOS
    def tela_amigos(self):
        # Constrói o topo e o menu lateral deixando a aba amigos ativa
        centro = self.construir_layout_base(aba_ativa="amigos")

        # Container principal com rolagem para os amigos
        scroll_amigos = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        scroll_amigos.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # SEÇÃO 1: SEUS AMIGOS
        # ---------------------------------------------------------
        ctk.CTkLabel(
            scroll_amigos,
            text="Seus Amigos",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 15))

        # Lista simulada de amigos (com base nos usuários cadastrados tirando você mesmo)
        amigos_ficticios = [u["usuario"] for u in usuarios if u["usuario"] != usuario_logado]

        if not amigos_ficticios:
            ctk.CTkLabel(
                scroll_amigos,
                text="Você ainda não adicionou nenhum amigo. 👥",
                font=("Segoe UI", 14, "italic"),
                text_color="gray"
            ).pack(anchor="w", padx=20, pady=10)
        else:
            for amigo in amigos_ficticios:
                card_amigo = ctk.CTkFrame(scroll_amigos, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=10, height=60, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
                card_amigo.pack(fill="x", pady=5, padx=5)
                card_amigo.pack_propagate(False)

                # Nome do amigo
                btn_perfil_amigo = ctk.CTkButton(
                    card_amigo,
                    text=f"👤 {amigo}",
                    font=("Segoe UI", 14, "bold"),
                    text_color=("#000000", "#FFFFFF"),
                    fg_color="transparent",
                    hover_color=("#F0F2F5", "#2A2A2A"),
                    height=35,
                    command=lambda nome_amigo=amigo: self.tela_perfil(usuario_alvo=nome_amigo)
                )
                btn_perfil_amigo.pack(side="left", padx=15)

                # Botão para Remover/Mensagem
                ctk.CTkButton(
                    card_amigo,
                    text="Remover",
                    width=90,
                    height=30,
                    fg_color="transparent",
                    text_color=("#FF4D4D", "#FF4D4D"),
                    hover_color=("#FEE2E2", "#2D1F1F"),
                    corner_radius=8,
                    command=lambda a=amigo: print(f"Remover {a}")
                ).pack(side="right", padx=20)

        # Separador de seções
        ctk.CTkFrame(scroll_amigos, height=2, fg_color=("#E0E0E0", "#2D2D2D")).pack(fill="x", padx=10, pady=25)

        # ---------------------------------------------------------
        # SEÇÃO 2: SUGESTÕES DE AMIZADE
        # ---------------------------------------------------------
        ctk.CTkLabel(
            scroll_amigos,
            text="Pessoas que você talvez conheça",
            font=("Segoe UI", 16, "bold"),
            text_color="gray"
        ).pack(anchor="w", padx=10, pady=(0, 15))

        # Sugestões estáticas para ilustrar a tela
        sugestoes = ["Alice_Silva", "Carlos_Edu", "Dev_Python"]

        for sug in sugestoes:
            card_sug = ctk.CTkFrame(scroll_amigos, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=10, height=60, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
            card_sug.pack(fill="x", pady=5, padx=5)
            card_sug.pack_propagate(False)

            ctk.CTkLabel(
                card_sug,
                text=f"✨ {sug}",
                font=("Segoe UI", 14)
            ).pack(side="left", padx=20)

            ctk.CTkButton(
                card_sug,
                text="Adicionar",
                width=90,
                height=30,
                corner_radius=8,
                command=lambda s=sug: print(f"Adicionar {s}")
            ).pack(side="right", padx=20)

    # TELA DE PERFIL
    def tela_perfil(self, usuario_alvo=None):
        # Constrói o layout base (topo e menu)
        centro = self.construir_layout_base(aba_ativa="perfil" if usuario_alvo is None else "inicio")
        self.nova_foto_perfil = None 

        # Se nenhum usuário foi passado, significa que você está abrindo o SEU próprio perfil
        eh_meu_perfil = (usuario_alvo is None or usuario_alvo == usuario_logado)
        
        # Define quem é o dono da página que estamos visitando
        dono_da_pagina = usuario_logado if eh_meu_perfil else usuario_alvo

        # Encontra os dados do dono da página no banco de dados
        dados_usuario = next((u for u in usuarios if u["usuario"] == dono_da_pagina), {"bio": "Este usuário não adicionou uma biografia.", "foto_perfil": None})
        posts_do_usuario = [p for p in posts if p["autor"] == dono_da_pagina]

        # =========================================================
        # CARD PRINCIPAL DO PERFIL (Fixo no topo do 'centro')
        # =========================================================
        card_perfil = ctk.CTkFrame(centro, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=15, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
        card_perfil.pack(fill="x", pady=(5, 10), padx=5)

        # Cabeçalho: Foto + Nome
        frame_foto_nome = ctk.CTkFrame(card_perfil, fg_color="transparent")
        frame_foto_nome.pack(fill="x", padx=25, pady=(15, 5))

        if dados_usuario.get("foto_perfil") and os.path.exists(dados_usuario["foto_perfil"]):
            try:
                img_p = Image.open(dados_usuario["foto_perfil"])
                img_p.thumbnail((60, 60))
                foto_p = ctk.CTkImage(light_image=img_p, dark_image=img_p, size=(60, 60))
                lbl_foto = ctk.CTkLabel(frame_foto_nome, image=foto_p, text="")
                lbl_foto.image = foto_p
                lbl_foto.pack(side="left", padx=(0, 15))
            except:
                pass

        ctk.CTkLabel(frame_foto_nome, text=f"👤 {dono_da_pagina}", font=("Segoe UI", 22, "bold")).pack(side="left", anchor="center")

        # Botão de voltar ao feed para perfis de terceiros
        if not eh_meu_perfil:
            btn_voltar_feed = ctk.CTkButton(
                frame_foto_nome, text="⬅️ Voltar ao Feed", width=120, height=30,
                fg_color=("#E4E6EB", "#2A2A2A"), text_color=("#000000", "#FFFFFF"),
                hover_color=("#D8DADF", "#3A3A3A"), font=("Segoe UI", 12, "bold"),
                command=self.tela_feed
            )
            btn_voltar_feed.pack(side="right", padx=10)

        # Biografia exibida
        bio_atual = dados_usuario.get("bio") if dados_usuario.get("bio") else "Nenhuma biografia adicionada ainda."
        ctk.CTkLabel(card_perfil, text=bio_atual, font=("Segoe UI", 13, "italic"), text_color="gray", justify="left", wraplength=700).pack(anchor="w", padx=25, pady=2)
        
        # Contador de publicações
        ctk.CTkLabel(card_perfil, text=f"📊 {len(posts_do_usuario)} publicações", font=("Segoe UI", 12, "bold"), text_color=("#1F6AA5", "#4AA3DF")).pack(anchor="w", padx=25, pady=(0, 10))

        # =========================================================
        # PAINEL DE EDIÇÃO FIXO (SÓ APARECE NO SEU PERFIL)
        # =========================================================
        if eh_meu_perfil:
            frame_edicao = ctk.CTkFrame(card_perfil, fg_color=("#F9F9F9", "#1A1A1A"), corner_radius=10)
            frame_edicao.pack(fill="x", padx=20, pady=(0, 15))

            frame_inputs = ctk.CTkFrame(frame_edicao, fg_color="transparent")
            frame_inputs.pack(fill="x", padx=15, pady=10)

            # Foto e Bio na mesma linha para economizar espaço vertical fixo
            frame_linha_inputs = ctk.CTkFrame(frame_inputs, fg_color="transparent")
            frame_linha_inputs.pack(fill="x", pady=5)

            btn_mudar_foto = ctk.CTkButton(
                frame_linha_inputs, text="🖼️ Escolher Foto", width=120, height=30, 
                fg_color=("#E4E6EB", "#2A2A2A"), text_color=("#000000", "#FFFFFF"), 
                hover_color=("#D8DADF", "#3A3A3A"), font=("Segoe UI", 11, "bold"), 
                command=lambda: self.escolher_foto_perfil(lbl_status_foto)
            )
            btn_mudar_foto.pack(side="left", anchor="center")

            lbl_status_foto = ctk.CTkLabel(frame_linha_inputs, text="Nenhuma foto alterada", font=("Segoe UI", 11), text_color="gray")
            lbl_status_foto.pack(side="left", padx=10, anchor="center")

            txt_bio = ctk.CTkTextbox(frame_linha_inputs, height=35, font=("Segoe UI", 12))
            txt_bio.pack(side="left", fill="x", expand=True, padx=15)
            txt_bio.insert("1.0", dados_usuario.get("bio", ""))

            btn_salvar_dados = ctk.CTkButton(frame_linha_inputs, text="Salvar", width=70, height=30, font=("Segoe UI", 11, "bold"), command=lambda: self.salvar_dados_perfil(txt_bio))
            btn_salvar_dados.pack(side="right", anchor="center")

            # Separador sutil interno
            ctk.CTkFrame(frame_edicao, height=1, fg_color=("#E0E0E0", "#2D2D2D")).pack(fill="x", padx=15, pady=2)

            # Interruptor de Tema
            frame_tema = ctk.CTkFrame(frame_edicao, fg_color="transparent")
            frame_tema.pack(fill="x", padx=15, pady=5)

            modo_atual = ctk.get_appearance_mode()
            switch_var = ctk.StringVar(value="on" if modo_atual == "Dark" else "off")

            self.switch_tema = ctk.CTkSwitch(frame_tema, text="Modo Escuro Ativo", font=("Segoe UI", 12), variable=switch_var, onvalue="on", offvalue="off", command=self.alternar_tema_sistema)
            self.switch_tema.pack(side="left", padx=5)

        # =========================================================
        # SEÇÃO DE PUBLICAÇÕES (Apenas esta área possui scroll)
        # =========================================================
        titulo_secao = "Minhas Publicações" if eh_meu_perfil else f"Publicações de {dono_da_pagina}"
        ctk.CTkLabel(centro, text=titulo_secao, font=("Segoe UI", 15, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=(5, 5))

        # Criamos uma caixa com rolagem independente ocupando o resto do espaço inferior
        scroll_publicacoes = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        scroll_publicacoes.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Vincula o motor de posts a esta caixa isolada de rolagem
        self.feed_frame = scroll_publicacoes
        
        # Desenha as publicações dentro do scroll inferior
        self.renderizar_lista_posts(posts_do_usuario, de_perfil=eh_meu_perfil)

    # LOGICA E RENDERIZAÇÃO DOS POSTS
    def escolher_foto(self):
        arquivo_origem = filedialog.askopenfilename(
            title="Anexar imagem ao post",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")]
        )
        
        if arquivo_origem:
            try:
                _, extensao = os.path.splitext(arquivo_origem)
                
                # Pega o timestamp atual
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                try:
                    autor = usuario_logado
                except NameError:
                    autor = self.usuario_logado

                try:
                    pasta = PASTA_MIDIAS
                except NameError:
                    pasta = "midias"

                nome_novo_arquivo = f"post_{autor}_{timestamp}{extensao}"
                caminho_destino = os.path.join(pasta, nome_novo_arquivo)
                
                if not os.path.exists(pasta):
                    os.makedirs(pasta)
                
                shutil.copy(arquivo_origem, caminho_destino)
                
                self.caminho_imagem = caminho_destino 
                
                self.btn_foto.configure(
                    text="Foto Anexada!", 
                    fg_color=("#1F6AA5", "#4AA3DF"), 
                    text_color="#FFFFFF"
                )

            except Exception as e:
                print(f"Erro ao anexar foto: {e}")
                self.caminho_imagem = None
                self.btn_foto.configure(
                    text="Falha ao Anexar", 
                    fg_color=("#FF4D4D", "#CC3333"), 
                    text_color="#FFFFFF"
                )

    def publicar_post(self):
        # Garante que a variável exista na classe mesmo se o usuário não escolher foto
        if not hasattr(self, 'caminho_imagem'):
            self.caminho_imagem = None

        texto = self.post_texto.get("1.0", "end").strip()
        if not texto and not self.caminho_imagem:
            return

        posts.insert(0, {
            "autor": usuario_logado,
            "texto": texto,
            "imagem": self.caminho_imagem, # Agora vai ler o caminho correto!
            "curtidas": 0
        })

        salvar_posts()
        self.post_texto.delete("1.0", "end")
        self.caminho_imagem = None # Reseta corretamente para o próximo post
        
        # Opcional: Se você estiver usando o label_status_post para avisar que a foto foi anexada,
        # lembre-se de resetar o texto dele aqui também se quiser limpar a tela por completo!
        self.btn_foto.configure(text="📷 Adicionar Foto", fg_color=("#F0F2F5", "#2A2A2A"), text_color=("#000000", "#FFFFFF"))
        self.tela_feed()

    def curtir(self, post_alvo, de_perfil):
        # Encontra o post real na lista global 'posts' para atualizar as curtidas
        for p in posts:
            if p == post_alvo:
                p["curtidas"] += 1
                break
        
        salvar_posts()
        # Atualiza a tela atual em que o usuário está navegando
        if de_perfil:
            self.tela_perfil()
        else:
            self.tela_feed()

    def renderizar_lista_posts(self, lista_filtrada, de_perfil=False):
        """Renderiza dinamicamente posts com foto de autor, exclusão e comentários"""
        for w in self.feed_frame.winfo_children():
            w.destroy()

        if not lista_filtrada:
            ctk.CTkLabel(self.feed_frame, text="Nenhuma publicação encontrada aqui. 👀", font=("Segoe UI", 14, "italic"), text_color="gray").pack(pady=40)
            return

        for post in lista_filtrada:
            card = ctk.CTkFrame(self.feed_frame, fg_color=("#FFFFFF", "#1E1E1E"), corner_radius=12, border_width=1, border_color=("#E0E0E0", "#2D2D2D"))
            card.pack(fill="x", pady=8, padx=2)

            # CABEÇALHO DO POST (Foto + Autor + Botão Deletar)
            cabecalho = ctk.CTkFrame(card, fg_color="transparent")
            cabecalho.pack(fill="x", padx=15, pady=(12, 5))

            # Procura se o autor do post tem foto de perfil cadastrada
            autor_dados = next((u for u in usuarios if u["usuario"] == post["autor"]), None)
            if autor_dados and autor_dados.get("foto_perfil") and os.path.exists(autor_dados["foto_perfil"]):
                try:
                    img_mini = Image.open(autor_dados["foto_perfil"])
                    img_mini.thumbnail((32, 32))
                    foto_mini = ctk.CTkImage(light_image=img_mini, dark_image=img_mini, size=(32, 32))
                    lbl_mini = ctk.CTkLabel(cabecalho, image=foto_mini, text="")
                    lbl_mini.image = foto_mini
                    lbl_mini.pack(side="left", padx=(0, 10))
                except:
                    pass

            btn_link_autor = ctk.CTkButton(
                cabecalho,
                text=f"{post['autor']}",
                font=("Segoe UI", 15, "bold"),
                text_color=("#1F6AA5", "#4AA3DF"),
                fg_color="transparent",
                hover_color=("#F0F2F5", "#2A2A2A"),
                width=0, # Ajusta ao tamanho do texto
                height=25,
                # CHAMA A TELA DE PERFIL PASSANDO O AUTOR DESTE POST ESPECÍFICO!
                command=lambda autor_post=post['autor']: self.tela_perfil(usuario_alvo=autor_post)
            )
            btn_link_autor.pack(side="left", anchor="center", padx=(0, 5))

            # BOTÃO DELETAR (Apenas se o post for seu!)
            if post["autor"] == usuario_logado:
                btn_deletar = ctk.CTkButton(
                    cabecalho, text="🗑️", width=30, height=30,
                    fg_color="transparent", text_color="#FF4D4D",
                    hover_color=("#FEE2E2", "#2D1F1F"), font=("Segoe UI", 14),
                    command=lambda p=post: self.deletar_post(p, de_perfil)
                )
                btn_deletar.pack(side="right")

            # CONTEÚDO DE TEXTO
            if post["texto"]:
                ctk.CTkLabel(card, text=post["texto"], font=("Segoe UI", 14), wraplength=650, justify="left").pack(anchor="w", padx=20, pady=(5, 10))

            # IMAGEM ANEXADA
            if post.get("imagem") and os.path.exists(post["imagem"]):
                try:
                    img = Image.open(post["imagem"])
                    img.thumbnail((500, 400))
                    foto = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                    label_img = ctk.CTkLabel(card, image=foto, text="")
                    label_img.image = foto
                    label_img.pack(pady=10, padx=20, anchor="w")
                except:
                    pass

            # SEÇÃO DE INTERAÇÃO (Curtidas)
            rodape = ctk.CTkFrame(card, fg_color="transparent")
            rodape.pack(fill="x", padx=20, pady=(5, 5))

            btn_like = ctk.CTkButton(
                rodape, text=f"❤️  {post['curtidas']}", width=80, height=32, 
                fg_color="transparent", text_color=("#E02424", "#F87171"), 
                hover_color=("#FEE2E2", "#2D1F1F"), font=("Segoe UI", 13, "bold"), corner_radius=8,
                command=lambda p=post: self.curtir(p, de_perfil)
            )
            btn_like.pack(side="left")

            # SEÇÃO DE COMENTÁRIOS (Nova!)
            frame_comentarios = ctk.CTkFrame(card, fg_color=("#F6F6F6", "#181818"), corner_radius=8)
            frame_comentarios.pack(fill="x", padx=15, pady=(5, 12))

            # Exibir Comentários Existentes
            if "comentarios" in post and post["comentarios"]:
                for cmt in post["comentarios"]:
                    lbl_cmt = ctk.CTkLabel(
                        frame_comentarios, 
                        text=f"💬 {cmt['autor']}: {cmt['texto']}", 
                        font=("Segoe UI", 12),
                        wraplength=600, justify="left"
                    )
                    lbl_cmt.pack(anchor="w", padx=15, pady=2)

            # Barra para digitar novo comentário
            barra_digitar_cmt = ctk.CTkFrame(frame_comentarios, fg_color="transparent")
            barra_digitar_cmt.pack(fill="x", padx=10, pady=8)

            entry_cmt = ctk.CTkEntry(barra_digitar_cmt, placeholder_text="Escreva um comentário...", height=28, font=("Segoe UI", 12), corner_radius=6)
            entry_cmt.pack(side="left", fill="x", expand=True, padx=(0, 8))

            btn_enviar_cmt = ctk.CTkButton(
                barra_digitar_cmt, text="Comentar", width=80, height=28, font=("Segoe UI", 11, "bold"), corner_radius=6,
                command=lambda p=post, e=entry_cmt: self.adicionar_comentario(p, e, de_perfil)
            )
            btn_enviar_cmt.pack(side="right")

app = RedeSocial()
app.mainloop()