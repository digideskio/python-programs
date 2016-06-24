from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import States
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
