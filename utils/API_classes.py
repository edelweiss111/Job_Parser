from abc import ABC, abstractmethod
from pprint import pprint

import requests


class UrlError(Exception):
    """Класс ошибки в URL адресе"""
    pass


class JobAPI(ABC):
    """Абстракный класс для работы с API платформ по поиску работы"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, name):
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API платформы HeadHunter"""

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, name):
        """Метод, который возвращает вакансии по заданному параметру"""
        response = requests.get(self.url, params={
            'text': name,
            'area': 113,
            'only_with_salary': True,
            'per_page': 100
        })
        return response.json()


class SuperJobAPI(JobAPI):
    """Класс для работы с API платформы SuperJob"""

    def __init__(self):
        pass

    def get_vacancies(self, name):
        pass


class Vacancy:
    """Класс для создания экземпляров вакансий и работы с ними"""

    def __init__(self, name, url, salary, requirement):
        self.name = name
        if not isinstance(self.name, str):
            raise TypeError("Название вакансии должно быть строкой")
        self.url = url
        if self.url[:8] != 'https://':
            raise UrlError("Ссылка должна начинаться с https://")
        self.salary = salary
        if self.salary is None:
            raise AttributeError('Поле не может быть пустым')
        self.requirement = requirement

    def __str__(self):
        return f'Название вакансии - {self.name}\n' \
               f'Ссылка - {self.url}\n' \
               f'З/п до {self.salary["to"]} {self.salary["currency"]}\n' \
               f'Требования - {self.requirement}\n'

    def __eq__(self, other):
        return self.salary['to'] == other.salary['to']

    def __ne__(self, other):
        return self.salary['to'] != other.salary['to']

    def __lt__(self, other):
        return self.salary['to'] < other.salary['to']

    def __le__(self, other):
        return self.salary['to'] <= other.salary['to']

    def __gt__(self, other):
        return self.salary['to'] > other.salary['to']

    def __ge__(self, other):
        return self.salary['to'] >= other.salary['to']

#
# hh = HeadHunterAPI().get_vacancies('python')
# vac = Vacancy(hh['items'][0]['name'], hh['items'][0]['alternate_url'], hh['items'][0]['salary'],
#               hh['items'][0]['snippet']['requirement'])
# vac1 = Vacancy(hh['items'][2]['name'], hh['items'][2]['alternate_url'], hh['items'][2]['salary'],
#                hh['items'][2]['snippet']['requirement'])
# pprint(hh['items'])
# pprint(vac < vac1)
