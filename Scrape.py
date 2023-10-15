from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service

URL = "https://data.gov.au/dataset/ds-vic-79163a67-097d-4454-ab4d-d77e58cc5985/details?q=ict%20projects"

# Start the browser and open the URL
s = Service(r"C:\Users\arshh\OneDrive\Desktop\DataScience Challenge 2023\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get(URL)

# Click the "Table" button
driver.find_element(By.XPATH, "//button[text()='Table']").click()

# Wait for the table to load
time.sleep(5)

# Click to show 100 rows
driver.find_element(By.XPATH, "//option[text()='100 rows']").click()
time.sleep(5)

# Initialize empty list to store all data across pages
data = []

# A function to scrape data from the current page
def scrape_current_page(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.select(".rt-tr")
    page_data = []
    
    for row in rows:
        columns = [col.get_text().strip() for col in row.select(".rt-td")]
        if columns:  # check if list is not empty
            page_data.append(columns)

    return page_data

# Get initial data from the first page
data.extend(scrape_current_page(driver))

# Keep clicking the "Next" button and scraping until the last page is reached
i=0
while i<4:
    try:
        # Click on the "Next" button
        next_button = driver.find_element(By.XPATH, "//button[text()='Next']")
        next_button.click()
        time.sleep(5)  # Give it time to load new page data
        
        # Scrape data from the current page
        page_data = scrape_current_page(driver)
        data.extend(page_data)
        i+=1
    except:
        # Break the loop if "Next" button is not found (indicating we're on the last page)
        break

# Extract headers
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
headers_elements = soup.select(".rt-resizable-header-content")
headers = [header.get_text().strip() for header in headers_elements]

rows_list = []

for row_data in data:
    row_dict = {}
    for i, header in enumerate(headers):
        if i < len(row_data):  # To handle any potential mismatch in length
            row_dict[header] = row_data[i]
    rows_list.append(row_dict)

df = pd.DataFrame(rows_list)
print(df)

# Save to CSV
df.to_csv("output_data.csv", index=False)
