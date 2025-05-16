import pandas as pd
import re


def extract_percentage_payout(text):
    if isinstance(text, str):
        text = text.strip()  # Clean up any extra whitespace

        if 'No need to calculate' in text:
            return 'N.A.'
        elif 'Insufficient data' in text:
            return "NULL"  # Return NULL as a string

        match = re.search(r"(\d+(\.\d+)?)%", text)
        return match.group(1) + "%" if match else "N/A"

    return "N/A"


def extract_assets_to_equity(text):
    if isinstance(text, str):  # Ensure it's a string
        # Check for specific phrases and return "N.A." or NULL
        lowered = text.strip().lower()  # Convert to lowercase to avoid case-sensitivity issues
        if 'no need to calculate' in lowered:
            return 'N.A.'
        elif 'insufficient data' in lowered:
            return "NULL"

        # Proceed with the regex if no special phrases were found
        match = re.search(r"(-?\d+(\.\d+)?)x", text)  # Match optional '-' + numbers followed by 'x'
        return match.group(1) + "x" if match else "N/A"

    return "N/A"

# Function to extract Allowance for Bad Loans percentage
def extract_bad_loan_allowance(text):
    if isinstance(text, str):  # Ensure it's a string
        match = re.search(r"(\d+(\.\d+)?)%", text)  # Match numbers followed by '%'
        return match.group(1) + "%" if match else "N/A"
    return "N/A"

# Function to extract Loans to Assets ratio percentage
def extract_loans_to_assets_ratio(text):
    if isinstance(text, str):  # Ensure it's a string
        match = re.search(r"(\d+(\.\d+)?)%", text)  # Match numbers followed by '%'
        return match.group(1) + "%" if match else "N/A"
    return "N/A"

# Function to extract Bad Loans percentage
def extract_bad_loans(text):
    if isinstance(text, str):  # Ensure it's a string
        match = re.search(r"(\d+(\.\d+)?)%", text)  # Match numbers followed by '%'
        return match.group(1) + "%" if match else "N/A"
    return "N/A"

# Function to extract Loans to Deposits ratio
def extract_loans_deposits_ratio(text):
    if isinstance(text, str):
        lowered = text.lower()
        # Handle known non-applicable case
        if "no customer deposits" in lowered:
            return "N.A."
        # Try to extract percentage value
        match = re.search(r"(\d+(\.\d+)?)%", text)
        return match.group(1) + "%" if match else "N.A."
    return "N.A."

# Function to calculate Low Risk % based on High Risk %
def calculate_low_risk(text):
    if isinstance(text, str):  # Ensure it's a string
        match = re.search(r"(\d+(\.\d+)?)%", text)  # Match numbers followed by '%'
        if match:
            high_risk = float(match.group(1))  # Extract high-risk percentage number
            if high_risk == 100:
                return "100%"  # If 100% high-risk, low-risk is 100%
            else:
                low_risk = 100 - high_risk  # Otherwise, subtract from 100%
                return f"{low_risk}%"
    return "No data available"


