from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import binanceBot
import sqlite3
import contextlib
import os
from twilio.rest import Client

app = Flask(__name__)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
introMsg = "Hello and welcome to your crypto trader on your phone (USDT only). See the possible actions before. To load more USDT, please load into your binance acconut.\nBuy coin: BUY <coin> <number>\n Sell coin: SELL <coin> <number>\n Get price: GET <coin>\n Get balance: BALANCE <coin>"

@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    number = data['number']
    apikey = data['apikey']
    apisecret = data['apisecret']
    with contextlib.closing(sqlite3.connect("users.db")) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                cursor.execute(f"INSERT INTO users VALUES ('{number}', '{apikey}', {apisecret})")

    message = client.messages.create(body=introMsg, from_='+13203481536', to=number)
    return jsonify({"success": True})

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    incoming = request.values.get('From', None)
    with contextlib.closing(sqlite3.connect("users.db")) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                rows = cursor.execute("SELECT apikey, apisecret FROM users WHERE number = " + str(incoming)).fetchall()

    apikey, apisecret = rows[0][0], rows[0][1]
    binance = binanceBot.BinanceBot(apikey, apisecret)

    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    action, coin, number = body.split()[0], body.split()[1], body.split()[2]
    try:
        if action.upper() == 'BUY':
            if (len(body.split()) < 3):
                resp.message("Please enter a coin and a number of coins to buy. The format is BUY <coin> <number>")
            amountBought, amountLeft = binance.buy(coin, number)
            price = binance.getPrice(coin) * amountBought
            resp.message("Bought {amountBought} {coin} for {price} USDT. {amountLeft} USDT left.")
        elif action.upper() == 'SELL':
            if (len(body.split()) < 3):
                resp.message("Please enter a coin and a number of coins to buy. The format is BUY <coin> <number>")
            amountSold, amountLeft = binance.sell(coin, number)
            resp.message(f"SOLD {amountSold} {coin}. You have {amountLeft} left.")
        elif action.upper() == 'GET':
            if (len(body.split()) < 3):
                resp.message("Please enter a coin and a number of coins to buy. The format is BUY <coin> <number>")
            price = binance.getPrice(coin)
            resp.message("Current Price of {coin} is {price}")
        elif action.upper() == 'BALANCE':
            if (len(body.split()) < 3):
                resp.message("Please enter a coin and a number of coins to buy. The format is BUY <coin> <number>")
            balance = binance.getBalance(coin)
            resp.message(f"You have {balance} {coin}")
        else:
            resp.message("Please enter a valid action.\n Buy coin: BUY <coin> <number>\n Sell coin: SELL <coin> <number>\n Get price: GET <coin>\n Get balance: BALANCE <coin>")
    except:
        resp.message("Please enter a valid action.\n Buy coin: BUY <coin> <number>\n Sell coin: SELL <coin> <number>\n Get price: GET <coin>\n Get balance: BALANCE <coin>")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)