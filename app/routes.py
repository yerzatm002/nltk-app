from flask import Flask, request, render_template, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app.utils import process_pdf
import os

UPLOAD_FOLDER = 'app/uploads'
PROCESSED_FOLDER = 'app/processed'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"error": "Файл жоқ"}, 400  # Возвращаем JSON с ошибкой

    file = request.files['file']
    if file.filename == '':
        return {"error": "Файл таңдалмаған"}, 400  # Возвращаем JSON с ошибкой

    # Сохранение файла
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Обработка файла
    pdf_file = process_pdf(filepath, app.config['PROCESSED_FOLDER'])

    if pdf_file:  # Успешная обработка
        # file_url = url_for('download_file', filename=os.path.abspath, _external=True)
        return {"file_url": os.path.abspath(pdf_file)}, 200  # Возвращаем JSON с ссылкой на файл
    else:
        return {"error": "Өңдеу қатесі"}, 500  # Возвращаем JSON с ошибкой


@app.route('/processed/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)