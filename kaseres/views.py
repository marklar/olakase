from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.template import Context, loader
from django.shortcuts import render
from datetime import datetime, date

# from kaseres.models import Task, User, TaskList
from kaseres.models import Task
from kaseres.accepts import accepts_json, accepts_html, accepts_xml
from kaseres.responses import json_models_response, json_obj_response, xml_models_response, xml_obj_response, make_response

def restify(f):
    """
    the view fn must return:
    { 'models': models,
      'template': STR,
      'context': {},
      'status': 200,   # optional
      'location: url   # optional
    }
    """
    def wrapper(request):
        d = f(request)
        if accepts_json(request):
            return json_models_response(d['models'])
        # FIXME
        # elif accepts_xml(request):
        elif False:
            return xml_models_response(d['models'])
        else:
            return render(request, d['template'], d['context'])
    return wrapper


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
    tasks = Task.objects.order_by(get_sort(request.GET))
    return {
        'models': tasks,
        'template': get_index_template(request.is_ajax()),
        'context': {
            'tasks': tasks,
            'priorities': Task.PRIORITIES,
            'sort_attrs': SORT_ATTRS
        }
    }

@require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    task = create_task_from_data(request.POST)
    q_set = Task.objects.exclude(id=task.id).order_by(get_sort(request.POST))
    all_tasks = [t for t in q_set]
    all_tasks.insert(0, task)

    template = loader.get_template('tasks/all_tasks.html')
    context = Context({
        'tasks': all_tasks,
        'priorities': Task.PRIORITIES
    })
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


@require_safe
def index_old(request):
    hi_pri_tasks = Task.objects.order_by('-priority')[:5]
    if accepts_json(request):
        return json_models_response(hi_pri_tasks)
    elif False: # accepts_xml(request):
        return xml_models_response(hi_pri_tasks)
    else:
        context = {
            'tasks': hi_pri_tasks,
            'priorities': Task.PRIORITIES
        }
        return render(request, 'tasks/index.html', context)
        # template = loader.get_template('tasks/index.html')
        # context = Context({
        #     'tasks': hi_pri_tasks,
        #     'priorities': Task.PRIORITIES
        # })
        # return HttpResponse(template.render(context))

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

def get_sort(req_data):
    sort_prefix = get_sort_prefix(req_data)
    sort_attr = get_sort_attr(req_data)
    return sort_prefix + sort_attr

def get_sort_attr(req_data):
    a = 'sort_attr'
    return req_data[a] if a in req_data else 'priority'

def get_sort_prefix(req_data):
    a = 'sort_is_asc'
    is_asc = req_data[a] == 'true' if a in req_data else False
    return '' if is_asc else '-'

def create_task_from_data(req_data):
    task = Task(title = req_data['title'],
                details = req_data['details'],
                due_date = get_due_date(req_data),
                is_completed = get_is_completed(req_data),
                priority = get_priority(req_data))
    task.save()
    return task

def get_due_date(req_data):
    if 'due_date' in req_data:
        return datetime.strptime(req_data['due_date'], '%B %d, %Y').date()
    else:
        return date.today()

def get_priority(req_data):
    if 'priority' in req_data:
        return int(req_data['priority'])
    else:
        return 2

def get_is_completed(req_data):
    if 'is_completed' in req_data:
        return req_data['is_completed'] == 'true'
    else:
        return False

def get_index_template(is_ajax):
    if is_ajax:
        return 'tasks/all_tasks.html'
    else:
        return 'tasks/index.html'

# -- unused --
def all_tasks_html(status=200, location=None):
    # how sorted?
    tasks = Task.objects.all()
    # template = loader.get_template('tasks/all_tasks.html')
    context = Context({
        'tasks': tasks,
        'priorities': Task.PRIORITIES
    })
    return make_response(
        template.render(context), 'text/html', status, location)

