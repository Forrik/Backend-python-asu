from django.contrib import admin

from .models import (AcademicDegree, AcademicTitle, Consultancy,
                     ConsultancyType, EducationBase, EducationForm,
                     EducationLevel, Graduation, Position, Speciality,
                     StudentGroup, StudentStatus, Ticket, TimeNorm, VkrHours)

admin.site.register(Position)
admin.site.register(Ticket)
admin.site.register(AcademicTitle)
admin.site.register(AcademicDegree)
admin.site.register(EducationBase)
admin.site.register(VkrHours)
admin.site.register(StudentStatus)
admin.site.register(ConsultancyType)
admin.site.register(Consultancy)
admin.site.register(EducationLevel)
admin.site.register(EducationForm)
admin.site.register(Graduation)
admin.site.register(Speciality)
admin.site.register(StudentGroup)
admin.site.register(TimeNorm)
