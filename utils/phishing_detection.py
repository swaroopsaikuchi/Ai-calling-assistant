import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import openai
import time
import os

from email.parser import BytesParser
#openai.api_key = ''

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('', '')
mail.select('inbox')
subject = "salon appointment"

result, data = mail.uid('search', None, 'ALL')
uids = data[0].split()
print(f"UIDs: {uids}")

uids = [b'1']
# Loop through each uid to fetch headers and bodies
for uid in uids:
    result, data = mail.uid('fetch', uid, '(RFC822)')
    if result == 'OK':
        raw_email = data[0][1]
        #print(raw_email)
        #email_message = email.message_from_bytes(raw_email)
        email_message = """--0000000000000182ea061466e4c3
            Content-Type: text/plain; charset="UTF-8"

            You can call me Carla. I am a traditional  type of a girl . I want a long
            lasting  partnership  that will be romantic every step of the way . I
            believe I will make my  mate happy.
            You could be the man that makes me {happy | satisfied | pleased) to be in
            the location , Sign up for the website. <https://bit.ly/3Pci7SV>

            --0000000000000182ea061466e4c3
            Content-Type: text/html; charset="UTF-8"
            Content-Transfer-Encoding: quoted-printable

            <div dir=3D"ltr">You can call me Carla. I am a traditional =C2=A0type of a =
            girl . I want a long lasting =C2=A0partnership =C2=A0that will be romantic =
            every step of the way . I believe I will make my =C2=A0mate happy.<div><a h=
            ref=3D"https://bit.ly/3Pci7SV">You could be the  man that makes me {happy |=
            satisfied | pleased) to be in the  location , Sign up for the website.</a>=
            <br></div></div>

            --0000000000000182ea061466e4c3--"""
        email_message = BytesParser().parsebytes(email_message.encode())
        #print(email_message.walk())
        
        #print(email_message)

        # Extract conversation history from email body

        #conversation_history = ''
        for part in email_message.walk():
            #print('-------------------------------------------------------------------------------------------------------------------')
            #print(part)
            if part.get_content_type() == 'text/plain':
                #print(f"Payload: {part.get_payload(decode=True).decode()}")
                conversation_history = f"{part.get_payload(decode=True).decode()}"
                #print(f"Conversation history: {conversation_history}")
        

        # Extract sender's email address
        sender_email = email_message['From']

        

        # Construct the prompt including conversation history and sender's email address
        #prompt = f"Email Message: {email_message}. Sender's email: {sender_email}. Analyze whether the given email corresponds to phishing or contains any malicious content."
        prompt = f"Conversation history: {conversation_history}. Sender's email: {sender_email}. Analyze whether the given email corresponds to phishing or contains any malicious content."
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=250
        )
        reply_text = response.choices[0].text.strip()
        print(f"Generated reply: {reply_text}")
        print("--------------------------------------------------------------------------------------------------------------------------------------------")
# Logout from IMAP server
mail.close()
mail.logout()
