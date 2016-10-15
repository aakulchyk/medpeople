from django.conf.urls import url, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'docs', views.DocumentListViewSet)


# Wire up our API using automatic URL routing.

urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^(?P<document_id>pdfs/\w+\.pdf)/$', views.pdf_view_api, name='pdf_view_api'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
