from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comentar', max_length=200)
