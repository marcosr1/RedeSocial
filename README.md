# FacePit 🌐

O **FacePit** é uma aplicação desktop de rede social interativa desenvolvida em Python. Utilizando uma interface gráfica moderna e responsiva baseada em `customtkinter`, o ecossistema conta com gerenciamento local de dados em JSON e um motor de inteligência artificial nativo para interagir com os usuários no chat.

---

## ✨ Funcionalidades

* **Sistema de Autenticação:** Criação de conta e Login seguro de usuários com validação de credenciais.
* **Feed de Publicações:** Linha do tempo dinâmica onde é possível publicar textos, anexar imagens do computador, curtir (voto único por usuário) e comentar em posts.
* **Perfil Customizável:** Edição de biografia, upload de foto de perfil personalizada e alternância de tema gráfico (Modo Escuro / Modo Claro).
* **Gerenciamento de Amigos:** Adicione ou remova outros utilizadores da plataforma para liberar a comunicação direta.
* **Chat com IA Integrada:** Conversa privada com o **Bot_Python**, um agente cognitivo capaz de analisar o humor do usuário, sugerir ideias de projetos de programação e ajudar a debugar códigos com base no contexto da conversa.
* **Suporte Automatizado:** Canal direto com o `Suporte_Hub` para orientações técnicas e redirecionamento.

---

## 🛠️ Arquitetura do Projeto

O projeto é dividido em três módulos principais:

1.  `main.py`: Concentra a interface do usuário (GUI), transições de telas e regras de apresentação visual utilizando o paradigma de Orientação a Objetos.
2.  `gerenciador_dados.py`: Camada de persistência responsável por carregar e salvar dados de usuários, posts e mensagens em arquivos estruturados `.json`.
3.  `motor_ia.py`: Motor conversacional lógico que gerencia estados de memória de curto prazo, análise de sentimentos e filtros de intenção por palavras-chave.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado em sua máquina.

### Instalação das Dependências
Este projeto utiliza algumas bibliotecas de terceiros que precisam ser instaladas antes da execução. As bibliotecas nativas do Python utilizadas (`os`, `json`, `random`, `shutil`, `datetime` e `tkinter`) não requerem instalação adicional.
Para instalar as dependências externas, execute o comando abaixo no seu terminal:
```bash
pip install customtkinter pillow
```