# authors: Affrin Sultana, Helin Wang, Shi Yan Wang and Pavel Levchenko
# January,2022

# import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader as pdr
import datetime
import warnings
alt.renderers.enable('altair_viewer')

def percent_change(stock_ticker, start_date, end_date):
    """
    Calculates daily percentage change of a stock price within a given period of time
    
    Parameters
    ----------
    stock_ticker : string 
        Ticker of the stock such as 'AAPL'
    start_date : string
        Initial date for data extraction
    end_date : string
        Final date for stock analysis
    
    Returns
    --------
    DataFrame
        A data frame with dates and their corresponding stock price percentage changes.
    
    Examples
    --------
    >>> percent_change('AAPL', '2017-01-01', '2017-01-10')
                    Price Change Percentage(%) 
              Date
        2017-01-03                        0.000
        2017-01-04                       -0.112
        2017-01-05                        0.396
        2017-01-06                        1.515
        2017-01-09                        2.445
    """ 
    
    # Assert ticker input value
    ticker = yf.Ticker(stock_ticker)
    if(ticker.info["regularMarketPrice"] == None):
        raise NameError("You have entered an invalid stock ticker! Try again.")
    
    # Assert start date input value
    format = "%Y-%m-%d"
    try: datetime.datetime.strptime(start_date, format)
    except ValueError:
        raise ValueError("You have entered an invalid start date! Try date formatted in YYYY-MM-DD.")
    
    # Assert end date input value
    try: datetime.datetime.strptime(end_date, format)
    except ValueError:
        raise ValueError("You have entered an invalid end date! Try date formatted in YYYY-MM-DD.")

    # Assert end date is later than start date
    format = "%Y-%m-%d"
    if(datetime.datetime.strptime(end_date, format) < datetime.datetime.strptime(start_date, format)):
        raise ValueError("You have entered an end date which is earlier than the start date! Try again.")
    
    # Import original dataframe by giving stock ticker, start data and end date
    data = yf.download(stock_ticker, start=start_date, end=end_date)
    
    # Only Keep "Adj Close" Price for 
    data = data.drop(columns={'Open', 'High', 'Low', 'Adj Close', 'Volume'})
    
    # Carry out calculation
    for i in range(1,len(data)):
        data.iloc[i,:] = round((data.iloc[i,:] - data.iloc[0,:])/data.iloc[0,:]*100, 3)
    
    data.iloc[0,:] = round((data.iloc[0,:] - data.iloc[0,:])/data.iloc[0,:]*100, 3)
    
    # Manipulate column name
    data = data.rename(columns={"Close": "Price Change Percentage(%)"})
    
    # Return result
    return pd.DataFrame(data)


def profit_viz(stock_ticker, start_date , end_date, benchmark_ticker):
    """
    Visualizes trend of a stock price change against the market benchmark within a given period of time
    
    Parameters
    ----------
    stock_ticker : string
        Ticker of the stock such as 'AAPL'
    start_date : string 
        Initial date for data extraction
    end_date : string
        Final date for stock analysis
    benchmark_ticker : string 
        Ticker for benchmark comparison such as 'SP500' 
    
    Returns
    --------
    Altair Chart
        A line chart which shows percentage change in stock price and market performance over time 
    
    Examples
    --------
    >>> profit_viz('AAPL', '2015-01-01', '2021-12-31', 'SP500')
    """

    
    ticker = yf.Ticker(stock_ticker)
    bench_ticker = yf.Ticker(benchmark_ticker)

    try:
         # Assert ticker input value
        if(ticker.info["regularMarketPrice"] == None):
            raise NameError("You have entered an invalid stock ticker! Try again.")

        # check data type of input
        if type(stock_ticker) != str:
            raise TypeError("stock_ticker should be of type string.")
    
     # Assert benchmark ticker input value
    
        if(bench_ticker.info["regularMarketPrice"] == None):
            raise NameError("You have entered an invalid benchmark ticker! Try again.")

    # check data type of input
        if type(benchmark_ticker) != str:
            raise TypeError("Bench Mark ticker should be of type string.")
    
    # #check stock ticker and bench mark ticker are not same
    #     if stock_ticker is bench_ticker:
    #         raise NameError("Stock Mark ticker should not be same as Bench Ticker.")

    # #check stock ticker is not empty
    #     if not stock_ticker or not bench_ticker:
    #         raise ValueError("'Tickers' cannot be empty")

    # Assert start date input value
        format = "%Y-%m-%d"
        try: datetime.datetime.strptime(start_date, format)
        except ValueError:
            raise ValueError("You have entered an invalid start date! Try date formatted in YYYY-MM-DD.")
    
    # Assert end date input value
        try: datetime.datetime.strptime(end_date, format)
        except ValueError:
            raise ValueError("You have entered an invalid end date! Try date formatted in YYYY-MM-DD.")

    # Assert end date is later than start date
        format = "%Y-%m-%d"
        if(datetime.datetime.strptime(end_date, format) < datetime.datetime.strptime(start_date, format)):
            raise ValueError("You have entered an end date which is earlier than the start date! Try again.")
       
    except (TypeError, ValueError, NameError) as err:
        print(err)
        raise 

    # Code to generate the visualization of profit 
    try:
        stock_profit = percent_change(stock_ticker, start_date, end_date).reset_index()
        benchmark_profit = percent_change(benchmark_ticker, start_date, end_date).reset_index()
        profit_df = pd.merge(stock_profit, benchmark_profit, on="Date")
        profit_df.rename({'Price Change Percentage(%)_x': 'Profit Percent Stock', 'Price Change Percentage(%)_y': 'Profit Percent Benchmark'}, axis=1, inplace=True)
    # catch when dataframe is None
    except AttributeError:
        pass

    #Checks if the datatype of data frame is correct
    try:
        isinstance(profit_df, pd.DataFrame)
    except ValueError:
        raise ValueError("profit_df is not a pandas dataframe.")
    
    try:
        isinstance(stock_profit, pd.DataFrame)
    except ValueError:
        raise ValueError("stock_profit couldnot be converted to a pandas dataframe.")

    try:
        isinstance(benchmark_profit, pd.DataFrame)
    except ValueError:
        raise ValueError("Benchmark_profit couldnot be converted to a pandas dataframe.")

    # Code to plot the profit visualization
    chart = alt.Chart(profit_df, title='Profit Percent trend of Stock vs Benchmark ticker').mark_line().transform_fold(
    fold=['Profit Percent Stock', 'Profit Percent Benchmark'], 
    as_=['company', 'Profit Percent']
).encode(
    x='Date:T', 
    y = alt.Y('Profit Percent:Q', axis=alt.Axis(format='$.2f')),
    color=alt.Color('company:N', scale= alt.Scale(domain=['Profit Percent Stock','Profit Percent Benchmark'], range=['red', 'blue'])),
    tooltip=[alt.Tooltip('Profit Percent Stock'),alt.Tooltip('Profit Percent Benchmark')]
)
    return chart

    
def volume_change(stock_ticker, start_date, end_date):
    """ 
    Calculates the daily trading volume change status of a stock within a given period of time

    Parameters
    ----------
    stock_ticker : string 
        Ticker of the stock such as 'AAPL'
    start_date : string
        Initial date for data extraction
    end_date : string 
        Final date for stock analysis

    Returns
    --------
    DataFrame
        A data frame with dates and their corresponding trading volume and changes

    Examples
    --------
        >>> volume_change('AAPL', '2021-01-01', '2022-01-01')
        Date             Volume       Volume_Change
        01-01-2021        1000        Nan
        01-02-2021        2000        Increase
        01-03-2021        3000        Increase
        01-04-2021        2500        Decrease
        ...
        12-31-2021        4000        Increase
        01-01-2022        5000        Increase
    """
    # Assert ticker value
    ticker = yf.Ticker(stock_ticker)
    if(ticker.info["regularMarketPrice"] == None):
        raise NameError("You have entered an invalid stock ticker! Try again.")
        
    # Assert date value
    format = "%Y-%m-%d"
    try: datetime.datetime.strptime(start_date, format)
    except ValueError:
        raise ValueError("You have entered an invalid start date! Try again.")
    try: datetime.datetime.strptime(end_date, format)
    except ValueError:
        raise ValueError("You have entered an invalid end date! Try again.")
        
    df = pdr.get_data_yahoo(stock_ticker, start=start_date, end=end_date).reset_index()
    
    # Assert correct data fetched
    try:
        isinstance(df, pd.DataFrame)
    except ValueError:
        raise ValueError("Your input can't be converted to a pandas dataframe.")
    
    df["Price_diff"] = df["Close"].diff().to_frame()
    df['Price_change'] = np.select([df["Price_diff"] > 0, df["Price_diff"] < 0],
                                 ["Increase", "Decrease"], default = np.nan)
    return df[["Date", "Volume", "Price_change"]]
    

def volume_viz(stock_ticker, start_date, end_date):
    """
    Visualize the daily trading volume of a stock using bar plot within a given period of time
    
    Parameters
    ----------
    stock_ticker : string 
        Ticker of the stock such as 'AAPL'
    start_date : string
        Initial date for data extraction
    end_date : string 
        Final date for stock analysis
    
    Returns
    --------
    Chart
        Create interactive bar plot to view the volume change
    
    Examples
    --------
    >>> volume_viz('AAPL', '2021-01-01', '2022-01-01')
    """
    try:
        vdf = volume_change(stock_ticker, start_date, end_date)
    # catch when dataframe is None
    except AttributeError:
        raise AttributeError("Invalid volume change input!")
    

    vdf_increase = vdf.loc[vdf['Price_change']=='Increase']
    vdf_decrease = vdf.loc[vdf['Price_change']=='Decrease']


    fig = go.Figure()
    fig.add_trace(go.Bar(x=vdf_increase['Date'], y=vdf_increase['Volume'],
                    base=0,
                    marker_color='green',
                    name='Price Increase'))
    fig.add_trace(go.Bar(x=vdf_decrease['Date'], y=vdf_decrease['Volume'],
                    base=0,
                    marker_color='red',
                    name='Price Decrease'
                    ))

    return fig
