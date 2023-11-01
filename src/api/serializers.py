from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.constants import Role as RoleEnum
from api.constants import TicketStatusEnum, StudentStatusEnum
from api.models import (AcademicDegree, AcademicTitle, Consultancy,
                        ConsultancyType, EducationBase, EducationForm,
                        EducationLevel, Graduation, Position, Speciality,
                        StudentGroup, StudentStatus, Ticket, TimeNorm,
                        VkrHours)
from user.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField()

    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "position",
            "role",
            "academic_title",
            "academic_degree",
            "number_student_book",
            "student_status",
            "education_base",
            "student_group"
        )
        extra_kwargs = {"password": {"write_only": True}}

class UserPartialUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    role = serializers.IntegerField(required=False)
    

    class Meta:
            model = User
            fields = (
                "id",
                "username",
                "password",
                "first_name",
                "middle_name",
                "last_name",
                "position",
                "role",
                "academic_title",
                "academic_degree",
                "number_student_book",
                "student_status",
            )
            extra_kwargs = {"password": {"write_only": True}}

class PositionSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Position.objects.all())]
    )

    def create(self, validated_data):
        return Position.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

    class Meta:
        model = Position
        fields = ("id", "name")


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name")


class NewTicketSerializer(serializers.ModelSerializer):

    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    comment = serializers.CharField(required=True, max_length=1024)

    class Meta:
        model = Ticket
        fields = ("comment", "teacher")


class UpdateTicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("ticket_status",)

class TicketCreateSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    
    class Meta:
        model = Ticket
        fields = ("id", "comment", "ticket_status", "student", "teacher")

class AcademicTitleSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=AcademicTitle.objects.all())]
    )
    abbreviation = serializers.CharField(
        validators=[UniqueValidator(queryset=AcademicTitle.objects.all())]
    )

    class Meta:
        model = AcademicTitle
        fields = ("id", "name", "abbreviation")


class AcademicDegreeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=AcademicDegree.objects.all())]
    )
    abbreviation = serializers.CharField(
        validators=[UniqueValidator(queryset=AcademicDegree.objects.all())]
    )

    class Meta:
        model = AcademicDegree
        fields = ("id", "name", "abbreviation")


class EducationBaseSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=EducationBase.objects.all())]
    )

    class Meta:
        model = EducationBase
        fields = ("id", "name")


class EducationFormSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=EducationForm.objects.all())]
    )

    class Meta:
        model = EducationForm
        fields = ("id", "name")


class EducationLevelSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=EducationLevel.objects.all())]
    )

    class Meta:
        model = EducationLevel
        fields = ("id", "name")


class GraduationSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    graduation_type = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)

    def validate(self, attrs):
        if Graduation.objects.filter(graduation_type=attrs['graduation_type'], year=attrs['year']).exists():
            raise serializers.ValidationError("Такой выпуск уже существует")

        return attrs  

    class Meta:
        model = Graduation
        fields = ("id", "graduation_type", "year")

  


class StudentStatusSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=StudentStatus.objects.all())]
    )

    class Meta:
        model = StudentStatus
        fields = ("id", "name")


class ConsultancyTypeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=ConsultancyType.objects.all())]
    )

    class Meta:
        model = ConsultancyType
        fields = ("id", "name", "is_main")





class ConsultancySerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    consultancy_type = serializers.PrimaryKeyRelatedField(
        queryset=ConsultancyType.objects.all(), required=True
    )
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    comment = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=1024)

    class Meta:
        model = Consultancy
        fields = ("id", "consultancy_type", "teacher", "student", "comment")


class SpecialitySerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    code = serializers.CharField(
        validators=[UniqueValidator(queryset=Speciality.objects.all())]
    )
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Speciality.objects.all())]
    )
    abbreviation = serializers.CharField(
        validators=[UniqueValidator(queryset=Speciality.objects.all())]
    )
    education_level = EducationLevelSerializer(required=True)

    class Meta:
        model = Speciality
        fields = ("id", "code", "name", "abbreviation", "education_level")


class SpecialityCreateSerializer(SpecialitySerializer):
    education_level = serializers.PrimaryKeyRelatedField(
        queryset=EducationLevel.objects.all(), required=True
    )


class StudentGroupSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    speciality = SpecialitySerializer(required=True)
    course = serializers.IntegerField(required=True)
    number = serializers.IntegerField(required=True)
    education_form = EducationFormSerializer(required=True)
    graduation = serializers.PrimaryKeyRelatedField(
        queryset=Graduation.objects.all(), required=True
    )

    class Meta:
        model = StudentGroup
        fields = (
            "id",
            "speciality",
            "course",
            "number",
            "education_form",
            "graduation",
        )
class StudentGroupCreateSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    speciality = serializers.PrimaryKeyRelatedField(
        queryset=Speciality.objects.all(), required=True
    )
    course = serializers.IntegerField(required=True)
    number = serializers.IntegerField(required=True)
    education_form  = serializers.PrimaryKeyRelatedField(
        queryset=EducationForm.objects.all(), required=True
    )
    graduation = serializers.PrimaryKeyRelatedField(
        queryset=Graduation.objects.all(), required=True
    )

    class Meta:
        model = StudentGroup
        fields = (
            "id",
            "speciality",
            "course",
            "number",
            "education_form",
            "graduation",
        )

class ShortStudentSerializer(ShortUserSerializer):
    student_group = StudentGroupSerializer()

    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name", "student_group")


class TicketSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    dt_send = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=True)
    comment = serializers.CharField(required=True, max_length=1024)
    ticket_status = serializers.SerializerMethodField()
    teacher = ShortUserSerializer(required=True)
    student = ShortStudentSerializer(required=True)
    dt_response = serializers.DateTimeField(format="%d.%m.%Y %H:%M", required=False)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "dt_send",
            "comment",
            "ticket_status",
            "teacher",
            "student",
            "dt_response",
        )

    def get_ticket_status(self, obj):
        if obj.ticket_status is None:
            return None

        return dict(
            id=TicketStatusEnum(obj.ticket_status).value,
            name=TicketStatusEnum(obj.ticket_status).descr,
        )


class TimeNormSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    hours = serializers.IntegerField(required=True)
    speciality = SpecialitySerializer(required=True)
    consultancy_type = ConsultancyTypeSerializer(required=True)
    # consultancy_type = serializers.PrimaryKeyRelatedField(
    #     queryset=ConsultancyType.objects.all(), required=True
    # )
    graduation = serializers.PrimaryKeyRelatedField(
        queryset=Graduation.objects.all(), required=True
    )

    class Meta:
        model = TimeNorm
        fields = ("id", "hours", "speciality", "consultancy_type", "graduation")

class TimeNormCreateSerializer(serializers.ModelSerializer):

    
    
    class Meta:
        model = TimeNorm
        fields = ("id", "hours", "speciality", "consultancy_type", "graduation")


class UserSerializer(serializers.ModelSerializer):

    position = PositionSerializer()
    student_group = StudentGroupSerializer(required=False)
    education_level = EducationLevelSerializer(required=False)
    role = serializers.SerializerMethodField()
    education_base = EducationBaseSerializer(required=False)
    academic_title = AcademicTitleSerializer(required=False)
    academic_degree = AcademicDegreeSerializer(required=False)
    student_status = StudentStatusSerializer(required=False)


    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "position",
            "number_student_book",
            "student_group",
            "student_status",
            "education_base",
            "speciality",
            "role",
            "academic_title",
            "academic_degree",
            "education_level",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_role(self, obj):
        if obj.role is None:
            return None

        return dict(id=RoleEnum(obj.role).value, name=RoleEnum(obj.role).descr)

class UserWithOpenPasswordSerializer(UserSerializer):
    password_text = serializers.CharField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = (UserSerializer.Meta.fields+("password_text",))

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True
        )
    
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=6,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

class UserProfileSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "position",
            "number_student_book",
            "student_group",
            "student_status",
            "education_base",
            "speciality",
            "role",
            "academic_title",
            "academic_degree",
            "education_level",
        )


class VkrHoursSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    year = serializers.IntegerField(required=True)
    hours = serializers.IntegerField(required=True)
    teacher = ShortUserSerializer()

    class Meta:
        model = VkrHours
        fields = ("id", "year", "hours", "teacher")

class VkrHoursCreateSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    year = serializers.IntegerField(required=True)
    hours = serializers.IntegerField(required=True)
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )

    class Meta:
        model = VkrHours
        fields = ("id", "year", "hours", "teacher")

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data = dict(
            refresh=str(refresh),
            access=str(refresh.access_token),
            is_superuser=self.user.is_superuser,
            username=self.user.username,
            email=self.user.email,
            first_name=self.user.first_name,
            middle_name=self.user.middle_name,
            last_name=self.user.last_name,
            role_id=RoleEnum(self.user.role).value,
            role_name=RoleEnum(self.user.role).descr,
        )

        return data


class ShortUserWithRoleSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name", "role")


class StudentInGroupSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name", "role")


class ShortStudentWithHoursSerializer(ShortUserWithRoleSerializer):
    hours = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name", "role", "hours")

    def get_hours(self, obj):
        if obj is None:
            return None

        return obj.hours


class GroupWithStudentSerializer(ShortUserWithRoleSerializer):
    group_name = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    students = ShortStudentWithHoursSerializer(many=True)

    class Meta:
        model = StudentGroup
        fields = (
            "id",
            "hours",
            "group_name",
            "students",
        )

    def get_group_name(self, obj):
        if obj is None:
            return None

        return str(obj)

    def get_hours(self, obj):
        if obj is None:
            return None

        return obj.hours


class ShortTeacherWithGroupsSerializer(ShortUserWithRoleSerializer):
    groups = GroupWithStudentSerializer(many=True, source="groups_set")



class TimeNormGraduationSerializer(ShortTeacherWithGroupsSerializer):

    hours_sum = serializers.SerializerMethodField()
    vkr_hours = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "role",
            "groups",
            "hours_sum",
            "vkr_hours"
        )

    def get_hours_sum(self, obj):
        if obj is None:
            return None

        return obj.hours_sum
    
    def get_vkr_hours(self, obj):
        if obj is None:
            return None

        return {
            "id": obj.vkr_hours[1],
            "hours":obj.vkr_hours[0],
            }

class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = ("id", "name")
    
# class ShortStudentWithStatus(ShortUserSerializer):
#     student_status = StudentStatusSerializer()

#     class Meta:
#         model = User
#         fields = (ShortUserSerializer.Meta.fields+("student_status",))

class ShortStudentWithStatusSerializer(serializers.ModelSerializer):
    student_status = StudentStatusSerializer()
    class Meta:
        model = User
        fields = ("id", "first_name", "middle_name", "last_name", "student_status")

class RowInStudentGroupByConsultancySerializer(serializers.Serializer):
    student = ShortStudentWithStatusSerializer()
    teacher = ShortUserSerializer()
    comment = serializers.CharField()
    id = serializers.IntegerField()

class StudentsInGroupByConsultancySerializer(serializers.ModelSerializer):
    hours = serializers.FloatField()
    assigned = RowInStudentGroupByConsultancySerializer(many=True)
    not_assigned = ShortStudentWithStatusSerializer(many=True)

    class Meta:
        model = ConsultancyType
        fields = (
            "id",
            "hours",
            "name",
            "assigned",
            "not_assigned",
            "is_main"
        )
