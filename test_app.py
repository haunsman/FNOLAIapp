import unittest
import app
import os

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        if not os.path.exists(app.app.config['UPLOADED_FILES_DEST']):
            os.makedirs(app.app.config['UPLOADED_FILES_DEST'])

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        data = {
            'file': (open('sample.txt', 'rb'), 'sample.txt')  # Use a sample text file for testing
        }
        response = self.app.post('/upload', data=data)
        self.assertEqual(response.status_code, 200)

    def test_process(self):
        # TODO: Implement this test
        pass

if __name__ == '__main__':
    unittest.main()
