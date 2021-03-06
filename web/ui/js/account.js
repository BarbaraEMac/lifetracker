first_time = false;

$(document).ready(function() {
  $('#account-update-button').click(update_button_click);

  if (window.location.search.indexOf('first_time') != -1) {
    first_time = true;
    intro();
  }
});

// a series of dialogs/tooltips that introduce the user to the UI
intro = function() {
  $('#first-time-dialog').css('display', 'inline');
}

update_button_click = function(event) {
  event.preventDefault();
  user_email = $('#user_email').val()
  // get the phone number and the medium
  phone_number = $('#phone-number').val();
  
  medium = $('#query-medium').val()
  if (medium != 'SMS' && medium != 'email') {
    return;
  }

  if (medium == 'sms' && phone_number.length < 10) {
    alert('sms requires a valid phone number!');
    return;
  }

  // post them to /updateAccount
  data = {
    'phone_number': phone_number,
    'medium': medium,
    'user_email': user_email,
  }

  if (first_time) {
    data['first_time'] = true;
  }

  $.ajax({
    url: 'account/update',
    type: 'post',
    data: data,
    success: function () {
      if (window.location.search.indexOf('first_time') != -1) {
        window.location = '/dashboard?setup_complete=true';
      } else {
        window.location.reload();
      }
    },
  });
}
