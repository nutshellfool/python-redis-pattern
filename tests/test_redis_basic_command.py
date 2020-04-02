import unittest

from app import app as flask_app


class RedisBasicCommandsTestCase(unittest.TestCase):
    def setUp(self):
        flask_app.config["DEBUG"] = False
        self.app = flask_app.test_client()

    def test_hello_world(self):
        rv = self.app.get('/')
        self.assertIsNotNone(rv)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("Hello World!", str(rv.data, 'utf-8'))

    def test_echo_command(self):
        rv = self.app.get('/redis/echo')
        self.assertIsNotNone(rv)
        self.assertEqual(200, rv.status_code)
        self.assertEqual("foo", str(rv.data, 'utf-8'))


if __name__ == '__main__':
    unittest.main()
