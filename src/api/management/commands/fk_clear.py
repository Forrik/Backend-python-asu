
from django.core.management import call_command
from django.core.management.base import BaseCommand
from api import models
from user.models import User

class Command(BaseCommand):
    help = 'Импорт базовых (общих) данных'

    def handle(self, *args, **options):
        

        models.Consultancy.objects.all().delete()
        models.ConsultancyType.objects.all().delete()
        models.EducationBase.objects.all().delete()
        models.EducationForm.objects.all().delete()
        models.EducationLevel.objects.all().delete()
        models.AcademicDegree.objects.all().delete()
        models.AcademicTitle.objects.all().delete()
        models.Graduation.objects.all().delete()
        models.Position.objects.all().delete()
        models.Speciality.objects.all().delete()
        models.StudentGroup.objects.all().delete()
        models.StudentStatus.objects.all().delete()
        models.Ticket.objects.all().delete()
        models.TimeNorm.objects.all().delete()
        models.VkrHours.objects.all().delete()
        User.objects.all().exclude(username='root').delete()
        
       