import requests
from pathlib import Path
import bs4

url = 'https://magnit.ru/promo/'
responce = requests.get(url)
file_path = Path(__file__).parent.joinpath('magnit.html')

print(responce.text)

#soup = bs4.BeautifulSoup(responce.text)#, 'lxml')
#print(1)