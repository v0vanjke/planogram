#! /usr/bin/env python3

from dotenv import load_dotenv
from pymongo import MongoClient
from os import environ as E

load_dotenv()

client = MongoClient(
    E.get("mongo-host"),
    port=int(E.get("mongo-port", 27017)),
    username=E.get("mongo-username"),
    password=E.get("mongo-password"),
    authSource=E.get("mongo-auth-source"),
)

db_box = client["planogram_AAA"]["box"]
