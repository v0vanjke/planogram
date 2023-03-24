#! /usr/bin/env python3

import json
from flask import Flask
from flask import request
from flask_cors import CORS
from bson.objectid import ObjectId

from db import get_table
from db import db_box

from planogram import BOX
from planogram import COLLECTION
from planogram import SHOP
from planogram import SHOPBOX

from dotenv import load_dotenv
from os import environ as E
from pprint import pprint as pp


load_dotenv()


app = Flask(__name__)
cors = CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})
app.debug = True


@app.route("/get/boxes", methods=["GET", "POST"], endpoint="box_list")
def box_list():
    # список торгового оборудования
    return (
        json.dumps({"response": [BOX(**el).json for el in db_box.find()]}, default=str),
        200,
    )


@app.route("/get/collections", methods=["GET", "POST"], endpoint="collection")
def collection():
    # коллекции будем брать из api
    return {}, 200


@app.route("/get/shops", methods=["GET", "POST"], endpoint="shop")
def shop():
    # список магазинов
    return (
        json.dumps(
            {
                "response": [
                    SHOP(**el).json for el in get_table("tapeti", "shops").find()
                ]
            },
            default=str,
        ),
        200,
    )


@app.route("/add/shop", methods=["POST"], endpoint="shop_add")
def shop_add():
    # добавить магазин
    return {}, 200


@app.route("/shop/<shopID>/add/box", methods=["POST"], endpoint="shop_box_add")
def shop_box_add(shopID):
    # привязать оборудование к магазину
    data = request.json or {}
    if not data.get("boxID"):
        return {"error": "boxID not founded"}, 400
    box = SHOPBOX(
        _id=ObjectId(),
        index=1,
        shopID=shopID,
        boxID=data["boxID"],
        x=data.get("x"),
        y=data.get("y"),
        h=data.get("h"),
    )

    box.create(get_table("tapeti", "boxes"))
    return json.dumps(box.json, default=str), 200


@app.route("/shop/<shopID>/get/boxes", methods=["GET", "POST"], endpoint="shop_box")
def shop_box(shopID):
    # список оборудования в магазине
    return (
        json.dumps(
            {
                "response": [
                    SHOPBOX(el).json
                    for el in get_table("tapeti", "box").findall({"shopID": shopID})
                ]
            },
            default=str,
        ),
        200,
    )


@app.route("/box/update", methods=["POST"], endpoint="shop_box_update")
def shop_box_update():
    # изменить параметры оборудования
    data = request.json or {}
    if not data.get("_id"):
        return {"error": "_id not founded"}, 400
    box = SHOPBOX(**data)
    box.save(get_table("tapeti", "boxes"))
    return {"result": True}, 200


@app.route("/box/delete", methods=["POST"], endpoint="shop_box_delete")
def shop_box_delete():
    # удалить оборудование
    data = request.json or {}
    if not data.get("_id"):
        return {"error": "_id not founded"}, 400
    box = SHOPBOX(**data)
    box.delete(get_table("tapeti", "boxes"))
    return {}, 200


if __name__ == "__main__":
    app.run(host=E.get("flask-host"), port=int(E.get("flask-port", 8000)))
