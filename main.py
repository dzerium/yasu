import requests
import json 
import calendar
import datetime
import time
from lib.db_wrapper import db_wrapper

#from lib.request_wrapper import request_wrapper

LOCATION = r'C:\sqlite\ph_stocks.sqlite'
PHISIX_URL = r'http://phisix-api.appspot.com/stocks.json'
COL_URL = r'https://ph11.colfinancial.com/ape/colcharts/HISTORICAL/'

FLAG = False
def synchronize_db(sql_wrapper, symbol):
    global FLAG
    date = datetime.date.today()
    rows = []
    url =  COL_URL + symbol + r'.asp?symbol=' + symbol +'&range=&' + str(time.mktime(date.timetuple()))
    if symbol != 'LSC' and FLAG is False:
        return 
    else:
        FLAG = True 
    print(url)
    response = requests.get(url)
    if response.ok: 
        data = json.loads(response.content)
        for d in data:
            r = (d['Date'], d['Open'], d['Close'], d['High'], d['Low'], d['Volume'])
            rows.append(r)
        sql_wrapper.insert_row(symbol, rows)   
    else: 
        print('failed: ', symbol)
#end synchronize_db


def print_menu():
    print("====SQL====")
    print("[1] ")
#end print_menu


if __name__ == '__main__':
    response = requests.get(PHISIX_URL)
    sql_wrapper = db_wrapper(LOCATION)

    if response.ok:
        data = json.loads(response.content)
        if 'stock' in data.keys():
            for row in data['stock']:
                sql_wrapper.create_table(row['symbol'])
                synchronize_db(sql_wrapper, row['symbol'])
            #end loop
           
        else:
            print('Failure: ', response.raise_for_status())
    
    sql_wrapper.deinit()
#end main

