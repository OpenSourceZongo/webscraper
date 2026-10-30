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

def scrape_page(url, output_file):
    """Scrape a single page and save content"""
    if url in visited_urls:
        return
    
    visited_urls.add(url)
    
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save page content
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n{'='*80}\n")
            f.write(f"URL: {url}\n")
            f.write(f"{'='*80}\n\n")
            f.write(soup.get_text())
        
        # Find all links on the page
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            
            # BUG IS HERE: This condition will cause infinite loops
            # It only checks if the domain matches, but doesn't prevent
            # revisiting the same URLs or following pagination links endlessly
            if get_domain(next_url) == base_domain:
                scrape_page(next_url, output_file)
    
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
