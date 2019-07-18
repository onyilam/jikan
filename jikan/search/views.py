
from django.views.generic import ListView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Paper, Preference, Journal, Author, CustomUser, PaperEvent, ViewerComment, EventReaction
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from .forms import PaperForm, EditPaperForm, EventForm
from users.forms import CustomUserChangeForm
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
            return render(request, 'search_result.html', context)
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
    can_edit=False
    events = PaperEvent.objects.filter(paper=paper).order_by("-date")
    if request.user==paper.created_by:
         can_edit=True
    context = {'paper': paper, 'can_edit': can_edit, 'events': events}
    return render(request, 'paper_detail.html', context)

@login_required
def add_paper(request):
    if request.method == "POST":
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.created_by = request.user
            paper.save()
            return redirect('paper_detail', pk=paper.pk)
    else:
        form = PaperForm()
    return render(request, 'add_paper.html', {'form': form})

@login_required(login_url='/accounts/login/')
def like_paper(request):
    # if request.method == "GET":
    pid = request.GET['pk']
    user = request.user
    paper = Paper.objects.get(pk=pid)
    pref, _ = Preference.objects.get_or_create(user=user, paper=paper)
    # if there is no record of the user on the paper, incrrement the pref and likes of the paper
    if not pref.value:
        likes = paper.likes + 1
        value = 1
    # maximum allowable likes is 10 per person.
    elif pref.value < 10:
        likes = paper.likes + 1
        value = pref.value + 1
    else:
        likes = paper.likes 
        value = pref.value 
    pref.value = value  
    pref.save()
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
def load_paper(request):
    pk = request.GET.get('pk')
    print('pk', pk, request.method)
    object = get_object_or_404(Paper, pk = pk)
    form = PaperForm(instance=object)
    return render(request, 'edit_paper_modal.html', {
        'object': object,
        'pk': pk,
        'form': form,
        })

@login_required
def edit_paper(request, pk=None):
    template_name = 'edit_paper_modal.html'
    paper = get_object_or_404(Paper, pk = pk)
    can_edit=False
    if request.user==paper.created_by:
         can_edit=True
    if request.POST:
        form = PaperForm(instance=paper, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    context = {'paper': paper, 'can_edit': can_edit}
    return render(request, 'paper_detail.html', context)

def view_user(request, pk):
    creator = CustomUser.objects.get(pk=pk)
    can_edit=False
    print(request.user, creator)
    if request.user==creator:
         can_edit=True
    return render(request, 'profile.html', {"creator": creator, "can_edit": can_edit})
    #url = request.user.get_profile().url

@login_required
def load_user(request):
    pk = request.GET.get('pk')
    object = get_object_or_404(CustomUser, pk = pk)
    form = CustomUserChangeForm(instance=object)
    return render(request, 'edit_user_modal.html', {
        'object': object,
        'pk': pk,
        'form': form,
        })

@login_required
def edit_user(request, pk=None):
    template_name = 'edit_user_modal.html'
    user = get_object_or_404(CustomUser, pk = pk)
    can_edit=False
    if request.user==user:
         can_edit=True
    if request.POST:
        form = CustomUserChangeForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            print('saved')
    context = {'user': user, 'can_edit': can_edit}
    return redirect('view_user', pk)

@login_required
def remove_paper(request, pk=None):
    print('remove paper pk', pk)
    paper = get_object_or_404(Paper, pk = pk)
    paper.delete()
    return render(request, 'paper_removed.html')

@login_required
def add_event(request):
    """
    callling the add event form from the paper_detail.html
    """
    if request.method == 'GET':
        print('add event')
        pk = request.GET.get('pk')
        paper = Paper.objects.get(pk=pk)
        pe = PaperEvent()
        pe.paper = paper
        form = EventForm(instance=pe)
    return render(request, 'add_event_modal.html', {
            'form': form,
            'object': pe,
            'pk': pk,
            })

@login_required
def post_event(request, pk=None):
    """
    actually saving the event in the database. calls from the modal.html
    """
    event_pk = request.POST.get('event_pk')
    print('post event_pk', event_pk)
    if request.method == "POST":
        p=Paper.objects.get(pk=pk)
        if event_pk=="None":
            # add new event
            print('no event, new form')
            form = EventForm(initial={'paper':p}, data=request.POST, files=request.FILES)
        elif 'save_edits' in request.POST :
            #save edits to existing event
            print("there is an event already", event_pk)
            pe = PaperEvent.objects.get(pk=event_pk)
            form = EventForm(instance=pe, data=request.POST, files=request.FILES)
        elif 'deleteBtn' in request.POST:
            print("remove event")


        if form.is_valid():
            event = form.save(commit=False)
            event.paper = p
            event.save()
            return redirect('paper_detail', pk=pk)

@login_required
def edit_event(request, pk=None):
    event_pk = request.GET.get('pk')
    print('about to edit pk', event_pk, request.method)
    object = get_object_or_404(PaperEvent, pk = event_pk)
    form = EventForm(instance=object)
    #get the pk of the paper
    pk = object.paper.pk
    return render(request, 'edit_event_modal.html', {
        'object': object,
        'pk': pk,
        'form': form,
        })

@login_required
def remove_event(request, pk=None):
    print('remove pk', pk)
    pe = get_object_or_404(PaperEvent, pk = pk)
    paper_pk = pe.paper.pk
    pe.delete()
    return redirect('paper_detail', pk=paper_pk)

@login_required
def add_comment_to_event(request, event_pk=None):
    print('add comment to event', event_pk)
    pe = get_object_or_404(PaperEvent, pk = event_pk)
    paper_pk = pe.paper.pk
    if request.method == 'GET':
        comment_text = request.GET.get('comment')
        if comment_text is not None:
            vc = ViewerComment()
            vc.text = comment_text
            vc.commenter = request.user
            vc.event = pe
            vc.save()
        print('saved comment')

    return redirect('paper_detail', pk=paper_pk)

@login_required
def react_event(request):
    event_pk = request.GET['event_pk']
    pe = get_object_or_404(PaperEvent, pk = event_pk)
    user = request.user
    reaction, _ = EventReaction.objects.get_or_create(user=user, paperevent=pe)
    user_reaction = request.GET['submit']
    if user_reaction == 'like' and not reaction.likes:
        reaction.likes = 1
        likes = pe.likes + 1
        pe.likes = likes
    elif user_reaction == 'frown' and not reaction.frowns:
        reaction.frown = 1
        frowns = pe.frowns + 1
        pe.frowns = frowns
    reaction.save()
    pe.save()
    data = {'event_like_count': pe.likes, 'event_frown_count': pe.frowns}
    return JsonResponse(data)





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
