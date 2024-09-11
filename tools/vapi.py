
import requests

url = "https://api.vapi.ai/call/phone"

set_vapi = {
    'assistantId': 'xxxxx'
    'name': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    'xxxxxxx': 'xxxxx'
    }


payload = {
    "maxDurationSeconds": 1805,
    "assistantId": f"<string>",
    "assistant": {
        "name": "<string>",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "keywords": ["<string>"]
        },
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "systemPrompt": "<string>",
            "temperature": 1,
            "functions": [
                {
                    "name": "<string>",
                    "async": True,
                    "description": "<string>",
                    "parameters": {}
                }
            ]
        },
        "voice": {
            "provider": "11labs",
            "voiceId": "burt",
            "stability": 0.5,
            "similarityBoost": 0.5,
            "style": True,
            "useSpeakerBoost": True
        },
        "language": "en",
        "forwardingPhoneNumber": "<string>",
        "firstMessage": "<string>",
        "voicemailMessage": "<string>",
        "endCallMessage": "<string>",
        "interruptionsEnabled": True,
        "recordingEnabled": True,
        "endCallFunctionEnabled": True,
        "fillersEnabled": True,
        "clientMessages": ["function-call"],
        "serverMessages": ["end-of-call-report"],
        "silenceTimeoutSeconds": 305,
        "responseDelaySeconds": 5
    },
    "customerId": "<string>",
    "customer": {
        "number": "<string>",
        "name": "<string>"
    },
    "phoneNumberId": "<string>",
    "phoneNumber": {
        "twilioPhoneNumber": "<string>",
        "twilioAccountSid": "<string>",
        "twilioAuthToken": "<string>",
        "name": "<string>",
        "assistantId": "<string>"
    }
}
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)


# =============================================================================
# from vapi_python import Vapi
# 
# import vapi_python
# 
# vapi_python
# 
# 
# # Initialize Vapi with your API key
# vapi = Vapi(api_key='your-public-key')
# 
# # Define your assistant (or use an existing assistant ID)
# assistant = {
#   'firstMessage': 'Hey, how are you?',
#   'context': 'You are an employee at a drive thru...',
#   'model': 'gpt-3.5-turbo',
#   'voice': 'jennifer-playht',
#   "recordingEnabled": True,
#   "interruptionsEnabled": False
# }
# 
# # Start the call
# vapi.start(assistant=assistant)
# 
# 
# vapi.start(assistant_id='your-assistant-id')
# 
# 
# import requests
# 
# # Your Vapi API Authorization token
# auth_token = '<YOUR AUTH TOKEN>'
# # The Phone Number ID, and the Customer details for the call
# phone_number_id = '<PHONE NUMBER ID FROM DASHBOARD>'
# customer_number = "+14151231234"
# 
# # Create the header with Authorization token
# headers = {
#     'Authorization': f'Bearer {auth_token}',
#     'Content-Type': 'application/json',
# }
# 
# # Create the data payload for the API request
# data = {
#     'assistant': {
#         "firstMessage": "Hey, what's up?",
#         "model": {
#             "provider": "openai",
#             "model": "gpt-3.5-turbo",
#             "messages": [
#                 {
#                     "role": "system",
#                     "content": "You are an assistant."
#                 }
#             ]
#         },
#         "voice": "jennifer-playht"
#     },
#     'phoneNumberId': phone_number_id,
#     'customer': {
#         'number': customer_number,
#     },
# }
# 
# # Make the POST request to Vapi to create the phone call
# response = requests.post(
#     'https://api.vapi.ai/call/phone', headers=headers, json=data)
# 
# # Check if the request was successful and print the response
# if response.status_code == 201:
#     print('Call created successfully')
#     print(response.json())
# else:
#     print('Failed to create call')
# =============================================================================
    print(response.text)