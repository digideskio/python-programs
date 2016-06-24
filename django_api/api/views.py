import json
import requests

from django.views import generic


class IndexView(generic.ListView):
    states = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
              "PR", "PB", "PA", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SE", "SP", "TO"
              ]
    template_name = 'api/home.html'
    context_object_name = 'states'

    def get_queryset(self):
        return self.states


class News(generic.TemplateView):
    template_name = 'api/news.html'

    def get_context_data(self, **kwargs):
        state = self.kwargs['state']
        req = requests.get('http://c.api.globo.com/news/{}.json'.format(state.lower()))
        if req.status_code != 200:
            return {
                'error_message': 'Not Found, status: {}'.format(req.status_code)
            }
        return {
            'news': json.loads(req.text),
            'state': state
        }
