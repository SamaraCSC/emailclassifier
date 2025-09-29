# Classificador de Emails com Inteligência Artificial

## 📖 Descrição

Esta é uma aplicação web desenvolvida para otimizar a gestão de emails, automatizando a leitura, classificação e a sugestão de respostas. A ferramenta utiliza a API do Google Gemini para analisar o conteúdo dos emails e classificá-los em duas categorias principais, liberando tempo da equipe de tarefas manuais e repetitivas.

## ✨ Funcionalidades

-   **Classificação Automática**: Categoriza emails como **Produtivo** (requerem ação) ou **Improdutivo** (não requerem ação imediata).
-   **Sugestão de Respostas**: Gera respostas automáticas apropriadas para cada categoria de email.
-   **Interface Web Simples**: Permite o envio de emails através de upload de arquivos (`.txt`, `.pdf`) ou colando o texto diretamente.
-   **Exibição Clara dos Resultados**: Mostra a categoria do email e a resposta sugerida na tela.

## 🛠️ Tecnologias Utilizadas

-   **Backend**: Python 3, Flask
-   **Inteligência Artificial**: Google Gemini API
-   **Frontend**: HTML5, CSS3
-   **Bibliotecas Python**: `google-generativeai`, `pypdf2`, `python-dotenv`
-   **Servidor WSGI**: Gunicorn (para deploy)
-   **Plataforma de Deploy**: Render

## 🚀 Como Executar Localmente

Siga os passos abaixo para rodar a aplicação no seu ambiente de desenvolvimento.

1.  **Clone o Repositório** (se estiver no Git)
    ```bash
    git clone https://...
    cd email_classifier
    ```

2.  **Crie e Ative um Ambiente Virtual**
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure a Chave da API**
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Dentro dele, adicione sua chave da API do Gemini:
        ```
        GEMINI_API_KEY='SUA_CHAVE_SECRETA_AQUI'
        ```

5.  **Execute a Aplicação**
    ```bash
    flask run
    ```
    A aplicação estará disponível em `http://127.0.0.1:5000` no seu navegador.

## ☁️ Deploy no Render

O projeto está configurado para deploy na plataforma Render. O arquivo `Procfile` instrui o Render a usar o `gunicorn` para iniciar a aplicação web: