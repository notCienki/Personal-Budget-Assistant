import os
import sys
from fpdf import FPDF
from datetime import datetime

# Ścieżka do pliku czcionki
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf'))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.store import finance_repository as fr

def generate_pdf(month, year):
    spending = fr.get_month_spending(month, year)
    income = fr.get_month_income(month, year)

    income_summary = 0
    spending_summary = 0

    for i in income:
        income_summary += i['amount']

    for i in spending:
        spending_summary += i['amount']

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.add_font('DejaVu', 'B', font_path, uni=True)
    pdf.set_font('DejaVu', size=12)

    pdf.set_font("DejaVu", style='B', size=16)
    pdf.cell(200, 10, txt=f"Raport Wydatków i Wpływów - {month} / {year}", ln=True, align='C')
    pdf.ln(10)

    # Podsumowanie
    pdf.set_font("DejaVu", style='B', size=14)
    pdf.cell(200, 10, txt="1. Podsumowanie", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, txt=f"Całkowite przychody: {income_summary} PLN\nCałkowite wydatki: {spending_summary} PLN\nSaldo końcowe: {income_summary - spending_summary} PLN")
    pdf.ln(5)

    # Przychody
    pdf.set_font("DejaVu", style='B', size=14)
    pdf.cell(200, 10, txt="2. Przychody", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(40, 10, txt="Data", border=1)
    pdf.cell(40, 10, txt="Kwota (PLN)", border=1)
    pdf.cell(60, 10, txt="Opis", border=1)
    pdf.ln()

    for entry in income:
        if not entry['note']:
            entry['note'] = ""
        pdf.cell(40, 10, txt=entry['date'], border=1)
        pdf.cell(40, 10, txt=str(entry['amount']), border=1)
        pdf.cell(60, 10, txt=entry['note'], border=1)
        pdf.ln()
    pdf.ln(5)

    # Wydatki
    pdf.set_font("DejaVu", style='B', size=14)
    pdf.cell(200, 10, txt="3. Wydatki", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(40, 10, txt="Data", border=1)
    pdf.cell(50, 10, txt="Kategoria", border=1)
    pdf.cell(40, 10, txt="Kwota (PLN)", border=1)
    pdf.cell(60, 10, txt="Opis", border=1)
    pdf.ln()

    for entry in spending:
        if not entry['note']:
            entry['note'] = ""
        pdf.cell(40, 10, txt=entry['date'], border=1)
        pdf.cell(50, 10, txt=entry['category'].capitalize(), border=1)
        pdf.cell(40, 10, txt=str(entry['amount']), border=1)
        pdf.cell(60, 10, txt=entry['note'], border=1)
        pdf.ln()
    pdf.ln(5)

    # Data wygenerowania
    pdf.set_font("DejaVu", size=10)
    pdf.cell(200, 10, txt=f"Data wygenerowania raportu: {datetime.now().strftime('%d-%m-%Y')}", ln=True, align='C')

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)  # Upewnij się, że folder istnieje

    pdf.output(os.path.join(output_dir, f"raport_{month}_{year}.pdf"))
