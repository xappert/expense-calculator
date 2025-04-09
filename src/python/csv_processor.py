import pandas as pd
import logging
import requests
from typing import List, Dict

MCP_ENDPOINT = "http://localhost:8000/categorize"

def categorize_transactions(transactions: List[Dict]) -> List[Dict]:
    """Send transactions to MCP categorization service"""
    try:
        response = requests.post(
            MCP_ENDPOINT,
            json={"transactions": transactions},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Categorization failed: {str(e)}")
        return local_categorize(transactions)  # Fallback

def local_categorize(transactions: List[Dict]) -> List[Dict]:
    """Basic local categorization fallback"""
    categories = {
        "groceries": ["supermarket", "grocery", "food basics"],
        "dining": ["restaurant", "cafe", "coffee", "delivery"],
        "transportation": ["gas station", "metro", "bus", "repair"]
    }
    
    for t in transactions:
        t["category"] = "other"
        desc = t["description"].lower()
        for cat, keywords in categories.items():
            if any(kw in desc for kw in keywords):
                t["category"] = cat
                break
    return transactions

def process_csv(input_path: str, output_path: str) -> None:
    """Process CSV file with MCP categorization"""
    df = pd.read_csv(input_path)
    
    # Convert to list of dicts for MCP
    transactions = df.to_dict("records")
    
    # Get categorized transactions
    categorized = categorize_transactions(transactions)
    
    # Save results
    pd.DataFrame(categorized).to_csv(output_path, index=False)
