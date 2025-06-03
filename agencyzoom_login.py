from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

# Launch Chrome
driver = webdriver.Chrome()

# Open AgencyZoom login page
driver.get("https://app.agencyzoom.com/login")

# Wait for page load
time.sleep(3)

# Enter credentials (Update with your credentials)
username_input = driver.find_element(By.ID, "validation-email")
password_input = driver.find_element(By.ID, "validation-password")

username_input.send_keys("Patrick.Stabell@SWFLinsurance.com")
password_input.send_keys("Southwest2024")
password_input.send_keys(Keys.RETURN)

# Wait for login to process
time.sleep(5)
print("Login successful!")

# Navigate to Sales Reports page
driver.get("https://app.agencyzoom.com/sales-report/index")
time.sleep(5)

# Click the filter button
filter_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn') and contains(@class, 'btn-primary') and contains(@class, 'search')]"))
)
filter_button.click()
time.sleep(2)  # Allow filter popup to fully load

# Click the timeframe dropdown (Restoring previous method)
timeframe_dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Timeframe')]/following-sibling::div/button[contains(@class, 'dropdown-toggle')]"))
)
timeframe_dropdown.click()
time.sleep(3)  # Ensure dropdown stays open

# Debug: Print available dropdown items to confirm "Last Week" appears
dropdown_items = driver.find_elements(By.XPATH, "//ul[contains(@class, 'dropdown-menu show')]//a")
for item in dropdown_items:
    print(item.text)  # Ensure "Last Week" appears

# Select "Last Week" (Refining interaction to ensure selection)
last_week_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'date-selector') and contains(text(), 'Last Week')]"))
)
ActionChains(driver).move_to_element(last_week_option).click().perform()
time.sleep(2)  # Ensure selection applies

popup_buttons = driver.find_elements(By.XPATH, "//button")
for button in popup_buttons:
    print(button.text, button.get_attribute('class'))  # Verify what buttons exist

# Close all visible popups dynamically
popup_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'close')]")

for button in popup_buttons:
    try:
        button.click()
        time.sleep(1)  # Allow the UI to register the action
    except:
        print(f"Could not close popup: {button.get_attribute('outerHTML')}")


# Optional: Small wait to ensure the dropdown fully closes before proceeding
time.sleep(1)

# Click "Premium" next to your name (Update your exact name)
premium_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), 'Patrick Stabell')]/following-sibling::td/a"))
)
premium_link.click()
time.sleep(2)

import os
import time

# Open system print settings
os.system("rundll32 printui.dll,PrintUIEntry /p /n \"Microsoft Print to PDF\"")
time.sleep(3)  # Wait for dialog to appear

import pyautogui

time.sleep(2)  # Wait for settings to open

# Click "Preferences" (adjust coordinates for your screen)
pyautogui.click(300, 250)
time.sleep(1)

# Select "Landscape" Orientation
pyautogui.click(400, 350)
time.sleep(1)

# Click "OK" to apply
pyautogui.click(500, 500)
time.sleep(1)

# Click "Print" to save as PDF
pyautogui.click(600, 550)


time.sleep(2)  # Allow the print dialog to appear


print("Report downloaded successfully!")
driver.quit()