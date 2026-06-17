import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from datetime import datetime
import shutil
import os

# Importando os módulos locais que separamos
import gerenciador_dados as gd
from motor_ia import responder_como_ia

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PASTA_MIDIAS = "midias"
if not os.path.exists(PASTA_MIDIAS):
    os.makedirs(PASTA_MIDIAS)

# Carregamento inicial de dados usando o gerenciador
usuarios = gd.carregar_usuarios()
posts = gd.carregar_posts()
historico_mensagens = gd.carregar_mensagens()
usuario_logado = None

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

    def tela_login(self):
        self.limpar()
        frame_central = ctk.CTkFrame(self, width=420, height=500, corner_radius=16, fg_color=("#FFFFFF", "#161618"))
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        frame_central.pack_propagate(False)

        ctk.CTkLabel(frame_central, text="FacePit", font=("Segoe UI", 32, "bold")).pack(pady=(60, 5))
        ctk.CTkLabel(frame_central, text="Insira as suas credenciais para aceder.", font=("Segoe UI", 13), text_color="gray").pack(pady=(0, 40))

        self.login_usuario = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Utilizador")
        self.login_usuario.pack(pady=8)
        self.login_senha = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Palavra-passe", show="*")
        self.login_senha.pack(pady=8)
        
        self.lbl_erro = ctk.CTkLabel(frame_central, text="", text_color="#FF4D4D")
        self.lbl_erro.pack(pady=5)

        ctk.CTkButton(frame_central, text="Entrar", width=300, height=42, font=("Segoe UI", 13, "bold"), command=self.fazer_login).pack(pady=(15, 10))
        ctk.CTkButton(frame_central, text="Criar conta", width=300, height=35, fg_color="transparent", command=self.tela_cadastro).pack()

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

    def tela_cadastro(self):
        self.limpar()
        frame_central = ctk.CTkFrame(self, width=420, height=500, corner_radius=16, fg_color=("#FFFFFF", "#161618"))
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        frame_central.pack_propagate(False)

        ctk.CTkLabel(frame_central, text="Criar Conta", font=("Segoe UI", 28, "bold")).pack(pady=(60, 5))
        self.cad_usuario = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Nome de Utilizador")
        self.cad_usuario.pack(pady=8)
        self.cad_senha = ctk.CTkEntry(frame_central, width=300, height=42, placeholder_text="Defina uma Palavra-passe", show="*")
        self.cad_senha.pack(pady=8)

        ctk.CTkButton(frame_central, text="Registar", width=300, height=42, command=self.salvar_usuario).pack(pady=(20, 10))
        ctk.CTkButton(frame_central, text="Voltar ao Login", width=300, height=35, fg_color="transparent", command=self.tela_login).pack()

    def salvar_usuario(self):
        usuario = self.cad_usuario.get().strip()
        senha = self.cad_senha.get().strip()
        if not usuario or not senha: return
        if any(u["usuario"] == usuario for u in usuarios) or usuario in ["Suporte_Hub", "Bot_Python"]: return

        usuarios.append({"usuario": usuario, "senha": senha, "foto_perfil": None, "bio": "", "tema": "Dark", "amigos": []})
        gd.salvar_usuarios(usuarios)
        self.tela_login()

    def adicionar_amigo(self, nome_amigo):
        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
        perfil_amigo = next((u for u in usuarios if u["usuario"] == nome_amigo), None)
        if meu_perfil and perfil_amigo:
            if nome_amigo not in meu_perfil["amigos"]: meu_perfil["amigos"].append(nome_amigo)
            if usuario_logado not in perfil_amigo["amigos"]: perfil_amigo["amigos"].append(usuario_logado)
            gd.salvar_usuarios(usuarios)
            self.tela_amigos()

    def remover_amigo(self, nome_amigo):
        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
        perfil_amigo = next((u for u in usuarios if u["usuario"] == nome_amigo), None)
        if meu_perfil and perfil_amigo:
            if nome_amigo in meu_perfil["amigos"]: meu_perfil["amigos"].remove(nome_amigo)
            if usuario_logado in perfil_amigo["amigos"]: perfil_amigo["amigos"].remove(usuario_logado)
            gd.salvar_usuarios(usuarios)
            self.tela_amigos()

    def deletar_post(self, post_alvo, de_perfil):
        caminho_foto = post_alvo.get("imagem")
        if caminho_foto and os.path.exists(caminho_foto):
            try: os.remove(caminho_foto)
            except Exception as e: print(f"Erro físico: {e}")
        if post_alvo in posts: posts.remove(post_alvo)
        gd.salvar_posts(posts) 
        if de_perfil: self.tela_perfil()
        else: self.tela_feed()

    def deletar_usuario(self):
        global usuario_logado, usuarios, posts
        usuario_alvo = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
        if usuario_alvo:
            for u in usuarios:
                if usuario_logado in u.get("amigos", []): u["amigos"].remove(usuario_logado)
            usuarios.remove(usuario_alvo)
            gd.salvar_usuarios(usuarios)
            posts = [p for p in posts if p["autor"] != usuario_logado]
            gd.salvar_posts(posts)
            usuario_logado = None
            self.tela_login()

    def adicionar_comentario(self, post_alvo, campo_texto, de_perfil):
        texto = campo_texto.get().strip()
        if not texto: return
        if "comentarios" not in post_alvo: post_alvo["comentarios"] = []
        post_alvo["comentarios"].append({"autor": usuario_logado, "texto": texto})
        gd.salvar_posts(posts)
        if de_perfil: self.tela_perfil()
        else: self.tela_feed()

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
            except:
                label_status.configure(text="✕ Erro ao processar arquivo", text_color="#FF4D4D")

    def salvar_dados_perfil(self, campo_bio):
        nova_bio = campo_bio.get("1.0", "end").strip()
        for u in usuarios:
            if u["usuario"] == usuario_logado:
                u["bio"] = nova_bio
                if hasattr(self, 'nova_foto_perfil') and self.nova_foto_perfil:
                    u["foto_perfil"] = self.nova_foto_perfil
                break
        gd.salvar_usuarios(usuarios)
        self.tela_perfil()

    def construir_layout_base(self, aba_ativa):
        self.limpar()
        self.aba_atual = aba_ativa 
        topo = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkLabel(topo, text="FacePit", font=("Segoe UI", 20, "bold"), text_color=("#007AFF", "#FFFFFF")).pack(side="left", padx=25)
        self.campo_pesquisa = ctk.CTkEntry(topo, width=280, height=32, placeholder_text="Pesquisar usuário...", fg_color=("#F1F2F4", "#1E1E21"))
        self.campo_pesquisa.pack(side="left", padx=30)
        self.campo_pesquisa.bind("<Return>", self.ejecutar_pesquisa)

        ctk.CTkButton(topo, text="Sair", width=60, height=28, fg_color=("#FF3B30", "#FF453A"), command=self.tela_login).pack(side="right", padx=25)
        ctk.CTkLabel(topo, text=usuario_logado, font=("Segoe UI", 13, "bold"), text_color="gray").pack(side="right", padx=5)

        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=25, pady=20)

        largura_menu = 180 if self.menu_expandido else 55
        menu = ctk.CTkFrame(corpo, width=largura_menu, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        menu.pack(side="left", fill="y", padx=(0, 20))
        menu.pack_propagate(False)

        texto_hamburguer = "   Menu ☰" if self.menu_expandido else "☰"
        btn_toggle = ctk.CTkButton(menu, text=texto_hamburguer, height=35, width=40, fg_color="transparent", text_color="gray", command=self.alternar_menu)
        btn_toggle.pack(pady=(12, 10), anchor="w" if self.menu_expandido else "center", padx=12 if self.menu_expandido else 0)

        botoes_menu = [("  Início", "🏠", self.tela_feed, "inicio"), ("  Perfil", "👤", self.tela_perfil, "perfil"), ("  Amigos", "👥", self.tela_amigos, "amigos"), ("  Mensagens", "💬", self.tela_mensagens, "mensagens")]
        for texto_cheio, icone, comando, chave in botoes_menu:
            ativo = (chave == aba_ativa)
            texto_exibir = f"{icone} {texto_cheio}" if self.menu_expandido else icone
            btn = ctk.CTkButton(menu, text=texto_exibir, anchor="w" if self.menu_expandido else "center", height=38, fg_color=("#E6F0FA", "#1A2530") if ativo else "transparent", text_color=("#007AFF", "#4AA3DF") if ativo else ("#333333", "#A0A0A5"), command=comando)
            btn.pack(fill="x", padx=8 if self.menu_expandido else 4, pady=3)

        centro = ctk.CTkFrame(corpo, fg_color="transparent")
        centro.pack(side="left", fill="both", expand=True)
        return centro

    def tela_feed(self):
        centro = self.construir_layout_base(aba_ativa="inicio")
        caixa_post = ctk.CTkFrame(centro, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        caixa_post.pack(fill="x", pady=(0, 15))

        self.post_texto = ctk.CTkTextbox(caixa_post, height=65, fg_color=("#F9F9FB", "#1A1A1C"))
        self.post_texto.pack(fill="x", padx=15, pady=(15, 10))

        sub_barra = ctk.CTkFrame(caixa_post, fg_color="transparent")
        sub_barra.pack(fill="x", padx=15, pady=(0, 15))

        self.btn_foto = ctk.CTkButton(sub_barra, text="Anexar Imagem", width=120, height=30, fg_color=("#F1F2F4", "#222225"), text_color=("#333333", "#CCCCCC"), command=self.escolher_foto)
        self.btn_foto.pack(side="left")

        ctk.CTkButton(sub_barra, text="Publicar", width=80, height=30, fg_color="#007AFF", command=self.publicar_post).pack(side="right")

        self.feed_frame = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        self.feed_frame.pack(fill="both", expand=True)
        self.caminho_imagem = None
        self.renderizar_lista_posts(posts)

    def disparar_mensagem(self, destinatario, campo_texto):
        texto = campo_texto.get().strip()
        if not texto: return

        historico_mensagens.append({"enviado_por": usuario_logado, "recebido_por": destinatario, "texto": texto})

        if destinatario == "Bot_Python":
            resposta_ia = responder_como_ia(texto)
            historico_mensagens.append({"enviado_por": "Bot_Python", "recebido_por": usuario_logado, "texto": resposta_ia})
        elif destinatario == "Suporte_Hub":
            resposta_automatica = "Olá! Caso precise de suporte avançado para recuperação de conta ou bugs na interface, chame nossa equipe oficial via Whatsapp no número: (86) 98183-5751"
            historico_mensagens.append({"enviado_por": "Suporte_Hub", "recebido_por": usuario_logado, "texto": resposta_automatica})

        gd.salvar_mensagens(historico_mensagens)     
        campo_texto.delete(0, 'end')  
        self.tela_mensagens(destinatario)  

    def tela_mensagens(self, contato_selecionado=None):
        centro = self.construir_layout_base(aba_ativa="mensagens")
        container_chat = ctk.CTkFrame(centro, fg_color="transparent")
        container_chat.pack(fill="both", expand=True)

        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), {"amigos": []})
        contatos = ["Bot_Python", "Suporte_Hub"] + meu_perfil.get("amigos", [])

        if contato_selecionado is None or contato_selecionado not in contatos:
            contato_selecionado = contatos[0]

        coluna_esquerda = ctk.CTkFrame(container_chat, width=220, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        coluna_esquerda.pack(side="left", fill="y", padx=(0, 15))
        coluna_esquerda.pack_propagate(False)

        ctk.CTkLabel(coluna_esquerda, text="Conversas", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=15, pady=12)

        for contato in contatos:
            esta_ativo = (contato == contato_selecionado)
            prefixo = "🤖" if contato == "Bot_Python" else "🛠️" if contato == "Suporte_Hub" else "💬"
            btn_contato = ctk.CTkButton(coluna_esquerda, text=f"{prefixo} {contato}", anchor="w", height=38, fg_color=("#F0F4F8", "#1A242F") if esta_ativo else "transparent", text_color=("#007AFF", "#4AA3DF") if esta_ativo else ("#1A1A1A", "#BBBBBC"), command=lambda c=contato: self.tela_mensagens(contato_selecionado=c))
            btn_contato.pack(fill="x", padx=6, pady=2)

        coluna_direita = ctk.CTkFrame(container_chat, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
        coluna_direita.pack(side="left", fill="both", expand=True)

        topo_chat = ctk.CTkFrame(coluna_direita, height=45, fg_color="transparent")
        topo_chat.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(topo_chat, text=contato_selecionado, font=("Segoe UI", 13, "bold")).pack(side="left")

        area_baloes = ctk.CTkScrollableFrame(coluna_direita, fg_color="transparent")
        area_baloes.pack(fill="both", expand=True, padx=15, pady=5)

        mensagens_filtradas = [m for m in historico_mensagens if (m["enviado_por"] == usuario_logado and m["recebido_por"] == contato_selecionado) or (m["enviado_por"] == contato_selecionado and m["recebido_por"] == usuario_logado)]

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

        campo_msg = ctk.CTkEntry(barra_envio, placeholder_text="Mensagem...", fg_color=("#F1F2F4", "#1E1E21"))
        campo_msg.pack(side="left", fill="both", expand=True, padx=(0, 10))
        campo_msg.bind("<Return>", lambda event: self.disparar_mensagem(contato_selecionado, campo_msg))
        ctk.CTkButton(barra_envio, text="Enviar", width=70, command=lambda: self.disparar_mensagem(contato_selecionado, campo_msg)).pack(side="right", fill="y")

    def tela_amigos(self):
        centro = self.construir_layout_base(aba_ativa="amigos")
        scroll_amigos = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        scroll_amigos.pack(fill="both", expand=True)

        meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), {"amigos": []})
        meus_amigos = meu_perfil.get("amigos", [])

        ctk.CTkLabel(scroll_amigos, text="Os meus amigos", font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=5, pady=(5, 10))
        if not meus_amigos:
            ctk.CTkLabel(scroll_amigos, text="Lista vazia.", text_color="gray").pack(anchor="w", padx=15)
        else:
            for amigo in meus_amigos:
                card = ctk.CTkFrame(scroll_amigos, fg_color=("#FFFFFF", "#141416"), height=50)
                card.pack(fill="x", pady=3)
                card.pack_propagate(False)
                ctk.CTkButton(card, text=amigo, fg_color="transparent", command=lambda n=amigo: self.tela_perfil(usuario_alvo=n)).pack(side="left", padx=10)
                ctk.CTkButton(card, text="Remover", text_color="#FF3B30", fg_color="transparent", command=lambda a=amigo: self.remover_amigo(a)).pack(side="right", padx=15)

        ctk.CTkLabel(scroll_amigos, text="Lista de utilizadores", font=("Segoe UI", 14, "bold"), text_color="gray").pack(anchor="w", padx=5, pady=(20, 10))
        usuarios_restantes = [u["usuario"] for u in usuarios if u["usuario"] != usuario_logado and u["usuario"] not in meus_amigos and u["usuario"] not in ["Bot_Python", "Suporte_Hub"]]

        if not usuarios_restantes:
            ctk.CTkLabel(scroll_amigos, text="Nenhum utilizador registado pendente.", text_color="gray").pack(anchor="w", padx=15)
        else:
            for sug in usuarios_restantes:
                card_sug = ctk.CTkFrame(scroll_amigos, fg_color=("#FFFFFF", "#141416"), height=50)
                card_sug.pack(fill="x", pady=3)
                card_sug.pack_propagate(False)
                ctk.CTkButton(card_sug, text=sug, fg_color="transparent", command=lambda n=sug: self.tela_perfil(usuario_alvo=n)).pack(side="left", padx=10)
                ctk.CTkButton(card_sug, text="Adicionar", fg_color="#007AFF", command=lambda s=sug: self.adicionar_amigo(s)).pack(side="right", padx=15)

    def tela_perfil(self, usuario_alvo=None):
        centro = self.construir_layout_base(aba_ativa="perfil" if usuario_alvo is None else "inicio")
        self.nova_foto_perfil = None 
        eh_meu_perfil = (usuario_alvo is None or usuario_alvo == usuario_logado)
        dono_da_pagina = usuario_logado if eh_meu_perfil else usuario_alvo

        dados_usuario = next((u for u in usuarios if u["usuario"] == dono_da_pagina), {"bio": "", "foto_perfil": None})
        posts_do_usuario = [p for p in posts if p["autor"] == dono_da_pagina]

        card_perfil = ctk.CTkFrame(centro, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
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
            except: pass

        ctk.CTkLabel(frame_foto_nome, text=dono_da_pagina, font=("Segoe UI", 20, "bold")).pack(side="left", anchor="center")

        if not eh_meu_perfil:
            ctk.CTkButton(frame_foto_nome, text="Voltar ao Feed", command=self.tela_feed).pack(side="right")

        bio_atual = dados_usuario.get("bio") if dados_usuario.get("bio") else "Sem biografia."
        ctk.CTkLabel(card_perfil, text=bio_atual, font=("Segoe UI", 13, "italic"), text_color="gray").pack(anchor="w", padx=20, pady=2)

        if eh_meu_perfil:
            frame_edicao = ctk.CTkFrame(card_perfil, fg_color=("#FAFAFC", "#19191B"))
            frame_edicao.pack(fill="x", padx=15, pady=(0, 15))
            frame_linha = ctk.CTkFrame(frame_edicao, fg_color="transparent")
            frame_linha.pack(fill="x", padx=10, pady=10)

            ctk.CTkButton(frame_linha, text="Alterar Foto", command=lambda: self.escolher_foto_perfil(lbl_status_foto)).pack(side="left")
            lbl_status_foto = ctk.CTkLabel(frame_linha, text="Padrão", text_color="gray")
            lbl_status_foto.pack(side="left", padx=8)

            txt_bio = ctk.CTkTextbox(frame_linha, height=32)
            txt_bio.pack(side="left", fill="x", expand=True, padx=10)
            txt_bio.insert("1.0", dados_usuario.get("bio", ""))

            ctk.CTkButton(frame_linha, text="Salvar", command=lambda: self.salvar_dados_perfil(txt_bio)).pack(side="right")

            frame_tema = ctk.CTkFrame(frame_edicao, fg_color="transparent")
            frame_tema.pack(fill="x", padx=10, pady=(0, 10))
            self.switch_tema = ctk.CTkSwitch(frame_tema, text="Modo Escuro", variable=ctk.StringVar(value="on" if ctk.get_appearance_mode() == "Dark" else "off"), onvalue="on", offvalue="off", command=self.alternar_tema_sistema)
            self.switch_tema.pack(side="left")
            ctk.CTkButton(frame_tema, text="Excluir Conta", fg_color="#FF3B30", command=self.deletar_usuario).pack(side="right")

        scroll_publicacoes = ctk.CTkScrollableFrame(centro, fg_color="transparent")
        scroll_publicacoes.pack(fill="both", expand=True)
        self.feed_frame = scroll_publicacoes
        self.renderizar_lista_posts(posts_do_usuario, de_perfil=eh_meu_perfil)

    def escolher_foto(self):
        arquivo_origem = filedialog.askopenfilename(title="Anexar imagem", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
        if arquivo_origem:
            try:
                _, extensao = os.path.splitext(arquivo_origem)
                nome_novo_arquivo = f"post_{usuario_logado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extensao}"
                caminho_destino = os.path.join(PASTA_MIDIAS, nome_novo_arquivo)
                shutil.copy(arquivo_origem, caminho_destino)
                self.caminho_imagem = caminho_destino 
                self.btn_foto.configure(text="✓ Imagem Pronta", fg_color="#34C759", text_color="#FFFFFF")
            except:
                self.caminho_imagem = None
                self.btn_foto.configure(text="Falhou", fg_color="#FF3B30", text_color="#FFFFFF")

    def publicar_post(self):
        if not hasattr(self, 'caminho_imagem'): self.caminho_imagem = None
        texto = self.post_texto.get("1.0", "end").strip()
        if not texto and not self.caminho_imagem: return

        posts.insert(0, {"autor": usuario_logado, "texto": texto, "imagem": self.caminho_imagem, "curtidas": 0})
        gd.salvar_posts(posts)
        self.post_texto.delete("1.0", "end")
        self.caminho_imagem = None 
        self.btn_foto.configure(text="Anexar Imagem", fg_color=("#F1F2F4", "#222225"), text_color=("#333333", "#CCCCCC"))
        self.tela_feed()

    def curtir(self, post_alvo, de_perfil):
        for p in posts:
            if p == post_alvo:
                p["curtidas"] += 1
                break
        gd.salvar_posts(posts)
        if de_perfil: self.tela_perfil()
        else: self.tela_feed()

    def renderizar_lista_posts(self, lista_filtrada, de_perfil=False):
        for w in self.feed_frame.winfo_children(): w.destroy()
        if not lista_filtrada:
            ctk.CTkLabel(self.feed_frame, text="Nenhuma publicação disponível.", font=("Segoe UI", 12, "italic"), text_color="gray").pack(pady=30)
            return

        for post in lista_filtrada:
            card = ctk.CTkFrame(self.feed_frame, fg_color=("#FFFFFF", "#141416"), border_width=1, border_color=("#EAEAEA", "#1F1F22"))
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
                except: pass

            ctk.CTkButton(cabecalho, text=post['autor'], font=("Segoe UI", 13, "bold"), fg_color="transparent", command=lambda a=post['autor']: self.tela_perfil(usuario_alvo=a)).pack(side="left")

            if post["autor"] == usuario_logado:
                ctk.CTkButton(cabecalho, text="✕", width=20, height=20, fg_color="transparent", text_color="gray", command=lambda p=post: self.deletar_post(p, de_perfil)).pack(side="right")

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
                except: pass

            rodape = ctk.CTkFrame(card, fg_color="transparent")
            rodape.pack(fill="x", padx=15, pady=5)
            ctk.CTkButton(rodape, text=f"♥  {post['curtidas']}", width=50, height=24, fg_color="transparent", text_color="#FF3B30", command=lambda p=post: self.curtir(p, de_perfil)).pack(side="left")

            frame_comentarios = ctk.CTkFrame(card, fg_color=("#F9F9FB", "#18181A"))
            frame_comentarios.pack(fill="x", padx=15, pady=(5, 10))

            if "comentarios" in post and post["comentarios"]:
                for cmt in post["comentarios"]:
                    ctk.CTkLabel(frame_comentarios, text=f"{cmt['autor']}: {cmt['texto']}", justify="left").pack(anchor="w", padx=10, pady=1)

            barra_digitar_cmt = ctk.CTkFrame(frame_comentarios, fg_color="transparent")
            barra_digitar_cmt.pack(fill="x", padx=5, pady=5)
            entry_cmt = ctk.CTkEntry(barra_digitar_cmt, placeholder_text="Comentar...", height=24)
            entry_cmt.pack(side="left", fill="x", expand=True, padx=(0, 5))
            ctk.CTkButton(barra_digitar_cmt, text="OK", width=40, height=24, command=lambda p=post, e=entry_cmt: self.adicionar_comentario(p, e, de_perfil)).pack(side="right")

if __name__ == "__main__":
    app = FacePit()
    app.mainloop()