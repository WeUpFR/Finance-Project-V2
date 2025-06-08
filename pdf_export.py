from fpdf import FPDF
import pandas as pd
from typing import Dict

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Demerara Life (Trinidad & Tobago)', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def export_to_pdf(statements: Dict[str, pd.DataFrame], output_path: str):
    """
    Exports financial statements to a PDF file.
    """
    pdf = PDF()
    
    for statement_name, df in statements.items():
        if df.empty or df.iloc[0,0].startswith('Cash flow statement requires'):
            continue

        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, statement_name, 0, 1, 'L')
        pdf.cell(0, 5, 'For the period ended March 31, 2025', 0, 1, 'L')
        pdf.ln(5)
        
        effective_width = pdf.w - 2 * pdf.l_margin
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(effective_width * 0.7, 8, 'Description', 1)
        pdf.cell(effective_width * 0.3, 8, "Amount (TT$)", 1, 1, 'R')

        pdf.set_font('Arial', '', 10)
        for _, row in df.iterrows():
            line_item = str(row.get('Line Item', ''))
            amount = row.get('Amount')
            amount_str = f"{amount:,.2f}" if pd.notna(amount) else ''

            if row.get('is_header') or row.get('is_total'):
                pdf.set_font('Arial', 'B', 10)
            
            pdf.cell(effective_width * 0.7, 8, line_item, 'LR')
            pdf.cell(effective_width * 0.3, 8, amount_str, 'LR', 1, 'R')
            
            if row.get('is_total'):
                pdf.line(pdf.x + effective_width * 0.7, pdf.y, pdf.x + effective_width, pdf.y)
            if row.get('is_final_total'):
                pdf.line(pdf.x + effective_width * 0.7, pdf.y - 0.2, pdf.x + effective_width, pdf.y - 0.2)
                pdf.line(pdf.x + effective_width * 0.7, pdf.y, pdf.x + effective_width, pdf.y)

            pdf.set_font('Arial', '', 10)

    try:
        pdf.output(output_path)
        print(f"Successfully exported PDF report to {output_path}")
    except Exception as e:
        print(f"An error occurred while generating the PDF: {e}")
