import requests
import datetime 
import hashlib 
import hmac 
import json

class CCBitkub(object):

    RESOLUTION_CONV_DICT = {
        '1m' : '1',
        '5m' : '5',
        '15m' : '15',
        '1h' : '60',
        '4h' : '240',
        '1d' : '1D',
    }
    
    PERIOD_MULTIPLIER_DICT = {
        '1m' : 60,
        '5m' : 60 * 5,
        '15m' : 60 * 15,
        '1h' : 60 * 60,
        '4h' : 60 * 60 * 4,
        '1d' : 60 * 60 * 24,
    }
    
    def __init__(self, config={}):
        self.api_key = config.get('apiKey', '')
        self.api_secret = config.get('secret', '')
        self.async_loop = config.get('asyncio_loop', None)

    def _signature(self, payload):
        message = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        return hmac.new(self.api_secret.encode(), msg=message.encode(), digestmod=hashlib.sha256).hexdigest()

    async def fetchOHLCV(self, asset, interval, limit=1000):
        to_time = int( datetime.datetime.utcnow().timestamp() )
        from_time = to_time - self.PERIOD_MULTIPLIER_DICT[interval] * (limit - 2)
        request_result = requests.get('https://api.bitkub.com/tradingview/history', params={'symbol': asset.replace('/', '_'), 
                    'resolution': self.RESOLUTION_CONV_DICT[interval], 'from':from_time, 'to':to_time})
        json_r = request_result.json()
        latest_candle = json_r['t'][0]
        newest_candle = json_r['t'][-1]
        loop_time = latest_candle
        result_list = []
        latest_close = 0
        while loop_time <= newest_candle :
            if loop_time in json_r['t'] :
                i = json_r['t'].index(loop_time)
                result_list.append( [json_r['t'][i] * 1000, json_r['o'][i], json_r['h'][i], json_r['l'][i], json_r['c'][i], json_r['v'][i]] )
                latest_close = json_r['c'][i]
            else :
                result_list.append( [json_r['t'][i] * 1000, latest_close, latest_close, latest_close, latest_close, 0.0] )
            loop_time += self.PERIOD_MULTIPLIER_DICT[interval]
        return result_list

    async def fetchTicker(self, symbol):
        result = { "symbol": symbol, "timestamp":  int(datetime.datetime.utcnow().timestamp()) * 1000, 
                    "datetime": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') } 
        converted_asset = '_'.join(symbol.split('/')[::-1])
        request_result = requests.get('https://api.bitkub.com/api/market/ticker', params={'sym': converted_asset})
        json_r = request_result.json()[converted_asset]
        result['high'] = json_r['high24hr']
        result['low'] = json_r['low24hr']
        result['bid'] = json_r['highestBid']
        result['ask'] = json_r['lowestAsk']
        result['last'] = json_r['last']
        result['change'] = json_r['change']
        result['percentage'] = json_r['percentChange']
        result['baseVolume'] = json_r['baseVolume']
        result['info'] = {
            "symbol": symbol,
            "priceChange": str(json_r['change']),
            "priceChangePercent" : str(json_r['percentChange']),
            "lastPrice": str(json_r['last']),
            "highPrice": str(json_r['high24hr']),
            "lowPrice": str(json_r['low24hr']),
            "volume": str(json_r['baseVolume']),
        }
        return result

    def _get_bucket(self, raw):
        bucket = {}
        for i in raw :
            if i[3] in bucket :
                bucket[i[3]] += i[4]
            else :
                bucket[i[3]] = i[4]
        return bucket

    async def fetchOrderBook(self, asset, limit=100):
        converted_asset = '_'.join(asset.split('/')[::-1])
        request_result = requests.get('https://api.bitkub.com/api/market/depth', params={'sym': converted_asset, 'lmt': limit})
        json_r = request_result.json()
        raw_bits = json_r['bids']
        raw_asks = json_r['asks']
        result = {'symbol':asset, 'bids': raw_bits, 'asks': raw_asks, 'timestamp': int(datetime.datetime.utcnow().timestamp()) * 1000, 
                    'datetime': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') }
        return result

    async def fetchBalance(self):
        payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp())}
        payload["sig"] = self._signature(payload)
        request_result = requests.post('https://api.bitkub.com/api/market/balances', 
                    headers={"Content-Type":"application/json", "Accept":"application/json", "X-BTK-APIKEY":self.api_key}, 
                    data=json.dumps(payload, separators=(',', ':'), sort_keys=True))
        json_r = request_result.json()
        result = { "info" : {"positions":[]}, "timestamp": int(datetime.datetime.utcnow().timestamp()) * 1000, 
                    "datetime": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), 
                    "free":{"THB": json_r['result']['THB']['available']}, "used":{"THB":json_r['result']['THB']['reserved']}, "total":{"THB": 0} }
        ticker = requests.get('https://api.bitkub.com/api/market/ticker').json()
        for k, v in json_r['result'].items() :
            if "THB_" + k in ticker:
                result["info"]["positions"].append( { "symbol": k + "/THB", "leverage" : "1", "positionAmt": str(v['available'])} )
                result["used"]["THB"] += (v['available'] + v['reserved']) * ticker["THB_" + k]["last"]
        result["total"]["THB"] = result["used"]["THB"] + result["free"]["THB"]
        return result

    async def fetchOpenOrders(self, symbol):
        converted_asset = '_'.join(symbol.split('/')[::-1])
        payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()), 'sym':converted_asset}
        payload["sig"] = self._signature(payload)
        request_result = requests.post('https://api.bitkub.com/api/market/my-open-orders', 
                    headers={"Content-Type":"application/json", "Accept":"application/json", "X-BTK-APIKEY":self.api_key}, 
                    data=json.dumps(payload, separators=(',', ':'), sort_keys=True))
        json_r = request_result.json()['result']
        result = []
        for each_order in json_r :
            result.append( await self.fetchOrder(each_order['id'], symbol, {'side': each_order['side'].lower()}) )
        return result

    async def fetchOrder(self, id, symbol, params={}):
        converted_asset = '_'.join(symbol.split('/')[::-1])
        side = params.get('side', None)
        hash_value = params.get('hash', None)
        if side :
            payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()), 'sym':converted_asset, 'id':id, 'sd':side}
        if hash_value :
            payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()), 'hash':hash_value}
        payload["sig"] = self._signature(payload)
        request_result = requests.post('https://api.bitkub.com/api/market/order-info', 
                    headers={"Content-Type":"application/json", "Accept":"application/json", "X-BTK-APIKEY":self.api_key}, 
                    data=json.dumps(payload, separators=(',', ':'), sort_keys=True))
        json_r = request_result.json()['result']
        binance_status = 'NEW'
        cc_status = 'open'
        if json_r['status'] == 'filled' and not json_r['partial_filled'] :
            binance_status = 'FILLED'
            cc_status = 'closed'
        if json_r['partial_filled'] :
            binance_status = 'PARTIALLY_FILLED'
            cc_status = 'open'
        if json_r['status'] == 'cancelled' :
            binance_status = 'CANCELED'
            cc_status = 'canceled'
        if side == 'buy' :
            asset_amount = json_r['amount'] / json_r['rate']
            executed_asset_amount = json_r['filled'] / json_r['rate']
            remaining_asset_amount = json_r['remaining'] / json_r['rate']
            thb_filled = json_r['filled']
            thb_cost = json_r['filled']
            thb_fee = json_r['fee']
        elif side == 'sell' :
            asset_amount = json_r['amount'] 
            executed_asset_amount = json_r['filled']
            remaining_asset_amount = json_r['remaining']
            thb_filled = json_r['filled']
            thb_cost = json_r['filled']
            thb_fee = json_r['fee']
        result = {'info': {'orderId': json_r['id'], 'symbol': symbol, 'status': binance_status, 'price': str(json_r['rate']),
                    'avgPrice': '0.00000', 'origQty': str(asset_amount), 'executedQty': str(executed_asset_amount), 'type': '', 'side': side},
                    'id': json_r['id'], "timestamp": int(datetime.datetime.utcnow().timestamp()) * 1000, 
                    "datetime": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), 'symbol': symbol, 'type': '', 'side': side, 
                    'price': json_r['rate'], 'amount': asset_amount, 'cost': thb_cost, 'average': None, 'filled': thb_filled, 
                    'remaining': remaining_asset_amount, 'status': cc_status, 'fee': thb_fee, 'trade': [], 'fees': [] }
        return result

        # ccxt_binance
        # {'info': {'orderId': '42283831784', 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'x-xcKtGhcu79d783bce5aac8021b846e', 
        # 'price': '30000', 'avgPrice': '0.00000', 'origQty': '0.001', 'executedQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 
        # 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 
        # 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'time': '1643509489633', 'updateTime': '1643509489633'}, 
        # 'id': '42283831784', 'clientOrderId': 'x-xcKtGhcu79d783bce5aac8021b846e', 'timestamp': 1643509489633, 'datetime': '2022-01-30T02:24:49.633Z', 
        # 'lastTradeTimestamp': None, 'symbol': 'BTC/USDT', 'type': 'limit', 'timeInForce': 'GTC', 'postOnly': False, 'side': 'buy', 'price': 30000.0, 
        # 'stopPrice': None, 'amount': 0.001, 'cost': 0.0, 'average': None, 'filled': 0.0, 'remaining': 0.001, 'status': 'open', 'fee': None, 
        # 'trades': [], 'fees': []}

        # bitkub
        # {'error': 0, 'result': {'amount': 1000, 'client_id': '', 'credit': 0, 'fee': 2.5, 'filled': 0, 'first': 101366009, 'history': [], 
        # 'id': 101366009, 'last': 0, 'parent': 0, 'partial_filled': False, 'rate': 1000000, 'remaining': 1000, 'side': 'buy', 'status': 'unfilled', 
        # 'total': 1000}}

    async def createOrder(self, symbol, order_type, side, amount, price=0, params={}):
        converted_asset = '_'.join(symbol.split('/')[::-1])
        cc_bitkub_ticker = await self.fetchTicker(symbol)
        payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()), 'sym': converted_asset,
                    'amt': amount, 'rat': price, 'typ': order_type }
        if side == 'buy':
            if order_type == 'market' :
                current_rate = float( cc_bitkub_ticker['info']['lastPrice'] )
                thb_amount = amount * current_rate
            elif order_type == 'limit' :
                thb_amount = amount * price
            payload['amt'] = thb_amount
        payload["sig"] = self._signature(payload)
        if side == 'buy' :
            url = '/api/market/place-bid' 
        elif side == 'sell' :
            url = '/api/market/place-ask'
        request_result = requests.post('https://api.bitkub.com' + url, 
                    headers={"Content-Type":"application/json", "Accept":"application/json", "X-BTK-APIKEY":self.api_key}, 
                    data=json.dumps(payload, separators=(',', ':'), sort_keys=True))
        if request_result.json()['error'] != 0 :
            raise Exception("Error occur in bitkub request : {}".format(request_result.json()['error']))
        json_r = request_result.json()['result']
        cc_bitkub_order = await self.fetchOrder(json_r['id'], symbol, params={'side':side})
        return cc_bitkub_order

    async def cancelOrder(self, id, symbol, params={}):
        converted_asset = '_'.join(symbol.split('/')[::-1])
        side = params.get('side', None)
        hash_value = params.get('hash', None)
        if side :
            payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()), 'sym':converted_asset, 'id':id, 'sd':side}
        if hash_value :
            payload = {'ts': int((datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()), 'hash':hash_value}
        payload["sig"] = self._signature(payload)
        request_result = requests.post('https://api.bitkub.com/api/market/cancel-order', 
                    headers={"Content-Type":"application/json", "Accept":"application/json", "X-BTK-APIKEY":self.api_key}, 
                    data=json.dumps(payload, separators=(',', ':'), sort_keys=True))
        json_r = request_result.json()
        if json_r['error'] == 0 :
            cc_bitkub_order = await self.fetchOrder(id, symbol, params=params)
            return cc_bitkub_order
        else :
            raise Exception("Error occur in bitkub request : {}".format(json_r['error']))
