from django.views.generic.edit import FormView
from .forms import UploadForm
from .models import Document
from dictionary.models import MedicalTerm
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

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
    initial = {'file_list_string': ','.join(l)}
    return render(request, template_name, initial)


@login_required
def pdf_view(request, document_id):
    return FileResponse(open(document_id, 'rb'), content_type='application/pdf')


@login_required
def reindex_files(request):
    analyzeThread = AnalyzeThread('')
    analyzeThread.start()
    return HttpResponseRedirect(reverse('upload:index'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('upload:index'))


class UploadView(LoginRequiredMixin, FormView):
    template_name = 'upload/form.html'
    form_class = UploadForm
    success_url = 'done/'

    def strip_filters(self, filter_names):
        filters = []
        for f in filter_names:
            for found in MedicalTerm.objects.filter(name=f):
                filters.append(found)
        if not filters:
            filters.append(MedicalTerm())
        return filters

    def get(self, request, *args, **kwargs):
        self.request = request
        query = Document.objects.filter(user=request.user)
        if request.GET.get("filters"):
            filters = self.strip_filters(request.GET["filters"].split(','))
            for f in filters:
                query = query.filter(tags=f)

        docs = query.order_by('-visit_date')[:20]
        request_dict = {'form': self.form_class, 'document_list': docs}
        return render(request, self.template_name, request_dict)

    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            file_path = 'attachments/' + each.name
            # if no documents with this name
            o = Document.objects
            if (not o.filter(file_attached=file_path)):
                o.create(file_attached=each, user=self.request.user)
                pending_pdfs_list.append(file_path)
            else:
                print(file_path + ' exists!')

        return super(UploadView, self).form_valid(form)
