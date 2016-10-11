from os import listdir, remove
from os.path import join
from django.conf import settings
from .models import MedicalTerm
from . import urls

def fill_model_with_list(terms_list):
    for term in terms_list:
        if not MedicalTerm.objects.filter(name=term):
            print('new term ' + term)
            t = MedicalTerm(name=term)
            t.save()
        else:
            print('term %s exists' % term)
        
    print('Import is finished!')

def import_terms_from_data_dir():
    print('fill medical dictionary with new terms')
    path = join(settings.BASE_DIR, urls.app_name, 'data')
    print('path: ' + path)
    files = listdir(path)
    while files:
        filename = files.pop(0)
        print('import terms from file ' + filename)
        with open(join(path,filename), 'r') as f:
            text = f.read()
        fill_model_with_list(text.split(','))
        remove(join(path,filename))
        
    
