# SiGP
SISTEMA DE GESTÃO DA PREFEITURA DE PUREZA

## Descrição

O SiGP é um sistema desenvolvido durante o estágio na Prefeitura Municipal de Pureza, criado para substituir o sistema *Top Down Solution*, que apresentava falhas constantes e atrasava os processos administrativos. O objetivo do SiGP é proporcionar uma ferramenta eficiente, confiável e integrada para a gestão de projetos, protocolos, documentos e demais atividades administrativas da prefeitura.

---

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python  
- **Framework Web:** Flask  
- **Template Engine:** Jinja  
- **Frontend:** HTML, CSS, JavaScript  
- **Banco de Dados:** MySQL  
- **Controle de Autenticação:** Login e Logout para acesso seguro  

---

## Funcionalidades Principais

- CRUD completo para:  
  - Usuários  
  - Servidores  
  - Secretarias  
  - Cargos  
  - Notícias  
  - Atividades  
  - Calendário de eventos  
  - Protocolos e tramitações  
  - Documentos (GED - Gestão Eletrônica de Documentos)  
  - Logs do sistema  
  - Perfil do usuário (com autenticação)  

- Controle de autenticação com login e logout, garantindo segurança no acesso ao sistema.  
- Interface web responsiva e intuitiva.  

---

## Arquitetura do Sistema

O sistema segue o padrão MVC (Model-View-Controller):

- **Models:** Definem a estrutura das tabelas no banco de dados e mapeiam os dados da aplicação.  
- **Controllers:** Responsáveis pela lógica de negócio e tratamento das requisições HTTP.  
- **Forms:** Utilizados para validação e processamento seguro dos dados fornecidos pelo usuário através dos formulários.  

---

## Instalação

1. Clone este repositório:  
   ```bash
   git clone https://github.com/Leandersonborgess23/SiGP.git


2. Ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  #Linux/macOS  
   venv\Scripts\activate     #Windows

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt

4. Configure o banco de dados MySQL e atualize as configurações de conexão no arquivo de configuração do projeto.

5. Execute a aplicação:
   ```bash
   flask run


## Contato

Leanderson Borges

Estagiário na Prefeitura Municipal de Pureza

**Email:** leandersonborges39@gmail.com