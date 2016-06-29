from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from ..models import States
import os
import threading
import time

from ..signals import log_signal
# Create your tests here.


class TestSignals(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.request = RequestFactory()
        self.file = 'test_file'

    def tearDown(self):
        if os.path.exists(self.file):
            os.remove(self.file)

    def test_signal(self):
        requests = self.request.get('/fake-path')
        requests.user = self.user
        log_signal.send(sender=States, state='sp', file=self.file, requests=requests)
        expect_data = 'path: {}       username: {}       state: {}\n'.format(
            requests.path, requests.user.username, 'SP')
        while threading.active_count() != 1:
            time.sleep(0.5)
        with open(self.file, 'r') as fd:
            data = fd.read()
            self.assertEqual(data, expect_data)

    def test_signal_append(self):
        requests = self.request.get('/fake-path')
        requests.user = self.user
        log_signal.send(sender=States, state='sp', file=self.file, requests=requests)
        log_signal.send(sender=States, state='rj', file=self.file, requests=requests)
        expect_data = 'path: {}       username: {}       state: {}\n'.format(
            requests.path, requests.user.username, 'SP')
        expect_data += 'path: {}       username: {}       state: {}\n'.format(
            requests.path, requests.user.username, 'RJ')
        while threading.active_count() != 1:
            time.sleep(0.5)
        with open(self.file, 'r') as fd:
            data = fd.read()
            self.assertEqual(data, expect_data)

    def test_signal_wrong_sender(self):
        requests = self.request.get('/fake-path')
        requests.user = self.user
        log_signal.send(sender=None, state='sp', file=self.file, requests=requests)
        while threading.active_count() != 1:
            time.sleep(0.5)
        self.assertFalse(os.path.exists(self.file))
