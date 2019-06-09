
from django.views.generic import ListView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Paper, Preference
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .forms import CommentForm, PaperForm

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
        form = PaperForm(request.POST)
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

@login_required
def add_comment_to_paper(request):
    pid = request.GET['pk']
    paper = get_object_or_404(Paper, pk=pid)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = paper
            comment.save()
            return redirect('paper_detail', pk=paper.pk)
    else:
        form = CommentForm()
    return render(request, 'comment.html', {'form': form})

# @login_required
# def dislike_paper(request):
#     # if request.method == "GET":
#     pid = request.GET['pk']
#     paper = Paper.objects.get(pk=pid)
#     dislikes = paper.dislikes + 1
#     paper.dislikes = dislikes
#     paper.save()
#     data = {'dislikes': paper.dislikes}
#     return JsonResponse(data)


class HomePageView(ListView):
    model = Paper
    template_name = 'home.html'

class PaperCreateView(CreateView):
    model = Paper
    template_name =  'add_paper.html'
    fields = ('title', 'abstract', 'year')
