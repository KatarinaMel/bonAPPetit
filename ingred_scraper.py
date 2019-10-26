# File to scrape recipes from allrecipes.com
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# Attempts to get the content at the specified url
def simple_get(url):
  try:
    with closing(get(url, stream = True)) as resp:
      if is_good_response(resp):
        return resp.content
      else:
        return None

  except RequestException as e:
    log_error('Error during requests to {0} : {0}'.format(url, str(e)))
    return None

# Checks if the response seems to be HTML (returns true if so)
def is_good_response(resp):
  content_type = resp.headers['Content-Type'].lower()
  return (resp.status_code == 200
          and content_type is not None
          and content_type.find('html') > -1)

# Extract product heading/title
def extract_name(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for title in html.select("[class=product-heading]"):
      return title.h2.string

# Extract product cost
def extract_cost(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for plain_cost in html.select("[class=product-content]"):
      print(plain_cost)

    for orig_cost in html.select("[class=product-strike-base-price]"):
      print(orig_cost.span.string)
      return orig_cost.span.string

# Prints errors
def log_error(e):
  print(e)

url = "https://shop.vons.com/product-details.101100167.html"
url2 = "https://shop.vons.com/product-details.960017900.html?zipcode=92107&r=https%3A%2F%2Fwww.vons.com%2Fhome.html"
print(extract_name(url))
extract_cost(url)
