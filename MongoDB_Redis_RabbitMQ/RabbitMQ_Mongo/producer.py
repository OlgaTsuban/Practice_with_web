from faker import Faker
import pika
from RabbitMQ_Mongo.contact_model import Contact
from mongoengine import connect

fake = Faker()

# Generate fake contacts
def generate_fake_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        contact_data = {
            'full_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'preferred_contact_method': fake.random_element(elements=('email', 'sms'))
        }
        contacts.append(contact_data)
    return contacts

# Save contacts tp DB
def save_contacts_to_db(contacts):
    for contact_data in contacts:
        contact = Contact(**contact_data)
        contact.save()

# Send object id to queue RabbitMQ
def send_contact_ids_to_queue(contacts):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='contact_ids')

    for contact_data in contacts:
        contact_id = str(Contact.objects.get(email=contact_data['email']).id)
        channel.basic_publish(exchange='', routing_key='contact_ids', body=contact_id)

    connection.close()

if __name__ == '__main__':
    num_fake_contacts = 5
    fake_contacts = generate_fake_contacts(num_fake_contacts)
    # Connect with MongoDB and writing faking contacts
    uri = "mongodb+srv://tsubanolga:O1904@cluster0.yiefpq6.mongodb.net/Cluster0?retryWrites=true&w=majority"
    # Establish a connection to MongoDB
    connect(host=uri)   
    
    save_contacts_to_db(fake_contacts)

    send_contact_ids_to_queue(fake_contacts)
