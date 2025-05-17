import re
import pandas as pd
# Load CSV File
df = pd.read_csv(r"C:\..\.csv" )  # Replace with actual file path
# Updated regex patterns to support different currency symbols and handle spaces
patterns = {
    "Tenure (years)": r"tenure of ([\d\.]+) years",
    "Yearly Compensation": r"total yearly compensation is ([A-Z$€¥£]{1,3}\s?[\d,.]+[MBK]?)",
    "Salary Percentage": r"comprised of ([\d\.]+)% salary",
    "Bonus Percentage": r"([\d\.]+)% bonuses",
    "Company Share Ownership": r"directly owns ([\d\.]+)% of the company",
    "Share Ownership Value": r"worth ([A-Z$€¥£]{1,3}\s?[\d,.]+[MBK]?)",
    "Average Tenure of Management": r"average tenure of the management team.*?([\d\.]+) years",
    "Average Tenure of Board": r"average tenure.*?board of directors is ([\d\.]+) years"
}

def extract_management_details(text):
    """Extract management details using regex patterns."""
    results = {key: None for key in patterns}  # Initialize results with None

    if isinstance(text, str):  # Ensure the text is valid
        for key, pattern in patterns.items():
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
# Apply extraction function to the column
df_extracted = df["MANAGEMENT_IsBoardMajorityIndependent_Desc"].apply(extract_board_independence)
df = pd.concat([df, df_extracted], axis=1)
df["Board Average Tenure (Years)"] = df["MANAGEMENT_IsBoardSeasoned_Desc"].apply(extract_tenure)
df["3 Year Board Turnover"] = df["MANAGEMENT_IsBoardTurnoverAppropriate_Desc"].apply(extract_turnover)
df["CEO Compensation"] = df["MANAGEMENT_IsCEOCompensationAppropriate_Desc"].apply(lambda x: extract_compensation(x, ceo_comp_pattern))
df["Similar Size Company Market Average Compensation"] = df["MANAGEMENT_IsCEOCompensationAppropriate_Desc"].apply(lambda x: extract_compensation(x, market_comp_pattern))
df["Management Average Tenure (Years)"] = df["MANAGEMENT_IsManagementTeamSeasoned_Desc"].apply(extract_tenure2)

df.to_csv("Clean_Financials.csv", index=False)


