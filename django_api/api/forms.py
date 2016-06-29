from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comentario', max_length=200)
