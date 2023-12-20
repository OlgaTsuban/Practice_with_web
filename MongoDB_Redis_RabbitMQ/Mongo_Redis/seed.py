import json
from mongoengine.errors import NotUniqueError
from Mongo_Redis.models import Author, Quote
from pymongo import MongoClient
from mongoengine import connect

uri = "mongodb+srv://tsubanolga:O1904@cluster0.yiefpq6.mongodb.net/Cluster0?retryWrites=true&w=majority"

# Establish a connection to MongoDB
connect(host=uri)

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.Cluster0

# Send a ping to confirm a successful connection 
# Is not necessary part of program
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# Get data from files .json
def import_data_from_json(json_file, model_class, related_model=None, related_field=None):
    with open(json_file, encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                # Create an instance of the main model class
                instance = model_class(**el)

                # If there is a related model and field specified, try to associate them
                if related_model and related_field:
                    related_obj, *_ = related_model.objects(fullname=el.get(related_field))
                    setattr(instance, related_field, related_obj)

                instance.save()
            except NotUniqueError:
                print(f"{model_class.__name__} already exists: {el.get('fullname')}")

if __name__ == '__main__':
        # Example usage for authors
    import_data_from_json('authors.json', Author)
        # Example usage for quotes with related author
    import_data_from_json('quotes.json', Quote, related_model=Author, related_field='author')
