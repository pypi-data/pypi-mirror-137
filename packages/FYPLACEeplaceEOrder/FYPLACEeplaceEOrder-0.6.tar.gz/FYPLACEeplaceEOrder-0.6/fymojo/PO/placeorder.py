import json
import requests
def place_order(apiKey, apiSecret, clientId, symbol, qty, type1, side , productType,disclosedQty, offlineOrder):
    data = {
        "api_key": apiKey,
        "api_secret": apiSecret,
        "data":{
            "strategy_name":"test strategy",
            "symbol": symbol,
            "qty": qty,
            "type":type1,
            "side": side,
            "productType": productType,
            "disclosedQty": disclosedQty,
            "offlineOrder": offlineOrder,
            "validity": "DAY",
            "stopLoss": 0,
            "takeProfit": 0,
            "limitPrice": 0,
            "stopPrice": 0,
        }
        
    }
    response = requests.post("https://fyapi.algomojo.com/1.0/PlaceOrder",json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response)
    jsonValue = response.json()
    print(jsonValue)
    return  jsonValue