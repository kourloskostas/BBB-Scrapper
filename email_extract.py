from six.moves import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import multiprocessing
import time
from bs4 import BeautifulSoup
import glob
import requests
import csv
import logging
import os


print 'Initiated ' , 1 , '...'
dirpath = os.getcwd() # Path for current directory

chrdriver_path = dirpath + '/chromedriver'
options = webdriver.ChromeOptions()
"""
options.set_headless(True)
options.add_argument("--headless")
options.add_argument("--disable-gpu")
"""

options.add_argument('--proxy-server=http://%s' % '106.105.173.187:39360')

options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("user-agent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36]")
driver = webdriver.Chrome(executable_path = chrdriver_path,chrome_options=options)

usa_xpath = '/html/body/div[2]/div[3]/div/div/div/div[1]/button'
owner_xpath = '//*[@id="root"]/div/div/div/main/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/ul[2]/li'
emails_xpath = "//span[@class='dtm-email Text-sc-11w5ku6-0 kUdwma']"
email_hidden = "//input[@name='toEmail']"
bus_xpath = '/html/body/div[1]/div/div/div/main/div/div[4]/div/div[1]/div/div'

driver.get('https://www.bbb.org/')
usa = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, usa_xpath)))
usa.click()

  # Output
input  = open('unfiltered.csv' ) # TODO UNFILTERRED
output = csv.writer(open('filtered.csv', 'w+'))
csv_reader = csv.reader(input, delimiter=',')

line_count = 0
for row in csv_reader:
  print row[0]
  url = row[4]
  line_count += 1 

  try:
    driver.get(url + '/details')
    try:
      WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, emails_xpath)))
      email_btns = driver.find_elements_by_xpath(emails_xpath)
    except:
      email_btns =[]
      
    for btn in email_btns: 
      clicked = True
      try:  
        btn.click()
      except:
        clicked = False
    
      if clicked:
        line = []
        try:
          email = driver.find_element_by_xpath(email_hidden)
          email = email.get_attribute('value').rstrip()
          line.append(row[0])
          line.append(row[1])
          line.append(email)
          line.append(row[2])
          line.append(row[3])
          output.writerow(line)
          print  '*Thread ' , 1, ': ' , line_count
          print  '    @ ' , email
          break
        except: 
          print 'No email found!!'

    

  except:
    print 'Url problem!'
    time.sleep(3)


print('Proccesed : ' + str(line_count) + 'lines.')



try:
  driver.quit()
except:
  print 'EXITING FAILED!!'
  time.sleep(10)






"""
#validate ('data/dummy.csv','data/filtered_01.csv',1)
threads = []
for num in range(1,5):
  finame = 'data/unfiltered_0' + str(num) + '.csv'
  foname = 'data/filtered_0' + str(num) + '.csv'
  th = multiprocessing.Process(target=validate,args=(finame ,foname ,num))
  print ('Starting thread :' + str(num) + '...')
  th.start()
"""
