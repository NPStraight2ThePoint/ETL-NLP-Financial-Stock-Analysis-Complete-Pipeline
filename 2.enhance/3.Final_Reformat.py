import pandas as pd
from dir_nlp_utils import output_dir, FDM

exchanges_file = output_dir / f"exchanges_{FDM}.csv"

df1 = pd.read_csv(exchanges_file, encoding='utf-8')
exchange = df1['exchange'].iloc[0]
STATEMENTS = output_dir / f"NLP_{exchange}_Transposed_{exchange}_statements_{FDM}.csv"
df = pd.read_csv(STATEMENTS)

# Columns to convert
columns_to_convert=['3_Year_Payout Ratio %', 'Allowance for Bad Loans (%)', 'Loans to Assets Ratio (%)',
                    'Bad Loans (%)', 'Loans to Deposits Ratio (%)', 'High Risk Liabilities (%)',
                    'Cash Payout Ratio (%)', 'Payout Ratio (%)', 'Dividend Yield %',
                    'Bottom 25% Market Dividend Yield %', 'Top 25% Market Dividend Yield %',
                    '3-Year Annual Earnings Growth Forecast %',	'3-Year Annual Market Earnings Growth Forecast %',
                    'Savings Rate %', 'Annual Revenue Growth %', 'Annual Market Revenue Growth %',
                    'Profit Growth 1 Year Forecast %', 'Revenue Growth 1Y Forecast%', 'Loss Reduction 1 Year Forecast %',
                    'EPS Growth p.a. Forecast %', 'ROE 3Y Forecast %', 'FCF Historical Growth',	'Operating CF',	'Net debt / Equity ratio',
                    'Net Interest Margin', 'Salary Percentage', 'Bonus Percentage', 'Board Independence',
                    'Industry Average Board Independence', '3 month weekly volatility %',
                    '5 Year Earnings Growth p.a. %', '1 Year Revenue Growth %', 'Last year Net Profit margin %',
                    'Current Net Profit Margin %', '5-year average Earnings growth p.a. %', 'YoY Earnings growth %',
                    'Average annual earnings growth %', 'Industry Average annual earnings growth %',
                    'Average annual revenue growth %', 'ROE %', 'Net margin %', 'YoY Earnings Growth %',
                    'Industry YoY Average Earnings Growth %', 'ShareDilutionPercentage', 'ROE_Percentage',
                    'EarningsGrowthPercentage', 'DividendYieldPercentage', 'Discount to SWS Fair Value Estimate %',
                    'Earnings growth Forecast p.a. %', 'Revenue growth Forecast p.a. %', 'Analyst Price Target %',
                    'Revenue growth 1 Year %', 'Earnings growth 5 Year p.a.%', 'Earnings growth 3 Year Forecast p.a.%',
                    'Profit Margin T-1 Year %', 'Current Profit Margin %', 'Market 1 Year Return %',
                    'Industry 1 Year Return %', 'Industry 30 Day Return %', 'Market 30 Day Return %'
                    ]

# Custom function to handle 'N.A.' and 'NULL' values
def handle_na_null(value):
    # Return the value unchanged if it's 'N.A.' or 'NULL'
    if value == 'N.A.' or value == 'NULL':
        return value
    return value  # Return the value for valid conversion
for col in columns_to_convert:
    if col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Safe divide for numeric types
            df[col] = df[col] / 100
        elif df[col].dtype == 'object':
            # Convert % strings and floats, ignore 'N.A.' or 'NULL'
            def convert_percent(x):
                if isinstance(x, str):
                    if x in ['N.A.', 'NULL']:
                        return x
                    elif '%' in x:
                        try:
                            return float(x.strip('%')) / 100
                        except:
                            return x  # Keep original if conversion fails
                elif isinstance(x, (int, float)):
                    return x / 100
                return x
            df[col] = df[col].apply(convert_percent)

print(df)
df.to_csv(STATEMENTS, index=False)
