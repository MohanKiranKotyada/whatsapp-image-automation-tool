# WhatsApp Image Sender Automation Tool
Python script for sending images to multiple WhatsApp contacts, automating the process using Selenium WebDriver and Microsoft Edge browser. I have done this project on WSL, so all the commands are for Linux systems.

## **Overview**
This project automates sending images through WhatsApp using Selenium WebDriver and the Microsoft Edge browser. Follow this guide to set up the environment, understand the code, and troubleshoot issues.

---

## **1. Prerequisites and Setup**

### **a. Install Microsoft Edge Browser**
1. **Add Microsoft Edge repository:**
   ```bash
   curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
   sudo apt-add-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"

2. **Install Microsoft Edge:**
   ```bash
   sudo apt update
   sudo apt install microsoft-edge-stable
   ```

3. **Verify installation:**
   ```bash
   microsoft-edge-stable --version
   ```

### **b. Install Edge WebDriver (for Selenium integration)**
1. **Download the matching version of `msedgedriver`:**
- Go to [Microsoft Edge Driver download](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and download the version corresponding to your installed Edge version.
- Extract and move `msedgedriver` to `/usr/local/bin` (or another directory of your choice):
     ```bash
     sudo mv msedgedriver /usr/local/bin/
     sudo chmod +x /usr/local/bin/msedgedriver
     ```

### **c. Install Python and Required Libraries**
1. **Ensure Python3 is installed:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install required Python libraries (Selenium, Pandas, etc.):**
   ```bash
   pip3 install selenium pandas openpyxl
   ```
### **d. Setup the directories**
1. **Excel File (contacts.xlsx)**  
- Prepare an Excel file (`contacts.xlsx`) containing the phone numbers (in the column named "Phone Number") to which you want to send images.
- The file should look like this:
     | Phone Number |
     |--------------|
     | 1234567890   |
     | 0987654321   |
     | ...          |

2. **Image Folder**  
- Place the images you want to send in a folder named `images`. Ensure that each image is named sequentially as `1.png`, `2.png`, etc.
---

## **2. Code Explanation**

### **a. Imports and Initial Setup**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time
import os
import pandas as pd
```
- **Selenium WebDriver:** Used for browser automation.
- **Pandas:** Used to read phone numbers from an Excel file.
- **time and os:** For delays and file system interactions.

### **b. File Paths and Data Reading**
```python
# Paths
image_folder = 'images'
excel_file = '1.xlsx'

# Read phone numbers
df = pd.read_excel(excel_file)
```

### **c. Setting up the WebDriver**
```python
service = Service(executable_path='/usr/local/bin/msedgedriver')
options = webdriver.EdgeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')  # Run in headless mode (without GUI)

driver = webdriver.Edge(service=service, options=options)
driver.get('https://web.whatsapp.com')
```

### **d. QR Code Scan**
```python
input("Scan the QR code and press Enter...")
```

### **e. Sending Images**
```python
for index, row in df.iterrows():
    phone_number = row['Phone Number']
    image_path = os.path.join(image_folder, f"{index + 1}.png")
    
    if os.path.exists(image_path):
        try:
            driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
            time.sleep(5)
            
            attach_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Attach"]'))
            )
            attach_button.click()
            time.sleep(1)

            image_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            image_input.send_keys(os.path.abspath(image_path))
            time.sleep(2)
            
            send_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="send"]')
            send_button.click()
            time.sleep(5)
            print(f"Successfully sent {image_path} to {phone_number}")
        
        except Exception as e:
            print(f"Failed to send image {image_path} to {phone_number}: {e}")
    else:
        print(f"Image {image_path} not found. Skipping...")
```

### **f. Closing the WebDriver**
```python
driver.quit()
```

---

## **3. Troubleshooting Tips**
- **Webdriver issues:** Ensure `msedgedriver` is the correct version for your Microsoft Edge version.
- **GUI not launching:** Ensure that `DISPLAY` is set correctly (for WSL or native Linux systems).
- **Element not found:** Double-check the selectors using browser developer tools and adjust the XPath/CSS selectors as needed.

---

## **4. Final Thoughts**
This script can be extended by automating other tasks like sending messages, using attachments from different file types, or scheduling image sending. It leverages Selenium's powerful capabilities to interact with web elements, simulating human behavior in a browser.

This project was a really fun one! I had to send a bunch of images to my family members and was wondering if there were any automation tools for that. So, this was quite useful. 😄
