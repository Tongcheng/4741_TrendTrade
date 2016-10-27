# 4741 TrendTrade
This is Project for class ORIE 4741 by Tongcheng Li. 

# Quick Overview

In this project, we want to identify relations between Google Trend data and Stock's daily price and volume.
Specifically, we are interested in the following problems:

Given Daily prices (including: open price, close price, daily high price, daily low price) and volume of 500 S&P500 stocks.
We want to find how information of Google Trends contribute to the formation of prices in the following ways:

### (1) How does the Google Trend of stock abbreviated symbols (for example: AAPL for apple stock) indicate price change of the day, max price difference of the day and volume of the day.

Intuitively, we think something that cause significant change in price or volume can be represented in Google Trend information.

### (2) How does the Google Trend of stock abbreviated symbols (for example: AAPL for apple stock) plus some fundamental terminology (For example: debt, EPS (earning per share) etc.) contribute to a stock's price and volume.

This question is more interesting because when fundamental investors search for "AAPL EPS", they are looking for specific information of the stock, which indicates they are more likely (than usual) to buy/sell the stock. From one perspective, this is similar to sentiment indicator which tries to measure the sentiment of a stock in the market.

# Step 1: Data Gathering

Our S&P500 price and volume daily data was from https://quantquote.com/historical-stock-data.

But for our Google Trend data because (1): Google doesn't have an Official API to query Google Trend, (2): Google's unofficial API (I tried one python library called pytrends) was rate limited in a blackbox fashion which limits the efficient and scalable Google Trend data gathering, I have devise some method to gather the data.

The way I use to gather data is simulate manual process of typing a URL in browser, and click 

# Step 2: Data Cleanup

# Step 3: Correlation Modeling

# Midterm Conclusion and Future plans


<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_Volume_Corr.png" height="240">
