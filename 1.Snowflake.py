import psycopg2
import pandas as pd
from datetime import datetime

# Get the first day of the current month
today = datetime.now().replace(day=1)
today = today.strftime("%Y-%m-%d")

# Database connection details
DB_PARAMS = {
            "host": "localhost",
            "port": "5432",
            "database": "Simply_API_Prod",
            "user": "postgres",
            "password": "Arxidolemios39"}

#Define queries
queries = {"company_statements": "SELECT * FROM statements;"}
#queries = {"owners": "SELECT * FROM owners where exchange = 'ASX'"}
EXCEL_FILE = f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production_V2/SWS_API_Prod_V2/.venv/2.Enhancement/Output/Statements_{today}.xlsx'
try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_PARAMS)
    with pd.ExcelWriter(EXCEL_FILE, engine="xlsxwriter") as writer:
        for sheet_name, query in queries.items():
            df = pd.read_sql_query(query, conn)
            df.to_excel(writer, sheet_name=sheet_name, index=False)  # Save each DataFrame to a separate sheet
    print(f"Data saved to {EXCEL_FILE}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()

# Path to the exported Excel file
input_file = EXCEL_FILE
output_file = f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production_V2/SWS_API_Prod_V2/.venv/2.Enhancement/Output/Snowflake_{today}.xlsx'

# Load the Excel file
df = pd.read_excel(input_file, engine="openpyxl")

# Define the columns to keep
columns_to_keep = [
    "ticker", "exchange", "date",
    "VALUE_IsAnalystForecastTrustworthy_Value",
    "VALUE_IsGoodValueComparingPreferredMultipleToIndustry_Value",
    "VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Value",
    "VALUE_IsGoodValueComparingRatioToFairRatio_Value",
    "VALUE_IsUndervaluedBasedOnDCF_Value",
    "VALUE_IsHighlyUndervaluedBasedOnDCF_Value",
    "DIVIDENDS_IsDividendCoveredByFreeCashFlow_Value",
    "DIVIDENDS_IsDividendCovered_Value",
    "DIVIDENDS_IsDividendGrowing_Value",
    "DIVIDENDS_IsDividendSignificant_Value",
    "DIVIDENDS_IsDividendStable_Value",
    "DIVIDENDS_IsDividendYieldTopTier_Value",
    "FUTURE_IsExpectedAnnualProfitGrowthAboveMarket_Value",
    "FUTURE_IsExpectedAnnualProfitGrowthHigh_Value",
    "FUTURE_IsExpectedProfitGrowthAboveRiskFreeRate_Value",
    "FUTURE_IsExpectedRevenueGrowthAboveMarket_Value",
    "FUTURE_IsExpectedRevenueGrowthHigh_Value",
    "FUTURE_IsReturnOnEquityForecastAboveBenchmark_Value",
    "HEALTH_AreLongTermLiabilitiesCovered_Value",
    "HEALTH_AreShortTermLiabilitiesCovered_Value",
    "HEALTH_HasDebtReducedOverTime_Value",
    "HEALTH_IsDebtCoveredByCashflow_Value",
    "HEALTH_IsDebtLevelAppropriate_Value",
    "HEALTH_IsInterestCoveredByProfit_Value",
    "PAST_HasGrownProfitsOverPast5Years_Value",
    "PAST_HasHighQualityPastEarnings_Value",
    "PAST_HasPastNetProfitMarginImprovedOverLastYear_Value",
    "PAST_HasProfitGrowthAccelerated_Value",
    "PAST_IsGrowingFasterThanIndustry_Value",
    "PAST_IsReturnOnEquityAboveThreshold_Value"
]

df = df[columns_to_keep]
df.iloc[:, 3:] = df.iloc[:, 3:].fillna(False).astype(bool).astype(int)


score_categories = {
    "dividends_score": "DIVIDENDS",
    "future_score": "FUTURE",
    "value_score": "VALUE",
    "health_score": "HEALTH",
    "past_score": "PAST"
}

# Compute scores
for score_col, prefix in score_categories.items():
    matching_cols = [col for col in df.columns if col.startswith(prefix)]
    df[score_col] = df[matching_cols].sum(axis=1) / len(matching_cols)

# Compute Overall_Score as the sum of all _Score columns
df["overall_score"] = df[list(score_categories.keys())].sum(axis=1)

# Define final column order (keeping the underlying columns and placing _Score columns after "date")
final_columns = [
    "ticker", "exchange", "date",
    "overall_score", "dividends_score", "future_score", "value_score", "health_score", "past_score",
    "VALUE_IsAnalystForecastTrustworthy_Value",
    "VALUE_IsGoodValueComparingPreferredMultipleToIndustry_Value",
    "VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Value",
    "VALUE_IsGoodValueComparingRatioToFairRatio_Value",
    "VALUE_IsUndervaluedBasedOnDCF_Value",
    "VALUE_IsHighlyUndervaluedBasedOnDCF_Value",
    "DIVIDENDS_IsDividendCoveredByFreeCashFlow_Value",
    "DIVIDENDS_IsDividendCovered_Value",
    "DIVIDENDS_IsDividendGrowing_Value",
    "DIVIDENDS_IsDividendSignificant_Value",
    "DIVIDENDS_IsDividendStable_Value",
    "DIVIDENDS_IsDividendYieldTopTier_Value",
    "FUTURE_IsExpectedAnnualProfitGrowthAboveMarket_Value",
    "FUTURE_IsExpectedAnnualProfitGrowthHigh_Value",
    "FUTURE_IsExpectedProfitGrowthAboveRiskFreeRate_Value",
    "FUTURE_IsExpectedRevenueGrowthAboveMarket_Value",
    "FUTURE_IsExpectedRevenueGrowthHigh_Value",
    "FUTURE_IsReturnOnEquityForecastAboveBenchmark_Value",
    "HEALTH_AreLongTermLiabilitiesCovered_Value",
    "HEALTH_AreShortTermLiabilitiesCovered_Value",
    "HEALTH_HasDebtReducedOverTime_Value",
    "HEALTH_IsDebtCoveredByCashflow_Value",
    "HEALTH_IsDebtLevelAppropriate_Value",
    "HEALTH_IsInterestCoveredByProfit_Value",
    "PAST_HasGrownProfitsOverPast5Years_Value",
    "PAST_HasHighQualityPastEarnings_Value",
    "PAST_HasPastNetProfitMarginImprovedOverLastYear_Value",
    "PAST_HasProfitGrowthAccelerated_Value",
    "PAST_IsGrowingFasterThanIndustry_Value",
    "PAST_IsReturnOnEquityAboveThreshold_Value"
]

# Reorder DataFrame
df = df[final_columns]

# Save the processed data
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Processed data saved to {output_file}")


