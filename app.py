from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import processor
import json
import boto3
import botocore

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Configure AWS S3
S3_BUCKET_NAME = 'fnol-files'
S3_REGION = 'nyc3'
S3_ACCESS_KEY = 'DO00PUNYAAR7YQ8DA4CG'
S3_SECRET_KEY = 'UdfymTzv4m0YsEnBhE0R0g0WZOcbX4yrx49EPTNZbJ0'

session = boto3.session.Session()
client = session.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id='DO00PUNYAAR7YQ8DA4CG',
                        aws_secret_access_key='UdfymTzv4m0YsEnBhE0R0g0WZOcbX4yrx49EPTNZbJ0')


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

            # Upload file to S3 bucket
            s3_key = f"uploads/{filename_with_claim_id}"
            file_contents = file.read()
            client.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=file_contents)

            return redirect(url_for('upload_file'))

    return render_template('upload.html')


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
