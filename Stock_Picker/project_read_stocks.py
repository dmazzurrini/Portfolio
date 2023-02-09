file = open('Stocks.txt', 'r') #open file
stocks = file.read() #Read in all lines
file.close()
print(stocks) #Print out all lines
