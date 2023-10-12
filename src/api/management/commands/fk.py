
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
        print('FFFFFFFFFFf')

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
        
        for degree in academic_degrees:
            academic_degree_items.append(models.AcademicDegree.objects.create(name=degree))

        for title in academic_titles:
            academic_titles_items.append(models.AcademicTitle.objects.create(name=title))
        
        for education_base in education_bases:
            education_bases_items.append(models.EducationBase.objects.create(name=education_base))

        for education_level in education_levels:
            education_levels_item.append(models.EducationLevel.objects.create(name=education_level))

        for education_form in education_forms:
            education_form_items.append(models.EducationForm.objects.create(name=education_form))

        for consultancy_type_general in consultancy_types_general:
            consultancy_type_general_items.append(models.ConsultancyType.objects.create(name=consultancy_type_general))
        
        for consultancy_type_main in consultancy_types_main:
            consultancy_type_main_item.append(models.ConsultancyType.objects.create(name=consultancy_type_main, is_main=True))
            
        
        for spec in specs:
            specs_items.append(
                models.Speciality.objects.create(
                    name=spec[0],
                    code=f"{random.randint(10,99)}.{random.randint(10,99)}.{random.randint(10,99)}",
                    abbreviation=spec[1],
                    education_level=random.choice(education_levels_item),
                ))

        for graduation in graduations:
            graduations_items.append(models.Graduation.objects.create(
                graduation_type=graduation[0],
                year=graduation[1]))

        for group in range(0, groups_count):
            groups_items.append(models.StudentGroup.objects.create(
                course=4,
                number=400+random.randint(1,9),
                speciality=random.choice(specs_items),
                education_form=random.choice(education_form_items),
                graduation=random.choice(graduations_items),
            ))

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

            for vkr_hour in vkr_hours:
                models.VkrHours.objects.create(
                    teacher=tchr,
                    hours=vkr_hour[0],
                    year=vkr_hour[1]
                )

            teachers_items.append(tchr)
            
        for speciality in specs_items:
            for cons_type in consultancy_type_general_items:
                for graduation in graduations_items:
                    time_norms_items.append(models.TimeNorm.objects.create(
                        hours=random.choice([1.0,1.5,2,2.5]),
                        speciality=speciality,
                        consultancy_type=cons_type,
                        graduation=graduation
                    ))
            
            for cons_type_main in consultancy_type_main_item:
                for graduation in graduations_items:
                    time_norms_items.append(models.TimeNorm.objects.create(
                        hours=random.choice([1.0,1.5,2,2.5]),
                        speciality=speciality,
                        consultancy_type=cons_type_main,
                        graduation=graduation
                    ))


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
        


        for student in students_items[:student_counts-20]:
            while True:
                try:
                    ticket_items.append(models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        message=fake.text(),
                        ticket_status=random.choice(tickets_statuses),
                    ))
                    break
                except:
                    pass


        for student in students_items[:student_counts-400]:
            while True:
                try:
                    ticket_items.append(models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        message=fake.text(),
                        ticket_status=TicketStatusEnum.ACCEPTED,
                    ))
                    break
                except:
                    pass
        
        for student in students_items[student_counts-400:student_counts-600]:
            while True:
                try:
                    ticket_items.append(models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        message=fake.text(),
                        ticket_status=TicketStatusEnum.NEW,
                    ))
                    break
                except:
                    pass
        for student in students_items[student_counts-600:]:
             while True:
                try:
                    ticket_items.append(models.Ticket.objects.create(
                        student=student,
                        teacher=random.choice(teachers_items),
                        message=fake.text(),
                        ticket_status=TicketStatusEnum.REJECTED,
                    ))
                    break
                except:
                    pass

        for student in students_items[:student_counts-20]:
            for cons_type in consultancy_type_general_items:
                if bool(random.getrandbits(1)):
                    while True:
                        try:
                            ticket_items.append(models.Consultancy.objects.create(
                                student=student,
                                teacher=random.choice(teachers_items),
                                consultancy_type=random.choice(consultancy_type_general_items),
                            ))
                            break
                        except:
                            pass
        
       