import os
import unittest

from app import app, db


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.policy_id = 53
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:Jsv0#XY^ri@localhost/nexure_test'
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def test_fetch_master_policy(self):
        path = f"/policy_handler/{self.policy_id}"
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
