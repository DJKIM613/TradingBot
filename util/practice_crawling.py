import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pathlib

import pandas as pd
from datetime import datetime

from db_helper import *


def set_chrome_driver(download_path=None):
	chrome_options = webdriver.ChromeOptions()
	print(download_path)
	if download_path is not None:
		prefs = {}
		prefs["download.default_directory"] = download_path
		chrome_options.add_experimental_option("prefs", prefs)

	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
	return driver


def wait_element(driver, path, timeout=10):
	WebDriverWait(driver, timeout).until(
		EC.presence_of_element_located((By.XPATH, path))
	)
	WebDriverWait(driver, timeout).until(
		EC.element_to_be_clickable((By.XPATH, path))
	)


def crawlUniverse():
	cwd = os.getcwd()
	driver = set_chrome_driver(cwd)
	url_main = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203"
	driver.get(url_main)

	path_sebu = '//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/a'
	path_detail = '//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[5]/ul/li[2]/a'
	path_data = '//*[@id="jsMdiContent"]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[1]'
	path_download = '//*[@id="MDCSTAT035_FORM"]/div[3]/div/p[2]/button[2]'
	path_csv = '//*[@id="ui-id-1"]/div/div[2]/a'

	paths = [(path_sebu, path_detail), (path_detail, path_data), (path_download, path_csv), (path_csv, None)]

	wait_element(driver, path_sebu)
	for i in range(len(paths)):
		cur = driver.find_element(By.XPATH, paths[i][0])
		cur.click()
		if paths[i][1] is not None:
			wait_element(driver, paths[i][1])

		else:
			time.sleep(10)

	for name in pathlib.Path(cwd).glob('*.csv'):
		df = pd.read_csv(name, encoding='cp949')
		date = datetime.today().strftime("%Y%m%d")

		insert_df_to_db('universe', date, df)

		os.remove(name)

	time.sleep(2000)


if __name__ == "__main__":
	crawlUniverse()
