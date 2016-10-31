#from django.contrib.auth.models import User, Group
from dictionary.models import MedicalTerm
from upload.models import Document

from rest_framework import serializers


class DocumentListSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Document
        fields = ('file_attached','visit_date', 'tags', 'user')

'''
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
'''
