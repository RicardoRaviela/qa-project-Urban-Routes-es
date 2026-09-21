import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time

# no modificar la función retrieve_phone_code
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_taxi_button = (By.CSS_SELECTOR, '.button.round')
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_input_field = (By.ID, 'phone')
    phone_next_button = (By.CSS_SELECTOR, '.button.full')
    sms_code_field = (By.ID, 'code')
    sms_confirm_button = (By.XPATH, '//*[contains(text(), "Confirm")]')
    comfort_tariff_button = (By.XPATH, '//*[text()="Comfort"]')
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.CLASS_NAME, 'pp-plus-container')
    card_number_field = (By.ID, 'number')
    card_cvv_field = (By.NAME, 'code')
    link_card_confirm_button = (By.XPATH, '//*[text()="Add"]')
    comment_for_driver_field = (By.ID, 'comment')
    blanket_and_tissues_switch = (By.XPATH, '//*[text()="Blanket and handkerchiefs"]/..//span[@class="slider round"]')
    add_ice_cream_button = (By.XPATH, '//*[text()="Ice cream"]/..//div[@class="counter-plus"]')
    ice_cream_counter_value = (By.XPATH, '//*[text()="Ice cream"]/..//div[@class="counter-value"]')
    order_taxi_final_button = (By.CLASS_NAME, 'smart-button')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_from(self, from_address):
        self.wait.until(expected_conditions.element_to_be_clickable(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(expected_conditions.element_to_be_clickable(self.to_field)).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.wait.until(expected_conditions.visibility_of_element_located(self.from_field)).get_property('value')

    def get_to(self):
        return self.wait.until(expected_conditions.visibility_of_element_located(self.to_field)).get_property('value')

    def click_order_taxi(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.order_taxi_button)).click()

    def set_phone_number(self, phone):
        self.wait.until(expected_conditions.element_to_be_clickable(self.phone_button)).click()
        input_field = self.wait.until(expected_conditions.element_to_be_clickable(self.phone_input_field))
        input_field.clear()
        input_field.send_keys(phone)
        self.wait.until(expected_conditions.element_to_be_clickable(self.phone_next_button)).click()

    def confirm_sms_code(self, code):
        self.wait.until(expected_conditions.element_to_be_clickable(self.sms_code_field)).send_keys(code)
        self.wait.until(expected_conditions.element_to_be_clickable(self.sms_confirm_button)).click()


    def select_comfort_tariff(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.comfort_tariff_button)).click()

    def add_credit_card(self, card_num, cvv_num):
            from selenium.webdriver.common.keys import Keys
            self.wait.until(expected_conditions.element_to_be_clickable(self.payment_method_button)).click()
            self.wait.until(expected_conditions.element_to_be_clickable(self.add_card_button)).click()
            self.wait.until(expected_conditions.element_to_be_clickable(self.card_number_field)).send_keys(card_num)

            cvv_input = self.wait.until(expected_conditions.element_to_be_clickable(self.card_cvv_field))
            cvv_input.send_keys(cvv_num)
            cvv_input.send_keys(Keys.TAB)
            self.wait.until(expected_conditions.element_to_be_clickable(self.link_card_confirm_button)).click()

    def set_message_for_driver(self, message):
        input_field = self.wait.until(expected_conditions.element_to_be_clickable(self.comment_for_driver_field))
        input_field.clear()
        input_field.send_keys(message)

    def toggle_blanket_and_tissues(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.blanket_and_tissues_switch)).click()

    def add_ice_creams(self, quantity):
        plus_button = self.wait.until(expected_conditions.element_to_be_clickable(self.add_ice_cream_button))
        for _ in range(quantity):
            plus_button.click()
            time.sleep(0.25)

    def get_ice_cream_count(self):
        return self.wait.until(expected_conditions.visibility_of_element_located(self.ice_cream_counter_value)).text

    def click_final_order_button(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.order_taxi_final_button)).click()

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
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_add_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.set_phone_number(data.phone_number)
        sms_code = retrieve_phone_code(self.driver)
        routes_page.confirm_sms_code(sms_code)

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.select_comfort_tariff()
        tariff_element = self.driver.find_element(*routes_page.comfort_tariff_button)

        assert tariff_element.is_displayed()

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

        assert routes_page.driver.find_element(*routes_page.comment_for_driver_field).get_property(
            'value') == data.message_for_driver

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