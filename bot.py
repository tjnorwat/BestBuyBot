from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from os import path
from bs4 import BeautifulSoup
from configparser import ConfigParser


class Bot():
    def __init__(self):
        self.config = self.getConfig()
        self.checkout_url = 'https://www.bestbuy.com/checkout/r/fast-track'

        options = Options()
        options.page_load_strategy = 'normal'

        self.driver = webdriver.Chrome('chromedriver.exe', options=options)
        self.main()


    def main(self):
        # waits for items to load if it hasnt loaded already 
        self.driver.implicitly_wait(3)
        # get product page
        self.driver.get(self.config.get('URL', 'item_url'))

        # add to cart
        self.driver.find_element_by_class_name('add-to-cart-button').click()

        # redirect to checkout page
        self.driver.get(self.checkout_url)

        # wait for user to pick a store
        # input('Press Enter to continue once you have picked store \n>')

        # fill in email and phone number
        try:
            self.personalInformation()
        except NoSuchElementException:
            # if goes to checkout overview page, redirect to personal information 
            self.goToCheckout()
            self.personalInformation()

        #continue to billing address page
        self.driver.find_element_by_class_name('btn-secondary').click()

        # two different versions of checkout I have seen so far
        try:
            self.billingAddressConsolidated()
            self.driver.find_element_by_class_name('btn-secondary').click()
        except NoSuchElementException:
            self.billingAddressPayment()

        #enter in credit card information 
        self.creditCard()

        # pay
        self.driver.find_element_by_class_name('btn-primary').click()


    def getConfig(self):
        config = ConfigParser()
        if path.exists('config.mine.ini'):
            config.read('config.mine.ini')
        else:
            config.read('config.ini')
        return config


    def goToCheckout(self):
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_class_name('guest').click()


    def personalInformation(self):
        email_field = self.driver.find_element_by_id('user.emailAddress')
        phone_number_field = self.driver.find_element_by_id('user.phone')

        email_field.send_keys(self.config.get('Personal Information', 'email_address'))
        phone_number_field.send_keys(self.config.get('Personal Information', 'phone_number'))


    def billingAddressPayment(self):
        first_name_field = self.driver.find_element_by_id('payment.billingAddress.firstName')
        last_name_field = self.driver.find_element_by_id('payment.billingAddress.lastName')
        address_field = self.driver.find_element_by_id('payment.billingAddress.street')
        city_field = self.driver.find_element_by_id('payment.billingAddress.city')
        state_field = Select(self.driver.find_element_by_id('payment.billingAddress.state'))
        zip_code_field = self.driver.find_element_by_id('payment.billingAddress.zipcode')

        first_name_field.send_keys(self.config.get('Billing Address', 'first_name'))
        last_name_field.send_keys(self.config.get('Billing Address', 'last_name'))
        address_field.send_keys(self.config.get('Billing Address', 'address'))
        city_field.send_keys(self.config.get('Billing Address', 'city'))
        state_field.select_by_visible_text(self.config.get('Billing Address', 'state'))
        zip_code_field.send_keys(self.config.get('Billing Address', 'zip_code'))


    def billingAddressConsolidated(self):
        # consolidated sometimes changes; consolidatedAddresses.ui_address_xxxx.lastName
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        div = soup.find('div', {'class' : 'form-group'})
        consolidated_template = div.input['id'].replace('firstName', '')

        first_name_field = self.driver.find_element_by_id(consolidated_template + 'firstName')
        last_name_field = self.driver.find_element_by_id(consolidated_template + 'lastName')
        address_field = self.driver.find_element_by_id(consolidated_template + 'street')
        city_field = self.driver.find_element_by_id(consolidated_template + 'city')
        state_field = Select(self.driver.find_element_by_id(consolidated_template + 'state'))
        zip_code_field = self.driver.find_element_by_id(consolidated_template + 'zipcode')

        first_name_field.send_keys(self.config.get('Billing Address', 'first_name'))
        last_name_field.send_keys(self.config.get('Billing Address', 'last_name'))
        address_field.send_keys(self.config.get('Billing Address', 'address'))
        city_field.send_keys(self.config.get('Billing Address', 'city'))
        state_field.select_by_visible_text(self.config.get('Billing Address', 'state'))
        zip_code_field.send_keys(self.config.get('Billing Address', 'zip_code'))


    def creditCard(self):
        #send card number first and then rest will show up
        card_number_field = self.driver.find_element_by_id('optimized-cc-card-number')
        card_number_field.send_keys(self.config.get('Credit Card', 'card_number'))

        expiration_month_field = Select(self.driver.find_element_by_name('expiration-month'))
        expiration_year_field = Select(self.driver.find_element_by_name('expiration-year'))
        security_code_field = self.driver.find_element_by_id('credit-card-cvv')

        expiration_month_field.select_by_visible_text(self.config.get('Credit Card', 'expiration_month'))
        expiration_year_field.select_by_visible_text(self.config.get('Credit Card', 'expiration_year'))
        security_code_field.send_keys(self.config.get('Credit Card', 'security_code'))


if __name__ == '__main__':
    bot = Bot()
