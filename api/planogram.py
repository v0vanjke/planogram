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
    def __init__(
        self,
        _id: ObjectId,
        name: str,
        vendor: str,
        x: int = 10,
        y: int = 10,
        z: int = 10,
        shelf: int = 1,
        volume: int = 1,
    ):
        self._id = _id
        self.name = name
        self.vendor = vendor
        self.x = x
        self.y = y
        self.z = z
        self.shelf = shelf  # кол-во полок
        self.volume = volume  # объем

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
    def __init__(
        self, _id: ObjectId, shopID: str, name: str, x: int = 1000, y: int = 300
    ):
        self._id = _id
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
        _id: ObjectId,
        index: int,
        shopID: str,
        boxID: ObjectId,
        x: int = 10,
        y: int = 10,
        h: int = 0,
        r: int = 10,
        collection: list = [],
        articles: list = [],
    ):
        self._id = _id or None
        self.index = index
        self.shopID = shopID
        self.boxID = boxID
        self.x = x
        self.y = y
        self.h = h
        self.r = r
        self.collection = collection
        self.articles = articles

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
        self._id = ret.get("_id")
        return self

    def delete(self, db):
        db.delete_one({"_id": self._id})


def log():
    return


if __name__ == "__main__":
    from db import db_box
    from db import get_table

    boxes = [
        BOX("6 полок низкий 2020", "Victoria Stenova", 1240, 580, 698),
        BOX("6 полок высокий 2020", "Victoria Stenova", 1240, 580, 894),
        BOX("12 полок пристенный 2020", "Victoria Stenova", 1240, 220, 2222),
        BOX("6 полок пристенный 2020", "Victoria Stenova", 1240, 220, 1230),
    ]

    for b in boxes:
        b.save(db_box)
        print(b.__dict__)

    table_shop = get_table("tapeti", "shop")
    shops = [
        SHOP(shopID="371", name="371", x=15000, y=15000),
        SHOP(shopID="763", name="763", x=100000, y=30000),
    ]
    for s in shops:
        s.save(table_shop)
        print(s.__dict__)

    pass
