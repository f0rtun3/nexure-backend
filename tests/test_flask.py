import os
import unittest

from application import application, db


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = application
        self.client = self.app.test_client()
        self.policy_id = 53
        application.config['TESTING'] = True
        application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Jsv0#XY^ri@localhost/nexure_test'
        db.drop_all()
        db.create_all()
        self.assertEqual(application.debug, False)

    def test_fetch_master_policy(self):
        path = f"/policy_handler/{self.policy_id}"
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
