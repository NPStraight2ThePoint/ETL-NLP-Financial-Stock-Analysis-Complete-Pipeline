import re
import pandas as pd
import numpy as np

# Function to extract growth rate percentage
def extract_growth_rate(text):
    if isinstance(text, str):
        match = re.search(r"(-?\d+\.?\d*)%", text)
        return float(match.group(1)) if match else None
    return None

def determine_sign(text, value):
    if value is None:
        return None
    if "declined" in text or "losses have increased" in text:
        return -abs(value)  # Ensure it's negative
    elif "reduced losses" in text or "grown" in text or "growing" in text:
        return abs(value)   # Ensure it's positive
    return value  # Default case (no change)

# Function to handle missing or insufficient data
def extract_earnings_growth(text):
    if "Insufficient data" in text or "Unable to establish" in text:
        return None
    raw_value = extract_growth_rate(text)
    return determine_sign(text, raw_value)

# Function to extract and format gain/loss
def extract_gain_loss(text):
    match = re.search(r'of ([\w€$£¥.,-]+) .*? to (.+)\.', text)
    if match:
        amount, date = match.groups()
        if "loss" in text:
            return f"- {amount} ({date})"
        elif "gain" in text:
            return f"+ {amount} ({date})"
    return None

# Function to extract percentage value
def extract_percentage(text):
    match = re.search(r'([-+]?\d+\.\d+%)', text)  # Extracts percentage with sign
    return match.group(1) if match else None  # Return extracted value or None

# Updated Function to extract percentages (both whole numbers and decimals)
def extract_net_profit_margins(text):
    matches = re.findall(r'([-+]?\d+\.?\d*%)', text)  # Updated regex to include whole numbers
    if len(matches) == 2:
        return matches[1], matches[0]  # (Last Year, Current)
    return None, None  # Return None if not found

# Function to extract earnings growth percentages
def extract_earnings_growth2(text):
    matches = re.findall(r'([-+]?\d+\.?\d*)%', text)  # Extract whole numbers & decimals
    if len(matches) == 2:
        return matches[1], matches[0]  # (5-year avg, YoY growth)
    return None, None  # Return None if not found

# Function to extract Operating Years
def extract_operating_years(text):
    match = re.search(r'(\d+)\s+years?', text)  # Extract the first number before 'years'
    return int(match.group(1)) if match else None  # Convert to integer


# Function to extract numbers or return N/A if data is insufficient
def extract_numbers(text):
    if not isinstance(text, str) or "There is insufficient data" in text:  # Handle missing data
        return ["N/A"] * 5

    # Extract both whole numbers and decimals (including negative values)
    numbers = re.findall(r"-?\d+\.?\d*|\d+", text)
    numbers = [float(num) for num in numbers]  # Convert to float

    # Ensure all expected values are present
    while len(numbers) < 5:
        numbers.append(np.nan)  # Use NaN for missing values

    return numbers[:5]  # Extract only the first 5 numbers

# Convert to percentage format, replacing NaN with "N/A"
def format_percent(value):
    if pd.isna(value) or value == "N/A":
        return "N/A"
    return f"{value:.2f}%"

# Function to extract all percentages (inside or outside parentheses)
def extract_growth_numbers(text):
    if not isinstance(text, str) or "Insufficient data" in text:
        return ["N/A", "N/A"]  # If insufficient data, return "N/A"

    # Extract all numbers followed by '%', whether in parentheses or not
    matches = re.findall(r"(-?\d+\.?\d*)%", text)

    # Format the extracted numbers correctly
    if len(matches) >= 2:
        return [f"{matches[0]}%", f"{matches[1]}%"]
    elif len(matches) == 1:
        return ["N/A", f"{matches[0]}%"]
    else:
        return ["N/A", "N/A"]  # No valid numbers found


# Function to extract percentage from the description
def extract_percentage2(description):
    # Ensure the input is a string
    description = str(description)

    # Look for a percentage pattern in the text
    match = re.search(r'(\d+(\.\d+)?)%', description)
    if match:
        return match.group(1) + "%"  # Append the '%' sign to the extracted number
    return None  # Return None if no percentage found


# Function to extract percentage from the description
def extract_roe_percentage(description):
    # Ensure the input is a string
    description = str(description)

    # Look for a percentage pattern in the text
    match = re.search(r'(-?\d+(\.\d+)?)%', description)  # Handles negative percentages as well
    if match:
        return match.group(1) + "%"  # Append the '%' sign to the extracted number
    return None  # Return None if no percentage found




