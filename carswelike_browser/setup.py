#!/usr/bin/env python3

import os
import time

def setup(resolution="2160x3840", headless=False, download_dir=None):
    """
    Creates & returns a Chrome (undetected_chromedriver) WebDriver.
    
    Args:
        resolution (str): e.g. "2160x3840". Default is 4K vertical.
        headless (bool): Whether to run Chrome headless. Default = False.
        download_dir (str, optional): Folder path where downloaded files go.
                                      Defaults to the current working directory.

    Returns:
        WebDriver: A Selenium-compatible undetected_chromedriver instance.
    """
    # 1. PATCH undetected_chromedriver (if you have fix_undetected_chromedriver)
    try:
        from .fix_undetected_chromedriver import fix_undetected_chromedriver
        fix_undetected_chromedriver()
    except ImportError:
        print("[setup] WARNING: Could not import fix_undetected_chromedriver.")

    import undetected_chromedriver as uc

    if download_dir is None:
        download_dir = os.getcwd()

    # Parse resolution
    if "x" in resolution.lower():
        try:
            width, height = resolution.lower().split("x")
            width = width.strip()
            height = height.strip()
            _win_size = f"--window-size={width},{height}"
        except Exception:
            print(f"[setup] Warning: cannot parse resolution '{resolution}', "
                  "using 2160x3840 fallback.")
            _win_size = "--window-size=2160,3840"
    else:
        print(f"[setup] Unexpected resolution format '{resolution}', "
              "using 2160x3840 fallback.")
        _win_size = "--window-size=2160,3840"

    options = uc.ChromeOptions()
    options.add_argument(_win_size)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")

    if headless:
        # Use the "new" headless mode if your Chrome version >= 109
        # This is often less detectable / more similar to headful
        options.add_argument("--headless=new")
        # If you have an older Chrome version, try just "--headless"
        # or install a newer Chrome.

    # Preferences
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    time.sleep(2)

    # Remove navigator.webdriver property
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": '''
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            '''
        },
    )

    return driver

#### 20250219 backup ####
"""
#!/usr/bin/env python3

import os
import time

def setup(resolution="2160x3840", headless=False, download_dir=None):
    """
    Creates & returns a Chrome (undetected_chromedriver) WebDriver.
    
    Args:
        resolution (str): e.g. "2160x3840". Default is 4K vertical.
        headless (bool): Whether to run Chrome headless. Default = False.
        download_dir (str, optional): Folder path where downloaded files go.
                                      Defaults to the current working directory.

    Returns:
        WebDriver: A Selenium-compatible undetected_chromedriver instance.
    """
    # 1. PATCH undetected_chromedriver first (to remove 'distutils' references).
    #    Make sure fix_undetected_chromedriver.py doesn't do a top-level import
    #    of undetected_chromedriver itself.
    try:
        from .fix_undetected_chromedriver import fix_undetected_chromedriver
        fix_undetected_chromedriver()
    except ImportError:
        # If you can't import or don't have a patch script, just pass or install distutils
        print("[setup] WARNING: Could not import fix_undetected_chromedriver.")

    # 2. Now import undetected_chromedriver safely (after patch is applied).
    import undetected_chromedriver as uc

    if download_dir is None:
        download_dir = os.getcwd()  # default to present working directory

    # Parse resolution
    if "x" in resolution.lower():
        try:
            width, height = resolution.lower().split("x")
            width = width.strip()
            height = height.strip()
            _win_size = f"--window-size={width},{height}"
        except Exception:
            print(f"[setup] Warning: cannot parse resolution '{resolution}', "
                  "using 2160x3840 fallback.")
            _win_size = "--window-size=2160,3840"
    else:
        print(f"[setup] Unexpected resolution format '{resolution}', "
              "using 2160x3840 fallback.")
        _win_size = "--window-size=2160,3840"

    options = uc.ChromeOptions()
    options.add_argument(_win_size)

    if headless:
        options.add_argument("--headless")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    time.sleep(2)

    # Remove navigator.webdriver property
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": '''
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            '''
        },
    )

    return driver
"""
