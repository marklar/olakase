// Generated by CoffeeScript 1.6.2
(function() {
  var bg_colors, click_add_btn, click_create_submit, click_delete, click_sort_btn, click_toggle_details, delete_task, high_els, highlight_col, init_add_btn, init_all, init_datepicker, init_delete_btns, init_details_display, init_sort, init_sort_btns, init_toggle_details_btn, low_els, on_ajax_error, set_details_btn_text, set_sort_state, sort_tasks_by, state, toggle_sort_dir, unhighlight_col, unhighlight_task, update_tasks;

  on_ajax_error = function(jqXHR, textStatus, errorThrown) {
    console.log(textStatus);
    console.log(errorThrown);
    return console.log(jqXHR);
  };

  state = {
    details_showing: false,
    after_create: false,
    sort: {
      column: 'priority',
      direction: {
        title: '',
        due_date: '-',
        priority: '-',
        is_completed: ''
      }
    }
  };

  bg_colors = {
    sort: 'LightSteelBlue',
    regular: 'White'
  };

  update_tasks = function(htmlStr, textStatus, jqXHR) {
    $('#tasks_container').html(htmlStr);
    highlight_col(state.sort.column);
    init_delete_btns();
    init_details_display();
    init_datepicker();
    if (state.after_create) {
      state.after_create = false;
      $('#tasks > li').filter(':first').toggle().toggle(200);
      return low_els($('#tasks > li:first .attr'));
    }
  };

  sort_tasks_by = function(attr, direction) {
    return $.ajax({
      url: '/kaseres/tasks/',
      type: 'GET',
      data: {
        sort_attr: attr,
        sort_direction: direction
      },
      cache: false,
      dataType: 'html',
      success: update_tasks,
      error: function() {
        return on_ajax_error;
      }
    });
  };

  high_els = function(els) {
    return els.css('background-color', bg_colors.sort);
  };

  low_els = function(els) {
    return els.css('background-color', bg_colors.regular);
  };

  highlight_col = function(attr) {
    return high_els($(".attr." + attr));
  };

  unhighlight_col = function(attr) {
    return low_els($(".attr." + attr));
  };

  unhighlight_task = function(id) {
    console.log("unhighlighting id: " + id);
    return low_els($("#" + id + " > .attr." + state.sort.column));
  };

  toggle_sort_dir = function(attr) {
    return state.sort.direction[attr] = state.sort.direction[attr] === '-' ? '' : '-';
  };

  set_sort_state = function(attr) {
    if (state.sort.column === attr) {
      return toggle_sort_dir(attr);
    } else {
      return state.sort.column = attr;
    }
  };

  click_sort_btn = function(evt) {
    var attr;

    attr = this.id.match(/^sort_(.*)$/)[1];
    set_sort_state(attr);
    sort_tasks_by(attr, state.sort.direction[attr]);
    return highlight_col(attr);
  };

  init_sort_btns = function() {
    return $('.sort_btn').click(click_sort_btn);
  };

  init_sort = function() {
    init_sort_btns();
    bg_colors.regular = $('.attr.title:first-child').css('background-color');
    return highlight_col(state.sort.column);
  };

  click_create_submit = function() {
    return $.ajax({
      type: 'POST',
      url: '/kaseres/tasks/create/',
      data: {
        sort_attr: state.sort.column,
        sort_direction: state.sort.direction[state.sort.column],
        title: 'add title',
        details: ''
      },
      dataType: 'html',
      cache: false,
      error: on_ajax_error,
      success: update_tasks
    });
  };

  click_add_btn = function() {
    alert('Open form for creating task.');
    state.after_create = true;
    return click_create_submit();
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
    $('#toggle_details').click(click_toggle_details);
    set_details_btn_text();
    return init_details_display();
  };

  init_datepicker = function() {
    return $('.date').datepicker({
      dateFormat: 'MM d, yy'
    });
  };

  init_all = function() {
    init_sort();
    init_toggle_details_btn();
    init_add_btn();
    init_delete_btns();
    return init_datepicker();
  };

  $(document).ready(init_all);

}).call(this);
