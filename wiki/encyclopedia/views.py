import markdown2
from random import randint

from django.shortcuts import render, redirect

from . import util
from .forms import CreateForm, EditForm

def index(request):
    # If user submit the search form
    if request.method == 'POST':
        # Check if the query matches the name of an entry
        if util.get_entry(request.POST.get('q')) == None:
            return redirect('results', query=request.POST.get('q'))
        
        else:
            return redirect('entry', title=request.POST.get('q'))
    
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, title):
    # Check if the entry exists to show the appropriate page
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/entry.html",{
            "entry": "<h1>Entry not found!<h1>",
            "title": "ERROR Entry not found",
            "link": False
        })
    
    else:
        mdfile = util.get_entry(title)
        return render(request, "encyclopedia/entry.html",{
            "entry": markdown2.markdown(mdfile),
            "title": title,
            "link": True
        })

def results(request, query):
    # Save all entries in a list and check if the query is a substring
    entries = util.list_entries()

    resultsList = [i for i in entries if query in i]

    return render(request, "encyclopedia/results.html", {
        "resultsList": resultsList,
        "term": query
    })

def create(request):
    alert = ""
    if request.method == 'POST':
        form = CreateForm()
        form.title = request.POST.get('title')
        form.text = request.POST.get('text')
        #check if the entry exists
        if util.get_entry(form.title) != None:
            alert = "ERROR: This entry already exists!"
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "alert": alert
            })
        
        else:
            util.save_entry(form.title, form.text)
            return redirect('entry', title=form.title)
            
    else:
        form = CreateForm()
        return render(request, "encyclopedia/create.html", {
            "form": form,
            "alert": alert
        })

def edit(request, title):
    if request.method == 'POST':
        form = EditForm()
        form.text = request.POST.get('text')
        util.save_entry(title, form.text)
        return redirect('entry', title=title)

    else: #method == 'GET'
        #Check if the entry exists
        if util.get_entry(title) == None:
            return render(request, "encyclopedia/entry.html",{
                "entry": "<h1>Entry not found!<h1>",
                "title": "ERROR Entry not found",
                "link": False
            })
        
        else:
            form = EditForm(initial={'text': util.get_entry(title)})
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })

def random(request):
    #get all entries in a list
    entries_list = util.list_entries()
    #Generate random number using the list length 
    number = randint(0, (len(entries_list) - 1))
    #return a random element of the list
    return redirect('entry', title=entries_list[number])