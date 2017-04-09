from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Job
from . import forms

class create_job(CreateView):
    model = Job
    success_url = '/home'
    form_class = forms.JobForm

def search_jobs(request):
    if request.method == "POST":
        bool_tokens = ['jobtitle', 'description', 'zipcode', 'price',
                      'tags', 'due_date']
        jobs_list = Job.objects.all()
        for fieldval in request.POST:
            if fieldval in bool_tokens:
              newlist = jobs_list.filter(**{fieldval: request.POST.get(fieldval)})
              if newlist:
                  jobs_list = newlist
        if 'due_date_low' in request.POST:
                minDate = request.POST.get('due_date_low')
        if 'due_date_high' in request.POST:
                maxDate = request.POST.get('due_date_high')
        if minDate is not None and maxDate is not None:
            newlist = jobs_list.filter(due_date__range= [minDate, maxDate])
            if newlist:
                jobs_list = newlist
        return render(request, 'list_jobs.html', {'jobs': jobs_list})
    return render(request, 'search_jobs.html', {'jobs': None})

def list_jobs(request):
    def validateJobSearch(request):
        pass

    error_string = None
    if request.method == "POST":
        error_string = validateJobSearch(request)
        if error_string is not None:
            return search_jobs(request)
    return render(request, 'list_jobs.html', {'error_string': error_string})