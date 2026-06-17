import os
import json

ARQ_USUARIOS = "usuarios.json"
ARQ_POSTS = "posts.json"
ARQ_MENSAGENS = "mensagens.json"

def carregar_mensagens():
    if os.path.exists(ARQ_MENSAGENS):
        with open(ARQ_MENSAGENS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_mensagens(historico_mensagens):
    with open(ARQ_MENSAGENS, "w", encoding="utf-8") as f:
        json.dump(historico_mensagens, f, indent=4)

def carregar_usuarios():
    if os.path.exists(ARQ_USUARIOS):
        with open(ARQ_USUARIOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for u in dados:
                if "amigos" not in u:
                    u["amigos"] = []
            
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

def salvar_usuarios(usuarios):
    with open(ARQ_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)

def carregar_posts():
    if os.path.exists(ARQ_POSTS):
        with open(ARQ_POSTS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_posts(posts):
    with open(ARQ_POSTS, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)