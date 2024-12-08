import pytest
from unittest.mock import patch, Mock
from src.hh import HH, Vacancy


@pytest.fixture
def hh_instance():
    """Создает экземпляр класса HH."""
    return HH(file_worker=None)


def test_vacancy_comparison():
    """Тестируем сравнение вакансий."""
    vacancy1 = Vacancy(1, "Python Developer", "http://example.com/1", 150000, "Python experience required")
    vacancy2 = Vacancy(2, "Frontend Developer", "http://example.com/2", 120000, "React experience required")
    vacancy3 = Vacancy(3, "Data Scientist", "http://example.com/3", 180000, "Data analysis experience required")

    assert vacancy1 > vacancy2
    assert vacancy2 < vacancy3
    assert vacancy1 != vacancy3


def test_vacancy_salary_parsing():
    """Тестируем парсинг зарплаты в классе Vacancy."""
    vacancy = Vacancy(1, "Test Vacancy", "http://example.com", "От 100000 до 200000 RUB", "Description")
    assert vacancy._parse_salary_value(vacancy.salary) == 150000


@patch("src.hh.requests.get")
def test_hh_load_vacancies(mock_get, hh_instance):
    """Тестируем загрузку вакансий из API HH."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "id": "1",
                "name": "Python Developer",
                "alternate_url": "http://example.com/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
                "snippet": {"requirement": "Python experience required"}
            },
            {
                "id": "2",
                "name": "Frontend Developer",
                "alternate_url": "http://example.com/2",
                "salary": {"from": 120000, "to": 180000, "currency": "RUB"},
                "snippet": {"requirement": "React experience required"}
            }
        ]
    }
    mock_get.return_value = mock_response

    hh_instance.load_vacancies("developer")
    assert len(hh_instance.vacancies) == 2
    assert hh_instance.vacancies[0].title == "Python Developer"
    assert hh_instance.vacancies[0].salary == "От 100000 до 150000 RUB"


@patch("src.hh.requests.get")
def test_hh_api_error_handling(mock_get, hh_instance):
    """Тестируем обработку ошибок API HH."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    hh_instance.load_vacancies("developer")
    assert len(hh_instance.vacancies) == 0
