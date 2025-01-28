from django.template import loader
from django.http import HttpResponse
# Create your views here.

def polls(request):
    template = loader.get_template("index.html") 
    return HttpResponse(template.render)
    #return HttpResponse("Hello World. This is my app")