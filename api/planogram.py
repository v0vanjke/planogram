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
        group: str,
        vendor: str,
        size: dict,
        shelf: int = 1,
        volume: int = 1,
    ):
        self._id = _id
        self.name = name
        self.group = group
        self.vendor = vendor
        self.size = size
        self.shelf = shelf  # кол-во полок
        self.volume = volume  # объем

    @property
    def json(self):
        return self.__dict__

    @property
    def frontend_json(self):
        return {str(self._id): {k: self.json[k] for k in self.json if k != "_id"}}

    def save(self, db):
        if not self._id:
            # create

            ret = db.create_one(self.json)
            print(ret)
            print("обнови _id в карточке")
        else:
            # update

            db.update_one(
                {"_id": ObjectId(self._id)},
                {"$set": self.json},
                upsert=False,
            )
        return self


class SHOP:
    def __init__(
        self,
        _id: ObjectId,
        shopID: str,
        name: str,
        size: dict,
        x: int = 1000,
        y: int = 300,
    ):
        self._id = _id
        self.shopID = shopID
        self.name = name
        self.size = size
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


class SHOPWALL:
    def __init__(
        self,
        _id: ObjectId,
        shopID: str,
        y: int = 15,
        points: list[list[int]] = [[0, 0]],
    ):
        self._id = _id or None
        self.shopID = shopID
        self.y = y  # толщина стены
        self.points = points


class SHOPCOLLECTION:
    """коллекции на плане магазина"""

    def __init__(self, _id: ObjectId, name: str, vendor: str, articles: list):
        self._id = _id
        self.name = name
        self.vendor = vendor
        self.articles = articles

    @property
    def json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @property
    def frontend_json(self):
        return {str(self._id): self.json}


class SHOPBOX:
    def __init__(
        self,
        _id: ObjectId,
        index: int,
        shopID: str,
        size: dict,
        position: dict,
        rotation: dict,
        collection: list = [],
        articles: list = [],
        shelf: int = 1,
        volume: int = 1,
    ):
        self._id = _id or None
        self.index = index
        self.shopID = shopID
        self.size = size
        self.rotation = rotation
        self.position = position
        self.collection = collection
        self.articles = articles
        self.shelf = shelf  # кол-во полок
        self.volume = volume  # объем

    @property
    def json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @property
    def frontend_json(self):
        return {str(self._id): self.json}

    def save(self, db):
        if not self._id:
            # create

            ret = db.insert_one(self.json)
            self._id = ret.inserted_id
        else:
            # update

            print(self.json)
            db.update_one(
                {"_id": ObjectId(self._id)},
                {"$set": self.json},
                upsert=False,
            )

        return self

    def delete(self, db):
        db.delete_one({"_id": ObjectId(self._id)})


def log():
    return


if __name__ == "__main__":
    from db import db_box
    from db import get_table

    boxes = [
        # BOX("6 полок низкий 2020", "Victoria Stenova", 1240, 580, 698),
    ]

    for b in boxes:
        b.save(db_box)
        print(b.__dict__)

    table_shop = get_table("tapeti", "shop")
    shops = [
        # SHOP(shopID="371", name="371", x=15000, y=15000),
    ]
    for s in shops:
        s.save(table_shop)
        print(s.__dict__)

    pass
