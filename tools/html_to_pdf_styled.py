#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir HTML a PDF preservando estilos
"""

import asyncio
from pathlib import Path
from pyppeteer import launch

async def convert_html_to_pdf():
    """Convertir HTML a PDF usando Chromium headless"""
    html_file = Path('manual_bess_model.html').resolve()
    pdf_file = Path('manual_bess_model.pdf')
    
    print(f"Convirtiendo {html_file} a PDF...")
    
    # Lanzar navegador
    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    
    # Crear nueva página
    page = await browser.newPage()
    
    # Cargar el HTML local
    await page.goto(f'file://{html_file}', {'waitUntil': 'networkidle0'})
    
    # Generar PDF con opciones
    await page.pdf({
        'path': str(pdf_file),
        'format': 'A4',
        'printBackground': True,
        'margin': {
            'top': '20px',
            'right': '20px',
            'bottom': '20px',
            'left': '20px'
        }
    })
    
    # Cerrar navegador
    await browser.close()
    
    print(f"✓ PDF creado exitosamente: {pdf_file}")
    return pdf_file

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(convert_html_to_pdf())
