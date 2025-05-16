import pandas as pd
import re

# Function to extract the Yearly Earnings Growth Forecast and Yearly Market Earnings Growth Forecast
def extract_growth_forecasts(text):
    if isinstance(text, str):  # Ensure input is a string
        # Regex pattern to match percentages
        matches = re.findall(r"(-?\d+\.\d+%)", text)  # Capture percentages with optional negative sign
        if len(matches) >= 2:  # If two percentages exist
            return matches[0], matches[1]  # Extract first (company's growth) and second (market's growth)
        elif len(matches) == 1:  # If only one percentage exists, return 'N/A' for the missing one
            return matches[0], "N/A"
    return "N/A", "N/A"  # If no match found, return "N/A"

# Function to extract the savings rate percentage after [[savings rate]]
def extract_savings_rate(description):
    # Regex to find the savings rate percentage in parentheses following [[savings rate]]
    match = re.search(r"\[\[savings rate\]\]\s?\((\d+(\.\d+)?)%\)", description)
    if match:
        return match.group(1)  # Return the savings rate as a string (without the decimal part if no decimal)
    return None

def extract_earnings_growth_zero(text):
    if not isinstance(text, str):
        return None

    lowered = text.lower()

    # Handle specific cases
    if "insufficient data" in lowered:
        return None
    if "is forecast to become profitable over the next 3 years" in lowered:
        return 0

    # Clean text
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    text = re.sub(r'\s+', ' ', text)

    # Extract percentage
    match = re.search(r'(-?\d+(?:\.\d+)?)\s*%', text)
    return float(match.group(1)) if match else None

def extract_second_percentage(text):
    if not isinstance(text, str):
        return None
    # Clean up invisible characters and normalize whitespace
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    text = re.sub(r'\s+', ' ', text)
    # Find all percentages
    matches = re.findall(r'(-?\d+(?:\.\d+)?)\s*%', text)
    return float(matches[1]) if len(matches) > 1 else None

# Function to extract the profit growth percentage
def extract_profit_growth(text):
    if not isinstance(text, str):
        return None

    lowered = text.lower()

    # Handle specific condition
    if "not forecast to become profitable next year" in lowered:
        return 0

    # Try extracting the percentage
    match = re.search(r"(-?\d+\.\d+)%", text)
    if match:
        return float(match.group(1))

    return None

# Function to extract only the percentage value
def extract_revenue_growth(text):
    if not isinstance(text, str):
        return None
    lowered = text.lower()
    if "not expected to generate any revenue next year" in lowered:
        return 0
    match = re.search(r"(-?\d+\.\d+|-?\d+)%", text)
    return float(match.group(1)) if match else None


# Function to extract the correct percentage
def extract_loss_forecast(text):
    if isinstance(text, str):
        lowered = text.lower()

        # Case: No losses to reduce
        if "there are no losses to reduce" in lowered:
            return "N.A."

        # Case: Reduce losses
        match_reduce = re.search(r"reduce its losses by (\d+\.?\d*)%", text)
        if match_reduce:
            return float(match_reduce.group(1))  # Positive percentage

        # Case: Worsen losses
        match_worsen = re.search(r"worsen by (\d+\.?\d*)%", text)
        if match_worsen:
            return -float(match_worsen.group(1))  # Negative percentage

    return None  # Default if no match

# Function to extract EPS growth dynamically
def extract_eps_growth(text):
    if isinstance(text, str):
        # Match positive EPS growth
        match_growth = re.search(r"EPS is expected to grow by (-?\d+\.?\d*)%", text)
        if match_growth:
            return float(match_growth.group(1))  # Keep as-is
        match_decline = re.search(r"EPS is expected to decline by (-?\d+\.?\d*)%", text)
        if match_decline:
            return -float(match_decline.group(1))  # Convert to negative
    return None

# Function to extract ROE forecast dynamically
def extract_roe(text):
    if isinstance(text, str):
        match_roe = re.search(r"Return on equity is forecast to be (-?\d+\.?\d*)% in 3 years", text)
        if match_roe:
            return float(match_roe.group(1))
    return None

def extract_roe_2(text):
    if not isinstance(text, str):
        return None
    match = re.search(r'(-?\d+(?:\.\d+)?)\s*%', text)
    return float(match.group(1)) if match else None

def extract_earnings_growth_zero_2(text):
    if not isinstance(text, str):
        return None

    lowered = text.lower()

    # Handle specific cases
    if "insufficient data" in lowered:
        return None
    if "is forecast to become profitable over the next 3 years" in lowered:
        return 0
    if "no revenue next year" in lowered:
        return 0

    # Clean text
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    text = re.sub(r'\s+', ' ', text)

    # Extract percentage
    match = re.search(r'(-?\d+(?:\.\d+)?)\s*%', text)
    return float(match.group(1)) if match else None

