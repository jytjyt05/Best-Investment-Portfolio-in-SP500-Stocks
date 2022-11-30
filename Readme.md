
# Overview

This lightweight Data Analysis, Fintech App is created to find best investment portoflio in a given industry among stocks in S&P 500 index based on an estimation, such estimation has two parts: the stock's modified z-score and the stock's market to book ratio. The programming language is in Python, it also incorporates a tk interface for convinent usage.

# Features
```diff
- The user can enter the day range (such as 2020-01-01 to 2021-09-01).
- The user can also choose the industry from the stocks in S&P 500 index.
```

# Summary
- The code finds a list of stocks satisfying the Benjamen Graham Value Stock Criteria (Modified Altman Z-Score above A- level) and another list of stocks having a Modified Z-Score below BBB- level, both in year 2020.
- Then the code also finds a list of stocks with market-to-book (M2B) above 20 and another list with M2B below 2.0
- Long $50,000 in a stock that is both in the high-credit list and in the low-M2B list 
- Short $50,000 in a stock that is both in the low-credit list and in the high-M2B list 
- Return pairs of stocks with the highest investment return in dollars during the chosen day range


# Structure

![Screenshot1](https://github.com/jytjyt05/Best-Investment-Portfolio-in-SP500-Stocks/blob/52649205b7af5f08c94e3949dfc5dd1449b6f6e8/IMG_0230.jpg)

# Demo Screenshot
Entering informations on the boxes at top, after execution, the result is displayed in the box at the middle right. As we can see, the best investing pair in Energy industry is Long a stock in XOM and Short a stock in OXY.
![Screenshot2](https://github.com/jytjyt05/Best-Investment-Portfolio-in-SP500-Stocks/blob/fe043be706c946e716fcfc2878022ce2bff296f1/IMG.png)
