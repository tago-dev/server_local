import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verifica se o arquivo é permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página principal com formulário de upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return f'Arquivo enviado com sucesso: <a href="/files/{file.filename}">{file.filename}</a>'
    return render_template_string("""
        <h1>Upload de Arquivos</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        <a href="/files">Ver arquivos salvos</a>
    """)

# Lista arquivos enviados
@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    links = [f'<li><a href="/files/{file}">{file}</a></li>' for file in files]
    return '<h2>Arquivos Salvos:</h2><ul>' + ''.join(links) + '</ul>'

# Baixar arquivos
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Inicia o servidor na rede local (ex: 10.x.x.x)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)