import requests
from bs4 import BeautifulSoup
import csv

# Base URL for the Funds Directory
base_url = "https://markets.ft.com/data/funds/uk/directory/"

# Define a list of alphabetical sections (a to z)
alphabet = [chr(i) for i in range(97, 123)]  # 'a' to 'z'

# Create a CSV file to store the data
csv_file = open('ref_fund_providers.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Provider Name', 'Provider Link'])  # Write headers

# Create a function to scrape data from a given URL
def scrape_fund_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='mod-ui-table')
        for row in table.find_all('tr'):
            provider_name = row.find('a', class_='mod-ui-link')
            provider_link = provider_name['href'] if provider_name else None
            provider_name = provider_name.get_text() if provider_name else None
            if provider_name and provider_link:
                csv_writer.writerow([provider_name, provider_link])
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Iterate through alphabetical sections and pages
for letter in alphabet:
    page_number = 1
    while True:
        url = f"{base_url}{letter}?page={page_number}&pageSize=50"
        print(f"Scraping data from {url}")
        scrape_fund_data(url)
        page_number += 1

        # Check if there is a 'More results' button
        pagination = soup.find('div', class_='o-buttons__pagination')
        if not pagination:
            break
        next_button = pagination.find('button', class_='o-buttons-icon--arrow-right')
        if not next_button:
            break

print("Scraping and CSV writing complete.")
csv_file.close()
