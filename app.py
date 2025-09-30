import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from classifier import classify_and_respond, extract_text_from_file

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_text = request.form.get('email_text')
        uploaded_file = request.files.get('email_file')
        
        content_to_process = ""

        if uploaded_file and uploaded_file.filename != '':
            filename = uploaded_file.filename
            content_to_process = extract_text_from_file(uploaded_file.stream, filename)
        elif email_text:
            content_to_process = email_text
        
        if not content_to_process.strip():
            return render_template('index.html', error="Nenhum texto ou arquivo válido foi enviado.")

        result = classify_and_respond(content_to_process)
        
        return render_template('index.html', category=result['category'], response=result['response'], original_text=content_to_process)

    return render_template('index.html', category=None, response=None, original_text='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))