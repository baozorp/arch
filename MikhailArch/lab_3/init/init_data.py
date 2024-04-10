from faker import Faker
from pymongo import MongoClient
import random
from datetime import datetime, timedelta


class MongoConnector:
    _instance = None

    @classmethod
    def get_collection(cls):
        if cls._instance is None:
            username = "root"
            password = "example"
            mongo_uri = f"mongodb://{username}:{password}@mongo:27017/"
            cls._instance = MongoClient(mongo_uri)
        database = cls._instance["arch"]
        collection = database["chats"]
        return collection


chats_collection = MongoConnector.get_collection()


class Initializer():

    @staticmethod
    def random_date(start_date, end_date):
        time_between_dates = end_date - start_date
        random_number_of_days = random.randrange(time_between_dates.days)
        random_date = start_date + timedelta(days=random_number_of_days)
        return random_date

    @staticmethod
    def generate_chat():
        fake = Faker()
        chat = {}
        chat['is_PtP'] = random.choice([True, False])
        admins = []
        members = []
        if chat['is_PtP']:
            admins.append(fake.unique.pyint(min_value=0, max_value=9999))
            admins.append(fake.unique.pyint(min_value=0, max_value=9999))
            members = admins.copy()
        else:
            while len(admins) < random.randint(1, 5):
                admins.append(fake.unique.pyint(min_value=0, max_value=9999))
            members = set(admins)
            while len(members) < random.randint(2, 50):
                members.add(random.randint(1, 10000))
            members = list(members)
        print(chat['is_PtP'], members)
        chat['admins'] = admins
        chat['members'] = members
        chat['chat_name'] = 'Chat_' + fake.company()
        chat['messages'] = []
        for _ in range(random.randint(10, 100)):
            message = {}
            message['message_text'] = fake.text()
            message['send_date'] = Initializer.random_date(
                datetime(2022, 1, 1), datetime.now())
            message['member'] = random.choice(chat['members'])
            chat['messages'].append(message)

        return chat

    def generate_chats(num_chats):
        return [Initializer.generate_chat() for _ in range(num_chats)]


num_chats = 100
chats = Initializer.generate_chats(num_chats)
chats_collection.insert_many(chats)
