import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def get_card_bank_listpro(bin):
    """
    Utiliza Selenium para buscar en binlist.pro en caso de no encontrar el bin en binlist.net
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        driver.get("https://binlist.pro/")
        bin_input = driver.find_element(By.NAME, "bins")
        bin_input.send_keys(bin)

        submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-default')
        submit_button.click()
        time.sleep(5)

        try:
            bank_element = driver.find_element(By.CSS_SELECTOR, '.table-responsive table tbody tr td:nth-child(6) a')
        except:
            bank_element = driver.find_element(By.CSS_SELECTOR, '.table-responsive table tbody tr td:nth-child(6)')

        bank_name = bank_element.text
        driver.quit()
        if bank_name:
            return bank_name
        else:
            return ""
    except Exception as e:
        print("Error en selenium", e)
        return ""


def get_card_bank_lookup(bin):
    """
    Realiza una solicitud a la API de binlist.net y devuelve un diccionario
    con la información del emisor de la tarjeta.
    """
    url = f"https://lookup.binlist.net/{bin}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
        return response.json().get("bank", {}).get("name", "")
    else:
        return ""

def get_card_bank_control(bin):
    bank = get_card_bank_lookup(bin)
    if not bank:
        bank = get_card_bank_listpro(bin)
    return bank

if __name__ == "__main__":
    df = pd.read_excel("archivo.xlsx")
    df["emisor"] = df["numero_tarjeta"].astype(str).str[:6].apply(get_card_bank_control)
    df.to_excel("archivo_con_emisores.xlsx", index=False)