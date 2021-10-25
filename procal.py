from functions import DataStream



def NetProfitCalculator(token,buy_price, sell_price, totalamountinrs, takerfee , makerfee):

    token = DataStream('%s_INR'%(token), '1m')['close']

    amountIntoken = totalamountinrs / token

    quantity = amountIntoken / buy_price

    changeInPrice = sell_price - buy_price

    profit = changeInPrice * quantity

    buyFee = takerfee/100 * buy_price * quantity
    sellFee = makerfee/100 * sell_price * quantity

    totalFee = buyFee + sellFee

    netProfitIntoken = profit - totalFee

    netProfitInRS = netProfitIntoken * token

    return netProfitInRS




buy_price =1.614
sell_price = 1.625# Try Next Day
token = 'USDT'
takerfee = 0.1
makerfee = 0.1
amount = 5000

print('Profit in RS: ', NetProfitCalculator(token, buy_price, sell_price, amount, takerfee, makerfee))