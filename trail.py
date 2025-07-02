import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = FastAPI()

class ProductList(BaseModel):
    products: list[str]

def create_driver():
    options = Options()
    options.add_argument('--headless')  # Remove this if you want to see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver

def zepto_agent(product_list):
    driver = create_driver()
    try:
        # Step 1: Open ZeptoNow
        driver.get("https://www.zeptonow.com")
        time.sleep(5)

        # Step 2: Accept/close pop-ups if present (optional)
        try:
            esc_elem = driver.find_element(By.XPATH, '//button[text()="×"]')
            esc_elem.click()
        except:
            pass

        # Step 3: Select saved address (if applicable)
        # This part depends on your saved address setup; may require login

        # Step 4: Search and add each product
        for product in product_list:
            search_input = driver.find_element(By.tag_name, 'input')
            search_input.clear()
            search_input.send_keys(product)
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)

            # Click on first product’s "Add" button
            try:
                add_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Add')]")
                if add_buttons:
                    add_buttons[0].click()
                    time.sleep(2)
            except Exception as e:
                print(f"Error adding product {product}: {e}")

        # Step 5: Checkout
        # Click cart
        try:
            cart_icon = driver.find_element(By.XPATH, "//a[contains(@href,'/cart')]")
            cart_icon.click()
            time.sleep(3)
        except Exception as e:
            print("Error accessing cart:", e)

        # Proceed to checkout if login is handled
        return {"status": "success", "message": f"Ordered (simulated): {', '.join(product_list)}"}

    finally:
        driver.quit()

@app.post("/order")
def order_groceries(item: ProductList):
    try:
        result = zepto_agent(item.products)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
