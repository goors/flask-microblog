
import os
import blog
import unittest
import sys


class ApiTestCase(unittest.TestCase):

    def __init__(self, testname, user, password):
        super(ApiTestCase, self).__init__(testname)
        self.user = user
        self.password = password

    def setUp(self):
        self.app = blog.app.test_client()



if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(ApiTestCase("test_check_user", sys.argv[1], sys.argv[2]))

        unittest.TextTestRunner().run(suite)
