#! /usr/bin/env python3
from bson.objectid import ObjectId


class COLLECTION:
    def __init__(self, name: str, vendor: str, articles: list[str] = []):
        self.name = name
        self.vendor = vendor
        self.articles = articles

    @property
    def json(self):
        return self.__dict__


class BOX:
    def __init__(self, name: str, vendor: str, x: int = 10, y: int = 10, z: int = 10):
        self.name = name
        self.vendor = vendor
        self.x = x
        self.y = y
        self.z = z

    @property
    def json(self):
        return self.__dict__

    def save(self, db):
        db.update_one(
            {"name": self.name, "vendor": self.vendor},
            {"$set": self.json},
            upsert=True,
        )
        return self


class SHOP:
    def __init__(self, shopID: str, name: str, x: int = 1000, y: int = 300):
        self.shopID = shopID
        self.name = name
        self.x = x
        self.y = y

    @property
    def json(self):
        return self.__dict__

    def save(self, db):
        db.update_one(
            {"shopID": self.name},
            {"$set": self.json},
            upsert=True,
        )
        return self


class SHOPBOX:
    def __init__(
        self,
        _id: objectId,
        index: int,
        shopID: str,
        boxID: str,
        x: int = 10,
        y: int = 10,
        h: int = 0,
        r: int = 10,
    ):
        self._id = _id  # id объекта
        self.index = index
        self.shopID = shopID
        self.x = x  # позиция на плане
        self.y = y  # позиция на плане
        self.h = h  # высота на плане
        self.r = r  # угол поворота

    @property
    def json(self):
        return {k: v for k, v in self.__dict__ if not k.startswith("_")}

    def save(self, db):
        db.update_one(
            {"_id": self._id},
            {"$set": self.json},
            upsert=True,
        )
        return self

    def create(self, db):
        ret = db.insert_one(self.json)
        print(ret)
        return self


def log():
    return


if __name__ == "__main__":

    # from db import db_box

    # boxes = [
    #     BOX("6 полок низкий 2020", "Victoria Stenova", 1240, 580, 698),
    #     BOX("6 полок высокий 2020", "Victoria Stenova", 1240, 580, 894),
    #     BOX("12 полок пристенный 2020", "Victoria Stenova", 1240, 220, 2222),
    #     BOX("6 полок пристенный 2020", "Victoria Stenova", 1240, 220, 1230),
    # ]

    # for b in boxes:
    #     b.save(db_box)
    #     print(b.__dict__)

    pass
