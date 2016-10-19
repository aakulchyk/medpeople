from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Attachment
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .ocr import OcrThread
from .analyze import AnalyzeThread

from django.http import FileResponse

pending_pdfs_list = []

@login_required
def done(request):
    l = pending_pdfs_list[:]
    print('list!' + str(l))
    ocrThread = OcrThread(pending_pdfs_list)
    ocrThread.start()
    
    template_name = 'upload/done.html'
    initial = {'file_list_string' : ','.join(l)}    
    return render(request, template_name, initial)
   
@login_required  
def pdf_view(request, document_id):
    return FileResponse(open(document_id, 'rb'), content_type='application/pdf')

@login_required
def reindex_files(request):
    analyzeThread = AnalyzeThread('')
    analyzeThread.start()
    return HttpResponseRedirect(reverse('upload:index'));

class UploadView(LoginRequiredMixin, FormView):
    template_name = 'upload/form.html'
    form_class = UploadForm
    success_url = 'done/'
    
    def get(self, request, *args, **kwargs):
        self.request = request
        objects = Attachment.objects.filter(user = request.user)
        return render(request, self.template_name, {'form': self.form_class, 'document_list' : objects.order_by('-visit_date')[:20]})
    
    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            file_path = 'attachments/' + each.name
            # if no documents with this name
            if (not Attachment.objects.filter(file_attached=file_path)):
                Attachment.objects.create(file_attached=each, user = self.request.user)
                pending_pdfs_list.append(file_path)
            else:
                print(file_path + ' exists!')

        return super(UploadView, self).form_valid(form)
