# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
# о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172

from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mails']

driver = webdriver.Chrome(executable_path='.\chromedriver.exe')
driver.get('https://mail.ru/')

login = driver.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172')

pass_button = driver.find_element_by_id('mailbox:submit-button')
pass_button.click()
time.sleep(2)
pass_input = driver.find_element_by_id('mailbox:password-input')
pass_input.send_keys('NextPassword172')

submit_button = driver.find_element_by_id('mailbox:submit-button')
submit_button.click()
time.sleep(3)

mail = driver.find_element_by_class_name('llc')
mail_link = mail.get_attribute('href')
driver.get(mail_link)
time.sleep(2)

while True:
    time.sleep(1)
    msg_from = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    msg_date = driver.find_element_by_class_name('letter__date').text
    msg_subject = driver.find_element_by_class_name('thread__subject').text
    msg_text = driver.find_element_by_class_name('letter__body').text

    db.mails.insert_one({'from': msg_from,
                         'date': msg_date, #записывает строкой всё подряд
                         'subject': msg_subject,
                         'text': msg_text
                         })

    next_msg = driver.find_element_by_xpath('//span[@title = "Следующее"]')
    if not next_msg.get_attribute('disabled'):
        next_msg.click()
    else:
        break