import base64
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

def solve_captcha(driver, api_key):
    try:
        captcha_img = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div[3]/div[3]/div/div/div/form/div[5]/img"))
        )
        WebDriverWait(driver, 20).until(EC.visibility_of(captcha_img))
        driver.execute_script("arguments[0].scrollIntoView(true);", captcha_img)
        time.sleep(1)
        captcha_image_data = captcha_img.screenshot_as_png
        img_base64 = base64.b64encode(captcha_image_data).decode('utf-8')
        modified_api_key = f"{api_key}__mailru"
        task_data = {
            'clientKey': modified_api_key,
            'task': {'type': 'ImageToTextTask', 'body': img_base64}
        }
        response = requests.post('https://api.capmonster.cloud/createTask', json=task_data)
        task_id = response.json().get('taskId', None)
        if task_id:
            for _ in range(10):
                time.sleep(2)
                result_response = requests.post('https://api.capmonster.cloud/getTaskResult', json={'clientKey': api_key, 'taskId': task_id})
                result = result_response.json()
                if result.get('status') == 'ready':
                    return result['solution']['text']
            print("No solution returned by CapMonster.")
        else:
            print("Failed to create task:", response.json().get('errorCode'))
        return None
    except Exception as e:
        print(f"Error during captcha processing: {e}")
        return None
