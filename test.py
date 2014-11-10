'''import os
import run
import unittest
import sys


class ApiTestCase(unittest.TestCase):

    def setUp(self):

        self.app = run.app.test_client()
        self.key = 'D439EDD7A795FF0199ABBB1ADCC23194D521E783B1A14609F9A0220C1C20AE03'

    def test_legal(self):
        rv = self.app.post('/legal', data=dict(key=self.key), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_privacy(self):
        rv = self.app.post('/privacy', data=dict(key=self.key), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_prices(self):
        rv = self.app.post('/prices', data=dict(key=self.key), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_check_user(self):
        rv = self.app.post('/check_user', data=dict(email='nikola@pregmatch.org', key=self.key, password='sanja11'), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
        unittest.main()'''

import os
import run
import unittest
import sys


class ApiTestCase(unittest.TestCase):

    def __init__(self, testname, user, password):
        super(ApiTestCase, self).__init__(testname)
        self.user = user
        self.password = password

    def setUp(self):
        self.app = run.app.test_client()
        self.key = 'D439EDD7A795FF0199ABBB1ADCC23194D521E783B1A14609F9A0220C1C20AE03'

    def test_legal(self):
        rv = self.app.post('/legal', data=dict(key=self.key), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_privacy(self):
        rv = self.app.post('/privacy', data=dict(key=self.key), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_prices(self):
        rv = self.app.post('/prices', data=dict(key=self.key), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_check_user(self):
        rv = self.app.post('/check_user', data=dict(email=self.user, key=self.key, password=self.password), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(ApiTestCase("test_check_user", sys.argv[1], sys.argv[2]))

        unittest.TextTestRunner().run(suite)
