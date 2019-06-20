
from django.views.generic import ListView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Paper, Preference, Journal, Author
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from .forms import CommentForm, PaperForm
from django import forms
from dal import autocomplete
import json

class HomePageView(ListView):
    model = Paper
    template_name = 'home.html'


def searchpaper(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton= request.GET.get('submit')
        page = request.GET.get('page', 1)

        if query is not None:
            lookups = Q(title__icontains=query)
            results_queryset = Paper.objects.filter(lookups).distinct().order_by('-likes', '-n_citation')
            paginator = Paginator(results_queryset , 20)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            context = {'results': results,
                       'submitbutton': submitbutton,
                       }
            return render(request, 'home.html', context)
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')

def get_recommendation(request):
    pid = request.GET['pk']
    rec_values = Paper.objects.get(pk=pid)
    values_list = rec_values.title
    rec_journal = rec_values.journal
    data = {'rec_list': values_list, 'rec_journal': model_to_dict(rec_journal)['name']}
    return JsonResponse(data)

def paper_detail(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    return render(request, 'paper_detail.html', {'paper': paper})

@login_required
def add_paper(request):
    if request.method == "POST":
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.save()
            return redirect('paper_detail', pk=paper.pk)
    else:
        form = PaperForm()
    return render(request, 'add_paper.html', {'form': form})

@login_required
def like_paper(request):
   # if request.method == "GET":
    pid = request.GET['pk']
    paper = Paper.objects.get(pk=pid)
    likes = paper.likes + 1
    paper.likes = likes
    paper.save()
    data = {'likes': paper.likes}
    return JsonResponse(data)

def autocompletePaper(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        search_qs = Paper.objects.filter(title__icontains=q).order_by('title')
        results = []
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def edit_paper(request, pk=None):
    template_name = 'edit_paper_modal.html'
    if request.POST:
        print('trying to post')
        paper = get_object_or_404(Paper, pk = pk)
        form = PaperForm(instance=paper, data=request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
        return render(request, 'paper_detail.html', {'paper': paper})
    else:
        pk = request.GET.get('pk')
        object = get_object_or_404(Paper, pk = pk)
        form = PaperForm(instance=object)
        if object:
            print('object exists', pk, request.method)
        return render(request, template_name, {
            'object': object,
            'form': form,
            })



#
# class JournalAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         #if not self.request.user.is_authenticated():
#         #    return Paper.objects.none()
#
#         qs = Journal.objects.all()
#
#         if self.q:
#             qs = qs.filter(name__icontains=self.q).distinct().order_by('name')
#
#         return qs
