from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import States
from .signals import log_signal

import os
import threading
import time
# Create your tests here.


def create_state(uf, state):
    return States.objects.create(uf=uf, state=state)


class TestIndexView(TestCase):

    def test_views_without_states(self):
        response = self.client.get(reverse('api:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['states']), 0)
        self.assertTemplateUsed(response, 'api/home.html')
        self.assertContains(response, 'No state availbles')

    def test_views_with_states(self):
        create_state('rj', 'Rio de janeiro')
        create_state('sp', 'Sao Paulo')
        response = self.client.get(reverse('api:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['states']), 2)
        self.assertTemplateUsed(response, 'api/home.html')
        self.assertContains(response, 'Sao Paulo')


class TesteNewsView(TestCase):

    def test_news_with_states(self):
        create_state('RJ', 'Rio de Janeiro')
        response = self.client.get(reverse('api:news', kwargs={'uf': 'rj'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        self.assertContains(response, 'Noticias para Rio de Janeiro')

    def test_news_without_states(self):
        response = self.client.get(reverse('api:news', kwargs={'uf': 'rj'}))
        self.assertEqual(response.status_code, 404)


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
