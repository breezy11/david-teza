
import pandas as pd

def annualized_return(trades):
    total_return = trades['profit'].sum()
    duration_years = len(trades['entry_date'].dt.year.unique())
    return (1 + total_return) ** (1 / duration_years) - 1

def total_return(trades, initial_investment=100000):
    total_profit = trades['profit'].sum()
    return (total_profit / initial_investment) * 100

def maximum_drawdown(trades):
    cumulative_returns = (1 + trades['profit'].pct_change()).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (peak - cumulative_returns) / peak
    return drawdown.max()

def win_rate(trades):
    wins = trades[trades['profit'] > 0]
    return len(wins) / len(trades) * 100

def profit_factor(trades):
    gross_profit = trades[trades['profit'] > 0]['profit'].sum()
    gross_loss = abs(trades[trades['profit'] < 0]['profit'].sum())
    return gross_profit / gross_loss

# Assuming 'trades' is a DataFrame
# trades = pd.DataFrame(...)  # Define your DataFrame here

# Calculate each metric
# ar = annualized_return(trades)
# tr = total_return(trades)
# mdd = maximum_drawdown(trades)
# wr = win_rate(trades)
# pf = profit_factor(trades)

# Print the calculated metrics
# print("Annualized Return:", ar)
# print("Total Return:", tr)
# print("Maximum Drawdown:", mdd)
# print("Win Rate:", wr)
# print("Profit Factor:", pf)
