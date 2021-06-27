import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_top_10_app_ids(country="US"):
    url_base = url = 'https://play.google.com/store/apps/top?hl=en_US';
    url = url_base + '&gl=' + country   
    
    driver = webdriver.Chrome(ChromeDriverManager().install())    
    driver.get(url)    
    time.sleep(10)

    elems = driver.find_elements_by_xpath("//a[@class='poRVub']")    
    app_ids = []
    for elem in elems:    
        link = (elem.get_attribute("href"))        
        app_ids.append( link.split("id=")[1])
    
    driver.close()
    
    return app_ids[:20]

