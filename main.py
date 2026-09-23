import data
import time
from selenium import webdriver
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        tariff_element = self.driver.find_element(*routes_page.comfort_tariff_button)
        assert tariff_element.is_displayed()

    def test_click_phone_button(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        self.driver.find_element(*routes_page.phone_button).click()
        assert self.driver.find_element(*routes_page.phone_input_field).is_displayed()

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.set_phone_number(data.phone_number)
        assert self.driver.find_element(*routes_page.sms_code_field).is_displayed()

    def test_confirm_sms_code(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.set_phone_number(data.phone_number)
        sms_code = retrieve_phone_code(self.driver)
        routes_page.confirm_sms_code(sms_code)
        assert self.driver.find_element(*routes_page.payment_method_button).is_displayed()

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.add_credit_card(data.card_number, data.card_code)
        assert self.driver.find_element(*routes_page.payment_method_button).is_displayed()

    def test_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.set_message_for_driver(data.message_for_driver)
        assert routes_page.driver.find_element(*routes_page.comment_for_driver_field).get_property('value') == data.message_for_driver

    def test_add_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.toggle_blanket_and_tissues()
        assert self.driver.find_element(*routes_page.blanket_and_tissues_switch).is_displayed()

    def test_add_two_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.add_ice_creams(2)
        assert routes_page.get_ice_cream_count() == "2"

    def test_order_taxi_and_search_modal(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        routes_page.click_final_order_button()
        assert self.driver.find_element(*routes_page.order_taxi_final_button).is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()