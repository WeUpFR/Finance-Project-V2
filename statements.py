import pandas as pd
from typing import Dict, Any, List

def build_financial_statements(tb_df: pd.DataFrame, mapping: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Builds financial statement DataFrames based on the trial balance and mapping.

    Args:
        tb_df (pd.DataFrame): The trial balance DataFrame.
        mapping (Dict[str, Any]): The mapping dictionary.

    Returns:
        Dict[str, pd.DataFrame]: A dictionary of DataFrames, one for each
                                 financial statement.
    """
    if tb_df.empty or not mapping:
        return {}

    statements = {}
    
    # --- Income Statement ---
    # Revenue accounts typically have credit balances (negative in our balance column).
    # Expense accounts typically have debit balances (positive).
    is_data = []
    
    def get_section_sum(section_mapping: Dict) -> float:
        total = 0
        for accounts in section_mapping.values():
            total += tb_df[tb_df['account_number'].isin(accounts)]['balance'].sum()
        return total

    revenue_total = get_section_sum(mapping['Income Statement']['Revenue'])
    expense_total = get_section_sum(mapping['Income Statement']['Expenses'])
    
    # In our calculation `balance = debit - credit`, so revenue is negative.
    # We flip the sign for presentation.
    revenue_total = -revenue_total
    
    net_income = revenue_total - expense_total
    
    # Build the DataFrame for display
    is_data.append({'Line Item': 'Revenue', 'Amount': None, 'is_header': True})
    for line_item, accounts in mapping['Income Statement']['Revenue'].items():
        is_data.append({'Line Item': f"  {line_item}", 'Amount': -tb_df[tb_df['account_number'].isin(accounts)]['balance'].sum()})
    is_data.append({'Line Item': 'Total Revenue', 'Amount': revenue_total, 'is_total': True})
    
    is_data.append({'Line Item': 'Expenses', 'Amount': None, 'is_header': True})
    for line_item, accounts in mapping['Income Statement']['Expenses'].items():
        is_data.append({'Line Item': f"  {line_item}", 'Amount': tb_df[tb_df['account_number'].isin(accounts)]['balance'].sum()})
    is_data.append({'Line Item': 'Total Expenses', 'Amount': expense_total, 'is_total': True})
    
    is_data.append({'Line Item': 'Net Income', 'Amount': net_income, 'is_total': True, 'is_final_total': True})
    
    statements['Income Statement'] = pd.DataFrame(is_data)

    # --- Balance Sheet ---
    # Update Retained Earnings with Net Income from this period
    opening_re_accounts = mapping['Balance Sheet']['Equity']['Retained Earnings']
    # Net income increases equity (a credit), so we subtract it from the balance column
    tb_df.loc[tb_df['account_number'].isin(opening_re_accounts), 'balance'] -= net_income
    
    bs_data = []
    
    def process_bs_section(section_mapping: Dict, is_liability_or_equity: bool = False):
        section_total = 0
        for sub_section, items in section_mapping.items():
            bs_data.append({'Line Item': sub_section, 'Amount': None, 'is_header': True})
            sub_section_total = 0
            for line_item, accounts in items.items():
                # Flip sign for presentation of liabilities and equity
                sign = -1 if is_liability_or_equity else 1
                item_balance = tb_df[tb_df['account_number'].isin(accounts)]['balance'].sum() * sign
                bs_data.append({'Line Item': f"  {line_item}", 'Amount': item_balance})
                sub_section_total += item_balance
            bs_data.append({'Line Item': f"Total {sub_section}", 'Amount': sub_section_total, 'is_total': True})
            section_total += sub_section_total
        return section_total

    asset_total = process_bs_section(mapping['Balance Sheet']['Assets'])
    bs_data.append({'Line Item': 'Total Assets', 'Amount': asset_total, 'is_total': True, 'is_final_total': True})

    liabilities_total = process_bs_section(mapping['Balance Sheet']['Liabilities'], True)
    equity_total = process_bs_section(mapping['Balance Sheet']['Equity'], True)
    
    total_liabilities_and_equity = liabilities_total + equity_total
    bs_data.append({'Line Item': 'Total Liabilities and Equity', 'Amount': total_liabilities_and_equity, 'is_total': True, 'is_final_total': True})
    
    statements['Balance Sheet'] = pd.DataFrame(bs_data)
    
    # --- Cash Flow Statement (Placeholder) ---
    cf_data = [
        {'Line Item': 'Cash flow statement requires comparative balance sheets.', 'Amount': None},
    ]
    statements['Cash Flow Statement'] = pd.DataFrame(cf_data)
    
    print("Successfully built financial statements.")
    return statements
