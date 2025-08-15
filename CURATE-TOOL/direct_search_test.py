#!/usr/bin/env python3
"""
Test directo para verificar que las herramientas funcionan y encontrar URLs reales
"""
import sys
from src.tools import search_web

def test_direct_search(topic):
    """Test directo de búsqueda web"""
    print(f"🔍 Probando búsqueda directa para: {topic}")
    print("=" * 50)
    
    queries = [
        f"{topic} tutorial",
        f"{topic} guide", 
        f"{topic} article",
        f"{topic} beginner",
        f"learn {topic}"
    ]
    
    all_results = []
    
    for query in queries:
        print(f"\n🔍 Búsqueda: {query}")
        result = search_web(query)
        print(result)
        all_results.append(result)
        print("-" * 40)
    
    print(f"\n✅ Búsquedas completadas. Total: {len(all_results)} consultas realizadas")
    
    # Verificar si encontramos URLs reales
    found_real_urls = False
    for result in all_results:
        if "https://" in result and "example.com" not in result:
            found_real_urls = True
            break
    
    if found_real_urls:
        print("✅ URLs REALES encontradas!")
    else:
        print("❌ No se encontraron URLs reales")
    
    return all_results

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI marketing"
    test_direct_search(topic)