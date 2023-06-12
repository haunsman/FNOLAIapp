import superai as ai
import os
import boto3
import botocore

def process_file(file_url):
    client = ai.Client('5a030b7d-af35-4e17-a471-28a9a253c5b7')

    # Configure AWS S3
    S3_BUCKET_NAME = 'fnol-files'
    S3_REGION = 'nyc3'
    S3_ACCESS_KEY = 'DO00PUNYAAR7YQ8DA4CG'
    S3_SECRET_KEY = 'UdfymTzv4m0YsEnBhE0R0g0WZOcbX4yrx49EPTNZbJ0'

    session = boto3.session.Session()
    s3_client = session.client('s3',
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id='DO00PUNYAAR7YQ8DA4CG',
                            aws_secret_access_key='UdfymTzv4m0YsEnBhE0R0g0WZOcbX4yrx49EPTNZbJ0')

    # Extract the filename from the file_url
    filename = os.path.basename(file_url)

    # Construct the S3 key for the file
    s3_key = f"uploads/{filename}"

    try:
        file_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
    except Exception as e:
        return {'status': 'error', 'message': f'Error getting file from S3: {str(e)}'}

    file_content = file_object["Body"].read()

    # Now you can use the file_content with your AI client
    response = client.upload_data(
        mimeType="application/pdf",
        path=file_url,
        file=file_content,
        description=filename
    )

    client.create_jobs(
        app_id='295a75b8-5e89-484c-a435-ca7f282c5bcd',
        inputs=[{"documentUrl": "data://157528/"+file_url}],
    )

    return response







"""def process_file(file_url):
    client = ai.Client('5a030b7d-af35-4e17-a471-28a9a253c5b7')

    try:
        client.create_jobs(
            app_id='295a75b8-5e89-484c-a435-ca7f282c5bcd',
            inputs=[{"documentUrl": file_url}]
        )
        return {'status': 'success', 'message': 'File processing initiated.'}
    except Exception as e:
        return {'status': 'error', 'message': 'An error occurred during processing.', 'details': str(e)}
"""

"""
import superai as ai

client = ai.Client("5a030b7d-af35-4e17-a471-28a9a253c5b7")

client.create_jobs(
    app_id="295a75b8-5e89-484c-a435-ca7f282c5bcd",
    inputs=[{"documentUrl":"https://cdn.super.ai/invoice-example.pdf"}]
)


import superai as ai

client = ai.Client("live_1Ab23cdEFGH4iJ5K67Lmnop8qR10STulWX_2y3Za4_B")

f = open("hotel-pool-03.jpeg", "rb")

response = client.upload_data(
    mimeType="image/jpeg",
    path="default/hotel-pool-03.jpeg",
    file=f,
    description="Hotel pool image 03",
)

print(response)
"""