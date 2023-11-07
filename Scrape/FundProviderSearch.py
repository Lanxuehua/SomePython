import requests
from bs4 import BeautifulSoup

# Define the URL of the webpage with pagination
url = "https://markets.ft.com/data/funds/uk/directory/%23?page=1&pageSize=50"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing the provider names and links
    table = soup.find('table', class_='mod-ui-table')
    
    # Iterate through the rows of the table
    for row in table.find_all('tr'):
        # Find the provider name and its href link in each row
        provider_name = row.find('a', class_='mod-ui-link')
        provider_link = provider_name['href'] if provider_name else None
        provider_name = provider_name.get_text() if provider_name else None

        # Print the provider name and its href link
        if provider_name and provider_link:
            print(f"{provider_name},{provider_link}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
