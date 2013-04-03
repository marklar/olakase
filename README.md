olakase
=======

![ola k ase](http://www.actualidadjuvenil.com/wp-content/uploads/2012/12/ola-ke-ase-significado-300x300.jpg)

to-do web app

allows:
* display of to-do list
* manipulation of list (add/remove/modify entries)
* marking entries as completed
* assignment of:
    * priorities and
    * due dates
* sorting of entries by those as well

requirements:
* app:
    * minimal UI/UX design
    * single-page: cannot reload page.  each client operation is an Ajax call.
* REST API:
    * RESTful API allowing 3rd-party apps to trigger all the same actions


data model
----------

Entry
* title : string
* body : string
* priority : int
* due date : datetime
* completed : boolean
