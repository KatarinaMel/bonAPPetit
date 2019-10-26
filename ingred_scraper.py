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
    for title in html.select("[class=hf-Bot]"):
      return title.h1.string

# Extract product cost
def extract_cost(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for span in html.select("[class=price-characteristic]"):
      return float(span['content'])

# Extract price per unit
def extract_price_per_unit(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for ppu in html.select("[class*=prod-ProductOffer-ppu]"):
      words = ppu.string.split(' / ')
      price = words[0].replace('$', '')
      units = words[1]
  return [price, units]

# Prints errors
def log_error(e):
  print(e)

# Scrapes all the food products on walmart
def extract_food_data():
  base_url = "https://walmart.com/browse/food/976759/"
  # Check that the page exists
  i = 1
  while does_page_exist(base_url, i):
    for url in extract_food_urls(base_url + "?page=" + str(i)):
      name = extract_name(url)
      cost = extract_cost(url)
      ppu = extract_price_per_unit(url)

      if (name is not None) and (cost is not None) and (ppu is not None):
        print(name + " " + str(cost) + " " + str(ppu))
      i += 1

# Checks if the desired page number exists
def does_page_exist(base_url, num):
  # Get response from built url
  url = base_url + "?page=" + str(num)
  response = simple_get(url)

  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    # Return false if fbody is empty
    for error in html.select('body'):
      if error is not None:
        return True
      return False
  return False

# Extract food urls from page
def extract_food_urls(url):
  # Get response from built url
  response = simple_get(url)

  html = BeautifulSoup(response, 'html.parser')
  foods = set()
  for food in html.find_all(attrs={'class': 'search-result-productimage'}):
    foods.add("https://walmart.com" + food.div.a['href'])
  return list(foods)

extract_food_data()
