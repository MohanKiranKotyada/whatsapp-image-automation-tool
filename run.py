from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd

# Paths
image_folder = 'images'    #the path of the directory that contains the images
excel_file = '1.xlsx'     #the path for the excel sheet

# Read phone numbers
df = pd.read_excel(excel_file)

# Setup Edge WebDriver with Service
service = Service(executable_path='/usr/local/bin/msedgedriver')
options = webdriver.EdgeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# Remove headless mode to allow GUI to open

driver = webdriver.Edge(service=service, options=options)
driver.get('https://web.whatsapp.com')

# Wait for QR code scan
input("Scan the QR code and press Enter...")

# Send images
for index, row in df.iterrows():
    phone_number = row['Phone Number']
    image_path = os.path.join(image_folder, f"{index + 1}.png")
    
    if os.path.exists(image_path):
        try:
            # Open chat
            driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
            time.sleep(5)
            
            # Wait for the attachment button to be clickable
            attach_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Attach"]'))
            )
            attach_button.click()
            time.sleep(1)

            image_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            image_input.send_keys(os.path.abspath(image_path))
            time.sleep(2)
            
            # Send image
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
            )
            send_button.click()
            time.sleep(5)
            print(f"Successfully sent {image_path} to {phone_number}")
        
        except Exception as e:
            print(f"Failed to send image {image_path} to {phone_number}: {e}")
    else:
        print(f"Image {image_path} not found. Skipping...")

driver.quit()
