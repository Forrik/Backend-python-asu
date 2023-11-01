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
from api.permission import (IsSpecialist, IsSpecialistOrTeacher, IsStudent, IsTeacher)

from api.serializers import (AcademicDegreeSerializer, AcademicTitleSerializer, ChangePasswordSerializer,
                             ConsultancySerializer, ConsultancyTypeSerializer,
                             CustomTokenObtainSerializer,
                             EducationBaseSerializer, EducationFormSerializer,
                             EducationLevelSerializer, GraduationSerializer,
                             NewTicketSerializer, PositionSerializer,
                             SpecialityCreateSerializer, SpecialitySerializer, TicketCreateSerializer,
                             StudentGroupSerializer, StudentStatusSerializer,
                             TicketSerializer, TimeNormSerializer,
                             UpdateTicketStatusSerializer,
                             UserCreateSerializer, UserPartialUpdateSerializer, UserProfileSerializer,
                             UserSerializer, UserWithOpenPasswordSerializer, VkrHoursSerializer, StudentGroupCreateSerializer, VkrHoursCreateSerializer, TimeNormCreateSerializer)
from user.models import User
from django.db import IntegrityError, connection
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class UserViewSet(viewsets.ModelViewSet):

    # permission_classes = [IsAuthenticated]
    def get_permissions(self):

        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsSpecialist, ]

        return super(UserViewSet, self).get_permissions()

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
        elif self.action == "partial_update":
            return UserPartialUpdateSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)  
        if serializer.is_valid():
            _password = serializer.validated_data.pop("password")

            user = User.objects.create(**serializer.validated_data)
            if _password:
                user.set_password(_password)
                user.save()

            return Response(UserCreateSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        _password = serializer.validated_data.pop("password")

        if _password:
            instance.set_password(_password)

        self.perform_update(serializer)

        return Response(serializer.data)

    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        serializer = UserPartialUpdateSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return self.update(request, *args, **kwargs)
        
class UsersForSpecialistViewSet(UserViewSet):
    serializer_class = UserWithOpenPasswordSerializer
    permission_classes = [IsSpecialist]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.check_password(serializer.validated_data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data.get("new_password"))
        user.save()

        return Response(UserSerializer(user).data)
    
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

    # def get_serializer_class(self):
    #     return TicketSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TicketCreateSerializer
        else:
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

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return VkrHoursCreateSerializer
        else:
            return VkrHoursSerializer    


class ConsultancyViewSet(viewsets.ModelViewSet):

    queryset = Consultancy.objects.all()
    serializer_class = ConsultancySerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student", "teacher", "consultancy_type"]




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

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["graduation"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudentGroupCreateSerializer
        else:
            return StudentGroupSerializer


class TimeNormViewSet(viewsets.ModelViewSet):

    queryset = TimeNorm.objects.all()
    serializer_class = TimeNormSerializer

    filterset_fields = ["graduation"]
    filter_backends = [DjangoFilterBackend]


    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TimeNormCreateSerializer
        else:
            return TimeNormSerializer   


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
        try:
            main_con_type = ConsultancyType.objects.filter(is_main=True).get()
            main_con_type_id = main_con_type.id
        except ObjectDoesNotExist:
            return Response(
                {"error": "Отсутствует тип консультации с флагом 'Основная'"},
                status=status.HTTP_404_NOT_FOUND
                )
        except MultipleObjectsReturned:
            return Response(
                {"error": "Задано несколько типов консультации с флагом 'Основная'. Требуется лишь один."},
                status=status.HTTP_400_BAD_REQUEST
                )

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

                _hours = tn_dict.get(f"{main_con_type_id}_{group.speciality.id}_{graduation_id}")
                if _hours is None:
                    err_text = (f"Не задана норма времени для специальности "
                                f"`{group.speciality}`,выпуска `{graduation_id}` "
                                f"и типа  консультации `{main_con_type}`")

                    return Response(
                        data={"error": err_text},
                        status=status.HTTP_404_NOT_FOUND
                    )

                student.hours = _hours
                group.hours += _hours
                teacher.hours_sum += _hours
            else:
                raise Exception("Такой студент уже есть в группе")
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

            _cons_hours = tn_dict[f"{consultancy.consultancy_type.id}_{group.speciality.id}_{graduation_id}"]
            if _cons_hours is None:
                err_text = (f"Не задана норма времени для специальности "
                            f"`{group.speciality}`,выпуска `{graduation_id}` "
                            f"и типа  консультации `{consultancy.consultancy_type}`")
                return Response(
                    data={"error": err_text},
                    status=status.HTTP_400
                )
            student.hours += _cons_hours
            
            group.hours += _cons_hours
            teacher.hours_sum += _cons_hours
        
        teachers_ids = [teacher.id for teacher in result]

        try:
            year = Graduation.objects.get(id=graduation_id).year
        except Graduation.DoesNotExist:
            return Response(data="graduation not found", status=status.HTTP_404_NOT_FOUND)
        vkr_hours = VkrHours.objects.filter(
            teacher__id__in=teachers_ids,
            year=year
        ).values_list("teacher__id", "hours", "id")

        vkr_hours_dict = {}
        for vrk_hour in vkr_hours:
            vkr_hours_dict[vrk_hour[0]] = (vrk_hour[1], vrk_hour[2])

        for teacher in result:
            try:
                teacher.vkr_hours = vkr_hours_dict[teacher.id]  # только для года соответсвующего заданному graduaition_id
            except KeyError:
                return Response(
                    data={"error":
                          f"Для преподавателя {teacher.get_abbreviation()} (id={teacher.id}) не задана норма часов для ВКР"
                          },
                    status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.TimeNormGraduationSerializer(result, many=True)

        return Response(serializer.data)


class GerStudentsByConsultancyView(APIView):
    permission_classes = [IsSpecialistOrTeacher]
    def get(self, request, group_id, *args, **kwargs):
        students = User.objects.filter(
            student_group__id=group_id,
        ).select_related("student_status")

        group = StudentGroup.objects.get(id=group_id)
        speciality = group.speciality
        graduation = group.graduation

        timenorms = TimeNorm.objects.filter(
            speciality=speciality,
            graduation=graduation,
        ).select_related("consultancy_type")

        tickets = Ticket.objects.filter(
            student__in=students,
            ticket_status=TicketStatusEnum.ACCEPTED.value,
        ).select_related("teacher", "student", "student__student_status")

        consultancy = Consultancy.objects.filter(
            student__in=students,
        ).select_related("teacher", "student", "student__student_status")

        res = []
        for tn in timenorms:
            cons_type = tn.consultancy_type

            res.append(cons_type)
            cons_type.hours = tn.hours
            cons_type.assigned = []
            cons_type.not_assigned = []

            if cons_type.is_main:
                cons_type.assigned = tickets
                tickets_students = set(tickets.values_list("student__id", flat=True))
                cons_type.not_assigned = students.exclude(id__in=tickets_students)

            else:
                cons_by_type = consultancy.filter(consultancy_type=cons_type)
                cons_type.assigned = cons_by_type
                cons_by_type_students = set(cons_by_type.values_list("student__id", flat=True))

                cons_type.not_assigned = students.exclude(id__in=cons_by_type_students)

        serializer = serializers.StudentsInGroupByConsultancySerializer(res, many=True)

        return Response(serializer.data)


class TicketCreateView(APIView):

    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = NewTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = Ticket.objects.create(
                student=request.user,
                teacher=serializer.validated_data["teacher"],
                comment=serializer.validated_data["comment"],
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
