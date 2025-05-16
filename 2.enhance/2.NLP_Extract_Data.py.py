import pandas as pd
import re

from NLP_BANK import *
from NLP_DIVIDENDS import *
from NLP_FUTURE import *
from NLP_HEALTH import *
from NLP_MARKET import *
from NLP_PAST import *
from NLP_REWARDS import *
from NLP_RISKS import *
from NLP_VALUE import *
import os
import glob
from dir_nlp_utils import base_directories

patterns2 = {
    "Tenure (years)": r"tenure of ([\d\.]+) years",
    "Yearly Compensation": r"total yearly compensation is ([A-Z$€¥£]{1,3}\s?[\d,.]+[MBK]?)",
    "Salary Percentage": r"comprised of ([\d\.]+)% salary",
    "Bonus Percentage": r"([\d\.]+)% bonuses",
    "Company Share Ownership": r"directly owns ([\d\.]+)% of the company",
    "Share Ownership Value": r"worth ([A-Z$€¥£]{1,3}\s?[\d,.]+[MBK]?)",
    "Average Tenure of Management": r"average tenure of the management team.*?([\d\.]+) years",
    "Average Tenure of Board": r"average tenure.*?board of directors is ([\d\.]+) years"}

def apply_nlp_operations(df):
    # !!!!!!!!!!!!!!!!!NLP_BANK!!!!!!!!!!!!!!!!!!
    df["3_Year_Payout Ratio %"] = df["BANK_DIVIDENDS_IsDividendCoveredIn3Years_Desc"].apply(extract_percentage_payout)
    df["Assets to Equity ratio"] = df["BANK_HEALTH_HasAnAppropriateLevelOfAssets_Desc"].apply(extract_assets_to_equity)
    df["Allowance for Bad Loans (%)"] = df["BANK_HEALTH_HasAppropriateBadLoanAllowance_Desc"].apply(extract_bad_loan_allowance)
    df["Loans to Assets Ratio (%)"] = df["BANK_HEALTH_HasAppropriateLoanLevel_Desc"].apply(extract_loans_to_assets_ratio)
    df["Bad Loans (%)"] = df["BANK_HEALTH_HasAppropriateNonPerformingLoans_Desc"].apply(extract_bad_loans)
    df["Loans to Deposits Ratio (%)"] = df["BANK_HEALTH_HasPrimarilyDepositFunding_Desc"].apply(extract_loans_deposits_ratio)
    df["High Risk Liabilities (%)"] = df["BANK_HEALTH_HasPrimarilyLowRiskFunding_Desc"].apply(calculate_low_risk)

    # !!!!!!!!!!!!!!!!!NLP_DIVIDENDS!!!!!!!!!!!!!!!!!!
    df["Cash Payout Ratio (%)"] = df["DIVIDENDS_IsDividendCoveredByFreeCashFlow_Desc"].apply(extract_cash_payout)
    df["Payout Ratio (%)"] = df["DIVIDENDS_IsDividendCovered_Desc"].apply(extract_payout)
    df["Dividend Yield %"] = df["DIVIDENDS_IsFruitfulDividendIntro_Desc"].apply(extract_yield)
    df["Bottom 25% Market Dividend Yield %"] = df["DIVIDENDS_IsDividendSignificant_Desc"].apply(extract_low25_yield)
    df["Top 25% Market Dividend Yield %"] = df["DIVIDENDS_IsDividendYieldTopTier_Desc"].apply(extract_top25_yield)
    df[["Next Payment Date", "Ex-Date"]] = df["DIVIDENDS_IsFruitfulDividendIntro_Desc"].apply(lambda x: pd.Series(extract_dividend_dates(x)))

    # !!!!!!!!!!!!!!!!!NLP_FUTURE!!!!!!!!!!!!!!!!!!
    df["3-Year Annual Earnings Growth Forecast %"] = df["FUTURE_IsExpectedAnnualProfitGrowthAboveMarket_Desc"].apply(extract_earnings_growth_zero)
    df["3-Year Annual Market Earnings Growth Forecast %"] = df["FUTURE_IsExpectedAnnualProfitGrowthAboveMarket_Desc"].apply(extract_second_percentage)
    df["Savings Rate %"] = df["FUTURE_IsExpectedProfitGrowthAboveRiskFreeRate_Desc"].apply(extract_savings_rate)
    df['Annual Revenue Growth %'] = df['FUTURE_IsExpectedRevenueGrowthAboveMarket_Desc'].apply(extract_earnings_growth_zero_2)
    df['Annual Market Revenue Growth %'] = df['FUTURE_IsExpectedRevenueGrowthAboveMarket_Desc'].apply(extract_second_percentage)
    df['Profit Growth 1 Year Forecast %'] = df['FUTURE_IsExpectedToGrowProfitNextYear_Desc'].apply(extract_profit_growth)
    df["Revenue Growth 1Y Forecast%"] = df["FUTURE_IsExpectedToGrowRevenueNextYear_Desc"].apply(extract_revenue_growth)
    df["Loss Reduction 1 Year Forecast %"] = df["FUTURE_IsExpectedToReduceLossNextYear_Desc"].apply(extract_loss_forecast)
    df["EPS Growth p.a. Forecast %"] = df["FUTURE_IsFruitfulFutureIntro_Desc"].apply(extract_eps_growth)
    df["ROE 3Y Forecast %"] = df["FUTURE_IsReturnOnEquityForecastAboveBenchmark_Desc"].apply(extract_roe_2)

    # !!!!!!!!!!!!!!!!!NLP_HEALTH!!!!!!!!!!!!!!!!!!
    df[["Short Term Assets", "Long Term Liabilities"]] = df["HEALTH_AreLongTermLiabilitiesCovered_Desc"].apply(
        lambda x: pd.Series(extract_values(x)))
    df["Short Term Liabilities"] = df["HEALTH_AreShortTermLiabilitiesCovered_Desc"].apply(extract_values_shortterm)
    df[["Cash Runway", "FCF Historical Growth"]] = df["HEALTH_HasCashRunwayIfGrowing_Desc"].apply(
        lambda x: pd.Series(extract_values2(x)))
    df[["D/E Ratio", "D/E Ratio T-5 Year"]] = df["HEALTH_HasDebtReducedOverTime_Desc"].apply(
        lambda x: pd.Series(extract_de_ratios(x)))
    df["Net Debt to Ebitda"] = df["HEALTH_HasHighNetDebtToEBITDA_Desc"].apply(extract_net_debt_ebitda)
    df["Operating CF"] = df["HEALTH_IsDebtCoveredByCashflow_Desc"].apply(extract_percentage)
    df["Short term Assets / Debt"] = df["HEALTH_IsDebtCoveredByShortTermAssets_Desc"].apply(extract_ratio)
    df["Net debt / Equity ratio"] = df["HEALTH_IsDebtLevelAppropriate_Desc"].apply(extract_percentage_D_E)
    df["EBIT Interest coverage"] = df["HEALTH_IsInterestCoveredByProfit_Desc"].apply(extract_interest_coverage)
    df[list(patterns1.keys())] = df["HEALTH_IsGoodHealthIntro_Desc"].apply(extract_financials)

    # !!!!!!!!!!!!!!!!!NLP_MANAGEMENT!!!!!!!!!!!!!!!!!!
    def extract_management_details(text):
        """Extract management details using regex patterns."""
        results = {key: None for key in patterns2}  # Initialize results with None
        if isinstance(text, str):  # Ensure the text is valid
            for key, pattern in patterns2.items():
                match = re.search(pattern, text)
                if match:
                    results[key] = match.group(1).strip()  # Extract matched values and remove extra spaces
        return pd.Series(results)

    def extract_board_independence(text):
        """Extracts board independence percentages from the text description."""
        results = {"Board Independence": None, "Industry Average Board Independence": None}
        if isinstance(text, str):  # Ensure text is valid
            percentages = re.findall(r"(\d+)%", text)  # Extract all percentages
            if len(percentages) >= 2:
                results["Board Independence"] = percentages[0] + "%"
                results["Industry Average Board Independence"] = percentages[1] + "%"
            elif len(percentages) == 1:
                results["Board Independence"] = percentages[0] + "%"
        return pd.Series(results)

    # Function to extract tenure value from the description
    def extract_tenure(text):
        match = re.search(r"(\d+(\.\d+)?) years", text)
        return float(match.group(1)) if match else None

    # Function to extract the number of new directors
    def extract_turnover(text):
        if isinstance(text, str):  # Ensure the value is a string
            match = re.search(r"\((\d+) new directors\)", text)
            return int(match.group(1)) if match else None
        return None  # Return None if the value is not a string

    # Function to extract compensation values
    def extract_compensation(text, pattern):
        if isinstance(text, str):
            match = re.search(pattern, text)
            return match.group(1) if match else None
        return None

    # Patterns to extract values
    ceo_comp_pattern = r"\(\$(USD[\d\.MK]+)\)"  # Extracts first $USDxxx value
    market_comp_pattern = r"\(\$(USD[\d\.MK]+)\)\.$"  # Extracts last $USDxxx value

    # Function to extract management tenure (years)
    def extract_tenure2(text):
        if isinstance(text, str):
            match = re.search(r"(\d+\.?\d*) years", text)
            return float(match.group(1)) if match else None
        return None

    df_extracted = df["MANAGEMENT_HasManagementInformationIntro_Desc"].apply(extract_management_details)
    df = pd.concat([df, df_extracted], axis=1)  # Merge extracted data into the original DataFrame
    df_extracted = df["MANAGEMENT_IsBoardMajorityIndependent_Desc"].apply(extract_board_independence)
    df = pd.concat([df, df_extracted], axis=1)
    df["Board Average Tenure (Years)"] = df["MANAGEMENT_IsBoardSeasoned_Desc"].apply(extract_tenure)
    df["3 Year Board Turnover"] = df["MANAGEMENT_IsBoardTurnoverAppropriate_Desc"].apply(extract_turnover)
    df["CEO Compensation"] = df["MANAGEMENT_IsCEOCompensationAppropriate_Desc"].apply(lambda x: extract_compensation(x, ceo_comp_pattern))
    df["Similar Size Company Market Average Compensation"] = df["MANAGEMENT_IsCEOCompensationAppropriate_Desc"].apply(lambda x: extract_compensation(x, market_comp_pattern))
    df["Management Average Tenure (Years)"] = df["MANAGEMENT_IsManagementTeamSeasoned_Desc"].apply(extract_tenure2)

    # !!!!!!!!!!!!!!!!!NLP_MARKET!!!!!!!!!!!!!!!!!!
    df['3 month weekly volatility %'] = df['MARKET_HasPriceStabilityOverPast3Months_Desc'].apply(extract_last_percentage)

    # !!!!!!!!!!!!!!!!!NLP_PAST!!!!!!!!!!!!!!!!!!
    df["5 Year Earnings Growth p.a. %"] = df["PAST_HasGrownProfitsOverPast5Years_Desc"].apply(extract_earnings_growth)
    df["12 month One-Off Gain/Loss"] = df["PAST_HasHighQualityPastEarnings_Desc"].apply(extract_gain_loss)
    df["1 Year Revenue Growth %"] = df["PAST_HasIncreasedRevenueOverPastYear_Desc"].apply(extract_percentage)
    df[["Last year Net Profit margin %", "Current Net Profit Margin %"]] = df["PAST_HasPastNetProfitMarginImprovedOverLastYear_Desc"].apply(
        lambda x: pd.Series(extract_net_profit_margins(x)))
    df[["5-year average Earnings growth p.a. %", "YoY Earnings growth %"]] = df["PAST_HasProfitGrowthAccelerated_Desc"].apply(
        lambda x: pd.Series(extract_earnings_growth2(x)))
    df["Operating Years"] = df["PAST_HasTradedFor3Years_Desc"].apply(extract_operating_years)
    df[['Average annual earnings growth %',
        'Industry Average annual earnings growth %',
        'Average annual revenue growth %',
        'ROE %',
        'Net margin %']] = df['PAST_IsFruitfulPastIntro_Desc'].apply(lambda x: pd.Series(extract_numbers(x)))
    df[['Average annual earnings growth %',
        'Industry Average annual earnings growth %',
        'Average annual revenue growth %',
        'ROE %',
        'Net margin %']] = df[['Average annual earnings growth %',
                               'Industry Average annual earnings growth %',
                               'Average annual revenue growth %',
                               'ROE %',
                               'Net margin %']].applymap(format_percent)
    df[['YoY Earnings Growth %', 'Industry YoY Average Earnings Growth %']] = df['PAST_IsGrowingFasterThanIndustry_Desc'].apply(lambda x: pd.Series(extract_growth_numbers(x)))
    df['ShareDilutionPercentage'] = df['PAST_IsNotDilutedOverPastYear_Desc'].apply(extract_percentage2)
    df['ROE_Percentage'] = df['PAST_IsReturnOnEquityAboveThreshold_Desc'].apply(extract_roe_percentage)

    # !!!!!!!!!!!!!!!!!NLP_REWARDS!!!!!!!!!!!!!!!!!!
    df['EarningsGrowthPercentage'] = df['REWARDS_HasBeenGrowingProfitOrRevenue_Desc'].apply(extract_growth_percentage)
    df['DividendYieldPercentage'] = df['REWARDS_IsDividendAttractive_Desc'].apply(extract_dividend_yield)
    df[['P/E Ratio', 'Market P/E Ratio', 'Discount to SWS Fair Value Estimate %']] = df['REWARDS_IsGoodValue_Desc'].apply(
        apply_strategy)
    df[['Earnings growth Forecast p.a. %', 'Revenue growth Forecast p.a. %']] = df[
        'REWARDS_IsGrowingProfitOrRevenue_Desc'].apply(apply_strategy2)
    df["Analyst Price Target %"] = df["REWARDS_IsTradingBelowAnalystPriceTargets_Desc"].apply(extract_price_target)

    # !!!!!!!!!!!!!!!!!NLP_RISKS!!!!!!!!!!!!!!!!!!
    df[['Revenue growth 1 Year %', 'Earnings growth 5 Year p.a.%', 'Earnings growth 3 Year Forecast p.a.%']] = df[
        'RISKS_AreRevenueAndEarningsExpectedToGrow_Desc'].apply(lambda x: pd.Series(extract_growth(x)))
    df[['Gross Profit Margin T-1 Year', 'Current Gross Profit Margin']] = df[
        'RISKS_HasDecliningGrossProfitMargins_Desc'].apply(
        lambda x: pd.Series(extract_gross_profit_margins(x)))
    df[['Profit Margin T-1 Year %', 'Current Profit Margin %']] = df['RISKS_HasDecliningProfitMargins_Desc'].apply(
        lambda x: pd.Series(extract_profit_margins(x)))
    df['Last filed financial statements (days)'] = df['RISKS_HasFiledWithin6Months_Desc'].apply(extract_days)
    df['Market Cap'] = df['RISKS_HasMeaningfulMarketCap_Desc'].apply(extract_and_format_market_cap)
    df['Extracted_Value'] = df['RISKS_HasMeaningfulRevenue_Desc'].apply(extract_within_parentheses)
    #df['Dividend Yield %'] = df['RISKS_IsDividendSustainable_Desc'].apply(extract_dividend_yield)

    # !!!!!!!!!!!!!!!!!NLP_VALUE!!!!!!!!!!!!!!!!!!
    df[["Industry", "AVG Industry P/E"]] = df["VALUE_IsUndervaluedOnPERelativeToPeers_Desc"].apply(extract_industry_and_pe)
    df[["P/E Ratio 2", "AVG Market P/E Ratio 2"]] = df["VALUE_IsUndervaluedOnPERelativeToMarket_Desc"].apply(extract_pe_ratios)
    df[['Market', 'Market 1 Year Return %']] = df['VALUE_Is1YearReturnInLineOrAboveMarket_Desc'].apply(lambda x: pd.Series(extract_market_and_return(x)))
    df[['Market / Industry', 'Industry 1 Year Return %']] = df['VALUE_Is1YearReturnInLineOrAboveIndustry_Desc'].apply(lambda x: pd.Series(extract_industry_and_return(x)))
    df["Industry 30 Day Return %"] = df["VALUE_Is30DayReturnInLineOrAboveIndustry_Desc"].apply(extract_percentage)
    df["Market 30 Day Return %"] = df["VALUE_Is30DayReturnInLineOrAboveMarket_Desc"].apply(extract_percentage2)
    df[["Company Ratio", "Industry Avg Ratio", "Preferred Multiple"]] = df["VALUE_IsGoodValueComparingPreferredMultipleToIndustry_Desc"].apply(extract_ratios).apply(pd.Series)
    df["P/S Ratio"] = df.apply(lambda row: row["Company Ratio"] if row["Preferred Multiple"] == "P/S" else "N/A", axis=1)
    df["Industry AVG P/S Ratio"] = df.apply(lambda row: row["Industry Avg Ratio"] if row["Preferred Multiple"] == "P/S" else "N/A", axis=1)
    df["P/B Ratio"] = df.apply(lambda row: row["Company Ratio"] if row["Preferred Multiple"] == "P/B" else "N/A", axis=1)
    df["Industry AVG P/B Ratio"] = df.apply(lambda row: row["Industry Avg Ratio"] if row["Preferred Multiple"] == "P/B" else "N/A", axis=1)
    df["P/E Ratio"] = df.apply(lambda row: row["Company Ratio"] if row["Preferred Multiple"] == "P/E" else "N/A", axis=1)
    df["Industry AVG P/E Ratio"] = df.apply(lambda row: row["Industry Avg Ratio"] if row["Preferred Multiple"] == "P/E" else "N/A", axis=1)
    df.drop(columns=["Company Ratio", "Industry Avg Ratio"], inplace=True)
    df[["Peer AVG Ratio", "Preferred Multiple"]] = df["VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Desc"].apply(extract_peer_avg).apply(pd.Series)
    df["Peer AVG P/S Ratio"] = df.apply(lambda row: row["Peer AVG Ratio"] if row["Preferred Multiple"] == "P/S" else "N/A",axis=1)
    df["Peer AVG P/B Ratio"] = df.apply(lambda row: row["Peer AVG Ratio"] if row["Preferred Multiple"] == "P/B" else "N/A",axis=1)
    df["Peer AVG P/E Ratio"] = df.apply(lambda row: row["Peer AVG Ratio"] if row["Preferred Multiple"] == "P/E" else "N/A",axis=1)
    df.drop(columns=["Peer AVG Ratio"], inplace=True)
    df["Fair P/S"] = df.apply(lambda row: row["Fair Ratio"] if row["Preferred Multiple"] == "Fair P/S" else "N/A", axis=1)
    df["Fair P/E"] = df.apply(lambda row: row["Fair Ratio"] if row["Preferred Multiple"] == "Fair P/E" else "N/A", axis=1)
    df[["Current Price", "DCF Fair Value"]] = df["VALUE_IsUndervaluedBasedOnDCF_Desc"].apply(extract_prices).apply(pd.Series)
    df[["Fair Ratio", "Preferred Multiple"]] = df["VALUE_IsGoodValueComparingRatioToFairRatio_Desc"].apply(extract_fair_ratio).apply(pd.Series)
    df.drop(columns=["Fair Ratio"], inplace=True)
    df[["Industry_2", "P/B Ratio 2", "Industry_2 AVG P/B Ratio"]] = df["VALUE_IsUndervaluedBasedOnPB_Desc"].apply(extract_pb_data).apply(pd.Series)
    df["PEG Ratio"] = df["VALUE_IsUndervaluedBasedOnPEG_Desc"].apply(extract_peg_ratio)

    # List of prefixes to match
    prefixes = ["VALUE_", "RISKS_", "REWARDS_", "PAST", "MISC", "MARKET_", "MANAGEMENT_", "HEALTH_", "FUTURE_", "DIVIDENDS_", "BANK_"]
    pattern = '|'.join([f"^{prefix}" for prefix in prefixes])
    columns_to_drop = [col for col in df.columns if re.match(pattern, col)]
    df.drop(columns=columns_to_drop, inplace=True)
    return df

for base_directory in base_directories:
    print(f"🔍 Processing directory: {base_directory}")
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if "transposed" in file.lower() and file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"📄 Processing: {file_path}")
                try:
                    df = pd.read_csv(file_path)
                    df = apply_nlp_operations(df)
                    new_file_name = f"NLP_{file}"
                    new_file_path = os.path.join(root, new_file_name)
                    df.to_csv(new_file_path, index=False)
                    print(f"✅ NLP processed file saved: {new_file_path}")
                except Exception as e:
                    print(f"❌ Failed to process {file_path} due to error: {e}")
