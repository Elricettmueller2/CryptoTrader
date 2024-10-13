# backtesting/performance.py

import numpy as np

def calculate_performance_metrics(portfolio, risk_free_rate=0.0):
    returns = portfolio['returns']
    total_return = portfolio['total'][-1] / portfolio['total'][0] - 1
    annualized_return = np.mean(returns) * 252
    annualized_volatility = np.std(returns) * np.sqrt(252)
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    max_drawdown = calculate_max_drawdown(portfolio['total'])
    metrics = {
        'Total Return': total_return,
        'Annualized Return': annualized_return,
        'Annualized Volatility': annualized_volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': max_drawdown,
    }
    return metrics

def calculate_max_drawdown(total_portfolio_value):
    cumulative_max = total_portfolio_value.cummax()
    drawdown = (total_portfolio_value - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()
    return max_drawdown

