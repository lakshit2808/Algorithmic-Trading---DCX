import hmac
import hashlib
import base64
import json
import time
import requests


def BuyCall(key, secret, symbol, quantity):

    secret_bytes = bytes(secret, encoding='utf-8')

    timeStamp = int(round(time.time() * 1000))

    body = {
    "side": "buy", 
    "order_type": "market_order",
    "market": symbol,
    "total_quantity": quantity,
    "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))


    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()


    url = "https://api.coindcx.com/exchange/v1/orders/create"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return data


def SellCall(key, secret, symbol, quantity):

    secret_bytes = bytes(secret, encoding='utf-8')

    timeStamp = int(round(time.time() * 1000))

    body = {
    "side": "sell",
    "order_type": "market_order",
    "market": symbol,
    "total_quantity": quantity, 
    "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))


    signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()


    url = "https://api.coindcx.com/exchange/v1/orders/create"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return data


print(BuyCall(key, secret, "SNTBTC", 0.01))