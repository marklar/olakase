// Generated by CoffeeScript 1.6.2
(function() {
  var click_add_btn, click_delete, click_sort_btn, click_toggle_details, delete_task, display_sorted_tasks, edit_title, highlight_column, init_add_btn, init_all, init_datepicker, init_delete_btns, init_details_display, init_edit, init_sort, init_toggle_details_btn, on_ajax_error, prepend_task, save_title, set_details_btn_text, set_sort_btn_imgs, set_sort_state, show_saved, sort_tasks_by, state;

  on_ajax_error = function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus);
    console.log(errorThrown);
    return console.log(jqXHR);
  };

  state = {
    details_showing: false,
    sort: {
      column: 'priority',
      is_asc: {
        title: true,
        due_date: true,
        priority: false,
        is_completed: true
      }
    }
  };

  display_sorted_tasks = function(htmlStr, textStatus, jqXHR) {
    $('#tasks_container').html(htmlStr);
    highlight_column(state.sort.column);
    init_delete_btns();
    init_details_display();
    init_datepicker();
    return init_edit();
  };

  sort_tasks_by = function(attr, is_asc) {
    return $.ajax({
      url: '/kaseres/tasks/',
      type: 'GET',
      data: {
        sort_attr: attr,
        sort_is_asc: is_asc
      },
      cache: false,
      dataType: 'html',
      success: display_sorted_tasks,
      error: function() {
        return on_ajax_error;
      }
    });
  };

  set_sort_state = function(attr) {
    var s;

    s = state.sort;
    if (s.column === attr) {
      return s.is_asc[attr] = !s.is_asc[attr];
    } else {
      return s.column = attr;
    }
  };

  set_sort_btn_imgs = function(attr) {
    var dir;

    $('.sort_arrow').hide();
    dir = state.sort.is_asc[attr] ? 'up' : 'dn';
    return $("#" + dir + "_arrow_" + attr).show();
  };

  highlight_column = function(attr) {
    return $(".attr." + attr).addClass('highlighted');
  };

  click_sort_btn = function(evt) {
    var attr;

    attr = this.id.match(/^sort_(.+)$/)[1];
    set_sort_state(attr);
    set_sort_btn_imgs(attr);
    sort_tasks_by(attr, state.sort.is_asc[attr]);
    return highlight_column(attr);
  };

  init_sort = function() {
    $('.sort_btn').click(click_sort_btn);
    set_sort_btn_imgs(state.sort.column);
    return highlight_column(state.sort.column);
  };

  init_datepicker = function() {
    return $('.date').datepicker({
      dateFormat: 'MM d, yy'
    });
  };

  show_saved = function(evt) {
    return console.log('saved!');
  };

  save_title = function(evt) {
    var new_title;

    new_title = $.trim($(this).val());
    $("#task_title_" + evt.data.task_id).html(new_title).click(edit_title);
    if (new_title !== evt.data.prev_title) {
      if (state.sort.column === 'title') {
        $("#task_title_" + evt.data.task_id).removeClass('highlighted');
      }
      console.log("Save task " + evt.data.task_id + "'s new title: " + new_title);
      return $.ajax({
        type: 'PUT',
        url: "/kaseres/tasks/" + evt.data.task_id + "/update/",
        data: {
          title: new_title
        },
        dataType: 'html',
        cache: false,
        error: on_ajax_error,
        success: show_saved
      });
    }
  };

  edit_title = function() {
    var prev_title, task_id;

    $(this).unbind();
    task_id = this.id.match(/^task_title_(.+)$/)[1];
    prev_title = $.trim($(this).html());
    $(this).html("<input id='temp_edit' type='text' value='" + prev_title + "' />");
    return $('#temp_edit').focus().blur({
      task_id: task_id,
      prev_title: prev_title
    }, save_title);
  };

  init_edit = function() {
    return $('.attr.title').click(edit_title);
  };

  prepend_task = function(htmlStr, textStatus, jqXHR) {
    var task_id;

    task_id = htmlStr.match(/^<li id=\"task_(\d+)\"/)[1];
    $('#tasks').prepend(htmlStr);
    init_delete_btns();
    init_datepicker();
    init_edit();
    $("#task_details_" + task_id).hide();
    return $("#task_title_" + task_id).click();
  };

  click_add_btn = function() {
    return $.ajax({
      type: 'POST',
      url: '/kaseres/tasks/create/',
      data: {
        sort_attr: state.sort.column,
        sort_direction: state.sort.is_asc[state.sort.column],
        title: 'ADD TITLE',
        details: ''
      },
      dataType: 'html',
      cache: false,
      error: on_ajax_error,
      success: prepend_task
    });
  };

  init_add_btn = function() {
    return $('#add_task').click(click_add_btn);
  };

  delete_task = function(id) {
    return $.ajax({
      type: 'DELETE',
      url: "/kaseres/tasks/" + id + "/delete/",
      cache: false,
      error: on_ajax_error,
      success: function() {
        return console.log('success!');
      }
    });
  };

  click_delete = function(evt) {
    var elem, task_id;

    if (!confirm('Delete this task?')) {
      return;
    }
    task_id = this.id.match(/^delete_(.*)$/)[1];
    elem = $("#task_" + task_id);
    elem.toggle(200, function() {
      return elem.remove();
    });
    return delete_task(task_id);
  };

  init_delete_btns = function() {
    return $('.delete_btn').click(click_delete);
  };

  set_details_btn_text = function() {
    var verb;

    verb = state.details_showing ? 'Hide' : 'Show';
    return $('#toggle_details').html(verb + ' Details');
  };

  click_toggle_details = function(evt) {
    $('.task_details').toggle(200);
    state.details_showing = !state.details_showing;
    return set_details_btn_text();
  };

  init_details_display = function() {
    if (!state.details_showing) {
      return $('.task_details').toggle();
    }
  };

  init_toggle_details_btn = function() {
    $('#toggle_details').click(click_toggle_details).hide();
    set_details_btn_text();
    return init_details_display();
  };

  init_all = function() {
    init_sort();
    init_toggle_details_btn();
    init_add_btn();
    init_delete_btns();
    init_datepicker();
    return init_edit();
  };

  $(document).ready(init_all);

}).call(this);
