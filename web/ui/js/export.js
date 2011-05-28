$(document).ready(function() {
  query_id = $('#query-id').val();

  data = {
    query_id: query_id,
  }

  // it would be better to do this server side, for sure.  
  $.ajax({
    url: 'data/export',
    type: 'get',
    data: data, 
    success: function(response) {
      $('#export-textarea').html(response);
    },
  });


});
