# Classificador de Emails com Inteligencia Artificial

Esta é uma aplicação web desenvolvida para otimizar a gestão de emails, automatizando a leitura, classificação e a sugestão de respostas. A ferramenta utiliza API do Google Gemini categorizando emails como Produtivo ou Improdutivo.
Interface Web Simples para o envio de emails através de upload de arquivos (.txt, .pdf) ou colando o texto diretamente.

# Tecnologias Utilizadas:

Backend: Python 3, Flask
Inteligencia Artificial: Google Gemini API
Frontend: HTML5, CSS3
Bibliotecas Python: google-generativeai, pypdf2, python-dotenv
Servidor WSGI: Gunicorn (para deploy)
Plataforma de Deploy: Render (o plano gratuito que utilizei demora alguns minutos para iniciar)

# Como Executar Localmente

Clone o Repositório
    ```bash
    git clone https://...
    cd email_classifier
    ```

Crie e Ative um Ambiente Virtual
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

Instale as Dependências
    ```bash
    pip install -r requirements.txt
    ```

Configure a Chave da API
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Dentro dele, adicione sua chave da API do Gemini:
        ```
        GEMINI_API_KEY='SUA_CHAVE_SECRETA_AQUI'
        ```

Execute a Aplicação
    ```bash
    flask run
    ```
    A aplicação estará disponível em `http://127.0.0.1:5000` no seu navegador.

# Deploy no Render

O projeto está configurado para deploy na plataforma Render. O arquivo `Procfile` instrui o Render a usar o `gunicorn` para iniciar a aplicação web: