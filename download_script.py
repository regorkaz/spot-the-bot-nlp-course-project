import requests
from bs4 import BeautifulSoup
import os
import time

# Base URL for Danish language eBooks
base_url = "https://www.gutenberg.org/browse/languages/da"
save_dir = "Danish_texts"

os.makedirs(save_dir, exist_ok=True)

# Fetch the list of eBooks
response = requests.get(base_url)
if response.status_code != 200:
    print("Failed to fetch the eBooks page.")
    exit()

soup = BeautifulSoup(response.content, "html.parser")
book_links = []

# Extract links to individual eBook pages
for link in soup.find_all("a", href=True):
    if "/ebooks/" in link['href']:
        book_links.append("https://www.gutenberg.org" + link['href'])

# Download eBooks, excluding poetry
count = 0
for book_link in book_links:
    book_response = requests.get(book_link)
    book_soup = BeautifulSoup(book_response.content, "html.parser")

    # Check if the book is categorized as "Poetry"
    is_poetry = False
    for subject in book_soup.find_all("a", href=True):
        if "Poetry" in subject.text:
            is_poetry = True
            break

    if is_poetry:
        print(f"Skipping poetry book: {book_link}")
        continue

    # Look for txt UTF-8 format
    downloaded = False
    for download_link in book_soup.find_all("a", href=True):
        if "txt" in download_link['href']:
            download_url = "https://www.gutenberg.org" + download_link['href']
            file_name = download_url.split("/")[-1]
            file_path = os.path.join(save_dir, file_name)

            # Download the file
            print(f"Downloading {file_name}...")
            file_response = requests.get(download_url)
            with open(file_path, "wb") as f:
                f.write(file_response.content)
            print(f"Saved {file_name}")
            downloaded = True
            break

    if not downloaded:
        print(f"No downloadable formats found for {book_link}")

    print(f'{count}/{len(book_links)}')
    count += 1
    time.sleep(2)

print("All downloads completed.")
