# __init__.py
#
# Automatically patch undetected_chromedriver once, then expose setup() and scrape().

from .fix_undetected_chromedriver import fix_undetected_chromedriver
from .setup import setup
from .scrape import scrape

fix_undetected_chromedriver()  # run patch once

__all__ = ["setup", "scrape"]