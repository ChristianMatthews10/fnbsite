from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.fnb.co.za/rates/ForeignExchangeRates.html')

# Wait for the overlay to appear using WebDriverWait
wait = WebDriverWait(driver, 10)

# Accept cookies
accept_cookies_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.js-accept-cookies')))
accept_cookies_button.click()

# Trigger the overlay (e.g., by clicking the "View rates" button)
overlay_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.iconButton[data-trackclick="iconButton"] span.iconText')))
overlay_button.click()

# Wait for the overlay to appear (use WebDriverWait if necessary)
# Add code to wait for the overlay to appear here

# Once the overlay is visible, scrape its content
overlay_content = driver.find_element(By.CSS_SELECTOR, '#overlay-content').text
print(overlay_content)

# Close the browser
driver.quit()


