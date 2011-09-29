// apparently javascript doesn't have native deep-cloning for objects.
// that's stupid, so this is unelegant.
cloneMetric = function(oldMetric) {
  var new_metric = {}; 
  for (prop in oldMetric) {
    new_metric[prop] = oldMetric[prop];
  }
  return new_metric;
}

metrics = new Array();

metric_defaults = {
  "name": "default",
  "text": "What is the value of default right now?",
  "frequency": 1440,
  "format": "number",
  "template_id": 0,
}

// can't believe there ins't a jquery function for onload. sucks.
window.onload = (function() {
  $('#lt-prompt-shadow').offset($('#lt-prompt').offset());
  $('#lt-prompt-shadow').css('display', 'block');
  // don't let us focus the shadow input
  $('#lt-prompt-shadow').focus(function() { $('#lt-prompt').focus() });
  $('#lt-prompt').focus();
  new_metric_prompt_init(); 
});

newQuery = function(metric) {
  return "\
    <div id='metric-%(query_id)s' class='metric'>\
      <input type='hidden' id='metric-%(query_id)s-type' value='%(format)s'/>\
      <div class='metric-name-container'>\
        <h3 id='metric-%(query_id)s-name' class='metric-name'>" 
        + metric['name'] +  
        "</h3>\
        <input type='text' value='" + name + "' id='edit-name-%(query_id)s' class='edit-field edit-name'/>\
      </div>\
      <div class='metric-snapshot'>\
        <p class='overview-metric'>Current: None yet!</p>\
        <p class='overview-metric'>Analytics: None yet!</p> \
      </div>\
      <div class='metric-options'>\
        <a id='analyze-%(query_id)s' class='analyze-button' href='#'>Analyze</a>\
        <a id='edit-%(query_id)s' class='query-edit-button' href='#'>Edit</a>\
        <a id='submit-%(query_id)s' class='query-edit-submit-button' href='#'>Submit</a>\
        <a id='delete-%(query_id)s' class='query-delete-button' href='#'>Delete</a>\
        <a id='confirm-delete-%(query_id)s' class='query-delete-confirm-button' href='#'>Really?</a>\
      </div>\
    </div>\
"
}

showDashboard = function() {
  $('#lt-header').css('display', 'none');
  $('#lt-title-container').css('display', 'none');

  $('#lt-splash').addClass('adding');
  $('#lt-prompt-text').html("What else?");
  $('#dashboard').css('display', 'block');
  $('#example').css('display', 'none');
  $('#lt-prompt-shadow').offset($('#lt-prompt').offset());
}

// The current autocomplete. If the user hits 'enter' while this is non-
// empty, we take the completion to be what the user meant
completion = ''

new_metric_prompt_init = function() {
  metric_names = [];
  for (name in template_metrics) {
    metric_names.push(name);
  }

  $('#lt-prompt').autocomplete({
    source: metric_names,
    open: function(event, ui) {
      if ($('#lt-prompt').val().length >= 3) {
        completion = $('li.ui-menu-item a').html();
        $('#lt-prompt-shadow').val(completion);
      }
    },
    close: function(event, ui) {
      completion = '';
      $('#lt-prompt-shadow').val('');
    },
  });

  $('#lt-prompt').keypress(function(key) {
    if (key.which == 13) {
      var metric_name = '';
      if (completion != '') {
        metric_name = completion;  
      } else {
        metric_name = $('#lt-prompt').val();
      }

      addMetric(metric_name);

      $('#lt-prompt').val('');
      $('#lt-prompt-shadow').val('');
      $('#lt-prompt').autocomplete("close");

      if ($('.metric').size() >= 3) {
        $('#lt-splash').addClass('hidden');

        host = window.location.host;
        callback = 'http://' + host + "/firstTimeUser?";
        callback += 'metrics=' + JSON.stringify(metrics);
        data = {"url": callback}

        // ajax to get the login url
        $.ajax({
          url: 'loginURL',
          data: data,
          success: function(response) {
            // on success, show the intro dialog then redirect to the login
            // page
            callback_url = response;

            $('#dialog').dialog({
              width: '500px',
              buttons: [{
                text: 'Let\'s do it!',
                click: function() {
                  window.location = callback_url;
                }
              }]
            }); // dialog
          }, // success
        }); // ajax
      }

      showDashboard();
    }
  }); 
}

addMetric = function(metric_name) {
  var metric = {};

  if (template_metrics[metric_name.toLowerCase()] != undefined) {
    metric = getTemplateValues(metric_name.toLowerCase());
  } else {
    metric = getDefaultValues(metric_name);
  }

  metrics[metrics.length] = cloneMetric(metric);
  $('#query-list').prepend(newQuery(metric));
}

getDefaultValues = function(metric_name) {
  var new_metric = metric_defaults;
  new_metric["name"] = metric_name;
  new_metric["text"] = "What is the value of " + metric_name + " right now?";
  return new_metric;
}

getTemplateValues = function(template_name) {
  return template_metrics[template_name];
}
