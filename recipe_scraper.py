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

# Returns the link to the image source
def get_image(url):
  # Get response from url
  response = simple_get(url)
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for img in html.select("[class=rec-photo]"):
      print(img['src'])
      return img['src']

# Extracts list of ingredients and calculates cost
def calculate_cost(url):
  # Get response from url
  response = simple_get(url)
  cost = 0
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    for ingred_item in html.select("[itemprop=recipeIngredient]"):
      ingred = clean_up_ingred(ingred_item.string)
      cost += 1
  return cost

# Clean up ingredients from raw html
def clean_up_ingred(text):
  # Get rid of anything after a comma (e.g. egg, beated --> egg)
  unit_ingred = text.split(',')[0]
  vec = unit_ingred.split(' ')

  # Get rid of the number
  start_idx = 0
  while (vec[start_idx].isdigit()) or ("/" in vec[start_idx]):
    start_idx += 1

  # Get rid of (...)
  if vec[start_idx].startswith("("):
    while not vec[start_idx].endswith(")"):
      start_idx += 1
    start_idx += 1

  # Get rid of units of measurements
  units = ['cup', 'tablespoon', 'teaspoon', 'pound', 'ounce', 'pack', 'grate']
  while any(unit in vec[start_idx] for unit in units):
    start_idx += 1

  # Return the final ingredient
  ingred = vec[start_idx]
  start_idx += 1
  while start_idx < len(vec):
    ingred += (" " + vec[start_idx])
    start_idx += 1

  return ingred


# Extracts the needed data from all dinner recipes
def extract_dinner_data():
  base_url = "https://www.allrecipes.com/recipes/17562/dinner/"
  # Check that this page exists
  i = 1
  while does_page_exist(base_url, i) and i < 2:  
    for url in extract_recipe_urls(base_url + "?page=" + str(i)):
      time = get_time(url)
      name = get_name(url)
      servings = get_servings(url)
      img = get_image(url)
      cost = calculate_cost(url)
      
      if (time is not None) and (name is not None) and (servings is not None) and (cost is not None):
        print(str(time) + " " + name + " " + str(servings) + " " + str(cost))
    i += 1

# Checks if the desired page number exists
def does_page_exist(base_url, num):
# Get response from built url
  url = base_url + "?page=" + str(num)
  response = simple_get(url)
  
  if response is not None:
    html = BeautifulSoup(response, 'html.parser')
    # Return false if found tag with error-page class
    for error in html.select("[class=error-page]"):
      return False

    # Return true if didn't find error-page class
    return True

  # Return false if response is none
  return False

# Extract recipe urls from page
def extract_recipe_urls(url):
  # Get response from built url
  response = simple_get(url)

  html = BeautifulSoup(response, 'html.parser')
  recipes = set()
  for recipe in html.select('a[class=fixed-recipe-card__title-link]'):
    recipes.add(recipe['href'])
  return list(recipes)

extract_dinner_data()
