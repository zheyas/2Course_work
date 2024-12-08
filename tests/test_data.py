import os
import json
import pytest
from pathlib import Path
from src.data import JSONVacancyManager

@pytest.fixture
def manager():
    filename = Path(__file__).parent.parent / "data" / "vacancies.json"
    manager = JSONVacancyManager(filename)
    yield manager
    os.remove(filename)

def test_add_vacancy(manager):
    # Очистка существующих данных
    manager._save_data([])

    vacancy = {'id': 1, 'title': 'Test Vacancy', 'salary': 1000}
    manager.add_vacancy(vacancy)
    data = manager._load_data()

    assert len(data) == 1
    assert data[0] == vacancy


def test_add_vacancy_missing_id(manager):
    vacancy = {'title': 'Test Vacancy', 'salary': 1000}
    with pytest.raises(ValueError):
        manager.add_vacancy(vacancy)

def test_add_vacancy_missing_salary(manager):
    vacancy = {'id': 1, 'title': 'Test Vacancy'}
    manager.add_vacancy(vacancy)
    data = manager._load_data()
    assert data[0]['salary'] == 0

def test_get_vacancies(manager):
    vacancies = [
        {'id': 1, 'title': 'Test Vacancy 1', 'salary': 1000},
        {'id': 2, 'title': 'Test Vacancy 2', 'salary': 2000},
        {'id': 3, 'title': 'Test Vacancy 3', 'salary': 1500},
    ]
    for vacancy in vacancies:
        manager.add_vacancy(vacancy)

    criteria = {'salary': 1500}
    result = manager.get_vacancies(criteria)
    assert len(result) == 1
    assert result[0] == vacancies[2]

def test_delete_vacancy(manager):
    vacancies = [
        {'id': 1, 'title': 'Test Vacancy 1', 'salary': 1000},
        {'id': 2, 'title': 'Test Vacancy 2', 'salary': 2000},
    ]
    for vacancy in vacancies:
        manager.add_vacancy(vacancy)

    manager.delete_vacancy(1)
    data = manager._load_data()
    assert len(data) == 1
    assert data[0] == vacancies[1]
