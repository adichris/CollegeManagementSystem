from django.urls import path
from .views import (
    SemesterCreateView,
    SemesterAcademicYearView,
    SemesterUpdateView,
    PermissionGroupListView,
    PermissionGroupCreate,
    PermissionGroupDetails,
    PermissionDetail,
    AddPermissionTemplateView,
    get_permission_ajax,
    AddMemberToPermissionGroup,
    get_group_members_ajax,
    remove_group_member,
    get_group_member_information,
)


app_name = 'System'
urlpatterns = [
    path('semester/new/', SemesterCreateView.as_view(), name='semester_new'),
    path('semester/change/<str:name>/<int:id>/', SemesterUpdateView.as_view(), name='semester_update'),
    path('semesteracademicyear/', SemesterAcademicYearView.as_view(), name='semester_academic_year'),
    path('permissiongroups/', PermissionGroupListView.as_view(), name='permission_group'),
    path('permissiongroup/add/', PermissionGroupCreate.as_view(), name='permission_group_add'),
    path('permissiongroup/<int:pk>/', PermissionGroupDetails.as_view(), name='permission_group_detail'),
    path('permissiondetail/<int:permission_pk>/', PermissionDetail.as_view(), name='permission_detail'),
    path('addpermission2group/<str:group_name>/<int:group_pk>/', AddPermissionTemplateView.as_view(),
         name='add_permission2group'),
    path('ajaxpermissioncall/<int:permission_pk>/', get_permission_ajax, name='get_permission_ajax'),
    path('ajaxgroupmemberscall/<str:group_name>/', get_group_members_ajax, name='get_group_members_ajax'),
    path('removegroupmember/<str:group_name>/<str:member_identity>/', remove_group_member, name='remove_group_member'),
    path('addmenbertogroup/<str:group_name>/<int:group_pk>/',
         AddMemberToPermissionGroup.as_view(), name='add_member2group'),
    path('staffuserinformation/<str:identity>/<str:group_name>/', get_group_member_information, name='get_user_shortInfo'),
]
