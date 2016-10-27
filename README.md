# 4741 TrendTrade
This is Project for class ORIE 4741 by Tongcheng Li. 

# Quick Overview

In this project, we want to identify relations between Google Trend data and Stock's daily price and volume.
Specifically, we are interested in the following problems:

Given Daily prices (including: open price, close price, daily high price, daily low price) and volume of 500 S&P500 stocks.
We want to find how information of Google Trends contribute to the formation of prices in the following ways:

### (1) How does the Google Trend of stock abbreviated symbols (for example: AAPL for apple stock) indicate price change of the day, max price difference of the day and volume of the day.

### (2) How does the Google Trend of stock abbreviated symbols (for example: AAPL for apple stock) plus some fundamental terminology (For example: debt, EPS (earning per share) etc.) contribute to a stock's price and volume.

This question is more interesting because when fundamental investors search for "AAPL EPS", they are looking for specific information of the stock, which indicates they are more likely (than usual) to buy/sell the stock. From one perspective, this is similar to sentiment indicator which tries to measure the sentiment of a stock in the market.

# Step 1: Data Gathering

Our S&P500 price and volume daily data was from https://quantquote.com/historical-stock-data.

This data source claims it considers split and dividend adjustments, therefore this source is better than Yahoo finance data, which didn't include split and divident adjustments.

But for our Google Trend data because (1): Google doesn't have an Official API to query Google Trend, (2): Google's unofficial API (I tried one python library called pytrends) was rate limited in a blackbox fashion which limits the efficient and scalable Google Trend data gathering, I have devise some method to gather the data.

The way I use to gather data is simulate manual process of typing a URL in browser, and click some buttons to download the CSV, and move then rename the CSV to appropriate location with proper name. However, this is complicated by the following factors:

####(1): The python library used (pyautogui) is not very robust in typing characters, so when the script types a uppercase character, sometimes the following characters can change from lowercase to uppercase, which is distorted by pyautogui library.

This is solved by the data verification process in our Data Cleanup session.

####(2): The typing error can cause systematic problems, for example, if typing wants to make a uppercase character and if the next thing it want to type is enter, then it will likely to trigger hot key in Chrome, which is (Shift + Enter) to open a new window. Similarly, it can open a new tab.

Opening a new tab or window will systematically destroy our GUI automation to gather data because our data gathering is based on pixel wise operations, therefore we have to eliminate this type of problem.

In OS X environment I am using, in order to prevent new tabs, I used a chrome extension of xtab, which limits the number of tabs you can open. We set this limit to 1. In order to prevent new windows, I used a mac software called Keyboard Maestro, which changes the hotkey actions, to change (Shift + Enter)'s effect to go to Keyboard Maestro's official website, but this effect will be cancelled by new tab limit. Therefore new tab and new window problem is solved.

####(3): Google seems to block IP if we search too much Google Trends. 

This is solved by using VPN at different locations and using incognito mode in browser. It is necessary to change the VPN every 2 hours (Maybe next step can be changing the VPN automatically).

# Step 2: Data Cleanup

# Step 3: Correlation Modeling

# Midterm Conclusion and Future plans


<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_Volume_Corr.png" height="240">
