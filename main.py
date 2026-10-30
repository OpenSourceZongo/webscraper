import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

visited_urls = set()
base_domain = ""

def get_domain(url):
    """Extract domain from URL"""
    parsed = urlparse(url)
    return parsed.netloc

def scrape_page(url, output_file, max_depth=5, current_depth=0):
    """Scrape a single page and save content"""
    
    # FIX 1: Add depth limit
    if current_depth >= max_depth:
        return
    
    # FIX 2: Check visited URLs BEFORE making the recursive call
    if url in visited_urls:
        return
    
    visited_urls.add(url)
    
    try:
        print(f"Scraping: {url} (depth: {current_depth})")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n{'='*80}\n")
            f.write(f"URL: {url}\n")
            f.write(f"{'='*80}\n\n")
            f.write(soup.get_text())
        
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            
            # FIX 3: Add filtering for common problematic URL patterns
            if (get_domain(next_url) == base_domain and 
                '#' not in next_url and  # Skip anchor links
                next_url not in visited_urls):
                scrape_page(next_url, output_file, max_depth, current_depth + 1)
    
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <starting_url> [output_file]")
        print("Example: python scraper.py https://example.com scraped_content.txt")
        sys.exit(1)
    
    start_url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "scraped_content.txt"
    
    global base_domain
    base_domain = get_domain(start_url)
    
    # Clear output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Web Scrape of {start_url}\n")
    
    scrape_page(start_url, output_file)
    print(f"\nScraping complete! Content saved to {output_file}")

if __name__ == "__main__":
    main()
