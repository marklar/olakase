from django.contrib import admin
from kaseres.models import User, TaskList, Task

# can add an FooAdmin class (extending admin.ModelAdmin)
# to specify the order of fields to be shown (as a list of field names [strs]).
#
# pass that FooAdmin class as the second arg to admin.site.register().
#
# may even provide fieldsets, to split the form into grouped items.

# for c in [User, TaskList, Task]:
#     admin.site.register(c)

admin.site.register(User)

class TaskInline(admin.TabularInline):
    model = Task
    extra = 3

class TaskListAdmin(admin.ModelAdmin):
    # fieldsets = []
    inlines = [TaskInline]

admin.site.register(TaskList, TaskListAdmin)

admin.site.register(Task)
