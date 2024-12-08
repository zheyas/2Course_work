from abc import ABC, abstractmethod
import json
import os


class VacancyManager(ABC):
    """
    Абстрактный класс для управления вакансиями.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: dict):
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict) -> list:
        """Получает вакансии по указанным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: int):
        """Удаляет вакансию по ID."""
        pass


class JSONVacancyManager(VacancyManager):
    """
    Класс для работы с вакансиями в JSON-файле.
    """

    def __init__(self, filename: str):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)

    def _load_data(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def _save_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def add_vacancy(self, vacancy: dict):
        if 'id' not in vacancy:
            raise ValueError("Vacancy dictionary must contain 'id' key.")

        # Проверка на наличие зарплаты, если её нет - присваиваем 0
        if 'salary' not in vacancy or not vacancy['salary']:
            vacancy['salary'] = 0

        data = self._load_data()
        data.append(vacancy)
        self._save_data(data)

    def get_vacancies(self, criteria: dict) -> list:
        data = self._load_data()
        result = []
        for vacancy in data:
            if all(vacancy.get(key) == value for key, value in
                   criteria.items()):
                result.append(vacancy)
        return result

    def delete_vacancy(self, vacancy_id: int):
        data = self._load_data()
        data = [v for v in data if v.get('id') != vacancy_id]
        self._save_data(data)
