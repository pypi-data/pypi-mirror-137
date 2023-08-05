import socketio
import json
import requests
import base64
from datetime import datetime
from hashlib import sha256
import csv


class SocketEventBreeze(socketio.ClientNamespace):
    def __init__(self, namespace, breeze_instance):
        super().__init__(namespace)
        self.breeze = breeze_instance
        self.hostname = 'https://livestream.icicidirect.com'
        self.sio = socketio.Client()

    def connect(self):
        auth = {"user": self.breeze.user_id, "token": self.breeze.session_key}
        self.sio.connect(self.hostname, headers={"User-Agent":"python-socketio[client]/socket"}, auth=auth, transports="websocket", wait_timeout=3)

    def on_disconnect(self):
        self.sio.emit("disconnect", "transport close")

    def on_message(self, data):
        data = self.breeze.parse_data(data)
        self.breeze.on_ticks(data)

    def watch(self, data):
        self.sio.emit('join', data)
        self.sio.on('stock', self.on_message)

    def unwatch(self, data):
        self.sio.emit("leave", data)


class BreezeConnect():

    def __init__(self, api_key):  # needed for hashing json data
        self.user_id = None
        self.api_key = api_key
        self.session_key = None
        self.secret_key = None
        self.sio_handler = None
        self.api_handler = None
        self.on_ticks = None
        self.stock_subscribed_list = {}
        self.stock_script_dict_list = []

    def ws_connect(self):
        if not self.sio_handler:
            self.sio_handler = SocketEventBreeze("/", self)
            self.sio_handler.connect()

    def ws_disconnect(self):
        if not self.sio_handler:
            self.sio_handler = SocketEventBreeze("/", self)
        self.sio_handler.on_disconnect()
    
    def get_stock_token_value(self, exchange_code="", stock_code="", product_type="", strike_date="", strike_price="", right="", get_exchange_quotes=True, get_market_depth=True):
        if get_exchange_quotes == False and get_market_depth == False:
            raise GetStockTokenError(message = "Either getExchangeQuotes must be true or getMarketDepth must be true")
        else:
            exchange_code_name = ""
            exchange_code_list={
                "BSE":"1.",
                "NSE":"4.",
                "NDX":"13.",
                "MCX":"6.",
                "NFO":"4.",
            }
            exchange_code_name = exchange_code_list.get(exchange_code, False)
            if exchange_code_name == False:
                raise GetStockTokenError(message = "Exchange Code allowed are 'BSE', 'NSE', 'NDX', 'MCX' or 'NFO'.")
            elif stock_code == "":
                raise GetStockTokenError(message = "Stock-Code cannot be empty.")
            else:
                token_value = False
                if exchange_code == "BSE":
                    token_value = self.stock_script_dict_list[0].get(stock_code,False)
                elif exchange_code == "NSE":
                    token_value = self.stock_script_dict_list[1].get(stock_code,False)
                else:
                    if strike_date == "":
                        raise GetStockTokenError(message = "Strike-Date cannot be empty for given Exchange-Code.")
                    if product_type == "Futures":
                        contract_detail_value = "FUT"
                    elif product_type == "Options":
                        contract_detail_value = "OPT"
                    else:
                        raise GetStockTokenError(message = "Product-Type should either be Futures or Options for given Exchange-Code.")
                    contract_detail_value = contract_detail_value + "-" + stock_code  + "-" + strike_date
                    if product_type == "Options":
                        if strike_price != "":
                            contract_detail_value = contract_detail_value + "-" + strike_price
                        elif strike_price == "" and product_type == "Options":
                            raise GetStockTokenError(message = "Strike Price cannot be empty for Product-Type 'Options'.")
                        if right == "Put":
                            contract_detail_value = contract_detail_value + "-" + "PE"
                        elif right == "Call":
                            contract_detail_value = contract_detail_value + "-" + "CE"
                        elif product_type == "Options":
                            raise GetStockTokenError(message = "Rights should either be Put or Call for Product-Type 'Options'.")
                    if exchange_code == "NDX":
                        token_value = self.stock_script_dict_list[2].get(contract_detail_value,False)
                    elif exchange_code == "MCX":
                        token_value = self.stock_script_dict_list[3].get(contract_detail_value,False)
                    elif exchange_code == "NFO":
                        token_value = self.stock_script_dict_list[4].get(contract_detail_value,False)
                if token_value == False:
                    raise GetStockTokenError(message = "Stock-Code not found.")
                exchange_quotes_token_value = False
                if get_exchange_quotes != False:
                    exchange_quotes_token_value = exchange_code_name + "1!" + token_value
                market_depth_token_value = False
                if get_market_depth != False:
                    market_depth_token_value = exchange_code_name + "2!" + token_value
                return exchange_quotes_token_value, market_depth_token_value

    def subscribe_stock(self, stock_token="", exchange_code="", stock_code="", product_type="", strike_date="", strike_price="", right="", get_exchange_quotes=True, get_market_depth=True):
        if self.sio_handler:
            if stock_token != "":
                self.sio_handler.watch(stock_token)
            else:
                exchange_quotes_token, market_depth_token = self.get_stock_token_value(exchange_code=exchange_code, stock_code=stock_code, product_type=product_type, strike_date=strike_date, strike_price=strike_price, right=right, get_exchange_quotes=get_exchange_quotes, get_market_depth=get_market_depth)
                if exchange_quotes_token != False:
                    self.sio_handler.watch(exchange_quotes_token)
                if market_depth_token != False:
                    self.sio_handler.watch(market_depth_token)

    def unsubscribe_stock(self, stock_token="", exchange_code="", stock_code="", product_type="", strike_date="", strike_price="", right="", get_exchange_quotes=True, get_market_depth=True):
        if self.sio_handler:
            if stock_token != "":
                self.sio_handler.unwatch(stock_token)
            else:
                exchange_quotes_token, market_depth_token = self.get_stock_token_value(exchange_code=exchange_code, stock_code=stock_code, product_type=product_type, strike_date=strike_date, strike_price=strike_price, right=right, get_exchange_quotes=get_exchange_quotes, get_market_depth=get_market_depth)
                if exchange_quotes_token != False:
                    self.sio_handler.unwatch(exchange_quotes_token)
                if market_depth_token != False:
                    self.sio_handler.unwatch(market_depth_token)
        # raise SioHandlerNot

    def parse_market_depth(self, data, exchange):
        depth = []
        counter = 0
        for lis in data:
            counter += 1
            dict = {}
            if exchange == '1':
                dict["BestBuyRate-"+str(counter)] = lis[0]
                dict["BestBuyQty-"+str(counter)] = lis[1]
                dict["BestSellRate-"+str(counter)] = lis[2]
                dict["BestSellQty-"+str(counter)] = lis[3]
                depth.append(dict)
            else:
                dict["BestBuyRate-"+str(counter)] = lis[0]
                dict["BestBuyQty-"+str(counter)] = lis[1]
                dict["BuyNoOfOrders-"+str(counter)] = lis[2]
                dict["BuyFlag-"+str(counter)] = lis[3]
                dict["BestSellRate-"+str(counter)] = lis[4]
                dict["BestSellQty-"+str(counter)] = lis[5]
                dict["SellNoOfOrders-"+str(counter)] = lis[6]
                dict["SellFlag-"+str(counter)] = lis[7]
                depth.append(dict)
        return depth

    def parse_data(self, data):
        if data and len(data) == 46:
            order_dict = {}
            order_dict["sourceNumber"] = data[0]                            #Source Number
            order_dict["group"] = data[1]                                   #Group
            order_dict["userId"] = data[2]                                  #User_id
            order_dict["key"] = data[3]                                     #Key
            order_dict["messageLength"] = data[4]                           #Message Length
            order_dict["requestType"] = data[5]                             #Request Type
            order_dict["messageSequence"] = data[6]                         #Message Sequence
            order_dict["messageDate"] = data[7]                             #Date
            order_dict["messageTime"] = data[8]                             #Time
            order_dict["messageCategory"] = data[9]                         #Message Category
            order_dict["messagePriority"] = data[10]                        #Priority
            order_dict["messageType"] = data[11]                            #Message Type
            order_dict["orderMatchAccount"] = data[12]                      #Order Match Account
            order_dict["orderExchangeCode"] = data[13]                      #Exchange Code
            if data[11] == '4' or data[11] == '5':
                order_dict["stockCode"] = data[14]                     #Stock Code
                order_dict["orderFlow"] = data[15]                          # Order Flow
                order_dict["limitMarketFlag"] = data[16]                    #Limit Market Flag
                order_dict["orderType"] = data[17]                          #OrderType
                order_dict["orderLimitRate"] = data[18]                     #Limit Rate
                order_dict["productType"] = data[19]                        #Product Type
                order_dict["orderStatus"] = data[20]                        # Order Status
                order_dict["orderDate"] = data[21]                          #Order  Date
                order_dict["orderTradeDate"] = data[22]                     #Trade Date
                order_dict["orderReference"] = data[23]                     #Order Reference
                order_dict["orderQuantity"] = data[24]                      #Order Quantity
                order_dict["openQuantity"] = data[25]                       #Open Quantity
                order_dict["orderExecutedQuantity"] = data[26]              #Order Executed Quantity
                order_dict["cancelledQuantity"] = data[27]                  #Cancelled Quantity
                order_dict["expiredQuantity"] = data[28]                    #Expired Quantity
                order_dict["orderDisclosedQuantity"] = data[29]             # Order Disclosed Quantity
                order_dict["orderStopLossTrigger"] = data[30]               #Order Stop Loss Triger
                order_dict["orderSquareFlag"] = data[31]                    #Order Square Flag
                order_dict["orderAmountBlocked"] = data[32]                 # Order Amount Blocked
                order_dict["orderPipeId"] = data[33]                        #Order PipeId
                order_dict["channel"] = data[34]                            #Channel
                order_dict["exchangeSegmentCode"] = data[35]                #Exchange Segment Code
                order_dict["exchangeSegmentSettlement"] = data[36]          #Exchange Segment Settlement 
                order_dict["segmentDescription"] = data[37]                 #Segment Description
                order_dict["marginSquareOffMode"] = data[38]                #Margin Square Off Mode
                order_dict["orderValidDate"] = data[40]                     #Order Valid Date
                order_dict["orderMessageCharacter"] = data[41]              #Order Message Character
                order_dict["averageExecutedRate"] = data[42]                #Average Exited Rate
                order_dict["orderPriceImprovementFlag"] = data[43]          #Order Price Flag
                order_dict["orderMBCFlag"] = data[44]                       #Order MBC Flag
                order_dict["orderLimitOffset"] = data[45]                   #Order Limit Offset
                order_dict["systemPartnerCode"] = data[46]                  #System Partner Code
            elif data[11] == '6' or data[11] == '7':
                order_dict["underlying"] = data[14]                         #Underlying
                order_dict["productType"] = data[15]                        #Product Type
                order_dict["optionType"] = data[16]                         #Option Type
                order_dict["exerciseType"] = data[17]                       #Exercise Type
                order_dict["strikePrice"] = data[18]                        #Strike Price
                order_dict["expiryDate"] = data[19]                         #Expiry Date
                order_dict["orderValidDate"] = data[20]                     #Order Valid Date
                order_dict["orderFlow"] = data[21]                          #Order  Flow
                order_dict["limitMarketFlag"] = data[22]                    #Limit Market Flag
                order_dict["orderType"] = data[23]                          #Order Type
                order_dict["limitRate"] = data[24]                          #Limit Rate
                order_dict["orderStatus"] = data[25]                        #Order Status
                order_dict["orderReference"] = data[26]                     #Order Reference
                order_dict["orderTotalQuantity"] = data[27]                 #Order Total Quantity
                order_dict["executedQuantity"] = data[28]                   #Executed Quantity
                order_dict["cancelledQuantity"] = data[29]                  #Cancelled Quantity
                order_dict["expiredQuantity"] = data[30]                    #Expired Quantity
                order_dict["stopLossTrigger"] = data[31]                    #Stop Loss Trigger
                order_dict["specialFlag"] = data[32]                        #Special Flag
                order_dict["pipeId"] = data[33]                             #PipeId
                order_dict["channel"] = data[34]                            #Channel
                order_dict["modificationOrCancelFlag"] = data[35]           #Modification or Cancel Flag
                order_dict["tradeDate"] = data[36]                          #Trade Date
                order_dict["acknowledgeNumber"] = data[37]                  #Acknowledgement Number
                order_dict["stopLossOrderReference"] = data[37]             #Stop Loss Order Reference
                order_dict["totalAmountBlocked"] = data[38]                 # Total Amount Blocked
                order_dict["averageExecutedRate"] = data[39]                #Average Executed Rate
                order_dict["cancelFlag"] = data[40]                         #Cancel Flag
                order_dict["squareOffMarket"] = data[41]                    #SquareOff Market
                order_dict["quickExitFlag"] = data[42]                      #Quick Exit Flag
                order_dict["stopValidTillDateFlag"] = data[43]              #Stop Valid till Date Flag
                order_dict["priceImprovementFlag"] = data[44]               #Price Improvement Flag
                order_dict["conversionImprovementFlag"] = data[45]          #Conversion Improvement Flag
                order_dict["trailUpdateCondition"] = data[45]               #Trail Update Condition
                order_dict["systemPartnerCode"] = data[46]                  #System Partner Code
            return order_dict
        exchange = str.split(data[0], '!')[0].split('.')[0]
        data_type = str.split(data[0], '!')[0].split('.')[1]
        if data_type == '6':
            data_dict = {}
            data_dict["Symbol"] = data[0]
            data_dict["AndiOPVolume"] = data[1]
            data_dict["Reserved"] = data[2]
            data_dict["IndexFlag"] = data[3]
            data_dict["TotalQNTTraded"] = data[4]
            data_dict["LastTradedPrice"] = data[5]
            data_dict["LastTradedQuantity"] = data[6]
            data_dict["LastTradeTime"] = data[7]
            data_dict["AvgTradedPrice"] = data[8]
            data_dict["TotalBuyQnt"] = data[9]
            data_dict["TotalSellQnt"] = data[10]
            data_dict["ReservedStr"] = data[11]
            data_dict["ClosePrice"] = data[12]
            data_dict["OpenPrice"] = data[13]
            data_dict["HighPrice"] = data[14]
            data_dict["LowPrice"] = data[15]
            data_dict["ReservedShort"] = data[16]
            data_dict["CurrOpenInterest"] = data[17]
            data_dict["TotalTrades"] = data[18]
            data_dict["HightestPriceEver"] = data[19]
            data_dict["LowestPriceEver"] = data[20]
            data_dict["TotalTradedValue"] = data[21]
            marketDepthIndex = 0
            for i in range(22,len(data)):
                data_dict["Quantity-"+marketDepthIndex] = data[i][0]
                data_dict["OrderPrice-"+marketDepthIndex] = data[i][1]
                data_dict["TotalOrders-"+marketDepthIndex] = data[i][2]
                data_dict["Reserved-"+marketDepthIndex] = data[i][3]
                data_dict["SellQuantity-"+marketDepthIndex] = data[i][4]
                data_dict["SellOrderPrice-"+marketDepthIndex] = data[i][5]
                data_dict["SellTotalOrders-"+marketDepthIndex] = data[i][6]
                data_dict["SellReserved-"+marketDepthIndex] = data[i][7]
                marketDepthIndex += 1
        elif data_type == '1':
            data_dict = {
                "symbol": data[0],
                "open": data[1],
                "last": data[2],
                "high": data[3],
                "low": data[4],
                "change": data[5],
                "bPrice": data[6],
                "bQty": data[7],
                "sPrice": data[8],
                "sQty": data[9],
                "ltq": data[10],
                "avgPrice": data[11],
                "quotes": "Quotes Data"
            }
            # For NSE & BSE conversion
            if len(data) == 21:
                data_dict["ttq"] = data[12]
                data_dict["totalBuyQt"] = data[13]
                data_dict["totalSellQ"] = data[14]
                data_dict["ttv"] = data[15]
                data_dict["trend"] = data[16]
                data_dict["lowerCktLm"] = data[17]
                data_dict["upperCktLm"] = data[18]
                data_dict["ltt"] = datetime.fromtimestamp(
                    data[19]).strftime('%c')
                data_dict["close"] = data[20]
            # For FONSE & CDNSE conversion
            elif len(data) == 23:
                data_dict["OI"] = data[12]
                data_dict["CHNGOI"] = data[13]
                data_dict["ttq"] = data[14]
                data_dict["totalBuyQt"] = data[15]
                data_dict["totalSellQ"] = data[16]
                data_dict["ttv"] = data[17]
                data_dict["trend"] = data[18]
                data_dict["lowerCktLm"] = data[19]
                data_dict["upperCktLm"] = data[20]
                data_dict["ltt"] = datetime.fromtimestamp(
                    data[21]).strftime('%c')
                data_dict["close"] = data[22]
        else:
            data_dict = {
                "symbol": data[0],
                "time": datetime.fromtimestamp(data[1]).strftime('%c'),
                "depth": self.parse_market_depth(data[2], exchange),
                "quotes": "Market Depth"
            }
        if exchange == '4' and len(data) == 21:
            data_dict['exchange'] = 'NSE Equity'
        elif exchange == '1':
            data_dict['exchange'] = 'BSE'
        elif exchange == '13':
            data_dict['exchange'] = 'NSE Currency'
        elif exchange == '4' and len(data) == 23:
            data_dict['exchange'] = 'NSE Futures & Options'
        elif exchange == '6':
            data_dict['exchange'] = 'Commodity'
        return data_dict

    def api_util(self):
        try:
            headers = {
                "Content-Type": "application/json"
            }
            body = {
                "SessionToken": self.session_key,
                "AppKey": self.api_key
            }
            body = json.dumps(body, separators=(',', ':'))
            url = "https://api.icicidirect.com/breezeapi/api/v1/customerdetails"
            response = requests.get(url=url, data=body, headers=headers)
            if response.json()['Success']!=None:
                base64_session_token = response.json()['Success']['session_token']
                result = base64.b64decode(base64_session_token.encode('ascii')).decode('ascii')
                self.user_id = result.split(":")[0]
                self.session_key = result.split(":")[1]
            else:
                raise Exception("Could not authenticate credentials. Please check token and keys")
        except Exception as e:
            print("Could not authenticate credentials. Please check token and keys")

    def get_stock_script_list(self):
        try:
            self.stock_script_dict_list = [{},{},{},{},{}]
            with requests.Session() as s:
                download = s.get("https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv")
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                my_list = list(cr)
                for row in my_list:
                    if row[2] == "BSE":
                        self.stock_script_dict_list[0][row[3]]=row[5]
                    elif row[2] == "NSE":
                        self.stock_script_dict_list[1][row[3]]=row[5]
                    elif row[2] == "NDX":
                        self.stock_script_dict_list[2][row[7]]=row[5]
                    elif row[2] == "MCX":
                        self.stock_script_dict_list[3][row[7]]=row[5]
                    elif row[2] == "NFO":
                        self.stock_script_dict_list[4][row[7]]=row[5]
        except Exception as e:
            raise GetStockTokenError(message = e)
    
    def generate_session(self, api_secret, session_token):
        self.session_key = session_token
        self.secret_key = api_secret
        self.api_util()
        self.get_stock_script_list()
        self.api_handler = ApificationBreeze(self)

    def customer_login(self, user_id, password, date_of_birth):
        if self.api_handler:
            return self.api_handler.customer_login(user_id, password, date_of_birth, self.api_key)

    def get_customer_details(self, API_Session):
        if self.api_handler:
            return self.api_handler.get_customer_details(API_Session, self.api_key)

    def get_demat_holdings(self):
        if self.api_handler:
            return self.api_handler.get_demat_holdings()

    def get_funds(self):
        if self.api_handler:
            return self.api_handler.get_funds()

    def set_funds(self, transaction_type, amount, segment):
        if self.api_handler:
            return self.api_handler.set_funds(transaction_type, amount, segment)

    def get_historical_charts_list(self, interval, from_date, to_date, stock_code, exchange_code, product_type, expiry_date, option_type, strike_price, segment, exercise_type):
        if self.api_handler:
            return self.api_handler.get_historical_charts_list(interval, from_date, to_date, stock_code, exchange_code, product_type, expiry_date, option_type, strike_price, segment, exercise_type)

    def add_margins(self, product_type, stock_code, exchange_code, order_segment_code, order_settlement, add_amount, margin_amount, order_open_quantity, cover_quantity, category_INDSTK, contract_tag, add_margin_amount, expiry_date, order_optional_exercise_type, option_type, exercise_type, strike_price, order_stock_code):
        if self.api_handler:
            return self.api_handler.add_margins(product_type, stock_code, exchange_code, order_segment_code, order_settlement, add_amount, margin_amount, order_open_quantity, cover_quantity, category_INDSTK, contract_tag, add_margin_amount, expiry_date, order_optional_exercise_type, option_type, exercise_type, strike_price, order_stock_code)

    def get_margins(self, exchange_code):
        if self.api_handler:
            return self.api_handler.get_margins(exchange_code)

    def order_placement(self, stock_code, exchange_code, product, action, order_type, stoploss, quantity, price, validity, validity_date, disclosed_quantity, expiry_date, right, strike_price, user_remark):
        if self.api_handler:
            return self.api_handler.order_placement(stock_code, exchange_code, product, action, order_type, stoploss, quantity, price, validity, validity_date, disclosed_quantity, expiry_date, right, strike_price, user_remark)

    def get_order_detail(self, exchange_code, order_id):
        if self.api_handler:
            return self.api_handler.get_order_detail(exchange_code, order_id)

    def get_order_list(self, exchange_code, from_date, to_date):
        if self.api_handler:
            return self.api_handler.get_order_list(exchange_code, from_date, to_date)

    def order_cancellation(self, exchange_code, order_id):
        if self.api_handler:
            return self.api_handler.order_cancellation(exchange_code, order_id)

    def order_modification(self, order_id, exchange_code, order_type, stoploss, quantity, price, validity, disclosed_quantity, validity_date):
        if self.api_handler:
            return self.api_handler.order_modification(order_id, exchange_code, order_type, stoploss, quantity, price, validity, disclosed_quantity, validity_date)

    def get_portfolio_holdings(self, exchange_code, from_date, to_date, underlying, portfolio_type):
        if self.api_handler:
            return self.api_handler.get_portfolio_holdings(exchange_code, from_date, to_date, underlying, portfolio_type)

    def get_portfolio_positions(self):
        if self.api_handler:
            return self.api_handler.get_portfolio_positions()

    def get_quotes(self, stock_code, exchange_code, expiry_date, product_type, right, strike_price):
        if self.api_handler:
            return self.api_handler.get_quotes(stock_code, exchange_code, expiry_date, product_type, right, strike_price)

    def square_off(self, source_flag, order_stock_code, exchange_code, order_quantity, order_rate, order_flow, order_type, order_validity, order_stop_loss_price, order_disclosed_quantity, protection_percentage, order_segment_code, order_settlement, margin_amount, order_open_quantity, order_cover_quantity, order_product, order_exp_date, order_exc_type, order_option_type, order_strike_price, order_trade_date, trade_password, order_option_exercise_type):
        if self.api_handler:
            return self.api_handler.square_off(source_flag, order_stock_code, exchange_code, order_quantity, order_rate, order_flow, order_type, order_validity, order_stop_loss_price, order_disclosed_quantity, protection_percentage, order_segment_code, order_settlement, margin_amount, order_open_quantity, order_cover_quantity, order_product, order_exp_date, order_exc_type, order_option_type, order_strike_price, order_trade_date, trade_password, order_option_exercise_type)
    
    def get_trade_list(self, from_date, to_date, exchange_code, product_type, action, stock_code):
        if self.api_handler:
            return self.api_handler.get_trade_list(from_date, to_date, exchange_code, product_type, action, stock_code)

    def get_trade_detail(self, exchange_code, order_id):
        if self.api_handler:
            return self.api_handler.get_trade_detail(exchange_code, order_id)


class ApificationBreeze():

    def __init__(self, breeze_instance):
        self.breeze = breeze_instance
        self.hostname = 'https://api.icicidirect.com/breezeapi/api/v1/'
        self.base64_session_token = base64.b64encode(
            (self.breeze.user_id + ":" + self.breeze.session_key).encode('ascii')).decode('ascii')

    def generate_headers(self, body):
        try:
            current_date = datetime.utcnow().isoformat()[:19] + '.000Z'
            checksum = sha256(
                (current_date+body+self.breeze.secret_key).encode("utf-8")).hexdigest()
            headers = {
                "Content-Type": "application/json",
                'X-Checksum': "token "+checksum,
                'X-Timestamp': current_date,
                'X-AppKey': self.breeze.api_key,
                'X-SessionToken': self.base64_session_token
            }
            return headers
        except Exception as e:
            print("generate_headers() Error - ", e)

    def make_request(self, method, endpoint, body, headers):
        try:
            url = self.hostname + endpoint
            if method == "GET":
                res = requests.get(url=url, data=body, headers=headers)
                return res
            elif method == "POST":
                res = requests.post(url=url, data=body, headers=headers)
                return res
            elif method == "PUT":
                res = requests.put(url=url, data=body, headers=headers)
                return res
            elif method == "DELETE":
                res = requests.delete(url=url, data=body, headers=headers)
                return res
            else:
                print("Invalid Request Method - Must be GET, POST, PUT or DELETE")
        except Exception as e:
            print("Error while trying to make request "+method+" "+url+" - ", e)

    def customer_login(self, user_id, password, date_of_birth, app_key):
        try:
            headers = {
                "Content-Type": "application/json"
            }
            body = {
                "password": password,
                "dOB": date_of_birth,
                "iP_ID": "1.1.1.1",
                "appKey": app_key,
                "idirect_Userid": user_id,
                "user_Data": "ALL"
            }
            body = json.dumps(body, separators=(',', ':'))
            response = self.make_request("GET", "customerlogin", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("customer_login() Error - ", e)
            return {}

    def get_customer_details(self, API_Session, app_key):
        try:
            headers = {
                "Content-Type": "application/json"
            }
            body = {
                "SessionToken": API_Session,
                "AppKey": app_key
            }
            body = json.dumps(body, separators=(',', ':'))
            response = self.make_request(
                "GET", "customerdetails", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_customer_details() Error - ", e)

    def get_demat_holdings(self):
        try:
            body = {}
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "dematholdings", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_demat_holdings() Error- ", e)

    def get_funds(self):
        try:
            body = {}
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "funds", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_funds() Error - ", e)

    def set_funds(self, transaction_type, amount, segment):
        try:
            body = {
                "transaction_type": transaction_type,
                "amount": amount,
                "segment": segment
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "funds", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("set_funds() Error - ", e)

    def get_historical_charts_list(self, interval, from_date, to_date, stock_code, exchange_code, product_type, expiry_date, option_type, strike_price, segment, exercise_type):
        try:
            body = {
                "interval": interval,
                "from_date": from_date,
                "to_date": to_date,
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "product_type": product_type,
                "expiry_date": expiry_date,
                "option_type": option_type,
                "strike_price": strike_price,
                "segment": segment,
                "exercise_type": exercise_type
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request(
                "GET", "historicalcharts", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_historical_charts_list() Error - ", e)

    def add_margins(self, product_type, stock_code, exchange_code, order_segment_code, order_settlement, add_amount, margin_amount, order_open_quantity, cover_quantity, category_INDSTK, contract_tag, add_margin_amount, expiry_date, order_optional_exercise_type, option_type, exercise_type, strike_price, order_stock_code):
        try:
            body = {
                "product_type": product_type,
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "order_segment_code": order_segment_code,
                "order_settlement": order_settlement,
                "add_amount": add_amount,
                "margin_amount": margin_amount,
                "order_open_quantity": order_open_quantity,
                "cover_quantity": cover_quantity,
                "category_INDSTK": category_INDSTK,
                "contract_tag": contract_tag,
                "add_margin_amount": add_margin_amount,
                "expiry_date": expiry_date,
                "order_optional_exercise_type": order_optional_exercise_type,
                "option_type": option_type,
                "exercise_type": exercise_type,
                "strike_price": strike_price,
                "order_stock_code": order_stock_code,
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "margin", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("add_margins() Error - ", e)

    def get_margins(self, exchange_code):
        try:
            body = {
                "exchange_code": exchange_code
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "margin", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_margins() Error - ", e)

    def order_placement(self, stock_code, exchange_code, product, action, order_type, stoploss, quantity, price, validity, validity_date, disclosed_quantity, expiry_date, right, strike_price, user_remark):
        try:
            body = {
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "product": product,
                "action": action,
                "order_type": order_type,
                "stoploss": stoploss,
                "quantity": quantity,
                "price": price,
                "validity": validity,
                "validity_date": validity_date,
                "disclosed_quantity": disclosed_quantity,
                "expiry_date": expiry_date,
                "right": right,
                "strike_price": strike_price,
                "user_remark": user_remark
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("order_placement() Error - ", e)

    def get_order_detail(self, exchange_code, order_id):
        try:
            body = {
                "exchange_code": exchange_code,
                "order_id": order_id
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_order_detail() Error - ", e)

    def get_order_list(self, exchange_code, from_date, to_date):
        try:
            body = {
                "exchange_code": exchange_code,
                "from_date": from_date,
                "to_date": to_date
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_order_list() Error - ", e)

    def order_cancellation(self, exchange_code, order_id):
        try:
            body = {
                "exchange_code": exchange_code,
                "order_id": order_id
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("DELETE", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("order_cancellation() Error - ", e)

    def order_modification(self, order_id, exchange_code, order_type, stoploss, quantity, price, validity, disclosed_quantity, validity_date):
        try:
            body = {
                "order_id": order_id,
                "exchange_code": exchange_code,
                "order_type": order_type,
                "stoploss": stoploss,
                "quantity": quantity,
                "price": price,
                "validity": validity,
                "disclosed_quantity": disclosed_quantity,
                "validity_date": validity_date
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("PUT", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("order_modification() Error - ", e)

    def get_portfolio_holdings(self, exchange_code, from_date, to_date, underlying, portfolio_type):
        try:
            body = {
                "exchange_code": exchange_code,
                "from_date": from_date,
                "to_date": to_date,
                "underlying": underlying,
                "portfolio_type": portfolio_type
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request(
                "GET", "portfolioholdings", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_portfolio_holdings() Error - ", e)

    def get_portfolio_positions(self):
        try:
            body = {}
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request(
                "GET", "portfoliopositions", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_portfolio_positions() Error - ", e)

    def get_quotes(self, stock_code, exchange_code, expiry_date, product_type, right, strike_price):
        try:
            body = {
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "expiry_date": expiry_date,
                "product_type": product_type,
                "right": right,
                "strike_price": strike_price
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "quotes", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_quotes() Error - ", e)

    def square_off(self, source_flag, order_stock_code, exchange_code, order_quantity, order_rate, order_flow, order_type, order_validity, order_stop_loss_price, order_disclosed_quantity, protection_percentage, order_segment_code, order_settlement, margin_amount, order_open_quantity, order_cover_quantity, order_product, order_exp_date, order_exc_type, order_option_type, order_strike_price, order_trade_date, trade_password, order_option_exercise_type):
        try:
            body = {
                "source_flag": source_flag,
                "order_stock_code": order_stock_code,
                "exchange_code": exchange_code,
                "order_quantity": order_quantity,
                "order_rate": order_rate,
                "order_flow": order_flow,
                "order_type": order_type,
                "order_validity": order_validity,
                "order_stop_loss_price": order_stop_loss_price,
                "order_disclosed_quantity": order_disclosed_quantity,
                "protection_percentage": protection_percentage,
                "order_segment_code": order_segment_code,
                "order_settlement": order_settlement,
                "margin_amount": margin_amount,
                "order_open_quantity": order_open_quantity,
                "order_cover_quantity": order_cover_quantity,
                "order_product": order_product,
                "order_exp_date": order_exp_date,
                "order_exc_type": order_exc_type,
                "order_option_type": order_option_type,
                "order_strike_price": order_strike_price,
                "order_trade_date": order_trade_date,
                "trade_password": trade_password,
                "order_option_exercise_type": order_option_exercise_type
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "squareoff", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("square_off() Error - ", e)

    def get_trade_list(self, from_date, to_date, exchange_code, product_type, action, stock_code):
        try:
            body = {
                "from_date": from_date,
                "to_date": to_date,
                "exchange_code": exchange_code,
                "product_type": product_type,
                "action": action,
                "stock_code": stock_code,
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "trades", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_trade_list() Error - ", e)

    def get_trade_detail(self, exchange_code, order_id):
        try:
            body = {
                "exchange_code": exchange_code,
                "order_id": order_id
            }
            body = json.dumps(body, separators=(',', ':'))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "trades", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_trade_detail() Error - ", e)

class GetStockTokenError(Exception):
    """Exception raised for errors which need to be shown at user end"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)