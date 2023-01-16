import os
from twilio.rest import Client
import string
from random import choice

def send_otp(to_phno):
    if not to_phno.startswith('+91'):
        to_phno = '+91' + to_phno 
    otp =  ''.join(choice(string.digits) for _ in range(4))
    try:
        account_sid = 'ACa6bf7e3b7e1b3da0314576c5f4d04bd9'
        auth_token = 'b45390b278ed2cb1031c73f0816fecb3'
        client = Client(account_sid, auth_token)
        client.messages.create(from_="+12342184225",
                               to=str(to_phno),
                               body='OTP for login - '+str(otp))
        return {'Success':True,'otp':otp}
    except Exception as e:
        return {'Success':False,'error':e}