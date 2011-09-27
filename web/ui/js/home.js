metrics = new Array();

$(document).ready(function() {
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
        <a id='data-%(query_id)s' class='data-button' href='#'>Data</a>\
        <a id='edit-%(query_id)s' class='query-edit-button' href='#'>Edit</a>\
        <a id='submit-%(query_id)s' class='query-edit-submit-button' href='#'>Submit</a>\
        <a id='delete-%(query_id)s' class='query-delete-button' href='#'>Delete</a>\
        <a id='confirm-delete-%(query_id)s' class='query-delete-confirm-button' href='#'>Really?</a>\
      </div>\
    </div>\
"
}

addMetric = function(metric_name) {
  metric = template_metrics[metric_name];
  if (template_metrics[metric_name] != undefined) {
    // get the metric from template_metrics
  } else {
    // build it on the page such that the user has to enter in the custom fields
  }
  $('#query-list').prepend(newQuery(metric));
}

showDashboard = function() {
  $('#lt-header').css('display', 'none');
  $('#lt-title-container').css('display', 'none');

  $('#lt-splash').addClass('adding');
  $('#lt-prompt-text').html("What else?");
  $('#dashboard').css('display', 'block');
}

new_metric_prompt_init = function() {
  metric_names = [];
  for (name in template_metrics) {
    metric_names.push(name);
  }

  $('#lt-prompt').autocomplete({
    source: metric_names,
  });

  $('#lt-prompt').keypress(function(key) {
    if (key.which == 13) {
      // transition to the thingy
      metric_name = $('#lt-prompt').val();
      
      // ifs around this
      metrics.push(template_metrics[metric_name]);

      addMetric(metric_name);
      $('#lt-prompt').val('');

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
