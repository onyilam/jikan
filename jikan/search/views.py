
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
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

def paperpreference(request, pid, userpreference):
    if request.method == "POST":

        eachpaper = get_object_or_404(Paper, id=pid)

        obj = ''

        valueobj = ''

        try:
            obj = Preference.objects.get(user=request.user, post=eachpaper)
            valueobj = obj.value  # value of userpreference
            valueobj = int(valueobj)
            userpreference = int(userpreference)

            if valueobj != userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.post = eachpaper
                upref.value = userpreference

                if userpreference == 1 and valueobj != 1:
                    eachpaper.likes += 1
                    eachpaper.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    eachpaper.dislikes += 1
                    eachpaper.likes -= 1

                upref.save()

                eachpaper.save()

                context = {'eachpaper': eachpaper,
                           'paperid': pid}

                return render(request, 'home.html', context)


        except Preference.DoesNotExist:
            upref = Preference()

            upref.user = request.user

            upref.post = eachpaper

            upref.value = userpreference

            userpreference = int(userpreference)

            if userpreference == 1:
                eachpaper.likes += 1
            elif userpreference == 2:
                eachpaper.dislikes += 1

            upref.save()

            eachpaper.save()

            context = {'eachpost': eachpaper,
                       'postid': pid}

            return render(request, 'home.html', context)

    else:
        eachpaper = get_object_or_404(Paper, id=pid)
        context = {'eachpaper': eachpaper,
                   'pid': pid}

    return render(request, 'home.html', context)


class HomePageView(ListView):
    model = Paper
    template_name = 'home.html'


