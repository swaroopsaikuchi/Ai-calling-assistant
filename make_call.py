import requests

# Function to generate response using the local language model


# Your Vapi API Authorization token
auth_token = '1a9a3b2f-af0e-4160-8fb8-5e92275275a8'
# The Phone Number ID, and the Customer details for the call
phone_number_id = '17914db4-b20c-4911-b9d4-9918aa581b30'
customer_number = "+917207254977"

# Create the header with Authorization token
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json',
}

# Generate the message content using the local language model
# Create the data payload for the API request

data = {
    'assistant': {
        "firstMessage": "Hey, what's up?",
        "model": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"""You are an AI assistant, that helps customers for cake booking, ask questions like:
                    - what flavours do you like?
                    - Size of the cake? etc"""
                }
            ]
        },
        "voice": "jennifer-playht"
    },
    'phoneNumberId': phone_number_id,
    'customer': {
        'number': customer_number,
    },
}

"""data = {
    'assistant': {
        "firstMessage": message_content,
        "model": {
            "provider": "openai",
            #"url": "http://localhost:3000/v1",
            "model": "gpt-3.5",
            "messages": [
            {
                "role": "system",
                "content": "You are an assistant."
            }
            ],
        },
        "voice": "jennifer-playht" # Replace 'jennifer-playht' with your desired voice
    },
    
    'phoneNumberId': phone_number_id,
    'customer': {
        'number': customer_number,
    },
}
"""
# Make the POST request to Vapi to create the phone call
response = requests.post('https://api.vapi.ai/call/phone', headers=headers, json=data)

# Check if the request was successful and print the response
if response.status_code == 201:
    print('Call created successfully')
    print(response.json())
else:
    print('Failed to create call')
    print(response.text)
