import requests
import json
import time
from Random_Functions.colour_print import colour_print, RED
from nelson import nelson_lorimer

kucoin_all_coins_req = requests.get("https://api.kucoin.com/api/v1/market/allTickers").text
kucoin_all_coins_req = json.loads(kucoin_all_coins_req)
ticker_plus = 0
standalone_ticker = ""
ticker_list = []
try:
    while True:
        ticker = kucoin_all_coins_req["data"]["ticker"][ticker_plus]["symbol"]
        ticker_plus += 1
        for dash in ticker:
            if dash == "-":
                ticker_list.append(standalone_ticker)
                standalone_ticker = ""
                break
            else:
                standalone_ticker += dash
except IndexError:
    ticker_plus = 0


coingecko_get_coinid_request = requests.get("https://api.coingecko.com/api/v3/coins/list").text
coingecko_get_coinid_request = json.loads(coingecko_get_coinid_request)
coinid_plus = 0
kucoingeckoid_list = []
kucoin_gecko_coinid_list = []


try:
    while True:
        gecko_coinid = coingecko_get_coinid_request[coinid_plus]["id"]
        gecko_symbol = coingecko_get_coinid_request[coinid_plus]["symbol"]
        gecko_symbol = str(gecko_symbol.upper())
        coinid_plus += 1
        for kucoin_gecko_id in ticker_list:
            if gecko_symbol == kucoin_gecko_id:
                kucoingeckoid_list.append(gecko_symbol)
                kucoin_gecko_coinid_list.append(gecko_coinid)
                break
except IndexError:
    coinid_plus = 0


def gecko_results(coin_id: str):
    coin_info_req = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={}&order=market_cap_desc&per_page"
        "=100&page=1&sparkline=false".format(coin_id)).text
    coin_info_req = json.loads(str(coin_info_req))
    max_supply = str(coin_info_req[0]["max_supply"])
    if max_supply != "None":
        # Option for max sup < 21m
        if float(max_supply) < 21000000:
            nelson_lorimer("The coin {} has a max supply of {}".format(coin_id, max_supply))
        max_supply = format(float(max_supply), ",")
    circulating_supply = str(coin_info_req[0]["circulating_supply"])
    if circulating_supply != "None":
        circulating_supply = format(float(circulating_supply), ",")
    price = str(coin_info_req[0]["current_price"])
    if price != "None":
        price = format(float(price), ",")
    market_cap = str(coin_info_req[0]["market_cap"])
    if market_cap != "None":
        market_cap = format(float(market_cap), ",")
    print("The coin {} has a market cap of ${}, a circulating supply of {}, a maximum supply of {} and a price of ${}"
          .format(coin_id, market_cap, circulating_supply, max_supply, price))
    print()
    time.sleep(1)


for index, coin in enumerate(kucoin_gecko_coinid_list):
    try:
        gecko_results(coin)
    except json.decoder.JSONDecodeError:
        colour_print(("Error at position {} at coin {}, sleeping".format(index, coin)), RED)
        print()
        time.sleep(61)
        gecko_results(coin)

