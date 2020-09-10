import json
import unittest

from config import config

from app import db
from app import create_app

class TestApi(unittest.TestCase):
    def setUp(self):
        enviroment = config['test']
        self.app = create_app(enviroment)
        self.client = self.app.test_client()

        self.content_type = 'application/json'
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'
        self.path_first_task = self.path + '/1'
        self.path_fake = self.path +'/100'
        self.data = {
            'title':'title','description':'descriptio', 'deadline':'2020-09-09 12:00:00'
        }
        self.data_update = {'title':'Nuevo Titulo'}
 
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def teste_one_equals_one(self):
        self.assertEqual(1, 1)

    def test_get_all_tasks(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code,200)

    def get_task_id(self, response):
        data = json.loads(response.data.decode('utf-8'))
        return data['data']['id']

    def test_get_first_task(self):
        response = self.client.get(path=self.path_first_task, content_type=self.content_type)
        self.assertEqual(response.status_code,200)

        task_id = self.get_task_id(response)

        self.assertEqual(task_id, 1)

    def test_len_tasks(self):
        response = self.client.get(path=self.path, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(len(data.get('data')),2)

    def test_not_found(self):
        response = self.client.get(path=self.path_fake, content_type=self.content_type)

        self.assertEqual(response.status_code,404)

    def test_create_task(self):
        response = self.client.post(path=self.path, data=json.dumps(self.data),
                                    content_type=self.content_type)

        self.assertEqual(response.status_code,200)
        task_id = self.get_task_id(response)

        self.assertEqual(task_id,3)

    def test_update_task(self):
        response = self.client.put(path=self.path_first_task, data=json.dumps(self.data_update),
                                    content_type=self.content_type)
        
        self.assertEqual(response.status_code,200)
        data = json.loads(response.data.decode('utf-8'))
        title = data['data']['title']

        self.assertEqual(title, self.data_update['title'])
    
    def test_delete_task(self):

        reponse = self.client.delete(path=self.path_first_task, content_type=self.content_type)
        self.assertEqual(reponse.status_code, 200)

        reponse = self.client.delete(path=self.path_first_task, content_type=self.content_type)
        self.assertEqual(reponse.status_code, 404)


if __name__ == "__main__":
    unittest.main()