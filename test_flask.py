# coding=utf-8

import os
import unittest
from app import setup_app
from app.utils import md5
from flask import session
import urllib

app = setup_app()

class SampleTestCase(unittest.TestCase):

    def test_valid_login(self):
        with app.test_client() as client:
            data = {'username': 'nana', 'password': md5('nana')}
            fix = urllib.urlencode(data)
            response = client.get(
                '/ajax_login?' + fix,
                 # follow_redirects=True,
            )
            assert 'ok' in response.data
            print response.data
            # 这里需要登陆
            response = client.get(
                '/news/',
            )
            assert 'title' in response.data

    def test_get_news(self):
        with app.test_client() as client:
            response = client.get(
                '/news/',
            )
            print response.data


if __name__ == '__main__':
    unittest.main()
