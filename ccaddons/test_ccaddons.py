import unittest
import ccapi

class testHeaders(unittest.TestCase):

    def test_auth_expected(self):
        self.assertEqual(ccapi.make_authorization('ahoover', 'je5ter'), 
                    u'Basic  YWhvb3ZlcjpqZTV0ZXI=', 
                    'Wrong response to Expected parameters')

    def test_auth_none(self):
        self.assertEqual(ccapi.make_authorization(),                
                    u'Basic  YWhvb3ZlcjpqZTV0ZXI=', 
                    'Wrong response to null parameters')

    def test_auth_spaces(self):
        self.assertEqual(ccapi.make_authorization(' ', ' '),
                    u'Basic  IDog',
                    'Wrong response to spaces parameters')

