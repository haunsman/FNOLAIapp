from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import processor
from flask import Flask
from flask_bootstrap import Bootstrap
import json


app = Flask(__name__)

# Configure upload
UPLOAD_FOLDER = '/Users/creightonfowler/Desktop/FNOLProcess/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        claim_number = request.form.get('claim_number')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Append claim ID to the filename
            filename_with_claim_id = f"{os.path.splitext(filename)[0]}CID{claim_number}{os.path.splitext(filename)[1]}"
            
            # Save the renamed file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_with_claim_id))
            
            return redirect(url_for('upload_file'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=files)


@app.route('/process', methods=['POST'])
def process_file():
    filename = request.form['filename']
    file_url = url_for('upload_file', filename=filename, _external=True)
    file_url = file_url.replace("?filename=", "")
    file_url = file_url.replace("=", "")
    result = processor.process_file(file_url)
    
    # Delete the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    
    # Convert the result dictionary to a JSON string with double quotes for property names
    result_json = json.dumps(result, ensure_ascii=False)
    # Pass the JSON string to the processing_result template
    return redirect(url_for('processing_result', result=result_json))


@app.route('/processing_result')
def processing_result():
    result_json = request.args.get('result')
    # Parse the JSON string back into a dictionary
    result = json.loads(result_json)
    return render_template('processing_result.html', result=result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
