from pypdf import PdfReader
import sys

pdf_file = "Modelo de degradación.pdf"
txt_file = "Modelo de degradación.txt"

try:
    print(f"Abriendo {pdf_file}...", flush=True)
    with open(pdf_file, 'rb') as f:
        reader = PdfReader(f)
        total_pages = len(reader.pages)
        print(f"Total de páginas: {total_pages}", flush=True)
        
        text = f"DOCUMENTO: {pdf_file}\nTOTAL PÁGINAS: {total_pages}\n" + "="*70 + "\n"
        
        for i in range(min(total_pages, 5)):  # Primeras 5 páginas
            print(f"Extrayendo página {i+1}/{min(total_pages, 5)}...", flush=True)
            page = reader.pages[i]
            text += f"\n--- PÁGINA {i+1} ---\n"
            try:
                extracted = page.extract_text()
                text += extracted if extracted else "[Sin texto]"
            except:
                text += "[Error al extraer]"
    
    print(f"Guardando en {txt_file}...", flush=True)
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✓ Listo: {txt_file}", flush=True)

except Exception as e:
    print(f"✗ Error: {e}", flush=True)
    sys.exit(1)
