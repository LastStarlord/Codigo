"""
Conversor PDF a TXT usando PyPDF2 (alternativa ligera)
"""
import os
import sys

os.chdir(r"c:\Users\NorbertAlvarez\OneDrive - DM Solar\Escritorio\Codigo")

try:
    from PyPDF2 import PdfReader
    
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
            text = ""
            
            with open(pdf_file, 'rb') as f:
                reader = PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text += f"\n--- PÁGINA {i+1} ---\n"
                    text += page.extract_text()
            
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✓ {pdf_file} → {txt_file}")
        
        except Exception as e:
            print(f"✗ Error: {e}")

except ImportError:
    print("PyPDF2 no instalado. Instalando...")
    os.system("pip install PyPDF2 --quiet")
    print("Por favor, ejecuta nuevamente.")
