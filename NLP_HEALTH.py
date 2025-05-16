import pandas as pd
import re

# Function to extract values inside parentheses
def extract_values(text):
    if isinstance(text, str):
        matches = re.findall(r"\(([^)]+)\)", text)  # Extract all values inside parentheses
        if len(matches) == 2:
            return matches[0], matches[1]  # Return short-term assets & long-term liabilities
        elif "no long term liabilities" in text:
            return "No Data", "No Data"
        elif "negative shareholder equity" in text:
            return "No Data", "No Data"
    return None, None
# Function to extract values inside parentheses
def extract_values_shortterm(text):
    if isinstance(text, str):
        matches = re.findall(r"\(([^)]+)\)", text)  # Extract all values inside parentheses
        if len(matches) == 2:
            return matches[1]  # Return short-term assets & long-term liabilities
        elif "no short term liabilities" in text:
            return "No Data"
        elif "negative shareholder equity" in text:
            return "No Data"
    return None


# Function to extract Cash Runway and FCF Growth
def extract_values2(text):
    if isinstance(text, str):
        text = text.strip().lower()  # Normalize text

        # Extract the last percentage value in the text
        percentage_matches = re.findall(r"([-+]?\d+\.\d+)%", text)
        fcf_growth = percentage_matches[-1] if percentage_matches else "No Data"

        # If "reduce" is in the text, ensure the percentage is negative
        if "reduce" in text and fcf_growth != "No Data":
            if not fcf_growth.startswith("-"):
                fcf_growth = "-" + fcf_growth

        # Extract Cash Runway
        cash_runway_match = re.search(r"(\d+\.?\d*)\s*(years?|months?)", text)
        if cash_runway_match:
            cash_runway = f"{cash_runway_match.group(1)} {cash_runway_match.group(2).capitalize()}"
        elif "less than a year" in text:
            cash_runway = "1 Year"  # Handling "less than a year" case
        else:
            cash_runway = "No Data"

        return cash_runway, fcf_growth

    return "No Data", "No Data"  # Default return for non-string inputs
# Function to extract and format D/E ratios
def extract_de_ratios(text):
    percentages = re.findall(r"(\d+\.?\d*)%", text)  # Find all percentage values
    if len(percentages) == 2:
        return float(percentages[1]), float(percentages[0])  # Second is current, first is T-5
    elif len(percentages) == 1:
        return "", float(percentages[0])  # Only T-5 is available
    else:
        return "", ""  # No percentage found

# Function to extract Net Debt to EBITDA ratio from parentheses
def extract_net_debt_ebitda(text):
    match = re.search(r"\((-?\d+\.?\d*x)\)", text)  # Extract number inside ()
    return match.group(1) if match else ""  # Return extracted value or empty string

# Function to extract percentage from parentheses
def extract_percentage(text):
    match = re.search(r"\((\d+\.?\d*)%\)", text)  # Extract percentage inside ()
    return match.group(1) + "%" if match else ""  # Return extracted value or empty string

# Function to extract number with 'x' from parentheses
def extract_ratio(text):
    match = re.search(r"\(assets are ([\d\.]+x) debt\)", text)  # Extract number + 'x'
    return match.group(1) if match else ""  # Return extracted value or empty string

# Function to extract percentages from parentheses
def extract_percentage_D_E(text):
    match = re.search(r"\((\d+\.?\d*)%\)", text)  # Extract number with '%'
    return match.group(1) + "%" if match else ""  # Return extracted value or empty string

# Function to extract number + 'x' from parentheses
def extract_interest_coverage(text):
    match = re.search(r"\((\d+\.?\d*x)\s", text)  # Extract number with 'x'
    return match.group(1) if match else ""  # Return extracted value or empty string


# Define regex patterns for each metric
patterns1 = {
        "Shareholder equity": r"total shareholder equity of [^\d]*([\d\.]+[MBK])",
        "Total Debt": r"total debt of [^\d]*([\d\.]+[MBK])",
        "Total Assets": r"total assets and total liabilities are [^\d]*([\d\.]+[MBK])|total assets of [^\d]*([\d\.]+[MBK])",
        "Total Liabilities": r"total assets and total liabilities are [^\d]*[\d\.]+[MBK] and [^\d]*([\d\.]+[MBK])",
        "EBIT": r"EBIT is [^\d]*([\d\.]+[MBK])",
        "Cash and Short term Investments": r"cash and short-term investments of [^\d]*([\d\.]+[MBK])",
        "Net Interest Margin": r"Net Interest Margin of [^\d]*([\d\.]+%)",
        "Total Deposits": r"total deposits are [^\d]*([\d\.]+[MBK])",
        "Total Loans": r"total loans are [^\d]*([\d\.]+[MBK])"
}

# Function to extract values while maintaining order
def extract_financials(text):
    """Extract financial values and place them correctly, skipping missing ones."""
    results = {key: None for key in patterns1}  # Initialize with None

    if isinstance(text, str):  # Ensure input is valid
        for key, pattern in patterns1.items():
            match = re.search(pattern, text)
            if match:
                # Check for group match and assign the result (can be multiple groups)
                results[key] = next((m for m in match.groups() if m), None)

    return pd.Series(results)






