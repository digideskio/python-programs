import httpretty
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from ..models import States, Comment


def create_state(uf, state, comment=None):
    if comment:
        com = Comment(comment=comment)
        com.save()
        state = States.objects.create(uf=uf, state=state)
        state.comment.add(com)
        state.save()
        return
    return States.objects.create(uf=uf, state=state)


def create_comment(uf, comment):
    com = Comment(comment=comment)
    com.save()
    state = get_object_or_404(States, uf=uf)
    state.comment.add(com)
    return state.save()


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
        response = self.client.get(reverse('api:news', kwargs={'uf': 'RJ'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        self.assertContains(response, 'Noticias para Rio de Janeiro')
        self.assertContains(response, 'Comentario:')

    def test_news_without_states(self):
        response = self.client.get(reverse('api:news', kwargs={'uf': 'rj'}))
        self.assertEqual(response.status_code, 404)

    @httpretty.activate
    def test_news_capi_down(self):
        httpretty.register_uri(httpretty.GET,
                               "http://c.api.globo.com/news/rj.json",
                               status=404)
        create_state('RJ', 'Rio de Janeiro')
        response = self.client.get(reverse('api:news', kwargs={'uf': 'RJ'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        self.assertContains(response, 'Not Found, status: 404')

    def test_views_with_comments(self):
        create_state('RJ', 'Rio de Janeiro', 'comentario')
        state = get_object_or_404(States, pk='RJ')
        self.assertEqual(state.uf, 'RJ')
        self.assertEqual(state.state, 'Rio de Janeiro')
        self.assertEqual(state.comment.values()[0]['comment'], 'comentario')
        response = self.client.get(reverse('api:news', kwargs={'uf': 'rj'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        self.assertContains(response, 'Noticias para Rio de Janeiro')
        self.assertContains(response, 'comentario')
        self.assertContains(response, 'Comentarios:')


class TesteCreateCommentView(TestCase):

    def test_create_comment_ok(self):
        create_state('RJ', 'Rio de Janeiro')
        response = self.client.post(
            reverse('api:create_comment', kwargs={'uf': 'RJ'}),
            {'comment': 'test'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        state = get_object_or_404(States, pk='RJ')
        self.assertEqual(state.uf, 'RJ')
        self.assertEqual(state.state, 'Rio de Janeiro')
        self.assertEqual(state.comment.values()[0]['comment'], 'test')

    def test_create_comment_nok(self):
        response = self.client.post(
            reverse('api:create_comment', kwargs={'uf': 'RJ'}),
            {'comment': 'test'},
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_create_comment_multiple_comments(self):
        create_state('RJ', 'Rio de Janeiro', 'test2')
        response = self.client.post(
            reverse('api:create_comment', kwargs={'uf': 'RJ'}),
            {'comment': 'test'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        state = get_object_or_404(States, pk='RJ')
        self.assertEqual(state.uf, 'RJ')
        self.assertEqual(state.state, 'Rio de Janeiro')
        self.assertEqual(len(state.comment.values()), 2)
        self.assertEqual(state.comment.values()[0]['comment'], 'test2')
        self.assertEqual(state.comment.values()[1]['comment'], 'test')


class TestRemoveCommentView(TestCase):

    def test_remove_comment_ok(self):
        create_state('RJ', 'Rio de Janeiro', 'comment')
        response = self.client.get(
            reverse('api:delete_comment', kwargs={'uf': 'RJ', 'id': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        state = get_object_or_404(States, pk='RJ')
        self.assertEqual(state.uf, 'RJ')
        self.assertEqual(state.state, 'Rio de Janeiro')
        self.assertEqual(len(state.comment.values()), 0)

    def test_remove_comment_nok(self):
        response = self.client.get(
            reverse('api:delete_comment', kwargs={'uf': 'RJ', 'id': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 404)

    def test_remove_comment_multiple_comments(self):
        create_state('RJ', 'Rio de Janeiro', 'comment')
        create_comment('RJ', 'comment2')
        create_comment('RJ', 'comment3')
        old = get_object_or_404(States, pk='RJ')
        self.assertEqual(len(old.comment.values()), 3)
        response = self.client.get(
            reverse('api:delete_comment', kwargs={'uf': 'RJ', 'id': 2}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/news.html')
        new = get_object_or_404(States, pk='RJ')
        self.assertEqual(len(new.comment.values()), 2)
        self.assertEqual(new.comment.values()[0]['comment'], 'comment')
        self.assertEqual(new.comment.values()[1]['comment'], 'comment3')

    def test_remove_comment_invalid_id(self):
        create_state('RJ', 'Rio de Janeiro', 'comment')
        old = get_object_or_404(States, pk='RJ')
        self.assertEqual(len(old.comment.values()), 1)
        response = self.client.get(
            reverse('api:delete_comment', kwargs={'uf': 'RJ', 'id': 2}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        new = get_object_or_404(States, pk='RJ')
        self.assertEqual(len(new.comment.values()), 1)
        self.assertEqual(new.comment.values()[0]['comment'], 'comment')
