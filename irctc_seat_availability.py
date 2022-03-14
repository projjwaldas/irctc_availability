#!/usr/bin/env python
# coding: utf-8

# In[2]:

# Import Modules
from selenium import webdriver
import time, os, telegram
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# In[3]:

# Parameters
doj = "09-April 2022"
src_code = 'HWH'
dest_code = 'NJP'
train_code = '12041'
coach = 'CC'

#fpath = '/Users/projjwal/python_codebase'
url = 'https://www.etrains.in/seat-availability'

# In[4]:

# Derived Parameters
doj_date = doj.split("-")
doj_month = doj_date[1]
doj_day = doj_date[0]

# In[5]:

if coach == '1A':
    coach_dd = 0
elif coach == '2A':
    coach_dd = 1
elif coach == '3A':
    coach_dd = 2
elif coach == 'SL':
    coach_dd = 7
elif coach == 'CC':
    coach_dd = 3
elif coach == '2S':
    coach_dd = 6

# In[6]:

# Telegram Parameters
#TOKEN = '1878549077:AAE6MLzkEzlDrG7GWH3C6HgyQUUMsi_9Qig'
TOKEN = '1857792663:AAFG4l7S5PJeO3vyObWEtcj2K5FnIYaeHaU'
chat_id = 573007854

# Initialise the Bot
bot = telegram.Bot(TOKEN)

# In[ ]:

# Initialise Chrome Driver
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
driver.get(url)
driver.implicitly_wait(10)

# In[49]:

# Fetch Relevant Buttons
train_number = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/div/div/div/div/form/div[1]/span[1]/input[2]")
src = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div/div/div/div/form/div[2]/span/input[2]')
dest = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div/div/div/div/form/div[3]/span/input[2]')
train_class = Select(driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div/div/div/div/form/div[5]/select'))

# Set Values
train_number.send_keys(train_code)
src.send_keys(src_code)
dest.send_keys(dest_code)
train_class.select_by_index(coach_dd)

# In[58]:

# Datepicker
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div/div/div/div/form/div[4]').click()
all_dates = driver.find_elements_by_class_name("day")
for date in all_dates:
    try:
        if date.text == str(int(doj_day)):
            #print(date.text)
            date.click()
    except:
        pass

# In[60]:

# Submit Search
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div/div/div/div/form/button').click()

# Final Result
driver.implicitly_wait(10)
avlbl_seat = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/div/div[2]/div/div[1]/div/div/div/div/span').text


# In[61]:
# Close Driver
driver.quit()

# Send Telegram Message
bot.send_message(chat_id, f"Train Number: {train_code}\nSource: {src_code}, Dest: {dest_code}\nDOJ: {doj}, Class: {coach}\nTicket availability: {avlbl_seat}")

