from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import CustomTokenObtainSerializer

from api.models import Role, Position, TicketStatus, Ticket, AcademicTitle, AcademicDegree, EducationBase, EduForm, EduLevel, Graduation, StudStatus, WorkType, VkrHours, Consultancy, Speciality, StudentGroup, TimeNorm

from user.models import User

from api.serializers import UserSerializer, RoleSerializer, PositionSerializer, TicketStatusSerializer, TicketCreateSerializer, TicketSerializer, AcademicTitleSerializer, AcademicDegreeSerializer, EducationBaseSerializer, EduFormSerializer, EduLevelSerializer, GraduationSerializer, StudStatusSerializer, WorkTypeSerializer, VkrHoursSerializer, ConsultancySerializer, SpecialitySerializer, StudentGroupSerializer, TimeNormSerializer

from api.permission import IsStudent


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IsStudent]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PositionViewSet(viewsets.ModelViewSet):

    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TicketStatusViewSet(viewsets.ModelViewSet):

    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer


class TicketSerializerViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all()
    # serializer_class = TicketCreateSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
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
    serializer_class = SpecialitySerializer


class StudentGroupViewSet(viewsets.ModelViewSet):

    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class TimeNormViewSet(viewsets.ModelViewSet):

    queryset = TimeNorm.objects.all()
    serializer_class = TimeNormSerializer


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
