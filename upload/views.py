from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Attachment
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse

from .ocrtest import OcrThread

from django.http import FileResponse

pending_pdfs_list = []

def done(self):
    l = pending_pdfs_list[:]
    print('list!' + str(l))
    ocrThread = OcrThread(pending_pdfs_list)
    ocrThread.start()    
    return HttpResponse(','.join(l) + 'Uploaded and started to process!')
    
def pdf_view(request, document_id):
    print('PDF_ViEW!!!!!   ')
    return FileResponse(open(document_id, 'rb'), content_type='application/pdf')
    '''
    with open(document_id, 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed
    '''
class UploadView(FormView):
    template_name = 'form.html'
    form_class = UploadForm
    success_url = 'done/'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class, 'document_list' : Attachment.objects.all()})
    
    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            Attachment.objects.create(file_attached=each)
            pending_pdfs_list.append('attachments/' + each.name)

        return super(UploadView, self).form_valid(form)
        
    


