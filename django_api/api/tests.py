from django.test import TestCase
from django.core.urlresolvers import reverse

# Create your tests here.


class TestIndexView(TestCase):

    def test_views_ok(self):
        response = self.client.get(reverse('api:index'))
        self.assertEqual(response.status_code, 200)
        expected_states = ["AC", "AL", "AP", "AM", "BA", "CE", "DF",
                           "ES", "GO", "MA", "MT", "MS", "MG", "PR",
                           "PB", "PA", "PE", "PI", "RJ", "RN", "RS",
                           "RO", "RR", "SC", "SE", "SP", "TO"
                           ]
        self.assertEqual(response.context['states'], expected_states)
        self.assertTemplateUsed(response, 'api/home.html')


class TesteNewsView(TestCase):

    def test_news_ok(self):
        response = self.client.get(reverse('api:news', kwargs={'state': 'rj'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        self.assertContains(response, 'Noticias para rj')

    def test_news_invalid_state(self):
        response = self.client.get(reverse('api:news', kwargs={'state': 're'}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'api/news.html')
        self.assertContains(response, 'Not Found, status: 404')
