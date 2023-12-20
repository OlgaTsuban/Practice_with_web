from bson import ObjectId
import pika
from RabbitMQ_Mongo.contact_model import Contact
from mongoengine import connect

# Connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='contact_ids_email')

# This function simulates sending an email.
def send_email(email, message):
    print(f"Simulating email sent to {email}: {message}")

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
        print(f"Email sent for contact {contact_id}")

# Has main logic and set up consumer
def main():
    channel.basic_consume(queue='contact_ids', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    # Connect to Atlas MongoDB
    uri = "mongodb+srv://tsubanolga:O1904@cluster0.yiefpq6.mongodb.net/Cluster0?retryWrites=true&w=majority"
    connect(host=uri) 
    main()
