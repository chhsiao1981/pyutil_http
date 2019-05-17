# -*- coding: utf-8 -*-

import unittest
import logging
import re
import requests_mock

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from pyutil_http import util

from multiprocessing import Process

requests_mock.Mocker.TEST_PREFIX = 'test'

@requests_mock.Mocker()
class TestUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_http_multipost(self, m):
        m.post('http://localhost:1234/echo', text='echo1')
        m.post('http://localhost:1235/echo', text='echo2')

        url_data = {'http://localhost:1234/echo': 'echo1', 'http://localhost:1235/echo': 'echo2'}
        err, results = util.http_multipost(url_data)
        self.assertIsNone(err)

        err1, content1 = results['http://localhost:1234/echo']
        err2, content2 = results['http://localhost:1235/echo']

        self.assertIsNone(err1)
        self.assertEqual(b'echo1', content1)
        self.assertIsNone(err2)
        self.assertEqual(b'echo2', content2)

    def test_http_multipost_list(self, m):
        m.post('http://localhost:1234/echo', text='echo3')

        url_data_list = [
            ('http://localhost:1234/echo', 'echo3'),
            ('http://localhost:1236/echo', 'echo2'),
        ]

        err, results = util.http_multipost_list(url_data_list)
        self.assertIsNone(err)

        self.assertEqual(2, len(results))

        url1, (err1, content1) = results[0]
        url2, (err2, content2) = results[1]

        self.assertIsNone(err1)
        self.assertEqual(b'echo3', content1)
        self.assertIsNotNone(err2)
        self.assertEqual(b'', content2)

    def test_http_multiget(self, m):
        m.get('http://localhost:1234/echo?echo=echo1', text='echo1')
        m.get('http://localhost:1235/echo?echo=echo2', text='echo2')
        m.get('http://localhost:1236/echo?echo=echo3', text='echo3')

        urls = [
            'http://localhost:1234/echo?echo=echo1',
            'http://localhost:1235/echo?echo=echo2',
            'http://localhost:1236/echo?echo=echo3',
        ]

        err, results = util.http_multiget(urls)
        self.assertIsNone(err)

        err1, content1 = results['http://localhost:1234/echo?echo=echo1']
        err2, content2 = results['http://localhost:1235/echo?echo=echo2']
        err3, content3 = results['http://localhost:1236/echo?echo=echo3']
        self.assertIsNone(err1)
        self.assertEqual(b'echo1', content1)
        self.assertIsNone(err2)
        self.assertEqual(b'echo2', content2)
        self.assertIsNone(err3)
        self.assertEqual(b'echo3', content3)

    def test_send_requests(self, m):
        m.get('http://localhost:1234/echo?echo={"test":1}', text='{"test":1}')
        m.get('http://localhost:1235/echo?echo={"test":2}', text='{"test":2}')
        m.get('http://localhost:1236/echo?echo={"test":3}', text='{"test":3}')

        all_machines = [
            'http://localhost:1234/echo?echo={"test":1}',
            'http://localhost:1235/echo?echo={"test":2}',
            'http://localhost:1236/echo?echo={"test":3}',
        ]

        err, results = util.send_requests(all_machines, '', '', 'GET')
        self.assertIsNone(err)

        err1, content1 = results['http://localhost:1234/echo?echo={"test":1}']
        err2, content2 = results['http://localhost:1235/echo?echo={"test":2}']
        err3, content3 = results['http://localhost:1236/echo?echo={"test":3}']
        self.assertIsNone(err1)
        self.assertEqual({"test": 1}, content1)
        self.assertIsNone(err2)
        self.assertEqual({"test": 2}, content2)
        self.assertIsNone(err3)
        self.assertEqual({"test": 3}, content3)

    def test_send_requests_with_different_params(self, m):
        m.post('http://localhost:1234/echo', text='{"test":1}')
        m.post('http://localhost:1235/echo', text='{"test":2}')
        m.post('http://localhost:1236/echo', text='{"test":3}')

        the_url_data = {
            'http://localhost:1234/echo': '{"test":1}',
            'http://localhost:1235/echo': '{"test":2}',
            'http://localhost:1236/echo': '{"test":3}',
        }

        err, results = util.send_requests_with_different_params(the_url_data)
        self.assertIsNone(err)

        err1, content1 = results['http://localhost:1234/echo']
        err2, content2 = results['http://localhost:1235/echo']
        err3, content3 = results['http://localhost:1236/echo']
        self.assertIsNone(err1)
        self.assertEqual({"test": 1}, content1)
        self.assertIsNone(err2)
        self.assertEqual({"test": 2}, content2)
        self.assertIsNone(err3)
        self.assertEqual({"test": 3}, content3)
