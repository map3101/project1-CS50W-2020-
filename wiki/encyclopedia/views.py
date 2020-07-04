import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    #Check if the entry exists to show the appropriate page
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/entry.html",{
            "entry": "<h1>Entry not found<h1>"
        })
    
    else:
        mdfile = util.get_entry(title)
        return render(request, "encyclopedia/entry.html",{
            "entry": markdown2.markdown(mdfile)
        })