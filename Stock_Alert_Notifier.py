import telepot 
import requests 
from datetime import datetime
from timeloop import Timeloop
from datetime import timedelta
from twilio.rest import Client

def getStockData(ticker):
    base_url = "https://financialmodelingprep.com/api/v3/quote/"
    key = "771b5a44aa3356ba5194abbfc2e84de3"
    full_url = base_url + ticker + "?apikey=" + key
    r = requests.get(full_url)
    stock_data= r.json()
    return stock_data

def generateMessage(data):
    symbol = data[0]['symbol']
    price = data[0]["price"]
    changesPercent = data[0]["changesPercentage"]
    timestamp = data[0]['timestamp']
    
    current = datetime.fromtimestamp(timestamp)
    message = "Hello! This  is the Stock Market Details "+str(current)
    message += "\n" + symbol 
    message += "\n$" + str(price)    
    if(changesPercent < -2):
        message += "\nWarning! Price drop more than 2%!"
        
    return message

def sendMessage(text):
    account_sid = "SID" # Your Account SID from twilio.com/console
    auth_token  = "Token" # Your Auth Token from twilio.com/console

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="XXX", #enter your verified phone number
        from_="+14255411934",
        body=text)

    print(message.sid)

tl = Timeloop()

@tl.job(interval=timedelta(seconds=60))
def run_tasks():
    ticker = "AMZN"
    real_time_data = getStockData(ticker)
    textMessage = generateMessage(real_time_data)
    sendMessage(textMessage)
    
tl.start(block=True)
