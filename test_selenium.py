from selenium import webdriver

# Use ChromeDriver without specifying 'executable_path'
driver = webdriver.Chrome()

# Open Google to test functionality
driver.get("https://www.google.com")

# Wait for 5 seconds, then close
driver.implicitly_wait(5)
driver.quit()