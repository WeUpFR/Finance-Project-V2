import argparse
import os
import sys

# This allows running the script from the root directory
# e.g., `python src/main.py inputs/your_file.csv`
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.loader import load_trial_balance
from src.mapping import load_mapping_template
from src.statements import build_financial_statements
from src.formatter import format_and_export_excel
from src.pdf_export import export_to_pdf

def cli_run():
    """
    Main function to run the application from the command line.
    """
    parser = argparse.ArgumentParser(
        description="Generate financial statements from a trial balance."
    )
    parser.add_argument(
        'input_file',
        help="Path to the input trial balance Excel/CSV file."
    )
    parser.add_argument(
        '--mapping',
        default='mapping_template.json',
        help="Path to the mapping JSON file."
    )
    parser.add_argument(
        '--output_dir',
        default='outputs',
        help="Directory to save the output reports."
    )
    
    args = parser.parse_args()

    print("Running in Command-Line Interface (CLI) mode.")
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    tb_df = load_trial_balance(args.input_file)
    if tb_df.empty: return
        
    mapping = load_mapping_template(args.mapping)
    if not mapping: return
        
    statements = build_financial_statements(tb_df, mapping)
    if not statements: return
        
    base_name = os.path.splitext(os.path.basename(args.input_file))[0]
    excel_output_path = os.path.join(args.output_dir, f"{base_name}_statements.xlsx")
    pdf_output_path = os.path.join(args.output_dir, f"{base_name}_statements.pdf")
    
    format_and_export_excel(statements, excel_output_path)
    export_to_pdf(statements, pdf_output_path)

if __name__ == "__main__":
    # To run the CLI, use:
    # python src/main.py inputs/your_file.csv
    #
    # To run the UI, use:
    # streamlit run src/ui.py
    cli_run()
