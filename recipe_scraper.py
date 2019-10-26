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

# Prints errors
def log_error(e):
  print(e)

# Return the time that it takes to make the recipe
def get_time(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for span in html.select("[class=ready-in-time]"):
        words = span.string.split(' ')
        time = int(words[0])
        if words[1] == "h":
          time = time * 60
        return time

# Returns the name of the recipe
def get_name(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for name in html.select("[id=recipe-main-content]"):
      return name.string

# Returns the number of servings in the recipe
def get_servings(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for servings in html.select("[id=metaRecipeServings]"):
      return int(servings['content'])

url1 = 'https://www.allrecipes.com/recipe/65691/pumpkin-waffles-with-apple-cider-syrup/?internalSource=editorial_2&referringId=78&referringContentType=Recipe%20Hub';
url2 = 'https://www.allrecipes.com/recipe/23376/cinnamon-swirl-bread/'
print(get_time(url2))
print(get_name(url2))
print(get_servings(url2))
