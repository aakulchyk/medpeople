#from django.contrib.auth.models import User, Group
from dictionary.models import MedicalTerm
from upload.models import Attachment

from rest_framework import serializers


class DocumentListSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Attachment
        fields = ('file_attached','visit_date', 'tags')

'''
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
'''
