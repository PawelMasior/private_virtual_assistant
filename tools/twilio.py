# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from typing import Annotated, Literal
twilioAccountSid = os.environ["twilioAccountSid"]
twilioAuthToken = os.environ["twilioAuthToken"]

client_twilio = Client(twilioAccountSid, twilioAuthToken)
# twilio_nr = '+48732096499'
# receive_nr = "+48665937049"

def sms_send(
        body_msg: Annotated[str, "Describe the specific action being taken with general context"],
        to_nr: Annotated[str, "Phone number of the receipient, ex. +48665937049"],
        from_nr: Annotated[str, "Phone number of the sender, ex. +48732096499"] = '+48732096499',
        ) -> str:
    try:
      client_twilio.messages.create(
          body=body_msg,
          to=to_nr,
          from_=from_nr
        )
      return f'Success: SMS sent to {to_nr}'
    except Exception as e:
        return f"Error: {str(e)[:200]}"

def sms_inbox(
        limit_nr: Annotated[int, "Number of messages to retrive, default 5"] = 5,
        direction:  Annotated[str, "Direction of SMS: 'inbound', 'outbound' or 'all'; default 'inbound'"] = 'inbound',
        ) -> str:  
    if not direction in ['inbound', 'outbound', 'all']:
        return f"Error: direction argument has to be 'inbound' or 'outbound'"
    
    try:
        messages = client_twilio.messages.list(limit=limit_nr)
        if not len(messages):
            msg = 'No inbound SMS available.'
        else:
            data = []
            for m in messages:
                if direction in m.direction or direction=='all':
                    
                    data += [{
                        #'to': m.to,
                        'from': m.from_,
                        'body': m.body,
                        'date_sent': m.date_sent.strftime('%Y/%m/%d %H:%M:%S'),
                        #'direction': m.direction,
                        }]
            if not len(data):
                msg = 'No inbound SMS available.'     
            else:   
                msg = f"Latest inboud SMS list:\n"
                msg+= '\n'.join(str(d) for d in data)
    except Exception as e:
        msg = f"Error: {str(e)[:200]}"
    return msg

# =============================================================================
# direction = 'all'
# limit_nr = 2
# print(sms_inbox(limit_nr, direction))
# =============================================================================
# =============================================================================
# sms_send(
#     body_msg=""" 
#     Hi - its John Smith, your ai agent from Pawel Masior.
#     I confirm our meeting at 1.30pm. See you!
#     """,
#     to_nr = "+48665937049",
#     from_nr = "+48732096499",
#     )
# =============================================================================
# =============================================================================
# from datetime import datetime, timedelta
# date_from = datetime.today() - timedelta(days=1)
# date_from = datetime(2024, 9, 2)
# =============================================================================
