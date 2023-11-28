import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.express as px
import statsmodels.api as sm

# Function to download stock data for a given list of tickers and time period
def download_stock_data(tickers, start_date, end_date):
    df_list = []
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        df_list.append(data)
    return pd.concat(df_list, keys=tickers, names=['Ticker', 'Date']).reset_index()

# Function to calculate moving averages and volatility
def calculate_metrics(df):
    df['MA10'] = df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
    df['MA20'] = df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)
    df['Volatility'] = df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)
    return df

# Function to visualize moving averages
def visualize_moving_averages(df):
    for ticker, group in df.groupby('Ticker'):
        fig_ma = px.line(group, x='Date', y=['Close', 'MA10', 'MA20'], title=f"{ticker} Moving Averages")
        fig_ma.show()

# Function to visualize volatility
def visualize_volatility(df):
    fig_volatility = px.line(df, x='Date', y='Volatility', color='Ticker', title='Volatility of All Companies')
    fig_volatility.show()

# Function to visualize correlation between two stocks
def visualize_correlation(df_corr):
    fig_corr = px.scatter(df_corr, x='Close_AAPL', y='Close_MSFT', trendline='ols', title='Correlation between Apple and Microsoft')
    fig_corr.show()

# Main part of the script
if __name__ == "__main__":
    # Define start and end dates
    start_date = datetime.now() - pd.DateOffset(months=3)
    end_date = datetime.now()

    # Define the list of tickers
    tickers = ['AAPL', 'MSFT', 'NFLX', 'GOOG']

    # Download stock data
    df = download_stock_data(tickers, start_date, end_date)

    # Calculate metrics (moving averages and volatility)
    df = calculate_metrics(df)

    # Visualize moving averages
    visualize_moving_averages(df)

    # Visualize volatility
    visualize_volatility(df)

    # Create a DataFrame for correlation analysis (Apple and Microsoft)
    df_corr = pd.merge(df[df['Ticker'] == 'AAPL'][['Date', 'Close']],
                       df[df['Ticker'] == 'MSFT'][['Date', 'Close']],
                       on='Date', suffixes=('_AAPL', '_MSFT'))

    # Visualize correlation between Apple and Microsoft
    visualize_correlation(df_corr)
