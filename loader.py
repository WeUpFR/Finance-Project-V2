import pandas as pd
from typing import List, Dict, Any

def load_trial_balance(file_path: str) -> pd.DataFrame:
    """
    Loads trial balance data from an Excel or CSV file.
    It expects separate Debit and Credit columns and reconciles them
    into a single 'balance' column.

    Args:
        file_path (str): The path to the input file.

    Returns:
        pd.DataFrame: A DataFrame containing the trial balance data with
                      standardized column names.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Standardize column names
        df.columns = [col.lower().replace(' ', '_').replace('.', '') for col in df.columns]
        
        # --- Adaptation for Debit/Credit columns ---
        # Fill NaN values with 0 to allow for subtraction
        debits = df['debit_amt'].fillna(0)
        credits = df['credit_amt'].fillna(0)
        
        # Calculate a single balance column.
        df['balance'] = debits - credits

        # Rename account_id to account_number for consistency
        if 'account_id' in df.columns:
            df.rename(columns={'account_id': 'account_number'}, inplace=True)
            
        # Convert account number to string for consistent matching
        if 'account_number' in df.columns:
            df['account_number'] = df['account_number'].astype(str)

        print(f"Successfully loaded and processed {file_path}")
        return df

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return pd.DataFrame()
