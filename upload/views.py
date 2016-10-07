from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Attachment
from django.urls import reverse

from django.http import HttpResponse

from .ocrtest import OcrThread

pending_pdfs_list = []

def done(self):
    print('list!' + str(pending_pdfs_list))
    ocrThread = OcrThread(pending_pdfs_list)
    ocrThread.start()    
    return HttpResponse(','.join(pending_pdfs_list) + 'Uploaded and started to process!')

class UploadView(FormView):
    template_name = 'form.html'
    form_class = UploadForm
    success_url = 'done'
    
    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            Attachment.objects.create(file=each)
            pending_pdfs_list.append(each.name)

        return super(UploadView, self).form_valid(form)


