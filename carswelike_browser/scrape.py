#!/usr/bin/env python3

import time
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_RETRIES = 5
WAIT_BETWEEN_EXPANDS = 2
POSSIBLE_EXPAND_TEXTS = [
    "Show more",
    "Expand",
    "View more",
    "Load more",
]

SCROLL_STEP = 500
SCROLL_PAUSE = 1

def scrape(driver, url, scroll_mode=None):

    #Navigates 'driver' to 'url'.
    #Expands <details> and 'Show more' links.
    #If scroll_mode == "scroll", does slow scrolling.
    #Saves screenshot <domain>.png and final HTML <domain>.html.
    #Returns (screenshot_path, html_path).

    def expand_all_elements(d):
        for _ in range(MAX_RETRIES):
            expansions_this_round = 0

            details_elems = d.find_elements(By.TAG_NAME, "details")
            for dd in details_elems:
                if not dd.get_attribute("open"):
                    d.execute_script("arguments[0].setAttribute('open','')", dd)
                    expansions_this_round += 1

            for txt in POSSIBLE_EXPAND_TEXTS:
                elems = d.find_elements(
                    By.XPATH,
                    f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{txt.lower()}')]"
                )
                for e in elems:
                    try:
                        e.click()
                        expansions_this_round += 1
                        time.sleep(1)
                    except Exception:
                        pass

            time.sleep(WAIT_BETWEEN_EXPANDS)
            if expansions_this_round == 0:
                break

    def slow_scroll_to_bottom(d, step=SCROLL_STEP, pause=SCROLL_PAUSE):
        try:
            current_position = 0
            total_height = d.execute_script("return document.body.scrollHeight")
            while current_position < total_height:
                d.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(pause)
                current_position += step

            d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
        except Exception as e:
            print(f"[scrape] Slow scroll error: {e}")

    parsed = urlparse(url)
    domain = parsed.netloc or "page"
    screenshot_file = f"{domain}.png"
    html_file = f"{domain}.html"

    print(f"[scrape] Navigating to {url} ...")
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception:
        print("[scrape] Warning: page might not have fully loaded by 15s.")

    expand_all_elements(driver)

    if scroll_mode == "scroll":
        slow_scroll_to_bottom(driver)

    time.sleep(2)

    driver.save_screenshot(screenshot_file)
    print(f"[scrape] Saved screenshot to {screenshot_file}")

    final_html = driver.page_source
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[scrape] Saved HTML to {html_file}")

    return screenshot_file, html_file