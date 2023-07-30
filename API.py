from abc import ABC, abstractmethod
import requests


class Jobs(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями
    """

    @abstractmethod
    def get_jobs(self, text, area, per_page, pages):
        pass


class HeadHunterJobs(Jobs):
    """
    Класс, наследующийся от абстрактного класса для работы с платформой hh.ru
    Получает данные о вакансиях через API
    """
    def transform_hh_data(self, job):
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

    def get_jobs(self, text: str, pages: int = 5):
        url = 'https://api.hh.ru/vacancies'
        transformed_jobs = []

        for page in range(pages):
            params = {
                'text': text,
                'page': page,
                'per_page': 100,  # количество вакансий на одной странице
                'area': 1  # поиск только по Москве
            }
            response = requests.get(url, params=params)
            jobs = response.json()
            for job in jobs['items']:
                transformed_jobs.append(self.transform_hh_data(job))

        return transformed_jobs




class SuperJobJobs(Jobs):
    """
     Класс, наследующиеся от абстрактного класса для работы с платформой SuperJob.ru
    Получает данные о вакансиях через API
    """

    def get_jobs(self, text: str, area='Москва', per_page=100, pages=5):
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': 'v3.r.137698933.9643b5a8b7a8a043dff47daec327b86d79edf077.2194580be8c204d329ef6204bd3a46983bf65886'
        }
        transformed_jobs = []

        for page in range(pages):
            params = {
                'keyword': text,
                'town': area,
                'count': per_page,
                'page': page
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                jobs = response.json()
                for job in jobs['objects']:
                    transformed_jobs.append(self.transform_superjob_data(job))

        return transformed_jobs

    def transform_superjob_data(self, job):
        return {
            'title': job.get('profession'),
            'salary_from': job.get('payment_from'),
            'salary_to': job.get('payment_to'),
            'link': job.get('link'),
            'description': job.get('candidat'),
            'id': job.get('id'),
        }


def sort_jobs_by_salary(self, jobs, order='desc'):
    return sorted(jobs, key=lambda x: (x['salary_from'] or 0, x['salary_to'] or 0), reverse=(order == 'desc'))

def top_jobs_by_salary(self, jobs, top_n=10, order='desc'):
    sorted_jobs = self.sort_jobs_by_salary(jobs, order)
    return sorted_jobs[:top_n]

