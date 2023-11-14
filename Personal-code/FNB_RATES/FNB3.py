from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import timedelta, datetime
import csv  # Import the csv module

# Set up Chrome options and headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Use headless mode

# Specify the path to chromedriver.exe
chromedriver_path = "C:\chromedriver\chromedriver.exe"

# Create a Chrome driver instance
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape exchange rates for a given date and write to CSV
def scrape_exchange_rates(date, csv_writer):
    # Navigate to the FNB website
    driver.get("https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList")

    # Find the input box for the history date and enter the date
    date_input = driver.find_element("id", "btnExchangeRates")
    date_input.clear()
    date_input.send_keys(date)

    # Find the search button and click it
    search_button = driver.find_element("class name", "inputButtonSearch")
    search_button.click()

    # Wait for the table to load
    table = driver.find_element("id", "group1")

    # Extract exchange rate data from the table
    rows = table.find_elements("tag name", "tr")[1:]  # Skip the header row
    for row in rows:
        columns = row.find_elements("tag name", "td")
        if len(columns) == 5:
            currency = columns[1].text
            code = columns[2].text
            bank_selling = columns[3].text
            bank_buying = columns[4].text
            data = [date, currency, code, bank_selling, bank_buying]
            csv_writer.writerow(data)  # Write data to CSV

# Define the date range
start_date = datetime(2023, 9, 28)
end_date = datetime(2023, 9, 29)

# Open a CSV file for writing
file_name = f"{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}_exchange_rates.csv"
with open(file_name, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    
    # Write header row to CSV
    csv_writer.writerow(['Date', 'Currency', 'Code', 'Bank Selling', 'Bank Buying'])

    # Iterate through the date range and scrape data for each date
    current_date = start_date
    while current_date <= end_date:
        scrape_exchange_rates(current_date.strftime("%Y-%m-%d"), csv_writer)
        current_date += timedelta(days=1)

# Close the Chrome driver
driver.quit()

