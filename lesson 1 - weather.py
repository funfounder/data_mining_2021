# e5e4cd692a72b0b66ea0a6b80255d1c3
import requests
from pprint import pprint

city = 'BREST,BY'
my_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
my_params = {'q': city,
             'appid': 'e5e4cd692a72b0b66ea0a6b80255d1c3'}

url = 'http://api.openweathermap.org/data/2.5/weather'

response = requests.get(url, params=my_params, headers=my_headers)
j_data = response.json()
#pprint(j_data)
print(f"В городе {j_data['name']} температура {j_data['main']['temp'] - 273.15} градусов")
