from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.template import Context, loader
from datetime import datetime

# from kaseres.models import Task, User, TaskList
from kaseres.models import Task
from kaseres.accepts import accepts_json, accepts_html, accepts_xml
from kaseres.responses import json_models_response, json_obj_response, xml_models_response, xml_obj_response, make_response

# Check for desired format: HTML or JSON.
# If JSON, return data.  If HTML, use template.

def restify(f):
    def wrapper(request):
        d = f(request)

        # check whether 'obj' or 'models'
        # in order to call the right fn

        if accepts_json(request):
            return json_models_response(d['models'])
        # elif accepts_xml(request):
        elif False:
            return xml_models_response(d['models'])
        else:
            template = loader.get_template(d['template'])
            context = Context(d['context'])
            return HttpResponse(template.render(context))
    return wrapper

# the view fn must return:
#   { 'models': models,
#     'template': STR,
#     'context': {},
#     'status': 200,   # optional
#     'location: url   # optional
#   }
#

SORT_ATTRS = [
    ('Title', 'title'),
    ('Due', 'due_date'),
    ('Priority', 'priority'),
    ('Completed?', 'is_completed')
]

@require_safe
@restify
def index(request):
    """
    If ajax, return the HTML for just the list of tasks.
    """
    sort_attr = request.GET['sort_attr'] if 'sort_attr' in request.GET else 'priority'
    sort_dir = request.GET['sort_direction'] if 'sort_direction' in request.GET else '-'
    tasks = Task.objects.order_by(sort_dir + sort_attr)
    return {
        'models': tasks,
        'template': get_index_template(request.is_ajax()),
        'context': {'tasks': tasks, 'sort_attrs': SORT_ATTRS}
    }

@require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    task = create_task_from_data(request)

    sort_attr = request.GET['sort_attr'] if 'sort_attr' in request.GET else 'priority'
    sort_dir = request.GET['sort_direction'] if 'sort_direction' in request.GET else '-'
    all_tasks = [t for t in Task.objects.exclude(id=task.id).order_by(sort_dir + sort_attr)]
    all_tasks.insert(0, task)

    template = loader.get_template('tasks/all_tasks.html')
    context = Context({'tasks': all_tasks})
    res_url = ''
    return make_response(
        template.render(context), 'text/html', status=201, location=res_url)

    # FIXME -- return the *HTML* for the new task.
    # res_url = ''
    # template = loader.get_template('tasks/one_task.html')
    # context = Context({'task': task})
    # return make_response(
    #     template.render(context), 'text/html', status=201, location=res_url)
    # return json_model_response(task, status=201, location=res_url)

# helper, not a view.
def create_task_from_data(request):
    due_date = datetime.strptime(request.POST['due_date'], '%B %d, %Y').date()
    is_completed = request.POST['is_completed'] == 'true'
    task = Task(title = request.POST['title'],
                details = request.POST['details'],
                due_date = due_date,
                is_completed = is_completed,
                priority = int(request.POST['priority']))
    task.save()
    return task

@require_safe
def index_old(request):
    hi_pri_tasks = Task.objects.order_by('-priority')[:5]
    if accepts_json(request):
        return json_models_response(hi_pri_tasks)
    elif False: # accepts_xml(request):
        return xml_models_response(hi_pri_tasks)
    else:
        template = loader.get_template('tasks/index.html')
        context = Context({'tasks': hi_pri_tasks})
        return HttpResponse(template.render(context))


@require_safe
def read_task(request, task_id):
    task = Task.objects.get(task_id)
    # if accepts_json(request):
    if True:
        return json_models_response(task)
    elif accepts_xml(request):
        return xml_models_response(task)
    else:
        return HttpResponse('<h1>HTML</h1>')

@require_http_methods(['PUT'])
def update_task(request, task_id):
    pass


@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return HttpResponse('')

# -- helpers --

def get_index_template(is_ajax):
    if is_ajax:
        return 'tasks/all_tasks.html'
    else:
        return 'tasks/index.html'

def all_tasks_html(status=200, location=None):
    # how sorted?
    tasks = Task.objects.all()
    template = loader.get_template('tasks/all_tasks.html')
    context = Context({'tasks': tasks})
    return make_response(
        template.render(context), 'text/html', status, location)

