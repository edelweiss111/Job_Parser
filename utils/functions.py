from utils.API_classes import *
from utils.Save_classes import JSONSaver

platforms = ["HeadHunter", "SuperJob"]


def main():
    try:
        while True:
            '''Функция интерфейса пользователя'''
            # Пользователь выбирает платформу
            user_input = input('Введите название платформы. Если захотите выйти введите "exit"\n').lower()
            user_vacancy = input('Введите поисковый запрос:\n')
            if user_input == platforms[0].lower():
                hh_vacancies = HeadHunterAPI(user_vacancy).get_vacancies()
                if len(hh_vacancies) == 0:
                    print('Нет вакансий по вашему запросу')
                    continue
                vacancies = get_from_headhunter(hh_vacancies)
                break
            elif user_input == platforms[1].lower():
                sj_vacancies = SuperJobAPI(user_vacancy).get_vacancies()
                if len(sj_vacancies) == 0:
                    print('Нет вакансий по вашему запросу')
                    continue
                vacancies = get_from_superjob(sj_vacancies)
                break
            elif user_input.lower() == 'exit':
                exit()
            else:
                print('Такой платформы нет в базе')

        while True:
            # Пользователь фильтрует вакансии по требованиям
            filter_words = input("Введите ключевые слова для фильтрации вакансий:\n").lower().split()
            filtered_vacancies = filter_vacancies(vacancies, filter_words)
            sorted_vacancies = sort_vacancies(filtered_vacancies)
            if len(sorted_vacancies) == 0:
                print('Нет вакансий по данным критериям, введите другие критерии или "exit" для выхода')
            elif filter_words == 'exit':
                exit()
            else:
                break

        # Вакансии выводятся в топ N и сохраняются в JSON файл
        while True:
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N.\n"))
            except ValueError:
                print('"N" должно быть целым числом')
                continue
            else:
                top = get_top_vacancies(sorted_vacancies, top_n)
                for vacancy in top:
                    JSONSaver().add_vacancy(vacancy)
                    print(vacancy)
                break

    except Exception as e:
        raise e


def filter_vacancies(vacancies, filter_words):
    """Функция для фильтрации вакансий по критериям"""
    filtered_list = []
    for vacancy in vacancies:
        for word in filter_words:
            if word in vacancy.requirement.lower().split():
                filtered_list.append(vacancy)
    return filtered_list


def sort_vacancies(vacancies):
    """Функция для сортировки вакансий по зарплате"""
    return sorted(vacancies)


def get_top_vacancies(vacancies_list, top_number):
    top_list = []
    for vacancy in vacancies_list:
        top_list.append(vacancy)
    return top_list[:top_number]


def get_from_headhunter(vacancies):
    vacancies_list = []
    for item in vacancies:
        if item['salary']['to']:
            if item['salary']['currency'] == 'RUR':
                vacancy = Vacancy(item['name'], item['alternate_url'], item['salary']['to'],
                                  item['snippet']['requirement'])
                vacancies_list.append(vacancy)
    return vacancies_list


def get_from_superjob(vacancies):
    vacancies_list = []
    for item in vacancies:
        if item['payment_to']:
            if item['currency'] == 'rub':
                vacancy = Vacancy(item['profession'], item['link'], item['payment_to'],
                                  item['vacancyRichText'])
                vacancies_list.append(vacancy)
    return vacancies_list
