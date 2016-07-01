import json
import requests

from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import JsonResponse

from .models import States, Comment
from . import signals
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = 'api/home.html'
    context_object_name = 'states'

    def get_queryset(self):
        return States.objects.all().order_by('uf')


class News(generic.TemplateView):
    template_name = 'api/news.html'

    def get_context_data(self, **kwargs):
        # import pdb
        # pdb.set_trace()
        pk = self.kwargs['uf']
        signals.log_signal.send(sender=States, requests=self.request,
                                state=pk, file='log')
        state = get_object_or_404(States, pk=pk.upper())
        req = requests.get('http://c.api.globo.com/news/{}.json'.format(state.uf.lower()))
        comments = state.comment.values()
        if req.status_code != 200:
            return {
                'error_message': 'Not Found, status: {}'.format(req.status_code),
                'state': state
            }
        news = json.loads(req.text)
        return {
            'news': news,
            'state': state,
            'form': CommentForm(),
            'comments': comments
        }


class CreateCommentView(generic.View):
    template_name = 'api/news.html'

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        uf = kwargs['uf']
        if form.is_valid():
            state = get_object_or_404(States, pk=uf)
            comment = Comment(comment=form.cleaned_data['comment'])
            comment.save()
            state.comment.add(comment)
            state.save()

        return redirect(reverse('api:news', kwargs={'uf': uf.lower()}))


class RemoveCommentView(generic.View):

    def get(self, request, *args, **kwargs):
        uf = self.kwargs['uf']
        comment_id = self.kwargs['id']
        state = get_object_or_404(States, pk=uf)
        state.comment.remove(comment_id)
        return redirect(reverse('api:news', kwargs={'uf': uf.lower()}))


class GetStatesView(generic.View):

    def get(self, request, *args, **kwargs):
        data = serializers.serialize(
            'json', States.objects.all().order_by('uf'), fields=('uf', 'state',))
        return JsonResponse(data, safe=False)
