from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import CustomTokenObtainSerializer

from api.models import Role, Position, Ticket, AcademicTitle, AcademicDegree, EducationBase, EduForm, EduLevel, Graduation, StudStatus, WorkType, VkrHours, Consultancy, Speciality, StudentGroup, TimeNorm

from user.models import User

from api.serializers import UserSerializer, RoleSerializer, PositionSerializer, TicketSerializer, TicketSerializer, AcademicTitleSerializer, AcademicDegreeSerializer, EducationBaseSerializer, EduFormSerializer, EduLevelSerializer, GraduationSerializer, StudStatusSerializer, WorkTypeSerializer, VkrHoursSerializer, ConsultancySerializer, SpecialitySerializer, StudentGroupSerializer, TimeNormSerializer, SpecialityCreateSerializer, UserProfileSerializer, NewTicketSerializer, UpdateTicketStatusSerializer

from api import serializers

from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsStudent, IsTeacher, IsSpecialist, IsSpecialistOrTeacher
from datetime import datetime
# from api.permission import IsStudent
from api.constants import Role as RoleEnum, TicketStatusEnum



class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["role"]

class GetSelfProfileView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)




class RoleViewSet(viewsets.ModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PositionViewSet(viewsets.ModelViewSet):

    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ticketStatus", "student", "teacher"]
    # serializer_class = TicketCreateSerializer

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


class EduFormViewSet(viewsets.ModelViewSet):

    queryset = EduForm.objects.all()
    serializer_class = EduFormSerializer


class EduLevelViewSet(viewsets.ModelViewSet):

    queryset = EduLevel.objects.all()
    serializer_class = EduLevelSerializer


class GraduationViewSet(viewsets.ModelViewSet):

    queryset = Graduation.objects.all()
    serializer_class = GraduationSerializer


class StudStatusViewSet(viewsets.ModelViewSet):

    queryset = StudStatus.objects.all()
    serializer_class = StudStatusSerializer


class WorkTypeViewSet(viewsets.ModelViewSet):

    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class VkrHoursViewSet(viewsets.ModelViewSet):

    queryset = VkrHours.objects.all()
    serializer_class = VkrHoursSerializer


class ConsultancyViewSet(viewsets.ModelViewSet):

    queryset = Consultancy.objects.all()
    serializer_class = ConsultancySerializer


class SpecialityViewSet(viewsets.ModelViewSet):

    queryset = Speciality.objects.all()

    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SpecialityCreateSerializer
        else:
            return SpecialitySerializer


class StudentGroupViewSet(viewsets.ModelViewSet):

    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class TimeNormViewSet(viewsets.ModelViewSet):

    queryset = TimeNorm.objects.all()
    serializer_class = TimeNormSerializer


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

class UserGraduationView(APIView):

    def _get_hours_for_student(self, time_norms_qs, spec_id):
        qs = time_norms_qs.filter(speciality=spec_id)
        hours = 0
        for item in qs:
            hours += item.hours
        return hours

    def get(self, request, graduation_id, *args, **kwargs):
        tickets_qs = Ticket.objects.filter(
            student__studentGroup__eduGraduation_id=graduation_id,
            ticketStatus=TicketStatusEnum.ACCEPTED.value
        ).select_related('student__studentGroup')

        spec_ids = tickets_qs.values_list('student__studentGroup__speciality_id__id', flat=True)

        time_norms = TimeNorm.objects\
        .filter(graduation_id=graduation_id, speciality__id__in=set(spec_ids))

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

            group = ticket.student.studentGroup
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
                student.hours = self._get_hours_for_student(time_norms, group.speciality_id)
                group.hours += student.hours
                teacher.hours_sum += student.hours

        serializer = serializers.TimeNormGraduationSerializer(result, many=True)
        return Response(serializer.data)

class TicketCreateView(APIView):

    permission_classes = [IsStudent]
    def post(self, request, *args, **kwargs):
        serializer = NewTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        is_ticket_already_exist = Ticket.objects.filter(student=request.user, teacher__id=serializer.validated_data['teacher'].id).exists()
        print(is_ticket_already_exist)
        if is_ticket_already_exist:
            return Response({"error": "Ticket already exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ticket = Ticket.objects.create(student=request.user, teacher=serializer.validated_data['teacher'], message=serializer.validated_data['message'])
            


        return Response(serializer.data)

class TicketStatusUpdate(APIView):
    permission_classes = [IsSpecialistOrTeacher]

    def post(self, request, ticket_id, *args, **kwargs):
        serializer = UpdateTicketStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role == RoleEnum.TEACHER.value:


            if ticket.teacher != request.user:
                return Response({"error": "Wrong ticket"}, status=status.HTTP_403_FORBIDDEN)

            ticket.ticketStatus = serializer.validated_data['ticketStatus']
            ticket.dt_response = datetime.now()
            ticket.save()
        elif request.user.role == RoleEnum.SPECIALIST.value:
            ticket.ticketStatus = serializer.validated_data['ticketStatus']
            ticket.dt_response = datetime.now()
            ticket.save()
        else:
            return Response({"error": "Role should be teacher or specialist"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data)