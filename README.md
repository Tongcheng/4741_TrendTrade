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

# Step 5: Linear Regression (A Failed Attempt) 
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

This means simply using Linear Regression is not satisfactory, because it offer almost no predictive power in this case.

# Step 6: Linear Regression with Feature Engineering

Next, we define what really should be our objectives and use cases of Google Trend. 

### Feature Engineering: Z-score

Qualitatively the following holds: Google Trend of a stock's abbreviation, as a indicator, varies some amount by each day, and some proportion of the variation is correlated with the stock's volume or price change.

But this does not necessarily mean this qualitative statement can be easily converted to a quantitative statement. Consider the following 2 examples: 

Example 1: ABC, which stands for AmerisourceBergen Corp, a healthcare company, can also refer to English Alphabet in general (i.e. This 6 year old boy is just learning his ABCs). And when people are typing ABC, most of the cases are they are referring to the English Alphabet, therefore the Google Trend for ABC have a very small signal to noise ratio. 

Example 2: AAPL, which stands for Apple Inc, is not naturally a word. And at least as far as I know, AAPL does not have any connotations other than referring to the company Apple. Therefore the Google Trend for AAPL have a large signal to noise ratio.

Based on this observation, intuitively we want to "normalize" the signal to noise ratio for each company so that each abbreviation's Google Trend, after some feature transformation, should have similar impacts. 

We do this by the classical trick: First remove the mean, then devide by standard deviation. (Both mean and standard deviation is calculated using the 3 month horizen.)

Similarly, we have similar considerations for Y variables (Volume, (Max - Min) daily price,(Close - Open) daily price). For example, some small cap company can be very volatile but most large cap companies tend to be not very volatile (for most time).

We treat the Y values by also using Z-score as feature transformation (remove mean than devide by standard deviation).

### Feature Engineering: Avoid Future Function Bias

We also want to remove the bias of using future functions. That is using the information that is only available in future at a certain time point. We do this by changing the X vector to: Google Trend Z score {3 days before, 2 days before, 1 day before}.

For plotting, for each of {Volume prediction, Max - Min daily price prediction, Close - Open daily price prediction}, we have 3 plots, left one is the regression line, where the x-axis is the Google Trend Z score one day before, y-axis is the predicted value given information of 3-dimensional X vector; middle one is regression line with all the data points scattered; right one is the error distribution where X axis is Z_pred - Z_true.

For volume we have the following plot:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_V_line.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_V_Scatter.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_error_V.png" height="180">

For Max - Min daily price we have the following plot:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_MM_line.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_MM_scatter.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_error_MM.png" height="180">

For Close - Open daily price we have the following plot:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_CO_line.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_CO_scatter.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/LRplots/LR_error_CO.png" height="180">

According to the error Distribution plot, the error distribution do have fat tail in the negative direction. And Z = Z_pred - Z_true = -7 does occur for few data points' predictions. I think this corresponds to Z_true = Z_pred + 7, which is underestimated Volume traded.

Error of 7 standard deviation is absolutely a phenomena. This corresponds to severely under-estimated volume traded which corresponds to black swan events (event that is totally unexpected, originally from the scenario when you suppose a group of swans in the lake are all white swans, until you see a black swan, which changes your previous hypothesis) but statistically black swan events happens more often than expected.

On the other hand, the mean absolute error is in 0.68 for Volume, 0.73 for Max-Min daily price, 0.78 for Close-Open daily price, this verifies what we already know about the ordinary linear regression use maximum likelihood estimation, which is sensitive to outliers.

But by Law of Large Numbers, as long as we predict correctly consistently, we will make money (if we disregard complication such as transaction cost).

With Feature Engineering, this Linear Regression Model tells us the following improvements:

(1): There is certainly some black swan events that make certain cases very volatile (So much more volume traded). One way to model such events are using quantile regression for top quantiles, modeling such events are meaningful, as they could, in theory, provide us profitable opportunities if we can foresee black-swan events because people are less rational and more error-prone in trading during black-swan (or totally unexpected) events.

(2): Similar to quantile regression, we could find companies that more the best fit for our approach. That is, for every company, we evaluate the effectiveness of our model, and we only apply the model to the most effective set of companies.

This corresponds to the real world case where our alpha-generating method has is conditional on the companies selected.

# Step 7: Quantile Regression

Then I try Quantile Regression to model the top Volume changes, quantile regression models the response variable (y) for a given quantile (q) conditioned on variable x. In my case, variable x is vector with 3 elements, namely: Z-score of Google Trend 3 days before, Z-score Google Trend 2 days before and Z-score Google Trend 1 day before. The Y variable is Z-score of the volume traded.

The following plot on the left is Quantile Regression for corresponding quantities {Volume, Max - Min price, Close - Open price} for quantile = [0.5,0.55,0.6,...,0.95], while the plot on the right is Quantile Regression for quantile = [0.9,0.91,...,0.99].

The Volume Quantile plot is follows:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/Qplots/Q_V_Line.png" height="240"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/Qplots/Q_V_99_Line.png" height="240">

The Max-Min Daily price Quantile is follows:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/Qplots/Q_MM_Line.png" height="240"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/Qplots/Q_MM_99_Line.png" height="240">

The Close-Open Daily price Quantile is follows:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/Qplots/Q_CO_Line.png" height="240"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/Qplots/Q_CO_99_Line.png" height="240">

For all the 6 plots, the higher up a line is, the higher up percentile it belongs to, notice the even though x-axis is only the Google Trend Z-score one day before, Y-axis (predicted Y) use all information available in X vector's 3 coordinates. 

# Step 8: Linear Regression for each individual stocks:

Another natural idea to utilize the power of Google Trend is to build models for every individual stock, and only pick models that work relatively well. 

In this case, we will care Volume, (Max - Min) Daily Price and (Close - Open) Daily Price.

After doing 3 regressions on all stocks with abbreviation length >=3, we have the following error distribution plot:

<img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/MultiErr2/MultiErr2_V.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/MultiErr2/MultiErr2_MM.png" height="180"><img src="https://github.com/Tongcheng/4741_TrendTrade/blob/master/MultiErr2/MultiErr2_CO.png" height="180">

And we shall pick the stocks that will really work well for our models.

# Step 9: Alpha Generation and Backtesting

### Alpha:

The word Alpha in the title of step has its root in CAPM (Capital Asset Pricing Model), defined as the excess return over benchmark, and Alpha is uncorrelated with market risk. Intuitively, it means how well the fund/strategy is performing.

In a broader context, Alpha means the captured signal that could systematically generate profit for the strategy. And this is the meaning here for Alpha Generation.

The intuition of my Alpha signal is that, based on regression results, buy or sell some quantity of the stock proportional to the predicted value of (close - open) daily price, the frequency of the trading is once per trading day.

### Backtesting:

The word Backtesting in my title means the procedure for which quants test how well a strategy is performing, and also analyze the performance characteristics of a strategy. Some common performance characteristics include: return, sharpe ratio, sortino ratio, maximum downturn etc. These characteristics measure how well is the strategy is in return and risk.

However, in real world, backtesting does not mean everything. Because there are usually a lot of other factors in the real world that makes practice (real world money making) harder than backtesting. One example is market may not have enough liquidity when you are trying to buy. Another example is execution may have more latency than required which makes alpha-generating ideas not realizable. One particular case where execution's negative impact on strategy is called slippage, which means when you detect the price you want to trade, you trade at a less favorable price because you are too slow. The importance of these cases about the importance of execution (trading system) are especially important in cases such as high frequency market making.

For my backtest framework, I use first 2 years' (2010 and 2011) data to train the regression weight W_CO for each stock. Then use these trained weights, I test the results on the third year's (2012) to see the trajectory of return within 2012.

My backtest framework serves as the test for how well my strategy performs, the backtesting on every symbol with long enough symbol name (see step 4, a more informative subset of symbols) and enough clean data. Then it gets two indicators: (1) return and (2) sharpe ratio.

The return indicator measures how much money my strategy returns, but one disadvantage of return indicator is that it does not measure risk.

The Sharpe ratio is defined as Sharpe Ratio:=(return - risk_free_return)/(standar_deviation_of_returns). Usually the risk_free_return is assumed to be interest rate, in my case the risk_free_return is assumed to be 0 for simplicity. Sharpe ratio measures the ratio of return divided by risk. Sharpe ratio is the how good a strategy can be if it can be given leverage (means how good a strategy can be if it is given enough money scalability by borrowing money.)

The additional assumptions my backtesting framework makes are:

(1) In each day, we start with an empty portfolio, and end with a empty portfolio. We buy and sell stocks according to our alpha signal's direction and amount within the day to ensure that the portfolio is empty by the end of the day. This implicitly assumes there is enough liquidity in the market.

(2) The backtesting framework also assumes that we can short stock without any constraint. In real world, this assumption does not hold because there are usually short margin requirements for each account, that basically means you need to have enough money in your account to do the short. Here we remove this constraint to make backtesting easier.

(3) 

# Step 10: Optimal Allocation and Portfolio Optimization



