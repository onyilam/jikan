
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Paper, Preference
from django.http import JsonResponse
from django.forms.models import model_to_dict



def searchpaper(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query)
            results = Paper.objects.filter(lookups).distinct()
            context = {'results': results,
                      'submitbutton': submitbutton}
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
def dislike_paper(request):
    # if request.method == "GET":
    pid = request.GET['pk']
    paper = Paper.objects.get(pk=pid)
    dislikes = paper.dislikes + 1
    paper.dislikes = dislikes
    paper.save()
    data = {'dislikes': paper.dislikes}
    return JsonResponse(data)


class HomePageView(ListView):
    model = Paper
    template_name = 'home.html'


