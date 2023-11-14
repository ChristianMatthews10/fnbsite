import requests
import pandas as pd

numb_of_pages = 10 # enter the number of pages you want to scrape

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0"}
data_list = []  # Initialize an empty list to store scraped data

for nmb in range(1, numb_of_pages + 1):  # Include the last page
    url = f"https://www.hostelworld.com/properties/1850/reviews?sort=newest&page={nmb}&monthCount=36"
    data_raw = requests.get(url, headers=headers).json()
    data_list.extend(data_raw["reviews"])  # Extend the list with the reviews from the current page
    
    print(f"page: {nmb} out of {numb_of_pages}")

# Create a DataFrame from the list of scraped data
df = pd.DataFrame(data_list)

# Print the DataFrame
print(df)
