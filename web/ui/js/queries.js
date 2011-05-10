$(document).ready(function() {
  $('#new-query-create-button').click(function() {
    $('tr#query-input-row').css('display', 'table-row');
    $('#new-query-create-button').css('display', 'none');
  });

  $('#new-query-submit').click(function() {
    // get the data

    new_name = $('#new-query-name-input').val();
    new_text = $('#new-query-text-input').val();
    new_frequency = $('#new-query-frequency-input').val();
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
          window.location.reload() 
        },
    });
  });

  $('.query-edit-button').click(function() {
    query_id = $(this).attr('id').substring(5);
   submit_id = '#submit-' + query_id;
    edit_id = '#edit-' + query_id;
    tr_id = '#' + query_id;

    $(edit_id).css('display', 'none');
    $(submit_id).css('display', 'inline');
    $(tr_id + ' p').css('display', 'none');
    $(tr_id + ' input.query-edit-field').css('display', 'inline');  
  });

  $('.query-edit-submit-button').click(function() {
    query_id = $(this).attr('id').substring(7);
    
    // get the new values from the fields.
  
    name_id = '#edit-name-' + query_id;
    text_id = '#edit-text-' + query_id;
    frequency_id = '#edit-frequency-' + query_id;

    new_name = $(name_id).val();
    new_text = $(text_id).val();
    new_frequency = $(frequency_id).val();

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
        window.location.reload();
      },
    });

    submit_id = '#submit-' + query_id;
    edit_id = '#edit-' + query_id;
    tr_id = '#' + query_id;

    $(edit_id).css('display', 'inline');
    $(submit_id).css('display', 'none');
    $(tr_id + ' p').css('display', 'inline');
    $(tr_id + ' input.query-edit-field').css('display', 'none');  
  });
});
