import os
from abc import ABC, abstractmethod
import json

VACANCY_FILE = 'vacancies.json'


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
