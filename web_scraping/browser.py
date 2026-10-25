from playwright.async_api import async_playwright
from pathlib import Path
import asyncio
import base64
import json


def create_a_floder():
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    return output_dir   

def write_to_json(data_json, file_path):
    with open (file_path, "w", encoding="utf-8") as file:
        json.dump(data_json, file, indent=4)


'''read a input file and return url list'''
def urls_list():
    input_file = Path("input/urls.input")

    with open (input_file, "r", encoding="utf-8") as file:
        content = file.read()
    urls = content.splitlines()

    return urls


async def processing(index,url):

    output_dir = create_a_floder()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)


            # save all resources in page
        resources = []

        # create a new browser from all request
        page = await browser.new_page()

        # create a path folder
        folder_name = f"url_{index}"
        folder_path = output_dir / folder_name
        screenshot_path = folder_path / "screenshot.png"
        jsonFile_path = folder_path / "browse.json" 

        # create a floder
        folder_path.mkdir(exist_ok=True)

        # this lamda take all reqest from page
        page.on("request", lambda request: resources.append(request.url))

        # opens the page and waits for it to load
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # take data
        await page.screenshot(path= screenshot_path)
        html = await page.content()

        # take a screenshot and do it base64
        with open(screenshot_path, "rb") as image_file:
            image_bytes = image_file.read()

        screenshot_base64 = base64.b64encode(image_bytes).decode("utf-8")


        data_json = {
            "html": html,
            "resources": resources,
            "screenshot": screenshot_base64
        }
        write_to_json(data_json, jsonFile_path)
    
    #close a browser page
    page.close()

    # close a browser
    browser.close()

async def main():
    urls = urls_list()

    for index, url in enumerate(urls, start=1):
        await processing(index,url)
    
    print("finish")

if __name__ == "__main__":
    asyncio.run(main())