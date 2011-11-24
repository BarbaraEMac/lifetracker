program = 'casual';
sms = '';
email = '';
invite_code = '';

// this function is called from within the login iframe when the login 
// succeeds
to_dashboard = function() {
  window.location = 'dashboard?first_time=true';
}

// can't believe there ins't a jquery function for onload. sucks.
window.onload = (function() {
  // I wonder if there's a better way to do this
  $('.section').each(function() {
    $(this).click(function(event) {
      event.preventDefault();
      program_click($(this));
    });
  });

  $('#sms, #email').keypress(function(key) {
    if (key.which == 13) {
      sms_email_enter();
    }
  });

  $('#takealook').click(takealook_click);
  $('#contact-next').click(sms_email_enter);

  check_for_invite()
});

check_for_invite = function() {
  if (window.location.toString().indexOf('invite_code=') != -1) {
    start = window.location.toString().indexOf('invite_code=') + 12;
  
    invite_code = window.location.toString().substr(start);
  }
}

takealook_click = function(obj) {
  $('#hook').animate({
    opacity: 0,
  }, 500, function() {
    $('#hook').css('display', 'none');
    $('#hook').removeClass('active');

    $('#about-metrics').css('display', 'block');
    $('#about-metrics').addClass('active');
  });
}

program_click = function(obj) {
  program = $(obj).attr('id');

  $('#about-metrics').animate({
    opacity: 0,
  }, 500, function() {
    $('#about-metrics').css('display', 'none');
    $('#about-metrics').removeClass('active');

    $('#contact').css('display', 'block');
    $('#contact').addClass('active');
  });
}

sms_email_enter = function(event) {
  sms = $('#sms').val();
  email = $('#email').val();

  host = window.location.host;
  callback = 'http://' + host + "/firstTimeUser?";
  callback += 'sms=' + sms;
  callback += '&program=' + program;
  if (invite_code != '') {
    callback += '&invite_code=' + invite_code;
  }
  data = {"url": callback}

  // ajax to get the login url
  $.ajax({
    url: 'loginURL',
    data: data,
    success: function(response) {
      // on success, show the intro dialog then redirect to the login
      // page
      callback_url = response;
  
      $('#contact').removeClass('active');
      $('#contact').css('display', 'none');

      $('#metrics-container').removeClass('active');
      $('#metrics-container').css('display', 'none');

      $('#login-container').addClass('active');

      window.setTimeout(function() {
        window.location = callback_url;
      }, 4000);

    }, // success
  }); // ajax
}
