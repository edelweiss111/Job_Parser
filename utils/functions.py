from utils.API_classes import *
from utils.Save_classes import JSONSaver

platforms = ["HeadHunter", "SuperJob"]


def main():
    while True:
        '''Функция интерфейса пользователя'''
        # Пользователь выбирает платформу
        user_input = input('Введите название платформы. Если хотите выйти введите "exit"\n').lower()
        if user_input == platforms[0].lower():
            platform = HeadHunterAPI()
            break
        elif user_input == platforms[1].lower():
            platform = SuperJobAPI()
            break
        elif user_input.lower() == 'exit':
            exit()
        else:
            print('Такой платформы нет в базе')

    # Пользователь выбирает вакансии по критерию
    user_vacancy = input('Введите поисковый запрос:\n')
    vacancies = platform.get_vacancies(user_vacancy)
    if len(vacancies) == 0:
        print('Нет вакансий по вашему запросу')
        exit()

    # Пользователь фильтрует вакансии по требованиям
    filter_words = input("Введите ключевые слова для фильтрации вакансий:\n").lower().split()
    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    if len(sorted_vacancies) == 0:
        print('Нет вакансий по данному критерию для фильтра')
        exit()

    # Вакансии выводятся в топ N и сохраняются в JSON файл
    try:
        top_n = int(input("Введите количество вакансий для вывода в топ N:\n"))
    except ValueError:
        raise ValueError('"N" должно быть целым числом')

    top = get_top_vacancies(sorted_vacancies, top_n)
    for vacancy in top:
        JSONSaver().add_vacancy(vacancy)
        print(vacancy)


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
        if vacancy['salary']['to']:
            sorted_list.append(vacancy)
    return sorted(sorted_list, key=lambda d: d['salary']['to'], reverse=True)


def get_top_vacancies(vacancies_list, top_number):
    top_list = []
    for item in vacancies_list:
        vacancy = Vacancy(item['name'], item['alternate_url'], item['salary'], item['snippet']['requirement'])
        top_list.append(vacancy)
    return top_list[:top_number]
