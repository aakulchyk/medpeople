from django.conf.urls import url

from . import views

app_name = 'upload'
urlpatterns = [
    # ex: /upload/
    url(r'^$', views.UploadView.as_view(), name='index'),
    # ex: /upload/done/
    url(r'^done/$', views.done, name='done'),
    url(r'^(?P<document_id>attachments/\w+\.pdf)/$', views.pdf_view, name='view'),
]
