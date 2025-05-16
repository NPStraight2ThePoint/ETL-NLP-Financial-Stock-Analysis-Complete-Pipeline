import re
import pandas as pd
import numpy as np


# Function to extract percentage from the description
def extract_growth_percentage(description):
    # Ensure the input is a string
    description = str(description)

    # Look for a percentage pattern in the text, focusing on "Earnings" or "Revenue" and ignoring "No data" and "unprofitable"
    match = re.search(r'(\d+(\.\d+)?)%', description)

    if match:
        # Extract the percentage and return with '%'
        return match.group(1) + "%"
    return None  # Return None if no percentage found


# Function to extract percentage from the description
def extract_dividend_yield(description):
    # Ensure the input is a string
    description = str(description)

    # Look for a percentage pattern in the text
    match = re.search(r'(\d+(\.\d+)?)%', description)

    if match:
        # Extract the percentage and return with '%'
        return match.group(1) + "%"
    return None  # Return None if no percentage found


# Function to apply the strategy based on descriptions
def apply_strategy(description):
    # Initialize the fields as None or blank
    pe_ratio = None
    market_pe_ratio = None
    discount_to_sws = None

    # Check if it contains "Price-To-Earnings" and extract numbers
    pe_match = re.search(r'Price-To-Earnings\s*ratio\s*\((\d+(\.\d+)?)x\).*?(\d+(\.\d+)?)x', description)
    if pe_match:
        # Extract the two numbers as P/E Ratio and Market P/E Ratio
        pe_ratio = pe_match.group(1) + 'x'  # Append 'x' to the P/E ratio
        market_pe_ratio = pe_match.group(3) + 'x'  # Append 'x' to the Market P/E ratio

    # Check for percentages indicating discount to fair value
    elif "%" in description and "below" in description:
        discount_match = re.search(r'(\d+(\.\d+)?)%\s*below\s*our\s*estimate', description)
        if discount_match:
            discount_to_sws = discount_match.group(1) + "%"  # Extract and return percentage

    # Check for the "no longer trading below" condition
    elif "no longer trading below" in description:
        discount_to_sws = "0%"

    # If no match, set all fields as N/A or blank
    if pe_ratio is None and discount_to_sws is None and market_pe_ratio is None:
        pe_ratio = 'N/A'
        market_pe_ratio = 'N/A'
        discount_to_sws = 'N/A'

    return pd.Series([pe_ratio, market_pe_ratio, discount_to_sws])


# Function to apply the strategy based on descriptions
def apply_strategy2(description):
    earnings_growth = None
    revenue_growth = None

    # Check for analysts' expectations (both earnings and revenue)
    if re.search(r"Analysts don't expect .*? to grow its revenues next year", description):
        revenue_growth = "0%"
    if re.search(r"Analysts don't expect .*? to grow its earnings next year", description):
        earnings_growth = "0%"

        # Extract earnings growth percentage
    earnings_match = re.search(r'Earnings are forecast to grow (\d+(\.\d+)?)%', description)
    if earnings_match:
        earnings_growth = earnings_match.group(1) + "%"

        # Extract revenue growth percentage
    revenue_match = re.search(r'Revenue is forecast to grow (\d+(\.\d+)?)%', description)
    if revenue_match:
        revenue_growth = revenue_match.group(1) + "%"

        # Default to 'N/A' if no values were extracted
    return pd.Series([earnings_growth or 'N/A', revenue_growth or 'N/A'])


# Function to extract the correct value
def extract_price_target(description):
    if not isinstance(description, str):  # Handle NaN values
        return "N/A"

    if "Analysts not in good agreement" in description:
        return "0%"

    if "Not enough data to determine if stock price will rise" in description:
        return "N/A"

    match = re.search(r'(\d+(\.\d+)?)%', description)  # Extract number%
    return match.group(1) + "%" if match else "N/A"




