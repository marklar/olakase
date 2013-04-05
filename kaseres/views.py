from django.http import HttpResponse

import json

def index(request):
    # return HttpResponse("Yo yo yo.  KASERES index.")
    return HttpResponse(json.dumps({'foo': 'bar'}))

def create_task(request):
    pass

def read_task(request):
    pass

def update_task(request):
    pass

def delete_task(request):
    pass
