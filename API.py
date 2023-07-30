from abc import ABC, abstractmethod
import requests


def transform_hh_data(job):
    """
    Форматирование принимаемой информации через API (из файла job) в единый формат
    """
    salary = job.get('salary')
    return {
        'id': job.get('id'),
        'title': job.get('name'),
        'link': job.get('alternate_url'),
        'salary_from': salary.get('from') if salary else None,
        'salary_to': salary.get('to') if salary else None,
        'currency': salary.get('currency') if salary else None,
        'experience': job.get('experience'),
        'description': job.get('snippet')
    }


def transform_superjob_data(job):
    """
    Форматирование принимаемой информации через API (из файла job) в единый формат
    """
    transformed_job = {
        'title': job.get('profession'),
        'salary_from': job.get('payment_from'),
        'salary_to': job.get('payment_to'),
        'link': job.get('link'),
        'description': job.get('candidat'),
        'id': job.get('id'),
    }
    return transformed_job


class Jobs(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_jobs(self, text, area, per_page, page):
        pass


class HeadHunterJobs(Jobs):
    """
    Класс, наследующиеся от абстрактного класса для работы с платформой hh.ru
    Получает данные о вакансиях через API
    """

    def get_jobs(self, text, area='1', per_page='100', page='0'):
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': text,
            'area': area,
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            jobs = response.json()
            transformed_jobs = [transform_hh_data(job) for job in jobs['items']]
            return transformed_jobs
        else:
            return None


class SuperJobJobs(Jobs):
    """
     Класс, наследующиеся от абстрактного класса для работы с платформой SuperJob.ru
    Получает данные о вакансиях через API
    """

    def get_jobs(self, text, area='Москва', per_page=100, page=0):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': 'v3.r.137698933.9643b5a8b7a8a043dff47daec327b86d79edf077.2194580be8c204d329ef6204bd3a46983bf65886'
        }
        params = {
            'keyword': text,
            'town': area,
            'count': per_page,
            'page': page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            jobs = response.json()
            transformed_jobs = [transform_superjob_data(job) for job in jobs['objects']]
            return transformed_jobs
        else:
            return None
