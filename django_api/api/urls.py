from django.conf.urls import url

from . import views

app_name = "api"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^news/(?P<uf>[\w-]{2})/$', views.News.as_view(), name='news'),
    # url(r'^news/(?P<state>[\w-]{2})/comment/$', views.Comment, name='create_comment')
]
