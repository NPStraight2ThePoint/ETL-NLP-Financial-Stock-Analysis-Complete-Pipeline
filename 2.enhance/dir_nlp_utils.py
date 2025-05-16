from datetime import datetime
import os
from pathlib import Path

FDM = datetime.now().replace(day=1).strftime("%Y-%m-%d")
BACKUP_DIR = f'C:/.../.venv/Backup'
output_dir = Path('C:/.../.venv/output')
base_directories = [
    'C:/.../.venv/Output']
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

score_categories = {
    "dividends_score": "DIVIDENDS",
    "future_score": "FUTURE",
    "value_score": "VALUE",
    "health_score": "HEALTH",
    "past_score": "PAST"
}
