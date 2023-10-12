from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (AcademicDegreeViewSet, AcademicTitleViewSet,
                       ConsultancyTypeViewSet, ConsultancyViewSet,
                       CustomTokenObtainView, EducationBaseViewSet,
                       EducationFormViewSet, EducationLevelViewSet,
                       GetSelfProfileView, GraduationViewSet, PositionViewSet,
                        SpecialityViewSet, StudentGroupViewSet,
                       StudentStatusViewSet, TicketCreateView,
                       TicketStatusUpdate, TicketViewSet, TimeNormViewSet,
                       UserGraduationView, UserViewSet, VkrHoursViewSet)

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"position", PositionViewSet, basename="position")
router.register(r"ticket", TicketViewSet, basename="ticket")
router.register(r"academic_title", AcademicTitleViewSet, basename="academic_title")
router.register(r"academic_degree", AcademicDegreeViewSet, basename="academic_degree")
router.register(r"education_base", EducationBaseViewSet, basename="education_base")
router.register(r"edu_form", EducationFormViewSet, basename="edu_form")
router.register(r"edu_level", EducationLevelViewSet, basename="edu_level")
router.register(r"graduation", GraduationViewSet, basename="graduation")
router.register(r"stud_status", StudentStatusViewSet, basename="stud_status")
router.register(r"consultancy_type", ConsultancyTypeViewSet, basename="consultancy_type")
router.register(r"vkr_hours", VkrHoursViewSet, basename="vkr_hours")
router.register(r"consultancy", ConsultancyViewSet, basename="consultancy")
router.register(r"speciality", SpecialityViewSet, basename="speciality")
router.register(r"student_group", StudentGroupViewSet, basename="student_group")
router.register(r"time_norm", TimeNormViewSet, basename="time_norm")



urlpatterns = [
    path("login/", CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", GetSelfProfileView.as_view()),
    path(
        "user_graduation/<int:graduation_id>",
        UserGraduationView.as_view(),
        name="user_graduation",
    ),
    path("ticket_create/", TicketCreateView.as_view(), name="ticket_create"),
    path(
        "ticket_status_update/<int:ticket_id>",
        TicketStatusUpdate.as_view(),
        name="ticket_status_update",
    ),

]

urlpatterns += router.urls
