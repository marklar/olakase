from django.conf.urls import patterns, url

from kaseres import views

urlpatterns = patterns(
    '',

    # On client...
    # When (re)displaying results, do we...
    #
    # 1. Request the entire (sorted) list and display it?
    # -OR-
    # 2. Update client data model and redisplay it?
    #

    # GET
    # home page: show all tasks
    # ex: /kaseres/
    #
    # How do we pass additional query parameters?:
    #   * how we'd like the data sorted,
    #   * how many results,
    #   * etc.
    url(r'^$', views.index, name='index'),

    # POST (create)
    # ex: /kaseres/create/
    #
    # instance data goes in the POST data
    #
    # Response: "201 Created" with a Location header
    # containing the URL to the newly created resource.
    #
    url(r'^create/$', views.create_task, name='create_task'),

    # GET (read)
    # ex: /kaseres/12/read/
    url(r'^(?P<task_id>\d+)/read/', views.read_task, name='read_task'),

    # PUT (update) - idempotent w/ same params
    # ex: /kaseres/12/update/
    # Where do we pass in the k:v pairs?  PUT data?
    url(r'^(?P<task_id>\d+)/update/$', views.update_task, name='update_task'),

    # DELETE (delete)
    # ex: /kaseres/12/delete/
    url(r'^(?P<task_id>\d+)/delete/$', views.delete_task, name='delete_task'),
)
