$(document).ready(function() {
  $('.new-entry-button').click(function() {
    query_id = $(this).attr('id').substring(17);

    insert_row_id = '#input-row-' + query_id;
    submit_id = '#new-entry-submit-button-' + query_id;
    new_entry_id = '#new-entry-button-' + query_id;

    $(new_entry_id).css('display', 'none');
    $(insert_row_id).css('display', 'inline');   
    $(submit_id).css('display', 'inline');
   
    // do this as we send it 
    //$('.input-row .date-cell').html((new Date).getTime());
  });

  $('.new-entry-submit-button').click(function() {
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
  });
});
