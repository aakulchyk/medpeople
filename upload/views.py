from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Attachment
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse

from .ocrtest import OcrThread

from django.http import FileResponse

pending_pdfs_list = []

def done(request):
    l = pending_pdfs_list[:]
    print('list!' + str(l))
    ocrThread = OcrThread(pending_pdfs_list)
    ocrThread.start()
    
    template_name = 'done.html'
    initial = {'file_list_string' : ','.join(l)}    
    return render(request, template_name, initial)
    
def pdf_view(request, document_id):
    return FileResponse(open(document_id, 'rb'), content_type='application/pdf')

class UploadView(FormView):
    template_name = 'form.html'
    form_class = UploadForm
    success_url = 'done/'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class, 'document_list' : Attachment.objects.order_by('-visit_date')[:20]})
    
    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            file_path = 'attachments/' + each.name
            # if no documents with this name
            if (not Attachment.objects.filter(file_attached=file_path)):
                Attachment.objects.create(file_attached=each)
                pending_pdfs_list.append(file_path)
            else:
                print(file_path + ' exists!')

        return super(UploadView, self).form_valid(form)
        
    


