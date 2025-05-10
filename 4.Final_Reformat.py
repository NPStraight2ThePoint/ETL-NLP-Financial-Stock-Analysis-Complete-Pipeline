import pandas as pd

df = pd.read_csv('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production_V2/SWS_API_Prod_V2/.venv/output/NLP_ASX_Transposed_ASX_statements_2025-05-01.csv')

#df = pd.read_excel('your_file.xlsx', engine='openpyxl')

# Columns to convert
columns_to_convert=['3Year_Payout Ratio', 'Allowance for Bad Loans (%)', 'Loans to Assets Ratio (%)',
                    'Bad Loans (%)', 'Loans to Deposits Ratio (%)', 'High Risk Liabilities (%)',
                    'Cash Payout Ratio (%)', 'Payout Ratio (%)', 'Dividend Yield %',
                    'Bottom 25% Market Dividend Yield %', 'Top 25% Market Dividend Yield %']

# Convert percentage columns to numeric values and handle invalid entries with 'coerce'
for col in columns_to_convert:
    # Check if the column contains strings (percentage symbols)
    if df[col].dtype == 'object':  # If column has strings (percentage symbols)
        df[col] = pd.to_numeric(df[col].str.rstrip('%'), errors='coerce') / 100
    else:  # If column already contains numeric values (decimals or integers)
        df[col] = df[col] / 100  # Convert numeric values to decimals (e.g., 10 becomes 0.10)

# Display the updated DataFrame
print(df)

# Display the updated DataFrame
print(df)
df.to_csv('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production_V2/SWS_API_Prod_V2/.venv/output/NLP_ASX_Transposed_ASX_statements_2025-05-01.csv', index=False)

