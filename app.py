# app.py
# Servidor web Flask que lida com a interface e o processamento.
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from classifier import classify_and_respond, extract_text_from_file

# Carrega variáveis de ambiente (sua GEMINI_API_KEY) do arquivo .env
load_dotenv()

app = Flask(__name__)
# Define um tamanho máximo para o upload para evitar sobrecarga (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Pasta para salvar uploads temporariamente
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    # Se o método for POST, processa os dados
    if request.method == 'POST':
        email_text = request.form.get('email_text')
        uploaded_file = request.files.get('email_file')
        
        content_to_process = ""

        if uploaded_file and uploaded_file.filename != '':
            # Se um arquivo foi enviado, extrai o texto dele
            filename = uploaded_file.filename
            content_to_process = extract_text_from_file(uploaded_file.stream, filename)
        elif email_text:
            # Se não houver arquivo, usa o texto da área de texto
            content_to_process = email_text
        
        if not content_to_process.strip():
            # Retorna um erro se nenhum conteúdo for enviado
            return render_template('index.html', error="Nenhum texto ou arquivo válido foi enviado.")

        # Chama a função principal de classificação
        result = classify_and_respond(content_to_process)
        
        # Retorna a página COM os novos resultados
        return render_template('index.html', category=result['category'], response=result['response'], original_text=content_to_process)

    # Se o método for GET (carregamento inicial da página), retorna a página sem resultados
    return render_template('index.html', category=None, response=None, original_text=None)

if __name__ == '__main__':
    # O Render usa um servidor WSGI como o Gunicorn, então isso é principalmente para teste local
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))