from django.conf.urls import url
from . import views

app_name = 'dictionary'

urlpatterns = [
    # ex: /upload/
    url(r'^$', views.dict_index, name='index'),
    # ex: /upload/done/
    url(r'^fill/$', views.fill, name='fill'),
]
