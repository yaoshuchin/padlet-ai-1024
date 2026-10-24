import json
import re
from bs4 import BeautifulSoup

# Check if BeautifulSoup is available or write a regex parser
try:
    from bs4 import BeautifulSoup
    has_bs4 = True
except ImportError:
    has_bs4 = False

print(f"BeautifulSoup available: {has_bs4}")
