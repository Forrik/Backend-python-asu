from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import CustomTokenObtainSerializer

from api.models import Role, Position, Ticket, AcademicTitle, AcademicDegree, EducationBase, EduForm, EduLevel, Graduation, StudStatus, WorkType, VkrHours, Consultancy, Speciality, StudentGroup, TimeNorm

from user.models import User

from api.serializers import UserSerializer, RoleSerializer, PositionSerializer, TicketSerializer, TicketSerializer, AcademicTitleSerializer, AcademicDegreeSerializer, EducationBaseSerializer, EduFormSerializer, EduLevelSerializer, GraduationSerializer, StudStatusSerializer, WorkTypeSerializer, VkrHoursSerializer, ConsultancySerializer, SpecialitySerializer, StudentGroupSerializer, TimeNormSerializer, SpecialityCreateSerializer, UserProfileSerializer, UserGraduationSerializer, NewTicketSerializer

from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsStudent

# from api.permission import IsStudent


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

    def get(self, request, graduation_id, *args, **kwargs):
        groups_for_graduation = StudentGroup.objects.filter(eduGraduation_id=graduation_id)
        queryset = User.objects.filter(teacherGroups__in=groups_for_graduation).distinct()
        serializer = UserGraduationSerializer(queryset, many=True)
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