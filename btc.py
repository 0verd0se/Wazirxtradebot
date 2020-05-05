import requests
import time
nextStep = 'buy'
history=[]

lastBuyPrice = 0
amountLeft = 1000
currentUnits = 0
momentum = 0
file1 = open("./profits.txt", "w+", "a")
file2 = open("./prices.txt", "w+", "a")
while(1):
    response = requests.get('https://api.wazirx.com/api/v2/tickers')
    btcinr = response.json()['btcinr']
    price = btcinr['last']
    number_of_digits = price.find('.')
    price = int(price[:number_of_digits])
    if nextStep=='buy':
        if len(history)==0:
            history.append(price)
            continue
        lastPrice = history[-1]
        if price >= lastPrice:
            print('buying')
            unitsToBuy = float("{0:.4f}".format(float(amountLeft)/float(price)))
            priceOfBuying = float("{0:.1f}".format(unitsToBuy * price))
            commision = float("{0:.2f}".format(0.002 * priceOfBuying))
            lastBuyPrice = float("{0:.2f}".format(priceOfBuying+commision))
            amountLeft = float("{0:.2f}".format(amountLeft - priceOfBuying-commision))
            currentUnits = currentUnits + unitsToBuy
            filewrite = 'Buying price: '+str(priceOfBuying) + '\n'
            file1.write(filewrite)
            nextStep = 'sell'


    elif nextStep =='sell':
        lastPrice = history[-1]
        if price < lastPrice:
            print('selling')
            unitsToSell = currentUnits
            priceOfSelling = float("{0:.1f}".format(unitsToSell * price))
            commision = float("{0:.2f}".format(0.002 * priceOfSelling))
            profit = float("{0:.2f}".format(priceOfSelling-commision-lastBuyPrice))
            if profit>0:
                amountLeft = float("{0:.2f}".format(amountLeft + priceOfSelling-commision))
                currentUnits = 0

                filewrite = 'Selling Price: '+str(priceOfSelling)+':::: Profit from this sell='+str(profit)+'\n'
                print(filewrite)
                file1.write(filewrite)
                nextStep = 'buy'
                

        
    history.append(price)
    writee = str(price)+'\n'
    file2.write(writee)
    print(price)
    time.sleep(10)
file1.close()