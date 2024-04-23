from bson import ObjectId
from connector.mongo_conn import MongoConnector
from models.message_model import Message
from models.chats_model import ChatModel


class ChatHandler:
    _collection = None

    def __new__(cls):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        return cls._instance

    @classmethod
    async def get_chat(cls, chat_id: str):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        chat = await cls._collection.find_one({"_id": ObjectId(chat_id)})
        print(chat)
        if chat:
            chat["_id"] = str(chat["_id"])
        return chat

    @classmethod
    async def get_chats(cls, limit: int, offset: int):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        chats = await cls._collection.find().skip(offset).limit(limit).to_list(length=None)
        for chat in chats:
            chat["_id"] = str(chat["_id"])
        return chats

    @classmethod
    async def change_chat_name(cls, chat_id: str, name):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        filter_query = {"_id": ObjectId(chat_id)}
        update_query = {"$set": {"chat_name": name}}
        chat = await cls._collection.update_one(filter_query, update=update_query)
        return chat

    @classmethod
    async def add_message(cls, chat_id: str, message: Message):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        filter_query = {"_id": ObjectId(chat_id)}
        update_query = {"$push": {"messages": Message.model_dump(message)}}
        chat = await cls._collection.update_one(filter_query, update=update_query)
        return chat

    @classmethod
    async def add_member(cls, chat_id: str, member: int):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        filter_query = {"_id": ObjectId(chat_id)}
        update_query = {"$push": {"members": member}}
        chat = await cls._collection.update_one(filter_query, update=update_query)
        return chat

    @classmethod
    async def add_chat(cls, chat: ChatModel):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        print(chat)
        print(ChatModel.model_dump(chat))
        result = await cls._collection.insert_one(ChatModel.model_dump(chat))
        inserted_id = str(result.inserted_id)
        return inserted_id


# async def main():
#     # pass
#     # print(await ChatHandler.get_chat(id="66176ae227d08c2528be32e4",))
#     message_dict = {
#         "message_text": "new_message",
#         "send_date": datetime.now(),
#         "member": 10
#     }
#     chat = {
#         "admins": [1, 2],
#         "members": [1, 2],
#         "chat_name": "Guys",
#         "messages": [message_dict],
#         "is_PtP": True
#     }
#     print(await ChatHandler.add_chat(chat=chat))


# asyncio.run(main=main())
