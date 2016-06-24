import json
import requests

from django.views import generic
from django.shortcuts import get_object_or_404

from .models import States


class IndexView(generic.ListView):
    template_name = 'api/home.html'
    context_object_name = 'states'

    def get_queryset(self):
        return States.objects.all().order_by('uf')


class News(generic.TemplateView):
    template_name = 'api/news.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['uf']
        state = get_object_or_404(States, pk=pk.upper())
        req = requests.get('http://c.api.globo.com/news/{}.json'.format(state.uf.lower()))
        if req.status_code != 200:
            return {
                'error_message': 'Not Found, status: {}'.format(req.status_code)
            }
        return {
            'news': json.loads(req.text),
            'state': state
        }
