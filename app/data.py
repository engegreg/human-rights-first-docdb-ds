"""
Labs DS Data Engineer Role
- Database Interface
- Visualization Interface
"""
from os import getenv
from typing import Iterator, Dict, Iterable, Optional

from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv


class Data:
    """ MongoDB Data Model """
    load_dotenv()
    db_url = getenv("DB_URL", default="mongodb://localhost:27017/")
    db_name = getenv("DB_NAME", default="DocDB")
    db_table = getenv("DB_TABLE", default="docs")

    def connect(self):
        return MongoClient(self.db_url)[self.db_name][self.db_table]

    def find(self, query: Dict, projection: Dict = None) -> Iterator[Dict]:
        return self.connect().find(query, projection)

    def find_one(self, query: Dict, projection: dict = None) -> Optional[Dict]:
        return self.connect().find_one(query, projection or {"_id": False})

    def insert(self, data: Iterable[Dict]):
        self.connect().insert_many(data)

    def update(self, query: Dict, data_update: Dict):
        self.connect().update_one(query, {"$set": data_update})

    def delete(self, query: Dict):
        self.connect().delete_many(query)

    def df(self) -> pd.DataFrame:
        return pd.DataFrame(self.find({}, {"_id": False}))

    def count(self, query: Dict) -> int:
        return self.connect().count_documents(query)

    def search(self, search: str, projection: dict = None):
        return self.find({"$text": {"$search": search}}, projection or {"_id": False})

    def add_tag(self, file_id: str, new_tag: str):
        self.connect().update({'id': file_id}, {'$push': {'tags': new_tag}})

    def __str__(self):
        return f"{self.df()}"


if __name__ == '__main__':
    db = Data()

    # db.delete({})

    # text_index_name = list(db.connect().index_information().keys())[1]
    # db.connect().drop_index(text_index_name)

    # db.connect().create_index([("$**", "text")])

    # db.insert([
    #     {"FilePath": "S3::Documents/Images/Test00.jpg", "Content": "This is an image"},
    #     {"FilePath": "Box::Documents/PDFs/Test01.pdf", "Content": "This is a text document"},
    #     {"FilePath": "Box::Documents/PDFs/Test02.pdf", "Content": "This is a text document"},
    #     {"FilePath": "Box::Documents/PDFs/Test03.pdf", "Content": "This is a text document"},
    #     {"FilePath": "Box::Documents/PDFs/Test04.pdf", "Content": "This is a text document"},
    # ])
    # query = {
    #     'id' = ['76743684225'']
    # }
    # file_id = '23511711927'
    # result = db.find({"id": file_id}, {"_id": False})
    # print(type(result[0]))
    # for item in result:
    #     print(item)
