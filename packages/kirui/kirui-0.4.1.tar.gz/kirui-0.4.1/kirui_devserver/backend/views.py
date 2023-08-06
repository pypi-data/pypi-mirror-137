import datetime
import time

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.template.loader import get_template
from django.views import View

from django_kirui.utils.paginator import Paginator
from kirui_devserver.backend.forms import SampleForm, FilterForm
from kirui_devserver.backend.models import Activity


def index(request):
    return render(request, 'xml/index.html')


class FormView(View):
    def get(self, request):
        form = SampleForm(request.POST or None, request.FILES or None)
        return render(request, 'xml/form.html', context={'form': form})

    def post(self, request):
        # print(request.POST, request.FILES)
        form = SampleForm(request.POST or None, request.FILES or None, instance=Activity.objects.first())
        if form.is_valid():
            resp = HttpResponseRedirect('/backend/index/')
            resp.status_code = 340
            return resp
        else:
            data = get_template('xml/form_data.html').render(context={'form': form}, request=request, to='js_template', include_root=False)
            resp = HttpResponse(data)
            resp.status_code = 403
            return resp


def modal(request):
    form = SampleForm(request.POST or None, request.FILES or None)
    form.now = datetime.datetime.now()
    if form.is_valid():
        return HttpResponse('OK')

    data = get_template('xml/modal.html').render(context={'form': form}, request=request, to='js_template')
    resp = HttpResponse(data)
    if form.is_valid():
        resp.status_code = 200
    else:
        resp.status_code = 403

    return resp


def table(request):
    data = []
    for row in range(1, 200):
        data.append({'first': f'{row}.1', 'second': f'{row}.2'})

    paginate_to = int(request.GET.get('paginate_to', 1))
    p = Paginator(data, 30)
    page = p.page(paginate_to)

    if request.GET.get('paginate_to', None):
        data = get_template('xml/table_data.html').render(context={'page': page}, request=request, to='js_template', include_root=False)
        return HttpResponse(data)
    else:
        return render(request, 'xml/table.html', context={'page': page})


class FilteredTable(View):
    def dispatch(self, request, *args, **kwargs):
        data = []
        for row in range(1, 20):
            data.append({'first': f'{row}.1', 'second': f'{row}.2'})
        self.data = data
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = FilterForm()
        p = Paginator(self.data, 4)
        page = p.page(1)
        return render(request, 'xml/filtered_table.html', context={'form': form, 'page': page})

    def post(self, request):
        form = FilterForm(request.POST)
        if form.is_valid():
            data = [row for row in self.data if row['first'].startswith(form.cleaned_data['field'])]
        p = Paginator(data, 4)

        paginate_to = int(request.GET.get('paginate_to', 1))
        page = p.page(paginate_to)
        data = get_template('xml/filtered_table_data.html').render(context={'form': form, 'page': page}, request=request, to='js_template', include_root=False)
        return HttpResponse(data)
