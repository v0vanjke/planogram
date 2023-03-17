#! /usr/bin/env python3

import json
from flask import Flask
from flask_cors import CORS
from flask import request

from dotenv import load_dotenv
from db import db_box
from api import BOX
from os import environ as E

load_dotenv()


app = Flask(__name__)
cors = CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})


@app.route("/get/boxes", methods=["GET", "POST"], endpoint="box_list")
def box_list():
    # список торгового оборудования
    return (
        json.dumps(
            {"response": [BOX(el).json for el in db_box.findall()]}, default=str
        ),
        200,
    )


@app.route("/get/collections", methods=["GET", "POST"], endpoint="collection")
def collection():
    # коллекции будем брать из api
    pass


@app.route("/get/shops", methods=["GET", "POST"], endpoint="shop")
def shop():
    # список магазинов
    pass


@app.route("/shop/add", methods=["POST"], endpoint="shop_add")
def shop_add():
    # добавить магазин
    pass


@app.route("/shop/<shopID>/get/boxes", methods=["GET", "POST"], endpoint="shop_box")
def shop_box(shopID):
    # список оборудования в магазине
    pass


@app.route("/shop/<shopID>/box/add", methods=["POST"], endpoint="shop_box_add")
def shop_box_add(shopID):
    # привязать оборудование к магазину
    pass


@app.route("/<shopID>/<id>/update", methods=["POST"], endpoint="shop_box_update")
def shop_box_update(shopID, id):
    # изменить параметры оборудования
    pass


@app.route("/<shopID>/<id>/delete", methods=["POST"], endpoint="shop_box_delete")
def shop_box_delete(shopID, id):
    # удалить оборудование
    pass


if __name__ == "__main__":
    app.run(host=E.get("flask-host"), port=int(E.get("flask-port", 8000)))
