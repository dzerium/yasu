import requests
import json 
import calendar
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
from lib.db_wrapper import db_wrapper

LOCATION = r'C:\sqlite\ph_stocks.sqlite'
COL_URL = r'https://ph11.colfinancial.com/ape/colcharts/HISTORICAL/'

def synch_stock_db(sql_wrapper, symbol):
    today = datetime.today()
    rows = []
    url =  COL_URL + symbol + r'.asp?symbol=' + symbol +'&range=&' + str(time.mktime(today.timetuple()))
    
    print("Synching symbol:", symbol)
    response = requests.get(url)
    if response.ok: 
        data = json.loads(response.content)
        for d in data:
            r = (d['Date'], d['Open'], d['Close'], d['High'], d['Low'], d['Volume'])
            rows.append(r)
        sql_wrapper.insert_row(symbol, rows, today)   
    else: 
        print('failed: ', symbol)
#end build_stock_db
    
def print_menu():
    print("====SQL====")
    print("[1] Synchronize Database")
    print("[2] Analyze stocks")
#end print_menu

if __name__ == '__main__':
    sql_wrapper = db_wrapper(LOCATION)
      
    while True: 
        print_menu()
        option = input("Enter option: ")
        print(option)
        if option == '1': 
            lists = sql_wrapper.get_monitor_status()
            for item in lists:
                synch_stock_db(sql_wrapper, item[0])
        elif option == '2':
            print("Analyze stocks")
        elif option == '3':
            break

    sql_wrapper.deinit()
#end main

