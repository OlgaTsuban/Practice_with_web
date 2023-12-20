from mongoengine import Document, StringField, BooleanField

# Presents atributes of document in DB 
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    preferred_contact_method = StringField(choices=['email', 'sms'], default='email')
    message_sent = BooleanField(default=False)
