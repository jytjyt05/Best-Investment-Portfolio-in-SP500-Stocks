
# Best-Investment-Portfolio-in-SP500-Stocks

This Project was created to find best investment portoflio among stocks in S&P 500 index based on estimation.
The estimation has two parts: the stock's modified z-score and the stock's market to book ratio.

Although it was implemented in Python, it uses a tk interface for convinent usage.

## What can user do
- The user can enter the day range (such as 2020-01-01 to 2021-09-01).
- The user can also choose the industry from the stocks in S&P 500 index.

## After selecting the industry
- The code finds a list of stocks satisfying the Benjamen Graham Value Stock Criteria (Modified Altman Z-Score above A- level) and another list of stocks having a Modified Z-Score below BBB- level, both in year 2020.
- Then the code also finds a list of stocks with market-to-book (M2B) above 20 and another list with M2B below 2.0
- Long $50,000 in a stock that is both in the high-credit list and in the low-M2B list 
- Short $50,000 in a stock that is both in the low-credit list and in the high-M2B list 
- Return pairs of stocks with the highest investment return in dollars during the chosen day range


## Structure

![Screenshot](https://github.com/jytjyt05/Best-Investment-Portfolio-in-SP500-Stocks/blob/52649205b7af5f08c94e3949dfc5dd1449b6f6e8/IMG_0230.jpg)

## Sample Run
![Screenshot](https://github.com/jytjyt05/Best-Investment-Portfolio-in-SP500-Stocks/blob/52649205b7af5f08c94e3949dfc5dd1449b6f6e8/IMG_0230.jpg)
