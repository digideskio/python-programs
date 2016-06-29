from django.test import TestCase

from ..forms import CommentForm


class TestForms(TestCase):

    def test_form_data_valid(self):
        form_data = {'comment': 'something'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_data_not_valid(self):
        a = ''
        for i in range(204):
            a += 'a'
        form_data = {'comment': a}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
