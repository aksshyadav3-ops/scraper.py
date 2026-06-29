import requests
from bs4 import BeautifulSoup
import csv

def scrape_remote_jobs():
    url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Connecting to training site...")
    
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return

    # Using the required BeautifulSoup and lxml setup
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Each entry sits inside an HTML product pod article element
    job_rows = soup.find_all('article', class_='product_pod')
    
    if not job_rows:
        print("No entries found on the page.")
        return
        
    print(f"Found {len(job_rows)} entries. Writing to CSV...")
    
    csv_file = "internships.csv"
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Location', 'Link', 'Date Posted'])
        
        processed_count = 0
        
        for row in job_rows:
            # 1. Target the text block inside the heading link tag
            title_el = row.find('h3')
            if title_el and title_el.find('a'):
                title = title_el.find('a')['title']
            else:
                title = "N/A"
                
            # 2. Extract price details out of the text container element
            price_el = row.find('p', class_='price_color')
            if price_el:
                company = price_el.text.strip()
            else:
                company = "Not Specified"
            
            # 3. Extract stock status strings
            stock_el = row.find('p', class_='instock availability')
            if stock_el:
                location = stock_el.text.strip()
            else:
                location = "Remote"
            
            # 4. Target anchor attributes safely
            link_el = row.find('a', href=True)
            if link_el:
                link = "http://books.toscrape.com/catalogue/" + link_el['href'].replace('../../../', '')
            else:
                link = "N/A"
            
            date_posted = "Recently"
            
            writer.writerow([title, company, location, link, date_posted])
            processed_count += 1
                
        print(f"Success! {processed_count} rows saved to '{csv_file}'")

if __name__ == "__main__":
    scrape_remote_jobs()