"""
Conversor de PDF a TXT usando pdfplumber
"""

import os

try:
    import pdfplumber
    
    pdf_files = [
        "Modelo de degradación.pdf",
        "Virtual_Europe_2020_Paper_PBMs.pdf"
    ]
    
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            print(f"⚠ No encontrado: {pdf_file}")
            continue
        
        try:
            txt_file = pdf_file.replace('.pdf', '.txt')
            
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for i, page in enumerate(pdf.pages):
                    text += f"\n--- PÁGINA {i+1} ---\n"
                    text += page.extract_text() or "[Página sin texto]"
            
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✓ Convertido: {pdf_file} → {txt_file}")
        
        except Exception as e:
            print(f"✗ Error en {pdf_file}: {e}")

except ImportError:
    print("pdfplumber no está instalado.")
    print("\nInstala con:")
    print("  pip install pdfplumber")
