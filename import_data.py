import os, django, csv
from phonenumber_field.phonenumber import PhoneNumber
import datetime

os.environ["DJANGO_SETTINGS_MODULE"] = "w3.settings"

django.setup()

from employee.models import *

#----------------------------- CSV TO DB IMPORTS ------------------------------------------

#------------------ PERSON DB IMPORT FROM CSV -----------------------------
# with open("C:\\Users\\nehor\Downloads\persons.csv", newline='') as csvfile:
#     csv_reader = csv.reader(csvfile)
#     headers = next(csv_reader)
#     for row in csv_reader:
#         date_birth = datetime.datetime.strptime(row[5], '%m/%d/%Y').strftime('%Y-%m-%d')
#         line = Person(id=row[0], first_name=row[1], last_name=row[2], personal_email=row[3], gender=row[4], birth_date=date_birth)
#         line.save()

#------------------ COMPANY DB IMPORT FROM CSV -----------------------------
# with open("C:\\Users\\nehor\Downloads\companies.csv", newline='', encoding="utf8") as csvfile:
#     csv_reader = csv.reader(csvfile)
#     headers = next(csv_reader)
#     for row in csv_reader:
#         line = Company(id=row[0], company_name=row[1], country=row[2], city=row[3], address=row[4], phone_num=row[5].replace("-",""))
#         line.save()

#------------------ EMPLOYEE DB IMPORT FROM CSV -----------------------------
# with open("C:\\Users\\nehor\Downloads\employees.csv", newline='') as csvfile:
#     csv_reader = csv.reader(csvfile)
#     headers = next(csv_reader)
#     for row in csv_reader:
#         line = Employee(id=row[0], person=Person(row[1]), company=Company(row[2]), job_title=row[3], is_current_job=row[4].capitalize(), company_email=row[5])
#         line.save()


def get_person_name_by_if(person_id: int) -> str:
    person = Person.objects.get(id=person_id)
    print(f"Person ID {person_id} full name is: {person.first_name} {person.last_name}")


def get_people_by_age(age: int) -> list[Person]:
    person = Person.objects.all()
    age = datetime.datetime.today().year - age
    person = person.filter(birth_date__iso_year=age)
    print(person)


def get_people_by_gender(gender: str) -> list[Person]:
    person = Person.objects.all()
    person = person.filter(gender__iexact=gender)
    print(person)


def get_companies_by_country(country: str) -> list[str]:
    company = Company.objects.all()
    company = company.filter(country__iexact=country).values_list('company_name')
    print(company)


def get_company_employees(company_id: int, current_only: bool) -> list[Person]:
    employee = Employee.objects.all()
    employee = employee.filter(company_id=company_id, is_current_job=current_only).values_list('person_id')
    persons = Person.objects.filter(id__in=employee)
    print(persons)


def get_person_jobs(person_id: int) -> list[dict[str, str]]:
    # employee = Employee.objects.get(person_id=person_id)
    person = Person.objects.get(id=person_id)
    # print(person.employee_set.all())
    companys_id = person.employee_set.all().values_list('company_id')
    employee_info = person.employee_set.all().values_list('job_title')
    companies = Company.objects.filter(id__in=companys_id).values_list('company_name')
    my_dict = dict(zip(companies,employee_info))
    print(my_dict)




if __name__ == '__main__':
    # get_person_name_by_if(5)
    # get_people_by_age(55)
    # get_people_by_gender("female")
    # get_companies_by_country("france")
    # get_company_employees(1, False)
    get_person_jobs(9)