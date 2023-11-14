from flask import Flask, render_template, request, send_file, make_response
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta, datetime
import csv
import os
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

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

        # Create a StringIO object and a CSV writer for it
        csv_io = io.StringIO()
        csv_writer = csv.writer(csv_io)
        
        # Write header row to CSV
        csv_writer.writerow(['Date', 'Currency', 'Code', 'Bank Selling', 'Bank Buying'])

        # Iterate through the date range and scrape data for each date
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        while current_date <= end_date:
            scrape_exchange_rates(current_date.strftime("%Y-%m-%d"), csv_writer)
            current_date += timedelta(days=1)

        # Close the Edge driver
        driver.quit()

        # Get the CSV data from the StringIO object and create a response with it as content
        csv_data = csv_io.getvalue()
        response = make_response(csv_data)
        
        # Create a filename using the start and end dates
        filename = f"exchange_rates_{start_date}_to_{end_date}.csv"
        
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        response.headers['Content-type'] = 'text/csv'
        
        return response

    return '''
        <form method="POST">
          Start Date: <input type="date" name="start_date"><br>
          End Date: <input type="date" name="end_date"><br>
          <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
