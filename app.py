# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from module import extract_text_from_pdf, extract_keywords, match_reviewers, send_email, reviewers

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.secret_key = 'supersecretkey'  # Necessary for flash messages

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        text = extract_text_from_pdf(file_path)
        keywords = extract_keywords(text)
        matched_reviewers = match_reviewers(keywords, reviewers)
        
        if matched_reviewers:
            for reviewer in matched_reviewers:
                send_email(reviewer, "New Research Paper for Review", "Please review the attached paper.", file_path)
            flash('Emails sent to matched reviewers.')
        else:
            flash('No reviewers matched for the uploaded paper.')
        
        return redirect(url_for('index'))
    flash('Invalid file type. Only PDFs are allowed.')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
