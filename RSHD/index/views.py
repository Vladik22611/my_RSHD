from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm

def index(request):
    # View code here...
    return render(request, "index/main.html")


def route(request):
    f = request.POST.get("first_text", "абвгд")
    return HttpResponse(f"<h2>Name: {f}")

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse(f"<h2>Name: {form.cleaned_data['your_name']}")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "index/name.html", {"form": form})