"""
HTTPs
HEADERS


"""


from pathlib import Path
import time
import json
import requests

params = {
    'record_per_page': 50,
    'page': 1,

}


url = 'https://5ka.ru/api/v2/special_offers/'
headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'

}

responce = requests.get(url, params=params, headers=headers)
html_temp = Path(__file__).parent.joinpath('temp.html')
json_temp = Path(__file__).parent.joinpath('temp.json')
json_temp.write_text(responce.text, encoding='UTF-8')

class Parse5Ka:
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }

    def __init__(self, start_url:str, products_path:Path):
        self.start_url = start_url
        self.products_path = products_path

    def _get_responce(self, url):
        while True:
            responce = requests.get(url, headers=self.headers)
            if responce.status_code == 200:
                return responce
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.products_path.joinpath(f'{product["id"]}.json')
            self.save(product, product_path)

    def _parse(self, url):
        while url:
            responce = self._get_responce(url)
            data = responce.json()
            #data = json.loads(responce.text)
            url = data['next']
            for product in data['results']:
                yield product

    @staticmethod
    def save(data: dict, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='UTF-8')

if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_path = Path(__file__).parent.joinpath('products')
    if not save_path.exists():
        save_path.mkdir()


    parser = Parse5Ka(url, save_path)
    parser.run()