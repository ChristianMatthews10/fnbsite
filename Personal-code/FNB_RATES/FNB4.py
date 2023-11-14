from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta, datetime
import csv

# Setup Edge driver with webdriver_manager
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Function to scrape exchange rates for a given date and write to CSV
def scrape_exchange_rates(date, csv_writer):
    # Navigate to the FNB website
    driver.get("https://www.fnb.co.za/Controller?nav=rates.forex.list.ForexRatesList")

    # Find the input box for the history date and enter the date
    date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btnExchangeRates")))
    date_input.clear()
    date_input.send_keys(date)

    # Find the search button and click it
    search_button = driver.find_element(By.CLASS_NAME, "inputButtonSearch")
    search_button.click()

    # Wait for the table to load
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "group1")))

    # Extract exchange rate data from the table
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip the header row
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) == 5:
            currency = columns[1].text
            code = columns[2].text
            bank_selling = columns[3].text
            bank_buying = columns[4].text
            data = [date, currency, code, bank_selling, bank_buying]
            csv_writer.writerow(data)  # Write data to CSV

# Define the date range
start_date = datetime(2023, 10, 28)
end_date = datetime(2023, 10, 29)

# Specify the full path to your Downloads folder where you want to save the CSV file using a raw string
file_path = r"C:\Users\Christianm\Downloads"  # Replace with your desired path

# Open a CSV file for writing in your Downloads folder
file_name = f"{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}_exchange_rates.csv"
with open(file_path + '\\' + file_name, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    
    # Write header row to CSV
    csv_writer.writerow(['Date', 'Currency', 'Code', 'Bank Selling', 'Bank Buying'])

    # Iterate through the date range and scrape data for each date
    current_date = start_date
    while current_date <= end_date:
        scrape_exchange_rates(current_date.strftime("%Y-%m-%d"), csv_writer)
        current_date += timedelta(days=1)

# Close the Edge driver
driver.quit()
