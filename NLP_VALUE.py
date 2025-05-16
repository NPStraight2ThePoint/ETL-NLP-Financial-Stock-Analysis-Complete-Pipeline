import re
import pandas as pd
import numpy as np

# Function to extract industry and return percentage
def extract_industry_and_return(description):
    if not isinstance(description, str):  # Handle NaN values
        return '', ''
    # Extract industry name (Assumes "industry" is a keyword at the end of the name)
    industry_match = re.search(r'the (.*?) industry', description)
    industry = industry_match.group(1) if industry_match else ''
    # Extract industry return percentage
    return_match = re.search(r'(-?\d+\.?\d*)%', description)
    industry_return = return_match.group(1) + '%' if return_match else ''
    return industry, industry_return

# Function to extract market and return percentage
def extract_market_and_return(description):
    if not isinstance(description, str):  # Handle NaN values
        return '', ''
    # Extract market name (Assumes "Market" follows the market name)
    market_match = re.search(r'the (.*?) Market', description)
    market = market_match.group(1) if market_match else ''
    # Extract market return percentage
    return_match = re.search(r'(-?\d+\.?\d*)%', description)
    market_return = return_match.group(1) + '%' if return_match else ''
    return market, market_return

# Function to extract percentage value safely
def extract_percentage(text):
    if isinstance(text, str):  # Ensure text is a string before applying regex
        match = re.search(r"-?\d+\.?\d*%", text)  # Find first occurrence of number with %
        return match.group(0) if match else "N/A"  # Return the number or "N/A" if not found
    return "N/A"  # If text is NaN, return "N/A"

# Function to extract percentage values safely
def extract_percentage2(text):
    if isinstance(text, str):  # Ensure text is a string before applying regex
        match = re.search(r"-?\d+\.?\d*%", text)  # Find first occurrence of number with %
        return match.group(0) if match else "N/A"  # Return the number or "N/A" if not found
    return "N/A"  # If text is NaN, return "N/A"

# Function to extract ratios and determine preferred multiple
def extract_ratios(text):
    if isinstance(text, str):
        patterns = {
            "P/S": r"Price-To-Sales.*?\((\d+\.?\d*)x\).*?(\d+\.?\d*)x",
            "P/B": r"Price-To-Book.*?\((\d+\.?\d*)x\).*?(\d+\.?\d*)x",
            "P/E": r"Price-To-Earnings.*?\((\d+\.?\d*)x\).*?(\d+\.?\d*)x"
        }
        for multiple, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1), match.group(
                    2), multiple  # Extracted company value, industry avg, and multiple type
    return "N/A", "N/A", "N/A"  # Default if no match

# Function to extract peer average and determine metric type
def extract_peer_avg(text):
    if isinstance(text, str):
        patterns = {
            "P/S": r"Price-To-Sales.*?peer average \((\d+\.?\d*)x\)",
            "P/B": r"Price-To-Book.*?peer average \((\d+\.?\d*)x\)",
            "P/E": r"Price-To-Earnings.*?peer average \((\d+\.?\d*)x\)"
        }
        for multiple, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1), multiple  # Extracted peer average value and metric type
    return "N/A", "N/A"  # Default if no match

# Function to extract fair ratio and determine metric type
def extract_fair_ratio(text):
    if isinstance(text, str):
        patterns = {
            "Fair P/S": r"Fair Price-To-Sales Ratio \((\d+\.?\d*)x\)",
            "Fair P/E": r"Fair Price-To-Earnings Ratio \((\d+\.?\d*)x\)"
        }
        for multiple, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1), multiple  # Extracted fair value and metric type
    return "N/A", "N/A"  # Default if no match

# Function to extract first and second numbers in parentheses
def extract_prices(text):
    if isinstance(text, str):
        matches = re.findall(r"\(([^)]+)\)", text)  # Find all values in parentheses
        if len(matches) >= 2:
            return matches[0], matches[1]  # First value = Current Price, Second value = DCF Fair Value
    return "N/A", "N/A"

# Function to extract values
def extract_pb_data(text):
    if isinstance(text, str):
        matches = re.findall(r"\(([\d\.]+x)\)", text)  # Extract numbers in parentheses
        industry_match = re.search(r"compared to the (.*?) industry average", text)  # Extract industry
        p_b_ratio = matches[0] if len(matches) > 0 else "N/A"
        industry_avg_pb = matches[1] if len(matches) > 1 else "N/A"
        industry_name = industry_match.group(1) if industry_match else "N/A"
        return industry_name, p_b_ratio, industry_avg_pb
    return "N/A", "N/A", "N/A"

# Function to extract PEG Ratio
def extract_peg_ratio(text):
    if isinstance(text, str):
        match = re.search(r"\(([\d\.]+x)\)", text)  # Extract number inside parentheses
        return match.group(1) if match else "N/A"
    return "N/A"

# Function to extract the two P/E values
def extract_pe_ratios(text):
    if isinstance(text, str):
        matches = re.findall(r"\(([\d\.]+x)\)", text)  # Extract all numbers in parentheses
        if len(matches) == 2:
            return pd.Series(matches)
    return pd.Series(["N/A", "N/A"])

# Function to extract Industry Name and Industry P/E Ratio
def extract_industry_and_pe(text):
    if isinstance(text, str):
        industry_match = re.search(r"compared to the (.*?) industry average", text)
        pe_matches = re.findall(r"\(([\d\.]+x)\)", text)  # Extract all numbers in parentheses
        industry = industry_match.group(1) if industry_match else "N/A"
        avg_pe = pe_matches[-1] if len(pe_matches) >= 2 else "N/A"  # Get the second extracted number
        return pd.Series([industry, avg_pe])
    return pd.Series(["N/A", "N/A"])



