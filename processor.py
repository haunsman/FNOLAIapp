import superai as ai
import os

def process_file(file_url):
    client = ai.Client('5a030b7d-af35-4e17-a471-28a9a253c5b7')

    # Get the base directory path of your project
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Extract the filename from the file_url
    filename = os.path.basename(file_url)

    # Construct the absolute file path by joining the base directory and the filename
    file_path = os.path.join(base_dir, 'uploads', filename)

    if os.path.isfile(file_path):
        # Open the file using the file path
        with open(file_path, "rb") as f:
            response = client.upload_data(
                mimeType="application/pdf",
                path=file_url,
                file=f,
                description=filename
            )
            print(file_url)
            client.create_jobs(
                app_id='295a75b8-5e89-484c-a435-ca7f282c5bcd',
                inputs=[{"documentUrl": "data://157528/"+file_url}],
        
        )
    else:
        return {'status': 'error', 'message': 'File not found.'}

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