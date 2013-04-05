from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
import json

# Check for desired format: HTML or JSON.
# If JSON, return data.  If HTML, use template.


def json_response(obj):
    return HttpResponse(json.dumps(obj), mimetype="application/json")


@require_safe
def index(request):
    return json_response({'foo': 'bar'})

# Response: "201 Created" with a Location header
# containing the URL to the newly created resource.
@require_POST
def create_task(request):
    pass

@require_safe
def read_task(request):
    pass

# @require_PUT
def update_task(request):
    pass

# @require_DELETE
def delete_task(request):
    pass
