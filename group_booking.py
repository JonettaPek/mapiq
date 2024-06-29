from config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--disable-features=NetworkServiceInProcess")
options.add_argument('--auto-select-certificate-for-urls=https://app.mapiq.com/')
options.add_argument('--disable-popup-blocking')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=options
)

url = 'https://app.mapiq.com/' 

driver.get(url)
actions = ActionChains(driver)

main_window_handle = driver.current_window_handle

try:
    print('Logging in...')
    
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'sc-fbYMXx.dyuplY'))
    )
    actions.click(login_button).perform()
    
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'signInName'))
    )
    email_input.clear()
    email_input.send_keys(EMAIL + Keys.ENTER) #TODO: remove email address

    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'form-control.input.ext-input.text-box.ext-text-box'))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD + Keys.ENTER) #TODO: remove password

    time.sleep(10)

    calendar_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="organisms-navigation-calendar"]'))
    )
    actions.click(calendar_tab).perform()

    print('Logged in successfully.')

    date_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'a[data-testid="undefined-card-cell-{DATE}"]')) 
    )
    actions.click(date_card).perform()

    where_will_you_be_tile = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="workday-tile"]'))
    )
    actions.click(where_will_you_be_tile).perform()

    singapore_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/div/div[3]/div'))
    )
    actions.click(singapore_button).perform()

    invitees_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-bqWxrE.sc-gsGlKL.fHjzj.eRpPDZ'))
    )
    actions.click(invitees_button).perform()

    for invitee in INVITEES:
        emails_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea[data-testid="molecules-ChipSelect_text-input"]'))        
        )
        actions.click(emails_textarea).send_keys(invitee.email).perform()

        invitee_cell = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'p[data-testid="molecules-InviteeCardCell_name-or-email"]'))
        )
        actions.click(invitee_cell).perform()

    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/div/div[3]/button'))
    )
    actions.click(confirm_button).perform()

    workspace_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="select-workspace-button"]'))
    )
    actions.click(workspace_button).perform()

except Exception as e:
    print('An error occurred:', e)

finally:
    input("Press Enter to close the browser and end the script...")
    driver.quit()