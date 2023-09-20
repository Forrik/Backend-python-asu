from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Role, Position, Ticket, AcademicTitle, AcademicDegree, EducationBase, EduForm, EduLevel, Graduation, StudStatus, WorkType, VkrHours, Consultancy, Speciality, StudentGroup, TimeNorm
from user.models import User
from rest_framework.validators import UniqueValidator
from api.constants import Role as RoleEnum
from api.constants import TicketStatusEnum





class RoleSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=Role.objects.all())])

    def create(self, validated_data):
        return Role.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    

    class Meta:
        model = Role
        fields = ('id', 'name')


class PositionSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=Position.objects.all())])

    def create(self, validated_data):
        return Position.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    

    class Meta:
        model = Position
        fields = ('id', 'name')

class ShortUserSerializer(serializers.ModelSerializer):



    class Meta:
        model = User
        fields = ('id', 'first_name','middle_name', 'last_name')



class TicketSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    dt_send = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=True)
    message = serializers.CharField(required=True, max_length=1024)
    ticketStatus = serializers.SerializerMethodField()
    teacher = ShortUserSerializer(required=True)
    student = ShortUserSerializer(required=True)
    dt_response = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)


    class Meta:
        model = Ticket
        fields = ('id', 'dt_send', 'message', 'ticketStatus', 'teacher', 'student', 'dt_response')

    def get_ticketStatus(self, obj):
        if obj.ticketStatus is None:
            return None

        return dict(id=TicketStatusEnum(obj.ticketStatus).value, name=TicketStatusEnum(obj.ticketStatus).descr)




class NewTicketSerializer(serializers.ModelSerializer):
    
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    message = serializers.CharField(required=True, max_length=1024)

    class Meta: 
        model = Ticket
        fields = ('message', 'teacher')

class AcademicTitleSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=AcademicTitle.objects.all())])
    abbreviation = serializers.CharField(validators=[UniqueValidator(queryset=AcademicTitle.objects.all())])

    class Meta:
        model = AcademicTitle
        fields = ('id', 'name', 'abbreviation')

class AcademicDegreeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=AcademicDegree.objects.all())])
    abbreviation = serializers.CharField(validators=[UniqueValidator(queryset=AcademicDegree.objects.all())])

    class Meta:
        model = AcademicDegree
        fields = ('id', 'name', 'abbreviation')


class EducationBaseSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=EducationBase.objects.all())])

    class Meta:
        model = EducationBase
        fields = ('id', 'name')

class EduFormSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=EduForm.objects.all())])

    class Meta:
        model = EduForm
        fields = ('id', 'name')

class EduLevelSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=EduLevel.objects.all())])

    class Meta:
        model = EduLevel
        fields = ('id', 'name')
    
class GraduationSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    typeGraduation = serializers.CharField(required=True)
    # typeGraduation = serializers.CharField(validators=[UniqueValidator(queryset=Graduation.objects.all())]) 
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Graduation
        fields = ('id', 'typeGraduation', 'year')

class StudStatusSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=StudStatus.objects.all())])

    class Meta:
        model = StudStatus
        fields = ('id', 'name')

class WorkTypeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(validators=[UniqueValidator(queryset=WorkType.objects.all())])

    class Meta:
        model = WorkType
        fields = ('id', 'name')

class  VkrHoursSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    year = serializers.IntegerField(required=True)
    hours = serializers.IntegerField(required=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = VkrHours
        fields = ('id', 'year', 'hours', 'user_id')

class ConsultancySerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    workType = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all(), required=True)
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    comment = serializers.CharField(required=True, max_length=1024)

    class Meta:
        model = Consultancy
        fields = ('id', 'workType', 'teacher', 'student', 'comment')

class SpecialitySerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    code = serializers.CharField(validators=[UniqueValidator(queryset=Speciality.objects.all())])
    name = serializers.CharField(validators=[UniqueValidator(queryset=Speciality.objects.all())])
    abbreviation = serializers.CharField(validators=[UniqueValidator(queryset=Speciality.objects.all())])
    edulevel = EduLevelSerializer(required=True)

    class Meta:
        model = Speciality
        fields = ('id', 'code', 'name', 'abbreviation', 'edulevel')

class SpecialityCreateSerializer(SpecialitySerializer):
    edulevel = serializers.PrimaryKeyRelatedField(queryset=EduLevel.objects.all(), required=True)
    

class StudentGroupSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    speciality_id = SpecialitySerializer(required=True)
    course = serializers.IntegerField(required=True)
    number = serializers.IntegerField(required=True)
    eduForm_id = EduFormSerializer(required=True)
    eduGraduation_id = serializers.PrimaryKeyRelatedField(queryset=Graduation.objects.all(), required=True)
    


    class Meta:
        model = StudentGroup
        fields = ('id', 'speciality_id', 'course', 'number', 'eduForm_id', 'eduGraduation_id')

class TimeNormSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    hours = serializers.IntegerField(required=True)
    speciality = SpecialitySerializer(required=True)
    workType = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all(), required=True)
    graduation_id = serializers.PrimaryKeyRelatedField(queryset=Graduation.objects.all(), required=True)



    class Meta:
        model = TimeNorm
        fields = ('id', 'hours', 'speciality', 'workType', 'graduation_id')    

class UserSerializer(serializers.ModelSerializer):

    position = PositionSerializer()
    studentGroup = StudentGroupSerializer()
    eduLevel = EduLevelSerializer()
    role = serializers.SerializerMethodField()
    educationBase = EducationBaseSerializer(required=False)
    academicTitle = AcademicTitleSerializer(required=False)
    academicDegree = AcademicDegreeSerializer(required=False)
    vkrHours = VkrHoursSerializer(required=False)
    teacher_groups = StudentGroupSerializer(many=True, source = 'teacherGroups')


    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'middle_name', 'last_name', 'position', 'number_student_book', 'studentGroup', 'studStatus', 'educationBase', 'speciality', 'role', 'academicTitle', 'academicDegree', 'eduLevel', 'vkrHours', 'teacher_groups')
        extra_kwargs = {'password': {'write_only': True}}

    def get_role(self, obj):
        if obj.role is None:
            return None

        return dict(id=RoleEnum(obj.role).value, name=RoleEnum(obj.role).descr)    

class UserProfileSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'middle_name', 'last_name', 'position', 'number_student_book', 'studentGroup', 'studStatus', 'educationBase', 'speciality','role', 'academicTitle', 'academicDegree', 'eduLevel', 'vkrHours')

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
      def validate(self, attrs):

        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data = dict(
            refresh = str(refresh),
            access = str(refresh.access_token),
            is_superuser = self.user.is_superuser,
            username = self.user.username,
            email = self.user.email,
            first_name = self.user.first_name,
            middle_name = self.user.middle_name,
            last_name = self.user.last_name,
            role_id = RoleEnum(self.user.role).value,
            role_name = RoleEnum(self.user.role).descr

        )

        return data

class StudentInGroupSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'role')

class GroupWithStudentSerializer(StudentGroupSerializer):
    student_group = StudentInGroupSerializer(many=True)

    class Meta:
        model = StudentGroup
        fields = ('id', 'speciality_id', 'course', 'number', 'eduForm_id', 'eduGraduation_id', 'student_group')

class UserGraduationSerializer(UserSerializer):
    teacherGroups = GroupWithStudentSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'position', 'role', 'teacherGroups')