"""
Conversor PDF a TXT usando pypdf
"""
import os

os.chdir(r"c:\Users\NorbertAlvarez\OneDrive - DM Solar\Escritorio\Codigo")

from pypdf import PdfReader

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
            print(f"  Leyendo {pdf_file} ({len(reader.pages)} páginas)...")
            for i, page in enumerate(reader.pages):
                text += f"\n--- PÁGINA {i+1} ---\n"
                extracted = page.extract_text()
                if extracted:
                    text += extracted
                else:
                    text += "[Página sin texto]"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✓ {pdf_file} → {txt_file}")
    
    except Exception as e:
        print(f"✗ Error en {pdf_file}: {str(e)[:100]}")
