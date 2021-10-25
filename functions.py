import pandas_ta as ta
import requests
import pandas as pd

def HeikinAshi(df_HA):
    HAdf = df_HA[['Open', 'High', 'Low', 'Close']]
    
    #Closing
    HAdf['close'] = round(((df_HA['Open'] + df_HA['High'] + df_HA['Low'] + df_HA['Close'])/4),2)
    
    #Opening
    for i in range(len(df_HA)):
        if i == 0:
            HAdf.iat[0,0] = round(((df_HA['Open'].iloc[0] + df_HA['Close'].iloc[0])/2),2)
        else:
            HAdf.iat[i,0] = round(((HAdf.iat[i-1,0] + HAdf.iat[i-1,3])/2),2)
            
    #High & Low
    HAdf['high'] = HAdf.loc[:,['Open', 'Close']].join(df_HA['High']).max(axis=1)
    HAdf['low'] = HAdf.loc[:,['Open', 'Close']].join(df_HA['Low']).min(axis=1)
    
    return HAdf.close


def MACD(df_macd, fast_length = 12, slow_length = 26, signal_smoothing = 9):

    # dff = df_macd.ta.macd(close='HeikinAshi', fast=fast_length, slow=slow_length, signal=signal_smoothing, append=True)
    
    # dff.rename({"MACD_%s_%s_%s"%(fast_length,slow_length,signal_smoothing): 'MACD', "MACDs_%s_%s_%s"%(fast_length,slow_length,signal_smoothing): 'SIGNAL'}, axis=1, inplace=True)
    exp1 = df_macd.HeikinAshi.ewm(span=fast_length, adjust=False).mean()
    exp2 = df_macd.HeikinAshi.ewm(span=slow_length, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_smoothing, adjust=False).mean()

    dff = pd.DataFrame({"MACD": macd, "SIGNAL": signal})
    return dff


def SignalFromMACD(data):
    Buy = []
    for i in range(2 , len(data)):
        # if data.MACD.iloc[i] < data.SIGNAL.iloc[i] and data.MACD.iloc[i-1] > data.SIGNAL.iloc[i-1]:
        if data.MACD.iloc[i] < data.SIGNAL.iloc[i] and data.MACD.iloc[i-1] > data.SIGNAL.iloc[i-1] and data.MACD.iloc[i] < 0 and data.MACD.iloc[i] > -0.5:
            Buy.append(i)
            
    return Buy


def DataStream(symbol, interval, limit=0):
    data= {}
    try:
        data = requests.get('https://public.coindcx.com/market_data/candles?pair=B-%s&interval=%s'%(symbol, interval))
        if limit == 0:
            data = data.json()[0]
        else:
            data = data.json()[:limit]
    except IndexError:
        try:
            data = requests.get('https://public.coindcx.com/market_data/candles?pair=I-%s&interval=%s'%(symbol, interval))
            if limit == 0:
                data = data.json()[0]
            else:
                data = data.json()[:limit]
        except IndexError:
            try:
                data = requests.get('https://public.coindcx.com/market_data/candles?pair=HB-%s&interval=%s'%(symbol, interval))
                if limit == 0:
                    data = data.json()[0]
                else:
                    data = data.json()[:limit]
            except IndexError:
                try:
                    data = requests.get('https://public.coindcx.com/market_data/candles?pair=H-%s&interval=%s'%(symbol, interval))
                    if limit == 0:
                        data = data.json()[0]
                    else:
                        data = data.json()[:limit]
                except IndexError:
                    data = requests.get('https://public.coindcx.com/market_data/candles?pair=BM-%s&interval=%s'%(symbol, interval))
                    if limit == 0:
                        data = data.json()[0]
                    else:
                        data = data.json()[:limit]
    return data
