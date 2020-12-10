from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import csv

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver', options=chrome_options)
act=ActionChains(driver)
driver.get("https://web.whatsapp.com/")
input("PRESS ENTER AFTER LOGIN")

name = input('Enter group name (Please enter the excat name of the group)')
excel = name + '.csv'


csv_file = open(excel, 'w', encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['NAME', 'PHONE'])

driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]').send_keys(name)
sleep(2)
driver.find_element_by_xpath('//span[@title = "{}"]'.format(name)).click()
sleep(2)
# driver.find_element_by_class_name('_1vGIp').click()
driver.find_element_by_xpath('//div[@class = "_1vGIp" and @role = "button"]').click()
sleep(1)

try:
    driver.find_element_by_xpath('//span[@data-testid = "{0}" and @data-icon = "{0}" ]'.format("down")).click()
except Exception:
    pass 
driver.execute_script("document.body.style.zoom='10%'")
sleep(5)
data=driver.find_elements_by_xpath('//div[@title="Exit group" and @role="button"]//..//../div[5]/div[2]/div/div[@class="_210SC"]')
nameList= []
for all_contacts in data:
    html= all_contacts.get_attribute('innerHTML')
    soup= BeautifulSoup(html, 'lxml')
    name = soup.find_all('span', class_ = "_3Whw5")
    if name[0].text[0] == "+":
        if len(name)==1:
            content= "N/A", [name[0].text]
            print(f"{name[0].text} --> N/A")
        if len(name)==2:
            content= [name[1].text, name[0].text]
            print(f"{name[0].text} --> {name[1].text}")
        if len(name)==3:
            content= [name[2].text, name[0].text]
            print(f"{name[0].text} --> {name[2].text}")
        csv_writer.writerow(content)
    else:
        nameList.append(name[0].text)
nameList.remove('You') 

driver.execute_script("document.body.style.zoom='100%'")
sleep(3)
for name in nameList:
    driver.find_element_by_xpath('//span[@data-testid = "{0}" and @data-icon = "{0}" ]'.format("x-alt")).click()
    driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]').send_keys(name)
    sleep(1.5)
    driver.find_element_by_xpath('//span[@title = "{}"]'.format(name)).click()
    sleep(1.5)
    driver.find_element_by_class_name('_1iFv8').click()
    sleep(1)
    phn= driver.find_elements_by_xpath('//div[@title="Report contact" and @role="button"]//..//../div[4]')
    if len(phn)==0:
        phn =  driver.find_elements_by_xpath('//div[@title="Delete chat" and @role="button"]//..//../div[6]')[0].text.split("\n")[-1]
    else:
        phn= phn[0].text.split("\n")[-1]
    csv_writer.writerow([name, phn])
    print(f"{phn} --> {name}")