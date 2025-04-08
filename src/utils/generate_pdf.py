# Standard library imports
import os
import sys
import calendar
import logging
from datetime import datetime
from pathlib import Path

# Third-party imports
from fpdf import FPDF

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Local imports
from src.repositories import finance_repository as fr

# Configure logger
logger = logging.getLogger(__name__)

# Font path using pathlib for better cross-platform compatibility
FONT_PATH = Path(__file__).parent.parent.parent / "static" / "fonts" / "DejaVuSans.ttf"

class BudgetPDF(FPDF):
    """Extended PDF class with header and footer for budget reports"""
    
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        # Set utf-8 encoding to properly handle Polish characters
        self.core_fonts_encoding = 'utf-8'
        self.WIDTH = 210  # A4 width in mm
        self.title = "Raport Budżetu Domowego"
    
    def sanitize_text(self, text):
        """Sanitize text to ensure it's compatible with PDF encoding"""
        if isinstance(text, str):
            # Replace problematic characters if needed
            return text
        return str(text)
        
    def header(self):
        # Set font for header
        self.set_font('DejaVu', 'B', 12)
        
        # Add title centered on the page
        self.cell(self.WIDTH - 20, 10, self.title, 0, 0, 'C')
        
        # Draw a line below header
        self.ln(12)
        self.line(10, self.get_y(), self.WIDTH - 10, self.get_y())
        self.ln(10)
        
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        
        # Set font for footer
        self.set_font('DejaVu', size=8)
        
        # Add page number
        self.cell(0, 10, f'Strona {self.page_no()}/{{nb}}', 0, 0, 'C')
        
        # Add generation date
        date_str = datetime.now().strftime('%d-%m-%Y %H:%M')
        self.cell(0, 10, f'Wygenerowano: {date_str}', 0, 0, 'R')
        
    def section_title(self, title):
        """Add a section title"""
        self.set_font('DejaVu', 'B', 14)
        self.ln(5)
        self.cell(0, 10, title, 0, 1)
        self.ln(2)
        
    def table_header(self, headers, widths):
        """Add a table header with specified column widths"""
        self.set_font('DejaVu', 'B', 10)
        self.set_fill_color(230, 230, 230)  # Light gray background
        
        for i, header in enumerate(headers):
            # Use sanitize_text to handle Polish characters
            safe_header = self.sanitize_text(header)
            self.cell(widths[i], 10, safe_header, 1, 0, 'C', 1)
        self.ln()
        
    def table_row(self, data, widths):
        """Add a table row with specified column widths"""
        self.set_font('DejaVu', '', 10)
        
        for i, value in enumerate(data):
            # Handle number formatting if needed
            if isinstance(value, (int, float)):
                text = f"{value:.2f}"
            else:
                text = str(value)
            
            # Use sanitize_text to handle Polish characters
            safe_text = self.sanitize_text(text)
            self.cell(widths[i], 8, safe_text, 1, 0, 'L')
        self.ln()


def generate_pdf(month, year, user_id=1):
    """Generate a PDF report with financial data
    
    Args:
        month (int): Month number (1-12)
        year (int): Year
        user_id (int, optional): User ID
        
    Returns:
        str: Path to the generated PDF file
    """
    logger.info(f"Generating report for month {month}, year {year}, user {user_id}")
    
    # Fetch financial data
    try:
        spending = fr.get_month_spending(month, year, user_id)
        income = fr.get_month_income(month, year, user_id)
        
        # Calculate summary data
        income_summary = sum(i['amount'] for i in income)
        spending_summary = sum(i['amount'] for i in spending)
        balance = income_summary - spending_summary
    except Exception as e:
        logger.error(f"Error fetching financial data: {e}")
        raise
    
    # Get month name for better report title
    month_name = calendar.month_name[month]
    
    # Create PDF document
    pdf = BudgetPDF()
    pdf.alias_nb_pages()
    font_path_str = str(FONT_PATH)
    pdf.add_font('DejaVu', '', font_path_str, uni=True)
    pdf.add_font('DejaVu', 'B', font_path_str, uni=True)
    pdf.add_font('DejaVu', 'I', font_path_str, uni=True)
    
    # Set document title
    pdf.title = f"Raport Budżetu Domowego - {month_name} {year}"
    
    # Add first page
    pdf.add_page()
    
    # Main title
    pdf.set_font('DejaVu', 'B', 16)
    pdf.cell(0, 10, f"Raport Budżetu Domowego", ln=True, align='C')
    pdf.set_font('DejaVu', 'B', 14)
    pdf.cell(0, 10, f"{month_name} {year}", ln=True, align='C')
    pdf.ln(10)
    
    # Executive summary section
    pdf.section_title("1. Podsumowanie")
    pdf.set_font('DejaVu', size=11)
    
    # Create a summary table
    summary_data = [
        ["Przychody:", f"{income_summary:.2f} PLN"],
        ["Wydatki:", f"{spending_summary:.2f} PLN"],
        ["Bilans:", f"{balance:.2f} PLN"]
    ]
    
    for row in summary_data:
        pdf.set_font('DejaVu', 'B', 11)
        pdf.cell(40, 8, row[0], 0, 0)
        
        # Use a different font style (and color for balance) based on value
        if "Bilans" in row[0]:
            if balance >= 0:
                pdf.set_text_color(0, 128, 0)  # Green for positive balance
            else:
                pdf.set_text_color(255, 0, 0)  # Red for negative balance
                
        pdf.set_font('DejaVu', '', 11)
        pdf.cell(60, 8, row[1], 0, 1)
        
        # Reset text color to black
        pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    
    # Income detailed section
    pdf.add_page()
    pdf.section_title("2. Szczegóły przychodów")
    
    # Income details table
    if income:
        pdf.ln(5)
        pdf.set_font('DejaVu', '', 11)
        pdf.cell(0, 8, f"Łączna kwota przychodów: {income_summary:.2f} PLN", ln=1)
        
        # Create income table
        income_headers = ["Data", "Kwota (PLN)", "Opis"]
        income_widths = [40, 40, 110]
        
        pdf.table_header(income_headers, income_widths)
        
        # Sort income by date
        sorted_income = sorted(income, key=lambda x: x['date'])
        
        for entry in sorted_income:
            note = entry.get('note', '')
            if not note:
                note = "-"
                
            pdf.table_row([
                entry['date'],
                entry['amount'],
                note
            ], income_widths)
    else:
        pdf.cell(0, 10, "Brak zarejestrowanych przychodów w wybranym okresie.", ln=1)
    
    # Expenses detailed section
    pdf.add_page()
    pdf.section_title("3. Szczegóły wydatków")
    
    # Expenses details table
    if spending:
        pdf.ln(5)
        pdf.set_font('DejaVu', '', 11)
        pdf.cell(0, 8, f"Łączna kwota wydatków: {spending_summary:.2f} PLN", ln=1)
        
        # Create expenses table
        expense_headers = ["Data", "Kategoria", "Nazwa", "Kwota (PLN)"]
        expense_widths = [30, 50, 70, 40]
        
        pdf.table_header(expense_headers, expense_widths)
        
        # Sort expenses by date
        sorted_spending = sorted(spending, key=lambda x: x['date'])
        
        for entry in sorted_spending:
            pdf.table_row([
                entry['date'],
                entry.get('category', 'Brak kategorii'),
                entry.get('name', ''),
                entry['amount']
            ], expense_widths)
    else:
        pdf.cell(0, 10, "Brak zarejestrowanych wydatków w wybranym okresie.", ln=1)

    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Generate the PDF file
    output_path = output_dir / f"raport_budzetowy_{month}_{year}_user{user_id}.pdf"
    try:
        # Use a try/except block to catch and handle encoding errors
        pdf.output(str(output_path), 'F')  # 'F' means output to file
    except UnicodeEncodeError as e:
        logger.error(f"Encoding error during PDF generation: {e}")
        # If encoding fails, try with a different approach
        pdf_content = pdf.output(dest='S').encode('latin-1', 'ignore')  # 'S' returns string
        with open(output_path, 'wb') as f:
            f.write(pdf_content)
    
    logger.info(f"Report generated: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    # Configure logger for test usage
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test the PDF generation
    report_path = generate_pdf(4, 2025, 1)
    print(f"Report generated: {report_path}")
