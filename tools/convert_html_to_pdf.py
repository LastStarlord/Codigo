#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir HTML a PDF
"""

import sys
import os
from pathlib import Path

def convert_with_pyppeteer():
    """Intentar convertir con pyppeteer (basado en Chromium)"""
    try:
        import asyncio
        from pyppeteer import launch
        
        async def pdf_convert():
            html_path = Path('manual_bess_model.html').resolve()
            pdf_path = Path('manual_bess_model.pdf')
            
            browser = await launch()
            page = await browser.newPage()
            await page.goto(f'file://{html_path}')
            await page.pdf({'path': str(pdf_path)})
            await browser.close()
            return str(pdf_path)
        
        pdf_file = asyncio.get_event_loop().run_until_complete(pdf_convert())
        print(f"PDF creado exitosamente: {pdf_file}")
        return True
    except Exception as e:
        print(f"Error con pyppeteer: {e}")
        return False

def convert_with_fpdf():
    """Convertir HTML a PDF usando FPDF (texto simple)"""
    try:
        from fpdf import FPDF
        from html.parser import HTMLParser
        
        class HTMLToText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False
                
            def handle_starttag(self, tag, attrs):
                if tag in ['script', 'style']:
                    self.skip = True
                    
            def handle_endtag(self, tag):
                if tag in ['script', 'style']:
                    self.skip = False
                elif tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
                    self.text.append('\n')
                    
            def handle_data(self, data):
                if not self.skip:
                    text = data.strip()
                    if text:
                        self.text.append(text + ' ')
        
        # Leer HTML
        with open('manual_bess_model.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extraer texto
        parser = HTMLToText()
        parser.feed(html_content)
        text = ''.join(parser.text)
        
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 10)
        
        # Escribir texto en PDF (FPDF necesita texto válido)
        # Usar encoding latin-1 para evitar problemas
        text_latin1 = text.encode('latin-1', errors='ignore').decode('latin-1')
        pdf.multi_cell(0, 5, text_latin1)
        
        pdf.output('manual_bess_model.pdf')
        print("PDF creado exitosamente: manual_bess_model.pdf")
        return True
    except Exception as e:
        print(f"Error con FPDF: {e}")
        return False

def convert_with_pypdf():
    """Usar reportlab para un mejor resultado"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        from html.parser import HTMLParser
        from html import unescape
        
        class HTMLExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.paragraphs = []
                self.current_text = []
                
            def handle_starttag(self, tag, attrs):
                if tag in ['h1', 'h2', 'h3']:
                    self._flush()
                    
            def handle_endtag(self, tag):
                if tag in ['p', 'div', 'h1', 'h2', 'h3']:
                    self._flush()
                    
            def handle_data(self, data):
                text = data.strip()
                if text:
                    self.current_text.append(text)
                    
            def _flush(self):
                if self.current_text:
                    self.paragraphs.append(' '.join(self.current_text))
                    self.current_text = []
            
            def get_paragraphs(self):
                self._flush()
                return self.paragraphs
        
        # Leer HTML
        with open('manual_bess_model.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extraer párrafos
        extractor = HTMLExtractor()
        extractor.feed(html_content)
        paragraphs = extractor.get_paragraphs()
        
        # Crear documento PDF
        doc = SimpleDocTemplate("manual_bess_model.pdf", pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        for para_text in paragraphs:
            if para_text:
                # Limpiar caracteres especiales
                para_text = unescape(para_text)
                para_text = para_text.encode('latin-1', errors='ignore').decode('latin-1')
                story.append(Paragraph(para_text, styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
        
        doc.build(story)
        print("PDF creado exitosamente: manual_bess_model.pdf")
        return True
    except Exception as e:
        print(f"Error con ReportLab: {e}")
        return False

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Intentar métodos en orden
    print("Intentando convertir HTML a PDF...")
    
    if convert_with_fpdf():
        sys.exit(0)
    
    print("\nIntentando con ReportLab...")
    if convert_with_pypdf():
        sys.exit(0)
    
    print("\nIntentando con Pyppeteer...")
    if convert_with_pyppeteer():
        sys.exit(0)
    
    print("\nNo se pudo crear el PDF con los métodos disponibles.")
    sys.exit(1)
