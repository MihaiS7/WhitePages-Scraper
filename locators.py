from selenium.webdriver.common.by import By

class MainLocators():
    VIEW_DETAILS = (By.XPATH, '//button[@aria-label="View Details"]')
    TOTAL_PAGES = (By.XPATH, '//div[@class="page-selectors"]/a[last() - 1]')
    STATES = (By.XPATH, '//div[@class="links-wrapper"]/a')

class DetailLocators():
    NAME = (By.XPATH, '//h1')
    ALIAS = (By.XPATH, '//p[@id="person-akas"]/span') 
    AGE = (By.XPATH, '//div[@class="mr-8"]/div[2]')
    LOCATION = (By.XPATH, '//div[@class="mr-8"]/following-sibling::div/div[2]')
    ADDRESS = (By.XPATH, '//a[@class="mb-1 raven--text td-n"]')
    PROPERTIES = (By.XPATH, '//span[contains(text(), "Properties")]/following-sibling::a')
    CRIMINAL_RECORD = (By.XPATH, '//span[contains(text(), "Criminal & Traffic Records")]/following-sibling::a') 
    PHONES = (By.XPATH, '//div[@id="landline"]/div/a[not(@target)]')
    RELATED = (By.XPATH, '//div[@id="relatives"]//a[not(@target)]') 



