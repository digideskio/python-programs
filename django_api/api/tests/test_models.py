from django.test import TestCase

from ..models import Comment, States


class TestModelsComment(TestCase):

    def test_comment_str(self):
        c_obj = Comment(comment='teste')
        self.assertEqual(str(c_obj), 'teste')


class TestModelsStates(TestCase):

    def test_states_str(self):
        s_obj = States(uf='RJ', state='Rio de Janeiro')
        self.assertEqual(str(s_obj), 'RJ')
