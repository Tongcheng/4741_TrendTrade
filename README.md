# 4741 TrendTrade
This is Project for class ORIE 4741 by Tongcheng Li. 

# Final Report

In this project, we want to identify relations between Google Trend data and Stock's daily price and volume.
Specifically, we are interested in the following problems:

Given Daily prices (including: open price, close price, daily high price, daily low price) and volume of 500 S&P500 stocks.
We want to find how information of Google Trends contribute to the formation of prices in the following ways:

### (1) How does the Google Trend of stock abbreviated symbols (for example: AAPL for apple stock) indicate price change of the day, max price difference of the day and volume of the day.

This question is interesting because when Google Trend of a stock in spiked, it could mean some major events happened to the company, for example, Apple launched its new products.


# Step 1: Data Gathering

Our S&P500 price and volume daily data was from https://quantquote.com/historical-stock-data.

This data source claims it considers split and dividend adjustments, therefore this source is better than Yahoo finance data, which didn't include split and divident adjustments.

But for our Google Trend data because (1): Google doesn't have an Official API to query Google Trend, (2): Google's unofficial API (I tried one python library called pytrends) was rate limited in a blackbox fashion which limits the efficient and scalable Google Trend data gathering, I have devise some method to gather the data.

The way I use to gather data is simulate manual process of typing a URL in browser, and click some buttons to download the CSV, and move then rename the CSV to appropriate location with proper name. However, this is complicated by the following factors:

#### (1): The python library used (pyautogui) is not very robust in typing characters, so when the script types a uppercase character, sometimes the following characters can change from lowercase to uppercase, which is distorted by pyautogui library.

This is solved by the data verification process in our Data Cleanup session.

#### (2): The typing error can cause systematic problems, for example, if typing wants to make a uppercase character and if the next thing it want to type is enter, then it will likely to trigger hot key in Chrome, which is (Shift + Enter) to open a new window. Similarly, it can open a new tab.

Opening a new tab or window will systematically destroy our GUI automation to gather data because our data gathering is based on pixel wise operations, therefore we have to eliminate this type of problem.

In OS X environment I am using, in order to prevent new tabs, I used a chrome extension of xtab, which limits the number of tabs you can open. We set this limit to 1. In order to prevent new windows, I used a mac software called Keyboard Maestro, which changes the hotkey actions, to change (Shift + Enter)'s effect to go to Keyboard Maestro's official website, but this effect will be cancelled by new tab limit. Therefore new tab and new window problem is solved.

#### (3): Google seems to block IP if we search too much Google Trends. 

This is solved by using VPN at different locations and using incognito mode in browser. It is necessary to change the VPN every 2 hours (Maybe next step can be changing the VPN automatically).

#### (4): Google Trend has different granularity of output given different length of time range queried.

So Google returns daily granularity for Google Trend for date range queries less than 4 months, and the second level is weekly granularity, and the third level is monthly granularity. Therefore in our case, we query every 3 months.

#### (5): Network latency is hard to predict, therefore need redundant time between clicks.

### So Google Trend data we gathered is the 2010-2012's three year data for each abbreviated symbol. Each symbol requires 12 downloads since we are doing 3 month length query range every download.

# Step 2: Data Cleanup

For CSV files downloaded, we want to verify it is correct before using it since there exist possibility of typing the wrong query before download. First, we merge the CSV file of GoogleTrends to the CSV of prices and volume. So we create a csv file for every 3 months between Year [2010,2012]. As a cleanup, we throw away merge CSV files which have too few trade days or too much trade days, because that would mean something is wrong with it. In particular, we throw away CSV with <= 55 trade days and CSV with >=70 trade days, with the concern that normally there are 21 to 22 trade days per month, and other holidays should not affect every 3 month by more than -8 or +6 days.

### Then we define our problem concretely as follows: For each 3-month time frame, given complete Google Trend data and trade data(only happens on business days, which excludes weekends and holidays), try to model the correlation.

Then we notice the map from Trade entries to Trend entries is a one-to-one but not onto mapping. This is equivalent to saying, for each trade entry, there is a trend entry, but not the other way around.

# Step 3: Correlation Modeling on Complete S&P 500 Symbols
First attempt we try is using all 500 S&P stock symbols, with two perspectives:

### Perspective I:

(1): Using the current day Google Trend data to model trading information.

(2): Using the past 3-day arithmetic average to model trading information.

(3): Using the past 7-day arithmetic average to model trading information.

### Perspective II:

(1): Try to model Volume traded.

(2): Try to model Max Price Difference (Daily High Price - Daily Low Price) of the day.

(3): Try to model (Close price - Open price) of the day.

### Currently the criterion we will examine is for all 3-month windows combined, we look at the histogram of r (the correlation coefficient).

##### The histogram of r using 1 day Google Trend information with volume traded, with mean correlation = 0.097:
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_Volume_Corr.png" height="240">

From this plot, even though the correlation information seems low, it is actually very high based on stock markets being very noisy. And this plot has some portion with almost 1 correlation which is interesting.

##### The histogram of r using 1 day Google Trend information with (max price of day - min price of day), with mean correlation = 0.0594.

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_priceMaxMinDiff.png" height="240">

There is certainly a positive correlation between daily price range (can be think of close to volatility) and Google Trends which makes sense: When some big news happens, volatility rises, and on the other hand, people tend to search for stock symbol, which cause Google Trend to rise.

##### The histogram of r using 1 day Google Trend information with (close price of day - open price of day) with mean correlation -0.00513.

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_priceCloseOpenDiff.png" height="240">

From this plot, we notice that change of price of the day is negatively correlated with Google Trend of the day, this can be explained by volatility is asymmetrical in terms of direction. That is, it is more volatile for price to decrease (when stock price plummeted overnight) but not as volatile for price to increase (when price increase steadily though slowly over 3 months due to Good Expectations).

### Then we examine over different time averages of Google Trend:
### 1-day vs. 3-day vs. 7-day Volatility Correlation: with r1 = 0.097, r3 = 0.101, r7 = 0.073.
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_Volume_Corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/3dayArithmeticTrend_volume_corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/7dayArithmeticTrend_Volume_Corr.png" height="180">

We can see that Correlation of Trend with Volatility is less spiked as time range considered is longer. This is because information is dispersed. And it also seems 3-day average is most predictive, which can be think of either (1) appropriate time needed (eigen time) for information to propagate to Google Trend or (2) Saturday and Sunday's cumulative effect on Monday.

### 1-day vs. 3-day vs. 7-day (Max Daily Price - Min Daily Price) Correlation: with r1 = 0.0594, r3 = 0.056, r7 = 0.037.
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_priceMaxMinDiff.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/3dayArithmeticTrend_priceMaxMinDiff_corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/7dayArithmetic_MaxMinPrice_Corr.png" height="180">

### 1-day vs. 3-day vs. 7-day (Daily Close Price - Daily Open Price) Correlation: with r1 = -0.00513, r3 = -0.0055, r7 = -0.0067
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/1dayTrend_priceCloseOpenDiff.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/3dayTrend_CloseOpenDiff_corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/7dayArithmetic_CloseOpenPriceDiff_Corr.png" height="180">

# Step 4: Correlation Modeling on a More Informative Subset of Stock Symbols

Notice that in our select of stock symbols, there are symbols such as 'a', which we don't really know if the person searching 'a' is looking for "Agilent Technologies" which has abbreviation "a" or just typing random things. 

### Therefore we limit the set of symbols we look at to smaller and more informative subset, namely symbols with length >= 3.

### Now the plots over different trade features:

### 1-day vs. 3-day vs. 7-day Volatility Correlation: with r1 = 0.11, r3 = 0.1143, r7 = 0.082.
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/1day_volume_corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/3day_Volume_Corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/7day_Volume_Corr.png" height="180">

We can see that Correlation of Trend with Volatility is less spiked as time range considered is longer. This is because information is dispersed. And it also seems 3-day average is most predictive, which can be think of either (1) appropriate time needed (eigen time) for information to propagate to Google Trend or (2) Saturday and Sunday's cumulative effect on Monday.

### 1-day vs. 3-day vs. 7-day (Max Daily Price - Min Daily Price) Correlation: with r1 = 0.068, r3 = 0.064, r7 = 0.0425.
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/1day_maxminprice_corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/3day_MaxMinPriceDiff_Corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/7day_MaxMinPriceDiff_Corr.png" height="180">

### 1-day vs. 3-day vs. 7-day (Daily Close Price - Daily Open Price) Correlation: with r1 = -0.0044, r3 = -0.0063, r7 = -0.0064
<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/1Day_CloseOpen_Corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/3day_CloseOpenPriceDiff_Corr.png" height="180"> <img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LongNameS%26P500/7day_CloseOpenPriceDiff_Corr.png" height="180">

### After this cleanup, our mean correlation is becoming larger in magnitude, which means filter out short name symbols will increase information in Google Trend signal.

# Step 5: Linear Regression 
First, we try to model the Volume Traded using past 3 days' Google Trend with Linear Regression.
Intuitively, overall Volume should be normalized because large cap stocks will be traded with larger daily volume therefore if we didn't normalize, the prediction will be biased toward large cap stocks. 
Therefore we attempt with the first kind of normalization for Y, which is dividing the original Y value's 3 month average.

So for example, the scatter plot of GoogleTrend of the day (X variable) and Normalized Volume Traded:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/LR_scatter_withoutNormX.png" height="240">

While using Ordinary Linear Regression, our fitted line looks like:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/LR_Line_withoutNormX.png" height="240">

Combine the scatter plot with Ordinary Linear Regression:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/All500S%26Pplots/LR_line_scatter_withoutNormX.png" height="240">

The weights for Linear Regression for Normalized Volume is: coefficient for 2 days before = -2.19 * 1e-3, coefficient for 1 day before = 3.73 * 1e-4, coefficient for current day is 2.99* 1e-3, intercept is 9.24*1e-1.

Notice that in the line plot, even though our X axis is only current day's google trend, the corresponding Y is the predicted Y that considers Google Trend 2 days before and Google Trend 1 day before.

Similarly, We build a Normalized Price for Max - Min price, called NormalizedMaxMinRatio = (Max price - Min price)/mean_over3month(Price).

This regression has regression weight -3.47 * 1e-5 for Google Trend 2 days before, weight -7.02 * 1e-6 for Google Trend 1 day before, weight 4.85 * 1e-5 for current day's Google Trend and intercept 2.3 * 1e-2.

For Normalized Price for Close - Open price, called NormalizedCloseOpenRatio = (Close price - Open price)/mean_over3month(Price).

This regression has regression weight -2.003 * 1e-6 for Google Trend 2 days before, weight 9.91 * 1e-7 for Google Trend 1 day before, weight -9.24 * 1e-7 for current day's Google Trend and intercept 2.77 * 1e-4.








