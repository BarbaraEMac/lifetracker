// this is temporary, until I think of the right way to do this

var new_metric_template = "\
<div id='metric-%(query_id)s' class='metric'>\
  <input type='hidden' id='metric-%(query_id)s-type' value='%(format)s'/>\
  <input type='hidden' id='metric-%(query_id)s-time' value='%(ask_when)s'/>\
  <div class='metric-name-container'>\
    <h3 id='metric-%(query_id)s-name' class='metric-name'>%(name)s</h3>\
    <input type='text' value='%(name)s' id='edit-name-%(query_id)s' class='edit-field edit-name'/>\
  </div>\
  <div class='metric-snapshot'>\
    <p class='overview-metric'>Current: None Yet!</p>\
    <p class='overview-metric'>None Yet!</p> \
    <p class='edit-field'>\
      <input type='hidden' id='freq-minutes-%(query_id)s' value='%(freq_minutes)s'/>\
      Frequency: <select id='edit-frequency-%(query_id)s' class='edit-field edit-frequency'>\
      <option id='freq-1440' checked='true'>Every Day</option>           \
      <option id='freq-360'>Every 6 Hours</option>           \
      <option id='freq-180'>Every 3 Hours</option>           \
      <option id='freq-60'>Every Hour</option>           \
      <option id='freq-1'>Every Minute</option>         \
    </select>\
  </p>\
  </div>\
  <div class='metric-options'>\
    <a id='analyze-%(query_id)s' class='analyze-button' href='#'>\
      <img src='images/lightbulb_icon.png'/>\
    </a>\
    <a id='edit-%(query_id)s' class='query-edit-button' href='#'>\
      <img src='images/cog_icon.png'/>\
    </a>\
    <a id='submit-%(query_id)s' class='query-edit-submit-button' href='#'>\
      <img src='images/checkmark_icon.png'/>\
    </a>\
  </div>\
  <div id='edit-format-container-%(query_id)s' class='edit-field edit-format-container'>\
    <p>Format</p>\
    <form id='edit-format-%(query_id)s' class='edit-format'>\
    <p>\
      Text <input type='radio' name='format' class='format-text' value='text'/>\
      Number <input type='radio' name='format' class='format-number' value='number' checked='true'/>\
      Time <input type='radio' name='format' class='format-time' value='time'/>\
    </p>\
    </form>\
  </div>\
  <div id='edit-time-container-%(query_id)s' class='edit-field edit-time-container'>\
    <p>Ask me During</p>\
    <p>\
      Morning <input type='checkbox' id='morning-%(query_id)s' class='ask-when-%(query_id)s' value='morning' checked='true'/>\
      Afternoon <input type='checkbox' id='afternoon-%(query_id)s' value='afternoon' class='ask-when-%(query_id)s' checked='true'/>\
      Evening <input type='checkbox' id='evening-%(query_id)s' value='evening' class='ask-when-%(query_id)s' checked='true'/>\
    </p>\
  </div>\
  <div id='edit-text-container-%(query_id)s' class='edit-field edit-text-container'>\
    <p>Query Text:</p>\
    <input id='edit-text-%(query_id)s' class='edit-field edit-text' type='text' value='What is the value of %(name)s right now?'/>\
  </div>\
\
\
  <div id='delete-container-%(query_id)s' class='edit-field delete-container'>\
      <a id='delete-%(query_id)s' class='query-delete-button' href='#'>Delete</a>\
      <a id='confirm-delete-%(query_id)s' class='query-delete-confirm-button' href='#'>Really?</a>\
  </div>\
\
\
  <div id='analytics-container-%(query_id)s' class='analytics-container'>\
    <div id='numeric-analytics-container-%(query_id)s' class='numeric-analytics'>\
      <img class='analytics-loading' src='images/loading.gif'/>\
      <table id='analytics-%(query_id)s' class='analytics-table'></table>\
      <p>\
        <a href='analyze?query_id=%(query_id)s' id='analytics-more-%(query_id)s' class='more-analytics-button'>More</a>\
      </p>\
    </div>\
    <div id='chart-%(query_id)s' class='chart'>\
      <img class='chart-loading' src='images/loading.gif'/>\
    </div>\
  </div>\
</div>";

metric_defaults = {
  "name": "default",
  "text": "What is the value of default right now?",
  "frequency": 1440,
  "format": "number",
  "template_id": 0,
}

var completion = '';

$(document).ready(function() { 
  $('select.edit-frequency').each(select_edit_frequency_init); 
  $('.query-delete-confirm-button').click(query_delete_confirm_click);
  $('.query-delete-button').click(query_delete_click);
  $('#new-query-create-button').click(new_query_create_click);
  $('#new-query-submit').click(new_query_create_submit_click);
  $('.query-edit-button').click(query_edit_click);
  $('.query-edit-submit-button').click(query_edit_submit_click);
  $('a.analyze-button').click(analyze_click);
  $('.metric').each(edit_format_init);
  $('.metric').each(edit_time_init);

  $('#intro').click(intro_next_page_click);

  // don't let us focus the shadow input
  $('#lt-prompt-shadow').focus(function() { $('#lt-new-metric-prompt').focus() });

  new_metric_prompt_init();

  if (window.location.search.indexOf('first_time') != -1) {
    intro();
  } else if (window.location.search.indexOf('setup_complete') != -1) {
    intro_complete();
  }
});

intro_next_page_click = function(event) {
  event.preventDefault();

  this_page = parseInt($('div.intro-page.active').attr('id').substr(10));

  next_page = this_page + 1;

  this_page_id = '#intro-page' + this_page;
  next_page_id = '#intro-page' + next_page;

  $(this_page_id).animate({
    opacity: 0,
  }, 500, function() {
    $(this_page_id).css('display', 'none');
    $(this_page_id).removeClass('active');

    $(next_page_id).css('display', 'block');
    $(next_page_id).addClass('active');

    if (next_page == 2) {
      intro_2();
    } else if (next_page == 3) {
      intro_3();
    } else if (next_page == 4) {
      intro_4();
    } if (next_page == 5) {
      intro_5();
    } else if (next_page == 6) {
      intro_6();
    } else if (next_page > 6) {
      $('#intro').css('display', 'none');
    }
  });
}

edit_time_init = function() {
  metric_id = $(this).attr('id').substring(7);
  ask_when_id = '#metric-' + metric_id + '-time';
  ask_when = eval($(ask_when_id).val());

  for (i in ask_when) {
    time_id = '#' + ask_when[i] + '-' + metric_id;
    $(time_id)[0].checked = true;
  }
}

edit_format_init = function() {
  metric_id = $(this).attr('id').substring(7);
  format_id = '#metric-' + metric_id + '-type';
  format = $(format_id).val();

  format_thing = '#metric-' + metric_id + ' .edit-format .format-' + format;

  $(format_thing)[0].checked = true;
}

intro_complete = function() {
  // tip all the different things
  $('#setup-complete-dialog').dialog({
    width: '500px',
    position: ['top','center'],
    buttons: [{
      text: 'Awesome',
      click: function() {
        $(this).dialog("close");
      }
    }]
  });
}

glow_twice = function(obj, num) {
  if (num == undefined) num = 0;
  if (num == 2) return;

  $(obj).animate({
    backgroundColor: "#bbbbbf",
  }, 500, function() {
    $(obj).animate({
      backgroundColor: "#f8f8ff",
    }, 500, function() {
      glow_twice(obj, num += 1);
    });
  });
}

intro_2 = function() {
  $('.metric').each(function() {
    glow_twice($(this), 0);
  });
}

intro_3 = function() {
  $('.query-edit-button', $('.metric')[0]).click();
}

intro_4 = function() {
  $('.analyze-button', $('.metric')[0]).click();
}

intro_5 = function() {
  $('.metric').animate({
    height: '100px',
  });

  $('.metric').removeClass('analyzing');
  $('.metric').removeClass('editing');

  $('#new-query-create-button').click();
  $('#lt-new-metric-prompt').val('Running');
}

intro_6 = function() {
  $('#lt-new-metric-prompt').val('');
  $('#new-metric-container').removeClass('active');

  $('body').animate({
    'scrollTop': '0px',
  }); 

  $('#intro').delay(2000).animate({
    opacity: '0.0',
  }, 1000).removeClass('active');
}

// a series of dialogs/tooltips that introduce the user to the UI
intro = function() {
  $('#intro').css('display', 'block');
}

addMetric = function(metric_name) {
  var metric;

  if (template_metrics[metric_name] != undefined) {
    metric = getTemplateValues(metric_name);
  } else {
    metric = getDefaultValues(metric_name);
  }

  user_email = $('#user_email').val();

  // set the spinner and hide the inputs
  $('#new-metric-container').addClass('loading');
  $('#new-metric-container').removeClass('active');
  
  // We do this to hide the autocomplete
  $('body').focus();

  // post to /addQuery
  data = {
    'frequency': metric['frequency'],
    'text': metric['text'],
    'format': metric['format'],
    'template_id': metric['template_id'],
    'name': metric['name'],
    'user_email': user_email,
  }

  $.ajax({
    url: 'data/newQuery',
    type: 'post',
    data: data,
    success: function(response) {
      addMetricCallback(response, metric['name']);
      $('#new-metric-container').removeClass('loading');
    }
  });
}

addMetricCallback = function(metric_id, name) {
  // Get the new HTML
  metric_html = new_metric_template.replace(/\%\(query_id\)s/g, metric_id);
  metric_html = metric_html.replace(/\%\(name\)s/g, name);

  // Place it in the DOM
  $('#user_email').before(metric_html);

  // Bind the new buttons
  metric = '#metric-' + metric_id;

  $(metric + ' .query-delete-button').click(query_delete_click);
  $(metric + ' .query-delete-confirm-button').click(query_delete_confirm_click);
  $(metric + ' .query-edit-button').click(query_edit_click);
  $(metric + ' .query-edit-submit-button').click(query_edit_submit_click);
  $(metric + ' a.analyze-button').click(analyze_click);

  // Update the new-metric prompt
  $('#new-metric-container').removeClass('active');
  $('#lt-new-metric-prompt').val('');
  $('#lt-prompt-shadow').val('');
}


getDefaultValues = function(name) {
  metric = metric_defaults;
  metric["name"] = name;
  metric["text"] = "What is the value of " + name + " right now?";
  return metric;
}

getTemplateValues = function(template_name) {
  return template_metrics[template_name];
}

select_edit_frequency_init = function() {
  query_id = $(this).attr('id').substring(15);
  
  freq_minutes_id = '#freq-minutes-' + query_id;

  freq_minutes = $(freq_minutes_id).val();

  select_id = '#edit-frequency-' + query_id; 
  option_id = '#freq-' + freq_minutes;

  $(select_id + ' ' + option_id).attr('selected', 'selected');
}

query_delete_confirm_click = function(event) {
  event.preventDefault();
  query_id = $(this).attr('id').substring(15);
 
  data = {
    'query_id': query_id,
  };

  // do a post and on success reload the page
  $.ajax({
    url: 'data/deleteQuery',
    type: 'post',
    data: data,
    failure: function() {
      alert('failure!');
    },
    success: function() {
      window.location = '/dashboard';
    },
  }); 
}

query_delete_click = function(event) {
  event.preventDefault();
  query_id = $(this).attr('id').substring(7);
  confirm_button_id = '#confirm-delete-' + query_id;

  $(this).css('display', 'none');
  $(confirm_button_id).css('display', 'block');
}

new_query_create_click = function(event) {
  event.preventDefault();
  $('#new-metric-container').addClass('active');

  // make the page taller and scroll so that the whole autocomplate
  // will be in view
  height = $('#lt-base').height()
  $('#lt-base').height(height + 400 + 'px');
  $("body").animate({
    "scrollTop": $('#lt-new-metric-prompt').offset().top + "px"
  }, 500, function() {
    $('#lt-new-metric-prompt').focus();
  });

  $('#lt-prompt-shadow').offset($('#lt-new-metric-prompt').offset());
}

new_query_create_submit_click = function() {
  new_name = $('#new-query-name-input').val();
  new_text = $('#new-query-text-input').val();
  new_frequency = $('#new-query-frequency-input :selected').attr('id').substring(5);
  new_format = $('#new-query-format-input').val();
  user_email = $('#user_email').val();

  data = {
    'name': new_name,
    'text': new_text,
    'frequency': new_frequency,
    'format': new_format,
    'user_email': user_email,
  };

  $.ajax({
    type: 'post',
    url: 'data/newQuery',
    data: data, 
    success: function() {
        window.location = '/dashboard';
      },
  });
}

query_edit_click = function(event) {
  event.preventDefault();
  query_id = $(this).attr('id').substring(5);
  metric_id = '#metric-' + query_id;

  // collapse any other expanded edit-tabs
  close_tabs();

  // expand this tab

  $(metric_id).animate({
    height: '340px',
  }, 200);

  $(metric_id).addClass('editing');
}

query_edit_submit_click = function(event) {
  event.preventDefault();
  query_id = $(this).attr('id').substring(7);
  
  name_id = '#edit-name-' + query_id;
  text_id = '#edit-text-' + query_id;
  frequency_id = '#edit-frequency-' + query_id;
  format_id = '#edit-format-' + query_id;
  ask_when_class = '.ask-when-' + query_id;

  new_name = $(name_id).val();
  new_text = $(text_id).val();
  new_frequency = $(frequency_id + ' :selected').attr('id').substring(5);
  new_format = $(format_id + ' :checked').val();

  new_ask_when = '';

  $(ask_when_class + ':checked').each(function() {
    new_ask_when = new_ask_when + $(this).val() + ',';
  });

  new_query_data = {
    'query_id': query_id,
    'name': new_name,
    'text': new_text,
    'frequency': new_frequency,
    'format': new_format,
    'ask_when': new_ask_when,
  };

  $.ajax({
    url: 'data/editQuery',
    type: 'POST',
    data: new_query_data,
    success: function() {
      window.location = '/dashboard';
    },
  });
}

close_tabs = function () {
  $('div.metric.analyzing, div.metric.editing').animate({
    height: '100px',
  }, 250);

  $('div.metric.analyzing').removeClass('analyzing');
  $('div.metric.editing').removeClass('editing');
}

analyze_click = function(event) {
  event.preventDefault();
  query_id = $(this).attr('id').substring(8);
  metric_id = '#metric-' + query_id;
  analytics = '#analytics-' + query_id;

  // collapse all other analytics tabs
  close_tabs();

  // expand this analytics tab

  $(metric_id).animate({
    height: '510px',
  }, 500);

  $(metric_id).addClass('analyzing');

  // at this point, if the analytics are already loaded, 
  // stop and do nothing more
  if($(metric_id).hasClass('analytics-loaded')) {
    return
  }
  
  if(!$(metric_id).hasClass('analytics-loaded')) {
    params = {
      'query_id': query_id,
    };

    $.ajax({
      url: 'analyzeJSON',
      type: 'GET',
      data: params,
      success: function(response) {
        data = eval(response);

        for (index in data) {
          row = "<tr><td>" + data[index][0] + "</td><td>" + data[index][1] + "</td></tr>";
          $(analytics).append(row);
          if (index > 5) break; // only show the top seven for now.
        }        
   
        // mark the metric has having its analytics in place so we
        // don't reload them the next time we click 
        $(metric_id).addClass('analytics-loaded');
      },
    });
  }

  if(!$(metric_id).hasClass('chart-loaded')) {
    // TODO: 
    // number: line-chart DONE
    // time: line-chart DONE
    // text: bar-graph of incidences of the most frequent words

    // ajax to /data/pointsForQuery to get all the points
    // parse them into the format google wants
    // do the google-charty stuff

    chart_div = 'chart-' + query_id;

    // get the type of the metric
    metric_type_id = metric_id + '-type';
    type = $(metric_type_id).val();

    // get the name of the metric
    metric_name_id = metric_id + '-name';
    metric_name = $(metric_name_id).html();

    if (type == 'text') {
      $.ajax({
        url: 'analyze/text/wordFrequencies',
        type: 'GET',
        data: params,
        success: function(response) {
          $(metric_id).addClass('chart-loaded');

          data = eval(response)[0];

          // there's gotta be a better way to do this
          // JSON is serializing as an object, not an associative array
          data_length = 0;
          for (key in data) {
            data_length++;
          }

          var chart_data = new google.visualization.DataTable();
          chart_data.addColumn('string', 'word');
          chart_data.addColumn('number', metric_name);

          chart_data.addRows(data_length);

          i = 0;
          for (key in data) {
            chart_data.setValue(parseInt(i), 0, key); 
            chart_data.setValue(parseInt(i), 1, data[key]);           
            i++;
          }
          
          var chart = new google.visualization.BarChart(
            document.getElementById(chart_div));

          chart.draw(chart_data, {
            width: 440, 
            height: 390, 
            vAxis: {'title': 'Word', 'titleTextStyle': {'color': 'red', 'fontSize': 14}},
            hAxis: {'title': 'Occurrences', 'titleTextStyle': {'color': 'red', 'fontSize': 14}},
          });
        },
      });
    } else if (type == 'number' || type == 'time') {
      $.ajax({
        url: 'data/pointsForQuery',
        type: 'GET',
        data: params,
        success: function(response) {
          $(metric_id).addClass('chart-loaded');

          data = eval(response);

          var chart_data = new google.visualization.DataTable();
          chart_data.addColumn('string', 'index');
          chart_data.addColumn('number', metric_name);

          chart_data.addRows(data.length);

          for (i in data) {
            chart_data.setValue(parseInt(i), 0, (i).toString()); 
            chart_data.setValue(parseInt(i), 1, parseInt(data[i]['text']));           }
          
          var chart = new google.visualization.LineChart(
            document.getElementById(chart_div));

          chart.draw(chart_data, {
            width: 440, 
            height: 390, 
            hAxis: {'title': 'Time', 'titleTextStyle': {'color': 'red', 'fontSize': 14}},
          });
        },
      });
    }
  }
}

new_metric_prompt_init = function() {
  metric_names = [];
  for (name in template_metrics) {
    metric_names.push(name);
  }

  $('#lt-new-metric-prompt').autocomplete({
    source: metric_names,
    open: function(event, ui) {
      if ($('#lt-new-metric-prompt').val().length >= 3) {
        completion = $('li.ui-menu-item a').html();
        $('#lt-prompt-shadow').val(completion);
      }
    },
    close: function(event, ui) {
      completion = '';
      $('#lt-prompt-shadow').val('');
    },
  });

  $('#lt-new-metric-prompt').keypress(function(key) {
    if (key.which == 13) {
      var metric_name = '';
      if (completion != '') {
        metric_name = completion;
      } else {
        metric_name = $('#lt-new-metric-prompt').val();
      }
      addMetric(metric_name);
    }
  });
}
