import random
from django.core.management.base import BaseCommand
from faker import Faker
from Compaines.models import Company, Department, Employee, Address, Project, Task

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        

        for _ in range(5):
            company = Company.objects.create(
                company_name=fake.company(),
                company_description=fake.text(),
                company_website=fake.url()
            )


            Address.objects.create(
                company=company,
                street=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country()
            )


            for _ in range(3):
                department = Department.objects.create(
                    company=company,
                    department_name=fake.word()
                )


                for _ in range(10):
                    employee = Employee.objects.create(
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email(),
                        company=company,
                        department=department,
                        hire_date=fake.date_this_decade()
                    )


                    for _ in range(2):
                        project = Project.objects.create(
                            company=company,
                            name=fake.word(),
                            description=fake.text(),
                            start_date=fake.date_this_year(),
                            end_date=fake.date_this_year()
                        )
                        project.employees.add(employee)

                    for _ in range(5):
                        Task.objects.create(
                            employee=employee,
                            title=fake.word(),
                            description=fake.text(),
                            due_date=fake.date_this_year(),
                            completed=fake.boolean()
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
