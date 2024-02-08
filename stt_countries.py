from bs4 import BeautifulSoup
from IPython.display import display
import requests
import pandas as pd

url = 'https://www.scrapethissite.com/pages/simple/'
page = requests.get(url)
print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')
countries = soup.find_all('div', class_='col-md-4 country')
country_names = [country.h3.text.strip() for country in countries]

df = pd.DataFrame(country_names, columns=['Country'])

country_info = soup.find_all('div', class_='country-info')
country_capitals = soup.find_all('span', class_='country-capital')
country_populations = soup.find_all('span', class_='country-population')
country_areas = soup.find_all('span', class_='country-area')

df['Capital'] = [capital.text.strip() for capital in country_capitals]
df['Population'] = [population.text.strip() for population in country_populations]
df['Area'] = [area.text.strip() for area in country_areas]

display(df)