import os
from abc import ABC, abstractmethod
import requests
from pprint import pprint
import json

VACANCY_FILE = 'vacancies.json'


class UrlError(Exception):
    pass

class JobAPI(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, name):
        pass


class Saver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class HeadHunterAPI(JobAPI):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, name):
        """Метод, который возвращает вакансии по заданному параметру"""
        response = requests.get(self.url, params={'text': name})
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


class JSONSaver(Saver):
    def add_vacancy(self, vacancy):
        """Метод добавляющий вакансию в JSON файл"""
        data = {'name': vacancy.name, 'url': vacancy.url, 'salary': vacancy.salary,
                'description': vacancy.description}
        with open(VACANCY_FILE, 'a') as file:
            if os.stat(VACANCY_FILE).st_size == 0:
                json.dump([data], file, ensure_ascii=False)
            else:
                with open(VACANCY_FILE) as json_file:
                    data_list = json.load(json_file)
                data_list.append(data)
                with open(VACANCY_FILE, 'w') as json_file:
                    json.dump(data_list, json_file, ensure_ascii=False)

    def get_vacancies_by_salary(self, salary):
        """Метод, возвращающий вакансию по заданной з/п"""
        with open(VACANCY_FILE) as json_file:
            data_list = json.load(json_file)
            for item in data_list:
                if item['salary']:
                    if item['salary']['to'] >= int(salary) >= item['salary']['from']:
                        return item

    def delete_vacancy(self, vacancy):
        """Метод, удаляющий выбранную вакансию из JSON файла"""
        with open(VACANCY_FILE) as json_file:
            data_list = json.load(json_file)
            for item in data_list:
                if item['url'] == vacancy.url:
                    data_list.remove(item)
        with open(VACANCY_FILE, 'w') as json_file:
            json.dump(data_list, json_file, ensure_ascii=False)



hh = HeadHunterAPI()
hh1 = hh.get_vacancies('python')

vacanc = Vacancy(hh1['items'][0]['name'], hh1['items'][0]['alternate_url'], hh1['items'][0]['salary'],
                 hh1['items'][0]['snippet']['requirement'])
# pprint(hh1)

json_saver = JSONSaver()
# json_saver.add_vacancy(vacanc)
# json_saver.delete_vacancy(vacanc)
pprint(json_saver.get_vacancies_by_salary(50000))
# print(json_saver.get_vacancies_by_salary('15000 -150000'))
