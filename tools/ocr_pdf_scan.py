"""
Conversor PDF escaneado a TXT usando EasyOCR (sin Tesseract)
"""
import os
os.chdir(r"c:\Users\NorbertAlvarez\OneDrive - DM Solar\Escritorio\Codigo")

try:
    from pdf2image import convert_from_path
    import easyocr
    
    pdf_file = "Modelo de degradación.pdf"
    txt_file = "Modelo de degradación_OCR.txt"
    
    print(f"Instalando modelo de OCR (primera vez lenta)...")
    reader = easyocr.Reader(['es', 'en'], gpu=False)
    
    print(f"Convirtiendo PDF a imágenes...")
    images = convert_from_path(pdf_file)
    
    print(f"Total de páginas: {len(images)}")
    
    all_text = f"=== DOCUMENTO OCR: {pdf_file} ===\n"
    all_text += f"Total páginas: {len(images)}\n\n"
    
    for i, image in enumerate(images, 1):
        print(f"Extrayendo página {i}/{len(images)}...")
        results = reader.readtext(image, detail=0)
        page_text = "\n".join(results)
        
        all_text += f"\n--- PÁGINA {i} ---\n"
        all_text += page_text
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"\n✓ Convertido: {pdf_file} → {txt_file}")
    
except ImportError as e:
    print(f"Falta instalar: {e}")
    print("\nIntentando instalar easyocr...")
    os.system("pip install easyocr --quiet")
except Exception as e:
    print(f"Error: {e}")
