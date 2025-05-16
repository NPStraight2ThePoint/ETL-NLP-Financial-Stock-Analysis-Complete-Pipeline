import re
import pandas as pd
import math

# Function to extract the last percentage and adjust if it ends with 'a day'
def extract_last_percentage(text):
    # Ensure the text is a string
    if isinstance(text, str):
        # Find all percentages in the text
        match = re.findall(r'(\d+)%', text)
        if match:
            # Get the last percentage
            last_percentage = float(match[-1])

            # Check if the text ends with 'a day' (indicating daily volatility)
            if text.endswith('a day.'):
                # Convert daily volatility to weekly by multiplying by sqrt(5)
                last_percentage *= math.sqrt(5)

            return last_percentage
    return None  # Return None if no match or text is not a string



