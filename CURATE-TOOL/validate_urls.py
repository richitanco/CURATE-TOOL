#!/usr/bin/env python3
"""
Script para verificar URLs en archivos de curación de contenido
"""
import re
import requests
from urllib.parse import urlparse
import time

def is_valid_url(url):
    """Check if URL has valid format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def check_url_works(url, timeout=10):
    """Check if URL is accessible"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except:
        return False

def extract_urls_from_file(filename):
    """Extract URLs from markdown file"""
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find URLs in multiple formats
        patterns = [
            r'\*\*URL:\*\*\s+(https?://[^\s\n]+)',  # **URL:** format
            r'https?://[^\s\n\)>\]]+(?:[^\s\n\)>\].,;:]|[.,;:]\S)',  # Any http URL
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if match not in urls:
                    urls.append(match.strip())
            
        return urls
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def validate_urls_in_file(filename):
    """Validate all URLs in a file and report results"""
    print(f"\n🔍 Analizando archivo: {filename}")
    print("=" * 50)
    
    urls = extract_urls_from_file(filename)
    
    if not urls:
        print("❌ No se encontraron URLs en el archivo")
        return
    
    print(f"📋 URLs encontradas: {len(urls)}")
    print()
    
    valid_urls = []
    invalid_urls = []
    fake_urls = []
    
    for i, url in enumerate(urls, 1):
        print(f"🔗 {i}. Verificando: {url}")
        
        # Check if it's obviously fake
        fake_indicators = [
            'example.com', 'example-url', 'http://example',
            'placeholder', 'fake-url', 'sample-url'
        ]
        
        if any(indicator in url.lower() for indicator in fake_indicators):
            print(f"   ❌ URL INVENTADA/FALSA")
            fake_urls.append(url)
            continue
            
        # Check format
        if not is_valid_url(url):
            print(f"   ❌ FORMATO INVÁLIDO")
            invalid_urls.append(url)
            continue
            
        # Check if accessible
        print(f"   🌐 Verificando accesibilidad...")
        if check_url_works(url):
            print(f"   ✅ URL FUNCIONA")
            valid_urls.append(url)
        else:
            print(f"   ❌ URL NO ACCESIBLE")
            invalid_urls.append(url)
            
        # Small delay to be respectful
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*50)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("="*50)
    print(f"✅ URLs válidas y funcionando: {len(valid_urls)}")
    print(f"❌ URLs no accesibles: {len(invalid_urls)}")
    print(f"🚫 URLs inventadas/falsas: {len(fake_urls)}")
    print(f"📈 Porcentaje de éxito: {len(valid_urls)/len(urls)*100:.1f}%")
    
    if fake_urls:
        print(f"\n🚫 URLs INVENTADAS DETECTADAS:")
        for url in fake_urls:
            print(f"   - {url}")
    
    if invalid_urls:
        print(f"\n❌ URLs NO ACCESIBLES:")
        for url in invalid_urls:
            print(f"   - {url}")
    
    if valid_urls:
        print(f"\n✅ URLs VÁLIDAS:")
        for url in valid_urls:
            print(f"   - {url}")

def main():
    import sys
    import glob
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        validate_urls_in_file(filename)
    else:
        # Find the most recent output file
        output_files = glob.glob("output/course_*.markdown")
        if output_files:
            latest_file = max(output_files, key=lambda f: f.split('_')[-1])
            print(f"📁 Usando archivo más reciente: {latest_file}")
            validate_urls_in_file(latest_file)
        else:
            print("❌ No se encontraron archivos de salida en output/")
            print("Uso: python validate_urls.py [archivo.markdown]")

if __name__ == "__main__":
    main()