<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 19:08:33 2022

hello
@author: Trader_MIKE
"""

import pandas as pd
from flask import Flask, render_template, request,jsonify,session
import pandas_ta as ta
import os
import datetime
import zipfile
#logging.basicConfig(filename="trading_log/mangesh_server_logs"+datetime.datetime.today().strftime("%d_%m_%y_%H_%M_%S")+".log",
#                    format='%(asctime)s %(message)s',
#                    filemode='w')
#logger = logging.getLogger()



app = Flask(__name__)
app.secret_key="Mangesh@115"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login_post():

    username = request.form['username']
    password = request.form['password']

    # Check if the credentials are valid
    if username == 'mangesh' and password == 'mangesh':
        # If the credentials are valid, start a new session
        session['logged_in'] = True
    return render_template("dashboard.html")

def get_data_raw(stock_name,time_interval,to_time,from_time):
    z = zipfile.ZipFile('data/stock_data.zip')
    df=pd.DataFrame(z.filelist,columns=['zipobj'])
    df['filename'] = df['zipobj'].apply(lambda x:x.filename)
    if stock_name+"_minute_data_with_indicators.csv" in os.listdir("data"):
        data = pd.read_csv("data/"+stock_name+"_minute_data_with_indicators.csv",index_col=False)[['date','open','high','low','close','volume']]
        data['date1'] = pd.to_datetime(data['date'])
        data = data.loc[(data.date1.dt.time >= datetime.time(9, 15)) & 
                        (data.date1.dt.time < datetime.time(15, 30)) & (data.date1.dt.date > datetime.datetime.strptime(from_time+" 00:00:00+05:30",'%Y-%m-%d %H:%M:%S%z').date())
                        & (data.date1.dt.date < datetime.datetime.strptime(to_time+" 00:00:00+05:30","%Y-%m-%d %H:%M:%S%z").date())].sort_index()
        data['high'] = data[['high', 'low']].max(axis=1)
        data['low'] = data[['high', 'low']].min(axis=1)
        data = data.set_index(pd.DatetimeIndex(data['date1']))
        if time_interval == '5min':
            return data.resample('5T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '30min':
            return data.resample('30T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '60min':
            return data.resample('60T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '240min':
            return data.resample('240T',offset = '75T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna() 
        elif time_interval == '120min':
            return data.resample('120T',offset = "75T").agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '1day':
            return data.resample('1D').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        else:
            return data[['date','open','high','low','close','volume']]
    else:
        data = pd.read_csv(z.extract(stock_name+"_minute_data_with_indicators.csv","data"))
        data['date1'] = pd.to_datetime(data['date'])
        data = data.loc[(data.date1.dt.time >= datetime.time(9, 15)) & (data.date1.dt.time < datetime.time(15, 30))]
        data = data.fillna(method='ffill')
        data = data.set_index(pd.DatetimeIndex(data['date1']))
        if time_interval == '5min':
            return data.resample('5T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '30min':
            return data.resample('30T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '60min':
            return data.resample('60T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '240min':
            return data.resample('240T',offset = '75T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna() 
        elif time_interval == '120min':
            return data.resample('120T',offset = "75T").agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '1day':
            return data.resample('1D').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        else:
            return data[['date','open','high','low','close','volume']]

def get_data(stock_name,time_interval,to_time,from_time):
    data = get_data_raw(stock_name,time_interval,to_time,from_time)
    data_raw = data
    data = data[:200]
    data = data.join(ta.adx(data['high'],data['low'],data['close']))
    data = data.join(ta.ao(data['high'],data['low']))
    data = data.join(ta.aroon(data['high'],data['low']))
    data = data.join(ta.atr(data['high'],data['low'],data['close']))
    data = data.join(ta.cci(data['high'],data['low'],data['close']))
    data = data.join(ta.chop(data['high'],data['low'],data['close']))
    data = data.join(ta.ema(data['close']))
    data = data.join(ta.hma(data['close']))
    data = data.join(ta.macd(data['close']))
    data = data.join(ta.mom(data['close']))
    data = data.join(ta.rsi(data['close']))
    data = data.join(ta.sma(data['close']))
    data = data.join(ta.uo(data['high'],data['low'],data['close']))
    data = data.join(ta.willr(data['high'],data['low'],data['close']))
    ichimoku_data = pd.DataFrame(ta.ichimoku(data['high'],data['low'],data['close']))
    ichimoku_data = ichimoku_data.add_prefix('ichimoku_')
    data = data.join(ichimoku_data)
    return data_raw,data


@app.route('/get_stock_data', methods=['GET','POST'])
def get_stock_data():
    req = request.get_json()
    print(req)

    data,processed = get_data(stock_name = req['stock'],time_interval=req['time_frame'],to_time=req['to_time'],from_time=req['from_time'])

    print(data.head())
    return jsonify({"candles":data[['date','open','high','low','close','volume']].to_dict(orient='records'),"processed": processed.iloc[-1].fillna(0).to_dict()})

@app.route('/get_stock_list', methods=['GET','POST'])
def get_stock_list():
    z = zipfile.ZipFile('data/stock_data.zip')
    stock_list=pd.DataFrame(z.filelist,columns=['zipobj'])
    stock_list['filename'] = stock_list['zipobj'].apply(lambda x:x.filename)
    filename=stock_list['filename'].tolist()
    filename = [sub.replace('_minute_data_with_indicators.csv', '') for sub in filename]
    filename = filename[1:]
    #print(filename)
    return jsonify(filename)
@app.route('/dropdown', methods=['GET','POST'])
def dropdown():
    return render_template("test_drop_down.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5005', debug=True, use_reloader=True)

    
=======
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 19:08:33 2022

hello
@author: Trader_MIKE
"""

import pandas as pd
from flask import Flask, render_template, request,jsonify,session
import pandas_ta as ta
import os
import datetime
import zipfile
#logging.basicConfig(filename="trading_log/mangesh_server_logs"+datetime.datetime.today().strftime("%d_%m_%y_%H_%M_%S")+".log",
#                    format='%(asctime)s %(message)s',
#                    filemode='w')
#logger = logging.getLogger()



app = Flask(__name__)
app.secret_key="Mangesh@115"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login_post():

    username = request.form['username']
    password = request.form['password']

    # Check if the credentials are valid
    if username == 'mangesh' and password == 'mangesh':
        # If the credentials are valid, start a new session
        session['logged_in'] = True
    return render_template("dashboard.html")

def get_data_raw(stock_name,time_interval,to_time,from_time):
    z = zipfile.ZipFile('data/stock_data.zip')
    df=pd.DataFrame(z.filelist,columns=['zipobj'])
    df['filename'] = df['zipobj'].apply(lambda x:x.filename)
    if stock_name+"_minute_data_with_indicators.csv" in os.listdir("data"):
        data = pd.read_csv("data/"+stock_name+"_minute_data_with_indicators.csv",index_col=False)[['date','open','high','low','close','volume']]
        data['date1'] = pd.to_datetime(data['date'])
        data = data.loc[(data.date1.dt.time >= datetime.time(9, 15)) & 
                        (data.date1.dt.time < datetime.time(15, 30)) & (data.date1.dt.date > datetime.datetime.strptime(from_time+" 00:00:00+05:30",'%Y-%m-%d %H:%M:%S%z').date())
                        & (data.date1.dt.date < datetime.datetime.strptime(to_time+" 00:00:00+05:30","%Y-%m-%d %H:%M:%S%z").date())].sort_index()
        data['high'] = data[['high', 'low']].max(axis=1)
        data['low'] = data[['high', 'low']].min(axis=1)
        data = data.set_index(pd.DatetimeIndex(data['date1']))
        if time_interval == '5min':
            return data.resample('5T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '30min':
            return data.resample('30T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '60min':
            return data.resample('60T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '240min':
            return data.resample('240T',offset = '75T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna() 
        elif time_interval == '120min':
            return data.resample('120T',offset = "75T").agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '1day':
            return data.resample('1D').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        else:
            return data[['date','open','high','low','close','volume']]
    else:
        data = pd.read_csv(z.extract(stock_name+"_minute_data_with_indicators.csv","data"))
        data['date1'] = pd.to_datetime(data['date'])
        data = data.loc[(data.date1.dt.time >= datetime.time(9, 15)) & (data.date1.dt.time < datetime.time(15, 30))]
        data = data.fillna(method='ffill')
        data = data.set_index(pd.DatetimeIndex(data['date1']))
        if time_interval == '5min':
            return data.resample('5T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '30min':
            return data.resample('30T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '60min':
            return data.resample('60T',offset = '15T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '240min':
            return data.resample('240T',offset = '75T').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna() 
        elif time_interval == '120min':
            return data.resample('120T',offset = "75T").agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        elif time_interval == '1day':
            return data.resample('1D').agg({
                'date':'first',
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        else:
            return data[['date','open','high','low','close','volume']]

def get_data(stock_name,time_interval,to_time,from_time):
    data = get_data_raw(stock_name,time_interval,to_time,from_time)
    data_raw = data
    data = data[:200]
    data = data.join(ta.adx(data['high'],data['low'],data['close']))
    data = data.join(ta.ao(data['high'],data['low']))
    data = data.join(ta.aroon(data['high'],data['low']))
    data = data.join(ta.atr(data['high'],data['low'],data['close']))
    data = data.join(ta.cci(data['high'],data['low'],data['close']))
    data = data.join(ta.chop(data['high'],data['low'],data['close']))
    data = data.join(ta.ema(data['close']))
    data = data.join(ta.hma(data['close']))
    data = data.join(ta.macd(data['close']))
    data = data.join(ta.mom(data['close']))
    data = data.join(ta.rsi(data['close']))
    data = data.join(ta.sma(data['close']))
    data = data.join(ta.uo(data['high'],data['low'],data['close']))
    data = data.join(ta.willr(data['high'],data['low'],data['close']))
    ichimoku_data = pd.DataFrame(ta.ichimoku(data['high'],data['low'],data['close']))
    ichimoku_data = ichimoku_data.add_prefix('ichimoku_')
    data = data.join(ichimoku_data)
    return data_raw,data


@app.route('/get_stock_data', methods=['GET','POST'])
def get_stock_data():
    req = request.get_json()
    print(req)

    data,processed = get_data(stock_name = req['stock'],time_interval=req['time_frame'],to_time=req['to_time'],from_time=req['from_time'])

    print(data.head())
    return jsonify({"candles":data[['date','open','high','low','close','volume']].to_dict(orient='records'),"processed": processed.iloc[-1].fillna(0).to_dict()})

@app.route('/get_stock_list', methods=['GET','POST'])
def get_stock_list():
    z = zipfile.ZipFile('data/stock_data.zip')
    stock_list=pd.DataFrame(z.filelist,columns=['zipobj'])
    stock_list['filename'] = stock_list['zipobj'].apply(lambda x:x.filename)
    filename=stock_list['filename'].tolist()
    filename = [sub.replace('_minute_data_with_indicators.csv', '') for sub in filename]
    filename = filename[1:]
    #print(filename)
    return jsonify(filename)
@app.route('/dropdown', methods=['GET','POST'])
def dropdown():
    return render_template("test_drop_down.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5005', debug=True, use_reloader=True)

    
>>>>>>> ee0e8e15a2815f7bf27a6f3ddb7c50fad67ddaf1
