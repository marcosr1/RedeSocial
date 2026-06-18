# FacePit

O **FacePit** é uma aplicação desktop de rede social desenvolvida em Python, com foco em interação entre usuários, compartilhamento de conteúdo e comunicação inteligente. O sistema utiliza uma interface gráfica moderna baseada em **CustomTkinter**, armazenamento local em arquivos JSON e um agente conversacional integrado chamado **Bot_Python**.

---

# Funcionalidades

## Sistema de Autenticação

- Cadastro de novos usuários
- Login com validação de credenciais
- Prevenção de nomes de usuário duplicados
- Proteção de contas reservadas do sistema

## Feed de Publicações

- Criação de publicações de texto
- Upload de imagens locais
- Sistema de curtidas com voto único por usuário
- Sistema de comentários
- Atualização dinâmica do feed

## Perfil Personalizável

- Alteração da foto de perfil
- Edição de biografia
- Personalização de informações do usuário
- Alternância entre modo claro e modo escuro

## Gerenciamento de Amigos

- Adição de amigos
- Remoção de amigos
- Controle de relacionamentos entre usuários

## Sistema de Mensagens

- Conversas privadas entre usuários
- Histórico persistente de mensagens
- Integração com serviços automatizados

## Bot_Python

O FacePit possui um agente conversacional integrado chamado **Bot_Python**, desenvolvido para auxiliar usuários em tarefas relacionadas à programação e tecnologia.

### Recursos do Bot

- Memória de curto prazo por usuário
- Análise básica de humor e sentimento
- Contexto de conversa persistente durante a execução
- Sugestões de projetos de programação
- Auxílio em depuração de código
- Respostas dinâmicas baseadas em intenções identificadas

### Tópicos Reconhecidos

- Erros e bugs em código
- Ideias de projetos
- Programação Python
- Desenvolvimento de software
- Jogos e tecnologia
- Conversação casual

## Suporte Automatizado

O sistema também conta com o usuário especial **Suporte_Hub**, responsável por fornecer orientações básicas e direcionamento para atendimento técnico.

---

# Arquitetura do Projeto

A aplicação foi organizada de forma modular para facilitar manutenção, evolução e reutilização de código.

## main.py

Responsável pela interface gráfica da aplicação.

### Funções principais

- Construção das telas
- Navegação entre janelas
- Exibição de publicações
- Interação com componentes visuais
- Atualização do feed

## logica_interface.py

Responsável pelas regras de negócio.

### Funções principais

- Cadastro de usuários
- Login
- Gerenciamento de posts
- Curtidas
- Comentários
- Controle de mensagens
- Persistência de dados

## motor_ia.py

Motor conversacional responsável pelo funcionamento do Bot_Python.

### Funções principais

- Memória contextual
- Análise de humor
- Processamento de intenções
- Geração de respostas
- Sugestão de projetos

---

# Estrutura do Projeto

```text
FacePit/
│
├── main.py
├── logica_interface.py
├── motor_ia.py
├── gerenciador_dados.py
│
├── usuarios.json
├── posts.json
├── mensagens.json
│
├── midias/
│
└── README.md
```

# Tecnologias Utilizadas

- Python 3.8+
- CustomTkinter
- Pillow (PIL)
- JSON
- Tkinter
- Datetime
- OS
- Shutil
- Random

---

# Como Executar o Projeto

## Pré-requisitos

- Python 3.8 ou superior

## Instalação das Dependências

```bash
pip install customtkinter pillow
```

## Executando a Aplicação

```bash
python main.py
```

---