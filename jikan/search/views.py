from django.shortcuts import render
from django.db.models import Q
from .models import Paper
import json


def searchpaper(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(abstract__icontains=query)
            results = Paper.objects.filter(lookups).distinct()
            context = {'results': results,
                      'submitbutton': submitbutton}

            return render(request, 'home.html', context)
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')

def get_recommendation(request):

    rec_list = [1,3,4]
    context = {
        'rec_list': rec_list
    }

    return render(request, 'home.html', context)

