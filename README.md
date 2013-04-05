olakase
=======

![ola k ase](http://www.actualidadjuvenil.com/wp-content/uploads/2012/12/ola-ke-ase-significado-300x300.jpg)

What: To-do web app

Allows:
* display of to-do list
* manipulation of list (add/remove/modify entries)
* marking entries as completed
* assignment of:
    * priorities and
    * due dates
* sorting of entries by those as well

Requirements:
* app:
    * minimal UI/UX design
    * single-page: cannot reload page.  each client operation is an Ajax call.
* REST API:
    * RESTful API allowing 3rd-party apps to trigger all the same actions


Data Model
----------

User
* id
* first_name : string
* last_name : string
* email : EmailField

List
* id
* user_id : int
* name : string

Entry
* id
* list_id : int
* title : string
* body : string
* priority : int
* due date : datetime
* completed : boolean

Immutable.  Like Datamic.
Every time we change an entry in the list, we create a new list?
Use CommaSeparatedIntegerField to store the lists?


