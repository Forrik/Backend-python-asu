from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, RoleViewSet, PositionViewSet, TicketViewSet, AcademicTitleViewSet, AcademicDegreeViewSet, EducationBaseViewSet, EduFormViewSet, EduLevelViewSet, GraduationViewSet, StudStatusViewSet, WorkTypeViewSet, VkrHoursViewSet, ConsultancyViewSet, SpecialityViewSet, StudentGroupViewSet, TimeNormViewSet, CustomTokenObtainView, GetSelfProfileView, UserGraduationView, TicketCreateView

router = DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'role', RoleViewSet, basename='role')
router.register(r'position', PositionViewSet, basename='position')
router.register(r'ticket', TicketViewSet, basename='ticket')
router.register(r'academic_title', AcademicTitleViewSet, basename='academic_title')
router.register(r'academic_degree', AcademicDegreeViewSet, basename='academic_degree')
router.register(r'education_base', EducationBaseViewSet, basename='education_base')
router.register(r'edu_form', EduFormViewSet, basename='edu_form')
router.register(r'edu_level', EduLevelViewSet, basename='edu_level')
router.register(r'graduation', GraduationViewSet, basename='graduation')
router.register(r'stud_status', StudStatusViewSet, basename='stud_status')
router.register(r'work_type', WorkTypeViewSet, basename='work_type')
router.register(r'vkr_hours', VkrHoursViewSet, basename='vkr_hours')
router.register(r'consultancy', ConsultancyViewSet, basename='consultancy')
router.register(r'speciality', SpecialityViewSet, basename='speciality')
router.register(r'student_group', StudentGroupViewSet, basename='student_group')
router.register(r'time_norm', TimeNormViewSet, basename='time_norm')



# router.register(r'page', views.PageView, basename='page')


urlpatterns = [
    path('login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', GetSelfProfileView.as_view()),
    path('user_graduation/<int:graduation_id>', UserGraduationView.as_view(), name='user_graduation'),
    path('ticket_create/', TicketCreateView.as_view(), name='ticket_create'),
    # path('profile/', views.GetProfileView.as_view()),
    # path('profile/change_password', views.ChangePasswordView.as_view()),
    # path('search/<str:search>', views.SearchView.as_view()),
    # path('feedback/', views.FeedbackCreateView.as_view()),
    
    # path('page/<int:page_id>/', views.PageView.as_view())
]

urlpatterns += router.urls
