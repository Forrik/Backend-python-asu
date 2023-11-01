
import random
from django.core.management import call_command
from django.core.management.base import BaseCommand
from faker import Faker
from api import models
from api.constants import Role, TicketStatusEnum

from user.models import User
fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Импорт базовых (общих) данных'

    def handle(self, *args, **options):

        positions_names = ['Старший преподователь', 'Преподаватель', 'Ассистент']
        academic_degrees = ['Кандидат наук', 'Доктор наук'] #Ученая степень
        academic_titles = ['Доцент', 'Профессор']
        education_bases = ['Бюджет', 'Договор', 'Целевая квота']
        consultancy_types_general = [ 'Руководство ВКР', 'Информационная безопасность' 'Нормоконтроль', 'Экономическая часть']
        consultancy_types_main = ['Основная часть',]
        education_forms = ['Очная', 'Заочная']
        education_levels = ['Бакалавр','Магистр','Специалист']
        specs = [
            ('Информатика и вычислительная техника', 'ИВТ'), 
            ('Прикладная информатика', 'ПИ'),
            ('Эксплуатация автоматизированных систем', 'ЭАС'),
            ('Информационные системы', 'ИС'),
            ('Информационная безопасность', 'ИБ')
            ]
        positions_items = []
        graduations_items = []
        specs_items = []
        groups_items = []
        students_items = []
        teachers_items = []
        specialists_items = []
        academic_degree_items = []
        academic_titles_items = []
        education_bases_items = []
        education_levels_item = []
        teacher_counts = 50
        student_counts = 1000
        specialist_counts = 5
        tickets_statuses = [TicketStatusEnum.NEW.value, TicketStatusEnum.ACCEPTED.value, TicketStatusEnum.REJECTED.value]
        ticket_items = []
        consultancy_items = []
        education_form_items = []
        consultancy_type_general_items = []
        consultancy_type_main_item = []
        time_norms_items = []
        groups_count = 15
        graduations = [('Зима',2024), ('Лето',2024)]
        vkr_hours = [(600, 2022),(600, 2023),(600, 2024)]

        for position in positions_names:
            positions_items.append(models.Position.objects.create(name=position))
        print('positions: OK')
        
        for degree in academic_degrees:
            academic_degree_items.append(models.AcademicDegree.objects.create(name=degree))
        print('academic_degrees: OK')

        for title in academic_titles:
            academic_titles_items.append(models.AcademicTitle.objects.create(name=title))
        print('academic_titles: OK')

        for education_base in education_bases:
            education_bases_items.append(models.EducationBase.objects.create(name=education_base))
        print('education_bases: OK')

        for education_level in education_levels:
            education_levels_item.append(models.EducationLevel.objects.create(name=education_level))
        print('education_levels: OK')

        for education_form in education_forms:
            education_form_items.append(models.EducationForm.objects.create(name=education_form))
        print('education_forms: OK')

        for consultancy_type_general in consultancy_types_general:
            consultancy_type_general_items.append(models.ConsultancyType.objects.create(name=consultancy_type_general))
        print('consultancy_types: OK')

        for consultancy_type_main in consultancy_types_main:
            consultancy_type_main_item.append(models.ConsultancyType.objects.create(name=consultancy_type_main, is_main=True))
        print('consultancy_type_main: OK')   
        
        for spec in specs:
            while 1:
                try:
                    item = models.Speciality.objects.create(
                            name=spec[0],
                            code=f"{random.randint(10,99)}.{random.randint(10,99)}.{random.randint(10,99)}",
                            abbreviation=spec[1],
                            education_level=random.choice(education_levels_item),
                        )
                    specs_items.append(item)
                    print(f"speciality created: {item.name}")
                    break
                except:
                    pass

            print("specs: OK")

        for graduation in graduations:
            while 1:
                try:
                    graduations_items.append(models.Graduation.objects.create(
                        graduation_type=graduation[0],
                        year=graduation[1]))
                    print(f"graduation created: {graduation[1]}")
                    break
                except:
                    pass
        print("graduations: OK")               

        for group in range(0, groups_count):
            while 1:
                try:
                    item = models.StudentGroup.objects.create(
                        course=4,
                        number=400+random.randint(1,9),
                        speciality=random.choice(specs_items),
                        education_form=random.choice(education_form_items),
                        graduation=random.choice(graduations_items),
                    )
                    groups_items.append(item)
                    print(f"group created: {item}")
                    break
                except Exception:
                    pass
        print("groups: OK")

        for teacher_idx in range(0, teacher_counts):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            tchr = User.objects.create_user(
                first_name=fake.first_name(),
                last_name= fake.last_name(),   #
                middle_name=fake.middle_name(),
                username=username,
                password=username,
                email=fake.email(),
                position=fake.random_element(positions_items),
                role=Role.TEACHER.value,
                academic_degree=fake.random_element(academic_degree_items),
                academic_title=fake.random_element(academic_titles_items),

            )
            print(f"teacher created: {tchr}")

            for vkr_hour in vkr_hours:
                models.VkrHours.objects.create(
                    teacher=tchr,
                    hours=vkr_hour[0],
                    year=vkr_hour[1]
                )

            teachers_items.append(tchr)
        
        print(f"teachers: OK")
        for speciality in specs_items:
            for cons_type in consultancy_type_general_items:
                for graduation in graduations_items:
                    item = models.TimeNorm.objects.create(
                        hours=random.choice([1.0,1.5,2,2.5]),
                        speciality=speciality,
                        consultancy_type=cons_type,
                        graduation=graduation
                    )
                    time_norms_items.append(item)
                    print(f"time_norm created: {item}")
            
            for cons_type_main in consultancy_type_main_item:
                for graduation in graduations_items:
                    item = models.TimeNorm.objects.create(
                        hours=random.choice([1.0,1.5,2,2.5]),
                        speciality=speciality,
                        consultancy_type=cons_type_main,
                        graduation=graduation
                    )
                    time_norms_items.append(item)
                    print(f"time_norm created: {item}")
        print("time_norms: OK")


        for _ in range(0, student_counts):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            stdnt = User.objects.create_user(
                first_name=fake.first_name(),
                last_name= fake.last_name(),
                middle_name=fake.middle_name(),
                username=username,
                password=username,
                email=fake.email(),
                role=Role.STUDENT.value,
                student_group=fake.random_element(groups_items),
                number_student_book=random.randint(100000,200000),
                education_base=fake.random_element(education_bases_items),
                speciality=fake.random_element(specs_items)
            )

            students_items.append(stdnt)
            print(f"student created: {stdnt}")
        print("students: OK")

        for _ in range(0, specialist_counts):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            specialist = User.objects.create_user(
                first_name=fake.first_name(),
                last_name= fake.last_name(),
                middle_name=fake.middle_name(),
                username=username,
                password=username,
                email=fake.email(),
                role=Role.SPECIALIST.value,
            )

            specialists_items.append(specialist)
            print(f"specialist created: {specialist}")
        print("specialists: OK")


        for student in students_items[:student_counts-20]:
            while True:
                try:
                    item = models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        comment=fake.text(),
                        ticket_status=random.choice(tickets_statuses),
                    )
                    ticket_items.append(item)
                    print(f"NEW ticket created: {item}")
                    break
                except Exception as exc:
                    print(exc)
                    continue

        print("tickets NEW: OK")

        for student in students_items[:student_counts-400]:
            while True:
                try:
                    item = models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        comment=fake.text(),
                        ticket_status=TicketStatusEnum.ACCEPTED,
                    )
                    ticket_items.append(item)
                    print(f"ACCEPTED ticket created: {item}")
                    break
                except Exception as exc:
                    print(exc)
                    continue
        print("tickets ACCEPTED: OK")
        
        for student in students_items[student_counts-400:student_counts-600]:
            while True:
                try:
                    item = models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        comment=fake.text(),
                        ticket_status=TicketStatusEnum.NEW,
                    )
                    ticket_items.append(item)
                    print(f"NEW ticket created: {item}")
                    break
                except:
                    continue
        print("tickets NEW: OK")

        for student in students_items[student_counts-600:]:
             while True:
                try:
                    item = models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        comment=fake.text(),
                        ticket_status=TicketStatusEnum.REJECTED,
                    )
                    ticket_items.append(item)
                    print(f"REJECTED ticket created: {item}")
                    break
                except Exception as exc:
                    print(exc)
                    continue
        print("tickets REJECTED: OK")

        for student in students_items[:student_counts-20]:
            for cons_type in consultancy_type_general_items:
                if bool(random.getrandbits(1)):
                    while True:
                        try:
                            item = models.Consultancy.objects.create(
                                student=student,
                                teacher=random.choice(teachers_items),
                                consultancy_type=random.choice(consultancy_type_general_items),
                                comment=fake.text(),
                            )
                            ticket_items.append(item)
                            print(f"CONSULTANCY created: {item}")
                            break
                        except Exception as exc:
                            print(exc)
                            continue
        print("consultancies: OK")

        print("FINISH")
        
       