######################## Importing Dependences #################
import requests
import pandas as pd
from datetime import datetime
from functions import DataStream
from functions import HeikinAshi, MACD, SignalFromMACD

######################### Declaring Variables ##################
opens, closes,highs,lows,date,time,timestamp,BuyList, SellList,open = [],[],[],[],[],[],[],[],[],[0,0]
LastPrice,LastBuyPrice,LastSellPrice,OrderCompleted,StopLoss = 0,0,0,0,0
OrderStatus = 'Buy'
BuyOrderRunning = False

######################### Previous Trades #######################
data = DataStream('MATIC_USDT', '1m',50)
for i in data:

    timestamp.append(i['time']/1000)
    opens.append(i['open'])
    closes.append(i['close'])
    highs.append(i['high'])
    lows.append(i['low'])

for j in timestamp:
    date.append(datetime.fromtimestamp(j).strftime('%Y-%m-%d'))
    time.append(datetime.fromtimestamp(j).strftime('%H:%M:%S'))

######################### Main Work #######################
while True:

    ################################ Data Stream ################################################
    data = DataStream('MATIC_USDT', '1m')

    open_ = data['open']
    open.append(open_)
    
    if open[-1] != open[-2]:

        opens.append(data['open'])
        closes.append(data['close'])
        highs.append(data['high'])
        lows.append(data['low'])

        df = pd.DataFrame(opens,columns=['Open'])
        df['Close'] = closes
        df['High'] = highs
        df['Low'] = lows

        now = datetime.now()
        currentD = now.strftime("%d/%m/%Y")
        currentT = now.strftime("%H:%M:%S")
        date.append(currentD)
        time.append(currentT)

        df['Date'] = date
        df['Time'] = time

        MainDF= df[['Date','Time', 'Open', 'Close', 'High', 'Low']]

    ################################## Putting Data in Indicators ########################################################
        HA = HeikinAshi(df)
        MainDF['HeikinAshi'] = HA
        
        macdfunc = MACD(MainDF,4, 6, 2)
        MainDF['MACD'] = macdfunc.MACD
        MainDF['SIGNAL'] = macdfunc.SIGNAL

        MainDF['BuyPrice'] = MainDF.iloc[SignalFromMACD(MainDF)].Close
        

        print(MainDF)

    #################################### Making BUY CALL ###################################################################
        # Buy
        LastPrice = MainDF.Close.iloc[-1]
        if OrderStatus == 'Buy':
            LastBuyPrice = MainDF.BuyPrice.iloc[-1]
            
            print('Looking to Buy')

            if LastPrice == LastBuyPrice:

                print("Buy Price: %s"%(LastBuyPrice))
                BuyList.append(LastBuyPrice)
                OrderStatus = 'Sell'
                BuyOrderRunning = True
                
                
        
    #################################### Making SELL CALL ###################################################################

        # Sell


        if OrderStatus == 'Sell':
            LastSellPrice = BuyList[-1] + 0.01 ######## Price Change #########
            print(LastSellPrice)
            if LastPrice >= LastSellPrice:

                print("Buy Price %s \nSell Price %s"%(BuyList[-1], LastPrice))
                OrderStatus = 'Buy'
                BuyOrderRunning = False
                SellList.append(LastPrice)
                OrderCompleted += 1
                
                ##################### Ending ############################
                if OrderCompleted == 2:
                    BuySell = pd.DataFrame({'Buy':BuyList,'Sell':SellList})
                    BuySell.to_csv('BuySell.csv', index=False)
                    MainDF.to_csv('NEXO_USDT.csv', index=False)
                    exit()

            ######## Stop Loss #############        
            StopLoss = BuyList[-1] - 0.014 ######## Price Change #########
            if LastPrice < StopLoss:
                print("Buy Price %s \nSell Price %s"%(BuyList[-1], LastPrice))
                OrderStatus = 'Buy'
                BuyOrderRunning = False
                SellList.append(LastPrice)
                OrderCompleted += 1
                
                ##################### Ending ############################
                if OrderCompleted == 2:
                    BuySell = pd.DataFrame({'Buy':BuyList,'Sell':SellList})
                    BuySell.to_csv('BuySell.csv', index=False)
                    MainDF.to_csv('NEXO_USDT.csv', index=False)
                    exit()

        #################################### Order Status ###################################################################

        if BuyOrderRunning == True:
            print("Buy Order Running for %s"%(BuyList[-1]))
        
        if OrderCompleted > 0:
            print("Order Completed: %s"%(OrderCompleted))