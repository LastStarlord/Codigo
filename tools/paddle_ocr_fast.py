"""
OCR rápido con PaddleOCR (más rápido que EasyOCR)
"""
import os
os.chdir(r"c:\Users\NorbertAlvarez\OneDrive - DM Solar\Escritorio\Codigo")

try:
    from pdf2image import convert_from_path
    from paddleocr import PaddleOCR
    
    pdf_file = "Modelo de degradación.pdf"
    txt_file = "Modelo de degradación_OCR.txt"
    
    print(f"Inicializando PaddleOCR...")
    ocr = PaddleOCR(use_angle_cls=True, lang='es')
    
    print(f"Convirtiendo PDF a imágenes...")
    images = convert_from_path(pdf_file, first_page=1, last_page=5)  # Primeras 5 páginas
    
    print(f"Total de páginas a procesar: {len(images)}")
    
    all_text = f"=== DOCUMENTO OCR: {pdf_file} ===\n"
    all_text += f"Páginas procesadas: {len(images)}\n\n"
    
    for i, image in enumerate(images, 1):
        print(f"Extrayendo página {i}...", flush=True)
        results = ocr.ocr(image, cls=True)
        
        page_text = ""
        for line in results:
            if line:
                for word_info in line:
                    page_text += word_info[1][0] + " "
            page_text += "\n"
        
        all_text += f"\n--- PÁGINA {i} ---\n"
        all_text += page_text
    
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"\n✓ Listo: {txt_file}")
    
except ImportError:
    print("Instalando PaddleOCR...")
    os.system("pip install paddleocr --quiet")
except Exception as e:
    print(f"Error: {e}")
