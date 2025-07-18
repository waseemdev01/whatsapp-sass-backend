import os
from twilio.rest import Client
from django.template import Template, Context

def send_whatsapp_message(to, template_str, context_data):
    client = Client(
        os.environ.get('TWILIO_ACCOUNT_SID'),
        os.environ.get('TWILIO_AUTH_TOKEN')
    )

    rendered = Template(template_str).render(Context(context_data))

    message = client.messages.create(
        from_=os.environ.get('TWILIO_WHATSAPP_NUMBER'),
        body=rendered,
        to=f"whatsapp:{to}"
    )

    return message.sid
