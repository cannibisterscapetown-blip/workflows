#!/usr/bin/env python3
import json
from fpdf import FPDF

# Cannibisters Branding Colors
# Dark Green: 46, 139, 87 (SeaGreen)
# Light Green: 144, 238, 144 (LightGreen) - for highlights
# Dark Gray: 50, 50, 50
# White: 255, 255, 255

class CanniReport(FPDF):
    def header(self):
        # Background for header
        self.set_fill_color(46, 139, 87) # Deep Sea Green
        self.rect(0, 0, 210, 45, 'F')
        
        # Logo
        logo_path = "/Users/norton/.gemini/antigravity/brain/dd1ee179-e4e8-4cbb-a367-64d29c53e525/uploaded_image_1767101409851.png"
        try:
            self.image(logo_path, x=85, y=5, w=40)
        except:
            print("⚠️ Could not load logo image")
            
        # Title
        self.set_y(28)
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'Advent Calendar Performance Report - Dec 2025', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pretty_pdf():
    # Load data
    with open('sales_comparison_results.json', 'r') as f:
        data = json.load(f)
    
    pdf = CanniReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Summary Section
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, "Sales Performance Comparison", ln=True)
    pdf.ln(3)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, "This report compares sales performance on 'Advent Featured Days' (Dec 2025) against 'Usual Daily Sales' (calculated from Nov 2025 baseline). Highlighted rows indicate high-performing campaign peaks.")
    pdf.ln(5)
    
    # Table Header
    pdf.set_fill_color(46, 139, 87)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 9)
    
    col_widths = [22, 90, 25, 25, 25] # Date, Product, Advent, Usual, Lift
    headers = ["Date", "Featured Product", "Advent", "Usual Avg", "Lift %"]
    
    for i in range(len(headers)):
        pdf.cell(col_widths[i], 8, headers[i], 1, 0, 'C', 1)
    pdf.ln()
    
    # Table Body
    pdf.set_text_color(50, 50, 50)
    
    row_height = 6.0
    fill = False
    for row in data:
        # Zebra striping
        if fill:
            pdf.set_fill_color(240, 250, 240)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        # Highlight top performers (Lift > 50%)
        if row['lift_percent'] >= 50:
             pdf.set_font("helvetica", "B", 8)
             pdf.set_text_color(0, 100, 0)
        else:
             pdf.set_font("helvetica", "", 8)
             pdf.set_text_color(50, 50, 50)
        
        lift_str = f"+{row['lift_percent']}%" if row['lift_percent'] > 0 else f"{row['lift_percent']}%"
        if row['usual_avg'] == 0 and row['advent_sold'] > 0: lift_str = "NEW"
        
        pdf.cell(col_widths[0], row_height, row['date'], 1, 0, 'C', 1)
        pdf.cell(col_widths[1], row_height, row['product'][:50], 1, 0, 'L', 1)
        pdf.cell(col_widths[2], row_height, str(row['advent_sold']), 1, 0, 'C', 1)
        pdf.cell(col_widths[3], row_height, str(row['usual_avg']), 1, 0, 'C', 1)
        pdf.cell(col_widths[4], row_height, lift_str, 1, 0, 'C', 1)
        pdf.ln()
        fill = not fill

    pdf.ln(5)
    
    # Key Insights Section
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 8, "Significant Performance Lifts", ln=True)
    
    pdf.set_font("helvetica", "", 9.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5.5, "- Brainstorm Joint: Massive +446.5% lift over daily average.\n"
                    "- 510 Battery Bundle: Incredible +900% growth on featured day.\n"
                    "- Greendoor Super Cheese: Solid +122.2% increase during Advent.\n"
                    "- Queen of the South: Maintained high volume with a +25.4% lift.")
    pdf.ln(5)

    pdf.output("advent_calendar_comparative_report_2025.pdf")
    print("✅ Comparative PDF Report generated: advent_calendar_comparative_report_2025.pdf")

if __name__ == '__main__':
    generate_pretty_pdf()
