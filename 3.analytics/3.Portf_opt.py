import pandas as pd
import numpy as np
import cvxpy as cp
from config_analytics_utils import output_dir
# Parameters

exchange = 'ASX'

# Save to a new file
enhanced_file = output_dir / f"top_50_companies_final_returns_{exchange}.csv"
optimal_weights_file = output_dir / f'{exchange}_optimized_portfolio_weights.csv'
df = pd.read_csv(enhanced_file)

rf = 0.035  # risk-free rate

# Step 1: Select the asset with highest Sharpe ratio per primary_industry
idx_best = df.groupby('primary_industry')['Sharpe Ratio'].idxmax()
df_selected = df.loc[idx_best].reset_index(drop=True)

# Extract values
returns = df_selected['Total Return'].values
volatilities = df_selected['Volatility %'].values
n = len(df_selected)

# Optimization variables
w = cp.Variable(n, nonneg=True)

# Portfolio return and volatility (assume zero correlations)
portfolio_return = returns @ w
portfolio_volatility = cp.norm(cp.multiply(volatilities, w))

# Objective: maximize Sharpe ratio = (portfolio_return - rf) / portfolio_volatility
# Non-convex, so instead do grid search over volatility or fix volatility and maximize excess return.

constraints = [
    cp.sum(w) == 1,
    w <= 0.20  # Each weight must be less than or equal to 20%
]

best_sharpe = -np.inf
best_weights = None
best_return = None
best_vol = None

# Grid search volatility from 0.5% to 20%
target_vols = np.linspace(0.005, 0.2, 50)

for target_vol in target_vols:
    prob = cp.Problem(cp.Maximize(portfolio_return - rf),
                      constraints + [portfolio_volatility <= target_vol])
    prob.solve(solver=cp.SCS, verbose=False)

    if prob.status == 'optimal':
        ret = portfolio_return.value
        vol = portfolio_volatility.value
        sharpe = (ret - rf) / vol if vol > 1e-8 else 0
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            best_weights = w.value
            best_return = ret
            best_vol = vol

print(f"Best Sharpe Ratio: {best_sharpe:.4f}")
print(f"Portfolio Return: {best_return:.4f}")
print(f"Portfolio Volatility: {best_vol:.4f}")

df_selected['weight'] = best_weights
print(df_selected[['ticker', 'primary_industry', 'weight']])

# Prepare the summary metrics as commented CSV header
summary_lines = [
    f"# Best Sharpe Ratio: {best_sharpe:.4f}",
    f"# Portfolio Return: {best_return:.4f}",
    f"# Portfolio Volatility: {best_vol:.4f}"
]

# Generate CSV body of the weights table
csv_body = df_selected.to_csv(index=False)

# Combine and write out
with open(optimal_weights_file, 'w') as f:
    f.write("\n".join(summary_lines) + "\n")
    f.write(csv_body)

print(f"✅ Saved portfolio weights and metrics to '{optimal_weights_file}'")
