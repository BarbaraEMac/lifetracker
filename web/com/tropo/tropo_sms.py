""" 
This is the script that is invoked by Tropo when our canadian SMS
number receives a text, and when prompt them to send a text via their
API. Its counterintuitive that both these cases are handled in a single
script, but you work with the API you're given.

These two cases are handled as follows. If 'currentCall' is defined it 
means the script was prompted by an incoming SMS. Otherwise, it means we 
are trying to send an SMS ourselves. Hence these two if statements.
"""

import urllib

if currentCall != None:
  if currentCall.network == "SMS":
    data = urllib.urlencode({
      'From': currentCall.callerID,
      'Body': currentCall.initialText,
    })

    response = urllib.urlopen('http://www.youaresuperhuman.com/sms/receive', data)
elif numberToDial != None and msg != None:
  call(numberToDial, {"network":"SMS"})
  say(msg)
