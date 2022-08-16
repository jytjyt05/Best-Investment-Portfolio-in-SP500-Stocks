# Modified Z-Score
# M-Z-score = 3.25 + 6.56A + 3.26B + 6.72C + 1.05D
# A = (Current Assets - Current Liabilities) / Total Assets
# B = Retained Earnings / Total Assets
# C = EBIT / Total Assets
# D = Book Equity / Total Liabilities

# Rating 	Minimum Z-score
# AAA		8.80
# AA		8.40
# A+		8.22
# A		6.94
# A-		6.12
# BBB+		5.80
# BBB		5.75
# BBB-		5.70
# BB+		5.65
# BB		5.52
# BB-		5.07
# B+		4.81
# B		4.03
# B-		3.74
# CCC+		2.84
# CCC		2.57
# CCC-		1.72
# D		0.05


import random as rd
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import tkinter as tk
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as bac

def DownloadData(ticker, begin_day, end_day):
    try:
        dt.datetime.strptime(begin_day, '%Y-%m-%d')
        dt.datetime.strptime(end_day, '%Y-%m-%d')
        mydata = yf.download(ticker, begin_day, end_day)
        return mydata['Adj Close']
    except:
        print('Date must be entered as YYYY-MM-DD')
        return 0
          
# Load all U.S. stocks in all sectors:
stock_list = pd.read_csv('sp500.csv')

def main():
    # calculate stocks' z-score and market to book ratio
    # and categories them
    industry=myindustry.get()
    begin_day=bday.get()
    end_day=eday.get()
    
    high_rating={}
    low_rating={}
    high_M2B={}
    low_M2B={}
    # establish industry data frame
    new_frame = stock_list[stock_list['Industry']==industry]
    tickers = new_frame[['Ticker','Company']].reset_index(drop=True)

    count=0
    print("Loading......")
    for i in tickers['Ticker']:
        count+=1
        # make sure less than 30 runs to avoid being identified as a hacker
        if count<30:
            #find z-score by calling function zscore()
            #find market to book by calling function M2B()
            z=zscore(i)
            m=M2B(i)
            print(i,z,m)
            if z>=6.12:
                high_rating[i]=z
            elif z<=5.07 and z!=-1:
                low_rating[i]=z
            if m>=20:
                high_M2B[i]=m
            elif m<=2 and m!=0:
                low_M2B[i]=m
    print('High Rating:',high_rating)
    print('Low Rating:',low_rating)
    print('High M2B:',high_M2B)
    print('Low M2B:',low_M2B)

    longdict={}
    shortdict={}
    # find qualifying stocks to long
    for i in high_rating:
        if i in low_M2B:
            stockdata=DownloadData(i,begin_day,end_day)
            longdict[i]=(stockdata[-1]-stockdata[0])*(round(50000/stockdata[0]))
    # find qualifying stocks to short
    for i in low_rating:
        if i in high_M2B:
            stockdata=DownloadData(i,begin_day,end_day)
            shortdict[i]=(stockdata[0]-stockdata[-1])*(round(50000/stockdata[0]))
    print("Longdict:",longdict)
    print("Shortdict:",shortdict)

    # append best pair into best_pair list
    best_pair=[]
    if len(longdict)!=0 and len(shortdict)!=0:
        # find the key corresponding to the max value within that dictionary
        lkey=max(longdict,key=longdict.get)
        skey=max(shortdict,key=shortdict.get)
        best_pair.append(lkey)
        best_pair.append(skey)
    
    # display result both in "best pair" box
    # and in the scroll box
    SetSelect(best_pair,tickers)

def M2B(my_ticker):
    # calculate market to book value based on 2020 data
    begin_day=bday.get()
    end_day=eday.get()
    fin_data = yf.Ticker(my_ticker)
    so = fin_data.get_info()['sharesOutstanding']
    price_dataframe = fin_data.history(period='1y')['Close']
    
    # get Market Value
    mv = so*price_dataframe.loc['2020-12-31']
    # get Book Value
    balance_sheet = fin_data.get_balancesheet()
    # if 2020 book value is found, calculate market to book ratio
    if '2020' in balance_sheet:
        current_asset = balance_sheet.loc['Total Current Assets']['2020']
        current_liab = balance_sheet.loc['Total Current Liabilities']['2020']
        bv=current_asset[0]-current_liab[0]
        M2B = mv/bv
    else:
        # if 2020 book value is not found, skip the stock
        M2B = 0
    
    return M2B
    
def zscore(my_ticker):
    # calculate z-score based on 2020 data
    fin_data = yf.Ticker(my_ticker)
    income_stmt = fin_data.get_financials()
    balance_sheet = fin_data.get_balancesheet()

    if '2020' in balance_sheet and '2020' in income_stmt and 'Retained Earnings' in balance_sheet.index:
    # Ratio of Working Capital / Total Assets (WC_TA)  #A
        current_asset = balance_sheet.loc['Total Current Assets']['2020']
        current_liab = balance_sheet.loc['Total Current Liabilities']['2020']
        total_asset = balance_sheet.loc['Total Assets']['2020']
        wc_ta = (current_asset[0] - current_liab[0]) / total_asset[0]

    # Ratio of Retained Earnings / Total Asset (RE_TA) #B
        retain_earning = balance_sheet.loc['Retained Earnings']['2020']
        re_ta = retain_earning[0] / total_asset[0]
    
    # Ratio of EBIT / Total Asset (EBIT_TA)  #C
        ebit = income_stmt.loc['Ebit']['2020']
        ebit_ta = ebit[0] / total_asset[0]
    
    # Ratio of Equity MV / Total Liabilities (MV_TL)   #D
        total_liab = balance_sheet.loc['Total Liab']['2020']
        so = fin_data.get_info()['sharesOutstanding']
        price_dataframe = fin_data.history(period='1y', interval='1d')['Close']
        mv_tl = so * price_dataframe.loc['2020-12-31'] / total_liab

        # if has data for 2020, calculate the Z-Score
        z_score = 3.25 + 6.65*wc_ta + 3.26*re_ta + 6.72*ebit_ta + 1.05*mv_tl
        return z_score[0]
    else:
        # if doesn't have data for 2020, return -1, skipping the ticker
        return -1


## Functions for TK interface
def SetSelect(best_pair,tickers):
    # if the best pair dictionary is not empty, show result
    # else, show "no..." msg in Entry
    if len(best_pair)!=0:
        # show best pair in Entry
        result='Long:'+best_pair[0]+'; Short:'+best_pair[1]
        mypair.set(result)
        # show best pair and its full company name in Scroll Box
        myselect.delete(0,tk.END)
        for s in best_pair:
            comp = tickers.loc[tickers.Ticker==s,'Company'].values[0]
            myselect.insert (tk.END, s+', '+comp)
    else:
        mypair.set('No best pair found')
def ClearInput():
    bday.set('')
    eday.set('')
    myindustry.set('')
def QuitNow():
    mywindow.quit()
    mywindow.destroy()


mywindow = tk.Tk()
mywindow.geometry('600x600')
mywindow.title('Porject 3')

myframe = tk.Frame(mywindow)
myframe.pack(side = tk.RIGHT)
myscroll = tk.Scrollbar(myframe, orient=tk.VERTICAL)
myselect = tk.Listbox(myframe, yscrollcommand=myscroll.set)
myselect.pack(side=tk.LEFT)
myscroll.config(command=myselect.yview)
myscroll.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(mywindow, text = 'Industry').place(x=30, y=10)
myindustry = tk.StringVar()
tk.Entry(mywindow, textvariable = myindustry).place(x=100, y=10)

tk.Label(mywindow, text = 'Start Date').place(x=30, y=50)
bday = tk.StringVar()
tk.Entry(mywindow, textvariable = bday).place(x=100, y=50)

tk.Label(mywindow, text = 'End Date').place(x=300, y=50)
eday = tk.StringVar()
tk.Entry(mywindow, textvariable = eday).place(x=370, y=50)

tk.Label(mywindow, text = 'Best Pair').place(x=150, y=90)
mypair = tk.StringVar()
tk.Entry(mywindow, textvariable = mypair).place(x=220, y=90)

tk.Button(mywindow,text="RUN", command = main).place(x= 60, y=190)
tk.Button(mywindow,text="CLEAR", command = ClearInput).place(x=60, y=230)
tk.Button(master=mywindow, text="Quit Now", activeforeground='red',command= QuitNow).pack(side=tk.BOTTOM)

mywindow.mainloop()



