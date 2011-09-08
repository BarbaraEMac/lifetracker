metric_defaults = {
  "name": "default",
  "text": "What is the value of default right now?",
  "frequency": 1440,
  "format": "number",
  "template_id": 0,
}

$(document).ready(function() { 
  $('select.edit-frequency').each(function() {
    query_id = $(this).attr('id').substring(15);
    
    freq_minutes_id = '#freq-minutes-' + query_id;

    freq_minutes = $(freq_minutes_id).val();

    select_id = '#edit-frequency-' + query_id; 
    option_id = '#freq-' + freq_minutes;

    $(select_id + ' ' + option_id).attr('selected', 'selected');
  });

  $('.query-delete-confirm-button').click(function() {
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
  });

  $('.query-delete-button').click(function() {
    query_id = $(this).attr('id').substring(7);
    confirm_button_id = '#confirm-delete-' + query_id;
 
    $(this).css('display', 'none');
    $(confirm_button_id).css('display', 'block');
  });

  $('#new-query-create-button').click(function() {
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
  });

  $('#new-query-submit').click(function() {
    // get the data

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

    // do a post and reload the page on success
    $.ajax({
      type: 'post',
      url: 'data/newQuery',
      data: data, 
      success: function() {
          window.location = '/dashboard';
        },
    });
  });

  $('.query-edit-button').click(function() {
    query_id = $(this).attr('id').substring(5);
    metric_id = '#metric-' + query_id;

    // collapse any other expanded edit-tabs

    $('.metric.editing').animate({
      height: '100px',
    });

    $('.metric.editing').removeClass('editing');
  
    // expand this tab

    $(metric_id).animate({
      height: '170px',
    }, 200);

    $(metric_id).addClass('editing');
  });

  $('.query-edit-submit-button').click(function() {
    query_id = $(this).attr('id').substring(7);
    
    // get the new values from the fields.
  
    name_id = '#edit-name-' + query_id;
    text_id = '#edit-text-' + query_id;
    frequency_id = '#edit-frequency-' + query_id;

    new_name = $(name_id).val();
    new_text = $(text_id).val();
    new_frequency = $(frequency_id + ' :selected').attr('id').substring(5);

    new_query_data = {
      'query_id': query_id,
      'name': new_name,
      'text': new_text,
      'frequency': new_frequency,
    };

    // do some ajax shit in here.
    $.ajax({
      url: 'data/editQuery',
      type: 'POST',
      data: new_query_data,
      success: function() {
        window.location = '/dashboard';
      },
    });
  });

  $('a.data-button').click(function() {
    query_id = $(this).attr('id').substring(5);

    // get the data
    new_query_data = {
      'query_id': query_id,
    };

    // do some ajax shit in here.
    $.ajax({
      url: 'data/pointsForQuery',
      type: 'GET',
      data: new_query_data,
      success: function(response) {
        // expand the thingy
        metric_id = '#metric-' + query_id;
        raw_data_container = '#raw-data-' + query_id;

        data = eval(response);

        $(metric_id).css('height', '500px');

        // populate it into a div underneath the thing
        for (index in data) {
          row = "<tr><td>" + data[index]['timestamp'] + "</td><td>" + data[index]['text'] + "</td><td><a id='delete-"+ data[index]['dp_id'] + "' class='dp-delete-button' href='#'>Delete</a></td></tr>";
          $(raw_data_container).append(row);
        }
      },
    });

    // populate it into a div underneath the thing
  });

  $('a.analyze-button').click(function() {
    query_id = $(this).attr('id').substring(8);
    metric_id = '#metric-' + query_id;
    analytics = '#analytics-' + query_id;

    // collapse all other analytics tabs
    $('div.metric.analyzing').animate({
      height: '100px',
    }, 250);

    $('div.metric.analyzing').removeClass('analyzing');

    // expand this analytics tab

    $(metric_id).animate({
      height: '500px',
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
            if (index > 7) break; // only show the top seven for now.
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

  });

  metric_names = [];
  for (name in template_metrics) {
    metric_names.push(name);
  }


  $('#lt-new-metric-prompt').autocomplete({
    source: metric_names,
  });

  $('#lt-new-metric-prompt').keypress(function(key) {
    if (key.which == 13) {
      metric_name = $('#lt-new-metric-prompt').val();
      addMetric(metric_name);
    }
  });

  if (window.location.search.indexOf('first_time') != -1) {
    intro();
  } else if (window.location.search.indexOf('setup_complete') != -1) {
    intro_complete();
  }
});

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

// a series of dialogs/tooltips that introduce the user to the UI
intro = function() {
  $('#first-time-dialog').dialog({
    width: '500px',
    buttons: [{
      text: 'Let\'s do it!',
      click: function() {
        window.location = '/account?first_time=true';
      }
    }]
  });
}

addMetric = function(name) {
  var metric;

  if (template_metrics[metric_name] != undefined) {
    metric = getTemplateValues(metric_name);
  } else {
    metric = getDefaultValues(metric_name);
  }

  user_email = $('#user_email').val();

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
    success: function() {
        window.location = '/dashboard';
    }
  });
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
