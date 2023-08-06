from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import LinkForm
from .crawler import main


class Index(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('gatherlinks:thanks')
        return render(request, 'gatherlinks/add-link.html', {'form': LinkForm})

    def post(self, request, **kwargs):
        form = LinkForm(request.POST)
        if form.is_valid():
            start = main.StartPoint(request.POST['links'], max_crawl=3)
            start.start()
            return render(request, 'gatherlinks/thanks.html')
        else:
            pass


class Thanks(View):
    pass


def crawled_links(arg):
    return arg


