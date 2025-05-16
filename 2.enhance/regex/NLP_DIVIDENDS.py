import pandas as pd
import re


def extract_cash_payout(text):
    if isinstance(text, str):
        lowered = text.lower()

        # Case 1: Extract % if present and convert to decimal
        match = re.search(r"(\d+(\.\d+)?)\s*%", text)
        if match:
            return float(match.group(1)) / 100  # ✅ Convert to decimal here

        # Case 2: Handle 'Insufficient data' as NULL
        if 'insufficient data' in lowered:
            return None

        # Case 3: Handle known non-applicable phrases
        if any(phrase in lowered for phrase in [
            "unable to calculate",
            "not paying a notable dividend",
            "no free cash flows",
            "has not reported any payouts"
        ]):
            return "N.A."

    # Case 4: Return N.A. for anything else
    return "N.A."


def extract_payout(text):
    if isinstance(text, str):
        lowered = text.lower()

        # Case 1: Extract % if present and convert to decimal
        match = re.search(r"(\d+(\.\d+)?)\s*%", text)
        if match:
            return float(match.group(1)) / 100  # ✅ Convert to decimal here

        # Case 2: Handle 'Insufficient data' as NULL
        if 'insufficient data' in lowered:
            return None

        # Case 3: Handle known non-applicable phrases
        if any(phrase in lowered for phrase in [
            "unable to calculate",
            "not paying a notable dividend",
            "no free cash flows",
            "has not reported any payouts"
        ]):
            return "N.A."

    # Case 4: Return N.A. for anything else
    return "N.A."

def extract_yield(text):
    if not isinstance(text, str):
        return "N.A."

    # Clean and normalize whitespace
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    text = re.sub(r'\s+', ' ', text).strip()

    lowered = text.lower()
    if "unable to evaluate" in lowered:
        return "N.A."

    # Extract % and convert to decimal
    match = re.search(r'([\d.]+)\s*%', text)
    return float(match.group(1)) / 100 if match else "N.A."

def extract_low25_yield(text):
    if isinstance(text, str):
        lowered = text.lower()

        # Handle cases like "Unable to evaluate"
        if "unable to evaluate" in lowered or "insufficient data" in lowered:
            return "N.A."

        # Extract all % values
        matches = re.findall(r"(\d+\.\d+|\d+)\s*%", text)

        if len(matches) >= 3:
            return float(matches[2]) / 100  # Convert 3rd match to decimal
        else:
            return "N.A."

    return "N.A."

def extract_top25_yield(text):
    if isinstance(text, str):
        lowered = text.lower()
        if "unable to evaluate" in lowered or "insufficient data" in lowered:
            return "N.A."
        matches = re.findall(r"(\d+\.\d+|\d+)\s*%", text)
        if len(matches) >= 3:
            return float(matches[2]) / 100  # Return as decimal
        else:
            return "N.A."
    return "N.A."

# Function to extract Next Payment Date and Ex-Date
def extract_dividend_dates(text):
    if isinstance(text, str):  # Ensure input is a string
        matches = re.findall(r"(\d{1,2}(?:st|nd|rd|th)?\s+\w+,\s+\d{4})", text)
        if len(matches) >= 2:  # If at least two dates exist
            return matches[0], matches[1]  # Extract Next Payment Date and Ex-Date
    return "N/A", "N/A"  # If not found, return N/A




