#import necessary libraries
from bs4 import BeautifulSoup as bs
import requests

print("This program determines whether a stock is a good general dividend stock to own based on a long term investing point of view\n")
print("Green led will light if the entered stock is a good one to own, red if not, yellow if maybe\n\n")

#Default URL
url = "https://www.marketwatch.com/investing/stock/"
good = 100
Data = {'Open':'', 'Day_Range':'', 'Year_Range':'', 'Market_Cap':'', 'Outstanding':'', 'Float':'', 'Beta':'', 'Revenue_per_employee':'', 'P_E':'', 'EPS':'', 'Yield':'', 'Dividend':'', 'Ex_Div_Date':'', 'Short_Interest':'', 'Per_Float_Short':'', 'Volume':''}
Stock_File = open("Stocks.txt", "a+")
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
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    Key_Data = soup.find("ul", class_="list list--kv list--col50")
    if Key_Data is not None:
        Data_Categories = Key_Data.findAll("small", {"class" : "label"})
        Data_Values = Key_Data.findAll("span", {"class" : "primary"})
        i = 0
        print("Stock Symbol: ", ticker)
        print("__________________________________________")
        for key in Data:
            Data[key]=Data_Values[i].text
            i+=1
            print(f"{key}: {Data[key]}")
        print("__________________________________________")
        Div_yield = Data['Yield']
        Div_yield = Div_yield.replace('%', '')
        if Div_yield == 'N/A':
            print(f"\nWith no dividend yield, ")
            good = -1
            Div_yield = 0
        else:
            Div_yield = float(Div_yield)
            Year_split = Data['Year_Range'].split("-", 1)
            Year_low = float(Year_split[0])
            open = Data['Open'].replace('$', '')
            open = open.replace('p', '')
            open = float(open)
            Open_to_Low = open/Year_low*100 - 100
            beta = float(Data['Beta'])
            print(f"\nWith a dividend yield of {Div_yield}, \nA Beta of {beta} and a percentage above the 52 week low of {Open_to_Low}%:")
            if beta <= 1 and Open_to_Low > 5 and Div_yield > 3:
                good = 1
            else:
                good = 0
    #Perform calculations to determine if stock is good dividend stock

    #Light Green led if the stock would be a good buy
    if good == 1:
        print("This stock is a good pick for a dividend based portfolio\n")
        Stock_File.write(f"Ticker Symbol: {ticker}, Dividend Yield: {Div_yield}.  This stock is a good pick for your portfolio\n")
    #Light red led if the stock would not be a good buy
    elif good == -1:
        print("This stock is not a good pick for a dividend based portfolio\n")
        Stock_File.write(f"Ticker Symbol: {ticker}, Dividend Yield: {Div_yield}.  This stock is NOT a good pick for your portfolio\n")
    #Light yellow led if the stock could be either good or bad
    elif good == 0:
        print("This stock could have potential in a dividend based portfolio\nTo make your decision, please do research on the company.\n")
        Stock_File.write(f"Ticker Symbol: {ticker}, Dividend Yield: {Div_yield}.  This stock needs more research\n")
    else:
        print("There was a problem with this ticker, please enter a new one \n\n")
    good = 100
    url = "https://www.marketwatch.com/investing/stock/"
Stock_File.close()
