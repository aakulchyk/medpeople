from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Attachment
from django.urls import reverse

from django.http import HttpResponse

def done(self):
    return HttpResponse('Done!')

class UploadView(FormView):
    template_name = 'form.html'
    form_class = UploadForm
    success_url = '/done'
    
    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            Attachment.objects.create(file=each)
        return super(UploadView, self).form_valid(form)


