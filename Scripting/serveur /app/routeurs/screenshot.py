from fastapi import APIRouter, HTTPException
from app.models import ScreenshotRequest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import platform
from uuid import uuid4

router = APIRouter()

@router.post("/screenshot/")
async def take_screenshot(request: ScreenshotRequest):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    if platform.system() == "Windows":
        chromedriver_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe'
    else:
        chromedriver_path = '/usr/local/bin/chromedriver'
    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(request.url)
        filename = request.url.replace("https://", "").replace("/", "_").replace(".", "_") + ".png"
        output_dir = "static"
        os.makedirs(output_dir, exist_ok=True)
        uuid_filename = f"{uuid4()}.png"
        filepath = os.path.join(output_dir, uuid_filename)
        driver.save_screenshot(filepath)
        return {"url": f"http://localhost:9098/static/{uuid_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error taking screenshot")
    finally:
        driver.quit()
