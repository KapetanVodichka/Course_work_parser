from abc import ABC, abstractmethod
import json


class JobStorage(ABC):
    """
    абстрактный класс для работы с вакансиями
    """
    @abstractmethod
    def add_jobs(self, jobs):
        pass

    @abstractmethod
    def get_jobs_by_criteria(self, criteria):
        pass

    @abstractmethod
    def remove_jobs(self, job_ids):
        pass


class JsonJobStorage(JobStorage):
    """
    Класс для добавления вакансий в файл, удаления и выделения вакансий по критериям
    """
    def __init__(self, filename):
        self.filename = filename

    def add_jobs(self, jobs):
        """
        Добавление вакансий в файл
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.extend(jobs)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_jobs_by_criteria(self, criteria):
        """
        Выборка вакансий по ключевым словам
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return [job for job in data if self.matches_criteria(job, criteria)]

    def remove_jobs(self, job_ids):
        """
        Удаление вакансий из файла
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        data = [job for job in data if job['id'] not in job_ids]

        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def matches_criteria(self, job, criteria):
        for key, value in criteria.items():
            if value not in job.get(key, ''):
                return False
        return True


class Job:
    def __init__(self, title, url, salary, description):
        if not title or not url or not description or (salary and salary < 0):
            raise ValueError("Некорректные данные")

        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

    def __lt__(self, other):
        if not isinstance(other, Job):
            return NotImplemented
        if self.salary is None:
            return True
        if other.salary is None:
            return False
        return self.salary < other.salary

    def __eq__(self, other):
        return self.salary == other.salary
