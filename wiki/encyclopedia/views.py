import markdown2

from django.shortcuts import render, redirect

from . import util


def index(request):
    #If user submit the search form
    if request.method == 'POST':
        #Check if the query matches the name of an entry
        if util.get_entry(request.POST.get('q')) == None:
            return redirect('entry', title="NOTFOUND")
        
        else:
            return redirect('entry', title=request.POST.get('q'))
    
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, title):
    #Check if the entry exists to show the appropriate page
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/entry.html",{
            "entry": "<h1>Entry not found!<h1>",
            "title": "ERROR Entry not found"
        })
    
    else:
        mdfile = util.get_entry(title)
        return render(request, "encyclopedia/entry.html",{
            "entry": markdown2.markdown(mdfile),
            "title": title
        })