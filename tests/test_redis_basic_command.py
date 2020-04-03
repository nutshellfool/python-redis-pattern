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

    #   Actually the unit test should test and verify the unit logic,
    #   Should not depend on third-part module (such as database, file system and so on)
    #   the demonstration of redis usage is quite sample, do not have too much logic her,
    #   so It's pretty reasonable to ignore the unittest case.
    #
    #   In some complex scenario, use unittest.mock (MagicMock, @patch) to mock the logic.
    #
    #
    # def test_echo_command(self):
    #     rv = self.app.get('/redis/echo')
    #     self.assertIsNotNone(rv)
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual("foo", str(rv.data, 'utf-8'))


if __name__ == '__main__':
    unittest.main()
