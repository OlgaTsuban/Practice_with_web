from bson import ObjectId
import pika
from RabbitMQ_Mongo.contact_model import Contact
from mongoengine import connect

# Connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Declare the queues
channel.queue_declare(queue='contact_ids_email')
channel.queue_declare(queue='contact_ids_sms')

 # This function simulates sending an email.
def send_email(email, message):
    print(f"Simulating email sent to {email}: {message}")

# This function simulates sending an SMS.
def send_sms(phone_number, message):
    print(f"Simulating SMS sent to {phone_number}: {message}")

# This function is intended to be called when a message is received 
# from the RabbitMQ queue, and it processes the message by sending 
# an email to the contact specified in the message.
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=ObjectId(contact_id)).first()
    if contact and not contact.message_sent:
        send_email(contact.email, "Your message content goes here.")
        contact.message_sent = True
        contact.save()
        print(f"Message sent for contact {contact_id}")

# Set up the consumer and manages queues, has main logic
def main():
    contacts = Contact.objects()
    for contact in contacts:
        contact_id = str(contact.id)
        if contact.preferred_contact_method == 'email':
            channel.basic_publish(exchange='', routing_key='contact_ids_email', body=contact_id)
        elif contact.preferred_contact_method == 'sms':
            channel.basic_publish(exchange='', routing_key='contact_ids_sms', body=contact_id)
    connection.close()

if __name__ == '__main__':
    # Establish a connection to MongoDB
    uri = "mongodb+srv://tsubanolga:O1904@cluster0.yiefpq6.mongodb.net/Cluster0?retryWrites=true&w=majority"
    connect(host=uri) 
    main()
