$(document).ready(function() {
  $('#account-update-button').click(function() { 
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
    
  });

  if (window.location.search.indexOf('first_time') != -1) {
    intro();
  }
});

// a series of dialogs/tooltips that introduce the user to the UI
intro = function() {
  $('#first-time-dialog').css('display', 'inline');
}
