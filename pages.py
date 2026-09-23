from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_taxi_button = (By.CSS_SELECTOR, '.button.round')
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_input_field = (By.ID, 'phone')
    phone_next_button = (By.CSS_SELECTOR, '.button.full')
    sms_code_field = (By.ID, 'code')
    sms_confirm_button = (By.XPATH, '//*[contains(text(), "Confirm") or contains(text(), "Confirmar")]')
    comfort_tariff_button = (By.XPATH, '//*[text()="Comfort"]')
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.CLASS_NAME, 'pp-plus-container')
    card_number_field = (By.ID, 'number')
    card_cvv_field = (By.CSS_SELECTOR, 'input#code.card-input')
    link_card_confirm_button = (By.CSS_SELECTOR, 'button[type="submit"]')
    comment_for_driver_field = (By.ID, 'comment')
    blanket_and_tissues_switch = (By.CSS_SELECTOR, '.r-sw-label, .slider.round')
    add_ice_cream_button = (By.CSS_SELECTOR, '.counter-plus')
    ice_cream_counter_value = (By.CSS_SELECTOR, '.counter-value')
    order_taxi_final_button = (By.CLASS_NAME, 'smart-button')
    card_modal_header = (By.XPATH, '//*[text()="Adding a card" or text()="Añadir tarjeta"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- MÉTODOS DE ACCIÓN ---
    def set_route(self, from_address, to_address):
        self.wait.until(expected_conditions.element_to_be_clickable(self.from_field)).send_keys(from_address)
        self.wait.until(expected_conditions.element_to_be_clickable(self.to_field)).send_keys(to_address)

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
        button_element = self.wait.until(expected_conditions.presence_of_element_located(self.link_card_confirm_button))
        self.driver.execute_script("arguments[0].click();", button_element)

    def set_message_for_driver(self, message):
        input_field = self.wait.until(expected_conditions.element_to_be_clickable(self.comment_for_driver_field))
        input_field.clear()
        input_field.send_keys(message)

    def toggle_blanket_and_tissues(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.blanket_and_tissues_switch)).click()

    def add_ice_creams(self, quantity):
        import time
        plus_button = self.wait.until(expected_conditions.element_to_be_clickable(self.add_ice_cream_button))
        for _ in range(quantity):
            plus_button.click()
            time.sleep(0.25)

    def get_ice_cream_count(self):
        return self.wait.until(expected_conditions.visibility_of_element_located(self.ice_cream_counter_value)).text

    def click_final_order_button(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.order_taxi_final_button)).click()