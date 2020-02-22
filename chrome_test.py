import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://www.baidu.com/s?wd=python%20%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2&pn=0")

time.sleep(3)
content_left = browser.find_element_by_id('content_left')
lst = browser.find_elements_by_xpath("//div[@class='result c-container ']/h3//a[@data-click]")
for item in lst:
    print(item.get_attribute('href'))


browser.find_elements_by_class_name('pc')[3].click()
time.sleep(3)
browser.find_elements_by_class_name('pc')[5].click()
time.sleep(3)
browser.find_elements_by_class_name('pc')[8].click()


