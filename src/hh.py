from abc import ABC, abstractmethod
import requests


class Parser(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    @abstractmethod
    def __init__(self, file_worker):
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword, max_pages=1):
        self.params['text'] = keyword
        while self.params.get('page') < max_pages:
            response = requests.get(self.url,
                                    headers=self.headers, params=self.params)
            if response.status_code == 200:
                vacancies_data = response.json()['items']
                for vacancy_data in vacancies_data:
                    vacancy = Vacancy(
                        id=vacancy_data['id'],
                        title=vacancy_data['name'],
                        link=vacancy_data['alternate_url'],
                        salary=self._parse_salary(vacancy_data['salary']),
                        description=vacancy_data['snippet']['requirement']
                    )
                    self.vacancies.append(vacancy)
                self.params['page'] += 1
            else:
                print(f"Error: {response.status_code}")
                break

    def _parse_salary(self, salary_data):
        if salary_data is None:
            return 0
        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        if salary_from is None and salary_to is None:
            return 0
        elif salary_from is None:
            return f"До {salary_to} {salary_data['currency']}"
        elif salary_to is None:
            return f"От {salary_from} {salary_data['currency']}"
        else:
            return f"От {salary_from} до {salary_to} {salary_data['currency']}"


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, id, title, link, salary, description):
        self.id = id
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description

    def __repr__(self):
        return (f"Vacancy(id={self.id}, title='{self.title}',"
                f" link='{self.link}',"
                f" salary='{self.salary}', description='{self.description}')")

    def __eq__(self, other):
        if isinstance(other, Vacancy):
            return (self._parse_salary_value(self.salary) ==
                    self._parse_salary_value(other.salary))
        return False

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            return (self._parse_salary_value(self.salary) <
                    self._parse_salary_value(other.salary))
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            return (self._parse_salary_value(self.salary) >
                    self._parse_salary_value(other.salary))
        return NotImplemented

    def _parse_salary_value(self, salary):
        """
        Преобразует строку зарплаты в числовое значение.
        Если зарплата не указана, возвращает 0.
        """
        if salary in [None, "Зарплата не указана"]:
            return 0
        if isinstance(salary, int):  # Если зарплата уже число, возвращаем как есть
            return salary
        salary_parts = salary.split()
        if "От" in salary and "до" in salary:
            salary_from = int(salary_parts[1].replace(" ", ""))
            salary_to = int(salary_parts[3].replace(" ", ""))
            return (salary_from + salary_to) // 2
        elif "От" in salary:
            return int(salary_parts[1].replace(" ", ""))
        elif "До" in salary:
            return int(salary_parts[1].replace(" ", ""))
        return 0
