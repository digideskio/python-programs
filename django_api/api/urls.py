from django.conf.urls import url

from . import views

app_name = "api"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^news/(?P<uf>[\w-]{2})/$', views.News.as_view(), name='news'),
    url(r'^news/(?P<uf>[\w-]{2})/comment/$',
        views.CreateCommentView.as_view(), name='create_comment'),
    url(r'^news/(?P<uf>[\w-]{2})/(?P<id>[\d+]+)/comment/$',
        views.RemoveCommentView.as_view(), name='delete_comment')
]
