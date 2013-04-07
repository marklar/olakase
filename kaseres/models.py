from django.db import models
from datetime import date

MAX_LEN = 256

#---------------------------------------
# class User(models.Model):
#     """ A person with TaskLists """
#     first_name = models.CharField(max_length=MAX_LEN)
#     last_name = models.CharField(max_length=MAX_LEN)
#     email = models.EmailField(max_length=MAX_LEN)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def full_name(self):
#         return u' '.join([self.first_name, self.last_name])

#     def __unicode__(self):
#         return u', '.join([self.full_name(), self.email])


# #---------------------------------------
# class TaskList(models.Model):
#     """ A collection of Tasks """
#     user = models.ForeignKey(
#         User,
#         on_delete=models.DO_NOTHING
#     )
#     name = models.CharField(max_length=MAX_LEN)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#         return self.name + ' (' + self.user.__unicode__() + ')'


#---------------------------------------
class Task(models.Model):
    """ A to-do item. """
    # task_list = models.ForeignKey(
    #     TaskList,
    #     on_delete=models.DO_NOTHING
    # )
    title = models.CharField(max_length=MAX_LEN)
    details = models.TextField()
    due_date = models.DateField(default=date.today())
    is_completed = models.BooleanField(default=False)
    PRIORITIES = (
        (3, 'High'),
        (2, 'Med'),
        (1, 'Low')
    )
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITIES,
        default=2
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title + ' :: ' + self.details
