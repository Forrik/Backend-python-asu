from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api import serializers
# from api.permission import IsStudent
from api.constants import Role as RoleEnum
from api.constants import TicketStatusEnum
from api.models import (AcademicDegree, AcademicTitle, Consultancy,
                        ConsultancyType, EducationBase, EducationForm,
                        EducationLevel, Graduation, Position, Speciality,
                        StudentGroup, StudentStatus, Ticket, TimeNorm,
                        VkrHours)
from api.permission import (IsSpecialist, IsSpecialistOrTeacher, IsStudent,
                            IsTeacher)
from api.serializers import (AcademicDegreeSerializer, AcademicTitleSerializer,
                             ConsultancySerializer, ConsultancyTypeSerializer,
                             CustomTokenObtainSerializer,
                             EducationBaseSerializer, EducationFormSerializer,
                             EducationLevelSerializer, GraduationSerializer,
                             NewTicketSerializer, PositionSerializer,
                             SpecialityCreateSerializer, SpecialitySerializer,
                             StudentGroupSerializer, StudentStatusSerializer,
                             TicketSerializer, TimeNormSerializer,
                             UpdateTicketStatusSerializer,
                             UserCreateSerializer, UserProfileSerializer,
                             UserSerializer, VkrHoursSerializer, StudentGroupCreateSerializer)
from user.models import User
from django.db import connection
from django.db.models import Prefetch


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = User.objects.select_related(
        "student_group",
        "student_group__speciality",
        "student_group__education_form",
        "student_group__graduation",
        "position",
        "academic_title",
        "academic_degree",
        "education_base",
        "education_level",
        ).all()
    serializer_class = UserSerializer
    filterset_fields = ["role", "student_group"]
    filter_backends = [DjangoFilterBackend]

    search_fields = ["first_name", "last_name"]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return UserCreateSerializer
        else:
            return UserSerializer


class GetSelfProfileView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class PositionViewSet(viewsets.ModelViewSet):

    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ticket_status", "student", "teacher"]

    def get_serializer_class(self):
        return TicketSerializer


class AcademicTitleViewSet(viewsets.ModelViewSet):

    queryset = AcademicTitle.objects.all()
    serializer_class = AcademicTitleSerializer


class AcademicDegreeViewSet(viewsets.ModelViewSet):

    queryset = AcademicDegree.objects.all()
    serializer_class = AcademicDegreeSerializer


class EducationBaseViewSet(viewsets.ModelViewSet):

    queryset = EducationBase.objects.all()
    serializer_class = EducationBaseSerializer


class EducationFormViewSet(viewsets.ModelViewSet):

    queryset = EducationForm.objects.all()
    serializer_class = EducationFormSerializer


class EducationLevelViewSet(viewsets.ModelViewSet):

    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class GraduationViewSet(viewsets.ModelViewSet):

    queryset = Graduation.objects.all()
    serializer_class = GraduationSerializer


class StudentStatusViewSet(viewsets.ModelViewSet):

    queryset = StudentStatus.objects.all()
    serializer_class = StudentStatusSerializer


class ConsultancyTypeViewSet(viewsets.ModelViewSet):

    queryset = ConsultancyType.objects.all()
    serializer_class = ConsultancyTypeSerializer


class VkrHoursViewSet(viewsets.ModelViewSet):

    queryset = VkrHours.objects.all()
    serializer_class = VkrHoursSerializer


class ConsultancyViewSet(viewsets.ModelViewSet):

    queryset = Consultancy.objects.all()
    serializer_class = ConsultancySerializer


class SpecialityViewSet(viewsets.ModelViewSet):

    queryset = Speciality.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return SpecialityCreateSerializer
        else:
            return SpecialitySerializer


class StudentGroupViewSet(viewsets.ModelViewSet):

    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return StudentGroupCreateSerializer
        else:
            return StudentGroupSerializer


class TimeNormViewSet(viewsets.ModelViewSet):

    queryset = TimeNorm.objects.all()
    serializer_class = TimeNormSerializer


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class UserGraduationView(APIView):

    def get(self, request, graduation_id, *args, **kwargs):

        
        tickets_qs = Ticket.objects.filter(
            student__student_group__graduation=graduation_id,
            ticket_status=TicketStatusEnum.ACCEPTED.value,
        ).select_related(
            "teacher",
            "student__student_group__speciality"
            )
        main_con_type = ConsultancyType.objects.filter(is_main=True).first().id
                

        cons_qs = Consultancy.objects.filter(
            student__student_group__graduation=graduation_id,
        ).select_related(
            "teacher",
            "student__student_group__speciality",
            "consultancy_type")

        spec_ids = set(tickets_qs.values_list(
            "student__student_group__speciality__id", flat=True
        ).union(cons_qs.values_list("student__student_group__speciality__id", flat=True)))
        

        timenorms = TimeNorm.objects.filter(
            speciality__id__in=spec_ids
        ).values(
            "consultancy_type",
            "speciality",
            "graduation",
            "hours")

        tn_dict = {}
        for tn in timenorms:
            tn_dict[f"{tn['consultancy_type']}_{tn['speciality']}_{tn['graduation']}"] = tn['hours']

        result = []
        for ticket in tickets_qs:
            
            teacher = ticket.teacher

            if teacher not in result:
                result.append(teacher)
                teacher.hours_sum = 0
                teacher.groups_set = []
            else:
                teacher_idx = result.index(teacher)
                teacher = result[teacher_idx]
            
            group = ticket.student.student_group

            if group not in teacher.groups_set:
                teacher.groups_set.append(group)
                group.hours = 0
                group.students = []
            else:
                group_idx = teacher.groups_set.index(group)
                group = teacher.groups_set[group_idx]

            student = ticket.student
            if student not in group.students:
                group.students.append(student)
                student.hours = tn_dict[f"{main_con_type}_{group.speciality.id}_{graduation_id}"]
                group.hours += student.hours
                teacher.hours_sum += student.hours

        for consultancy in cons_qs:
            teacher = consultancy.teacher
            if teacher not in result:
                result.append(teacher)
                teacher.hours_sum = 0
                teacher.groups_set = []
            else:
                teacher_idx = result.index(teacher)
                teacher = result[teacher_idx]

            group = consultancy.student.student_group
            if group not in teacher.groups_set:
                teacher.groups_set.append(group)
                group.hours = 0
                group.students = []
            else:
                group_idx = teacher.groups_set.index(group)
                group = teacher.groups_set[group_idx]

            student = consultancy.student
            if student not in group.students:
                group.students.append(student)
                student.hours = 0
                
            else:
                student_idx = group.students.index(student)
                student = group.students[student_idx]
            student.hours += tn_dict[f"{consultancy.consultancy_type.id}_{group.speciality.id}_{graduation_id}"]

            group.hours += student.hours
            teacher.hours_sum += student.hours
        
        teachers_ids = [teacher.id for teacher in result]

        try:
            year = Graduation.objects.get(id=graduation_id).year
        except Graduation.DoesNotExist:
            return Response(data="graduation not found", status=status.HTTP_404_NOT_FOUND)
        vkr_hours = VkrHours.objects.filter(
            teacher__id__in=teachers_ids,
            year=year
        ).values_list("teacher__id", "hours")

        vkr_hours_dict = {}
        for vrk_hour in vkr_hours:
            vkr_hours_dict[vrk_hour[0]] = vrk_hour[1]

        for teacher in result:
            teacher.vkr_hours = vkr_hours_dict[teacher.id]  # только для года соответсвующего заданному graduaition_id

    
        print(vkr_hours_dict)
        serializer = serializers.TimeNormGraduationSerializer(result, many=True)
        print(len(connection.queries))
        return Response(serializer.data)


class TicketCreateView(APIView):

    permission_classes = [IsStudent]

    def post(self, request, *args, **kwargs):
        serializer = NewTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        is_ticket_already_exist = Ticket.objects.filter(
            student=request.user, teacher__id=serializer.validated_data["teacher"].id
        ).exists()
        print(is_ticket_already_exist)
        if is_ticket_already_exist:
            return Response(
                {"error": "Ticket already exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            ticket = Ticket.objects.create(
                student=request.user,
                teacher=serializer.validated_data["teacher"],
                message=serializer.validated_data["message"],
            )

        return Response(serializer.data)


class TicketStatusUpdate(APIView):
    permission_classes = [IsSpecialistOrTeacher]

    def post(self, request, ticket_id, *args, **kwargs):
        serializer = UpdateTicketStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.role == RoleEnum.TEACHER.value:

            if ticket.teacher != request.user:
                return Response(
                    {"error": "Wrong ticket"}, status=status.HTTP_403_FORBIDDEN
                )

            ticket.ticket_status = serializer.validated_data["ticket_status"]
            ticket.dt_response = datetime.now()
            ticket.save()
        elif request.user.role == RoleEnum.SPECIALIST.value:
            ticket.ticket_status = serializer.validated_data["ticket_status"]
            ticket.dt_response = datetime.now()
            ticket.save()
        else:
            return Response(
                {"error": "Role should be teacher or specialist"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(serializer.data)
