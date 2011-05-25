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
        window.location.reload();
      },
    });
    
  });
});
