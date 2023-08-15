from abc import ABC, abstractmethod
import requests


class UrlError(Exception):
    pass


class JobAPI(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, name):
        pass


class HeadHunterAPI(JobAPI):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, name):
        """Метод, который возвращает вакансии по заданному параметру"""
        response = requests.get(self.url, params={'text': name, 'area': 113})
        return response.json()


class SuperJobAPI(JobAPI):
    def __init__(self):
        pass

    def get_vacancies(self, name):
        pass


class Vacancy:
    def __init__(self, name, url, salary, description):
        self.name = name
        if not isinstance(self.name, str):
            raise TypeError("Название вакансии должно быть строкой")
        self.url = url
        if self.url[:8] != 'https://':
            raise UrlError("Ссылка должна начинаться с https://")
        self.salary = salary
        if self.salary is None:
            raise AttributeError('Поле не может быть пустым')
        self.description = description
