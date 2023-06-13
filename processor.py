import superai as ai
import os
import boto3
import botocore
import requests

def generate_presigned_url(s3_client, bucket_name, object_key, expiration=3600):
    """
    Generate a presigned URL to share an S3 object

    :param s3_client: Boto3 S3 client
    :param bucket_name: string
    :param object_key: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_key},
                                                    ExpiresIn=expiration)
    except botocore.exceptions.ClientError as e:
        # If there's a client error, return None.
        return None

    # The response contains the presigned URL
    return response



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

    presigned_url = generate_presigned_url(s3_client, S3_BUCKET_NAME, s3_key)

    if presigned_url is None:
        return {'status': 'error', 'message': 'Could not generate presigned URL'}

    # Download the file from the presigned url
    response = requests.get(presigned_url)
    open(filename, 'wb').write(response.content)

    # Now you can use the downloaded file with your AI client
    response = client.upload_data(
        mimeType="application/pdf",
        path=filename,
        file=open(filename, 'rb'),
        description=filename
    )

    # Delete the file after uploading
    os.remove(filename)

    client.create_jobs(
        app_id='295a75b8-5e89-484c-a435-ca7f282c5bcd',
        inputs=[{"documentUrl": "data://157528/"+file_url}],
    )

    return response
