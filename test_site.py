import pytest, time
from locators import Locators
from test_data import Test_Data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_website(browser):

    # Navigate & Verify title
    browser.get(Test_Data.URL_JACKETS)
    assert browser.title == Test_Data.TITLE_JACKETS

    # Open Size filter section & select medium
    browser.find_element(*Locators.FILTER_SIZE_CATEGORY).click()
    browser.find_element(*Locators.FILTER_MEDIUM).click()

    # Confirm 1st page shows 12 results by default
    item = browser.find_elements(*Locators.RESULTS_PHOTOS)
    assert len(item) == Test_Data.RESULT_QTY

    # Select the first item
    firstitem = item[0]
    firstitem.click()

    # Set the quantity
    qty = browser.find_element(*Locators.PRODUCT_QTY)
    qty.clear()
    qty.send_keys(Test_Data.ORDER_QTY)

    # Select size & color
    browser.find_element(*Locators.PRODUCT_MEDIUM).click()
    browser.find_element(*Locators.PRODUCT_BLUE).click()

    # Wait for the add product to load (takes a moment after selecting size & color), then add to cart
    add = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.PRODUCT_ADD_TO_CART))
    )
    add.click()

    # Wait for page load, then validate the order quantity updated for the cart
    WebDriverWait(browser, Test_Data.DELAY).until(
        EC.text_to_be_present_in_element((Locators.CART_ITEM_COUNT), str(Test_Data.ORDER_QTY))
    )
    assert browser.find_element(*Locators.CART_ITEM_COUNT).text == str(Test_Data.ORDER_QTY)

    # Navigate to the shopping cart
    browser.get(Test_Data.URL_CART)

    WebDriverWait(browser, Test_Data.DELAY).until(
        EC.title_is(Test_Data.TITLE_CART)
    )

    # Validate total price
    total_price = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.TOTAL_PRICE))
    )
    assert total_price.text == Test_Data.TOTAL_PRICE

    # Checkout
    browser.find_element(*Locators.PROCEED_TO_CHECKOUT).click()

    # Wait for page to load & fields to be available for shipping entry
    WebDriverWait(browser, Test_Data.DELAY).until(
        EC.title_is(Test_Data.TITLE_CHECKOUT)
    )
    email = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.CHECKOUT_EMAIL))
    )

    # Enter shipping info
    email.click()
    email.send_keys(Test_Data.EMAIL)

    browser.find_element(*Locators.CHECKOUT_FIRST_NAME).send_keys(Test_Data.FIRST_NAME)
    browser.find_element(*Locators.CHECKOUT_LAST_NAME).send_keys(Test_Data.LAST_NAME)
    browser.find_element(*Locators.CHECKOUT_ADDRESS).send_keys(Test_Data.ADDRESS)
    browser.find_element(*Locators.CHECKOUT_CITY).send_keys(Test_Data.CITY)
    browser.find_element(*Locators.CHECKOUT_STATE).send_keys(Test_Data.STATE)
    browser.find_element(*Locators.CHECKOUT_ZIP).send_keys(Test_Data.ZIPCODE)
    browser.find_element(*Locators.CHECKOUT_PHONE).send_keys(Test_Data.PHONE)

    # Choose method of shipping (updates after State changes), then click next
    method = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.CHECKOUT_METHOD))
    )
    btn_next = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.CHECKOUT_NEXT))
    )
    method.click()
    btn_next.click()

    # Wait for place order button to appear & be interactable.
    WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.CHECKOUT_PLACE_ORDER))
    )
    placeholder_click = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.element_to_be_clickable((Locators.CHECKOUT_PLACE_ORDER))
    )
    placeholder_click.click()

    # Order placed successfully
    WebDriverWait(browser, Test_Data.DELAY).until(
        EC.title_is(Test_Data.TITLE_SUCCESS)
    )

    place_order_result = WebDriverWait(browser, Test_Data.DELAY).until(
        EC.presence_of_element_located((Locators.CHECKOUT_SUCCESS))
    )
    assert Test_Data.ORDER_STRING in place_order_result.text