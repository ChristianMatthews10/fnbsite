from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import timedelta, datetime  # Import timedelta

# Set up Chrome options and headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Use headless mode

# Specify the path to chromedriver.exe
chromedriver_path = "C:\chromedriver\chromedriver.exe"

# Create a Chrome driver instance
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape exchange rates for a given date
def scrape_exchange_rates(date):
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
            print(f"Date: {date}, Currency: {currency}, Code: {code}, Bank Selling: {bank_selling}, Bank Buying: {bank_buying}")

# Define the date range from 2023-01-01 to 2023-09-17
start_date = datetime(2023, 1, 1)  # Convert start_date to a datetime object
end_date = datetime(2023, 9, 17)   # Convert end_date to a datetime object


# Iterate through the date range and scrape data for each date
current_date = start_date
while current_date <= end_date:
    scrape_exchange_rates(current_date.strftime("%Y-%m-%d"))  # Convert datetime to string
    current_date += timedelta(days=1)

# Close the Chrome driver
driver.quit()


