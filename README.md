# Este é o material de estudo criado durante as aulas de FasteAPI do zero, apresentadas por Eduardo Mendes, também conhecido como [dunossauro](https://github.com/dunossauro).

# 🚀 Aprendizados e Tecnologias do Projeto

Neste projeto, foram explorados os conceitos fundamentais do desenvolvimento backend moderno em Python, abrangendo desde a criação de APIs até o deploy em produção.

---

## 🛠️ Tecnologias e Conceitos Aplicados

### ⚡ **FastAPI**
- Construção de endpoints assíncronos e estruturação de APIs de alta performance.

### 🧪 **Testes Automatizados**
- **Pytest**: Execução e estruturação de testes unitários e de integração para garantir a estabilidade da aplicação.

### 🔄 **Migrações de Banco de Dados**
- **Alembic**: Gerenciamento e controle de versionamento do esquema do banco de dados.

### 🗄️ **Banco de Dados & Evolução Arquitetural**
A camada de persistência evoluiu progressivamente ao longo do desenvolvimento:
1. **SQLite**: Utilizado na fase inicial para prototipagem e testes locais.
2. **Suporte Assíncrono**: Implementação da biblioteca `aiosqlite` para operações de E/S não bloqueantes.
3. **PostgreSQL**: Migração final para um banco de dados relacional robusto e pronto para produção.

### 🐳 **Docker**
- Conteinerização da aplicação, com foco nos comandos e conceitos essenciais para criação de imagens, execução e gerenciamento de containers.

### ☁️ **Deploy & Infraestrutura**
- **Histórico**: A aplicação foi inicialmente implantada via **Fly.io** (SaaS).
- **Ajuste**: Devido a restrições na plataforma, o deploy foi migrado para o **Render**.
- **Adaptações**: Ajustes pontuais no script de configurações (`settings.py`) e no `Dockerfile` foram realizados para suporte à nova plataforma.
