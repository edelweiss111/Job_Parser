from utils.API_classes import *
from pprint import pprint

platforms = ["headhunter", "superjob"]


def main():
    user_platform = input('Введите название платформы\n').lower()
    if user_platform not in platforms:
        print('Такой платформы нет в базе')
        exit()
    # platform = HeadHunterAPI()
    user_vacancy = input('Введите поисковый запрос:\n')
    top = int(input("Введите количество вакансий для вывода в топ N:\n"))
    # vacancy = platform.get_vacancies(user_vacancy)
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()


def filter_vacancies(vacancies, filter_words):
    """Функция для фильтрации вакансий по критериям"""
    filtered_list = []
    for vacancy in vacancies['items']:
        for words in filter_words:
            if words in vacancy['snippet']['requirement'].lower().split():
                filtered_list.append(vacancy)
    return filtered_list


def sort_vacancies(vacancies):
    """Функция для сортировки вакансий по зарплате"""
    sorted_list = []
    for vacancy in vacancies:
        if vacancy['salary'] is not None:
            if vacancy['salary']['to'] is not None:
                sorted_list.append(vacancy)
    return sorted(sorted_list, key=lambda d: d['salary']['to'], reverse=True)



hh = HeadHunterAPI()
hh1 = hh.get_vacancies('python')

filt = filter_vacancies(hh1, ['знание', 'sql'])
filt_sort = sort_vacancies(filt)


pprint(filt_sort)
