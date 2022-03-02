import requests
from tokens import token_api_yndex
from settings import *


# API Яндекс.Диска
class YDisk:
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token: str):
        self.token = token
        self.headers = {'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def get_resources(self, path):
        """Метод получает информацию и возращает код о результате запроса 'path'"""
        headers = self.headers.copy()
        resp = requests.get(self.API_BASE_URL + 'resources', headers=headers,
                            params={'path': path, 'fields': 'name'})
        print(resp.json())
        return resp.status_code

    def create_directory(self, directory: str):
        """Метод создаёт дерикторию 'directory'"""
        headers = self.headers.copy()
        headers.update({'Content-Type': 'application/json'})
        resp = requests.put(self.API_BASE_URL + 'resources', headers=headers, params={'path': directory})
        cod = resp.status_code
        if cod == 201:
            print(f'{str_purple}Папка, "{directory}", успешно созданна{str_reset}')
            return True
        elif cod == 409:
            print(f'{str_purple}Дериктория, "{directory}", уже была созданна{str_reset}')
            return cod
        else:
            print(f'{str_red}Ошибка: {cod}{str_reset}')
            return False


if __name__ == '__main__':
    user = YDisk(token=token_api_yndex)
    path = 'download'
    result = user.create_directory(path)
    print(result)
    result = user.get_resources(path + '111')
    print(result)
