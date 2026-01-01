#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir HTML a PDF con estilos usando Chrome/Edge
"""

import os
import json
import base64
from pathlib import Path

def convert_with_selenium():
    """Convertir usando Selenium con Chrome/Edge"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        
        html_file = Path('manual_bess_model.html').resolve()
        pdf_file = Path('manual_bess_model.pdf')
        
        print(f"Convirtiendo {html_file.name} a PDF...")
        
        # Configurar opciones de Chrome
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Intentar usar Chrome
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Chrome no disponible: {e}")
            print("Intentando con Edge...")
            from selenium.webdriver.edge.options import Options as EdgeOptions
            edge_options = EdgeOptions()
            edge_options.add_argument('--headless')
            edge_options.add_argument('--disable-gpu')
            driver = webdriver.Edge(options=edge_options)
        
        # Cargar HTML
        driver.get(f'file:///{html_file}')
        
        # Esperar un poco para que cargue todo
        driver.implicitly_wait(2)
        
        # Configurar opciones de impresión
        print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        }
        
        # Ejecutar comando de impresión a PDF
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
        
        # Decodificar y guardar PDF
        pdf_data = base64.b64decode(result['data'])
        with open(pdf_file, 'wb') as f:
            f.write(pdf_data)
        
        driver.quit()
        
        print(f"✓ PDF creado exitosamente: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"Error con Selenium: {e}")
        import traceback
        traceback.print_exc()
        return False

def convert_with_pdfkit_check():
    """Verificar si wkhtmltopdf está disponible"""
    try:
        import pdfkit
        
        html_file = 'manual_bess_model.html'
        pdf_file = 'manual_bess_model.pdf'
        
        print(f"Intentando con pdfkit...")
        
        # Configuración para Windows
        config = None
        
        # Intentar encontrar wkhtmltopdf en ubicaciones comunes
        possible_paths = [
            r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',
            r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                config = pdfkit.configuration(wkhtmltopdf=path)
                break
        
        options = {
            'enable-local-file-access': None,
            'print-media-type': None,
            'no-outline': None,
        }
        
        pdfkit.from_file(html_file, pdf_file, options=options, configuration=config)
        print(f"✓ PDF creado exitosamente: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"pdfkit no disponible: {e}")
        return False

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    print("=== Convertidor HTML a PDF con estilos ===\n")
    
    # Intentar con Selenium primero
    if convert_with_selenium():
        exit(0)
    
    print("\n" + "="*50)
    print("Intentando método alternativo...\n")
    
    # Si falla, intentar con pdfkit
    if convert_with_pdfkit_check():
        exit(0)
    
    print("\n❌ No se pudo convertir con los métodos disponibles.")
    print("\nOpciones:")
    print("1. Instalar Chrome/Edge y selenium (ya instalado selenium)")
    print("2. Instalar wkhtmltopdf desde: https://wkhtmltopdf.org/downloads.html")
    exit(1)
