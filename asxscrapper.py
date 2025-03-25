import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Define the output folder
output_folder = "D:/ASX Agent"
os.makedirs(output_folder, exist_ok=True)

# URL to scrape
url = "https://www.asx.com.au/markets/trade-our-cash-market/equity-market-prices"

# Set up Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
try:
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load tables

    # Parse the fully rendered page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all tables
    tables = soup.find_all("table")
    if len(tables) < 3:
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise Exception("Fewer than 3 tables found; check debug.html")

    # Function to convert table to DataFrame
    def table_to_df(table):
        headers = [th.text.strip() for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr")[1:]:  # Skip header row
            cells = [td.text.strip() for td in tr.find_all("td")]
            if cells:
                rows.append(cells)
        return pd.DataFrame(rows, columns=headers)

    # Process and save each table
    table_names = ["gains", "declines", "volume_outliers"]
    for i, table_name in enumerate(table_names):
        df = table_to_df(tables[i])
        file_path = os.path.join(output_folder, f"{table_name}.csv")
        df.to_csv(file_path, index=False)
        print(f"Saved {table_name}.csv to D:\\ASX Agent")

    print("Completed scraping and saving 3 tables")

finally:
    driver.quit()