from typing import List, Any
import redis
from redis_lru import RedisLRU
from Mongo_Redis.models import Author, Quote
from mongoengine import connect
from pymongo import MongoClient

# Information for connection
clients = redis.StrictRedis(host="127.0.0.1", port=6379, password=None)
cache = RedisLRU(clients)
uri = "mongodb+srv://tsubanolga:O1904@cluster0.yiefpq6.mongodb.net/Cluster0?retryWrites=true&w=majority"

# Establish a connection to MongoDB
connect(host=uri)

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.Cluster0

# Functon can find information using the tags , using cache
@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]

    # keys = clients.keys('*')
    # print(keys)

    return result

# Functon can find inform using authors , using cache
@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

# Main function, has all logic
def main():
    while True:
        try:
            args_str = input("Enter command and value (e.g., name: John): ")
            if args_str == "exit":
                print("Exiting the script.")
                break
            args_list = args_str.split(":")
            command = args_list[0].strip()
            value = args_list[1].strip()
            if command == "name":
                result = find_by_author(value)
            elif command == "tag":
                result = find_by_tag(value)
            elif command == "tags":
                # Split the comma-separated tags
                tags = value.split(",")
                result = {tag: find_by_tag(tag) for tag in tags}
            else:
                print("Invalid command.")
                continue

            print(result)
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
    