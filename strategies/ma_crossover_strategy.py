# imports
import pandas as pd
import numpy as np
import ta  # Technical Analysis library for trading indicators

# Custom import for additional metrics calculation (not used in this example but included for structure)
from metrics_calculation import *


def load_data(filepath):
	"""
	Load the dataset and set the index to datetime.
	"""
	df = pd.read_csv(filepath, index_col=0)
	df.index = pd.to_datetime(df.index)
	return df


def prepare_data(df, split_date):
	"""
	Prepare training and testing datasets based on the split date provided.
	Find the start date for the test set 10 data points before the split date.
	"""
	test_start_date = df[df.index < split_date].index[-10]  # Adjust the offset if needed
	df_test = df[(df.index >= test_start_date) & (df.index < '2024-01-01')]
	df_train = df[df.index < test_start_date]
	return df_train, df_test


def calculate_sma(df):
	"""
	Calculate short-term and long-term simple moving averages (SMAs).
	"""
	df_return = df.copy()

	df_return['sma_short'] = ta.trend.SMAIndicator(df_return['Close'], window=5).sma_indicator()
	df_return['sma_long'] = ta.trend.SMAIndicator(df_return['Close'], window=10).sma_indicator()
	df_return.dropna(inplace=True)  # Ensure all NA values are dropped to avoid issues in trading signals
	return df_return


def generate_signals(df):
	"""
	Generate trading signals based on SMA crossovers.
	"""
	df_return = df.copy()
	df_return['signal'] = np.where(df_return['sma_short'] > df_return['sma_long'], 1, np.where(df_return['sma_short'] < df_return['sma_long'], -1, 0))
	return df_return


def simulate_trades(data):
	"""
	Simulate trading based on SMA crossover signals, assuming an initial capital of $100,000.
	"""
	position = 0
	cash = 100000  # Initial capital
	trade_history = []

	data.reset_index(inplace=True)

	for index, row in data.iterrows():
		if row['signal'] == 1 and position == 0:  # Buy signal
			position = 1
			entry_price = row['Close']
			entry_date = row['Date']
		elif row['signal'] == -1 and position == 1:  # Sell signal
			position = 0
			exit_price = row['Close']
			exit_date = row['Date']
			profit = (exit_price - entry_price) * (cash / entry_price)  # Update to calculate actual profit
			cash += profit
			trade_history.append({
				'entry_date': entry_date,
				'exit_date': exit_date,
				'entry_price': entry_price,
				'exit_price': exit_price,
				'profit': profit
			})

	return pd.DataFrame(trade_history)

def backtest_ma():
	# Load and prepare data
	df = load_data('data/crude_oil_daily.csv')
	df_train, df_test = prepare_data(df, '2018-01-01')

	# Calculate SMAs and generate signals
	df_test = calculate_sma(df_test)
	df_test = generate_signals(df_test)

	# Simulate trades
	trades = simulate_trades(df_test)

	return trades


