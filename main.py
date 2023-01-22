from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config_gs import NAME_SHEET, SAMPLE_SPREADSHEET_ID

x = 1

while x != 6715:

    with open('urls.txt') as file:
        url_site = file.readlines()

    url = url_site[x]

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'

    creds = None
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=f"""{NAME_SHEET}!A1:N100000000""").execute()

    values = result.get('values', [])

    try:

        option = Options()
        option.add_argument('--disable-infobars')
        browser = webdriver.Chrome('C:\\webdriverchrome\\chromedriver.exe', chrome_options=option)

        browser.get(url=url)
        time.sleep(3)

        vakanciya = browser.find_element(By.TAG_NAME, 'h1').text
        zarplata = browser.find_element(By.CLASS_NAME, 'salary_7tPJD').text
        organizaciya = browser.find_element(By.CLASS_NAME, 'title_7MBDL').text
        gorod = browser.find_element(By.CLASS_NAME, 'address_3E_Ck').text
        grafic_raboti_i_2_stolbik = browser.find_element(By.CLASS_NAME, 'descriptions_wVg5R').text
        new_grafic = grafic_raboti_i_2_stolbik.split(',')
        fio = browser.find_element(By.CLASS_NAME, 'hr_cY2do').text
        elem = browser.find_element(By.XPATH, "//button[text()='Показать целиком']").click()
        telephone_number = browser.find_element(By.CLASS_NAME, 'item_2PkbF').text
        print(telephone_number.split('\n'))

        result_list = [vakanciya, zarplata, organizaciya, gorod, new_grafic[0], new_grafic[1]+',\n'+new_grafic[2], fio, str(telephone_number.split('\n')[0]).replace('+', ''), url]
        print(result_list)

        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f"{NAME_SHEET}!{'A' + str(x + 1)}",
                                        valueInputOption="USER_ENTERED",
                                        body={'values': [result_list]}).execute()

        print(request)
        x = x + 1
        
    except Exception as ex:
        result_list = ['']

        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f"{NAME_SHEET}!{'A' + str(x + 1)}",
                                        valueInputOption="USER_ENTERED",
                                        body={'values': [result_list]}).execute()

        print(request)
        x = x + 1
