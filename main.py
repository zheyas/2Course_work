from src.hh import HH, Vacancy
from src.data import JSONVacancyManager
from pathlib import Path


def main():
    """
    Основная программа для взаимодействия с пользователем.
    """
    # Создаем путь к файлу с вакансиями относительно текущего скрипта
    file_path = Path(__file__).parent / "data" / "vacancies.json"
    file_worker =\
        JSONVacancyManager(file_path)  # Используем класс для работы с файлом
    hh_parser = HH(file_worker)

    while True:
        print("\nВыберите действие:")
        print("1. Запросить вакансии с hh.ru и сохранить в файл")
        print("2. Показать сохранённые вакансии")
        print("3. Получить топ N вакансий по зарплате")
        print("4. Фильтровать вакансии по ключевому слову в описании")
        print("5. Удалить вакансию по ID")
        print("0. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            keyword = input("Введите поисковый запрос: ")
            print("Загружаю вакансии с hh.ru...")
            hh_parser.load_vacancies(keyword)
            for index, vacancy in enumerate(hh_parser.vacancies, start=1):
                file_worker.add_vacancy({
                    "id": index,  # Добавляем уникальный id вакансии
                    "title": vacancy.title,
                    "link": vacancy.link,
                    "salary": vacancy.salary,
                    "description": vacancy.description,
                })
            print("Вакансии успешно загружены и сохранены в файл.")

        elif choice == "2":
            vacancies = file_worker.get_vacancies({})
            if vacancies:
                print("\nСохранённые вакансии:")
                for i, vacancy in enumerate(vacancies, start=1):
                    print(f"{i}. {vacancy['title']} - "
                          f"{vacancy['salary']} ({vacancy['link']})")
            else:
                print("Вакансии не найдены.")

        elif choice == "3":
            n = int(input("Введите количество топовых вакансий по зарплате: "))
            vacancies = file_worker.get_vacancies({})
            if vacancies:
                vacancies = [Vacancy(**vac) for vac in vacancies]
                top_vacancies = sorted(vacancies, reverse=True)[:n]
                print("\nТоп вакансий по зарплате:")
                for i, vacancy in enumerate(top_vacancies, start=1):
                    print(f"{i}. {vacancy.title} - "
                          f"{vacancy.salary} ({vacancy.link})")
            else:
                print("Вакансии не найдены.")

        elif choice == "4":

            keyword = input("Введите ключевое слово для фильтрации: ")

            vacancies = file_worker.get_vacancies({})

            filtered_vacancies = [

                vac for vac in vacancies

                if 'description' in vac and vac['description']
                   is not None and keyword.lower() in vac[
                    'description'].lower()

            ]

            if filtered_vacancies:

                print("\nВакансии с ключевым словом:")

                for i, vacancy in enumerate(filtered_vacancies,
                                            start=1):
                    print(f"{i}. {vacancy['title']} - "
                          f"{vacancy['salary']} ({vacancy['link']})")

            else:

                print("Вакансии с таким ключевым словом не найдены.")

        elif choice == "5":
            vacancy_id = int(input("Введите ID вакансии для удаления: "))
            file_worker.delete_vacancy(vacancy_id)
            print("Вакансия успешно удалена.")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
