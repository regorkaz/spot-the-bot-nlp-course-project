import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

# Constants
LIBGEN_SEARCH_URL = "https://libgen.is/fiction/?q=&criteria=&language=Lithuanian&format="
DOWNLOAD_DIR = "lithuanian_fiction_books"

# Create download directory if not exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_book_links():
    """Scrape the LibGen search results for book links."""
    response = requests.get(LIBGEN_SEARCH_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    book_links = []
    # Find all links to book details
    for link in soup.select('a[href*="fiction"][href*="view"]'):
        book_links.append(link['href'])
        
    return book_links

def get_download_link(book_link):
    """Extract the direct download link from a book's page."""
    response = requests.get(book_link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the first download link available
    download_link = None
    for a in soup.select('a[href*="download.php?md5="]'):
        download_link = a['href']
        break
        
    return download_link

def download_book(download_link):
    """Download the book file from the provided download link."""
    parsed_link = urllib.parse.urlparse(download_link)
    file_name = os.path.basename(parsed_link.path)
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    
    print(f"Downloading {file_name}...")
    response = requests.get(download_link, stream=True)
    response.raise_for_status()
    
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded: {file_path}")
    

def main():
    print("Fetching Lithuanian fiction books from LibGen...")
    book_links = get_book_links()
    print(f"Found {len(book_links)} books. Starting downloads...")
    
    for book_link in book_links:
        full_link = urllib.parse.urljoin(LIBGEN_SEARCH_URL, book_link)
        download_link = get_download_link(full_link)
        if download_link:
            download_book(download_link)
        else:
            print(f"No download link found for {full_link}")

if __name__ == "__main__":
    main()

# Notes:
# - This script only downloads the first available link for each book.
# - Error handling is minimal; this is a basic version!
# - Use responsibly and ensure legality of downloads in your region.
