from abc import ABC, abstractmethod
import os
import requests

API_KEY = os.getenv('SUPERJOB_API')


class UrlError(Exception):
    """Класс ошибки в URL адресе"""
    def __init__(self, msg):
        super.__init__(msg)


class JobAPI(ABC):
    """Абстрактный класс для работы с API платформ по поиску работы"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API платформы HeadHunter"""

    def __init__(self, keyword: str):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            'text': keyword,
            'area': 113,
            'only_with_salary': True,
            'page': 0,
            'per_page': 100,
            'search_field': 'name'
        }

    def get_vacancies(self):
        """Метод, который возвращает вакансии по заданному параметру"""

        response = requests.get(self.url, params=self.params)
        return response.json()['items']


class SuperJobAPI(JobAPI):
    """Класс для работы с API платформы SuperJob"""

    def __init__(self, keyword: str):
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.params = {
            'keyword': keyword,
            'countries': 1,
            'count': 100,
            'page': 0
        }

    def get_vacancies(self):
        """Метод, который возвращает вакансии по заданному параметру"""
        headers = {
            'X-Api-App-Id': API_KEY
        }
        response = requests.get(self.url, headers=headers, params=self.params)
        return response.json()['objects']


class Vacancy:
    """Класс для создания экземпляров вакансий и работы с ними"""
    __slots__ = {'name', 'url', 'salary', 'requirement'}

    def __init__(self, name: str, url: str, salary: int, requirement: str):
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
               f'З/п до {self.salary} RUR\n' \
               f'Требования - {self.requirement}\n'

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        return self.salary != other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary
