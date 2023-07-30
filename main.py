from API import HeadHunterJobs, SuperJobJobs
from Vacancies import JsonJobStorage


def interact():
    """
    Главная функция для взаимодействия с пользователем
    """
    hh_api = HeadHunterJobs()
    sj_api = SuperJobJobs()
    job_storage = JsonJobStorage('jobs.json')

    while True:
        print("\nВыберите действие:")
        print("1. Получить вакансии")
        print("2. Просмотреть сохраненные вакансии")
        print("3. Удалить сохраненные вакансии")
        print("4. Выйти")
        choice = input("> ")

        if choice == '1':
            jobs = []

            print("\nВыберите платформу:")
            print("1. hh.ru")
            print("2. superjob.ru")
            platform_choice = input("> ")

            print("\nВведите поисковый запрос:")
            query = input("> ")

            if platform_choice == '1':
                jobs = hh_api.get_jobs(text=query)
            elif platform_choice == '2':
                jobs = sj_api.get_jobs(query)
            else:
                print("\nНеизвестная платформа. Пожалуйста, попробуйте снова.")
                continue

            job_storage.add_jobs(jobs)
            print(f"\nДобавлено {len(jobs)} вакансий.")

        elif choice == '2':
            print("\nВведите ключевое слово для фильтрации вакансий (или нажмите Enter, чтобы пропустить):")
            keyword = input("> ")
            jobs = job_storage.get_jobs_by_criteria({'title': keyword})

            if jobs:
                for job in jobs:
                    print(f"\nНазвание: {job['title']}")
                    if job['salary_from'] in [0, None] and job['salary_to'] in [0, None]:
                        print('Зарплата: не указана')
                    elif job['salary_from'] in [0, None]:
                        print(f"Зарплата: до {job['salary_to']}")
                    elif job['salary_to'] in [0, None]:
                        print(f"Зарплата: от {job['salary_from']}")
                    else:
                        print(f"Зарплата: от {job['salary_from']} до {job['salary_to']}")
                    print(f"Ссылка: {job['link']}")
                    print(f"Описание: {job['description']}")
                    print('-------------------------------------------------------------------------------------------')
            else:
                print("\nВакансий не найдено.")

        elif choice == '3':
            job_ids = [job['id'] for job in job_storage.get_jobs_by_criteria({})]
            job_storage.remove_jobs(job_ids)
            print("\nВсе вакансии удалены.")

        elif choice == '4':
            break


interact()
