from faker import Faker
from typing import Sequence, Mapping
import hashlib
import random
import psycopg2.extras
from utils.postgres_connector import PostgresConnector
from faker import Faker
from typing import Sequence, Mapping
import hashlib
import random
import psycopg2.extras


class PSQLManager:

    def create_tables(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        with open("./init/tables_creation_script.sql", "r") as tables_creation_cript:
            cursor.execute(tables_creation_cript.read())
        cursor.connection.commit()
        connector.close_connection()

    def insert_data_to_table(self, db_name: str, table_name: str, data: Sequence[Mapping]) -> None:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)
        cursor.connection.commit()
        connector.close_connection()

    def insert_connections(self, db_name: str, table_name: str, data: Sequence[Mapping]) -> None:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)
        cursor.connection.commit()
        connector.close_connection()


class DataFaker():

    def get_fake_users(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        users: Sequence[Mapping] = []
        for _ in range(count):
            user = self.create_fake_user(fake)
            users.append(user)
        return users

    def create_fake_user(self, fake: Faker) -> Mapping:
        user: dict = {}
        user_name: str = fake.unique.user_name()
        full_name: Sequence[str] = fake.unique.name().split()[:2]
        second_name: str = full_name[0]
        first_name: str = full_name[1]
        password: str = fake.unique.password()
        hashed_password: str = hashlib.sha256(password.encode()).hexdigest()
        user["user_name"], user["first_name"], user["second_name"], user["password"] = user_name, first_name, second_name, hashed_password
        return user

    def get_fake_chats(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        chats: Sequence[Mapping] = []
        for _ in range(count):
            chat = {
                "chat_name": fake.unique.company(),
                "mongo_id": fake.unique.sbn9(),
                "is_group": str(random.getrandbits(1)),
            }
            chats.append(chat)

        return chats

    def get_fake_chats_members(self, db_name) -> Mapping:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()

        user_ids_sql = "SELECT user_id FROM users"
        cursor.execute(user_ids_sql)
        user_ids: Sequence[int] = [i[0] for i in cursor.fetchall()]

        chats_info_sql = "SELECT chat_id, is_group FROM chats;"
        cursor.execute(chats_info_sql)
        chats_info = cursor.fetchall()
        chat_members: Mapping = {}
        for chat_id, is_group in chats_info:
            flag = 1
            if is_group == "1":
                num_users = random.randint(1, len(user_ids))
                members = random.sample(user_ids, num_users)
            else:
                for _ in range(10):
                    members = random.sample(user_ids, 2)
                    for members_list in chat_members.values():
                        if members_list == members:
                            flag = 0
                    if flag == 1:
                        break
            if flag == 0:
                members = random.sample(user_ids, 1)
            chat_members[chat_id] = members
        return chat_members


class Initializer:

    def init_data(self):
        print("Start initializing")
        db_worker = PSQLManager()
        db_name = "messenger_db"
        creater_data = DataFaker()
        db_worker.create_tables(db_name)
        fake_users: Sequence[Mapping] = creater_data.get_fake_users(10)
        fake_chats: Sequence[Mapping] = creater_data.get_fake_chats(10)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="users", data=fake_users)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="chats", data=fake_chats)

        print("Succesfully inited")


Initializer().init_data()
