#import necessary libraries
import RPi.GPIO as gpio
from bs4 import BeautifulSoup as bs
import requests

print("This program determines whether a stock is a good general dividend stock to own based on a long term investing point of view\n")
print("Green led will light if the entered stock is a good one to own, red if not, yellow if maybe\n\n")

#Setup pin numbers
red = 24
green = 16
yellow = 5

#Initialize pins
gpio.setmode(gpio.BCM)
gpio.setup(red, gpio.OUT)
gpio.setup(green, gpio.OUT)
gpio.setup(yellow, gpio.OUT)

#Default URL
url = "https://www.marketwatch.com/investing/stock/"
good = 100 #Integer for determining where a stock fits
#Empty dictionary for key data inputs
Data = {'Open':'', 'Day_Range':'', 'Year_Range':'', 'Market_Cap':'', 'Outstanding':'', 'Float':'', 'Beta':'', 'Revenue_per_employee':'', 'P_E':'', 'EPS':'', 'Yield':'', 'Dividend':'', 'Ex_Div_Date':'', 'Short_Interest':'', 'Per_Float_Short':'', 'Volume':''}
Stock_File = open("Stocks.txt", "a+") #Open file to append data
while True:
    #Ask user to input the ticker of the stick they want to check
    ticker = input("Please enter the ticker symbol of the stock or enter 'quit' to exit the program:\n")
    ticker.lower()
    #if user enters "Quit", stop the loop
    if ticker == "quit":
        print("Exitting program")
        break
    #Scrape necessary data from website
    url+=ticker
    print(url)
    page = requests.get(url) #Gets info from url
    soup = bs(page.content, "html.parser") #Puts data from page to a python readable format
    Key_Data = soup.find("ul", class_="list list--kv list--col50") #Imputs all of the key data from the marketwatch webpage
    #If data was successfully gathered
    if Key_Data is not None:
        Data_Categories = Key_Data.findAll("small", {"class" : "label"}) #Gather category labels
        Data_Values = Key_Data.findAll("span", {"class" : "primary"}) #Gather category values
        i = 0 #Iterator for loop
        print("Stock Symbol: ", ticker)
        print("__________________________________________")
        for key in Data:
            Data[key]=Data_Values[i].text #Put data in correct location in dictionary
            i+=1
            print(f"{key}: {Data[key]}")
        print("__________________________________________")
        Div_yield = Data['Yield'] #This is the dividend yield
        Div_yield = Div_yield.replace('%', '')
        #If no dividend yield, this stock sucks for dividend portfolio
        if Div_yield == 'N/A':
            print(f"\nWith no dividend yield, ")
            good = -1
            Div_yield = 0
        else:
            Div_yield = float(Div_yield)
            Year_split = Data['Year_Range'].split("-", 1) #Year low and high split up
            Year_low = float(Year_split[0]) #Year low as a float
            open = Data['Open'].replace('$', '') #Open price
            open = open.replace('p', '')
            open = float(open)
            Open_to_Low = open/Year_low*100 - 100 #Calculate percentage of year low to day open
            beta = float(Data['Beta']) #Stock beta value as float 
            print(f"\nWith a dividend yield of {Div_yield}, \nA Beta of {beta} and a percentage above the 52 week low of {Open_to_Low}%:")
            if beta <= 1 and Open_to_Low > 5 and Div_yield > 3:
                good = 1
            else:
                good = 0
    #Perform calculations to determine if stock is good dividend stock

    #Light Green led if the stock would be a good buy
    if good == 1:
        print("This stock is a good pick for a dividend based portfolio\n")
        gpio.output(green,True)
        gpio.output(red, False)
        gpio.output(yellow, False)
        Stock_File.write(f"Ticker Symbol: {ticker}, Dividend Yield: {Div_yield}.  This stock is a good pick for your portfolio\n")
    #Light red led if the stock would not be a good buy
    elif good == -1:
        print("This stock is not a good pick for a dividend based portfolio\n")
        gpio.output(red,True)
        gpio.output(green, False)
        gpio.output(yellow, False)
        Stock_File.write(f"Ticker Symbol: {ticker}, Dividend Yield: {Div_yield}.  This stock is NOT a good pick for your portfolio\n")
    #Light yellow led if the stock could be either good or bad
    elif good == 0:
        print("This stock could have potential in a dividend based portfolio\nTo make your decision, please do research on the company.\n")
        gpio.output(yellow,True)
        gpio.output(red, False)
        gpio.output(green, False)
        Stock_File.write(f"Ticker Symbol: {ticker}, Dividend Yield: {Div_yield}.  This stock needs more research\n")
    else:
        print("There was a problem with this ticker, please enter a new one \n\n")
        gpio.output(yellow,False)
        gpio.output(red, False)
        gpio.output(green, False)
    good = 100
    url = "https://www.marketwatch.com/investing/stock/"
Stock_File.close()
