# My Scrape Package

This is a simple package that:
- Auto-patches undetected_chromedriver for Python 3.12+ references.
- Provides `setup()` to create a non-headless 4K Chrome driver (or headless if desired).
- Provides `scrape()` to expand weg page elements like \<details\> or "Show more" sections, optionally scroll,
  and save final HTML & screenshot.

## Installation

    pip install git+https://github.com/PrimitiveContext/carswelike_browser.git

## Importing

    import my_scrape_package

## Usage

    driver = carswelike_browser.setup(resolution="2160x3840", headless=False)
    png, html = carswelike_browser.scrape(driver, "https://example.com", scroll_mode="scroll")
