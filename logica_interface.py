import os
import shutil
from datetime import datetime
from tkinter import filedialog
import gerenciador_dados as gd
from motor_ia import responder_como_ia

# Esta função apenas ajuda a main a carregar os dados para o escopo dela de forma limpa
def carregar_dados_iniciais():
    return gd.carregar_usuarios(), gd.carregar_posts(), gd.carregar_mensagens()

def salvar_usuario_logica(usuarios, usuario, senha):
    if not usuario or not senha: 
        return False
    if any(u["usuario"] == usuario for u in usuarios) or usuario in ["Suporte_Hub", "Bot_Python"]: 
        return False

    usuarios.append({"usuario": usuario, "senha": senha, "foto_perfil": None, "bio": "", "tema": "Dark", "amigos": []})
    gd.salvar_usuarios(usuarios)
    return True

def adicionar_amigo_logica(usuarios, usuario_logado, nome_amigo):
    meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
    perfil_amigo = next((u for u in usuarios if u["usuario"] == nome_amigo), None)
    if meu_perfil and perfil_amigo:
        if nome_amigo not in meu_perfil["amigos"]: 
            meu_perfil["amigos"].append(nome_amigo)
        if usuario_logado not in perfil_amigo["amigos"]: 
            perfil_amigo["amigos"].append(usuario_logado)
        gd.salvar_usuarios(usuarios)

def remover_amigo_logica(usuarios, usuario_logado, nome_amigo):
    meu_perfil = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
    perfil_amigo = next((u for u in usuarios if u["usuario"] == nome_amigo), None)
    if meu_perfil and perfil_amigo:
        if nome_amigo in meu_perfil["amigos"]: 
            meu_perfil["amigos"].remove(nome_amigo)
        if usuario_logado in perfil_amigo["amigos"]: 
            perfil_amigo["amigos"].remove(usuario_logado)
        gd.salvar_usuarios(usuarios)

def deletar_post_logica(posts, post_alvo):
    caminho_foto = post_alvo.get("imagem")
    if caminho_foto and os.path.exists(caminho_foto):
        try: 
            os.remove(caminho_foto)
        except Exception as e: 
            print(f"Erro físico: {e}")
    if post_alvo in posts: 
        posts.remove(post_alvo)
    gd.salvar_posts(posts)

def deletar_usuario_logica(usuarios, posts, usuario_logado):
    usuario_alvo = next((u for u in usuarios if u["usuario"] == usuario_logado), None)
    if usuario_alvo:
        for u in usuarios:
            if usuario_logado in u.get("amigos", []): 
                u["amigos"].remove(usuario_logado)
        usuarios.remove(usuario_alvo)
        gd.salvar_usuarios(usuarios)
        posts_filtrados = [p for p in posts if p["autor"] != usuario_logado]
        gd.salvar_posts(posts_filtrados)
        return posts_filtrados
    return posts

def adicionar_comentario_logica(posts, post_alvo, usuario_logado, texto):
    if "comentarios" not in post_alvo: 
        post_alvo["comentarios"] = []
    post_alvo["comentarios"].append({"autor": usuario_logado, "texto": texto})
    gd.salvar_posts(posts)

def escolher_foto_perfil_logica(usuario_logado, label_status, pasta_midias):
    arquivo_origem = filedialog.askopenfilename(title="Foto de perfil", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
    if arquivo_origem:
        try:
            _, extensao = os.path.splitext(arquivo_origem)
            nome_novo_arquivo = f"perfil_{usuario_logado}{extensao}"
            caminho_destino = os.path.join(pasta_midias, nome_novo_arquivo)
            shutil.copy(arquivo_origem, caminho_destino)
            label_status.configure(text="✓ Imagem importada com sucesso", text_color="#28A745")
            return caminho_destino
        except:
            label_status.configure(text="✕ Erro ao processar arquivo", text_color="#FF4D4D")
    return None

def salvar_dados_perfil_logica(usuarios, usuario_logado, nova_bio, nova_foto_perfil):
    for u in usuarios:
        if u["usuario"] == usuario_logado:
            u["bio"] = nova_bio
            if nova_foto_perfil:
                u["foto_perfil"] = nova_foto_perfil
            break
    gd.salvar_usuarios(usuarios)

def disparar_mensagem_logica(historico_mensagens, usuario_logado, destinatario, texto):
    historico_mensagens.append({"enviado_por": usuario_logado, "recebido_por": destinatario, "texto": texto})

    if destinatario == "Bot_Python":
        resposta_ia = responder_como_ia(texto)
        historico_mensagens.append({"enviado_por": "Bot_Python", "recebido_por": usuario_logado, "texto": resposta_ia})
    elif destinatario == "Suporte_Hub":
        resposta_automatica = "Olá! Caso precise de suporte avançado para recuperação de conta ou bugs na interface, chame nossa equipe oficial via Whatsapp no número: (86) 98183-5751"
        historico_mensagens.append({"enviado_por": "Suporte_Hub", "recebido_por": usuario_logado, "texto": resposta_automatica})

    gd.salvar_mensagens(historico_mensagens)

def escolher_foto_logica(usuario_logado, btn_foto, pasta_midias):
    arquivo_origem = filedialog.askopenfilename(title="Anexar imagem", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
    if arquivo_origem:
        try:
            _, extensao = os.path.splitext(arquivo_origem)
            nome_novo_arquivo = f"post_{usuario_logado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extensao}"
            caminho_destino = os.path.join(pasta_midias, nome_novo_arquivo)
            shutil.copy(arquivo_origem, caminho_destino)
            btn_foto.configure(text="✓ Imagem Pronta", fg_color="#34C759", text_color="#FFFFFF")
            return caminho_destino
        except:
            btn_foto.configure(text="Falhou", fg_color="#FF3B30", text_color="#FFFFFF")
            return None
    return None

def publicar_post_logica(posts, usuario_logado, texto, caminho_imagem):
    posts.insert(0, {"autor": usuario_logado, "texto": texto, "imagem": caminho_imagem, "curtidas": []})
    gd.salvar_posts(posts)

def curtir_logica(posts, usuario_logado, post_alvo):
    for p in posts:
        if p == post_alvo:
            if isinstance(p.get("curtidas"), int):
                p["curtidas"] = []
            
            if usuario_logado in p["curtidas"]:
                p["curtidas"].remove(usuario_logado)
            else:
                p["curtidas"].append(usuario_logado)
            break
    gd.salvar_posts(posts)