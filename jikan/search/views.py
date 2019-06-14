
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

# @login_required
# def add_comment_to_paper(request):
#     pid = request.GET['pk']
#     paper = get_object_or_404(Paper, pk=pid)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = paper
#             comment.save()
#             return redirect('paper_detail', pk=paper.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'comment.html', {'form': form})


class HomePageView(ListView):
    model = Paper
    template_name = 'home.html'


class JournalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Paper.objects.none()

        qs = Journal.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q).distinct().order_by('name')

        return qs



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
def paper_update(request, pk):

    # Either render only the modal content, or a full standalone page
    if request.is_ajax():
        template_name = 'add_paper.html'
    object = get_object_or_404(Artist, pk)
    if request.method == 'POST':
        form = PaperForm(instance=object, data=request.POST)
        if form.is_valid():
            form.save()
    # if is_ajax(), we just return the validated form, so the modal will close
    else:
        form = PaperForm(instance=object)
    return render(request, template_name, {
        'object': object,
        'form': form,
        })
