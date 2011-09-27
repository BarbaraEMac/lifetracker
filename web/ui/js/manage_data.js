$(document).ready(function() {
  $('.dp-delete-button').click(delete_datapoint_click); 
  $('.new-entry-button').click(new_datapoint_click);
  $('.new-entry-submit-button').click(new_datapoint_submit_click); 
});

new_datapoint_submit_click = function() {
  query_id = $(this).attr('id').substring(24);

  // get the new dp
  text = $('#input-row-' + query_id + ' input').val();
  time = (new Date).getTime();

  dp = {
    'data': text, 
    'time': time,
    'query_id': query_id};
      
  // do some ajax
  $.ajax({
    url: 'data/newPoint',
    type: 'POST',
    data: dp,
    success: function() {
      window.location.reload(); 
    }
  });
}

new_datapoint_click = function() {
  query_id = $(this).attr('id').substring(17);

  insert_row_id = '#input-row-' + query_id;
  submit_id = '#new-entry-submit-button-' + query_id;
  new_entry_id = '#new-entry-button-' + query_id;

  $(new_entry_id).css('display', 'none');
  $(insert_row_id).css('display', 'table-row');   
  $(submit_id).css('display', 'inline');
}

delete_datapoint_click = function() {
  dp_id = $(this).attr('id').substring(7);

  data =  {
    'dp_id': dp_id,
  }

  $.ajax({
    url: 'data/deletePoint',
    type: 'POST',
    data: data,
    success: function() {
      window.location.reload(); 
    }
  });
}
