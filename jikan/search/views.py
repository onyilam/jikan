from django.shortcuts import render
from django.db.models import Q
from .models import Paper

def searchpaper(request):
    #search paper in the Paper model, if it doesn't exist, pull from Google Scholar and add to the Paper model
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



def add_paper(request):
    #user paste the exact title of the paper in the search bar. if it doesn't exist, fetch the info from Google scholar
    # and add to the Papers model
    query = request.GET.get('q')
    paper_search, _ = Paper.objects.update_or_create(title= query.decode('utf-8').lower())


