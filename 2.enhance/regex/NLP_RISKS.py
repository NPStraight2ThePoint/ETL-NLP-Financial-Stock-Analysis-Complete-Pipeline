import re
import pandas as pd
import numpy as np

# Function to extract and categorize values
def extract_growth(description):
    if not isinstance(description, str):  # Handle NaN values
        return None, None, None

    earnings_5y, earnings_3y, revenue_1y = None, None, None

    # Match signed or unsigned percentages
    match = re.search(r'(-?\d+(\.\d+)?)%', description)

    if match:
        value = match.group(1)  # Capture the number with potential negative sign

        # Check for earnings forecast (3-year)
        if "Earnings are forecast to decline" in description:
            earnings_3y = f"-{value}%"
        elif "Earnings are forecast to grow" in description:
            earnings_3y = f"{value}%"

        # Check for past earnings growth (5-year)
        if "Earnings have declined" in description:
            earnings_5y = f"-{value}%"
        elif "Earnings have grown" in description:
            earnings_5y = f"{value}%"  # Use the extracted value (preserves negative if present)

        # Check for revenue growth (1-year)
        if "Revenue grew" in description:
            revenue_1y = f"{value}%"
        elif "Revenue has declined" in description:
            revenue_1y = f"-{value}%"

    return revenue_1y, earnings_5y, earnings_3y


# Function to extract gross profit margins with signs and whole numbers
def extract_gross_profit_margins(description):
    if not isinstance(description, str):  # Handle NaN values
        return None, None

    # Match numbers, including whole numbers like '1x' and negatives like '-0.58x'
    matches = re.findall(r'(-?\d+\.?\d*)x', description)

    if len(matches) >= 2:  # Ensure at least two values are found
        return f"{matches[0]}x", f"{matches[1]}x"

    return None, None


# Function to extract profit margins with signs and percentages
def extract_profit_margins(description):
    if not isinstance(description, str):  # Handle NaN values
        return None, None

    # Match percentages, including negative signs (e.g., '-77.27%', '8.18%')
    matches = re.findall(r'(-?\d+\.\d+%)', description)

    if len(matches) >= 2:  # Ensure at least two values are found
        return matches[0], matches[1]

    return None, None


# Function to extract the number of days
def extract_days(description):
    if not isinstance(description, str):  # Handle NaN values
        return None

    # Match the number of days (e.g., '67 days ago', '21 days ago')
    match = re.search(r'(\d+)\s+days\s+ago', description)

    if match:
        return int(match.group(1))  # Return the number of days as an integer

    return None


# Function to extract and format market cap into a single string (e.g. "€1B", "€406M", or "€897")
def extract_and_format_market_cap(description):
    if not isinstance(description, str):  # Handle NaN values
        return ''

    # Regular expression to capture currency symbol, number (with optional commas/decimals), and unit (M/B/K optional)
    match = re.search(r'([€$£¥])([0-9,\.]+)([MBK]?)(?![a-zA-Z])', description)

    if match:
        currency_symbol = match.group(1)  # Currency symbol (€ or $ or other)
        number = match.group(2)  # The number part (with commas/decimals)
        unit = match.group(3)  # Unit (M/B/K, optional)

        # Remove commas for the number part (e.g., "8,700" -> "8700")
        number = number.replace(',', '')

        # If no unit is specified, return the currency with the number only
        if unit == '':
            return f"{currency_symbol}{number}"

        # Format the result as "currency_numberunit" (e.g. "€8700B")
        return f"{currency_symbol}{number}{unit}"
    return ''


# Function to extract whatever is inside the parentheses
def extract_within_parentheses(description):
    if not isinstance(description, str):  # Handle NaN values
        return ''

    # Regular expression to capture whatever is in the parentheses
    match = re.search(r'\((.*?)\)', description)

    if match:
        return match.group(1)  # Return whatever is inside the parentheses
    return ''


# Function to extract percentage from the description
def extract_dividend_yield(description):
    if not isinstance(description, str):  # Handle NaN values
        return ''

    # Regular expression to capture number with % (including decimals)
    match = re.search(r'(\d+\.?\d*)%', description)

    if match:
        return match.group(1) + '%'  # Return the extracted percentage
    return ''  # Return empty if no percentage is found




