from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.template import Context, loader

from kaseres.models import Task
from kaseres.accepts import accepts_json, accepts_html, accepts_xml
from kaseres.responses import json_models_response, json_obj_response, xml_models_response, xml_obj_response

# Check for desired format: HTML or JSON.
# If JSON, return data.  If HTML, use template.

@require_safe
def index(request):

    hi_pri_tasks = Task.objects.order_by('-priority')[:5]

    if accepts_json(request):
        return json_models_response(hi_pri_tasks)
    elif False: # accepts_xml(request):
        return xml_models_response(hi_pri_tasks)
    else:
        template = loader.get_template('tasks/index.html')
        context = Context({'tasks': hi_pri_tasks})
        return HttpResponse(template.render(context))


# @require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    # task_list_id
    # title
    # body
    # due_date
    # is_completed
    # priority
    res_url = ''
    if accepts_json(request):
        return json_obj_response(request.GET, status=201, location=res_url)
    elif accepts_xml(request):
        return xml_obj_response(request.GET, status=201, location=res_url)
    else:
        return HttpResponse("<h1>HTML</h1>")


@require_safe
def read_task(request, task_id):
    # task_id is a STRING
    pass


@require_http_methods(['PUT'])
def update_task(request, task_id):
    # task_id is a STRING
    pass


@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    # task_id is a STRING
    pass

