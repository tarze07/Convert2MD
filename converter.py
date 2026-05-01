import os
from playwright.sync_api import sync_playwright
from readability import Document
from markdownify import markdownify as md

def convert_url_to_markdown(url: str, output_path: str, progress_callback=None):
    """
    Pobiera stronę, wyciąga główną treść i zapisuje jako plik Markdown.
    Używa Playwright do renderowania JavaScript.
    """
    try:
        if progress_callback:
            progress_callback("Rozpoczynanie przeglądarki...")
            
        with sync_playwright() as p:
            # Używamy zainstalowanego w systemie Google Chrome
            browser = p.chromium.launch(channel="chrome", headless=True)
            page = browser.new_page()
            
            if progress_callback:
                progress_callback(f"Otwieranie strony: {url} (to może chwilę potrwać)...")
                
            # Czekamy na załadowanie sieci, co jest dobre dla stron SPA
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            if progress_callback:
                progress_callback("Pobrano stronę. Wyciąganie głównej treści...")
                
            html_content = page.content()
            browser.close()
            
        # Wyciąganie głównej zawartości
        doc = Document(html_content)
        article_html = doc.summary()
        title = doc.title()
        
        if progress_callback:
            progress_callback("Konwersja z HTML na Markdown...")
            
        # Konwersja na Markdown, ignorujemy niepotrzebne tagi
        markdown_text = md(article_html, heading_style="ATX", strip=['script', 'style', 'img'])
        
        # Opcjonalne: czyszczenie pustych linii
        markdown_text = "\n".join([line for line in markdown_text.splitlines() if line.strip() != ""])
        
        final_markdown = f"# {title}\n\n{markdown_text}"
        
        if progress_callback:
            progress_callback(f"Zapisywanie do pliku: {output_path}")
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_markdown)
            
        if progress_callback:
            progress_callback("Zakończono sukcesem!")
            
        return True, "Zakończono sukcesem!"
        
    except Exception as e:
        error_msg = f"Wystąpił błąd: {str(e)}"
        if progress_callback:
            progress_callback(error_msg)
        return False, error_msg
