#! /usr/bin/env python3

import json
from flask import Flask
from flask import request
from flask_cors import CORS
from bson.objectid import ObjectId
import requests

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
    ret = {}
    for el in db_box.find():
        print(el)
        ret.update(BOX(**el).frontend_json)
    return json.dumps({"response": ret}, default=str), 200


@app.route("/get/collections", methods=["GET", "POST"], endpoint="get_collections")
def get_collections():
    h = {"apiKey": E.get("oboiru-api-key"), "Content-Type": "application/json"}
    resp = requests.post("https://api.oboi.ru/v3/collection", headers=h)

    if resp.status_code != 200:
        return {"error": f"api return status code {resp.status_code}"}, 400
    # удалю описание коллекции из ответа
    # нужна мемоизация
    clearable_response = [
        {k: v for k, v in el.items() if k != "description"}
        for el in resp.json().get("response")
    ]
    return json.dumps({"response": clearable_response}, default=str), 200


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


@app.route("/shop/<shopID>/get/boxes", methods=["GET", "POST"], endpoint="shop_box")
def shop_box(shopID):
    # список оборудования в магазине
    ret = {}
    for el in get_table("tapeti", "boxes").find({"shopID": shopID}):
        ret.update(SHOPBOX(**el).frontend_json)
    return (
        json.dumps({"response": ret}, default=str),
        200,
    )


@app.route("/shop/<shopID>/add/box", methods=["POST"], endpoint="shop_box_add")
def shop_box_add(shopID):
    # привязать оборудование к магазину
    data = request.json or {}
    data.update({"shopID": shopID})
    return (
        json.dumps(
            {
                "response": SHOPBOX(**data)
                .save(get_table("tapeti", "boxes"))
                .frontend_json
            },
            default=str,
        ),
        200,
    )


@app.route("/shop/<shopID>/upgrade/box", methods=["POST"], endpoint="shop_box_update")
def shop_box_update(shopID):
    # изменить параметры оборудования
    data = request.json or {}
    data.update({"shopID": shopID})
    SHOPBOX(**data).save(get_table("tapeti", "boxes"))
    return {"response": True}, 200


@app.route("/delete/box/<boxID>", methods=["POST"], endpoint="shop_box_delete")
def shop_box_delete(boxID):
    # удалить оборудование
    data = request.json or {}
    if not boxID:
        return {"error": "_id not founded"}, 400
    box = SHOPBOX(_id=boxID, **data)
    box.delete(get_table("tapeti", "boxes"))
    return {"response": True}, 200


if __name__ == "__main__":
    app.run(host=E.get("flask-host"), port=int(E.get("flask-port", 8000)))
